import asyncio
import discord
import os
import traceback
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(
  command_prefix = "demo.test.",
  intents = discord.Intents.all(),
  help_command = None
)

async def load():
  for folder in os.listdir('cogs'):
    for file in os.listdir(f'cogs/{folder}'):
      if file.endswith(".py"):
        await bot.load_extension(f'cogs.{folder}.{file[:-3]}')

async def main():
  await load()
  await bot.start(os.getenv("TOKEN"), reconnect = True)

try:
  asyncio.run(main())
except:
  traceback.print_exc()