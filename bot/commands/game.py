import discord
from discord.ext import commands, tasks
import aiohttp

CHANNEL_ID = 1136822338810290308

class Game(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.checked_games = set()
        self.check_free_games.start()

    def cog_unload(self):
        self.check_free_games.cancel()

    @tasks.loop(hours=6)
    async def check_free_games(self):
        await self.bot.wait_until_ready()
        channel = self.bot.get_channel(CHANNEL_ID)
        if not channel:
            return

        games = await self.get_epic_games()
        for game in games:
            if game["id"] not in self.checked_games:
                self.checked_games.add(game["id"])
                embed = discord.Embed(
                    title=game["title"],
                    description=game["description"],
                    url=game["url"],
                    color=discord.Color.green()
                )
                embed.set_image(url=game["image"])
                await channel.send("@here 🎮 Guys ada game gratis Nih!", embed=embed)

    async def get_epic_games(self):
        url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions?locale=id-ID&country=ID&allowCountries=ID"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                data = await resp.json()

        games = []
        elements = data["data"]["Catalog"]["searchStore"]["elements"]
        for element in elements:
            title = element["title"]
            desc = element.get("description", "Game gratis dari Epic!")

            # Gambar
            image = None
            for img in element.get("keyImages", []):
                if img["type"] in ["DieselStoreFrontWide", "OfferImageWide"]:
                    image = img["url"]
                    break

            # URL aman
            slug = element.get("productSlug")
            if not slug:
                pages = element.get("catalogNs", {}).get("mappings", [])
                if pages:
                    slug = pages[0].get("pageSlug")

            url = f"https://store.epicgames.com/p/{slug}" if slug else "https://store.epicgames.com/"

            # Pastikan benar-benar sedang gratis
            if element.get("promotions") and element["promotions"].get("promotionalOffers"):
                games.append({
                    "id": element["id"],
                    "title": title,
                    "description": desc,
                    "image": image,
                    "url": url
                })

        return games


    @commands.command()
    async def checkgames(self, ctx):
        """Cek game gratis secara manual."""
        games = await self.get_epic_games()
        if not games:
            await ctx.send("Saat ini tidak ada game gratis.")
            return

        for game in games:
            embed = discord.Embed(
                title=game["title"],
                description=game["description"],
                url=game["url"],
                color=discord.Color.green()
            )
            embed.set_image(url=game["image"])
            await ctx.send("@here 🎮 Guys ada game gratis Nih", embed=embed)
