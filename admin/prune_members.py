#import discord py library
import discord
#Imports commands
from discord.ext import commands
#import permissions
from discord.ext.commands import has_permissions

class prune_members(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def prune(self, ctx, days:str):
        estimate = await ctx.guild.estimate_pruned_members(days=days)
        await ctx.send(f"Cleared the strip of {estimate} stranglers")
        await ctx.guild.prune_members(days=days)


def setup(client):
    client.add_cog(prune_members(client))
