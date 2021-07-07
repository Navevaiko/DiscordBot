from discord.ext import commands
from context import gameContext
from models.GameModel import Game

@commands.command()
async def accept(ctx):
  '''
    Aceita o desafio (se houver algum)
  '''
  game = gameContext.get()

  if ctx.author.id == game.challenged_user_id:
    channel_name = f'game-{random.randint(1, 1000)}'
    game.channel = await ctx.message.guild.create_text_channel(channel_name)

    game.add_user(ctx.author.id)
    game.init_game()

    current_player_id = game.get_current_player()['id']

    await game.channel.send('Iniciando jogo')
    await game.channel.send(f'Vez do <@{current_player_id}>. Use o comando !place [linha] [coluna] para jogar')

    await game.print_board()
  else:
    await ctx.send('Você não tem nenhum desafio para aceitar!')