 ```python
import os
import asyncio
from datetime import datetime, timedelta
from telegram.ext import Application
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import holidays

TOKEN = os.environ.get("BOT_TOKEN")
CHAT_ID = os.environ.get("CHAT_ID")
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

# MENSAGEM STOP (igual para todos)
async def stop(app):
    await send_msg(app, """🛑 SESSÃO ENCERRADA!

Obrigada pela vossa participação 🥳

Ponham os favoritos em ordem ✅
Estamos aqui todos para o mesmo 🙌""")

# 12:30
async def go_1230(app):
    await send_msg(app, """🚀 GO!

🔗 SESSÃO ARMÁRIO
♥️ 5 FAVORITOS
⏰ 12:30 – 13:00

Podem começar a enviar 👠🔥""")

# 17:30
async def go_1730(app):
    await send_msg(app, """🚀 GO!

🔗 SESSÃO ARMÁRIO
♥️ 5 FAVORITOS
⏰ 17:30 – 18:00

Podem começar a enviar 👠🔥""")

# 21:00 - depende do dia
async def go_21(app):
    dia = datetime.now().weekday()
    if dia in [0, 2, 4]:  # seg, qua, sex
        await send_msg(app, """🚀 GO!

🔗 SESSÃO 5 LINKS
♥️ 5 FAVORITOS
⏰ 21:00 – 22:00

Podem começar a enviar 👠🔥""")
    else:  # ter, qui, sab, dom
        await send_msg(app, """🚀 GO!

🔗 SESSÃO ARMÁRIO
♥️ 10 FAVORITOS
⏰ 21:00 – 22:00

Podem começar a enviar 👠🔥""")

# NOTURNA 23:00 - só dom, seg, ter, qua, qui (exceto vésperas feriado)
async def go_noturna_util(app):
    hoje = datetime.now().date()
    dia = datetime.now().weekday()
    if dia in [0, 1, 2, 3, 6] and not is_eve_of_holiday(hoje):
        await send_msg(app, """🚀 GO!

🔗 SESSÃO ARMÁRIO
♥️ 10 FAVORITOS
⏰ 23:00 – 09:00

Podem começar a enviar 👠🔥""")

# NOTURNA 23:30 - só sex, sab e vésperas feriado
async def go_noturna_fds(app):
    hoje = datetime.now().date()
    dia = datetime.now().weekday()
    if dia in [4, 5] or is_eve_of_holiday(hoje):
        await send_msg(app, """🚀 GO!

🔗 SESSÃO ARMÁRIO
♥️ 10 FAVORITOS
⏰ 23:30 – 10:30

Podem começar a enviar 👠🔥""")

# FECHO NOTURNA 09:00 - dias úteis
async def stop_noturna_util(app):
    hoje = datetime.now().date()
    if not is_holiday_or_weekend(hoje):
        await stop(app)

# FECHO NOTURNA 10:30 - fins de semana e feriados
async def stop_noturna_fds(app):
    hoje = datetime.now().date()
    if is_holiday_or_weekend(hoje):
        await stop(app)

async def main():
    app = Application.builder().token(TOKEN).build()

    # 12:30
    scheduler.add_job(go_1230, "cron", hour=12, minute=30, args=[app])
    scheduler.add_job(stop, "cron", hour=13, minute=0, args=[app])

    # 17:30
    scheduler.add_job(go_1730, "cron", hour=17, minute=30, args=[app])
    scheduler.add_job(stop, "cron", hour=18, minute=0, args=[app])

    # 21:00
    scheduler.add_job(go_21, "cron", hour=21, minute=0, args=[app])
    scheduler.add_job(stop, "cron", hour=22, minute=0, args=[app])

    # NOTURNA
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
```
