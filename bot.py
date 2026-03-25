import os
import asyncio
from pyrogram import Client, filters

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")

app = Client(
    "filelinkbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text("Bot is working ✅\nSend me a file")

@app.on_message(filters.document | filters.video | filters.audio)
async def file_handler(client, message):
    file_id = message.document.file_id if message.document else message.video.file_id if message.video else message.audio.file_id
    
    link = f"https://t.me/{(await client.get_me()).username}?start={file_id}"
    
    await message.reply_text(f"Download link:\n{link}")

async def main():
    await app.start()
    print("Bot started...")
    await idle()

from pyrogram import idle

if name == "main":
    asyncio.run(main())
