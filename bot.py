import datetime
import json
import traceback

import coc
import discord
from discord.ext import commands

import creds
from cogs.utils.error_handler import error_handler
from database.botdb import BotDatabase

description = """   
                Bot made to help with the Buds Alliance
                Owner : Ay355#0905

                The prefix is ,

                Tags can be typed with or without the hashtag

                Please DM or ping Ay355 if you need any help
            """





coc_client = coc.login(
    creds.coc_dev_email,
    creds.coc_dev_password, 
    client = coc.EventsClient,
    correct_tags=True
    )


intents = discord.Intents.all()
intents.members = True





initial_extensions = (
    "cogs.game_info",
    "cogs.database_bg",
    "cogs.auto_role",
    "cogs.moderation",
    "cogs.attack_strats",
    "cogs.misc"
)

# Important stuff

PREFIX = ","
SQLITE_FILE = 'database\db_filepath.db'



class BudBot(commands.Bot):
    def __init__(self):
        # Important things we will use throughout the bot

        super().__init__(
                        command_prefix=commands.when_mentioned_or(PREFIX),
                        description=description,
                        case_insensitive=True,
                        intents=intents
                        )


        self.coc = coc_client
        self.owner_ids = creds.owner_ids                    #Me and my alts
        self.client_id = creds.discord_client_id
        self.bot_id = creds.discord_bot_id
        self.uptime = datetime.datetime.utcnow()



        # Starts the database file
        self.dbconn = BotDatabase(SQLITE_FILE)




        # Load all the cogs
        for extension in initial_extensions:
            try:
                self.load_extension(extension)
            except Exception as extension:
                traceback.print_exc()




    async def on_ready(self):
        print(f"Logged in as {self.user}\nID: {self.user.id}\nDiscord Version: {discord.__version__}\nCoc Version: {coc.__version__}")
        activity = discord.Game(f"Getting 99% | ,help")
        await self.change_presence(status=discord.Status.online, activity=activity)


    async def on_command_error(self, ctx, exception):
        try:
            return await error_handler(ctx, exception)
        except:
            traceback.print_exc()


# Makes sure its the correct file

if __name__ == "__main__":
    try:
        bot = BudBot()
        bot.run(creds.discord_bot_token)
    except:
        traceback.print_exc()

