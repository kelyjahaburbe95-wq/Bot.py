###############################################
# telegram_bot_2.py — Version Render Complète #
###############################################

import os
import asyncio
from flask import Flask, request
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler


# ============================================
# 🔐 TOKEN (Render le fournit automatiquement)
# ============================================
TOKEN = os.getenv("BOT_TOKEN")   # <-- NE RIEN CHANGER ICI

if not TOKEN:
    raise RuntimeError("❌ BOT_TOKEN n'est pas défini dans Render.")


# ============================================
# 🚀 FLASK APP
# ============================================
app = Flask(__name__)


# ============================================
# 🤖 CONFIGURATION DU BOT TELEGRAM
# ============================================
application = Application.builder().token(TOKEN).build()


# ============================================
# 📌 COMMANDE /start
# ============================================
async def start(update: Update, context):
    bouton = [[InlineKeyboardButton("Canal principal 🔵",
                                    url="https://t.me/+3RSkDPs9bS02NDZk")]]

    await update.message.reply_text(
        "Bienvenue sur le bot !\n\nClique ci-dessous pour rejoindre le canal officiel ⬇️",
        reply_markup=InlineKeyboardMarkup(bouton)
    )

application.add_handler(CommandHandler("start", start))


# ============================================
# 🌐 WEBHOOK (Render envoie ICI les messages)
# ============================================
@app.post("/webhook")
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    asyncio.run(application.process_update(update))
    return "OK", 200


# ============================================
# 🚀 MODE LOCAL (pour tests)
# ============================================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    print(f"Bot lancé en local sur le port {port}")
    app.run(host="0.0.0.0", port=port)