from parseAPI import gData as g
from discord import Embed as Fembed
from discord import Color as Fcolor

class Embed():
    def __init__(self, json):
        self.json = json

    def to_dict(self):
        return self.json


color = 15452014

api_template_main = \
    """
{
color: {color},
title: "{group}",
description: "**[PROS API Reference](https://pros.cs.purdue.edu/api/#fopen)**",
fields: [
{
name: "Declaration",
value: "```Cpp\
{declaration}\
```",
},
{
name: "Description",
value: "{description}",
inline: true,
},
{more_fields}
]
}
"""

api_template_parameters = \
    """
{
name: "Parameters",
value: "{parameterS}",
},
"""

api_template_returns = \
    """
{
name: "Returns",
value: "{returns}",
},
"""

tutorial_template = \
    """
{
color: {},
title: "PROS Tutorials",
description: "**[{}](https://pros.cs.purdue.edu/tutorials/{})**",
fields = [],
}
"""

f_template_main = \
    """
{
color: {color},
title: "Matches for `{regex}`",
fields: [
{fields}
],
}
"""

f_template_match = \
    """
{
name: "{name}",
value: "{description} {link}",
inline: true,
},
"""


def api(tdata):
    group = g(tdata, "group")
    link = "**[PROS API Reference](" + g(tdata, "link") + ")**"
    declaration = ""
    more = ""
    params = ""
    if len(g(tdata, "params")) > 0:
        for param in g(tdata, "params"):
            paramm = param.decode('utf-8').split(" ")
            params += "`" + paramm.pop(0) + "`: " + \
                " ".join(paramm).strip() + "\n"
    params = params.replace("\n", "\n\\")
    if g(tdata, "typec").lower() == "function":
        declaration = "```Cpp\n" + \
            g(tdata, "extra") + " " + g(tdata, "name") + "\n```"
    elif g(tdata, "typec").lower() == "macro":
        declaration = "```Cpp\n#define " + \
            g(tdata, "name") + " " + g(tdata, "extra") + "\n```"
    if len(g(tdata, "description")) > 1024:
        tdata[bytes("description", 'utf-8')] = g(tdata,
                                                 "description")[:1018] + " . . ."
    description = g(tdata, "description")
    if len(g(tdata, "params")) > 0:
        more += api_template_parameters.format(parameterS=params)
    if g(tdata, "returns") is not "":
        more += api_template_returns.format(returns=returns)
    result = api_template_main.format(
        color=color, group=group, declaration=declaration, description=description, more_fields=more)
    return Embed(result)

def tutorial(name):
    return Embed(tutorial_template.format(color, name.title(), name)

def found(regex, matches):
    fields = ""
    result = ""
    for m in range(len(matches)):
        fname = g(matches[m], "extra") + " " + g(matches[m], "name")
        if g(matches[m], "typec").lower() == "macro":
            fname = "#define " + g(matches[m], "name") + " " + g(matches[m], "extra")
        flink = "*[" + u"\u279A" + "](" + g(matches[m], "link") + ")*"
        fdes = ""
        if len(g(matches[m], "description")) <= 175:
            fdes = g(matches[m], "description")
        else:
            fdes = g(matches[m], "description")[:169] + " . . ."
        fields += f_template_match.format(name=fname, description=fdes, link=flink)
    if len(matches) is 0:
        result = Fembed(title="Matches for `{}`".format(regex), color=Fcolor(color))
        result.add_field(name="None", value="No matches for `" + regex + "` found.")
    else:
        result = Embed(color=color, regex=regex, fields=fields)
    return result
