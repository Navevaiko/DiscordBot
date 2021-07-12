from discord.ext import commands

@commands.command()
async def end(ctx):
  '''
    Finaliza o jogo e remove o canal de texto criado
  '''
  game = ctx.bot.game
  messages = ctx.bot.messages
  
  await game.channel.send(messages.END_FINISH_GAME_MESSAGE.value)
  await game.channel.delete()

  ctx.bot.game = None