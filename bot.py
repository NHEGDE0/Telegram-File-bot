import threading
from pyrogram import Client, filters
from flask import Flask, Response

API_ID = 34945118
API_HASH = "4f40fc2316771408843047e2003d1aea"
BOT_TOKEN = "8506591391:AAFeZ3JqlyQx_7DJzWLjF161TCVHXM-h9TQ"

app = Client("stream_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)
web = Flask(__name__)

FILES = {}

# RECEIVE FILE
@app.on_message(filters.document | filters.video)
async def handle_file(client, message):
    file_id = message.document.file_id if message.document else message.video.file_id

    unique_id = str(message.id)
    FILES[unique_id] = file_id

    link = f"http://192.168.29.29:5000/file/{unique_id}"
    await message.reply(f"🔗 Link:\n{link}")

# STREAM FILE (NO DOWNLOAD)
@web.route("/file/<file_id>")
def stream_file(file_id):

    file_id_real = FILES.get(file_id)

    if not file_id_real:
        return "Invalid file"

    def generate():
        for chunk in app.stream_media(file_id_real):
            yield chunk

    return Response(generate(), content_type="application/octet-stream")


# RUN FLASK
def run_flask():
    web.run(host="0.0.0.0", port=5000)


# RUN BOTH
if __name__ == "__main__":
    threading.Thread(target=run_flask).start()
    app.run()