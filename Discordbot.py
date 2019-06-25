#!/usr/bin/python3

#To run this code
#Python 3.6 64bit or higher is required.
#For required modules. Check Requirements.txt

"""
========================
Modules is placed here!
========================
"""

#import discord library
import discord
#Imports commands
from discord.ext import commands
from discord.ext.commands import has_permissions

#This is required to fetch the nuke codes or other files from urls
import requests
#Allows us to read json files
import json
import sqlite3

from os import listdir
from os.path import isfile, join

"""
===========
Prep files
===========
"""

#opens token.json file on disk to be read. You will need to edit the token file for your own use.
with open("token.json") as json_file:
        #makes the name "data" a reference to the json file.
        data = json.load(json_file)

#Making a new function to get the prefix
def get_prefix(client, message):
    try:
        #connect to database
        conn = sqlite3.connect("databases/ServerConfigs.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        #Check if guild is in database
        c.execute("SELECT * FROM prefixes WHERE GuildID LIKE ?", ('{}'.format(message.guild.id),))
        response = c.fetchone()
        #if guild exists. Respond with guild prefix
        #will need to make a command to change prefix
        if response:
            prefi = []
            prefi.append(response["prefix"])
            prefix = prefi
        else:
            prefix = ">"
        conn.close()
    except:
        prefix = ">"

    if not message.guild:
        return commands.when_mentioned_or(*prefix)(client, message)

    # Allow users to @mention the bot instead of using a prefix when using a command. Also optional
    # Do `return prefixes` if u don't want to allow mentions instead of prefix.
    return commands.when_mentioned_or(*prefix)(client, message)

#Makes "token" a reference to the json file's value token
token = data["token"]

#This is the bot prefix. All "Async def usercommand():" will always check if user has used the prefix
client = commands.Bot(
    command_prefix=get_prefix,
    status=discord.Status.idle,
    activity=discord.Game(name="Booting..."),
    case_insensitive=True
    )

#Disabling the standard help function in discord to make our on in a embed later.
client.remove_command("help")

"""
=================
Functions checks
=================
"""

#defines the fuction is the user the owner.
def is_owner():
    #if the message from the user = his user ID then the user is owner
    def predicate(ctx):
        #For your own use. Remove the existing ID and replace it with your own User ID
        return ctx.message.author.id == 189490137762103298
    return commands.check(predicate)

"""
============================
Login proccedure for the bot
============================
"""

#will print when the bot has connected to the server
@client.event
async def on_ready():
    #prints that the bot is ready with its username, id,  version & number of guilds.
    print(f"\nBot is ready\nLogged in as\nBot's name: {client.user.name}\nBot id: {client.user.id}\nDiscord.py version: {discord.__version__}\n------\nBot is serving: {str(len(client.guilds))} guilds.")
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name="The Strip"))

#starts a client.event
@client.event
#Defines a fuction when a message is sent
async def on_message(message):

    #Keeps the command in mind when event is running to prevent commands from not working
    await client.process_commands(message)

@client.event
async def on_guild_join(guild):
    #await client.change_presence(status=discord.Status.online, activity=discord.Game(name="The Strip"))
    print(f"Bot is serving: {str(len(client.guilds))} guilds.")

"""
===========================
extension files loads here!
===========================
"""

#Here is all the extensions in the discord client. If a new extension is added. Add it here.
cogs_dir = "cogs"
admin_dir = "admin"

if __name__ == "__main__":
    for load_dir in [cogs_dir,admin_dir]:
        for extension in [f.replace('.py', '') for f in listdir(load_dir) if isfile(join(load_dir, f))]:
            try:
                client.load_extension(load_dir + "." + extension)
                print('loaded extension {}'.format(extension))
            except Exception as e:
                exc = '{}: {}'.format(type(e).__name__, e)
                print('Failed to load extension {}\n{}'.format(extension, exc))


"""
==================
Cogs / Extensions
==================
"""

#client starts a command group
@client.group(hidden=True)
#checks to see if the user is the owner of the bot
@is_owner()
#Defines a function when the owner uses the reload command
async def reload(ctx):
    print(f"A reload command was executed in \"{ctx.guild.name}\" ")
    #if no sub command in group is run. Run code.
    if ctx.invoked_subcommand is None:
        #Reloads a extension.
        if __name__ == "__main__":
            tempcoglist = []
            #Will loop through the startup_extensions list
            for extension in [f.replace('.py', '') for f in listdir(cogs_dir) if isfile(join(cogs_dir, f))]:
                #Code will try to unload the extensions & reload the extensions
                try:
                    #unloads extension
                    cogToUnload = client.get_cog(extension)
                    if cogToUnload:
                        client.unload_extension(cogs_dir + "." + extension)
                    #loads extension
                    client.load_extension(cogs_dir + "." + extension)
                    tempcoglist.append(extension)
                #If extension fails to load. Execption error
                except Exception as e:
                    #Bot will shot itself
                    await ctx.channel.send('\N{PISTOL}')
                    #Bot replys with the problem
                    await ctx.channel.send('{}: {}'.format(type(e).__name__, e))
            #Prints out each extension it reloads
            await ctx.send(f"Reloaded the following cogs:\n{tempcoglist}")

#command recognizes its in a group.
#will not run without main command being specified.
@reload.command(hidden=True)
#checks to see if the user is the owner of the bot
@is_owner()
#Defines a function when the owner uses the reload command
async def admin(ctx):
    print(f"A reload command was executed in \"{ctx.guild.name}\" ")
    #Reloads a extension.
    if __name__ == "__main__":
        tempcoglist = []
        #Will loop through the startup_extensions list
        for extension in [f.replace('.py', '') for f in listdir(admin_dir) if isfile(join(admin_dir, f))]:
            #Code will try to unload the extensions & reload the extensions
            try:
                #unloads extension
                cogToUnload = client.get_cog(extension)
                if cogToUnload:
                    client.unload_extension(admin_dir + "." + extension)
                #loads extension
                client.load_extension(admin_dir + "." + extension)
                tempcoglist.append(extension)
            #If extension fails to load. Execption error
            except Exception as e:
                #Bot will shot itself
                await ctx.channel.send('\N{PISTOL}')
                #Bot replys with the problem
                await ctx.channel.send('{}: {}'.format(type(e).__name__, e))
        #Prints out each extension it reloads
        await ctx.send(f"Reloaded the following cogs:\n{tempcoglist}")

"""
============================
Logs the bot out of discord
============================
"""

#logs out the bot from discord
@client.command(name="logout", aliases=["shutdown", "kill-yourself"])
#User must have the role to continue
@is_owner()
#defines a new function call logout
async def logout(ctx):
    print("\nBot logout requested. Shutting down...\n")
    await ctx.send("Logging out.")
    await client.change_presence(status=discord.Status.invisible)
    #tells the bot to logout
    await client.logout()

"""
===========================
This is the end of the client.
===========================
"""

#Checks token to login the bot into discord. Bot will reconnect if discord goes offline.
client.run(token, bot=True, reconnect=True)
