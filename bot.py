import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# 🔐 Token from Railway variable
TOKEN = os.environ.get("BOT_TOKEN")

# 🚀 Flask app
app = Flask(__name__)

# 🤖 Telegram bot application
application = Application.builder().token(TOKEN).build()


# =========================
# ✅ INITIALIZE BOT
# =========================
async def init():
    await application.initialize()

asyncio.run(init())


# =========================
# 🤖 COMMANDS
# =========================
async def start(update: Update, context):
    await update.message.reply_text("✅ Bot is working!")

async def echo(update: Update, context):
    await update.message.reply_text(f"You said: {update.message.text}")


# =========================
# 📌 HANDLERS
# =========================
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


# =========================
# 🌐 WEBHOOK
# =========================
@app.route("/", methods=["POST"])
def webhook():
    try:
        data = request.get_json(force=True)
        update = Update.de_json(data, application.bot)

        asyncio.run(application.process_update(update))

        return "OK"
    except Exception as e:
        print("ERROR:", e)
        return "OK"   # Always return 200 to Telegram


# =========================
# 🚀 RUN SERVER
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
