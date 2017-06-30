import discord
import asyncio
import re
import vegan
from time import gmtime, strftime
from parseAPI import Data, load
from unidecode import unidecode
from search import *

with open('../pros_token.txt', 'r') as discord_file:
    DISCORD_TOKEN = discord_file.read()[:-2]
print(DISCORD_TOKEN, end=';\n')

prefix = "$"
client = discord.Client()
color = discord.Color(15452014)
base = "https://pros.cs.purdue.edu/"
tutorial = base + "tutorials/"
api = base + "api/#"
data = load()

@client.event
@asyncio.coroutine
def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------\n')
    yield from client.send_message(client.get_channel("315552571823489024"), "Connected at " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))

@client.event
@asyncio.coroutine
def on_message(message):
    global data, prefix, client, base, tutorial, api, foo
    if len(message.content) <= 0:
        return
    content = message.content[1:]
    if message.content[0] == prefix or client.user in message.mentions or message.channel.is_private:
        if client.user in message.mentions:
            content = " ".join(message.content.split("<@" + str(client.user.id) + ">")).strip()
        if message.channel.is_private:
            content = message.content
        result = ""
        if content.startswith("api "):
            c = content.split(" ")[1].strip()
            tdata = None
            if "vegan" in c:
                em = discord.Embed(title="Vegan Counter", description="How many times Jess has said 'vegan'", color=color)
                em.add_field(name="Total Count", value="**[" + str(vegan.count()) + "]()**")
                yield from client.send_message(message.channel, embed=em)
            else:
                try:
                    tdata = search(c)[0]
                except:
                    tdata = None
                if tdata == None:
                    result = "Not found"
                else:
                    result = ""
                    link = "**[PROS API Reference](" + tdata.link + ")**"
                    params = ""
                    if len(tdata.params) > 0:
                        for param in tdata.params:
                            paramm = param.split(" ")
                            params += "`" + paramm.pop(0) + "`: " + " ".join(paramm).strip() + "\n"
                    em = discord.Embed(title=tdata.group, description=link, color=color)
                    if tdata.typec.lower() == "function":
                        em.add_field(name="Declaration", value="```Cpp\n" + tdata.extra + " " + tdata.name + "\n```")
                        em.add_field(name="Description", value=tdata.description)
                        if len(tdata.params) > 0:
                            em.add_field(name="Parameters", value=params)
                        if tdata.returns is not "":
                            em.add_field(name="Returns", value = tdata.returns)
                    elif tdata.typec.lower() == "macro":
                        em.add_field(name="Declaration", value="```Cpp\n#define " + tdata.name + " " + tdata.extra + "\n```")
                        em.add_field(name="Description", value=tdata.description)
                    if em != None:
                        yield from client.send_message(message.channel, embed=em)
        elif content.startswith("tutorial "):
            c = content[9:].strip()
            result = "<" + tutorial + c + ">"
        elif content.startswith("f "):
            c = content[2:].lower().strip()
            matches = search(c)
            em = discord.Embed(title="Matches for `" + c + "`", color=color)
            for m in range(len(matches)):
                fname = "`" + matches[m].extra + " " + matches[m].name + "`"
                if matches[m].typec.lower() == "macro":
                    fname = "`#define " + matches[m].name + " " + matches[m].extra + "`"
                flink = "*[" +  u"\u279A" + "](" + matches[m].link + ")*"
                fdes = ""
                if len(matches[m].description) <= 175:
                    fdes = matches[m].description
                else:
                    fdes = matches[m].description[:169] + " . . ."
                em.add_field(name=fname, value=fdes + " " + flink, inline=True)
            if len(matches) is 0:
                em.add_field(name="None", value="No matches for " + c + " found.")
            yield from client.send_message(message.author, embed=em)
        elif content.lower().strip().startswith("help"):
            em = discord.Embed(title="Help", description="About the available commands", color=color)
            em.add_field(name="`$`", value="Use the prefix `$` or mention me at the beginning of a message that has a command.")
            em.add_field(name="`api`", value="Use the command `api <function/macro>` to get information on a function or macro.")
            em.add_field(name="`tutorial`", value="Use the command `tutorial <tutorial> to get a link to a PROS tutorial.")
            em.add_field(name="`f`", value="Use `f <regex>` to search the API using a regex for specific functions/macros.")
            em.add_field(name="help", value="Display this (hopefully helpful) message")
            yield from client.send_message(message.author, embed=em)
        if result != None and result != "":
            yield from client.send_message(message.channel, result)
    elif str(message.author.id) == "168643881066299392":
        for i in range(message.content.lower().count("vegan")):
            vegan.add()
    data = load()

client.run(DISCORD_TOKEN)
