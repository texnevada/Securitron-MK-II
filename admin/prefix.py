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
    @commands.guild_only()
    async def prefix(self, ctx, arg:str):
        #checks to see if user has manage channel permissions
        if ctx.author.guild_permissions.manage_channels:
            #connects to database
            conn = sqlite3.connect("databases/ServerConfigs.db")
            conn.row_factory = sqlite3.Row
            c = conn.cursor()
            #checks if there is any prefixes connected with said guild.
            c.execute("SELECT * FROM prefixes WHERE GuildID = ?", (ctx.guild.id, ))
            #makes a response variable.
            response = c.fetchone()
            #checks to see if there is a prefix for embed to show later.
            oldprefix = []
            #If runs there is a response
            if response:
                #appends old prefix
                oldprefix.append(response["Prefix"])
                isprefixold = True
                c.execute("DELETE FROM prefixes WHERE GuildID = ?", [ctx.guild.id])
            #Will run if there is no response
            if not response:
                isoldprefix = False
            #adds new prefix into the system.
            c.execute("INSERT INTO prefixes (GuildID,GuildName,Prefix) VALUES (?,?,?)", (ctx.guild.id, ctx.guild.name, arg,))
            #commits changes
            conn.commit()
            #closes database
            conn.close()

            embed = discord.Embed(
                color = 0xe7e9d3
            )

            embed.set_footer(text="This was brought to you by Robco Industries automated reply system")
            #embed.set_image(url="")
            embed.set_thumbnail(url="")
            embed.set_author(name="Securitron MK II systems")
            if isprefixold == True:
                embed.add_field(name="Your server prefix has changed!", value="Your prefix is now changed\n**Old:** {}\n**New:** {}\nYou can also use \"@Securitron MK\" II for commands even if you forget your prefix".format(oldprefix[0], arg))
            elif isprefixold == False:
                embed.add_field(name="Your server prefix has changed!", value="Your prefix is now changed\n**New:** {}".format(arg) )
            await ctx.send(embed=embed)
        else:
            await ctx.send("Strip secure.")

def setup(client):
    client.add_cog(prefix(client))
