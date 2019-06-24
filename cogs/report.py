#import discord py library
import discord
#Imports commands
from discord.ext import commands
#import permissions
from discord.ext.commands import has_permissions
import sqlite3

class prefix(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def report(self, ctx, *, arg:str):
        conn = sqlite3.connect("databases/ServerConfigs.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM prefixes WHERE GuildID LIKE ?", ('{}'.format(guild.id),))
        response = c.fetchone()
        if response:
            


def setup(client):
    client.add_cog(prefix(client))
