import discord
from discord.ext import commands, tasks
import aiohttp
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SENT_FILE = "sent_games.txt"
CHECK_INTERVAL = 3600  # Cek tiap 1 jam
CHANNEL_ID = 1136822338810290308

class FreeSteam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.check_free_games.start()

    def cog_unload(self):
        self.check_free_games.cancel()

    def load_sent_games(self):
        if not os.path.exists(SENT_FILE):
            return set()
        with open(SENT_FILE, "r") as f:
            return set(line.strip() for line in f.readlines())

    def save_sent_game(self, game_id):
        with open(SENT_FILE, "a") as f:
            f.write(f"{game_id}\n")


    async def fetch_free_games(self):
        self.clear_sent_games_if_new_day()
        sent_games = self.load_sent_games()

        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.gamerpower.com/api/giveaways") as response:
                if response.status != 200:
                    print("❌ Gagal mengambil data dari GamerPower.")
                    return []

                data = await response.json()

                return [
                    game for game in data
                    if game.get("type") == "Game"
                    and game.get("worth", "").startswith("$")
                    and any(p in game.get("platforms", "") for p in ["Steam", "Epic"])
                    and str(game["id"]) not in sent_games
                    and "steam key" not in game.get("description", "").lower()
                    and "steam key" not in game.get("title", "").lower()
                ]

    @tasks.loop(seconds=CHECK_INTERVAL)
    async def check_free_games(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(CHANNEL_ID)
        if not channel:
            print("❌ Channel tidak ditemukan.")
            return

        free_games = await self.fetch_free_games()
        if not free_games:
            print("✅ Tidak ada game gratis baru.")
            return

        for game in free_games:
            await self.send_game(channel, game)
            self.save_sent_game(str(game["id"]))

    async def send_game(self, channel, game):
        platform = game["platforms"]
        platform_icon = None

        if "Steam" in platform:
            platform_icon = "https://cdn.patchbot.io/games/109/steam_sm.webp"
        elif "Epic" in platform:
            platform_icon = "https://cdn.patchbot.io/games/107/epic_games_sm.webp"

        embed = discord.Embed(
            title=game["title"],
            url=game["open_giveaway_url"],
            description=game.get("description", "Tidak ada deskripsi."),
            color=discord.Color.green()
        )
        if platform_icon:
            embed.set_author(name=platform, icon_url=platform_icon)
        embed.set_image(url=game["image"])
        embed.set_footer(text=f"Platform: {platform} | Berakhir: {game['end_date']}")

        await channel.send("@here Buruan Claim game gratis!", embed=embed)

    @commands.command()
    async def cekgame(self, ctx):
        """Cek manual game gratis"""
        free_games = await self.fetch_free_games()
        if not free_games:
            await ctx.send("✅ Tidak ada game gratis Boss.")
            return

        await ctx.send(f"🎮 Menemukan {len(free_games)} game gratis:")
        for game in free_games:
            await self.send_game(ctx.channel, game)
            self.save_sent_game(str(game["id"]))

async def setup(bot):
    await bot.add_cog(FreeSteam(bot))
