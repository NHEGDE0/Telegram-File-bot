import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters

TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = "https://telegram-bot-production-31b5.up.railway.app/"

# Commands
async def start(update: Update, context):
    await update.message.reply_text("✅ Bot is LIVE 24/7!")

async def echo(update: Update, context):
    await update.message.reply_text(f"You said: {update.message.text}")

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # 🔥 THIS IS THE KEY (no Flask needed)
    app.run_webhook(
        listen="0.0.0.0",
        port=int(os.environ.get("PORT", 8080)),
        webhook_url=WEBHOOK_URL
    )

if __name__ == "__main__":
    main()
