from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler
import asyncio
import os

# ==============================
# 🔐 Token Telegram
# ==============================
TOKEN = os.getenv("BOT_TOKEN", "8544709960:AAH6128cdjtCw0-BI3vHvdFapMgGH5WKaIw")
CANAL_PRINCIPAL = "https://t.me/+3RSkDPs9bS02NDZk"

app = Flask(__name__)

# ==============================
# 🤖 Application Telegram
# ==============================
application = Application.builder().token(TOKEN).build()

# ==============================
# 📌 Commande /start
# ==============================
async def start(update: Update, context):
    keyboard = [
        [InlineKeyboardButton("Canal principal 🔵", url=CANAL_PRINCIPAL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Bienvenue sur le bot !\n\nClique ci-dessous pour rejoindre le canal officiel ⬇️",
        reply_markup=reply_markup
    )

application.add_handler(CommandHandler("start", start))

# ==============================
# 🌐 Webhook Endpoint
# ==============================
@app.post(f"/webhook/{TOKEN}")
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    asyncio.run(application.process_update(update))
    return "OK", 200

# ==============================
# 🚀 Lancement Render
# ==============================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    base_url = os.getenv("RENDER_EXTERNAL_URL")

    if not base_url:
        raise RuntimeError("RENDER_EXTERNAL_URL n'est pas défini dans Render !")

    # Définition du webhook
    webhook_url = f"{base_url}/webhook/{TOKEN}"

    asyncio.get_event_loop().run_until_complete(
        application.bot.set_webhook(webhook_url)
    )

    print("Webhook installé sur :", webhook_url)

    app.run(host="0.0.0.0", port=port)