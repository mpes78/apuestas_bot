import os, random, asyncio, pytz
from datetime import datetime
from telegram import Bot, constants

CHAT_ID = int(os.getenv("CHAT_ID"))
TOKEN   = os.getenv("BOT_TOKEN")
if not (TOKEN and CHAT_ID):
    raise RuntimeError("Faltan BOT_TOKEN o CHAT_ID")

PARTIDOS = [
    ("Alianza Lima", "UTC Cajamarca"),
    ("Sporting Cristal", "Universitario"),
    ("Liverpool", "Chelsea"),
    ("Real Madrid", "Cádiz"),
    ("Bayern", "Augsburg"),
]

async def main():
    bot = Bot(TOKEN)
    fecha = datetime.now(pytz.timezone("America/Lima")).strftime("%d/%m/%Y")
    elegidos = random.sample(PARTIDOS, 3)
    texto = [f"📅 <b>Picks {fecha}</b>\n"]
    for loc, vis in elegidos:
        mercado = random.choice(["Más de 2.5 goles", "Victoria local", "Ambos anotan: Sí"])
        texto.append(f"⚽ <b>{loc} vs {vis}</b>\n🔹 <i>Apuesta:</i> {mercado}\n")
    await bot.send_message(chat_id=CHAT_ID,
                           text="\n".join(texto),
                           parse_mode=constants.ParseMode.HTML)

asyncio.run(main())