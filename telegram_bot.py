import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from core.models import TelegramUser, User
from django.conf import settings

TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    username = update.effective_user.username
    
    # Save to database
    TelegramUser.objects.update_or_create(
        chat_id=str(chat_id),
        defaults={'telegram_username': username}
    )
    
    await context.bot.send_message(
        chat_id=chat_id,
        text=f"Hello {username}! Your details have been saved."
    )

def run_bot():
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.run_polling()