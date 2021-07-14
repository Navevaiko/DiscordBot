from discord.ext import commands
from discord.utils import get
from utils import get_game_by_channel_name

@commands.command()
async def end(ctx):
  '''
    Finaliza o jogo e remove o canal de texto criado
  '''
  if ctx.channel.topic != 'game':
    await ctx.send('Esse canal não é o canal de um jogo')
    return

  game = get_game_by_channel_name(ctx.bot.games, ctx.channel.name)
  messages = ctx.bot.messages
  
  await game.channel.send(messages.END_FINISH_GAME_MESSAGE.value)
  await game.channel.delete()

  ctx.bot.games = list(filter(lambda current_game: current_game.id != game.id, ctx.bot.games))
