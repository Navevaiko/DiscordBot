from discord.ext import commands
from models.main import Game
import utils

@commands.command()
async def play(ctx, invited_user):
  '''
    Convida usuário para uma partida
  '''
  messages = ctx.bot.messages
  challenged_user_id = utils.get_id_from_mention(invited_user)

  if challenged_user_id == ctx.author.id:
    await ctx.send(messages.PLAY_SAME_PLAYER_ERROR.value)
    return
  
  game = Game(challenged_user_id)

  if game.state != 0:
    await ctx.send(messages.IN_PROGRESS_GAME_ERROR.value)
    return

  game.add_user(ctx.author.id)
  
  ctx.bot.game = game
  final_message = messages.PLAY_CHALLEGING_MESSAGE.value.format(
      invited_user, 
      ctx.author.id
  )
  await ctx.send(final_message)

@play.error
async def handle_play_error(ctx, error):
  messages = ctx.bot.messages
  
  if isinstance(error, commands.errors.MissingRequiredArgument):
    await ctx.send(messages.PLAY_MISSING_PARAM_ERROR.value)
  elif isinstance(error, commands.errors.CommandInvokeError):
    await ctx.send(messages.PLAY_INVALID_PARAM_ERROR.value)
  