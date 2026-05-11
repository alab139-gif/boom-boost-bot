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

# ✅ CORRIGIDO
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

    await send_msg(app, """🚨 Deixa tudo em ordem

🫶🏻 Obrigada pela participação  
👋🏻 Até à próxima""")

# ------------------ 12:30 (DIAS ÚTEIS) ------------------

async def go_1230(app):
    hoje = datetime.now().date()
    if not is_holiday_or_weekend(hoje):
        await send_photo(app, "roupeiro1230.jpg")

        await asyncio.sleep(2)

        await send_msg(app, """🔗 Coloca o link do teu PERFIL

❤️ Dá 5 favoritos em CADA perfil
❗ É obrigatório interagir com TODOS

🚨 Se já não tiveres favoritos suficientes para dar (perfil cheio com os teus ❤️), cria um conjunto com o número de artigos em falta

⏰ Cumpre o horário""")

async def stop_1300(app):
    hoje = datetime.now().date()
    if not is_holiday_or_weekend(hoje):
        await stop(app)

# ------------------ 14:30 (FDS/FERIADOS) ------------------

async def go_1430(app):
    hoje = datetime.now().date()
    if is_holiday_or_weekend(hoje):
        await send_photo(app, "roupeiro1430.jpg")

        await asyncio.sleep(2)

        await send_msg(app, """🔗 Coloca o link do teu PERFIL

❤️ Dá 5 favoritos em CADA perfil
❗ É obrigatório interagir com TODOS

🚨 Se já não tiveres favoritos suficientes para dar (perfil cheio com os teus ❤️), cria um conjunto com o número de artigos em falta

⏰ Cumpre o horário""")

async def stop_1500(app):
    hoje = datetime.now().date()
    if is_holiday_or_weekend(hoje):
        await stop(app)

# ------------------ 17:30 ------------------

async def go_1730(app):
    await send_photo(app, "roupeiro1730.jpg")

    await asyncio.sleep(2)

    await send_msg(app, """🔗 Coloca o link do teu PERFIL

❤️ Dá 5 favoritos em CADA perfil
❗ É obrigatório interagir com TODOS

🚨 Se já não tiveres favoritos suficientes para dar (perfil cheio com os teus ❤️), cria um conjunto com o número de artigos em falta

⏰ Cumpre o horário""")

async def stop_1800(app):
    await stop(app)

# ------------------ 21:00 ------------------

async def go_21(app):
    dia = datetime.now().weekday()

    if dia in [0, 2, 4]:
        await send_photo(app, "5artigos.jpg")

        await asyncio.sleep(2)

        await send_msg(app, """🔗 Coloca 5 links de ARTIGOS (não perfil)
⚠️ 1 link por linha na mesma mensagem:

1️⃣ https://vinted.pt/...
2️⃣ https://vinted.pt/...
3️⃣ https://vinted.pt/...
4️⃣ https://vinted.pt/...
5️⃣ https://vinted.pt/...

❤️ Abre TODOS os links e dá 1 favorito em cada um deles
❗ É obrigatório interagir com TODOS

🚨 Se algum artigo já tiver like, reage com: 👀

⏰ Cumpre o horário""")

    else:
        await send_photo(app, "roupeiro10favs_21h.jpg")

        await asyncio.sleep(2)

        await send_msg(app, """🔗 Coloca o link do teu PERFIL

❤️ Dá 10 favoritos em CADA perfil
❗ É obrigatório interagir com TODOS

🚨 Se já não tiveres favoritos suficientes para dar (perfil cheio com os teus ❤️), cria um conjunto com o número de artigos em falta

⏰ Cumpre o horário""")

# ------------------ NOTURNAS ------------------

async def go_noturna_util(app):
    hoje = datetime.now().date()
    dia = datetime.now().weekday()

    if dia in [0, 1, 2, 3, 6] and not is_eve_of_holiday(hoje):
        await send_photo(app, "roupeiro5favs_22h30.jpg")

        await asyncio.sleep(2)

        await send_msg(app, """🔗 Coloca o link do teu PERFIL

❤️ Dá 5 favoritos em CADA perfil
❗ É obrigatório interagir com TODOS

🚨 Se já não tiveres favoritos suficientes para dar (perfil cheio com os teus ❤️), cria um conjunto com o número de artigos em falta

⏰ Cumpre o horário""")

async def go_noturna_fds(app):
    hoje = datetime.now().date()
    dia = datetime.now().weekday()

    if dia in [4, 5] or is_eve_of_holiday(hoje):
        await send_photo(app, "roupeiro10favs_23h00.jpg")

        await asyncio.sleep(2)

        await send_msg(app, """🔗 Coloca o link do teu PERFIL

❤️ Dá 10 favoritos em CADA perfil
❗ É obrigatório interagir com TODOS

🚨 Se já não tiveres favoritos suficientes para dar (perfil cheio com os teus ❤️), cria um conjunto com o número de artigos em falta

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

# ------------------ TURBO ONE (DIAS ÚTEIS) ------------------

async def go_turbo_one_util(app, photo_name):
    hoje = datetime.now().date()

    if not is_holiday_or_weekend(hoje):
        await send_photo(app, photo_name)

        await asyncio.sleep(2)

        await send_msg(app, """🔗 Coloca 1 link de ARTIGO (não perfil)

❤️ Abre TODOS os links e dá 1 favorito em cada um deles
❗ É obrigatório interagir com TODOS

🚨 Se algum artigo já tiver like, reage com: 👀

⏰ Cumpre o horário""")

# ------------------ TURBO DUO (DIAS ÚTEIS) ------------------

async def go_turbo_duo_util(app):
    hoje = datetime.now().date()

    if not is_holiday_or_weekend(hoje):
        await send_photo(app, "turbo_duo_dias_uteis_19h20.jpg")

        await asyncio.sleep(2)

        await send_msg(app, """🔗 Coloca 2 links de ARTIGOS (não perfil)
⚠️ 1 link por linha na mesma mensagem:

1️⃣ https://vinted.pt/...
2️⃣ https://vinted.pt/...

❤️ Abre TODOS os links e dá 1 favorito em cada um deles
❗ É obrigatório interagir com TODOS

🚨 Se algum artigo já tiver like, reage com: 👀

⏰ Cumpre o horário""")

# ------------------ TURBO ONE (FDS/FERIADOS) ------------------

async def go_turbo_one_fds(app, photo_name):
    hoje = datetime.now().date()

    if is_holiday_or_weekend(hoje):
        await send_photo(app, photo_name)

        await asyncio.sleep(2)

        await send_msg(app, """🔗 Coloca 1 link de ARTIGO

❤️ Abre TODOS os links e dá 1 favorito em cada um deles
❗ É obrigatório interagir com TODOS

🚨 Se algum artigo já tiver like, reage com: 👀

⏰ Cumpre o horário""")

# ------------------ TURBO DUO (FDS/FERIADOS) ------------------

async def go_turbo_duo_fds(app, photo_name):
    hoje = datetime.now().date()

    if is_holiday_or_weekend(hoje):
        await send_photo(app, photo_name)

        await asyncio.sleep(2)

        await send_msg(app, """🔗 Coloca 2 links de ARTIGOS (não perfil)
⚠️ 1 link por linha na mesma mensagem:

1️⃣ https://vinted.pt/...
2️⃣ https://vinted.pt/...

❤️ Abre TODOS os links e dá 1 favorito em cada um deles
❗ É obrigatório interagir com TODOS

🚨 Se algum artigo já tiver like, reage com: 👀

⏰ Cumpre o horário""")

# ------------------ LEMBRETE 20:20 ------------------

async def reminder_2020(app):
    await send_msg(app, """Se queres MESMO vender, publica novos artigos ou republica os antigos (apaga e volta a publicar) ♻️🆕🔄

A Vinted adora contas dinâmicas… e ainda mais os artigos recentes 🤫🚀

Cereja no topo do bolo? Leva esses anúncios a jogo 🎮▶️😎""")

# ------------------ STOPS TURBO ------------------

async def stop_util(app):
    hoje = datetime.now().date()

    if not is_holiday_or_weekend(hoje):
        await stop(app)

async def stop_fds(app):
    hoje = datetime.now().date()

    if is_holiday_or_weekend(hoje):
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

    # ------------------ TURBO ONE (DIAS ÚTEIS) ------------------

    scheduler.add_job(
        go_turbo_one_util,
        "cron",
        hour=18,
        minute=45,
        args=[app, "turbo_one_dias_uteis_18h45.jpg"]
    )

    scheduler.add_job(
        go_turbo_one_util,
        "cron",
        hour=20,
        minute=0,
        args=[app, "turbo_one_dias_uteis_20h00.jpg"]
    )

    scheduler.add_job(
        go_turbo_one_util,
        "cron",
        hour=22,
        minute=10,
        args=[app, "turbo_one_dias_uteis_22h10.jpg"]
    )

    scheduler.add_job(stop_util, "cron", hour=18, minute=55, args=[app])

    scheduler.add_job(stop_util, "cron", hour=20, minute=10, args=[app])

    scheduler.add_job(reminder_2020, "cron", hour=20, minute=20, args=[app])

    scheduler.add_job(stop_util, "cron", hour=22, minute=20, args=[app])

    # ------------------ TURBO DUO (DIAS ÚTEIS) ------------------

    scheduler.add_job(
        go_turbo_duo_util,
        "cron",
        hour=19,
        minute=20,
        args=[app]
    )

    scheduler.add_job(stop_util, "cron", hour=19, minute=35, args=[app])

# ------------------ TURBO ONE (FDS/FERIADOS) ------------------

    scheduler.add_job(
        go_turbo_one_fds,
        "cron",
        hour=11,
        minute=0,
        args=[app, "turbo_one_feriados_fds_11h00.jpg"]
    )

    scheduler.add_job(
        go_turbo_one_fds,
        "cron",
        hour=15,
        minute=30,
        args=[app, "turbo_one_feriados_fds_15h30.jpg"]
    )

    scheduler.add_job(
        go_turbo_one_fds,
        "cron",
        hour=16,
        minute=45,
        args=[app, "turbo_one_feriados_fds_16h45.jpg"]
    )

    scheduler.add_job(
        go_turbo_one_fds,
        "cron",
        hour=18,
        minute=30,
        args=[app, "turbo_one_feriados_fds_18h30.jpg"]
    )

    scheduler.add_job(
        go_turbo_one_fds,
        "cron",
        hour=19,
        minute=20,
        args=[app, "turbo_one_feriados_fds_19h20.jpg"]
    )

    scheduler.add_job(
        go_turbo_one_fds,
        "cron",
        hour=22,
        minute=15,
        args=[app, "turbo_one_feriados_fds_22h15.jpg"]
    )

    scheduler.add_job(
        go_turbo_one_fds,
        "cron",
        hour=22,
        minute=35,
        args=[app, "turbo_one_feriados_fds_22h35.jpg"]
    )

    scheduler.add_job(stop_fds, "cron", hour=11, minute=10, args=[app])
    scheduler.add_job(stop_fds, "cron", hour=15, minute=40, args=[app])
    scheduler.add_job(stop_fds, "cron", hour=16, minute=55, args=[app])
    scheduler.add_job(stop_fds, "cron", hour=18, minute=40, args=[app])
    scheduler.add_job(stop_fds, "cron", hour=19, minute=30, args=[app])
    scheduler.add_job(stop_fds, "cron", hour=22, minute=25, args=[app])
    scheduler.add_job(stop_fds, "cron", hour=22, minute=45, args=[app])

# ------------------ TURBO DUO (FDS/FERIADOS) ------------------

    scheduler.add_job(
    go_turbo_duo_fds,
    "cron",
    hour=11,
    minute=30,
    args=[app, "turbo_duo_feriados_fds_11h30.jpg"]
)

    scheduler.add_job(
    go_turbo_duo_fds,
    "cron",
    hour=16,
    minute=0,
    args=[app, "turbo_duo_feriados_fds_16h00.jpg"]
)

    scheduler.add_job(
    go_turbo_duo_fds,
    "cron",
    hour=18,
    minute=50,
    args=[app, "turbo_duo_feriados_fds_18h50.jpg"]
)

    scheduler.add_job(
    go_turbo_duo_fds,
    "cron",
    hour=19,
    minute=40,
    args=[app, "turbo_duo_feriados_fds_19h40.jpg"]
)

    scheduler.add_job(stop_fds, "cron", hour=11, minute=45, args=[app])
    scheduler.add_job(stop_fds, "cron", hour=16, minute=15, args=[app])
    scheduler.add_job(stop_fds, "cron", hour=19, minute=5, args=[app])
    scheduler.add_job(stop_fds, "cron", hour=19, minute=55, args=[app])

    scheduler.add_job(go_21, "cron", hour=21, minute=0, args=[app])
    scheduler.add_job(stop, "cron", hour=22, minute=0, args=[app])

    scheduler.add_job(go_noturna_util, "cron", hour=22, minute=30, args=[app])
    scheduler.add_job(go_noturna_fds, "cron", hour=23, minute=00, args=[app])
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
