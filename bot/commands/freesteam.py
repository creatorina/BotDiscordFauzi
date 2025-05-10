import os
import discord
import aiohttp
from discord.ext import commands, tasks

class FreeSteam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.channel_id = int("1136822338810290308")  # Ganti jika perlu
        self.checked_apps = set()
        self.check_free_games.start()

    def cog_unload(self):
        self.check_free_games.cancel()

    @tasks.loop(minutes=60)
    async def check_free_games(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(self.channel_id)
        if not channel:
            print("❌ Channel tidak ditemukan.")
            return

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://www.gamerpower.com/api/giveaways?platform=steam&type=game") as resp:
                    if resp.status != 200:
                        print(f"❌ Gagal mengambil data giveaway: {resp.status}")
                        return
                    data = await resp.json()

                    for game in data:
                        if game["id"] in self.checked_apps:
                            continue
                        self.checked_apps.add(game["id"])
                        title = game["title"]
                        link = game["open_giveaway_url"]
                        await channel.send(f"@here 🎁 Game gratis baru di Steam: **{title}**\n🔗 {link}")

        except Exception as e:
            print(f"❌ Terjadi kesalahan saat mengambil data giveaway: {e}")

def setup(bot):
    bot.add_cog(FreeSteam(bot))
