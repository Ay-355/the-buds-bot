import discord
from discord.ext import commands
import random

class Welcome(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @property
    def member_log_channel(self):
        return self.bot.get_channel()


    @commands.Cog.listener()
    async def on_member_join(self, member):
        await self.member_log_channel.send(f"""Welcome {member.mention} to the Buds Alliance discord server! If you are currently in one of our alliance's clans please send your tag and clan that your in. If you are a player wanting to join the alliance OR a clan wanting to join the alliance, please go to <#785208883953532948> and open a up a ticket. Support will be with you shortly.""")



    @commands.Cog.listener()
    async def on_member_leave(self, member):
        leave_messages = [
            f"{member.display_name} just left the server. Byyyeee",
            f"Bye {member.display_name}. Oh well, someone couldn't deal with the coolness.",
            f"{member.display_name} has left. Lmao too bad, missing out on the fun.",
            f"Can we have a moment of silence for {member.display_name}? Why would you want to leave such a cool alliance?"
        ]
        await self.member_log_channel.send(random.choice(leave_messages))