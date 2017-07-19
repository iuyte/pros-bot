import umsgpack as pickle
import jsonpickle

def Data(typec, group, name, description, params, extra="", access="", returns=""):
        link = ""
        if typec.lower() == "function":
                link = "https://pros.cs.purdue.edu/api/#" + name.split("(")[0]
        elif typec.lower() == "macro":
                link = "https://pros.cs.purdue.edu/api/#define-"
                link += "-".join(name.split("(")[0].split("_")).lower() + "-" + extra
        return {"typec": typec, "group": group, "name": name, "description": description, "params": params, "extra": extra, "access": access, "returns": returns, "link": link}

def parse(data):
        out = []
        line = 34
        group = ""
        cdef = ""
        params = []
        returns = ""
        types = ["typedef void *", "TaskHandle", "bool", "unsigned long", "unsigned int", "Encoder", "Gyro", "Ultrasonic", "typedef", "FILE*", "char*", "char", "FILE *", "FILE", "size_t", "long int", "void *", "void*", "Semaphore", "Mutex", "void", "int", "PROS_FILE*", "PROS_FILE *", "PROS_FILE"]
        skip = ["#if", "#end", "}", "\n"]
        while line < len(data):
            try:
                bskip = False
                for s in skip:
                    if data[line].startswith(s):
                        bskip = True
                if bskip:
                    line += 1
                    continue
                if data[line].startswith("// -"):
                        group = ""
                        for character in data[line]:
                                if character not in "/-":
                                        group += character
                        group = group.strip().title()
                        line += 1
                        continue
                if data[line].startswith("/**"):
                        line += 1
                        cdef = ""
                        params = []
                        lastp = False
                        lastr = False
                        while not data[line].startswith(" */"):
                                if data[line][3:].startswith("@param"):
                                        params.append(data[line][10:].strip().replace("<code>", "`").replace("</code>", "`"))
                                        lastp = True
                                elif data[line][3:].startswith("@return"):
                                        returns = data[line][11:].strip().replace("<code>", "`").replace("</code>", "`")
                                        lastr = True
                                elif lastr:
                                        returns += " " + data[line][3:].replace("<code>", "`").replace("</code>", "`")
                                elif lastp:
                                        params[-1] += " " + data[line][3:].replace("<code>", "`").replace("</code>", "`")
                                else:
                                        cdef += data[line][3:] + " "
                                line += 1
                        cdef = cdef.strip().replace("<code>", "`").replace("</code>", "`").replace("* \\c", "\n   "+u"\u2022 ")
                        returns = returns.strip()
                        line += 1
                        continue
                if data[line].startswith("#define "):
                        typec = "Macro"
                        vi = data[line].split(" ")
                        name = vi[1].strip()
                        value = vi[2].strip()
                        out.append(Data(typec, group, name, cdef, params, value, name.lower()))
                        cdef = ""
                        params = ""
                        line += 1
                        continue
                typec = "Function"
                rtype = ""
                for t in types:
                        if data[line].lower().startswith(t.lower()):
                                rtype = t
                                break
                name = data[line][(len(rtype) + 1):-1].strip()
                while data[line].strip()[-1] is not ";":
                    line += 1
                    name += " " + data[line].strip()
                access = name.split("(")[0].lower().strip()
                if rtype == "" or cdef == "" or name == "" or access.strip() in types or access.startswith("int "):
                    line += 1
                    continue
                out.append(Data(typec, group, name, cdef, params, rtype, access, returns))
                cdef = ""
                params = []
                returns = ""
                line += 1
            except:
                line += 1
                print("Error on line ", line)
        return out

def save():
        data = []
        with open("API.h", mode="r") as theta:
                data = parse(theta.read().split("\n"))
        with open("api.p", mode="wb") as thata:
                pickle.dump(data, thata)
        with open("api.json", mode="w") as jsonf:
                jsonf.write(jsonpickle.encode(data, unpicklable=False));

def load():
        data = []
        with open("api.p", mode="rb") as p:
                data = pickle.load(p)
        return data

def gData(data, key):
    key = bytes(key, 'utf-8')
    if type(data[key]) is bytes:
        return data[key].decode('utf-8')
    return data[key]

if __name__ == "__main__":
        save()
        print("Saved.")
