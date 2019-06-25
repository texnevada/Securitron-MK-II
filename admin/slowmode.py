#import discord py library
import discord
#Imports commands
from discord.ext import commands
#import permissions
from discord.ext.commands import has_permissions

class slowmode(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def slowmode(self, ctx, seconds:int):
        try:
            if seconds >= 21601:
                await ctx.send("Amount impossible. You can only do 21600 seconds or less.")
            elif seconds <= -1:
                await ctx.send("Amount impossible. You can only do 21600 seconds or less.")
            elif seconds != 0:
                await ctx.channel.edit(slowmode_delay=seconds)
                await ctx.send("The strip is now secure.")
            elif seconds == 0:
                await ctx.channel.edit(slowmode_delay=seconds)
                await ctx.send("Gates to the strip is now open.")
        except:
            await ctx.send("Well that went to shit")


def setup(client):
    client.add_cog(slowmode(client))
