import traceback

import coc
import discord

from discord.ext import commands

# clan_tags = "#2P28G9VC8"
# buds_alliance_server_id = 747395805131833414


class AutoRole(commands.Cog):
    """
    When a member changes clans it will change their clan role to the one that they are in
    
    Example: If I leave clan_1 and join clan_2, the bot will remove my clan_1 role and give me the clan_2 role
    
    """


    def __init__(self, bot):
        self.bot = bot
        self.bot.coc.add_events(
            self.on_clan_member_join,
            self.on_clan_member_leave
        )
        clan_tags = self.bot.dbconn.get_linked_clans_without_guild_id()
        for clan_tag in clan_tags:
            self.bot.coc.add_clan_updates(clan_tag)
        





    @property
    def general_channel(self):
        return self.bot.get_channel(802306491410415699)



    @coc.ClanEvents.member_join()
    async def on_clan_member_join(self, member, clan):

        try:
            joinEmbed = discord.Embed(title="Clan Member Update", description=f"**[{member.name}]({member.share_link})** just joined {clan.name}")
            await self.general_channel.send(embed=joinEmbed)

            registered_tags = self.bot.dbconn.get_tags()

            if member.tag in registered_tags:
                try:
                    user_id = self.bot.dbconn.get_member_with_tag((member.tag,))

                    guild = self.bot.get_guild(747395805131833414)
                    disc_member = guild.get_member(user_id)

                    role_to_give_id = self.bot.dbconn.get_role_from_clan_tag((clan.tag, guild.id,))
                    role_to_give = guild.get_role(role_to_give_id)

                    if role_to_give in disc_member.roles:
                        return
                    else:
                        await disc_member.add_roles(role_to_give)

                except:
                    traceback.print_exc()


            else:
                return

        except:
            traceback.print_exc()





    @coc.ClanEvents.member_leave()
    async def on_clan_member_leave(self, member, clan):
        try:
            leaveEmbed = discord.Embed(title="Clan Member Update", description=f"**[{member.name}]({member.share_link})** just left {clan.name}")
            await self.general_channel.send(embed=leaveEmbed)

            registered_tags = self.bot.dbconn.get_tags()

            if member.tag in registered_tags:

                try:
                    user_id = self.bot.dbconn.get_member_with_tag((member.tag,))

                    guild = self.bot.get_guild(747395805131833414)
                    disc_member = guild.get_member(user_id)

                    role_to_remove_id = self.bot.dbconn.get_role_from_clan_tag((clan.tag, guild.id,))
                    role_to_remove = guild.get_role(role_to_remove_id)

                    if role_to_remove not in disc_member.roles:
                        return
                    else:
                        await disc_member.remove_roles(role_to_remove)

                except:
                    traceback.print_exc()


            else:
                return

        except:
            traceback.print_exc()













def setup(bot):
    bot.add_cog(AutoRole(bot))




