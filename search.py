import re
from parseAPI import load
from parseAPI import gData as g

def re_contains(regex, string):
    return bool(re.search(regex, string))


def search(regex):
    matches = []
    regex = regex.lower()
    r = re.compile(eval("r'" + regex + "'"))
    data = load()
    for d in data:
        if len(g(d, "name")) > 1 and len(g(d, "description")) > 1:
            if bool(r.search(g(d, "access").strip())) or regex == g(d, "access").strip():
                matches.append(d)
                if regex.strip() == g(d, "access").strip():
                    return [d]
    return matches
