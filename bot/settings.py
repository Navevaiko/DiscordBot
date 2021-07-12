from pretty_help import PrettyHelp
from dotenv import load_dotenv
from enum import Enum
import json
import os

def load_messages(language):
  with open(f'bot/messages/{language}.json', 'r', encoding='utf-8') as json_file:
    messages = json.load(json_file)

  return Enum('Messages', messages)

def setup(bot):
  load_dotenv()
  
  ending_note = '''Digite #help command para mais informações sobre o comando.'''
  command_prefix = '!' if os.getenv('ENVIROMENT') == 'production' else '#'
  help_command = PrettyHelp(ending_note=ending_note, show_index=False, no_category='Geral')

  bot.game = None
  bot.languages = ['en', 'pt-br']
  bot.messages = load_messages(os.getenv('DEFAULT_LANGUAGE'))
  bot.help_command = help_command
  bot.command_prefix = command_prefix
