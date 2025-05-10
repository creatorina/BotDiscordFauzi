import discord
from discord.ext import commands

class MyEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = discord.utils.get(member.guild.text_channels, name='general')
        if channel:
            await channel.send(f"Selamat datang {member.mention} di server {member.guild.name}!")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if "halo" in message.content.lower():
            await message.channel.send(f"Halo juga, {message.author.mention}! 👋")
