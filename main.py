import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

from bot.events import MyEvents
from bot import scheduler

from bot.commands.general import General
from bot.commands.freesteam import FreeSteam
from bot.commands.weather import Weather

load_dotenv()

# Aktifkan intents
intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.presences = True

# Inisialisasi bot
bot = commands.Bot(command_prefix="!", intents=intents)

# ⬇️ INI YANG PENTING: pasang semua cog di sini
@bot.event
async def setup_hook():
    await bot.add_cog(General(bot))
    await bot.add_cog(Game(bot))
    await bot.add_cog(FreeSteam(bot))
    await bot.add_cog(Weather(bot))
    await bot.add_cog(MyEvents(bot))
    scheduler.setup(bot)

# Bot siap online
@bot.event
async def on_ready():
    print(f"{bot.user} is now online!")

# Jalankan bot
bot.run(os.getenv("BOT_TOKEN"))
