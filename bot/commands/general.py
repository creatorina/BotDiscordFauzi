import discord
from discord.ext import commands

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def hello(self, ctx):
        await ctx.send("Halo! Aku bot dan sudah siap 😄")

    @commands.command()
    async def bantuan(self, ctx):
        await ctx.send(
            "**Command Bot**\n"
            "- `!cekgame`: info game gratis\n"
            "- `!cuaca <kota>`: Info cuaca\n"
        )
