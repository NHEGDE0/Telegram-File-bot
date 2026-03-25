import os
from pyrogram import Client, filters
from flask import Flask, Response

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

BOT_USERNAME = None

app = Client(
    "stream_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

web = Flask(name)

FILES = {}

# 📩 Receive file
@app.on_message(filters.document | filters.video | filters.audio)
async def handle_file(client, message):
    global BOT_USERNAME
    
    if not BOT_USERNAME:
        me = await client.get_me()
        BOT_USERNAME = me.username

    file_id = (
        message.document.file_id if message.document else
        message.video.file_id if message.video else
        message.audio.file_id
    )

    unique_id = str(message.id)
    FILES[unique_id] = file_id

    link = f"https://{os.environ.get('RAILWAY_STATIC_URL')}/file/{unique_id}"

    await message.reply_text(f"🔗 Download:\n{link}")


# 🌐 Stream file to browser
@web.route("/file/<file_id>")
def stream_file(file_id):
    file_id_real = FILES.get(file_id)

    if not file_id_real:
        return "File not found"

    def generate():
        for chunk in app.stream_media(file_id_real):
            yield chunk

    return Response(generate(), content_type="application/octet-stream")


# 🚀 Run both
def run():
    import threading
    port = int(os.environ.get("PORT", 8080))
    
    threading.Thread(target=lambda: web.run(host="0.0.0.0", port=port)).start()
    app.run()

if name == "main":
    run()
