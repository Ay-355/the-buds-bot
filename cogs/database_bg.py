import traceback

import coc
import discord
from coc import utils
from database.botdb import BotDatabase
from discord.ext import commands, tasks
from discord.ext.commands.core import is_owner
from discord.utils import get

from cogs.utils.checks import is_leader_or_coleader, admin
from cogs.utils.utilityfuncs import getTownhall


class DatabaseBackground(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command(name="adduser")  
    @is_owner()   #TODO Also update member nickname to be the format (f"{player.name} | {player.clan.name}"), and if they already have one of those leave it
    async def adduser(self, ctx, player_tag, member: discord.Member):
        try:
            player_tag = utils.correct_tag(player_tag)
            player = await self.bot.coc.get_player(player_tag)
        except coc.NotFound:
            await ctx.send('This player does not exist')

        try:
            self.bot.dbconn.register_user((member.id, player.tag, player.name, player.town_hall, ))
            await ctx.send(f"Added {member.display_name}'s account to the database")

            player_th = int(player.town_hall)
            th_role_id = await getTownhall(player_th)
            th_role = ctx.author.guild.get_role(th_role_id)
            if th_role_id == None:
                await ctx.send("Couldn't add Townhall role")
            
            await member.add_roles(th_role)
            await ctx.send(f"Added the player's townhall role ({player.town_hall})")


            old_name = str(member.display_name)
            bar = "|"

            if bar in old_name:
                return
            else:
                nick_format = f"{player.name} | {player.clan.name}"
                await member.edit(nick=nick_format)



        except:
            traceback.print_exc()



    @commands.command(name="accounts")
    async def accounts(self, ctx, member: discord.Member = None):
        member = ctx.author if not member else member
        member_id = int(member.id)
        try:
            tags = self.bot.dbconn.get_player_with_id((member_id,))

            if tags == None:

                await ctx.send("There are no accounts currently registered")
            else:

                accountsEmbed = discord.Embed(title=f"Accounts linked to {member.name}", value=None, color=discord.Color.blue())
                for tag in tags:

                    try:
                        player = await self.bot.coc.get_player(tag)
                    except:
                        await ctx.send("There was an error")

                    if player.clan is None:
                        player_clan = "Not in a clan"
                    else:
                        player_clan = player.clan.name
                    accountsEmbed.add_field(
                        name=f"**{tag}**", 
                        value=f"[Open in game]({player.share_link})\nName: {player.name}\nTH: {player.town_hall}\nClan: {player_clan}\n", 
                        inline=False)
                
                await ctx.send(embed=accountsEmbed)

        except:
            traceback.print_exc()



    @commands.command(name="accowner")
    async def accowner(self, ctx, coc_tag):

        if not utils.is_valid_tag(coc_tag):
            await ctx.send("You didn't give me a proper tag!")

        else:

            try:
                id = self.bot.dbconn.get_member_with_tag((coc_tag,))
                if id == None:
                    await ctx.send("The person who owns this id is not registered")
                else:
                    mention_id = f"<@{id}>"
                    ownerEmbed = discord.Embed(title=f"Account owner for {coc_tag}", description=mention_id, color=discord.Color.blue())
                    await ctx.send(embed=ownerEmbed)

            except:
                traceback.print_exc()






    @commands.command(name="linkrole")
    @is_owner()
    async def linkrole(self, ctx, clan_tag, role: discord.Role):

        try:
            corrected_clan_tag = utils.correct_tag(clan_tag)
            clan = await self.bot.coc.get_clan(corrected_clan_tag)
        except coc.NotFound:
            await ctx.send('This clan does not exist')

        try:
            self.bot.dbconn.link_role_to_tag((ctx.guild.id, role.id, corrected_clan_tag,))
            await ctx.send(f"Linked clan {clan.name} (`{corrected_clan_tag}`) to role `{role.name}`")

        except:
            traceback.print_exc()



    @commands.command(name="linkedroles")
    async def linkedroles(self, ctx):
        roles = self.bot.dbconn.get_linked_roles((ctx.guild.id,))
        tags = self.bot.dbconn.get_linked_clans((ctx.guild.id,))

        try:
            if roles == None:
                await ctx.send("Nothing registered for this server")
            else:
                linkedrolesEmbed = discord.Embed(title=f"Linked roles for {ctx.guild.name}", value=None, color=discord.Color.dark_purple())
                for role_id, tag in zip(roles, tags):
                    clan = await self.bot.coc.get_clan(tag)
                    role = ctx.author.guild.get_role(role_id)
                    linkedrolesEmbed.add_field(
                        name=f"Clan: {clan.name} ({tag})", 
                        value=f"[Open in game]({clan.share_link})\n`Role linked to: {role.name}\nID: {role.id}`\n", inline=False)

                await ctx.send(embed=linkedrolesEmbed)

        except:
            traceback.print_exc()



    @tasks.loop(minutes=2280.0)
    async def update(self):
        """Updates the database to put new data in. Also does some server maintenance if anything has changed"""
        all_users = self.bot.dbconn.get_all_users
        for user in all_users:
            try:
                player = self.bot.coc.get_player(user[1])
            except:
                print(f"There was an error with {user[1]}")
        

            registered_th = self.bot.dbconn.get_townhall
            old_th_role = f"Townhall {registered_th}"
            current_player_th = await getTownhall(player.town_hall)
            new_th_role = f"Townhall {current_player_th}"

            if str(registered_th) == str(current_player_th):
                pass
            else:
                self.bot.dbconn.update_user_th((player.town_hall,))

            ser_member = user[0]

            if old_th_role in ser_member.roles:
                await ser_member.remove_roles(old_th_role)
                await ser_member.add_roles(new_th_role)



    @update.before_loop
    async def before_update(self):
        """Prevents bot from running before bot is connected"""
        await self.bot.wait_until_ready()




def setup(bot):
    bot.add_cog(DatabaseBackground(bot))
