import pickle

class Data:
        """The data of an API reference"""

        typec = ''
        group = ''
        name = ''
        description = ''
        params = []
        extra = None
        access = ""
        returns = ""
        link = ""
        
        def __init__(self, typec, group, name, description, params, extra=None, access="", returns=""):
                self.typec = typec
                self.group = group
                self.name = name
                self.description = description
                self.params = params
                self.returns = returns
                self.extra = extra
                self.access = access
                if typec.lower() == "function":
                        self.link = "https://pros.cs.purdue.edu/api/#" + name.split("(")[0]
                elif typec.lower() == "macro":
                        self.link = "https://pros.cs.purdue.edu/api/#define-"
                        self.link += "-".join(self.name.split("(")[0].split("_")).lower() + "-" + self.extra

def parse(data):
        out = []
        line = 34
        group = ""
        cdef = ""
        params = []
        returns = ""
        types = ["int", "TaskHandle", "void", "bool", "unsigned long", "unsigned int", "Encoder", "Gyro", "Ultrasonic", "typedef"]
        while line < len(data):
            try:
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
                                        params.append(data[line][10:].strip())
                                        lastp = True
                                elif data[line][3:].startswith("@return"):
                                        returns = data[line][11:].strip()
                                        lastr = True
                                elif lastr:
                                        returns += " " + data[line][3:]
                                elif lastp:
                                        params[-1] += " " + data[line][3:]
                                else:
                                        cdef += data[line][3:] + " "
                                line += 1
                        cdef.strip()
                        line += 1
                        continue
                if data[line].startswith("#define "):
                        typec = "Macro"
                        vi = data[line].split(" ")
                        name = vi[1]
                        value = vi[2]
                        out.append(Data(typec, group, name, cdef, params, value, name.lower()))
                        line += 1
                        continue
                typec = "Function"
                rtype = ""
                for t in types:
                        if data[line].startswith(t):
                                rtype = t
                name = data[line][(len(rtype) + 1):-1]
                access = name.split("(")[0].lower()
                out.append(Data(typec, group, name, cdef, params, rtype, access, returns))
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

def load():
        data = []
        with open("api.p", mode="rb") as p:
                data = pickle.load(p)
        return data

if __name__ == "__main__":
        save()
        print("Saved.")

