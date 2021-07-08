from discord.ext import commands
from models.main import Game
import utils

@commands.command()
async def play(ctx, invited_user):
  '''
    Convida usuário para uma partida
  '''
  challenged_user_id = utils.get_id_from_mention(invited_user)

  if challenged_user_id == ctx.author.id:
    await ctx.send('Você não pode jogar consigo mesmo!')
    return
  
  game = Game(challenged_user_id)

  if game.state != 0:
    await ctx.send('Há um jogo em andamento, utilize o comando !end para finalizar o jogo')
    return

  game.add_user(ctx.author.id)
  
  ctx.bot.game = game
  await ctx.send(f'{invited_user} o usuário <@{ctx.author.id}> está te desafiando para uma partida de Jogo da Velha!\nPara aceitar use o comando !accept')

@play.error
async def handle_play_error(ctx, error):
  print(error)
  if isinstance(error, commands.errors.MissingRequiredArgument):
    await ctx.send('É necessário passar um usuário para jogar com você!')
  elif isinstance(error, commands.errors.CommandInvokeError):
    await ctx.send('Usuário convidado é inválido!')
  