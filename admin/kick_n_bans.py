#import discord py library
import discord
#Imports commands
from discord.ext import commands
#import permissions
from discord.ext.commands import has_permissions
import sqlite3

class kick_n_bans(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        conn = sqlite3.connect("databases/ServerConfigs.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM reportconfig WHERE GuildID LIKE ?", ('{}'.format(ctx.guild.id),))
        response = c.fetchone()
        if response:
            channel = self.client.get_channel(response["LogChannelID"])
            await channel.send(f"User {member} has been kicked by {ctx.author.mention}\nReason: {reason}")
            await ctx.guild.kick(user=member, reason=reason)
        if not response:
            await ctx.guild.kick(user=member, reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, days:int, *, reason=None):
        if member.guild_permissions.manage_channels:
            await ctx.send("You cannot ban a moderator!")
        else:
            conn = sqlite3.connect("databases/ServerConfigs.db")
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            c.execute("SELECT * FROM reportconfig WHERE GuildID LIKE ?", ('{}'.format(ctx.guild.id),))
            response = c.fetchone()
            if response:
                channel = self.client.get_channel(response["LogChannelID"])
                await channel.send(f"User {member} has been kicked by {ctx.author.mention}\nReason: {reason}")
                await ctx.guild.ban(user=member, delete_message_days=days, reason=reason)
            if not response:
                await ctx.guild.ban(user=member, delete_message_days=days, reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member: discord.Member, *, reason=None):
        conn = sqlite3.connect("databases/ServerConfigs.db")
        conn.row_factory = sqlite3.Row
        c = conn.cursor()
        c.execute("SELECT * FROM reportconfig WHERE GuildID LIKE ?", ('{}'.format(ctx.guild.id),))
        response = c.fetchone()
        if response:
            channel = self.client.get_channel(response["LogChannelID"])
            await channel.send(f"User {member} has been kicked by {ctx.author.mention}\nReason: {reason}")
            await ctx.guild.unban(user=member, reason=reason)
        if not response:
            await ctx.guild.unban(user=member, reason=reason)

def setup(client):
    client.add_cog(kick_n_bans(client))
