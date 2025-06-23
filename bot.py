"""
bot.py  –  Versión demo 1.0
Envía 3 picks de apuestas cada día a las 10 a. m. (hora Lima).

Requisitos: python-telegram-bot, pandas, requests, pytz
La variable de entorno BOT_TOKEN debe contener tu token de BotFather.
"""

import os, asyncio, random, logging
from datetime import datetime, timedelta
import pytz
from telegram import Bot, constants

# Zona horaria Lima
LIMA = pytz.timezone("America/Lima")
SEND_HOUR, SEND_MIN = 10, 0

BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise RuntimeError("Define la variable de entorno BOT_TOKEN")

DEMO_MATCHES = [
    ("Alianza Lima", "UTC Cajamarca"),
    ("Sporting Cristal", "Universitario"),
    ("Liverpool", "Chelsea"),
    ("Real Madrid", "Cádiz"),
    ("Bayern", "Augsburg"),
]

async def get_picks():
    picks = []
    for local, visita in random.sample(DEMO_MATCHES, 3):
        mercado = random.choice(["Más de 2.5 goles",
                                 "Victoria local",
                                 "Ambos anotan: Sí"])
        prob = random.uniform(0.70, 0.90)
        cuota = round(1 / prob, 2)
        ev = round((prob * cuota) - (1 - prob), 2)
        picks.append(dict(
            partido=f"{local} vs {visita}",
            mercado=mercado, prob=prob, cuota=cuota, ev=ev))
    return picks

def format_msg(picks):
    bloques = []
    for p in picks:
        bloques.append(
            f"⚽ <b>{p['partido']}</b>\n"
            f"🔹 <i>Apuesta:</i> {p['mercado']}\n"
            f"🔍 <i>Prob:</i> {p['prob']*100:.1f}%\n"
            f"💰 <i>Cuota:</i> {p['cuota']}\n"
            f"📈 <i>EV:</i> {p['ev']:+}\n"
            f"✅ <b>Recomendado</b>\n")
    return "\n".join(bloques)

async def send_picks(bot: Bot):
    picks = await get_picks()
    fecha = datetime.now(LIMA).strftime("%d/%m/%Y")
    msg = f"📅 <b>Recomendaciones del día – {fecha}</b>\n\n{format_msg(picks)}"
    await bot.send_message(chat_id="@me", text=msg,
                           parse_mode=constants.ParseMode.HTML)

async def main_loop():
    bot = Bot(BOT_TOKEN)
    while True:
        now = datetime.now(LIMA)
        next_run = now.replace(hour=SEND_HOUR, minute=SEND_MIN,
                               second=0, microsecond=0)
        if now >= next_run:
            next_run += timedelta(days=1)
        await asyncio.sleep((next_run - now).total_seconds())
        try:
            await send_picks(bot)
        except Exception as e:
            logging.exception(e)
        await asyncio.sleep(60)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(message)s")
    asyncio.run(main_loop())
