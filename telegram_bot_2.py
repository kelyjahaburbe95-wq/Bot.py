from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")

CANAL_PRINCIPAL = "https://t.me/+3RSkDPs9bS02NDZk"
NOUVEAU_CANAL = "https://t.me/+3lW8pf60_hBhNDU0"

app = Flask(__name__)

# CREATE APPLICATION (IMPORTANT)
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Canal principal 🔵", url=CANAL_PRINCIPAL)],
        [InlineKeyboardButton("Que Du Cul 🔞", url=NOUVEAU_CANAL)]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Bienvenue sur le bot !\n\nChoisis un canal ci-dessous ⬇️",
        reply_markup=reply_markup
    )

application.add_handler(CommandHandler("start", start))

# RUN WEBHOOK (DOIT ÊTRE APRÈS 'application =')
application.run_webhook(
    listen="0.0.0.0",
    port=int(os.environ.get("PORT", 8443)),
    url_path=TOKEN,
    webhook_url=f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
)

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    asyncio.run(application.process_update(update))
    return "OK", 200