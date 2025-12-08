from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")
CANAL_PRINCIPAL = "https://t.me/+3RSkDPs9bS02NDZk"

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

async def start(update: Update, context):
    keyboard = [[InlineKeyboardButton("Canal principal 🔵", url=CANAL_PRINCIPAL)]]
    await update.message.reply_text(
        "Bienvenue sur le bot !\n\nClique ci-dessous pour rejoindre le canal officiel ⬇️",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

application.add_handler(CommandHandler("start", start))

@app.post("/")
def webhook():
    data = request.get_json()
    update = Update.de_json(data, application.bot)
    asyncio.run(application.process_update(update))
    return "OK", 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))

    render_url = os.getenv("RENDER_EXTERNAL_URL")
    webhook_url = f"{render_url}/"

    asyncio.get_event_loop().run_until_complete(
        application.bot.set_webhook(webhook_url)
    )

    print("Webhook installé sur :", webhook_url)
    app.run(host="0.0.0.0", port=port)