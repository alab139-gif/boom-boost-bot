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
    await send_photo(app, "stop.png")
    await asyncio.sleep(2)
    await send_msg(app, """⚠️ ATENÇÃO: confirma que deste os favoritos a cada um dos participantes desta sessão

🫶🏻 Obrigada pela participação
👋🏻 Até à próxima""")


# ------------------ 13:00 (DIAS ÚTEIS) ------------------

async def go_1300(app):
    hoje = datetime.now().date()
    if not is_holiday_or_weekend(hoje):
        await send_photo(app, "3links13h.png")
        await asyncio.sleep(2)
        await send_msg(app, """🔗 Partilha 3 links de ARTIGOS (não de perfil)
⚠️ 1 link por linha na mesma mensagem:

1️⃣ https://vinted.pt/...
2️⃣ https://vinted.pt/...
3️⃣ https://vinted.pt/...

❤️ Abre TODOS os links desta sessão e dá 1 favorito em cada um deles
❗ É obrigatório interagir com TODOS

ℹ️ As reações (emojis) no Telegram são opcionais
🚨 Exceto nos jogos de artigos, em que é OBRIGATÓRIO reagir com 👀, SE algum dos artigos já tiver o teu favorito (mesmo que consigas dar favoritos normalmente nos restantes)
👀 As visualizações também ajudam muito o algoritmo

⏰ Cumpre o horário""")

async def stop_1400_links(app):
    hoje = datetime.now().date()
    if not is_holiday_or_weekend(hoje):
        await send_photo(app, "stop.png")
        await asyncio.sleep(2)
        await send_msg(app, """⚠️ ATENÇÃO: confirma que deste os favoritos a cada um dos participantes desta sessão

🫶🏻 Obrigada pela participação
👋🏻 Até à próxima""")


# ------------------ 14:00 (FERIADOS, SÁB, DOM) ------------------

async def go_1400_fds(app):
    hoje = datetime.now().date()

    if is_holiday_or_weekend(hoje):
        await send_photo(app, "3links14h.png")
        await asyncio.sleep(2)
        await send_msg(app, """🔗 Partilha 3 links de ARTIGOS (não de perfil)
⚠️ 1 link por linha na mesma mensagem:

1️⃣ https://vinted.pt/...
2️⃣ https://vinted.pt/...
3️⃣ https://vinted.pt/...

❤️ Abre TODOS os links desta sessão e dá 1 favorito em cada um deles
❗ É obrigatório interagir com TODOS

ℹ️ As reações (emojis) no Telegram são opcionais
🚨 Exceto nos jogos de artigos, em que é OBRIGATÓRIO reagir com 👀, SE algum dos artigos já tiver o teu favorito (mesmo que consigas dar favoritos normalmente nos restantes)
👀 As visualizações também ajudam muito o algoritmo

⏰ Cumpre o horário""")

async def stop_1500_fds(app):
    hoje = datetime.now().date()
    
    if is_holiday_or_weekend(hoje):
        await send_photo(app, "stop.png")
        await asyncio.sleep(2)
        await send_msg(app, """⚠️ ATENÇÃO: confirma que deste os favoritos a cada um dos participantes desta sessão

🫶🏻 Obrigada pela participação
👋🏻 Até à próxima""")


# ------------------ 21:00 (ALTERNADO) ------------------

async def go_2100(app):
    dia = datetime.now().weekday()
    if dia in [0, 2, 4]:  # Seg, Qua, Sex → 3 links
        await send_photo(app, "3links21h.png")
        await asyncio.sleep(2)
        await send_msg(app, """🔗 Partilha 3 links de ARTIGOS (não de perfil)
⚠️ 1 link por linha na mesma mensagem:

1️⃣ https://vinted.pt/...
2️⃣ https://vinted.pt/...
3️⃣ https://vinted.pt/...

❤️ Abre TODOS os links desta sessão e dá 1 favorito em cada um deles
❗ É obrigatório interagir com TODOS

ℹ️ As reações (emojis) no Telegram são opcionais
🚨 Exceto nos jogos de artigos, em que é OBRIGATÓRIO reagir com 👀, SE algum dos artigos já tiver o teu favorito (mesmo que consigas dar favoritos normalmente nos restantes)
👀 As visualizações também ajudam muito o algoritmo

⏰ Cumpre o horário""")
    elif dia in [1, 3, 5, 6]:  # Ter, Qui, Sáb, Dom → perfil
        await send_photo(app, "perfil5terquisabdom.png")
        await asyncio.sleep(2)
        await send_msg(app, """🔗 Cola o link do teu PERFIL

❤️ Abre TODOS os links desta sessão e dá 5 favoritos em CADA perfil
❗ É obrigatório interagir com TODOS os perfis

ℹ️ As reações (emojis) no Telegram são opcionais

🚨 Se algum perfil não tiver artigos disponíveis suficientes para completares os favoritos:

🅰️ Cria um conjunto com os artigos em falta e envia esta mensagem: "🚀"

OU

🅱️ Se faltar apenas 1 favorito, envia esta mensagem: "🚀" num artigo à tua escolha

⏰ Cumpre o horário""")

async def stop_2200(app):
    await stop(app)


# ------------------ NOTURNAS ------------------

async def go_noturna_util(app):
    hoje = datetime.now().date()
    dia = datetime.now().weekday()
    # Dom=6, Seg=0, Ter=1, Qua=2, Qui=3 — e não véspera de feriado
    if dia in [6, 0, 1, 2, 3] and not is_eve_of_holiday(hoje):
        await send_photo(app, "noturnauteis.png")
        await asyncio.sleep(2)
        await send_msg(app, """🔗 Cola o link do teu PERFIL

❤️ Abre TODOS os links desta sessão e dá 5 favoritos em CADA perfil
❗ É obrigatório interagir com TODOS os perfis

ℹ️ As reações (emojis) no Telegram são opcionais

🚨 Se algum perfil não tiver artigos disponíveis suficientes para completares os favoritos:

🅰️ Cria um conjunto com os artigos em falta e envia esta mensagem: "🚀"

OU

🅱️ Se faltar apenas 1 favorito, envia esta mensagem: "🚀" num artigo à tua escolha

⏰ Cumpre o horário""")

async def go_noturna_fds(app):
    hoje = datetime.now().date()
    dia = datetime.now().weekday()
    # Sex=4, Sáb=5 — ou véspera de feriado (qualquer dia)
    if dia in [4, 5] or is_eve_of_holiday(hoje):
        await send_photo(app, "noturnaferiadosefds.png")
        await asyncio.sleep(2)
        await send_msg(app, """🔗 Cola o link do teu PERFIL

❤️ Abre TODOS os links desta sessão e dá 10 favoritos em CADA perfil
❗ É obrigatório interagir com TODOS os perfis

ℹ️ As reações (emojis) no Telegram são opcionais

🚨 Se algum perfil não tiver artigos disponíveis suficientes para completares os favoritos:

🅰️ Cria um conjunto com os artigos em falta e envia esta mensagem: "🚀"

OU

🅱️ Se faltar apenas 1 favorito, envia esta mensagem: "🚀" num artigo à tua escolha

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

    # Espelha go_noturna_fds: Sex=4, Sáb=5 — ou véspera de feriado
    if dia_ontem in [4, 5] or is_eve_of_holiday(ontem):
        await stop(app)


# ------------------ LEMBRETES ------------------

async def reminder_1300(app):
    hoje = datetime.now().date()

    if not is_holiday_or_weekend(hoje):
        await send_msg(app, """🕐 Próxima sessão às 13:00

🔗 Começa a preparar 3 links de artigos (de preferência renovados ♻️🆕)

⏰ Marca um lembrete para não te esqueceres

🚀🔥""")


async def reminder_1400(app):
    hoje = datetime.now().date()

    if is_holiday_or_weekend(hoje):
        await send_msg(app, """🕑 Próxima sessão às 14:00

🔗 Começa a preparar 3 links de artigos (de preferência renovados ♻️🆕)

⏰ Marca um lembrete para não te esqueceres

🚀🔥""")


async def reminder_2100_links(app):
    await send_msg(app, """🕘 Próxima sessão às 21:00

🔗 Começa a preparar 3 links de artigos (de preferência renovados ♻️🆕)

⏰ Marca um lembrete para não te esqueceres

🚀🔥""")


async def reminder_2100_profile(app):
    await send_msg(app, """🕘 Próxima sessão às 21:00

🔗 Começa a preparar o teu link de perfil (de preferência com artigos renovados ♻️🆕)

⏰ Marca um lembrete para não te esqueceres

🚀🔥""")


async def reminder_2230(app):
    await send_msg(app, """🕥 Próxima sessão às 22:30

🔗 Começa a preparar o teu link de perfil (de preferência com artigos renovados ♻️🆕)

⏰ Marca um lembrete para não te esqueceres

🚀🔥""")


async def reminder_vendas(app):
    hoje = datetime.now().date()

    if not is_holiday_or_weekend(hoje):
        await send_msg(app, """Se queres MESMO vender, publica novos artigos ou republica os antigos (apaga e volta a publicar) ♻️🆕🔄

A Vinted adora contas dinâmicas… e ainda mais os artigos recentes 🤫🚀

Cereja no topo do bolo? Leva esses anúncios a jogo logo em seguida 🎮▶️😎""")


async def reminder_vendas_fds(app):
    hoje = datetime.now().date()

    if is_holiday_or_weekend(hoje):
        await send_msg(app, """Se queres MESMO vender, publica novos artigos ou republica os antigos (apaga e volta a publicar) ♻️🆕🔄

A Vinted adora contas dinâmicas… e ainda mais os artigos recentes 🤫🚀

Cereja no topo do bolo? Leva esses anúncios a jogo logo em seguida 🎮▶️😎""")

# ------------------ MAIN ------------------

async def main():
    app = Application.builder().token(TOKEN).build()

    # SESSÕES
    scheduler.add_job(go_1300, "cron", hour=13, minute=0, args=[app])
    scheduler.add_job(stop_1400_links, "cron", hour=14, minute=0, args=[app])

    scheduler.add_job(go_1400_fds, "cron", hour=14, minute=0, args=[app])
    scheduler.add_job(stop_1500_fds, "cron", hour=15, minute=0, args=[app])

    scheduler.add_job(go_2100, "cron", hour=21, minute=0, args=[app])
    scheduler.add_job(stop_2200, "cron", hour=22, minute=0, args=[app])

    scheduler.add_job(go_noturna_util, "cron", hour=22, minute=30, args=[app])
    scheduler.add_job(go_noturna_fds, "cron", hour=22, minute=30, args=[app])

    scheduler.add_job(stop_noturna_util, "cron", hour=9, minute=0, args=[app])
    scheduler.add_job(stop_noturna_fds, "cron", hour=10, minute=30, args=[app])

    # ---------- LEMBRETES ----------

    # almoço úteis
    scheduler.add_job(
        reminder_1300,
        "cron",
        hour=12,
        minute=30,
        args=[app]
    )

    scheduler.add_job(
        reminder_vendas,
        "cron",
        hour=12,
        minute=40,
        args=[app]
    )

    # almoço fins de semana / feriados
    scheduler.add_job(
        reminder_1400,
        "cron",
        hour=13,
        minute=30,
        args=[app]
    )

    scheduler.add_job(
        reminder_vendas_fds,
        "cron",
        hour=13,
        minute=40,
        args=[app]
    )

    # sessão 21h → links
    scheduler.add_job(
        reminder_2100_links,
        "cron",
        hour=20,
        minute=30,
        day_of_week="mon,wed,fri",
        args=[app]
    )

    # sessão 21h → perfil
    scheduler.add_job(
        reminder_2100_profile,
        "cron",
        hour=20,
        minute=30,
        day_of_week="tue,thu,sat,sun",
        args=[app]
    )

    scheduler.add_job(
        reminder_vendas,
        "cron",
        hour=20,
        minute=40,
        args=[app]
    )

    # noturna
    scheduler.add_job(
        reminder_2230,
        "cron",
        hour=22,
        minute=15,
        args=[app]
    )

    scheduler.add_job(
        reminder_vendas,
        "cron",
        hour=22,
        minute=20,
        args=[app]
    )

    scheduler.start()

    print("Bot a correr...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        await asyncio.Event().wait()

    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())=0, args=[app])
    scheduler.add_job(stop_1500_fds, "cron", hour=15, minute=0, args=[app])

    scheduler.add_job(go_2100, "cron", hour=21, minute=0, args=[app])
    scheduler.add_job(stop_2200, "cron", hour=22, minute=0, args=[app])

    scheduler.add_job(go_noturna_util, "cron", hour=22, minute=30, args=[app])
    scheduler.add_job(go_noturna_fds, "cron", hour=22, minute=30, args=[app])

    scheduler.add_job(stop_noturna_util, "cron", hour=9, minute=0, args=[app])
    scheduler.add_job(stop_noturna_fds, "cron", hour=10, minute=30, args=[app])

    # ---------- LEMBRETES ----------

    # almoço úteis
    scheduler.add_job(
        reminder_1300,
        "cron",
        hour=12,
        minute=30,
        args=[app]
    )

    scheduler.add_job(
        reminder_vendas,
        "cron",
        hour=12,
        minute=40,
        args=[app]
    )

    # almoço fins de semana / feriados
    scheduler.add_job(
        reminder_1400,
        "cron",
        hour=13,
        minute=30,
        args=[app]
    )

    scheduler.add_job(
        reminder_vendas_fds,
        "cron",
        hour=13,
        minute=40,
        args=[app]
    )

    # sessão 21h → links
    scheduler.add_job(
        reminder_2100_links,
        "cron",
        hour=20,
        minute=30,
        day_of_week="mon,wed,fri",
        args=[app]
    )

    # sessão 21h → perfil
    scheduler.add_job(
        reminder_2100_profile,
        "cron",
        hour=20,
        minute=30,
        day_of_week="tue,thu,sat,sun",
        args=[app]
    )

    scheduler.add_job(
        reminder_vendas,
        "cron",
        hour=20,
        minute=40,
        args=[app]
    )

    # noturna
    scheduler.add_job(
        reminder_2230,
        "cron",
        hour=22,
        minute=15,
        args=[app]
    )

    scheduler.add_job(
        reminder_vendas,
        "cron",
        hour=22,
        minute=20,
        args=[app]
    )

    scheduler.start()

    print("Bot a correr...")

    await app.initialize()
    await app.start()
    await app.updater.start_polling()

    try:
        await asyncio.Event().wait()

    finally:
        await app.updater.stop()
        await app.stop()
        await app.shutdown()


if __name__ == "__main__":
    asyncio.run(main())
