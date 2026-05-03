import asyncio
from datetime import datetime, timedelta
from telegram.ext import Application
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import holidays
import os

# 🔴 METE AQUI OS TEUS DADOS
TOKEN = "8656939827:AAGxFebTouJhQtUVv8YrWkraI07dojvMzTw"
CHAT_ID = -1003758317502
THREAD_ID = 6364

scheduler = AsyncIOScheduler(timezone="Europe/Lisbon")
pt_holidays = holidays.Portugal()

def is_holiday_or_weekend(date):
    return date.weekday() >= 5 or date in pt_holidays

def is_eve_of_holiday(date):
    return (date + timedelta(days=1)) in pt_holidays

async def send_msg(app, text):
    await app.bot.send_message(
        chat_id=CHAT_ID,
        text=text,
        message_thread_id=THREAD_ID
    )

async def send_photo(app, photo_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, photo_path)

    if not os.path.exists(full_path):
        print(f"❌ Imagem não encontrada: {full_path}")
        return

    with open(full_path, "rb") as photo:
    await app.bot.send_document(
        chat_id=CHAT_ID,
        document=photo,
        message_thread_id=THREAD_ID
    )

async def stop(app):
    await send_photo(app, "Stop.png")

    await asyncio.sleep(2)

    await send_msg(app, """🚨 Deixa tudo em ordem

🫶🏻 Obrigada pela participação  
👋🏻 Até à próxima""")

# ------------------ 12:30 (DIAS ÚTEIS) ------------------

async def go_1230(app):
    hoje = datetime.now().date()
    if not is_holiday_or_weekend(hoje):
        await send_photo(app, "Roupeiro1230.png")

        await asyncio.sleep(2)

        await send_msg(app, """🔗 Coloca o link do teu PERFIL

❤️ Dá 5 favoritos em CADA perfil
❗ É obrigatório interagir com TODOS

⏰ Cumpre o horário""")

async def stop_1300(app):
    hoje = datetime.now().date()
    if not is_holiday_or_weekend(hoje):
        await stop(app)

# ------------------ 14:30 (FDS/FERIADOS) ------------------

async def go_1430(app):
    hoje = datetime.now().date()
    if is_holiday_or_weekend(hoje):
        await send_photo(app, "roupeiro1430.png")

        await asyncio.sleep(2)

        await send_msg(app, """🔗 Coloca o link do teu PERFIL

❤️ Dá 5 favoritos em CADA perfil
❗ É obrigatório interagir com TODOS

⏰ Cumpre o horário""")

async def stop_1500(app):
    hoje = datetime.now().date()
    if is_holiday_or_weekend(hoje):
        await stop(app)

# ------------------ 17:30 ------------------

async def go_1730(app):
    await send_photo(app, "roupeiro1730.png")

    await asyncio.sleep(2)

    await send_msg(app, """🔗 Coloca o link do teu PERFIL

❤️ Dá 5 favoritos em CADA perfil
❗ É obrigatório interagir com TODOS

⏰ Cumpre o horário""")

async def stop_1800(app):
    await stop(app)

# ------------------ 21:00 ------------------

async def go_21(app):
    dia = datetime.now().weekday()

    if dia in [0, 2, 4]:
        await send_photo(app, "5artigos.png")

        await asyncio.sleep(2)

        await send_msg(app, """🔗 Coloca 5 links de ARTIGOS (não perfil)
⚠️ 1 link por linha na mesma mensagem

1️⃣ https://vinted.pt/...
2️⃣ https://vinted.pt/...
3️⃣ https://vinted.pt/...
4️⃣ https://vinted.pt/...
5️⃣ https://vinted.pt/...

❤️ Abre cada link e dá 1 favorito
❗ Interage com TODOS os participantes (obrigatório)

🚨 Se algum artigo já tiver like, reage com: 👀

⏰ Cumpre o horário""")

    else:
        await send_photo(app, "roupeiro10favs_21horas.png")

        await asyncio.sleep(2)

        await send_msg(app, """🔗 Coloca o link do teu PERFIL

❤️ Dá 10 favoritos em CADA perfil
❗ É obrigatório interagir com TODOS

⏰ Cumpre o horário""")

# ------------------ NOTURNAS ------------------

async def go_noturna_util(app):
    hoje = datetime.now().date()
    dia = datetime.now().weekday()

    if dia in [0, 1, 2, 3, 6] and not is_eve_of_holiday(hoje):
        await send_photo(app, "roupeiro5favs_23horas.png")

        await asyncio.sleep(2)

        await send_msg(app, """🔗 Coloca o link do teu PERFIL

❤️ Dá 5 favoritos em CADA perfil
❗ É obrigatório interagir com TODOS

⏰ Cumpre o horário""")


async def go_noturna_fds(app):
    hoje = datetime.now().date()
    dia = datetime.now().weekday()

    if dia in [4, 5] or is_eve_of_holiday(hoje):
        await send_photo(app, "Roupeiro10favs_23h30.png")

        await asyncio.sleep(2)

        await send_msg(app, """🔗 Coloca o link do teu PERFIL

❤️ Dá 10 favoritos em CADA perfil
❗ É obrigatório interagir com TODOS

⏰ Cumpre o horário""")

async def stop_noturna_util(app):
    hoje = datetime.now().date()
    ontem = hoje - timedelta(days=1)
    dia_ontem = ontem.weekday()
    if dia_ontem in [0, 1, 2, 3, 6] and not is_eve_of_holiday(ontem):
        await stop(app)

async def stop_noturna_fds(app):
    hoje = datetime.now().date()
    ontem = hoje - timedelta(days=1)
    dia_ontem = ontem.weekday()
    if dia_ontem in [4, 5] or is_eve_of_holiday(ontem):
        await stop(app)

# ------------------ MAIN ------------------

async def main():
    app = Application.builder().token(TOKEN).build()

    scheduler.add_job(go_1230, "cron", hour=12, minute=30, args=[app])
    scheduler.add_job(stop_1300, "cron", hour=13, minute=0, args=[app])

    scheduler.add_job(go_1430, "cron", hour=14, minute=30, args=[app])
    scheduler.add_job(stop_1500, "cron", hour=15, minute=0, args=[app])

    scheduler.add_job(go_1730, "cron", hour=17, minute=30, args=[app])
    scheduler.add_job(stop_1800, "cron", hour=18, minute=0, args=[app])

    scheduler.add_job(go_21, "cron", hour=21, minute=0, args=[app])
    scheduler.add_job(stop, "cron", hour=22, minute=0, args=[app])

    scheduler.add_job(go_noturna_util, "cron", hour=23, minute=0, args=[app])
    scheduler.add_job(go_noturna_fds, "cron", hour=23, minute=30, args=[app])
    scheduler.add_job(stop_noturna_util, "cron", hour=9, minute=0, args=[app])
    scheduler.add_job(stop_noturna_fds, "cron", hour=10, minute=30, args=[app])

    scheduler.start()

    print("Bot a correr...")

    async with app:
        await app.start()
        while True:
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
