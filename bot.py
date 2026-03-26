import os
import threading
from flask import Flask, send_file
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

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

    # store file id
    FILES[unique_id] = file_id

    # create link
    base_url = os.environ.get("RAILWAY_STATIC_URL")
    link = f"{base_url}/file/{unique_id}"

    await message.reply_text(f"📥 Download:\n{link}")


# 🌐 Serve file
@app.route("/file/<file_id>")
def get_file(file_id):
    file_id_real = FILES.get(file_id)

    if not file_id_real:
        return "File not found"

    path = f"{file_id}.bin"

    bot.download_media(file_id_real, file_name=path)

    return send_file(path, as_attachment=True)


# 🚀 Run both
def run_bot():
    bot.run()

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    run_web()
