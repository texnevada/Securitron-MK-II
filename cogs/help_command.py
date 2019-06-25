#import discord library
import discord
#Imports commands
from discord.ext import commands
#Import permissions & error checks
from discord.ext.commands import has_permissions, MissingPermissions
#Allows us to read json files
import json
import sqlite3

with open("prefix.json") as json_prefix:
        #makes the name "prefix" a reference to the json file.
        pre = json.load(json_prefix)
class prefix_check:
    def __init__(guild, id):
        guild.id = id
    def pref(guild):
        try:
            conn = sqlite3.connect("databases/ServerConfigs.db")
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM prefixes WHERE GuildID LIKE ?", ('{}'.format(guild.id),))
            response = c.fetchone()
            if response:
                prefi = []
                prefi.append(response["prefix"])
                prefix = prefi
            else:
                prefix = pre["prefix"]
            conn.close()
        except:
            prefix = pre["prefix"]
        return prefix[0]

#Making a class to reference this file later as extension
class help_commands(commands.Cog):
    def __init__(self, client):
        self.client = client
    #Waiting for command from user
    @commands.command(name="help", aliases=["h", "commands"])
    async def help(self, ctx):
        conn = sqlite3.connect("databases/HelpCommands.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM HelpCommand")
        response = c.fetchall()
        #starts a embed in discord
        embed = discord.Embed(color = 0x80ff80)
        embed.set_footer(text="This was brought to you by Robco Industries automated reply system")
        #embed.set_image(url="")
        #embed.set_thumbnail(url="")
        #Sets author text
        embed.set_author(name="Help commands!")
        #check for guild prefix with guild id
        try:
            x = prefix_check(ctx.guild.id)
            prefix = x.pref()
        except:
            prefix = pre["prefix"]
        #Loop every entry in the database
        for entry in response:
            #Add embed from entry
            embed.add_field(name=prefix+entry["CommandName"], value=entry["CommandDescription"], inline=False)
        #sends embed
        conn.close()
        await ctx.send(embed=embed)

        try:
            if ctx.author.guild_permissions.manage_channels:
                conn = sqlite3.connect("databases/HelpCommands.db")
                conn.row_factory = sqlite3.Row
                c = conn.cursor()
                c.execute("SELECT * FROM AdminHelpCommand")
                response = c.fetchall()
                embed = discord.Embed(
                    color = discord.Color.red()
                )
                embed.set_footer(text="This was brought to you by Robco Industries automated reply system")
                #embed.set_image(url="")
                #embed.set_thumbnail(url="")
                #Sets author text
                embed.set_author(name="Admin help commands!")
                #check for guild prefix with guild id
                try:
                    x = prefix_check(ctx.guild.id)
                    prefix = x.pref()
                except:
                    prefix = pre["prefix"]
                #Loop every entry in the database
                for entry in response:
                    #Add embed from entry
                    embed.add_field(name=prefix+entry["CommandName"], value=entry["CommandDescription"], inline=False)
                #sends embed
                conn.close()
                await ctx.send(embed=embed)
            except:
                return None

def setup(client):
    client.add_cog(help_commands(client))
