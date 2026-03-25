import os
from pyrogram import Client, filters

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client(
    "file_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("✅ Bot is working!")

@app.on_message(filters.document | filters.video | filters.audio)
async def file_handler(client, message):
    file_id = message.document.file_id if message.document else message.video.file_id if message.video else message.audio.file_id
    
    link = f"https://t.me/{(await client.get_me()).username}?start={file_id}"
    
    await message.reply_text(f"🔗 Download Link:\n{link}")

app.run()
