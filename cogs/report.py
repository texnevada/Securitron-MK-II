#import discord py library
import discord
#Imports commands
from discord.ext import commands
#import permissions
from discord.ext.commands import has_permissions
import sqlite3

class report(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    #A very simple report system which can be adapted over time to be complex.
    async def report(self, ctx, *, arg:str):
        conn = sqlite3.connect("databases/ServerConfigs.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM reportconfig WHERE GuildID LIKE ?", ('{}'.format(ctx.guild.id),))
        response = c.fetchone()
        if response:
            channel = self.client.get_channel(response["LogChannelID"])
            await channel.send(f"Report send by: {ctx.author.mention}\nUser report: {arg}")
            await ctx.send("You've done the right thing, citizen. Reporting struggles, scuffles, and tussles is the civic duty of every man, woman, and child.")
        if not response:
            return None


def setup(client):
    client.add_cog(report(client))
