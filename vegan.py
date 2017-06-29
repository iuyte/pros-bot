def count():
    with open("vegan.txt", mode="r") as cf:
        return int(cf.read())

def add():
    c = str((count() + 1))
    with open("vegan.txt", mode="w") as cef:
        cef.write(c)

