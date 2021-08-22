import discord
from discord.ext import commands
import random

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @property
    def member_log_channel(self):
        return self.bot.get_channel(...)


    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.member_log_channel.send(f"Welcome {member.mention}")



    @commands.Cog.listener()
    async def on_member_leave(self, member):
        leave_messages = [
            f"{member.display_name} just left the server.",
            'Someone just left the server.',
            f"{member.name} abandoned the server",
        ]

        await self.member_log_channel.send(random.choice(leave_messages))
