from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler
import os

TOKEN = os.getenv("BOT_TOKEN")

CANAL_PRINCIPAL = "https://t.me/+3RSkDPs9bS02NDZk"
NOUVEAU_CANAL = "https://t.me/+3lW8pf60_hBhNDU0"

WEBHOOK_URL = "https://bot-py-7v5s.onrender.com/webhook"

async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Canal principal 🔵", url=CANAL_PRINCIPAL)],
        [InlineKeyboardButton("Que Du Cul 🔞", url=NOUVEAU_CANAL)]
    ]

    markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Bienvenue ! Choisis un canal 👇",
        reply_markup=markup
    )

def main():
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))

    application.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 10000)),
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()