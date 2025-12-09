from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")

CANAL_PRINCIPAL = "https://t.me/+3RSkDPs9bS02NDZk"
QUE_DU_CUL = "https://t.me/+3lW8pf60_hBhNDU0"

WEBHOOK_URL = "https://bot-py-7v5s.onrender.com/webhook"

app = Flask(__name__)

application = Application.builder().token(TOKEN).build()

# ---------------------- HANDLERS ------------------------

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Canal principal 🔵", url=CANAL_PRINCIPAL)],
        [InlineKeyboardButton("Que Du Cul 🔞", url=QUE_DU_CUL)]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Bienvenue sur le bot !\n\nChoisis un canal ci-dessous ⬇️",
        reply_markup=reply_markup
    )

application.add_handler(CommandHandler("start", start))

# ---------------------- WEBHOOK INIT ------------------------

@app.before_first_request
def init_webhook():
    asyncio.get_event_loop().create_task(start_bot())

async def start_bot():
    await application.initialize()
    await application.start()

    await application.bot.set_webhook(WEBHOOK_URL)

# ---------------------- FLASK ROUTE ------------------------

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    asyncio.get_event_loop().create_task(application.process_update(update))
    return "OK", 200


# ---------------------- RUN ------------------------

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))