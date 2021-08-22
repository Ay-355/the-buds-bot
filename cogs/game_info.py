import coc
import discord
from discord.ext import commands



class GameInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='clan', description= 'gets info about a clan', aliases=["getclan", "claninfo"])
    async def clan(self, ctx, clantag):
        clantag = coc.utils.correct_tag(clantag)

        try:
            clan = await self.bot.coc.get_clan(clantag)
        except coc.NotFound:
            await ctx.send("This clan doesn't exist")


        war_log = 'Private' if clan.public_war_log is False else 'Public'
        claninfoEmbed = discord.Embed(title=f"Clan stats for {clan.name}", colour=discord.Color.blue())
        claninfoEmbed.set_thumbnail(url=clan.badge.url)
        claninfoEmbed.add_field(
            name='Tag',
            value=f"{clan.tag}\n[Open in game]({clan.share_link})",
            inline=True,
        )

        claninfoEmbed.add_field(name='Clan Level', value=clan.level, inline=True)
        claninfoEmbed.add_field(
            name='Clan Description', value=clan.description, inline=False
        )

        claninfoEmbed.add_field(
            name='Clan Leader',
            value=clan.get_member_by(role=coc.Role.leader),
            inline=True,
        )

        claninfoEmbed.add_field(name='Clan Type', value=clan.type, inline=True)
        claninfoEmbed.add_field(name='Location', value=clan.location, inline=True)
        claninfoEmbed.add_field(
            name='Required Trophies', value=clan.required_trophies, inline=True
        )

        claninfoEmbed.add_field(
            name='Total Clan Trophies', value=clan.points, inline=True
        )

        claninfoEmbed.add_field(
            name='Total Versus Battle Trophies',
            value=clan.versus_points,
            inline=True,
        )

        claninfoEmbed.add_field(name='War Log Type', value=war_log, inline=True)
        claninfoEmbed.add_field(
            name='War Win Streak', value=clan.war_win_streak, inline=True
        )

        claninfoEmbed.add_field(
            name='War Frequency',
            value=(clan.war_frequency).capitalize(),
            inline=True,
        )

        claninfoEmbed.add_field(
            name='Member Count', value=f"{clan.member_count}/50", inline=True
        )

        claninfoEmbed.add_field(
            name='Clan War League Rank', value=clan.war_league, inline=True
        )

        claninfoEmbed.add_field(
            name='Clan War Record',
            value=f"Wars Won: {clan.war_wins}\nWars Lost: {clan.war_losses}\nWars Tied: {clan.war_ties}",
            inline=True,
        )

        claninfoEmbed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)

        await ctx.send(embed=claninfoEmbed)




    @commands.command(name="player", description="gets info about a player", aliases=["getplayer", "playerinfo"])
    async def player(self, ctx, playertag):
        playertag = coc.utils.correct_tag(playertag)

        try:
            player = await self.bot.coc.get_player(playertag)
        except coc.NotFound:
            await ctx.send("This player doesn't exist!")


        playerinfoEmbed = discord.Embed(title=f"Player stats for {player.name}", colour=discord.Color.dark_green())
        playerinfoEmbed.set_thumbnail(url=player.league.icon.url)
        playerinfoEmbed.add_field(name="Tag", value=f"{player.tag}\n[Open in game]({player.share_link})")
        playerinfoEmbed.add_field(name='XP Level', value=player.exp_level, inline=True)
        playerinfoEmbed.add_field(name='League', value=player.league, inline=True)
        playerinfoEmbed.add_field(
            name='War Stars', value=player.war_stars, inline=True
        )

        playerinfoEmbed.add_field(name='Player Clan', value=player.clan, inline=True)
        playerinfoEmbed.add_field(
            name='Player Clan Tag', value=player.clan.tag, inline=True
        )

        playerinfoEmbed.add_field(name='Clan Role', value=player.role, inline=True)
        playerinfoEmbed.add_field(
            name='Townhall', value=f"{player.town_hall}", inline=True
        )

        playerinfoEmbed.add_field(
            name='Builder Hall', value=f"{player.builder_hall}", inline=True
        )

        playerinfoEmbed.add_field(
            name='Attack/Defense Wins',
            value=f"{player.attack_wins}/{player.defense_wins}",
            inline=True,
        )

        playerinfoEmbed.add_field(name='Trophies', value=player.trophies, inline=True)
        playerinfoEmbed.add_field(
            name='Highest Trophies', value=player.best_trophies, inline=True
        )

        playerinfoEmbed.add_field(
            name='Versus Battle Trophies',
            value=player.versus_trophies,
            inline=True,
        )

        playerinfoEmbed.add_field(
            name='Highest Versus Trophies',
            value=player.best_versus_trophies,
            inline=True,
        )

        playerinfoEmbed.add_field(
            name='Versus Battle Wins', value=player.versus_attack_wins, inline=True
        )

        playerinfoEmbed.add_field(
            name='Donations', value=player.donations, inline=True
        )

        playerinfoEmbed.add_field(
            name='Donations Received', value=player.received, inline=True
        )

        playerinfoEmbed.set_footer(text=f"Requested by {ctx.author}", icon_url=ctx.author.avatar_url)
        await ctx.send(embed=playerinfoEmbed)


    @commands.command(name="heroes", description="Gets info about a players heroes", aliases=["getplayerheroes", "playerheroes", "pheroes"])
    async def heroes(self, ctx, playertag):
        playertag = coc.utils.correct_tag(playertag)

        try:
            player = await self.bot.coc.get_player(playertag)
        except coc.NotFound:
            await ctx.send("This player doesn't exist!")

        playerheroesEmbed = discord.Embed(title=f"Heroes for {player.name}")
        for hero in player.heroes:
            playerheroesEmbed.add_field(name=str(hero), value=f"Level: {hero.level}\nMax Level: {hero.max_level}", inline=False)
        
        await ctx.send(embed=playerheroesEmbed)



    @commands.command(name="troops", description="gets info about a players troops")
    async def troops(self, ctx, playertag):
        playertag = coc.utils.correct_tag(playertag)

        try:
            player = await self.bot.coc.get_player(playertag)
        except coc.NotFound:
            await ctx.send("This player doesn't exist!")


        playertroopsEmbed = discord.Embed(title=f"Troop stats for {player.name}", colour=discord.Color.dark_orange())
        for troop in player.troops:
            if troop.is_home_base:
                playertroopsEmbed.add_field(
                    name=f'{troop} Lvl: {troop.level}',
                    value=f"Max Level: {troop.max_level}",
                    inline=True,
                )


        await ctx.send(embed=playertroopsEmbed)


    @commands.command(name="buildert", description="gets info about a players builder base troops")
    async def buildertroops(self, ctx, playertag):
        playertag = coc.utils.correct_tag(playertag)

        try:
            player = await self.bot.coc.get_player(playertag)
        except coc.NotFound:
            await ctx.send("This player doesn't exist!")


        buildertroopsEmbed = discord.Embed(title=f"Builder troop stats for {player.name}", colour=discord.Color.dark_orange())
        for troop in player.troops:
            if troop.is_builder_base:
                buildertroopsEmbed.add_field(
                    name=f'{troop} Lvl: {troop.level}',
                    value=f"Max Level: {troop.max_level}",
                    inline=True,
                )


        await ctx.send(embed=buildertroopsEmbed)



    @commands.command(name="spells", description="gets info about a players spells")
    async def spells(self, ctx, playertag):
        playertag = coc.utils.correct_tag(playertag)

        try:
            player = await self.bot.coc.get_player(playertag)
        except coc.NotFound:
            await ctx.send("This player doesn't exist!")


        spellsEmbed = discord.Embed(title=f"Spell stats for {player.name}", colour=discord.Color.dark_orange())
        for spell in player.spells:
            spellsEmbed.add_field(
                name=f'{spell} Lvl: {spell.level}',
                value=f"Max Level: {spell.max_level}",
                inline=True,
            )


        await ctx.send(embed=spellsEmbed)


    #TODO figure this out
    # @commands.command(name="legendstats", description="gets info about a legend league")
    # async def spells(self, ctx, playertag):
    #     playertag = coc.utils.correct_tag(playertag)

    #     try:
    #         player = await self.bot.coc.get_player(playertag)
    #     except coc.NotFound:
    #         await ctx.send("This player doesn't exist!")
    #     if player.
    #     legendstatsEmbed = discord.Embed(title=f"Legend Stats for {player.name}")
    #     legendstatsEmbed.add_field(name="Legend Trophies", value=player.legend_trophies)
    #     legendstatsEmbed.add_field(name="Current Season Stats", value=player.current_season)
    #     legendstatsEmbed.add_field(name="Previous Season", value=player.previous_season)
    #     legendstatsEmbed.add_field(name="Best Season", value=player.best_season)




def setup(bot):
    bot.add_cog(GameInfo(bot))

