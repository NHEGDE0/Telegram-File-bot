import os
import time
import asyncio
from flask import Flask, send_file, request
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters

BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)
FILES = {}

BASE_URL = "https://telegram-bot-production-31b5.up.railway.app"

# Create application
application = ApplicationBuilder().token(BOT_TOKEN).build()

# START command
async def start(update, context):
    await update.message.reply_text("✅ Bot is working! Send me a file.")

# File handler
async def handle_file(update, context):
    file = update.message.document or update.message.video or update.message.audio

    if not file:
        return

    file_id = file.file_id
    unique_id = str(int(time.time()))

    FILES[unique_id] = file_id

    link = f"{BASE_URL}/file/{unique_id}"

    await update.message.reply_text(f"📥 Download:\n{link}")

# Add handlers
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.ALL, handle_file))

# Download route
@app.route("/file/<file_id>")
def download(file_id):
    if file_id not in FILES:
        return "❌ File not found"

    file_id_real = FILES[file_id]

    file = application.bot.get_file(file_id_real)
    path = f"{file_id}.bin"
    file.download_to_drive(path)

    return send_file(path, as_attachment=True)

# Webhook route (FIXED)
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json(force=True)

    update = Update.de_json(data, application.bot)

    asyncio.run(application.process_update(update))  # ✅ FIX

    return "OK"

# Set webhook
@app.route("/setwebhook")
def set_webhook():
    url = f"{BASE_URL}/"
    application.bot.set_webhook(url)
    return "Webhook set"

# Run server
if __name__ == "__main__":
    application.initialize()  # ✅ IMPORTANT
    app.run(host="0.0.0.0", port=8080)
