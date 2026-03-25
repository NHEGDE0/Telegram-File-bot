import asyncio
from pyrogram import Client, filters, idle

API_ID = int("34945118")
API_HASH = "4f40fc2316771408843047e2003d1aea"
BOT_TOKEN = "8506591391:AAFeZ3JqlyQx_7DJzWLjF161TCVHXM-h9TQ"

app = Client(
    "bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.command("start"))
async def start(client, message):
    await message.reply("Bot is working ✅")

async def main():
    await app.start()
    print("Bot started...")
    await idle()

if name == "main":
    asyncio.run(main())
