from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler
import asyncio
import os

app = Flask(__name__)

TOKEN = os.getenv("BOT_TOKEN")
CANAL_PRINCIPAL = "https://t.me/+3RSkDPs9bS02NDZk"

application = Application.builder().token(TOKEN).build()

# --- COMMAND /start ---
async def start(update: Update, context):
    keyboard = [[InlineKeyboardButton("Canal principal 🔵", url=CANAL_PRINCIPAL)]]
    await update.message.reply_text(
        "Bienvenue sur le bot !\n\nClique ici pour rejoindre le canal 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

application.add_handler(CommandHandler("start", start))


# --- WEBHOOK ROUTE ---
@app.post("/webhook")
def webhook():
    data = request.get_json()

    if data:
        update = Update.de_json(data, application.bot)

        if not application._initialized:
            asyncio.run(application.initialize())

        asyncio.run(application.process_update(update))

    return "OK", 200


@app.get("/")
def home():
    return "Bot Telegram en ligne ✔️"


# --- RUN FLASK SERVER (OBLIGATOIRE SUR RENDER) ---
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)