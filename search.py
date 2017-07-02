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
        if len(d[b"name"]) > 1 and len(d[b"description"]) > 1:
            if bool(r.search(d[b"access"].strip())) or regex == d[b"access"].strip():
                matches.append(d)
    return matches
