from discord.ext import commands
from utils import get_user_invites
from models.main import Game

@commands.command()
async def accept(ctx, option=0):
  '''
    Aceita o desafio (se houver algum)
  '''
  invites = ctx.bot.pending_invites
  messages = ctx.bot.messages

  user_invites = get_user_invites(invites, ctx.author.id)
  invite_index = 0

  if option != 0 and option <= len(user_invites):
    invite_index = option - 1
    
  if len(user_invites) == 0:
    await ctx.send(messages.ACCEPT_NO_CHALLENGE.value)
    return
  elif len(user_invites) > 1 and option == 0:
    await ctx.send(messages.ACCEPT_MULTIPLE_INVITES_QUESTION.value.format(len(user_invites)))

    for index, invite in enumerate(user_invites):
      await ctx.send(f'{index + 1} - <@{invite.challenger}>')
    
    await ctx.send(messages.ACCEPT_USE_COMMAND_TO_SELECT_MESSAGE.value)
    return

  invite = user_invites[invite_index]

  if ctx.author.id == invite.challenged_player:
    challenger_player = await ctx.bot.fetch_user(invite.challenger)
    challenged_player = await ctx.bot.fetch_user(invite.challenged_player)
    
    game = Game(challenger_player, challenged_player)

    game.channel = await ctx.message.guild.create_text_channel(str(game), topic='game')
    
    game.init_game()

    current_player_id = game.get_current_player()['id']

    await game.channel.send(messages.ACCEPT_INITIATING_GAME_MESSAGE.value)
    await game.channel.send(messages.ACCEPT_TURN_MESSAGE.value.format(current_player_id))
    
    await game.print_board()
    ctx.bot.games.append(game)
    
    user_invite_id = f'{invite.challenger}{invite.challenged_player}'
    user_inverted_invite_id = f'{invite.challenged_player}{invite.challenger}'

    ctx.bot.pending_invites = list(filter(lambda invite: not invite.id in [user_inverted_invite_id, user_invite_id], invites))
  else:
    await ctx.send(messages.ACCEPT_NO_CHALLENGE.value)
