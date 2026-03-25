import os
import threading
from pyrogram import Client, filters
from flask import Flask, send_file
import tempfile

# 🔑 ENV
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# 🤖 Bot
app = Client(
    "stream_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# 🌐 Flask
web = Flask(__name__)

FILES = {}

# 📩 Handle file
@app.on_message(filters.document | filters.video | filters.audio)
async def handle_file(client, message):

    file_id = (
        message.document.file_id if message.document else
        message.video.file_id if message.video else
        message.audio.file_id
    )

    unique_id = str(message.id)
    FILES[unique_id] = file_id

    domain = os.environ.get("RAILWAY_PUBLIC_DOMAIN")

    link = f"https://{domain}/file/{unique_id}"

    await message.reply_text(f"📥 Direct Download:\n{link}")


# 🌐 Download + send file
@web.route("/file/<file_id>")
def get_file(file_id):
    file_id_real = FILES.get(file_id)

    if not file_id_real:
        return "❌ File not found"

    # create temp file
    temp = tempfile.NamedTemporaryFile(delete=False)

    # download file
    app.download_media(file_id_real, file_name=temp.name)

    return send_file(temp.name, as_attachment=True)


# 🚀 Run
def run():
    port = int(os.environ.get("PORT", 8080))

    threading.Thread(
        target=lambda: web.run(host="0.0.0.0", port=port)
    ).start()

    app.run()


if __name__ == "__main__":
    run()
