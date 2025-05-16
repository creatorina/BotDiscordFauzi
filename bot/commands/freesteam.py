import discord
from discord.ext import commands, tasks
import aiohttp
import asyncio
import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

SENT_FILE = "sent_games.txt"
CHECK_INTERVAL = 21600  # 6 jam
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

    def clear_sent_games_if_new_day(self):
        if os.path.exists(SENT_FILE):
            file_time = datetime.fromtimestamp(os.path.getmtime(SENT_FILE))
            now = datetime.now()
            if file_time.date() != now.date():
                os.remove(SENT_FILE)
                print("🗑️ File sent_games.txt dihapus karena sudah hari baru.")

    async def fetch_free_games(self):
        self.clear_sent_games_if_new_day()
        sent_games = self.load_sent_games()

        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.gamerpower.com/api/giveaways") as response:
                if response.status != 200:
                    print("❌ Gagal mengambil data dari GamerPower.")
                    return []

                data = await response.json()

                print("🎮 Cek game dari Steam/Epic:")
                for game in data:
                    if game.get("platforms") and ("Steam" in game["platforms"] or "Epic" in game["platforms"]):
                        print(f"- {game['title']} | Worth: {game.get('worth')}")

                return [
                    game for game in data
                    if game.get("platforms") and ("Steam" in game["platforms"] or "Epic" in game["platforms"])
                    and str(game["id"]) not in sent_games
                    and game.get("worth", "").strip().startswith("$0.00")
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

        for game in free_games[:4]:
            await self.kirim_embed_game(channel, game)

    async def kirim_embed_game(self, channel, game):
        platform = game["platforms"]
        platform_icon = None
        if "Steam" in platform:
            platform_icon = "https://cdn.cloudflare.steamstatic.com/steamcommunity/public/images/apps/753/7c6e4184d42595e2daae64e147a3f40e9eaf09bb.jpg"
        elif "Epic" in platform:
            platform_icon = "https://upload.wikimedia.org/wikipedia/commons/3/31/Epic_Games_logo.png"

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

        await channel.send("@here ada info game gratis PC!", embed=embed)
        self.save_sent_game(str(game["id"]))
        await asyncio.sleep(1)

    @commands.command()
    async def cekgame(self, ctx):
        """Cek manual apakah ada game gratis baru"""
        free_games = await self.fetch_free_games()
        if not free_games:
            await ctx.send("✅ maaf Tidak ada game gratis .")
            return

        await ctx.send(f"🎉 Ditemukan {len(free_games)} game gratis baru! Akan dikirim ke channel.")
        channel = self.bot.get_channel(CHANNEL_ID)
        if channel:
            for game in free_games[:4]:
                await self.kirim_embed_game(channel, game)

async def setup(bot):
    await bot.add_cog(FreeSteam(bot))
