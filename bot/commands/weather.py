import requests
from discord.ext import commands

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.api_key = 'your_weather_api_key'  # Ganti dengan API key dari OpenWeatherMap

    @commands.command(name="weather")
    async def weather(self, ctx, city: str):
        base_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={self.api_key}&units=metric&lang=id"
        response = requests.get(base_url)
        data = response.json()

        if data["cod"] == "404":
            await ctx.send("Kota tidak ditemukan, coba periksa ejaan atau nama kota.")
        else:
            main = data["main"]
            weather_description = data["weather"][0]["description"]
            temperature = main["temp"]
            pressure = main["pressure"]
            humidity = main["humidity"]
            city_name = data["name"]
            country = data["sys"]["country"]

            # Kirim hasil cuaca ke channel
            weather_message = (f"Cuaca di {city_name}, {country}:\n"
                               f"Deskripsi: {weather_description}\n"
                               f"Suhu: {temperature}°C\n"
                               f"Tekanan: {pressure} hPa\n"
                               f"Humidity: {humidity}%")
            await ctx.send(weather_message)

def setup(bot):
    bot.add_cog(Weather(bot))
