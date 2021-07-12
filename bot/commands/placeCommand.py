# from context import get_value, set_value
from discord.ext import commands

@commands.command()
async def place(ctx, row:int, column:int):
  '''
    Coloca a marca do usuário na posição informada 
  '''
  game = ctx.bot.game
  messages = ctx.bot.messages

  current_player_id = game.get_current_player()['id']

  if game.state == 0:
    await game.channel.send(messages.PLACE_NO_ONGOING_GAME_ERROR.value)
    return

  if not (1 <= row <= game.row_size) or not (1 <= column <= game.column_size):
    await game.channel.send(messages.PLACE_INVALID_POSITION_ERROR.value.format(game.column_size))
    return

  if not game.position_available(row, column):
    await game.channel.send(messages.PLACE_UNAVAILABLE_POSITION_ERROR.value.format(ctx.author.id))
    return

  if current_player_id == ctx.author.id:
    game.add_to_board(row - 1, column - 1, ctx.author.id)
    winner = game.check_winner(current_player_id)
    
    ctx.bot.game = game

    await game.print_board()

    if game.turn == 9:
      await game.channel.send(messages.PLACE_TIE_MESSAGE.value)
      ctx.bot.game = None
      return

    if winner != None:
      winner_id = winner['id']
      await game.channel.send(messages.PLACE_WIN_MESSAGE.value.format(winner_id))
      ctx.bot.game = None
      return
  else:
    await game.channel.send(messages.PLACE_NOT_YOUR_TURN.value.format(ctx.author.id))

  current_player_id = game.get_current_player()['id']
  await game.channel.send(messages.ACCEPT_TURN_MESSAGE.value.format(current_player_id))

@place.error
async def handle_place_error(ctx, error):
  messages = ctx.bot.messages
  
  if isinstance(error, commands.errors.MissingRequiredArgument):
    await ctx.send(messages.PLACE_MISSING_PARAM_ERROR.value)
  elif isinstance(error, commands.errors.CommandInvokeError) or isinstance(error, commands.errors.BadArgument):
    await ctx.send(messages.PLACE_INVALID_PARAM_ERROR.value)