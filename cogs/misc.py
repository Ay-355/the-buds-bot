import datetime
import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    @commands.command(name="uptime")
    async def uptime(self, ctx):
        now = datetime.datetime.utcnow()
        delta_uptime = now - self.bot.uptime
        hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
        minutes, seconds = divmod(remainder, 60)
        days, hours = divmod(hours, 24)
        await ctx.send(f"{days}d, {hours}h, {minutes}m, {seconds}s")


def setup(bot):
    bot.add_cog(Misc(bot))
