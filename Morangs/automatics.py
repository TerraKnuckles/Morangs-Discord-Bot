from discord import ChannelType, Embed
from random import choice
from unidecode import unidecode

from core import client
from content import GetEmoji
from _package.discord_essentials import permission


class Automatic():
    def __init__(self, message):
        
        self.context = message
        self.author = message.author
        self.channel = message.channel
        self.guild = message.channel.guild
        self.content = str(message.content)
        

    async def message_log(self):
        if self.author.id != client.user.id:
            print(f'{self.author}: {self.content}')
        
        if self.channel.type is ChannelType.private:
            embed = Embed(color=0xffd500)
            embed.set_author(name=self.author, icon_url=self.author.avatar_url)
            embed.set_thumbnail(url=self.author.avatar_url)
            embed.add_field(name='Mensagem:', value=f'{self.content}', inline=False)
           
            await client.get_channel(866509934081605632).send(embed=embed)
        
        else:
            if self.channel.id in (856738722766913586, 866509934081605632) or self.guild.id in (1000612960428888064, 982120912398745683):
                return
            
            try:
                embed = Embed(title=f'Servidor: {self.guild.name}', description=f'**User:** {self.author} │ **Chat:** {self.channel.name} {self.channel.id}', color=0xffd500)
                embed.add_field(name=f'Mensagem: {self.context.id}', value=f'{self.content}', inline=False)
                
                await client.get_channel(856738722766913586).send(embed=embed)
            
            except:
                pass
    
    
    async def add_reaction_to(self):
        unaccented_msg = unidecode(self.content.lower())
        morangs_reactions = choice(('🍓', '❤️', '🌟', '🍰', GetEmoji.cupcake[1], '🍦', '🍪', '🍮', '🍧', '🍫', '🍵', '🍡', '🍩', '🍯'))
        
        if 'morang' in unaccented_msg.replace(' ', ''):
            print('Message reacted', morangs_reactions)
            await self.context.add_reaction(morangs_reactions)

    
    async def same_client_nickname(self):
        if self.context.webhook_id or self.channel.type is ChannelType.private:
            return
        elif self.author.nick in ('morang', client.user.name):
            print('same nickname detected!')
    
    
    async def block_links(self):
        try:
            permited_chats_file = open(f'Database/BlockLinksIn/{self.guild.id}.txt', 'r', encoding='utf-8')

        except:
            return

        permited_chats_list = permited_chats_file.read().split()
        permited_chats_file.close()

        if str(self.channel.id) not in permited_chats_list:

            if not self.author.bot or not await permission(self.context, 'administrator'):

                for word in self.content.split():

                    if 'http' in word and len(word) >= 9 and 'gif' not in word:
                        link_detection_msg = choice(('links não são permitidos nesse chat!', 'não mande links por favor.', 'Isso é um link? Nananinanão! Não pode!'))

                        await self.channel.send(f'<@{self.author.id}>, {link_detection_msg}')
                        await self.context.delete()

        
    async def update(self):
        await self.message_log()
        await self.add_reaction_to()
        await self.same_client_nickname()
        await self.block_links()