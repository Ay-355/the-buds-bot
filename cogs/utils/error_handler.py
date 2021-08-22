import discord
from discord.ext import commands
import traceback


async def error_handler(ctx, error):

    if isinstance(error, commands.NoPrivateMessage):
        return await ctx.author.send("Bot can't be used in private messages")

    if isinstance(error, commands.MissingPermissions):
        return await ctx.send("You do not have the required permissions needed to do that")

    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send(f"Hmm, looks like you are missing a required argument. "
                        "Please do `{ctx.prefix}help command` for more info")

    if isinstance(error, commands.BotMissingPermissions):
        return await ctx.send("Looks like I don't have the required permissions to do this. "
                        "Please make sure I have the permissions needed")

    if isinstance(error, commands.CommandNotFound):
        return

    if isinstance(error, commands.BadArgument):
        return

    if isinstance(error, discord.Forbidden):
        return

    return traceback.print_exc()

