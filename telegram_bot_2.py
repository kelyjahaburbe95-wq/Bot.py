from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")

CANAL_PRINCIPAL = "https://t.me/+3RSkDPs9bS02NDZk"
NOUVEAU_CANAL = "https://t.me/tonNouveauCanal"

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Canal principal 🔵", url=CANAL_PRINCIPAL)],
        [InlineKeyboardButton("Que Du Cul 🔞", url=t.me/QDCqueducul)]
    
    await update.message.reply_text(
        "Bienvenue sur le bot !\n\nChoisis un canal ci-dessous ⬇️",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

application.add_handler(CommandHandler("start", start))

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    asyncio.run(application.process_update(Update.de_json(data, application.bot)))
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))