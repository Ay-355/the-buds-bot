from discord.ext import commands
import json

# Guild Permissions checks

async def check_guild_permissions(ctx, perms, check=all):
    if await ctx.bot.is_owner(ctx.author):
        return True
    return perms in dict(ctx.author.guild_permissions).



def manage_guild():
    async def pred(ctx):
        perms = await check_guild_permissions(ctx, 'manage_guild')
        if not perms:
            raise commands.CheckFailure('You must have **Manage Server** permissions to use this command!')
        return True
    return commands.check(pred)


def admin():
    async def pred(ctx):
        perms = await check_guild_permissions(ctx, 'administrator')
        if not perms:
            raise commands.CheckFailure('You must have **Administrator** permissions to use this command!')
        return True
    return commands.check(pred)




# Check if has role

with open(r"cogs\utils\role_id.json") as f:
    roles_ids = json.load(f)


def check_if_has_leader_role(ctx):
    leader_role = int(roles_ids['special_roles']['leader'])
    return leader_role in ctx.author.roles


def check_if_has_coleader_role(ctx):
    co_leader_role = int(roles_ids['special_roles']["co-leader"])
    return co_leader_role in ctx.author.roles


def check_if_has_clan_member_role(ctx):
    clan_member_role = int(roles_ids['special_roles']['clan members'])
    return clan_member_role in ctx.author.roles


# Functions to see

def is_leader():
    def pred(ctx):
        return check_if_has_leader_role(ctx)
    return commands.check(pred)


def is_leader_or_coleader():
    def pred(ctx):
        return check_if_has_leader_role(ctx) or check_if_has_coleader_role(ctx)
    return commands.check(pred)


def is_clan_member():
    def pred(ctx):
        return check_if_has_clan_member_role(ctx)
    return commands.check(pred)
