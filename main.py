import discord
from discord.ext import commands
from dotenv import load_dotenv
from os import getenv

load_dotenv()
token = getenv("TOKEN")

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!")
bot.load_extension("bot_commands")

bot.run(token)
