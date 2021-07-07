from discord.ext import commands
import random
import game
import utils

challenged_user_id = 0
channel = ''

@commands.command()
async def play(ctx, invited_user):
  global challenged_user_id

  if game.game_state != 0:
    await ctx.send('Há um jogo em andamento, utilize o comando !end para finalizar o jogo')
    return

  if utils.get_id_from_mention(invited_user) == ctx.author.id:
    await ctx.send('Você não pode jogar consigo mesmo!')
    return

  game.game_state = 1
  game.add_user(ctx.author.id, True)
  challenged_user_id = utils.get_id_from_mention(invited_user)

  await ctx.send(f'{invited_user} o usuário <@{ctx.author.id}> está te desafiando para uma partida de Jogo da Velha!\nPara aceitar use o comando !accept')

@commands.command()
async def accept(ctx):
  global challenged_user_id
  global channel

  if ctx.author.id == challenged_user_id:
    channel_name = f'game-{random.randint(1, 1000)}'
    channel = await ctx.message.guild.create_text_channel(channel_name)

    game.add_user(ctx.author.id, True)
    game.init_game()

    current_player_id = game.get_current_player()['id']

    await channel.send('Iniciando jogo')
    await channel.send(f'Vez do <@{current_player_id}>. Use o comando !place [linha] [coluna] para jogar')

    await game.print_board(channel)
  else:
    await ctx.send('Você não tem nenhum desafio para aceitar!')

@commands.command()
async def place(ctx, row:int, column:int):
  global channel
  
  current_player_id = game.get_current_player()['id']

  if game.game_state == 0:
    await channel.send('Não há um jogo em andamento, utilize o comando !end para finalizar o jogo')
    return

  if not (1 <= row <= game.ROW_SIZE) or not (1 <= column <= game.COLUMN_SIZE):
    await channel.send(f'Posição inválida. Digite uma posição entre 1 e {game.COLUMN_SIZE}')
    return

  if not game.position_available(row, column):
    await channel.send(f'Posição não disponível, escolha outra <@{ctx.author.id}>')
    return

  if current_player_id == ctx.author.id:
    game.add_to_board(row - 1, column - 1, ctx.author.id)
    winner = game.check_winner(current_player_id)
    
    await game.print_board(channel)

    if game.turn == 9:
      await channel.send(f'Deu velha!!')
      game.end_game()
      return

    if winner != None:
      winner_id = winner['id']
      await channel.send(f'<@{winner_id}> ganhou!!')
      game.end_game()
      return
  else:
    await channel.send(f'Não é sua vez <@{ctx.author.id}>')

  current_player_id = game.get_current_player()['id']
  await channel.send(f'Vez do <@{current_player_id}>. Use o comando !place [linha] [coluna] para jogar')

@commands.command()
async def end(ctx):
  await channel.send('Jogo finalizado!')
  await channel.delete()
  game.end_game()

@play.error
async def handle_play_error(ctx, error):
  if isinstance(error, commands.errors.MissingRequiredArgument):
    await ctx.send('É necessário passar um usuário para jogar com você!')
  elif isinstance(error, commands.errors.CommandInvokeError):
    await ctx.send('Usuário convidado é inválido!')
  
@place.error
async def handle_place_error(ctx, error):
  if isinstance(error, commands.errors.MissingRequiredArgument):
    await ctx.send('Passe a posição desejada!')
  elif isinstance(error, commands.errors.CommandInvokeError) or isinstance(error, commands.errors.BadArgument):
    await ctx.send('Linha ou coluna são inválidos!')