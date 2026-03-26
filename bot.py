import os
import asyncio
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

# 🔐 Get token from Railway variable
TOKEN = os.environ.get("BOT_TOKEN")

# 🚀 Flask app
app = Flask(__name__)

# 🤖 Telegram Application
application = Application.builder().token(TOKEN).build()

# ✅ Initialize application
asyncio.run(application.initialize())


# =========================
# 🤖 BOT COMMANDS
# =========================

async def start(update: Update, context):
    await update.message.reply_text("✅ Bot is working!")

async def echo(update: Update, context):
    text = update.message.text
    await update.message.reply_text(f"You said: {text}")


# =========================
# 📌 ADD HANDLERS
# =========================

application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))


# =========================
# 🌐 WEBHOOK ROUTE
# =========================

@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    update = Update.de_json(data, application.bot)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(application.process_update(update))
    loop.close()

    return "OK"


# =========================
# 🚀 RUN SERVER
# =========================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
