from discord.ext import commands
import json

# Guild Permissions checks

async def check_guild_permissions(ctx, perms, check=all):
    if await ctx.bot.is_owner(ctx.author):
        return True
    is_owner = await ctx.bot.is_owner(ctx.author)
    if is_owner:
        return True



def manage_guild():
    async def pred(ctx):
        perms = await check_guild_permissions(ctx, {'manage_guild': True})
        if not perms:
            raise commands.CheckFailure('You must have **Manage Server** permissions to use this command!')
        return True
    return commands.check(pred)


def admin():
    async def pred(ctx):
        perms = await check_guild_permissions(ctx, {'administrator': True})
        if not perms:
            raise commands.CheckFailure('You must have **Administrator** permissions to use this command!')
        return True
    return commands.check(pred)




# Check if has role

with open(r"cogs\utils\role_id.json") as f:
    roles_ids = json.load(f)


def check_if_has_leader_role(ctx):
    leader_role = int(roles_ids['special_roles']['leader'])
    if leader_role in ctx.author.roles:
        return True
    else:
        return False


def check_if_has_coleader_role(ctx):
    co_leader_role = int(roles_ids['special_roles']["co-leader"])
    if co_leader_role in ctx.author.roles:
        return True
    else:
        return False


def check_if_has_clan_member_role(ctx):
    clan_member_role = int(roles_ids['special_roles']['clan members'])
    if clan_member_role in ctx.author.roles:
        return True
    else:
        return False


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
