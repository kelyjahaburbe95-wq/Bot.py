from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler
import asyncio
import os

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")  # Render doit contenir BOT_TOKEN dans les variables d'env
CANAL_PRINCIPAL = "https://t.me/+3RSkDPs9bS02NDZk"

# Application Telegram
application = Application.builder().token(TOKEN).build()

# === COMMANDE /start ===
async def start(update: Update, context):
    keyboard = [[InlineKeyboardButton("Canal principal 🔵", url=CANAL_PRINCIPAL)]]
    await update.message.reply_text(
        "Bienvenue sur le bot !\n\nClique ci-dessous pour rejoindre le canal officiel ⬇️",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

application.add_handler(CommandHandler("start", start))

# === FLASK WEBHOOK ROUTE ===
@app.post("/webhook")
def webhook():
    data = request.get_json()

    if data:
        update = Update.de_json(data, application.bot)
        asyncio.run(application.process_update(update))

    return "OK", 200

# === PAGE D'ACCUEIL ===
@app.get("/")
def home():
    return "Bot Telegram en ligne ✔️"