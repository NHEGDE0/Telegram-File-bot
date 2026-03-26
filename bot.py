import os
import time
from flask import Flask, send_file, request
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Flask(__name__)
FILES = {}

# 🌐 Your Railway URL
BASE_URL = "https://telegram-bot-production-31b5.up.railway.app"

# 🚀 Telegram app
application = ApplicationBuilder().token(BOT_TOKEN).build()

# ✅ START COMMAND
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ Bot is working! Send me a file.")

# 📥 HANDLE FILE
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document or update.message.video or update.message.audio

    if not file:
        return

    file_id = file.file_id
    unique_id = str(time.time())

    FILES[unique_id] = file_id

    link = f"{BASE_URL}/file/{unique_id}"

    await update.message.reply_text(f"📥 Download:\n{link}")

# 🌐 DOWNLOAD ROUTE
@app.route("/file/<file_id>")
def download(file_id):
    if file_id not in FILES:
        return "❌ File not found"

    file_id_real = FILES[file_id]

    file = application.bot.get_file(file_id_real)
    path = f"{file_id}.bin"
    file.download_to_drive(path)

    return send_file(path, as_attachment=True)

# 🌐 WEBHOOK ROUTE
@app.route("/", methods=["POST"])
async def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)
    await application.process_update(update)
    return "OK"

# 🚀 SET WEBHOOK
@app.route("/setwebhook")
def set_webhook():
    url = f"{BASE_URL}/"
    application.bot.set_webhook(url)
    return "Webhook set"

# 🚀 RUN APP
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
