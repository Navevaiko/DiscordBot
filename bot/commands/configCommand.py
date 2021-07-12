from discord.ext import commands
from settings import load_messages

@commands.command()
async def config(ctx, option, value):
  '''
    Configura as opções do bot.
    Opções disponíveis: 
      - language <[pt-br, en]>
  '''
  available_languages = ctx.bot.languages
  messages = ctx.bot.messages
  
  if option.lower() == 'language' and value in available_languages:
    ctx.bot.messages = load_messages(value)
    messages = ctx.bot.messages
    await ctx.send(messages.CONFIG_LANGUAGE_CHANGED.value)
  else:
    await ctx.send(messages.CONFIG_INVALID_OPTION.value)

@config.error
async def handle_config_error(ctx, error):
  messages = ctx.bot.messages
  
  if isinstance(error, commands.errors.MissingRequiredArgument):
    await ctx.send(messages.CONFI_MISSING_PARAM_ERROR.value)