# from context import get_value, set_value
from discord.ext import commands

@commands.command()
async def place(ctx, row:int, column:int):
  pass
  '''
    Coloca a marca do usuário na posição informada 
  '''
  game = ctx.bot.game
  
  current_player_id = game.get_current_player()['id']

  if game.state == 0:
    await game.channel.send('Não há um jogo em andamento, utilize o comando !end para finalizar o jogo')
    return

  if not (1 <= row <= game.row_size) or not (1 <= column <= game.column_size):
    await game.channel.send(f'Posição inválida. Digite uma posição entre 1 e {game.column_size}')
    return

  if not game.position_available(row, column):
    await game.channel.send(f'Posição não disponível, escolha outra <@{ctx.author.id}>')
    return

  if current_player_id == ctx.author.id:
    game.add_to_board(row - 1, column - 1, ctx.author.id)
    winner = game.check_winner(current_player_id)
    
    ctx.bot.game = game

    await game.print_board()

    if game.turn == 9:
      await game.channel.send(f'Deu velha!!')
      game.end_game()
      return

    if winner != None:
      winner_id = winner['id']
      await game.channel.send(f'<@{winner_id}> ganhou!!')
      game.end_game()
      return
  else:
    await game.channel.send(f'Não é sua vez <@{ctx.author.id}>')

  current_player_id = game.get_current_player()['id']
  await game.channel.send(f'Vez do <@{current_player_id}>. Use o comando !place [linha] [coluna] para jogar')

@place.error
async def handle_place_error(ctx, error):
  print(error)
  if isinstance(error, commands.errors.MissingRequiredArgument):
    await ctx.send('Passe a posição desejada!')
  elif isinstance(error, commands.errors.CommandInvokeError) or isinstance(error, commands.errors.BadArgument):
    await ctx.send('Linha ou coluna são inválidos!')