#!/usr/bin/python3.6
from random import randint, seed
from time import gmtime, strftime, time as Epoch

import discord
import griffin
import requests
import vegan

from search import *

with open('../pros_token.txt', 'r') as discord_file:
    DISCORD_TOKEN = discord_file.read().split(";")[0]
print(DISCORD_TOKEN, ";")

prefix = "$"
client = discord.Client()
color = discord.Color(15452014)
base = "https://pros.cs.purdue.edu/cortex/"
tutorial = base + "tutorials/"
api = base + "api/#"
data = load()
lastMessage = None

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
    await client.send_message(client.get_channel("315552571823489024"),
                              f"Connected at {strftime('%Y-%m-%d %H:%M:%S', gmtime())}")


async def handle_message(message, edited=False):
    global data, prefix, client, base, tutorial, api
    if not edited:
        global lastMessage
    if len(message.content) <= 0:
        return
    content = message.content[1:]
    if message.content[0] == prefix or client.user in message.mentions or message.channel.is_private:
        if client.user in message.mentions:
            content = " ".join(message.content.split(f"<@{client.user.id}>")).strip()
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
                em = discord.Embed(title="Vegan Counter", description="How many times Jess has said 'vegan'",
                                   color=color)
                em.add_field(name="Total Count", value=f"**[{vegan.count()}]()**")
                if edited:
                    await client.edit_message(lastMessage, embed=em)
                else:
                    lastMessage = await client.send_message(o, embed=em)
            else:
                try:
                    tdata = search(c)[0]
                except:
                    tdata = None
                if tdata is None:
                    result = "Not found"
                else:
                    result = ""
                    link = f"**[PROS API Reference]({g(tdata, 'link')})**"
                    params = ""
                    if len(g(tdata, "params")) > 0:
                        for param in g(tdata, "params"):
                            p = param.decode("utf-8").split(" ")
                            params += f"`{p.pop(0)}`: {' '.join(p).strip()}\n"
                    em = discord.Embed(title=g(tdata, "group"), description=link, color=color)
                    if g(tdata, "typec").lower() == "function":
                        em.add_field(name="Declaration", value=f"```Cpp\n{g(tdata, 'extra')} {g(tdata, 'name')}\n```")
                        if len(g(tdata, "description")) > 1024:
                            tdata[bytes("description", 'utf-8')] = g(tdata, "description")[:1018] + " . . ."
                        em.add_field(name="Description", value=g(tdata, "description"))
                        if len(g(tdata, "params")) > 0:
                            em.add_field(name="Parameters", value=params)
                        if g(tdata, "returns") is not "":
                            em.add_field(name="Returns", value=g(tdata, "returns"))
                    elif g(tdata, "typec").lower() == "macro":
                        em.add_field(name="Declaration",
                                     value=f"```Cpp\n#define {g(tdata, 'name')} {g(tdata, 'extra')}\n```")
                        em.add_field(name="Description", value=g(tdata, "description"))
                    if em is not None:
                        if edited:
                            await client.edit_message(lastMessage, embed=em)
                        else:
                            lastMessage = await client.send_message(o, embed=em)
        elif content.startswith("tutorial "):
            c = content[9:].strip()
            url = tutorial + c
            if requests.get(url).status_code == 404:
                result = "Tutorial not found"
            else:
                result = url
        elif content.startswith("f "):
            if o is message.channel:
                o = message.author
            c = content[2:].lower().strip()
            matches = search(c)
            em = discord.Embed(title=f"Matches for `{c}`", color=color)
            for m in range(len(matches)):
                fname = f"`{g(matches[m], 'extra')} {g(matches[m], 'name')}`"
                if g(matches[m], "typec").lower() == "macro":
                    fname = f"`#define {g(matches[m], 'name')} {g(matches[m], 'extra')}`"
                flink = "*[{}]({})*".format("\u279A", g(matches[m], "link"))
                fdes = ""
                if len(g(matches[m], "description")) <= 175:
                    fdes = g(matches[m], "description")
                else:
                    fdes = f"{g(matches[m], 'description')[:169]} . . ."
                em.add_field(name=fname, value=f"{fdes} {flink}", inline=True)
            if len(matches) is 0:
                em.add_field(name="None", value=f"No matches for {c} found.")
            if edited:
                await client.edit_message(lastMessage, embed=em)
            else:
                lastMessage = await client.send_message(o, embed=em)
        elif content.lower().startswith("epoch") or content.lower().startswith("time")\
                or content.lower().startswith("unix"):
            em = discord.Embed(title="Current Time", description=epoch(), color=discord.Color(randint(0, 16777215)))
            if edited:
                await client.edit_message(lastMessage, embed=em)
            else:
                lastMessage = await client.send_message(o, embed=em)
        elif content.lower().strip().startswith("help"):
            if o is message.channel:
                o = message.author
            em = discord.Embed(title="Help", description="About the available commands", color=color)
            em.add_field(name="`$`",
                         value="Use the prefix `$` or mention me at the beginning of a message that has a command.")
            em.add_field(name="`api`",
                         value="Use the command `api <function/macro>` to get information on a function or macro.")
            em.add_field(name="`tutorial`",
                         value="Use the command `tutorial <tutorial> to get a link to a PROS tutorial.")
            em.add_field(name="`f`", value="Use `f <regex>` to search the API using a regex for specific "
                                           "functions/macros.")
            em.add_field(name="`<letter>ing`", value="<letter>ong! `<epoch difference in time it took to send>`")
            em.add_field(name="help", value="Display this (hopefully helpful) message")
            if edited:
                await client.edit_message(lastMessage, embed=em)
            else:
                lastMessage = await client.send_message(o, embed=em)
        elif re.match("ping.*", content.lower().strip(" !.,?;'\"")) or re.match("pong.*", content.lower().strip(" !.,?;'\"")):
            title = content.lower().strip(" !.,?;'\"").replace("ing", "fefrfgtrhy78383938228").replace("ong", "ing").replace("fefrfgtrhy78383938228", "ong").title() + "!"
            epoch()
            tlast = float(Epoch())
            if edited:
                msg = await client.edit_message(lastMessage, embed=discord.Embed(title=title))
            else:
                msg = await client.send_message(message.channel, embed=discord.Embed(title=title))
            tdif = str(float(Epoch()) - tlast)
            if edited:
                await client.edit_message(lastMessage,
                                          embed=discord.Embed(title=title, description=tdif,
                                                              color=discord.Color(randint(0, 1677215))))
            else:
                lastMessage = await client.edit_message(msg, new_content="",
                                                        embed=discord.Embed(title=title, description=tdif,
                                                                            color=discord.Color(randint(0, 16777215))))
        elif "creator" in content and "not" not in content:
            result = "<@262949175765762050>"
        if result is not None and result != "":
            em = discord.Embed(color=color, description="**" + result + "**")
            if edited:
                await client.edit_message(lastMessage, embed=em)
            else:
                lastMessage = await client.send_message(o, embed=em)
    elif not edited and str(message.author.id) == "168643881066299392":
        for i in range(message.content.lower().count("vegan")):
            vegan.add()


@client.event
async def on_message(message):
    await handle_message(message)


@client.event
async def on_message_delete(message):
    epoch()
    if "griffin" in message.author.nick.lower() and "burn" in message.author.nick.lower() and False:
        lastMessage = await client.send_message(message.channel, embed=griffin.repost(message.content, message.timestamp))


@client.event
async def on_message_edit(before, message):
    await handle_message(message, edited=True)


client.run(DISCORD_TOKEN)
