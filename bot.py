import os
from flask import Flask, send_file
from pyrogram import Client, filters
import time
import asyncio
import threading

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

BASE_URL = "https://telegram-bot-production-31b5.up.railway.app"

app = Flask(__name__)
FILES = {}

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

    FILES[unique_id] = {
        "file_id": file_id,
        "time": time.time()
    }

    link = f"{BASE_URL}/file/{unique_id}"

    await message.reply_text(f"📥 Download:\n{link}")

# 🌐 Serve file
@app.route("/file/<file_id>")
def get_file(file_id):
    data = FILES.get(file_id)

    if not data:
        return "❌ File expired"

    file_id_real = data["file_id"]
    path = f"{file_id}.bin"

    bot.download_media(file_id_real, file_name=path)

    return send_file(path, as_attachment=True)

# 🔥 Run Flask separately
def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

# 🚀 MAIN FIX
async def main():
    threading.Thread(target=run_flask).start()
    await bot.start()
    print("Bot started")
    await idle()

from pyrogram import idle

if __name__ == "__main__":
    asyncio.run(main())
