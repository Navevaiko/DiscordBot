from pretty_help import PrettyHelp
from dotenv import load_dotenv
import os

def setup(bot):
  load_dotenv()
  
  ending_note = '''Digite #help command para mais informações sobre o comando.'''
  command_prefix = '!' if os.getenv('ENVIROMENT') == 'production' else '#'
  help_command = PrettyHelp(ending_note=ending_note, show_index=False, no_category='Geral')

  bot.game = None
  bot.help_command = help_command
  bot.command_prefix = command_prefix
