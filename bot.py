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

async def abrir_sessao():
    await enviar("🟢 Sessão aberta! Cola aqui o teu link!")

async def fechar_sessao():
    await enviar("🔴 Sessão encerrada!")

scheduler.add_job(abrir_sessao, "cron", hour=10, minute=10)
scheduler.add_job(fechar_sessao, "cron", hour=10, minute=20)

async def main():
    scheduler.start()
    print("Bot a correr...")
    while True:
        await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
