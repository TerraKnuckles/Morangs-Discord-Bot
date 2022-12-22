import discord
from traceback import print_exc
from aiohttp import ClientSession
from random import randint, choice
from requests import get
from os import startfile, path, remove
from sys import exit
from time import sleep
from unidecode import unidecode

from core import client, DEVELOPER_ID, morangs_id, PREFIX
from content import GetEmoji, StorageValues
import _package.discord_essentials as dses


class Commands():
    def __init__(self, message, has_prefix):
        
        self.context = message
        self.author = message.author
        self.channel = message.channel
        self.guild = message.channel.guild
        self.content = str(message.content)
        self.has_prefix = bool(has_prefix)

        if len(self.content) > 0:
            self.command = ''.join(self.content.split()[0]).replace(PREFIX, '')
        else:
            self.command = 'command_nullified'
            # It nullify the value because when the bot reads an attachment, it doesn't contain any text, so it can't have a command.

        self.uncommanded_content = dses.multiple_replace(['>', self.command], '', self.content).strip()

        self.parameter = self.content.split()[1:]
        for _ in range(5-len(self.parameter)):
            self.parameter.append(None)


    # # #
    # COMMON COMMANDS
    # # #
    async def invite(self):
        if self.command == 'invite':

            embed = discord.Embed(title='Quer me convidar para um servidor? Aqui está o meu link!',
                    url=f'https://discordapp.com/oauth2/authorize?client_id={morangs_id}&scope=bot&permissions=8',
                    description='⬆️ Clique na frase azul acima para ser redirecionado ao link.',
                    color=0x007bff)

            await self.channel.send(embed=embed)


    async def server_image(self):
        if self.command in ('serverpic', 'serverimg', 'serveravatar'):

            embed = discord.Embed(description=f'Ícone do servidor: **{self.guild.name}**',color=0x00eaff)
            embed.set_image(url=self.guild.icon_url)

            await self.channel.send(embed=embed)
    

    async def user_avatar(self, get_user=None):
        if self.command in ('userpic', 'userimg', 'useravatar'):

            if get_user:
                user_id = dses.multiple_replace('<>@!', '', get_user)

            else:
                user_id = self.author.id

            user = await self.guild.query_members(user_ids=[user_id])
            user = user[0]

            embed = discord.Embed(description=f'Avatar de: <@{user.id}>',color=0x00eaff)
            embed.set_image(url=user.avatar_url)

            await self.channel.send(embed=embed)


    async def report(self, report):
        if self.command == 'report':

            embed = discord.Embed()

            embed.set_author(name=f'👤 {self.author}\n💻 {self.guild.name}', icon_url=self.author.avatar_url)
            embed.set_thumbnail(url=self.guild.icon_url)

            embed.add_field(name='Informações do Usuário:', value=f'- *ID:* `{self.author.id}`\n- *IsBOT:* `{self.author.bot}`\n- *CanManageRoles:* `{self.author.guild_permissions.manage_roles}`', inline=True)
            embed.add_field(name='Informações do Servidor:', value=f'- *ServerID:* `{self.guild.id}`\n- *ChatName:* `{self.channel.name}`\n- *ChatID:* `{self.channel.id}`', inline=True)
            embed.add_field(name='Relatório de erro:', value=f'```{report}```', inline=False)

            date_n_time = dses.better_date_n_time()
            embed.set_footer(text=f'{date_n_time[1]} - {date_n_time[0]}')

            await client.get_channel(856624996683218984).send(embed=embed)
            await self.context.reply('Relatório de erro registrado.', delete_after=3)
            await dses.delete_message(self.context, 3)

    
    async def rock_paper_scissors(self, user_play):
        if dses.multiple_replace((':', 'news', '2', 'roll_of_'), '', self.command) in ('pedra', 'papel', 'tesoura', 'rock', 'paper', 'scissors'):

            user_play = dses.multiple_replace((':', 'news', '2', 'roll_of_'), '', user_play)
            client_play = choice(('pedra', 'papel', 'tesoura'))

            client_tie = choice(('Oh, empate.', 'Ih... Mais um empate.', '||https://tenor.com/view/empatamo-neymar-gif-18450271||'))
            client_win = choice(('GANHEI!!', 'YAY! MAIS UMA VITÓRIA!', '||https://media.tenor.com/GaD3ptFz71MAAAAd/ganhamo-cr7.gif||'))
            client_lose = choice(('Ah... Você ganhou.', 'Você levou essa... Parabéns.', '||https://tenor.com/view/perdemo-bielreispro-gif-18585028||'))

            # USER ROCK
            if user_play in ('pedra', 'rock') and client_play == 'pedra':
                await self.context.reply(f'**{client_play.upper()}!** {client_tie}')

            elif user_play in ('pedra', 'rock') and client_play == 'papel':
                await self.context.reply(f'**{client_play.upper()}!** {client_win}')

            elif user_play in ('pedra', 'rock') and client_play == 'tesoura':
                await self.context.reply(f'**{client_play.upper()}!** {client_lose}')

            # USER PAPER
            elif user_play in ('papel', 'paper') and client_play == 'pedra':
                await self.context.reply(f'**{client_play.upper()}!** {client_lose}')

            elif user_play in ('papel', 'paper') and client_play == 'papel':
                await self.context.reply(f'**{client_play.upper()}!** {client_tie}')

            elif user_play in ('papel', 'paper') and client_play == 'tesoura':
                await self.context.reply(f'**{client_play.upper()}!** {client_win}')

            # USER SCISSORS
            elif user_play in ('tesoura', 'scissors') and client_play == 'pedra':
                await self.context.reply(f'**{client_play.upper()}!** {client_win}')

            elif user_play in ('tesoura', 'scissors') and client_play == 'papel':
                await self.context.reply(f'**{client_play.upper()}!** {client_lose}')

            elif user_play in ('tesoura', 'scissors') and client_play == 'tesoura':
                await self.context.reply(f'**{client_play.upper()}!** {client_tie}')


    async def morse_code(self, normal_text):
        if self.command in ('morse', 'morsecode', 'codifymorse'):

            embed = discord.Embed(description='Codificando...', color=0x4287f5)
            encoding_msg = await self.channel.send(embed=embed)

            try:
                morse_code_dict = {'a': '.-', 'b': '-...', 'c': '-.-.', 'd': '-..', 'e': '.', 'f': '..-.', 'g': '--.', 'h': '....', 'i': '..', 'j': '.---',
                    'k': '-.-', 'l': '.-..', 'm': '--', 'n': '-.', 'o': '---', 'p': '.--.', 'q': '--.-', 'r': '.-.', 's': '...', 't': '-', 'u': '..-', 'v': '...-',
                    'w': '.--', 'x': '-..-', 'y': '-.--', 'z': '--..',
                    '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....', '6': '-....', '7': '--...', '8': '---..', '9': '----.', '0': '-----',
                    '.': '.-.-.-', '?': '..--..', '!': '-.-.--', '"': '.-..-.', '&': '.-...',
                    ':': '---...', ';': '-.-.-.', '/': '-..-.', '_': '..--.-', '=': '-...-', '+': '.-.-.', '-': '-....-', '$': '...-..-', '@': '.--.-.',
                    ' ': '/'}

                normal_text = unidecode(normal_text).strip().lower()
                morse_text = ''

                for char in normal_text:
                    if char not in morse_code_dict.keys():
                        continue

                    morse_text += morse_code_dict[f'{char}'] + ' '

                embed.description = f'**Servidor:** __{self.guild.name}__'
                embed.set_author(name=self.author, icon_url=self.author.avatar_url)
                embed.add_field(name=dses.empty_text, value=morse_text)

                await encoding_msg.edit(embed=embed)

            except Exception:
                print_exc()
                embed.description = 'Falha ao converter o texto para código morse.'
                embed.color = 0xfc0303
                await encoding_msg.edit(embed=embed, delete_after=5)

    
    async def calculator(self, equation):
        if self.command in ('calc', 'calculator'):
            print(equation)

            try:
                solve_equation = equation

                for (key, value) in {'x': '*', ':': '/', '^': '**', ',': '.'}.items():
                    solve_equation = solve_equation.replace(key, value)

                await self.context.reply(eval(solve_equation))

            except Exception:
                print_exc()
                embed = discord.Embed(description=f'**{self.author.name}**, tem certeza de que a sua equação está certa?\nVerifique se não esqueceu parênteses, se eles têm sinais no começo e no final, e se não há letras e símbolos incomuns.\n\n- Sua equação: `{" ".join(equation)}`\n\n- Sinais válidos:\n```adição: +\nsubtração: -\nmultiplicação: x , *\ndivisão: / , // , :\npotenciação: ** , ^```', color=0x364206)
                await self.channel.send(embed=embed)


    async def truth_or_dare(self, players:list):
        if self.command in ('verdadeoudesafio', 'vod', 'tod', 'truthordare'):

            # remove nonetypes
            for _ in range(dses.len_duplicates(players, None)):
                players.remove(None)

            players = dses.remove_duplicates(players)
            questioner = choice(players)
            players.remove(questioner)
            challenged = choice(players)

            embed = discord.Embed(description=f'{questioner} pergunta ou desafia {challenged}.', color=dses.randomcolor)
            
            await self.channel.send(embed=embed)


    async def heads_or_tails(self, user_choice):
        if self.command.replace('s', '') in ('cara', 'coroa', 'head', 'tail'):

            result = choice((['cara', 'head'], ['coroa', 'tail']))
            reply_message = choice(('Seu resultado foi', 'Caiu', 'O lado que caiu foi'))

            result_message = 'cara' if 'cara' in result else 'coroa'
            win_o_lose = '! 🌟' if user_choice in result else '.'

            await self.channel.send(f'{GetEmoji.coin} {reply_message} **{result_message}**{win_o_lose}')


    async def roll_dice(self, request):
        if 'd' in self.content.lower():

            try:    
                def roll_the_dice(quantity, max, operation):
                    dices_list = list(); dices_sum = int()

                    for _ in range(quantity):
                        dice = randint(1, max) # rolls the dice
                        apnd_dice = dice if dice != max else f'{dice}🌟'
                        dices_list.append(apnd_dice); dices_sum += dice # appends/adds the results of the dices

                    opr_result = eval(str(dices_sum) + operation)
                    opr_result = f'**{opr_result}** 🌟' if quantity == 1 and opr_result >= max else opr_result
                    dices_list = str(dices_list).replace("'", '')

                    return dices_list, opr_result

                if request[0] == '0':
                    return

                mathsym = '+-*/%'

                for sym in mathsym: # gets the math symbol position
                    math = request.find(sym)
                    if math != -1:
                        break

                operation = request[math:] if math != -1 else '+0' # represents the numbers after the math symbol *and the symbol*
                d = request.find('d') # represents the index position of the d
                quantity = request[:d] if d > 0 else 1 # the quantity of dices that will be rolled
                max = str() # the maximum value of the dice

                for char in request[d+1:]: # gets the dice max value
                    if char in mathsym:
                        break

                    else:
                        max = max + char

                if int(quantity) > 500:
                    await self.context.reply('Pra que você quer usar tudo isso de dado? Nada feito!')
                    return

                dices_list, opr_result = roll_the_dice(int(quantity), int(max), str(operation))
                if len(dices_list) >= 2000:
                    await self.context.reply('Que? Nãoo! Essa mensagem é muito grande pra enviar!')
                    return

                request = request if '**' not in request else request.replace('**', '^')
                await self.context.reply(f'🎲 **{request}** = {opr_result}\n`{dices_list}`')

            except:
                pass


    async def mention_quick_help(self, content):
        if content in (f'<@!{morangs_id}>', f'<@{morangs_id}>'):

            random_message = choice(('Oieee! Precisa de um `=help`?',
                                            'Yo! Tá precisando de `=ajuda`?',
                                            'Eae! Dica do dia: uma `=ajuda` é sempre bem vinda!',
                                            'Oi! Tá procurando por diversão? Posso te mostrar meus `=comandos` se quiser!',
                                            'Chamou?! Ei ei, você sabe que todos os bots têm `=comandos` né? Comigo não é diferente!',
                                            'Alguém me mencionou...  EI VOCÊ! Precisa de `=ajuda` com algo?'))
            
            await self.channel.send(random_message)


    # # #
    # ADMIN COMMANDS
    # # #
    async def ban_unban_member(self, ban_unban_banlist, get_user=None):
        if self.command in ('ban', 'unban', 'bannedlist', 'listbans'):

            if not await dses.permission(self.context, 'ban_members', 'Você não tem permissão para gerenciar banimentos!'): return

            user_id = dses.multiple_replace('<>@!', '', get_user) if get_user else None
            guild_banned_users = await self.guild.bans()

            if ban_unban_banlist == 'ban':
                await self.guild.ban(await client.fetch_user(int(user_id)))
                await self.channel.send(f'<@{user_id}> foi simbora!', delete_after=30)

            elif ban_unban_banlist == 'unban':
                if len(get_user) <= 5:
                    for entry in guild_banned_users:
                        if guild_banned_users.index(entry)+1 == int(get_user):
                            banned_id = entry.user.id
                            break

                else:
                    banned_id = get_user

                await self.guild.unban(await client.fetch_user(int(banned_id)))
                await self.channel.send(f'Certo. Vamos perdoar <@{banned_id}>.', delete_after=30)

            elif ban_unban_banlist in ('bannedlist', 'listbans'):
                embed = discord.Embed(title=f'Usuários banidos em __{self.guild.name}__:', color=0x424242)

                if len(guild_banned_users) >= 1:
                    for entry in guild_banned_users:
                        bot_boolean = GetEmoji.robot if entry.user.bot else '👤'
                        embed.add_field(name=f'__*{guild_banned_users.index(entry)+1}*.__  {entry.user.name}', value=f'*id=*`{entry.user.id}` **|** *user=*`{entry.user}` **|** {bot_boolean}', inline=False)
                        embed.set_footer(text='Esta mensagem será deletada em 2 minutos.')

                else:
                    embed.title = 'Não há usuários banidos.'

                banned_list_msg = await self.channel.send(embed=embed)
                await dses.delete_message((self.context, banned_list_msg), 120)


    async def mute_deafen(self, mute_deaf, get_user):
        if self.command in ('mute', 'deafen', 'deaf', 'silenciar', 'ensurdecer'):

            user_id = dses.multiple_replace('<>@!', '', get_user)
            user = await self.guild.query_members(user_ids=[user_id])
            user = user[0]

            true_false = True
            on_off = 'ativado'

            if mute_deaf in ('mute', 'silenciar'):
                if not await dses.permission(self.context, 'mute_members', 'Você não tem permissão para silenciar membros!'):
                    return

                if user.voice.mute:
                    true_false = False
                    on_off = 'desativado'

                await user.edit(mute=true_false)

            elif mute_deaf in ('deafen', 'deaf', 'ensurdecer'):
                if not await dses.permission(self.context, 'deafen_members', 'Você não tem permissão para ensurdecer membros!'):
                    return

                if user.voice.deaf:
                    true_false = False
                    on_off = 'desativado'

                await user.edit(deafen=true_false)

            await self.channel.send(f'{mute_deaf.capitalize()} {on_off} em {user}. {GetEmoji.microphone2[1]}🎧', delete_after=15)
            await dses.delete_message(self.context, 15)


    async def move_user(self, get_user, get_channel:int):
        if self.command == 'move':

            user_id = dses.multiple_replace('<>@!', '', get_user)
            user = await self.guild.query_members(user_ids=[user_id])
            user = user[0]
            voice_channel = discord.utils.get(self.guild.voice_channels, name=get_channel)

            await user.move_to(voice_channel)


    async def change_user_nickname(self, get_user, nickname, guild_id=None):
        if self.command.replace('name', '') in ('changenick', 'usernick'):

            user_id = dses.multiple_replace('<>@!', '', get_user)
            nickname = '' if nickname == '#' else nickname
            guild_id = self.guild.id if not guild_id else guild_id

            guild = client.get_guild(guild_id)

            await guild.get_member(user_id).edit(nick=nickname)
            await self.channel.send('Nickname alterado.', delete_after=3)


    async def add_emoji(self, emoji_name, emoji_url=None):
        if self.command == 'addemoji':

            try:
                if not await dses.permission(self.context, 'manage_emojis', 'Você não tem permissão para gerenciar emojis!'):
                    return

                if path.isfile("emoji.png"):
                    remove("emoji.png")

                if not emoji_url:
                    emoji_url = self.context.attachments[0].url

                with open('emoji.png', 'wb') as emoji_handler:
                    emoji_handler.write(get(emoji_url).content)
                    emoji_handler.close()

                with open('emoji.png', 'rb') as emoji_image:
                    await self.guild.create_custom_emoji(name=emoji_name, image=emoji_image.read())
                    emoji_image.close()

                await self.channel.send(f'Emoji **{emoji_name}** adicionado ao servidor!', delete_after=15)
                await dses.delete_message(self.context, 15)

            except Exception:
                print_exc()
                await self.channel.send(f'Sorry, eu não estou conseguindo entender...\nTente: `a=add_emoji (nome do emoji) (link da imagem)`', delete_after=10)
                await dses.delete_message(self.context, 10)


    async def clear_messages(self, amount=0):
        if self.command in ('clear', 'limpar'):

            if not await dses.permission(self.context, 'manage_messages', 'Você não tem permissão para gerenciar mensagens!'):
                pass

            amount = int(amount)

            if amount <= 0:
                await self.channel.send('Ok, mas... Quantas mensagens quer deletar? Eu preciso saber a quantidade de mensagens!\nUse `a=clear (número)`')
                pass

            await self.channel.purge(limit=amount+1)

            plural = ('mensagens', 'foram', 'reduzidas', 'enviadas', 'tiveram', 'sumiram') if amount > 1 else ('mensagem', 'foi', 'reduzida', 'enviada', 'teve', 'sumiu')
            random_message = choice((f'{plural[1]} {plural[2]} em poeira!', f'{plural[1]} {plural[3]} para outra dimensão!',
                                            f'{plural[4]} suas moléculas destruídas!', f'{plural[5]} para sempre! Tipo... Sempre mesmo!'))
            
            await self.channel.send(f'**{amount}** {plural[0]} {random_message}')


    # # #
    # DEVELOPER COMMANDS
    # # #
    async def shutdown(self):
        if self.command == 'shutdown':

            await self.context.add_reaction('⛔')
            await client.change_presence(status=discord.Status.offline, activity=discord.Activity(name='', type=0))
            exit()


    async def change_client_nickname(self, nick, guild_id:int=None):
        if self.command.replace('name', '') in ('selfnick', 'clientnick', 'mynick'):

            try:
                if nick == '#':
                    nick = ''

                if guild_id:
                    guild = client.get_guild(guild_id)
                else:
                    guild = client.get_guild(self.guild.id)

                await guild.get_member(morangs_id).edit(nick=nick)
                await self.channel.send('Nickname alterado.', delete_after=3)

            except Exception:
                print_exc()
                await self.channel.send(f'Sou só eu ou está difícil de ler?\nTente: `=clientnick (nick) (opt: guild_id)`', delete_after=10)
                await dses.delete_message(self.context, 10)


    async def restart_execution(self):
        if self.command == 'restart':

            await self.context.add_reaction('🔄')
            await client.change_presence(status=discord.Status.dnd, activity=discord.Activity(name='Reiniciando...', type=3))

            startfile('main.py')
            sleep(2.5)

            await client.change_presence(status=discord.Status.offline, activity=discord.Activity(name='', type=0))
            exit()


    async def change_activity(self, activity_type:int, activity_name):
        if self.command in ('changeactivity', 'status'):

            try:
                activity_name = " ".join(activity_name).strip()

                if len(activity_name) > 24:
                    await self.channel.send('⚠️ __activity_name__ muito grande para ser mostrada.', delete_after=5)
                    await dses.delete_message(self.context, 5)
                    return

                await client.change_presence(status=discord.Status.online, activity=discord.Activity(name=activity_name, type=activity_type))
                await self.channel.send('Atividade alterada!', delete_after=15)
                await dses.delete_message(self.context, 15)

            except Exception:
                print_exc()
                await self.channel.send(f'Isto está meio confuso pra mim...\nTente: `d=change_activity (activ_type_num) (activity_name)`', delete_after=10)
                await dses.delete_message(self.context, 10)


    async def leave_from_guild(self, guild_id):
        if self.command in ('leaveguild', 'guildleave'):

            server = client.get_guild(int(guild_id))
            await server.leave()
            await self.channel.send(f'Saindo de {server.name}!')


    async def get_guild_information(self, guild_id):
        if self.command in ('getinfo', 'guildinfo', 'serverinfo'):

            guild = client.get_guild(int(guild_id))

            dev_user = await self.guild.query_members(user_ids=[DEVELOPER_ID])
            dev_user = dev_user[0]

            invite_link = await guild.text_channels[0].create_invite(max_uses = 1, max_age = 0)
            invite_link = str(invite_link).replace('https://discord.gg/', '')

            embed = discord.Embed()
            embed.set_author(name=f'👤 {guild.owner}\n💻 {guild.name}', icon_url=guild.owner.avatar_url)
            embed.set_thumbnail(url=guild.icon_url)
            embed.add_field(name='Informações do Servidor:', value=f'''- *guildID:* `{guild.id}`
                                                                    - *OwnerID:* `{guild.owner.id}`
                                                                    - *Lengths:* `📄{len(guild.text_channels)} 🎧{len(guild.voice_channels)} 👥{len(guild.members)}`
                                                                    - *IsDevIn:* `{dev_user in guild.members}`
                                                                    - *InviteLink:* `{invite_link}`
                                                                    ''', inline=True)
            embed.add_field(name='Informações do Usuário:', value=f'- *ID:* `{self.author.id}`\n- *IsBOT:* `{self.author.bot}`\n- *CanManageRoles:* `{self.author.guild_permissions.manage_roles}`', inline=True)

            await self.channel.send(embed=embed)


    async def get_audit_logs(self):
        if self.command == 'auditlog':

            with open('temporary_audit_log.txt', 'w+', encoding='utf-8') as audit_logs_file:
                async for entry in self.guild.audit_logs(limit=100):
                    audit_logs_file.write('{0.user} did {0.action} to {0.target}\n'.format(entry))

            await self.channel.send(f'Os registros de auditoria de {self.guild.name} foram salvos!', delete_after=5)


    async def webhook_send_message(self, name, text):
        if self.command in ('webhook', 'wh', 'wbh'):

            webhook_dictionary = {
                'rash': {
                    'username': 'RashySketchy',
                    'avatar_url': 'https://media.discordapp.net/attachments/596147565376962571/1008902956986400799/unknown.png?width=194&height=194',
                    'webhook_url': 'https://discord.com/api/webhooks/999430811457695876/UIJdXbGPssvTgrWmrc0X8uaCy-mUSFBhwxWgNJU2TeHCZQ6qqfhE9ebyGLbBUcqhUhMX'
                },
                'senhor': {
                    'username': 'Phill',
                    'avatar_url': 'data:image/jpeg;base64,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',
                    'webhook_url': 'https://discord.com/api/webhooks/999430811457695876/UIJdXbGPssvTgrWmrc0X8uaCy-mUSFBhwxWgNJU2TeHCZQ6qqfhE9ebyGLbBUcqhUhMX'
                }
            }
            using_webhook = webhook_dictionary[name]


            text = ' '.join(text)
            async with ClientSession() as session:
                webhook = discord.Webhook.from_url(using_webhook['webhook_url'], adapter=discord.AsyncWebhookAdapter(session))
                await webhook.send(text, username=using_webhook['username'], avatar_url=using_webhook['avatar_url'])
            await self.context.delete()


    async def gentalha(self, content):
        if content.lower() == 'vamos morangs! não se junte com essa gentalha!':

            if self.author.id == DEVELOPER_ID:
                await self.channel.send('GENTALHA GENTALHA, PRLRLRLR')
                await self.guild.leave()

            elif StorageValues.gentalha_cooldown.clock >= 14400:
                randomize_msg = choice(('Você não pode usar esse comando...', 'Ei! Você não tem permissão para isso!'))
                await self.channel.send(randomize_msg)
                await StorageValues.gentalha_cooldown.clocking()


    async def send_messages(self, get_message):
        if self.channel.id == 990715648860651561:

            context = get_message.split()

            if context[0] == 'setchat':
                StorageValues.send_messages_chat = client.get_channel(int(context[1]))

                embed = discord.Embed(color=dses.randomcolor)
                embed.add_field(name='Especificado:', value=f'• {StorageValues.send_messages_chat.name}\n• {StorageValues.send_messages_chat.guild}', inline=False)

                await self.channel.send(embed=embed)
                return

            elif context[0] == 'reply':
                reply_message = await StorageValues.send_messages_chat.fetch_message(int(context[1]))
                await reply_message.reply(' '.join(context[2:]))

            else:
                await StorageValues.send_messages_chat.send(' '.join(context))

    
    async def list_guild_channels(self, guild_id):
        if self.command in ('listchats', 'chatlist', 'channellist', 'listchannels'):

            guild = client.get_guild(int(guild_id))
            embed = discord.Embed(color=dses.randomcolor)

            channels_string = str()
            for chat in guild.text_channels:
                channels_string += f'`{chat.id}` | **{chat.name}**\n'

            embed.add_field(name=f'__*Chats em {guild.name}:*__', value=channels_string, inline=False)

            await self.channel.send(embed=embed)


    async def get_guild_invite_link(self, guild_id):
        if self.command in ('guildinvitelink', 'guildlink', 'serverlink', 'serverinvitelink', 'createlink', 'createinvitelink'):
            
            guild = client.get_guild(int(guild_id))
            invite_link = await guild.text_channels[0].create_invite(max_uses = 1, max_age = 0)

            await self.channel.send(f'**Here is your invite link!** -> {invite_link}')


    async def update(self):

        if self.has_prefix:
            await self.invite()
            await self.server_image()
            await self.user_avatar(self.parameter[0])
            await self.report(self.uncommanded_content)
            await self.rock_paper_scissors(self.command)
            await self.morse_code(self.uncommanded_content)
            await self.calculator(self.uncommanded_content)
            await self.truth_or_dare(self.parameter)
            await self.heads_or_tails(self.command)
            await self.ban_unban_member(self.command, self.parameter[0])
            await self.mute_deafen(self.command, self.parameter[0])
            await self.move_user(self.parameter[0], self.parameter[1])
            await self.change_user_nickname()
            await self.add_emoji(self.parameter[0], self.parameter[1])
            await self.clear_messages(self.parameter[0])

        # NO PREFIX
        await self.roll_dice(self.content)
        await self.mention_quick_help(self.content)

        if self.author.id == DEVELOPER_ID:

            if self.has_prefix:
                await self.shutdown()
                await self.change_client_nickname(self.parameter[0], self.parameter[1])
                await self.restart_execution()
                await self.change_activity(self.parameter[0], self.parameter[1])
                await self.leave_from_guild(self.parameter[0])
                await self.get_guild_information(self.parameter[0])
                await self.get_audit_logs()
                await self.webhook_send_message(self.parameter[0], self.parameter[1])
                await self.list_guild_channels(self.parameter[0])
                await self.get_guild_invite_link(self.parameter[0])

            # NO PREFIX
            await self.gentalha(self.content)
            await self.send_messages(self.content)
