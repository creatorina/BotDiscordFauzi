from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
import pytz
import random
import os
import discord

# Daftar ucapan selamat pagi
greetings = [
    "Selamat pagi, {mention}! Semoga harimu menyenangkan ☀️",
    "Hai {mention}, semangat pagi ya! 💪",
    "Pagi {mention}! Jangan lupa sarapan 🍞",
    "Yo {mention}, good morning! ☕",
    "Selamat pagi {mention}, waktunya produktif! ✨"
    "Halo {mention}, Sii paling morning person ❤️😍😍"
    "Selamat pagi {mention}! Semoga harimu penuh energi 💪",
    "Hai {mention}, waktunya bangkit dan bersinar ☀️",
    "Pagi {mention}! Hari ini adalah kesempatan baru ✨",
    "Yo {mention}, semangat pagiii! 🚀",
    "Good morning {mention}, jangan lupa sarapan ya 🍞",
    "Waktunya produktif {mention}! 💼",
    "Selamat menjalani hari, {mention} 🌈",
    "Bangun bangun {mention}, rejeki udah nunggu 🐓",
    "Apa kabar pagi ini, {mention}? 😊",
    "Halo {mention}, selamat pagi dan semangat terus 💡",
    "Pagi cerah untukmu, {mention}! 🌤️",
    "Haii {mention}! Semoga kamu merasa luar biasa hari ini 🙌",
    "Selamat pagi {mention}, hari ini milikmu! 🎯",
    "Awali harimu dengan senyum, {mention} 😄",
    "Jangan lupa ngopi dulu, {mention} ☕",
    "Have a nice day, {mention}! 🌟"
]

# Fungsi setup yang dipanggil dari main.py
def setup(bot):
    scheduler = AsyncIOScheduler(timezone=pytz.timezone("Asia/Jakarta"))

    # Gunakan trigger terpisah agar job async didukung sepenuhnya
    async def greet_members():
        print("⏰ Scheduler aktif, mulai menyapa...")

        guild_id = int(os.getenv("GUILD_ID"))
        channel_id = int(os.getenv("CHANNEL_ID"))

        guild = bot.get_guild(guild_id)
        if not guild:
            print("❌ Guild tidak ditemukan.")
            return

        channel = bot.get_channel(channel_id)
        if not channel:
            print("❌ Channel tidak ditemukan.")
            return

        online_members = [
            m for m in guild.members
            if not m.bot and m.status == discord.Status.online
        ]

        print(f"👥 Total member online non-bot: {len(online_members)}")

        if online_members:
            selected_members = random.sample(
                online_members, min(len(online_members), 3)
            )
            mentions = ", ".join([member.mention for member in selected_members])
            greeting = f"Selamat pagi {mentions}! Semoga harimu menyenangkan ☀️"
            await channel.send(greeting)
            print(f"📣 Menyapa: {[m.display_name for m in selected_members]}")
        else:
            print("😴 Tidak ada member online.")


    # Tambahkan job async dengan trigger interval
    scheduler.add_job(
        greet_members,
        CronTrigger(hour=8, minute=0, timezone=pytz.timezone("Asia/Jakarta"))
    )

    scheduler.start()
