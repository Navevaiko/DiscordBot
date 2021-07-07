from discord.ext import commands
from dotenv import load_dotenv
import commands as bot_commands
import os 

load_dotenv()


COMMAND_PREFIX = '!' if os.getenv('ENVIROMENT') == 'production' else '#'

bot = commands.Bot(command_prefix=COMMAND_PREFIX)

bot.add_command(bot_commands.play)
bot.add_command(bot_commands.accept)
bot.add_command(bot_commands.end)
bot.add_command(bot_commands.place)

bot.run(os.getenv('DISCORD_TOKEN'))