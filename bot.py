import os
import asyncio
from flask import Flask, request, send_file
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Flask(__name__)

# Create bot app (FIXED)
application = ApplicationBuilder().token(BOT_TOKEN).build()

# Store files temporarily
FILES = {}

# Handle file
async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    file = update.message.document or update.message.video or update.message.audio

    if not file:
        await update.message.reply_text("Send a file")
        return

    file_id = file.file_id
    file_name = file.file_name or "file"

    FILES[file_id] = file_name

    link = f"https://telegram-bot-production-31b5.up.railway.app/file/{file_id}"

    await update.message.reply_text(f"Download link:\n{link}")

application.add_handler(MessageHandler(filters.ALL, handle_file))

# Download route
@app.route("/file/<file_id>")
async def get_file(file_id):
    file = await application.bot.get_file(file_id)
    path = f"{file_id}.bin"

    await file.download_to_drive(path)

    return send_file(path, as_attachment=True)

# Webhook route
@app.route("/", methods=["POST"])
def webhook():
    data = request.get_json(force=True)
    update = Update.de_json(data, application.bot)

    asyncio.run(application.process_update(update))  # FIXED

    return "OK"

# Start server
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
