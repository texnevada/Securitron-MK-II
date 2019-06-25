#import discord py library
import discord
#Imports commands
from discord.ext import commands
#import permissions
from discord.ext.commands import has_permissions

class purgecommand(commands.Cog):
    def __init__(self, client):
        self.client = client

    #Reads the users input if it has prefix or not
    @commands.command(name="clear", aliases=["purge"])
    #Will only execute command if user has the role
    @has_permissions(manage_channels=True)
    #sees user wants to use the command clear.
    async def clear(self, ctx, amount: int):
        try:
            await ctx.channel.purge(limit=amount+1)
            await ctx.channel.send("Messages cleared!")
            print(f"Purged messages in \"{ctx.guild.name}\" ")
        except Exception as e:
            await ctx.send("I require the permission \"manage channels\" to delete messages for you.")

def setup(client):
    client.add_cog(purgecommand(client))
