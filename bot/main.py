from pretty_help import PrettyHelp
from discord.ext import commands
import commands as bot_commands
from dotenv import load_dotenv
import os

ENDING_NOTE = '''Digite #help command para mais informações sobre o comando.'''

load_dotenv()


COMMAND_PREFIX = '!' if os.getenv('ENVIROMENT') == 'production' else '#'

bot = commands.Bot(command_prefix=COMMAND_PREFIX, help_command=PrettyHelp(ending_note=ENDING_NOTE, show_index=False, no_category='Geral'))

bot.add_command(bot_commands.play)
bot.add_command(bot_commands.accept)
bot.add_command(bot_commands.end)
bot.add_command(bot_commands.place)

bot.run(os.getenv('DISCORD_TOKEN'))