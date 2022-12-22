from discord import Status, Activity, Embed
from discord.utils import find

from core import client
import _package.discord_essentials as dses


class Event:


    @client.event
    async def on_ready():
        print(f'Sistema iniciado! {client.user.name} atualmente acordada!')
        embed = Embed(title=f'Ativada!', color=0x03f8fc)
        embed.description = '__*Amorii is now running!*__'
        date_n_time = dses.better_date_n_time()
        embed.set_footer(text=f'Inicialização: {date_n_time[1][:5]} - {date_n_time[0]}')
        await client.get_channel(856601441820737548).send(embed=embed)
        await client.change_presence(status=Status.online, activity=Activity(name='seus comandos!', type=3))


    @client.event
    async def on_guild_join(guild):

        async def send_join_message(channel):
            await channel.send(f'**{guild.name}** invadido pela Morangs!  🍓')
            print(f'{guild.name} foi invadido!')

        geral = find(lambda chat: chat.name in ['geral', 'general'], guild.text_channels)

        if geral and geral.permissions_for(guild.me).send_messages:
            await send_join_message(geral)

        else:
            for channel in guild.text_channels:
                if channel.permissions_for(guild.me).send_messages:
                    await send_join_message(channel)
                    break
