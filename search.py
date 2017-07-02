import re
from parseAPI import load

def reContains(regex, string):
    return bool(re.search(regex, string))

def search(regex):
    matches = []
    regex = regex.lower()
    r = re.compile(eval("r'" + regex + "'"))
    data = load()
    for d in data:
        if len(d["name"]) > 1 and len(d["description"]) > 1:
            if bool(r.search(d["access"].strip())) or regex == d["access"].strip():
                matches.append(d)
    return matches

