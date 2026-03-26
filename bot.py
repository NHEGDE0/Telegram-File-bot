import os
import threading
from flask import Flask, send_file
from pyrogram import Client, filters
import time

# 🔑 Telegram credentials
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# 🌐 Your Railway URL (FIXED)
BASE_URL = "https://telegram-bot-production-31b5.up.railway.app"

# Flask app
app = Flask(__name__)

# Temporary storage
FILES = {}

# Telegram bot
bot = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# 📥 Receive file
@bot.on_message(filters.document | filters.video | filters.audio)
async def handle_file(client, message):
    file = message.document or message.video or message.audio

    file_id = file.file_id
    unique_id = file.file_unique_id

    # Store file info
    FILES[unique_id] = {
        "file_id": file_id,
        "time": time.time()
    }

    # Generate link
    link = f"{BASE_URL}/file/{unique_id}"

    await message.reply_text(f"📥 Download:\n{link}")

# 🌐 Serve file
@app.route("/file/<file_id>")
def get_file(file_id):
    data = FILES.get(file_id)

    if not data:
        return "❌ File expired or not found"

    file_id_real = data["file_id"]

    path = f"{file_id}.bin"

    try:
        bot.download_media(file_id_real, file_name=path)
        return send_file(path, as_attachment=True)
    except Exception as e:
        return f"Error: {str(e)}"

# 🚀 Run bot
def run_bot():
    bot.run()

# 🌐 Run web server
def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# 🔥 Start both
if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    run_web()
