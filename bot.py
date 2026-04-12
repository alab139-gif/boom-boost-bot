import os
import asyncio
from datetime import datetime, timedelta
from telegram.ext import Application
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import holidays

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")

scheduler = AsyncIOScheduler(timezone="Europe/Lisbon")
pt_holidays = holidays.Portugal()

THREAD_ID = 6364  # 👈 teu tópico

# ------------------ FUNÇÕES AUXILIARES ------------------

def is_holiday_or_weekend(date):
    return date.weekday() >= 5 or date in pt_holidays

def is_eve_of_holiday(date):
    return (date + timedelta(days=1)) in pt_holidays

# ------------------ ENVIO ------------------

async def send_msg(app, text):
    await app.bot.send_message(
        chat_id=CHAT_ID,
        text=text,
        message_thread_id=THREAD_ID
    )

# ------------------ SESSÕES FIXAS ------------------

async def aviso_1230(app):
    await send_msg(app, """🚨 DAQUI A 30 MINUTOS!

👠 SESSÃO ARMÁRIO • 5 FAVORITOS
⏰ 12:30–13:00

Preparem os links 🥳🔥""")

async def go_1230(app):
    await send_msg(app, """🚀 GO!

🔗 SESSÃO ARMÁRIO
♥️ 5 FAVORITOS
⏰ 12:30 – 13:00

Podem começar a enviar 👠🔥""")

async def stop(app):
    await send_msg(app, """🛑 SESSÃO ENCERRADA!

Obrigada pela vossa participação 🥳

Ponham os favoritos em ordem ✅  
Estamos aqui todos para o mesmo 🙌""")

async def aviso_1730(app):
    await send_msg(app, """🚨 DAQUI A 30 MINUTOS!

👠 SESSÃO ARMÁRIO • 5 FAVORITOS
⏰ 17:30–18:00

Preparem os links 🥳🔥""")

async def go_1730(app):
    await send_msg(app, """🚀 GO!

🔗 SESSÃO ARMÁRIO
♥️ 5 FAVORITOS
⏰ 17:30 – 18:00

Podem começar a enviar 👠🔥""")

# ------------------ SESSÃO 21:00 ------------------

async def aviso_21(app):
    if datetime.now().weekday() in [0,2,4]:
        await send_msg(app, """🚨 DAQUI A 30 MINUTOS!

👠 SESSÃO 5 LINKS • 5 FAVORITOS
⏰ 21:00–22:00

Preparem os links 🥳🔥""")
    else:
        await send_msg(app, """🚨 DAQUI A 30 MINUTOS!

👠 SESSÃO ARMÁRIO • 10 FAVORITOS
⏰ 21:00–22:00

Preparem os links 🥳🔥""")

async def go_21(app):
    if datetime.now().weekday() in [0,2,4]:
        await send_msg(app, """🚀 GO!

🔗 SESSÃO 5 LINKS
♥️ 5 FAVORITOS
⏰ 21:00 – 22:00

Podem começar a enviar 👠🔥""")
    else:
        await send_msg(app, """🚀 GO!

🔗 SESSÃO ARMÁRIO
♥️ 10 FAVORITOS
⏰ 21:00 – 22:00

Podem começar a enviar 👠🔥""")

# ------------------ NOTURNA ------------------

async def aviso_noturna(app):
    hoje = datetime.now().date()

    if datetime.now().weekday() in [4,5] or is_eve_of_holiday(hoje):
        await send_msg(app, """🚨 DAQUI A 30 MINUTOS!

👠 SESSÃO ARMÁRIO • 10 FAVORITOS
⏰ 23:30–10:30

Preparem os links 🥳🔥""")
    else:
        await send_msg(app, """🚨 DAQUI A 30 MINUTOS!

👠 SESSÃO ARMÁRIO • 10 FAVORITOS
⏰ 23:00–09:00

Preparem os links 🥳🔥""")

async def go_noturna(app):
    agora = datetime.now()
    hoje = agora.date()

    # controlo horário correto
    if agora.minute == 30:
        if not (agora.weekday() in [4,5] or is_eve_of_holiday(hoje)):
            return
    else:
        if (agora.weekday() in [4,5] or is_eve_of_holiday(hoje)):
            return

    if agora.weekday() in [4,5] or is_eve_of_holiday(hoje):
        await send_msg(app, """🚀 GO!

🔗 SESSÃO ARMÁRIO
♥️ 10 FAVORITOS
⏰ 23:30 – 10:30

Podem começar a enviar 👠🔥""")
    else:
        await send_msg(app, """🚀 GO!

🔗 SESSÃO ARMÁRIO
♥️ 10 FAVORITOS
⏰ 23:00 – 09:00

Podem começar a enviar 👠🔥""")

async def stop_noturna(app):
    agora = datetime.now()
    hoje = agora.date()

    if is_holiday_or_weekend(hoje):
        if agora.hour != 10 or agora.minute != 30:
            return
    else:
        if agora.hour != 9 or agora.minute != 0:
            return

    await send_msg(app, """🛑 SESSÃO ENCERRADA!

Obrigada pela vossa participação 🥳

Ponham os favoritos em ordem ✅  
Estamos aqui todos para o mesmo 🙌""")

# ------------------ MAIN ------------------

async def main():
    app = Application.builder().token(TOKEN).build()

    # 12:30
    scheduler.add_job(aviso_1230, "cron", hour=12, minute=0, args=[app])
    scheduler.add_job(go_1230, "cron", hour=12, minute=30, args=[app])
    scheduler.add_job(stop, "cron", hour=13, minute=0, args=[app])

    # 17:30
    scheduler.add_job(aviso_1730, "cron", hour=17, minute=0, args=[app])
    scheduler.add_job(go_1730, "cron", hour=17, minute=30, args=[app])
    scheduler.add_job(stop, "cron", hour=18, minute=0, args=[app])

    # 21:00
    scheduler.add_job(aviso_21, "cron", hour=20, minute=30, args=[app])
    scheduler.add_job(go_21, "cron", hour=21, minute=0, args=[app])
    scheduler.add_job(stop, "cron", hour=22, minute=0, args=[app])

    # NOTURNA
    scheduler.add_job(aviso_noturna, "cron", hour=22, minute=30, args=[app])
    scheduler.add_job(go_noturna, "cron", hour=23, minute=0, args=[app])
    scheduler.add_job(go_noturna, "cron", hour=23, minute=30, args=[app])
    scheduler.add_job(stop_noturna, "cron", hour=9, minute=0, args=[app])
    scheduler.add_job(stop_noturna, "cron", hour=10, minute=30, args=[app])

    scheduler.start()

    print("Bot a correr...")

    async with app:
        await app.start()
        while True:
            await asyncio.sleep(60)

if __name__ == "__main__":
    asyncio.run(main())
