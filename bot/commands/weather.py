import discord
from discord.ext import commands
import aiohttp
import os

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = os.getenv("WEATHER_API_KEY")

    @commands.command()
    async def cuaca(self, ctx, *, kota: str):
        """Cek cuaca saat ini untuk kota tertentu"""
        url = f"http://api.openweathermap.org/data/2.5/weather?q={kota}&appid={self.api_key}&units=metric&lang=id"

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                if response.status != 200:
                    await ctx.send("❌ Gagal mengambil data cuaca. Pastikan nama kota benar.")
                    return

                data = await response.json()

        nama_kota = data["name"]
        suhu = data["main"]["temp"]
        cuaca = data["weather"][0]["description"].capitalize()
        kelembapan = data["main"]["humidity"]
        angin = data["wind"]["speed"]

        embed = discord.Embed(
            title=f"🌤️ Cuaca di {nama_kota}",
            description=f"{cuaca}",
            color=discord.Color.blue()
        )
        embed.add_field(name="🌡️ Suhu", value=f"{suhu}°C", inline=True)
        embed.add_field(name="💧 Kelembapan", value=f"{kelembapan}%", inline=True)
        embed.add_field(name="💨 Kecepatan Angin", value=f"{angin} m/s", inline=True)
        embed.set_footer(text="Data dari OpenWeatherMap")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(Weather(bot))
