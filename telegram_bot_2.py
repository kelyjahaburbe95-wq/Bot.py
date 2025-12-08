from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler
import asyncio
import os

# ---- FLASK ----
app = Flask(__name__)

# ---- TOKEN ----
TOKEN = os.getenv("BOT_TOKEN")
CANAL_PRINCIPAL = "https://t.me/+3RSkDPs9bS02NDZk"

# ---- APPLICATION TG ----
application = Application.builder().token(TOKEN).build()

# ---- GLOBAL EVENT LOOP ----
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)


# ---- START COMMAND ----
async def start(update: Update, context):
    keyboard = [[InlineKeyboardButton("Canal principal 🔵", url=CANAL_PRINCIPAL)]]
    await update.message.reply_text(
        "Bienvenue sur le bot !\n\nClique ici pour rejoindre le canal 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )


application.add_handler(CommandHandler("start", start))


# ---- WEBHOOK ROUTE ----
@app.post("/webhook")
def webhook():
    data = request.get_json()

    if data:
        update = Update.de_json(data, application.bot)

        if not application._initialized:
            loop.run_until_complete(application.initialize())

        loop.create_task(application.process_update(update))

    return "OK", 200


@app.get("/")
def home():
    return "Bot Telegram en ligne ✔️"


# ---- RUN FLASK SERVER ----
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)