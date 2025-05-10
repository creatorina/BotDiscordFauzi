import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Halo! Aku bot 😄")

    @commands.command()
    async def faq(self, ctx):
        await ctx.send(
            "**FAQ Bot**\n"
            "- `!hello`: Sapa bot\n"
            "- `!tebak`: Main tebak kata\n"
            "- `!cuaca <kota>`: Info cuaca\n"
            "- `!meme`: Kirim meme of the day\n"
            "- `!faq`: Lihat bantuan\n"
        )
