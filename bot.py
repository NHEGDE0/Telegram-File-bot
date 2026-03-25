import os
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")

app = Client(
    "filelinkbot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(client, message: Message):
    await message.reply_text("Bot is working ✅\nSend me a file")

@app.on_message(filters.document | filters.video | filters.audio)
async def file_handler(client, message: Message):
    file_id = message.document.file_id if message.document else message.video.file_id if message.video else message.audio.file_id
    
    bot_username = (await client.get_me()).username
    link = f"https://t.me/{bot_username}?start={file_id}"
    
    await message.reply_text(f"Download link:\n{link}")

async def main():
    await app.start()
    print("Bot started...")
    await idle()

from pyrogram import idle

if __name__ == "__main__":
    asyncio.run(main())
