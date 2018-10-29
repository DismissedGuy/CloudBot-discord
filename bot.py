import os
import logging
import discord
from discord.ext import commands
import aiohttp
import config

logging.basicConfig(level=logging.INFO)

bot = commands.Bot(command_prefix=['c!', 'C!'])
bot.session = aiohttp.ClientSession(raise_for_status=True, loop=bot.loop)

startup_extensions = ['cogs.' + f.rstrip('.py') for f in os.listdir('cogs') if os.path.isfile(f'cogs/{f}')]


@bot.event
async def on_ready():
    print(discord.__version__)
    print('----------------')
    print(f'Logged in as {bot.user} ({bot.user.id})')
    print(f'Currently serving {len(bot.guilds)} servers')
    print(f'Registered commands: {len(bot.commands)}')
    print('----------------')

if __name__ == '__main__':
    for ext in startup_extensions:
        try:
            bot.load_extension(ext)
        except Exception as e:
            exc = '{}: {}'.format(type(e).__name__, e)
            print('Failed to load extension {}\n{}'.format(ext, exc))

    bot.run(config.BOT_TOKEN)
