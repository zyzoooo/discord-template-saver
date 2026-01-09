import discord
from discord.ext import commands
import json
import os

zyzo_intents = discord.Intents.default()
zyzo_intents.guilds = True
zyzo_intents.guild_messages = True
zyzo_intents.message_content = True
zyzo_intents.members = True

zyzo_bot = commands.Bot(command_prefix=';', intents=zyzo_intents)

zyzo_template_file = 'template.txt'
zyzo_roles_file = 'roles.txt'

zyzo_allowed_users = [
    1234567890,  #  replace with your discord ID or the ID for allowed bot users
    0987654321
]

def zyzo_serialize_overwrites(zyzo_overwrites):
    zyzo_perms = {}
    for zyzo_target, zyzo_overwrite in zyzo_overwrites.items():
        if isinstance(zyzo_target, discord.Role):
            zyzo_allow, zyzo_deny = zyzo_overwrite.pair()
            zyzo_perms[str(zyzo_target.id)] = {
                'allow': zyzo_allow.value,
                'deny': zyzo_deny.value
            }
    return zyzo_perms

def zyzo_deserialize_overwrites(zyzo_guild, zyzo_perms):
    zyzo_overwrites = {}
    for zyzo_role_id, zyzo_perm in zyzo_perms.items():
        zyzo_role = discord.utils.get(zyzo_guild.roles, id=int(zyzo_role_id))
        if zyzo_role is None:
            continue
        zyzo_allow = discord.Permissions(zyzo_perm.get('allow', 0))
        zyzo_deny = discord.Permissions(zyzo_perm.get('deny', 0))
        zyzo_overwrites[zyzo_role] = discord.PermissionOverwrite.from_pair(zyzo_allow, zyzo_deny)
    return zyzo_overwrites

@zyzo_bot.event
async def on_ready():
    print(f"logged in as {zyzo_bot.user}")

@zyzo_bot.command()
async def savetemplate(ctx):
    if ctx.author.id not in zyzo_allowed_users:
        return
    if ctx.guild is None:
        return

    zyzo_guild = ctx.guild
    zyzo_template = []

    for zyzo_category in zyzo_guild.categories:
        zyzo_cat_data = {
            'name': zyzo_category.name,
            'channels': []
        }

        for zyzo_channel in zyzo_category.channels:
            zyzo_cat_data['channels'].append({
                'name': zyzo_channel.name,
                'type': str(zyzo_channel.type),
                'position': zyzo_channel.position,
                'permissions': zyzo_serialize_overwrites(zyzo_channel.overwrites)
            })

        zyzo_template.append(zyzo_cat_data)

    with open(zyzo_template_file, 'w') as zyzo_f:
        json.dump(zyzo_template, zyzo_f, indent=2)

    await ctx.send("saved")

@zyzo_bot.command()
async def loadtemplate(ctx):
    if ctx.author.id not in zyzo_allowed_users:
        return
    if ctx.guild is None:
        return
    if not os.path.exists(zyzo_template_file):
        return

    zyzo_guild = ctx.guild

    for zyzo_channel in list(zyzo_guild.channels):
        try:
            await zyzo_channel.delete()
        except:
            pass

    with open(zyzo_template_file, 'r') as zyzo_f:
        zyzo_template = json.load(zyzo_f)

    for zyzo_cat_data in zyzo_template:
        zyzo_category = await zyzo_guild.create_category(name=zyzo_cat_data['name'])

        zyzo_channels = sorted(zyzo_cat_data['channels'], key=lambda zyzo_x: zyzo_x['position'])

        for zyzo_ch in zyzo_channels:
            zyzo_overwrites = zyzo_deserialize_overwrites(zyzo_guild, zyzo_ch['permissions'])
            if 'text' in zyzo_ch['type']:
                await zyzo_guild.create_text_channel(
                    name=zyzo_ch['name'],
                    category=zyzo_category,
                    overwrites=zyzo_overwrites
                )
            else:
                await zyzo_guild.create_voice_channel(
                    name=zyzo_ch['name'],
                    category=zyzo_category,
                    overwrites=zyzo_overwrites
                )

@zyzo_bot.command()
async def saveroles(ctx):
    if ctx.author.id not in zyzo_allowed_users:
        return
    if ctx.guild is None:
        return

    zyzo_roles_data = []

    for zyzo_role in ctx.guild.roles:
        if zyzo_role.is_default() or zyzo_role.managed:
            continue

        zyzo_roles_data.append({
            'name': zyzo_role.name,
            'color': zyzo_role.color.value,
            'permissions': zyzo_role.permissions.value,
            'hoist': zyzo_role.hoist,
            'mentionable': zyzo_role.mentionable,
            'position': zyzo_role.position
        })

    with open(zyzo_roles_file, 'w') as zyzo_f:
        json.dump(zyzo_roles_data, zyzo_f, indent=2)

    await ctx.send("roles saved")

@zyzo_bot.command()
async def loadroles(ctx):
    if ctx.author.id not in zyzo_allowed_users:
        return
    if ctx.guild is None:
        return
    if not os.path.exists(zyzo_roles_file):
        return

    zyzo_guild = ctx.guild

    for zyzo_role in zyzo_guild.roles:
        if zyzo_role.is_default() or zyzo_role.managed:
            continue
        try:
            await zyzo_role.delete()
        except:
            pass

    with open(zyzo_roles_file, 'r') as zyzo_f:
        zyzo_roles_data = json.load(zyzo_f)

    zyzo_created_roles = []

    for zyzo_r in zyzo_roles_data:
        try:
            zyzo_role = await zyzo_guild.create_role(
                name=zyzo_r['name'],
                colour=discord.Colour(zyzo_r['color']),
                permissions=discord.Permissions(zyzo_r['permissions']),
                hoist=zyzo_r['hoist'],
                mentionable=zyzo_r['mentionable']
            )
            zyzo_created_roles.append((zyzo_role, zyzo_r['position']))
        except:
            pass

    try:
        zyzo_positions = {
            zyzo_role: zyzo_pos
            for zyzo_role, zyzo_pos in zyzo_created_roles
            if zyzo_role.position < zyzo_guild.me.top_role.position
        }
        await zyzo_guild.edit_role_positions(zyzo_positions)
    except:
        pass

    await ctx.send("roles loaded")

zyzo_bot.run("REPLACE TOKEN")
