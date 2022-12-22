from discord.ext import commands
from discord import Intents


PREFIX = ':'

client = commands.Bot(command_prefix=PREFIX, case_insensitive=True, intents=Intents.all())
client.remove_command('help')

DEVELOPER_ID = 441735023310143491

morangs_id = 511312830209851413

TOKEN = 'token'
