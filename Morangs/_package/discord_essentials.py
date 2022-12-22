from asyncio import sleep
from random import randint
from datetime import datetime

from core import client, DEVELOPER_ID


async def delete_message(message, time):
    await sleep(time)
    try:
        for msg in message:
            await msg.delete()
    except:
        await message.delete()


async def permission(message, permission_type, fail_message=None, time=5):
    permissions = {
        'add_reactions': message.author.guild_permissions.add_reactions,
        'administrator': message.author.guild_permissions.administrator,
        'attach_files': message.author.guild_permissions.attach_files,
        'ban_members': message.author.guild_permissions.ban_members,
        'change_nickname': message.author.guild_permissions.change_nickname,
        'connect': message.author.guild_permissions.connect,
        'create_instant_invite': message.author.guild_permissions.create_instant_invite,
        # 'create_private_threads': message.author.guild_permissions.create_private_threads,
        # 'create_public_threads': message.author.guild_permissions.create_public_threads,
        'deafen_members': message.author.guild_permissions.deafen_members,
        'embed_links': message.author.guild_permissions.embed_links,
        'external_emojis': message.author.guild_permissions.external_emojis,
        # 'external_stickers': message.author.guild_permissions.external_stickers,
        'kick_members': message.author.guild_permissions.kick_members,
        'manage_channels': message.author.guild_permissions.manage_channels,
        'manage_emojis': message.author.guild_permissions.manage_emojis,
        # 'manage_emojis_and_stickers': message.author.guild_permissions.manage_emojis_and_stickers,
        # 'manage_events': message.author.guild_permissions.manage_events,
        'manage_guild': message.author.guild_permissions.manage_guild,
        'manage_messages': message.author.guild_permissions.manage_messages,
        'manage_nicknames': message.author.guild_permissions.manage_nicknames,
        'manage_permissions': message.author.guild_permissions.manage_permissions,
        'manage_roles': message.author.guild_permissions.manage_roles,
        # 'manage_threads': message.author.guild_permissions.manage_threads,
        'manage_webhooks': message.author.guild_permissions.manage_webhooks,
        'mention_everyone': message.author.guild_permissions.mention_everyone,
        # 'moderate_members': message.author.guild_permissions.moderate_members,
        'move_members': message.author.guild_permissions.move_members,
        'mute_members': message.author.guild_permissions.mute_members,
        'priority_speaker': message.author.guild_permissions.priority_speaker,
        'read_message_history': message.author.guild_permissions.read_message_history,
        'read_messages': message.author.guild_permissions.read_messages,
        'request_to_speak': message.author.guild_permissions.request_to_speak,
        'send_messages': message.author.guild_permissions.send_messages,
        # 'send_messages_in_threads': message.author.guild_permissions.send_messages_in_threads,
        'send_tts_messages': message.author.guild_permissions.send_tts_messages,
        'speak': message.author.guild_permissions.speak,
        'stream': message.author.guild_permissions.stream,
        # 'use_application_commands': message.author.guild_permissions.use_application_commands,
        # 'use_embedded_activities': message.author.guild_permissions.use_embedded_activities,
        'use_external_emojis': message.author.guild_permissions.use_external_emojis,
        # 'use_external_stickers': message.author.guild_permissions.use_external_stickers,
        'use_voice_activation': message.author.guild_permissions.use_voice_activation,
        'value': message.author.guild_permissions.value,
        'view_audit_log': message.author.guild_permissions.view_audit_log,
        'view_channel': message.author.guild_permissions.view_channel,
        'view_guild_insights': message.author.guild_permissions.view_guild_insights
    }

    client.has_perm = True

    async def check_perm(permiss):
        if not permissions[str(permiss)]:
            if message.author.id == DEVELOPER_ID:
                client.has_perm = True

            else:
                if fail_message:
                    await message.reply(fail_message, delete_after=time)
                    await delete_message(message, time)

                client.has_perm = False
                
        return client.has_perm

    try:
        for perm in permission_type:
            if await check_perm(perm):
                break
    except:
        await check_perm(permission_type)

    return client.has_perm


def multiple_replace(characters:str, new_character:str, string_to_change:str):
    for char in characters:
        string_to_change = string_to_change.replace(char, new_character)

    return string_to_change


class Cooldown():
    def __init__(self, time):

        self.clock, self.time = time, time


    async def clocking(self):
        for _ in range(self.time):
            await sleep(1)
            self.clock -= 1

        self.clock = self.time


def send_request(request_call, index, var_type=None):
    send_request = var_type if len(request_call) <= index else request_call[index]

    return send_request


def better_date_n_time():
    date = datetime.today()
    time = datetime.now()

    datetime_values = [str(date.day), str(date.month), str(time.hour), str(time.minute), str(time.second)]

    for value in datetime_values:
        datetime_values[datetime_values.index(value)] = value if int(value) >= 10 else '0' + value

    date = f'{datetime_values[0]}/{datetime_values[1]}/{date.year}'
    time = f'{datetime_values[2]}:{datetime_values[3]}:{datetime_values[4]}'

    return date, time


async def user_object(message, user_id):
    user = await message.guild.query_members(user_ids=[user_id])
    user = user[0]

    return user[0]


def len_duplicates(list, value_to_find):
    duplicates_length = 0

    for value in list:
        if value == value_to_find:
            duplicates_length += 1

    return duplicates_length


def remove_duplicates(list):
    unduplicated = []

    for value in list:
        if value not in unduplicated:
            unduplicated.append(value)

    return unduplicated


randomcolor = int(hex(randint(0, 16777215)), 0)

empty_text = '‏‏‎ ‎'