#import discord py library
import discord
#Imports commands
from discord.ext import commands
#import permissions
from discord.ext.commands import has_permissions
import sqlite3

class serverinformation(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["server-info"])
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def serverinfo(self, ctx):
        try:
            embed = discord.Embed(color=discord.Color.red())
            embed.set_footer(text="This was brought to you by Robco industries automated reply system")
            #embed.set_image(url="")
            #embed.set_thumbnail(url="https://static1.squarespace.com/static/5bf3d1670dbda3ebca76e890/t/5bf3d4911ae6cfcc40a70d62/1547021826210/?format=1500w")
            embed.set_author(icon_url=ctx.guild.icon_url, name=f"Server information for {ctx.guild.name}")
            embed.add_field(name="Server owner", value=ctx.guild.owner, inline=True)
            embed.add_field(name="Region", value=ctx.guild.region, inline=True)
            embed.add_field(name="Server ID", value=ctx.guild.id, inline=True)
            embed.add_field(name="channel categories", value=len(ctx.guild.categories), inline=True)
            embed.add_field(name="Text channels", value=len(ctx.guild.text_channels), inline=True)
            embed.add_field(name="Voice channels", value=len(ctx.guild.voice_channels), inline=True)
            embed.add_field(name="Total channels", value=len(ctx.guild.channels), inline=True)
            embed.add_field(name="Members", value=ctx.guild.member_count, inline=True)
            #CANT FIND A WAY TO COUNT BOTS. AAAAAAAAAAAAAA
            if ctx.guild.premium_tier != 0:
                embed.add_field(name="Server\'s Nitro Tier", value=ctx.guild.premium_tier, inline=True)
            if ctx.guild.premium_subscription_count != 0:
                embed.add_field(name="Total server boosts", value=ctx.guild.premium_subscription_count, inline=True)
            if ctx.guild.features == False:
                embed.add_field(name="Server features", value=ctx.guild.features, inline=True)
            embed.add_field(name="Emoji limit", value=ctx.guild.emoji_limit, inline=True)
            bans = 0
            for x in await ctx.guild.bans():
                bans += 1
            embed.add_field(name="Bans", value=bans, inline=True)
            estimate = await ctx.guild.estimate_pruned_members(days=7)
            embed.add_field(name="Inactive members 7 days", value=estimate, inline=True)
            embed.add_field(name="Server created at", value=ctx.guild.created_at, inline=False)
            if ctx.guild.mfa_level == 0:
                embed.add_field(name="Verification level", value="**Poor.**\nWe recommend turning on 2FA on the server for good security.", inline=True)
            elif ctx.guild.mfa_level == 1:
                embed.add_field(name="Verification level", value="**Great!**", inline=True)
            await ctx.send(embed=embed)
        except:
            await ctx.send("Thats odd. I can't seem to give you that information. You better report this in to support.")

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def auditlogs(self, ctx):
        return None


    @commands.command()
    @commands.has_permissions(manage_channels=True)
    @commands.guild_only()
    async def modactions(self, ctx, arg1:str, *, arg2:str):
        #try:
        print(ctx.guild.me)
        entries = await ctx.guild.audit_logs(limit=None, user=ctx.guild.me).flatten()
        await ctx.send('This has made {} moderation actions.'.format(len(entries)))
        # except:
        #     await ctx.send("Did you mention the right user?")

def setup(client):
    client.add_cog(serverinformation(client))
