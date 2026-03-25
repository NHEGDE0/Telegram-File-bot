import os
import threading
import asyncio
from pyrogram import Client, filters
from flask import Flask, Response

# 🔑 ENV
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

# 🤖 Telegram bot
app = Client(
    "stream_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

# 🌐 Flask
web = Flask(__name__)

# 🗂 Memory storage
FILES = {}

# 📩 Receive file
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

    await message.reply_text(f"📥 Direct Download Link:\n{link}")


# 🌐 STREAM FIXED (IMPORTANT)
@web.route("/file/<file_id>")
def stream_file(file_id):
    file_id_real = FILES.get(file_id)

    if not file_id_real:
        return "❌ File not found"

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    async def streamer():
        async for chunk in app.stream_media(file_id_real):
            yield chunk

    def generate():
        gen = streamer()
        try:
            while True:
                chunk = loop.run_until_complete(gen.anext())
                yield chunk
        except StopAsyncIteration:
            pass

    return Response(generate(), content_type="application/octet-stream")


# 🚀 Run both
def run():
    port = int(os.environ.get("PORT", 8080))

    threading.Thread(
        target=lambda: web.run(host="0.0.0.0", port=port)
    ).start()

    app.run()


if __name__ == "__main__":
    run()
