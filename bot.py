import asyncio
from datetime import datetime, timedelta
from telegram.ext import Application
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import holidays
import os

# 🔴 METE AQUI OS TEUS DADOS
TOKEN = "8656939827:AAEm9czEedV0PT3Hl6kfHJzKKGcm4L64Juk"
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
        message_thread_id=THREAD_ID,
        disable_web_page_preview=True
    )

# ✅ CORRIGIDO: __file__ com underscores
async def send_photo(app, photo_path):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    full_path = os.path.join(base_dir, photo_path)

    if not os.path.exists(full_path):
        print(f"❌ Imagem não encontrada: {full_path}")
        return

    with open(full_path, "rb") as photo:
        await app.bot.send_photo(
            chat_id=CHAT_ID,
            photo=photo,
            message_thread_id=THREAD_ID
        )


async def stop(app):
    await send_photo(app, "stop.jpg")
    await asyncio.sleep(2)
    await send_msg(app, """🚨 Confirma que deste os favoritos a cada um dos participantes desta sessão

🫶🏻 Obrigada pela participação
👋🏻 Até à próxima""")


# ------------------ 12:00 (TODOS OS DIAS) ------------------

async def go_1200(app):
    await send_photo(app, "roupeiro5favs_12h00.jpg")
    await asyncio.sleep(2)
    await send_msg(app, """🔗 Cola o link do teu PERFIL

❤️ Dá 5 favoritos em CADA perfil
❗ É obrigatório interagir com TODOS os perfis

🚨 Se já não tiveres favoritos suficientes para dar (perfil cheio com os teus ❤️), cria um conjunto com o número de artigos em falta

⏰ Cumpre o horário""")

async def stop_1400(app):
    await stop(app)


# ------------------ 17:00 (TODOS OS DIAS) ------------------

async def go_1700(app):
    await send_photo(app, "roupeiro5favs_17h00.jpg")
    await asyncio.sleep(2)
    await send_msg(app, """🔗 Cola o link do teu PERFIL

❤️ Dá 5 favoritos em CADA perfil
❗ É obrigatório interagir com TODOS os perfis

🚨 Se já não tiveres favoritos suficientes para dar (perfil cheio com os teus ❤️), cria um conjunto com o número de artigos em falta

⏰ Cumpre o horário""")

async def stop_1900(app):
    await stop(app)


# ------------------ 20:00 (TODOS OS DIAS) ------------------

async def go_2000(app):
    await send_photo(app, "roupeiro10favs_20h00.jpg")
    await asyncio.sleep(2)
    await send_msg(app, """🔗 Cola o link do teu PERFIL

❤️ Dá 10 favoritos em CADA perfil
❗ É obrigatório interagir com TODOS os perfis

🚨 Se já não tiveres favoritos suficientes para dar (perfil cheio com os teus ❤️), cria um conjunto com o número de artigos em falta

⏰ Cumpre o horário""")

async def stop_2200(app):
    await stop(app)


# ------------------ NOTURNAS ------------------

async def go_noturna_util(app):
    hoje = datetime.now().date()
    dia = datetime.now().weekday()
    # Seg=0, Ter=1, Qua=2, Qui=3, Dom=6 — e não véspera de feriado
    if dia in [0, 1, 2, 3, 6] and not is_eve_of_holiday(hoje):
        await send_photo(app, "roupeiro5favs_22h30.jpg")
        await asyncio.sleep(2)
        await send_msg(app, """🔗 Cola o link do teu PERFIL

❤️ Dá 5 favoritos em CADA perfil
❗ É obrigatório interagir com TODOS os perfis

🚨 Se já não tiveres favoritos suficientes para dar (perfil cheio com os teus ❤️), cria um conjunto com o número de artigos em falta

⏰ Cumpre o horário""")

async def go_noturna_fds(app):
    hoje = datetime.now().date()
    dia = datetime.now().weekday()
    # Sex=4, Sáb=5 — ou véspera de feriado — ou o próprio dia é feriado
    if dia in [4, 5] or is_eve_of_holiday(hoje) or is_holiday_or_weekend(hoje):
        await send_photo(app, "roupeiro10favs_23h00.jpg")
        await asyncio.sleep(2)
        await send_msg(app, """🔗 Cola o link do teu PERFIL

❤️ Dá 10 favoritos em CADA perfil
❗ É obrigatório interagir com TODOS os perfis

🚨 Se já não tiveres favoritos suficientes para dar (perfil cheio com os teus ❤️), cria um conjunto com o número de artigos em falta

⏰ Cumpre o horário""")

async def stop_noturna_util(app):
    hoje = datetime.now().date()
    ontem = hoje - timedelta(days=1)
    dia_ontem = ontem.weekday()
    # STOP só dispara se a sessão util tiver arrancado ontem
    if dia_ontem in [0, 1, 2, 3, 6] and not is_eve_of_holiday(ontem):
        await stop(app)

async def stop_noturna_fds(app):
    hoje = datetime.now().date()
    ontem = hoje - timedelta(days=1)
    dia_ontem = ontem.weekday()
    # ✅ CORRIGIDO: cobre Sex/Sáb, véspera de feriado, e feriados
    if dia_ontem in [4, 5] or is_eve_of_holiday(ontem) or is_holiday_or_weekend(ontem):
        await stop(app)


# ------------------ LEMBRETE 2020 ------------------

async def reminder_2020(app):
    await send_msg(app, """Se queres MESMO vender, publica novos artigos ou republica os antigos (apaga e volta a publicar) ♻️🆕🔄

A Vinted adora contas dinâmicas… e ainda mais os artigos recentes 🤫🚀

Cereja no topo do bolo? Leva esses anúncios a jogo logo em seguida 🎮▶️😎""")


# ------------------ MAIN ------------------

async def main():
    app = Application.builder().token(TOKEN).build()

    scheduler.add_job(go_1200, "cron", hour=12, minute=0, args=[app])
    scheduler.add_job(stop_1400, "cron", hour=14, minute=0, args=[app])

    scheduler.add_job(go_1700, "cron", hour=17, minute=0, args=[app])
    scheduler.add_job(stop_1900, "cron", hour=19, minute=0, args=[app])

    scheduler.add_job(go_2000, "cron", hour=20, minute=0, args=[app])
    scheduler.add_job(stop_2200, "cron", hour=22, minute=0, args=[app])

    scheduler.add_job(go_noturna_util, "cron", hour=22, minute=30, args=[app])
    scheduler.add_job(go_noturna_fds, "cron", hour=23, minute=0, args=[app])
    scheduler.add_job(stop_noturna_util, "cron", hour=9, minute=0, args=[app])
    scheduler.add_job(stop_noturna_fds, "cron", hour=10, minute=30, args=[app])

    scheduler.add_job(reminder_2020, "cron", hour=11, minute=30, args=[app])
    scheduler.add_job(reminder_2020, "cron", hour=16, minute=30, args=[app])
    scheduler.add_job(reminder_2020, "cron", hour=19, minute=30, args=[app])
    scheduler.add_job(reminder_2020, "cron", hour=22, minute=20, args=[app])

    scheduler.start()
    print("Bot a correr...")

    async with app:
        await app.start()
        await app.updater.start_polling()

        while True:
            await asyncio.sleep(60)


# ✅ CORRIGIDO: __name__ e "__main__" com underscores
if __name__ == "__main__":
    asyncio.run(main())
    
