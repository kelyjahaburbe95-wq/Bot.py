from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler
import asyncio
import os

TOKEN = os.getenv("BOT_TOKEN")
CANAL_PRINCIPAL = "https://t.me/+3RSkDPs9bS02NDZk"

app = Flask(__name__)
application = Application.builder().token(TOKEN).build()

# ===== HANDLERS =====

async def start(update: Update, context):
    keyboard = [[InlineKeyboardButton("Canal principal 🔵", url=CANAL_PRINCIPAL)]]
    await update.message.reply_text(
        "Bienvenue sur le bot !\n\nClique ci-dessous pour rejoindre le canal officiel ⬇️",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

application.add_handler(CommandHandler("start", start))

# ===== WEBHOOK ROUTE =====

@app.post("/webhook")
def webhook():
    update = Update.de_json(request.json, application.bot)
    asyncio.get_event_loop().create_task(application.process_update(update))
    return "OK", 200

# ===== START APPLICATION =====
if __name__ == "__main__":
    # Render utilise PORT dans les variables système
    port = int(os.getenv("PORT", 10000))

    print(f"Bot started on port {port}")
    app.run(host="0.0.0.0", port=port)