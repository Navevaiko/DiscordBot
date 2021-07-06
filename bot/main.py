from discord.ext import commands
from dotenv import load_dotenv
import commands as bot_commands
import os 

load_dotenv()
bot = commands.Bot(command_prefix='!')

bot.add_command(bot_commands.play)
bot.add_command(bot_commands.accept)
bot.add_command(bot_commands.end)
bot.add_command(bot_commands.place)

bot.run(os.getenv('DISCORD_TOKEN'))