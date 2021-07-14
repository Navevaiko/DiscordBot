from discord.ext import commands
from models.main import Invite
from utils import get_game_by_players, get_id_from_mention, get_invite_by_players

@commands.command()
async def play(ctx, invited_user):
  '''
    Convida usuário para uma partida
  '''
  messages = ctx.bot.messages
  challenged_user_id = get_id_from_mention(invited_user)
  
  await ctx.bot.fetch_user(challenged_user_id)

  if challenged_user_id == ctx.author.id:
    await ctx.send(messages.PLAY_SAME_PLAYER_ERROR.value)
    return

  if get_game_by_players(ctx.bot.games, ctx.author.id, challenged_user_id) != None:
    await ctx.send(messages.PLAY_IN_PROGRESS_GAME_ERROR.value)
    return

  invite = get_invite_by_players(ctx.bot.pending_invites, ctx.author.id, challenged_user_id)
  if invite  != None:
    await ctx.send(messages.PLAY_IN_PROGRESS_GAME_ERROR.value)
    return
  
  invite = Invite(ctx.author.id, challenged_user_id)
  ctx.bot.pending_invites.append(invite)

  await ctx.send(messages.PLAY_CHALLEGING_MESSAGE.value.format(invited_user, ctx.author.id))

@play.error
async def handle_play_error(ctx, error):
  messages = ctx.bot.messages
  
  if isinstance(error, commands.errors.MissingRequiredArgument):
    await ctx.send(messages.PLAY_MISSING_PARAM_ERROR.value)
  elif isinstance(error, commands.errors.CommandInvokeError):
    await ctx.send(messages.PLAY_INVALID_PARAM_ERROR.value)
  