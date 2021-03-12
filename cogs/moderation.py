import traceback
import asyncio
import discord
from discord.ext import commands
from discord.ext.commands.core import has_permissions

from cogs.utils.checks import admin


class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot




    @commands.command(name="kick")
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        await member.kick(reason=reason)
        kickEmbed = discord.Embed(title="Member kicked!", description=f"**{member}** was kicked by **{ctx.author}**", colour=discord.Color.red())
        kickEmbed.add_field(name="Reason:", value=reason)
        await ctx.send(embed=kickEmbed)



    @commands.command(name="ban")
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        await member.ban(reason=reason)
        banEmbed = discord.Embed(title="Member banned!", description=f"**{member}** was banned by **{ctx.author}**", colour=discord.Color.red())
        banEmbed.add_field(name="Reason:", value=reason)
        await ctx.send(embed=banEmbed)




    @commands.command(name="purge")
    @commands.has_permissions(administrator=True)
    async def purge(self, ctx, number):  
        try:
            number = int(number)
        except:
            await ctx.send("Please give a correct number")

        if number < 1:
            await ctx.send("Please give a valid number to clear")
        
        amount_purged = await ctx.channel.purge(limit=number)
        purgeEmbed = discord.Embed(title='Done', description=f"**{ctx.author}** cleared **{len(amount_purged)}** messages",colour=discord.Color.green())
        await ctx.send(embed=purgeEmbed)





def setup(bot):
    bot.add_cog(Moderation(bot))
