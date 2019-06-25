#import discord py library
import discord
#Imports commands
from discord.ext import commands
#import permissions
from discord.ext.commands import has_permissions
import sqlite3

class logchannel(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    async def togglelogchannel(self, ctx):
        if ctx.author.guild_permissions.manage_channels:
            #connects to database
            conn = sqlite3.connect("databases/ServerConfigs.db")
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM reportconfig WHERE LogChannelID = ?", (ctx.channel.id, ))
            #makes a response variable.
            response = c.fetchone()
            if response:
                c.execute("DELETE FROM reportconfig WHERE GuildID = ?", [ctx.guild.id])
                await ctx.send(f"<#{ctx.channel.id}> is no longer a log channel")
            if not response:
                c.execute("SELECT * FROM reportconfig WHERE GuildID = ?", (ctx.guild.id, ))
                response = c.fetchone()
                if response:
                    oldchannel = []
                    oldchannel.append(response["LogChannelID"])
                    c.execute("DELETE FROM reportconfig WHERE GuildID = ?", [ctx.guild.id])
                    c.execute("INSERT INTO reportconfig (GuildID,GuildName,LogChannelID,LogChannelName) VALUES (?,?,?,?)", (ctx.guild.id, ctx.guild.name, ctx.channel.id, ctx.channel.name))
                    await ctx.send(f"The old log channel <#{oldchannel[0]}> is now replaced with <#{ctx.channel.id}>")
                if not response:
                    c.execute("INSERT INTO reportconfig (GuildID,GuildName,LogChannelID,LogChannelName) VALUES (?,?,?,?)", (ctx.guild.id, ctx.guild.name, ctx.channel.id, ctx.channel.name))
                    await ctx.send(f"Logs will now be posted in <#{ctx.channel.id}>")
            #commits changes
            conn.commit()
            #closes database
            conn.close()
        else:
            await ctx.send("Move along citizen.")

def setup(client):
    client.add_cog(logchannel(client))
