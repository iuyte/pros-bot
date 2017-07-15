#!/usr/bin/python3
import discord, asyncio, re, vegan, griffin
from time import gmtime, strftime, time as Epoch
from random import randint, seed
from parseAPI import load
from parseAPI import gData as g
from search import *

with open('../pros_token.txt', 'r') as discord_file:
    DISCORD_TOKEN = discord_file.read().split(";")[0]
print(DISCORD_TOKEN, end=';\n')

prefix = "$"
client = discord.Client()
color = discord.Color(15452014)
base = "https://pros.cs.purdue.edu/"
tutorial = base + "tutorials/"
api = base + "api/#"
data = load()

authorizedList = ["pros", "developers", "admins"]

def epoch():
    seed(str(float(Epoch())))
    return str(float(Epoch())).ljust(20)

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------\n')
    await client.send_message(client.get_channel("315552571823489024"), "Connected at " + strftime("%Y-%m-%d %H:%M:%S", gmtime()))

@client.event
async def on_message(message):
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
        ment = message.mentions
        o = message.channel
        try:
            if len([x for x in range(len(message.author.roles)) if message.author.roles[x].name.lower() in authorizedList]) > 0:
                if len(ment) > 0 and client.user not in ment:
                    o = ment[0]
                elif len(ment) > 1 and client.user in ment:
                    o = ment[1]
        except:
            o = message.channel
        if content.startswith("api "):
            ment = message.mentions
            o = message.channel
            if len(ment) > 0 and client.user not in ment:
                o = ment[0]
            elif len(ment) > 1 and client.user in ment:
                o = ment[1]
            c = content.split(" ")[1].strip()
            tdata = None
            if "vegan" in c:
                em = discord.Embed(title="Vegan Counter", description="How many times Jess has said 'vegan'", color=color)
                em.add_field(name="Total Count", value="**[" + str(vegan.count()) + "]()**")
                await client.send_message(o, embed=em)
            else:
                try:
                    tdata = search(c)[0]
                except:
                    tdata = None
                if tdata == None:
                    result = "Not found"
                else:
                    result = ""
                    link = "**[PROS API Reference](" + g(tdata, "link") + ")**"
                    params = ""
                    if len(g(tdata, "params")) > 0:
                        for param in g(tdata, "params"):
                            paramm = param.decode('utf-8').split(" ")
                            params += "`" + paramm.pop(0) + "`: " + " ".join(paramm).strip() + "\n"
                    em = discord.Embed(title=g(tdata, "group"), description=link, color=color)
                    if g(tdata, "typec").lower() == "function":
                        em.add_field(name="Declaration", value="```Cpp\n" + g(tdata, "extra") + " " + g(tdata, "name") + "\n```")
                        if len(g(tdata, "description")) >  1024:
                            tdata[bytes("description", 'utf-8')] = g(tdata, "description")[:1018] + " . . ."
                        em.add_field(name="Description", value=g(tdata, "description"))
                        if len(g(tdata, "params")) > 0:
                            em.add_field(name="Parameters", value=params)
                        if g(tdata, "returns") is not "":
                            em.add_field(name="Returns", value = g(tdata, "returns"))
                    elif g(tdata, "typec").lower() == "macro":
                        em.add_field(name="Declaration", value="```Cpp\n#define " + g(tdata, "name") + " " + g(tdata, "extra") + "\n```")
                        em.add_field(name="Description", value=g(tdata, "description"))
                    if em != None:
                        await client.send_message(o, embed=em)
        elif content.startswith("tutorial "):
            c = content[9:].strip()
            result = tutorial + c
        elif content.startswith("f "):
            if o is message.channel:
                o = message.author
            c = content[2:].lower().strip()
            matches = search(c)
            em = discord.Embed(title="Matches for `" + c + "`", color=color)
            for m in range(len(matches)):
                fname = "`" + g(matches[m], "extra") + " " + g(matches[m], "name") + "`"
                if g(matches[m], "typec").lower() == "macro":
                    fname = "`#define " + g(matches[m], "name") + " " + g(matches[m], "extra") + "`"
                flink = "*[" +  u"\u279A" + "](" + g(matches[m], "link") + ")*"
                fdes = ""
                if len(g(matches[m], "description")) <= 175:
                    fdes = g(matches[m], "description")
                else:
                    fdes = g(matches[m], "description")[:169] + " . . ."
                em.add_field(name=fname, value=fdes + " " + flink, inline=True)
            if len(matches) is 0:
                em.add_field(name="None", value="No matches for " + c + " found.")
            await client.send_message(o, embed=em)
        elif content.lower().startswith("epoch") or content.lower().startswith("time") or content.lower().startswith("unix"):
            em = discord.Embed(title="Current Time", description=epoch(), color=discord.Color(randint(0, 16777215)))
            await client.send_message(o, embed=em)
        elif content.lower().strip().startswith("help"):
            if o is message.channel:
                o = message.author
            em = discord.Embed(title="Help", description="About the available commands", color=color)
            em.add_field(name="`$`", value="Use the prefix `$` or mention me at the beginning of a message that has a command.")
            em.add_field(name="`api`", value="Use the command `api <function/macro>` to get information on a function or macro.")
            em.add_field(name="`tutorial`", value="Use the command `tutorial <tutorial> to get a link to a PROS tutorial.")
            em.add_field(name="`f`", value="Use `f <regex>` to search the API using a regex for specific functions/macros.")
            em.add_field(name="`<letter>ing`", value="<letter>ong! `<epoch difference in time it took to send>`")
            em.add_field(name="help", value="Display this (hopefully helpful) message")
            await client.send_message(o, embed=em)
        elif re.match(".*ing", content.lower().strip(" !.,?;'\"")):
            title = content.lower().strip(" !.,?;'\"").replace("ing", "ong").title()
            epoch()
            tlast = float(Epoch())
            msg = await client.send_message(message.channel, embed=discord.Embed(title=title))
            def check(tmsg):
                return msg.id is tmsg.id
            tdif = str(float(Epoch()) - tlast)
            await client.edit_message(msg, new_content="", embed=discord.Embed(title=title, description=tdif, color=discord.Color(randint(0, 16777215))))
        if result != None and result != "":
            em = discord.Embed(color=color, description="**" + result + "**")
            await client.send_message(o, embed=em)
    elif str(message.author.id) == "168643881066299392":
        for i in range(message.content.lower().count("vegan")):
            vegan.add()

@client.event
async def on_message_delete(message):
    epoch()
    if str(message.author.id).startswith("126080531535364096"):
        await client.send_message(message.channel, embed=griffin.repost(message.content), color=discord.Color(randint(0, 16777215)))

client.run(DISCORD_TOKEN)
