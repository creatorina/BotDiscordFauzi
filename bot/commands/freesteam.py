import discord
import aiohttp
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")
CHANNEL_ID = 1136822338810290308
SENT_FILE = "sent_games.txt"

intents = discord.Intents.default()
intents.guilds = True
intents.messages = True

client = discord.Client(intents=intents)

def load_sent_games():
    if not os.path.exists(SENT_FILE):
        return set()
    with open(SENT_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())

def save_sent_game(game_id):
    with open(SENT_FILE, "a") as f:
        f.write(f"{game_id}\n")

async def cek_game_gratis(channel: discord.TextChannel):
    sent_games = load_sent_games()

    async with aiohttp.ClientSession() as session:
        async with session.get("https://www.gamerpower.com/api/giveaways") as response:
            if response.status != 200:
                print("❌ Gagal mengambil data dari GamerPower.")
                return

            data = await response.json()

            free_games = [
                game for game in data
                if game.get("platforms") and ("Steam" in game["platforms"] or "Epic" in game["platforms"])
                and str(game["id"]) not in sent_games
                and game.get("worth") == "$0.00"
            ]

            if not free_games:
                print("✅ Tidak ada game gratis baru dengan diskon 100%.")
                return

            for game in free_games[:4]:
                platform = game["platforms"]

                platform_icon = None
                if "Steam" in platform:
                    platform_icon = "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/753/7c6e4184d42595e2daae64e147a3f40e9eaf09bb.jpg"
                elif "Epic" in platform:
                    platform_icon = "https://upload.wikimedia.org/wikipedia/commons/3/31/Epic_Games_logo.png"

                embed = discord.Embed(
                    title=game["title"],
                    url=game["open_giveaway_url"],
                    description=game["description"] or "Tidak ada deskripsi.",
                    color=discord.Color.green()
                )

                if platform_icon:
                    embed.set_author(name=platform, icon_url=platform_icon)

                embed.set_image(url=game["image"])
                embed.set_footer(text=f"Platform: {platform} | Berakhir: {game['end_date']}")

                await channel.send("@here ada info game gratis pc!", embed=embed)
                save_sent_game(str(game["id"]))
                await asyncio.sleep(1)

@client.event
async def on_ready():
    print(f"✅ {client.user} sudah login dan siap.")
    channel = client.get_channel(CHANNEL_ID)
    if not channel:
        print("❌ Channel tidak ditemukan.")
        return

    # Cek setiap 6 jam (21600 detik)
    while True:
        await cek_game_gratis(channel)
        await asyncio.sleep(21600)

client.run(TOKEN)
