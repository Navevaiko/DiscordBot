from discord.ext import commands

@commands.command()
async def end(ctx):
  '''
    Finaliza o jogo e remove o canal de texto criado
  '''

  game = ctx.bot.game
  
  await game.channel.send('Jogo finalizado!')
  await game.channel.delete()
  game.end_game()