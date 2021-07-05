from discord.ext import commands
import game
import utils

challenged_user_id = 0

@commands.command()
async def play(ctx, invited_user):
  global challenged_user_id
  
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
  game.end_game()