from discord.ext import commands
from commands.main import play, accept, place, end, config
import settings
import os

bot = commands.Bot(command_prefix='')

settings.setup(bot)

bot.add_command(play)
bot.add_command(accept)
bot.add_command(place)
bot.add_command(end)
bot.add_command(config)

bot.run(os.getenv('DISCORD_TOKEN'))
