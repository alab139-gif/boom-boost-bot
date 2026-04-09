import os
import asyncio
from telegram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

bot = Bot(token=TOKEN)
scheduler = AsyncIOScheduler(timezone="Europe/Lisbon")

async def enviar(mensagem):
    await bot.send_message(chat_id=CHAT_ID, text=mensagem)

async def teste():
    await enviar("🟢 Bot a funcionar! Teste bem sucedido! 🎉")

scheduler.add_job(teste, "cron", hour=0, minute=5)

async def main():
    scheduler.start()
    print("Bot a correr...")
    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
