import discord
import aiohttp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()  # Memuat BOT_TOKEN dari .env

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = 1136822338810290308  # Ganti dengan ID channel Discord kamu

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

client = discord.Client(intents=intents)

async def cek_game_gratis(channel: discord.TextChannel):
    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.gamerpower.com/api/giveaways") as response:
            if response.status != 200:
                await channel.send("Gagal mengambil data dari GamerPower.")
                return

            data = await response.json()

            # Filter hanya game Steam atau Epic
            free_games = [
                game for game in data
                if game["platforms"] and ("Steam" in game["platforms"] or "Epic" in game["platforms"])
            ]

            if not free_games:
                await channel.send("Tidak ada game gratis saat ini.")
                return

            for game in free_games[:3]:  # Maks 3 game
                platform = game["platforms"]

                # Default icon
                platform_icon = None
                if "Steam" in platform:
                    platform_icon = "https://cdn.patchbot.io/games/109/steam_sm.webp"
                elif "Epic" in platform:
                    platform_icon = "https://cdn.patchbot.io/games/107/epic_games_sm.webp"

                embed = discord.Embed(
                    title=game["title"],
                    url=game["open_giveaway_url"],
                    description=game["description"],
                    color=discord.Color.green()
                )

                if platform_icon:
                    embed.set_author(name=platform, icon_url=platform_icon)

                embed.set_image(url=game["image"])
                embed.set_footer(text=f"Platform: {platform} | Berakhir: {game['end_date']}")

                await channel.send("@here", embed=embed)
                await asyncio.sleep(1)  # Delay untuk hindari spam

@client.event
async def on_ready():
    print(f"{client.user} sudah login dan siap mengirim notifikasi.")
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        print("❌ Channel tidak ditemukan.")
        return
    await cek_game_gratis(channel)
    await client.close()  # Selesai, keluar

client.run(TOKEN)
