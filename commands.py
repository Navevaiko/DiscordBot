from discord.ext import commands
import game
import utils

challenged_user_id = 0

@commands.command()
async def play(ctx, invited_user):
  global challenged_user_id

  if utils.get_id_from_mention(invited_user) == ctx.author.id:
    await ctx.send('Você não pode jogar consigo mesmo!')
    return
  
  game.add_user(ctx.author.id, True)
  challenged_user_id = utils.get_id_from_mention(invited_user)

  await ctx.send(f'{invited_user} o usuário <@{ctx.author.id}> está te desafiando para uma partida de Jogo da Velha!\nPara aceitar use o comando !accept')

@commands.command()
async def accept(ctx):
  if ctx.author.id == challenged_user_id:
    game.add_user(ctx.author.id, True)
    game.init_game()

    current_player_id = game.get_current_player()['id']

    await ctx.send('Iniciando jogo')
    await ctx.send(f'Vez do <@{current_player_id}>. Use o comando !place [linha] [coluna] para jogar')

    await game.print_board(ctx)

@commands.command()
async def place(ctx, row:int, column:int):
  current_player_id = game.get_current_player()['id']

  if not (1 <= row <= game.ROW_SIZE) or not (1 <= column <= game.COLUMN_SIZE):
    await ctx.send(f'Posição inválida. Digite uma posição entre 1 e {game.COLUMN_SIZE}')
    return

  if not game.position_available(row, column):
    await ctx.send(f'Posição não disponível, escolha outra <@{ctx.author.id}>')
    return

  if current_player_id == ctx.author.id:
    game.add_to_board(row - 1, column - 1, ctx.author.id)
    winner = game.check_winner(current_player_id)
    
    await game.print_board(ctx)

    if winner != None:
      winner_id = winner['id']
      await ctx.send(f'<@{winner_id}> ganhou!!')
      game.end_game()
      return
  else:
    await ctx.send(f'Não é sua vez <@{ctx.author.id}>')

  current_player_id = game.get_current_player()['id']
  await ctx.send(f'Vez do <@{current_player_id}>. Use o comando !place [linha] [coluna] para jogar')

@commands.command()
async def end(ctx):
  await ctx.send('Jogo finalizado!')
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