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

async def stop(app):
await send_msg(app, """🛑 STOP 🔗

🙏🏻🫶🏻""")

------------------ 12:30 (APENAS DIAS ÚTEIS) ------------------

async def go_1230(app):
hoje = datetime.now().date()
if not is_holiday_or_weekend(hoje):
await send_msg(app, """🚀 GO!

🔗 ROUPEIRO • ARMARIO • DRESSING
❤️ 5 FAVS
⏰ 12:30 – 13:00""")

async def stop_1300(app):
hoje = datetime.now().date()
if not is_holiday_or_weekend(hoje):
await stop(app)

------------------ NOVA SESSÃO FDS/FERIADOS ------------------

async def go_1430(app):
hoje = datetime.now().date()
if is_holiday_or_weekend(hoje):
await send_msg(app, """🚀 GO!

🔗 ROUPEIRO • ARMARIO • DRESSING
♥️ 5 FAVS
⏰ 14:30 – 15:00""")

async def stop_1500(app):
hoje = datetime.now().date()
if is_holiday_or_weekend(hoje):
await stop(app)

------------------ 17:30 ------------------

async def go_1730(app):
await send_msg(app, """🚀 GO!

🔗 ROUPEIRO • ARMARIO • DRESSING
❤️ 5 FAVS
⏰ 17:30 – 18:00""")

------------------ 21:00 ------------------

async def go_21(app):
dia = datetime.now().weekday()
if dia in [0, 2, 4]:  # seg, qua, sex
await send_msg(app, """🚀 GO!

🔗 5 LINKS • ENLACES • LIENS
♥️ 5 FAVS
⏰ 21:00 – 22:00""")
else:
await send_msg(app, """🚀 GO!

👠 ROUPEIRO • ARMARIO • DRESSING
❤️ 10 FAVS
⏰ 21:00 – 22:00""")

------------------ NOTURNAS ------------------

async def go_noturna_util(app):
hoje = datetime.now().date()
dia = datetime.now().weekday()
if dia in [0, 1, 2, 3, 6] and not is_eve_of_holiday(hoje):
await send_msg(app, """🚀 GO!

🔗 ROUPEIRO • ARMARIO • DRESSING
♥️ 5 FAVS
⏰ 23:00 – 09:00""")

async def go_noturna_fds(app):
hoje = datetime.now().date()
dia = datetime.now().weekday()
if dia in [4, 5] or is_eve_of_holiday(hoje):
await send_msg(app, """🚀 GO!

🔗 ROUPEIRO • ARMARIO • DRESSING
♥️ 10 FAVS
⏰ 23:30 – 10:30""")

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

------------------ MAIN ------------------

async def main():
app = Application.builder().token(TOKEN).build()

# 12:30 (dias úteis)  
scheduler.add_job(go_1230, "cron", hour=12, minute=30, args=[app])  
scheduler.add_job(stop_1300, "cron", hour=13, minute=0, args=[app])  

# 14:30 (fds/feriados)  
scheduler.add_job(go_1430, "cron", hour=14, minute=30, args=[app])  
scheduler.add_job(stop_1500, "cron", hour=15, minute=0, args=[app])  

# 17:30  
scheduler.add_job(go_1730, "cron", hour=17, minute=30, args=[app])  
scheduler.add_job(stop, "cron", hour=18, minute=0, args=[app])  

# 21:00  
scheduler.add_job(go_21, "cron", hour=21, minute=0, args=[app])  
scheduler.add_job(stop, "cron", hour=22, minute=0, args=[app])  

# Noturnas  
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

if name == "main":
asyncio.run(main())
