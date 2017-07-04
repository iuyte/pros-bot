#!/usr/bin/python3
import discord
import asyncio
import re
import vegan
from time import gmtime, strftime
from parseAPI import load
from parseAPI import gData as g
from search import *
import embed

with open('../pros_token.txt', 'r') as discord_file:
    DISCORD_TOKEN = discord_file.read().split(";")[0]
print(DISCORD_TOKEN, end=';\n')

prefix = "$"
client = discord.Client()
data = load()


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
            content = " ".join(message.content.split(
                "<@" + str(client.user.id) + ">")).strip()
        if message.channel.is_private:
            content = message.content
        result = ""
        if content.startswith("api "):
            c = content.split(" ")[1].strip()
            tdata = None
            if "vegan" in c:
                em = discord.Embed(
                    title="Vegan Counter", description="How many times Jess has said 'vegan'", color=color)
                em.add_field(name="Total Count",
                             value="**[" + str(vegan.count()) + "]()**")
                await client.send_message(message.channel, embed=em)
            else:
                try:
                    tdata = search(c)[0]
                except:
                    tdata = None
                if tdata == None:
                    result = "Not found"
                else:
                    result = ""
                    await client.send_message(message.channel, embed=embed.api(tdata))
        elif content.startswith("tutorial "):
            c = content[9:].strip()
            await client.send_message(message.channel, embed=embed.tutorial(c))
        elif content.startswith("f "):
            c = content[2:].lower().strip()
            matches = search(c)
            await client.send_message(message.author, embed=embed.found(c, matches))
        elif content.lower().strip().startswith("help"):
            em = discord.Embed(
                title="Help", description="About the available commands", color=color)
            em.add_field(
                name="`$`", value="Use the prefix `$` or mention me at the beginning of a message that has a command.")
            em.add_field(
                name="`api`", value="Use the command `api <function/macro>` to get information on a function or macro.")
            em.add_field(
                name="`tutorial`", value="Use the command `tutorial <tutorial> to get a link to a PROS tutorial.")
            em.add_field(
                name="`f`", value="Use `f <regex>` to search the API using a regex for specific functions/macros.")
            em.add_field(
                name="help", value="Display this (hopefully helpful) message")
            await client.send_message(message.author, embed=em)
        if result != None and result != "":
            await client.send_message(message.channel, embed=discord.Embed(title=result, color=embed.color))
    elif str(message.author.id) == "168643881066299392":
        for i in range(message.content.lower().count("vegan")):
            vegan.add()

client.run(DISCORD_TOKEN)
