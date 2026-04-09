import os
import asyncio
from telegram.ext import Application
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

scheduler = AsyncIOScheduler(timezone="Europe/Lisbon")

async def teste(app):
    await app.bot.send_message(chat_id=CHAT_ID, text="🟢 Bot a funcionar!")

async def main():
    app = Application.builder().token(TOKEN).build()
    scheduler.add_job(teste, "cron", hour=0, minute=22, args=[app])
    scheduler.start()
    print("Bot a correr...")
    async with app:
        await app.start()
        while True:
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
