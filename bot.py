from dotenv import load_dotenv
import os
from telegram.ext import Application, CommandHandler, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
app = Application.builder().token(TOKEN).build()






async def start_msg(update, context):
    user_name = update.message.from_user.first_name
    await update.message.reply_text(f'Hi, {user_name}, im a simple Telegram bot for managing to-do tasks')
app.add_handler(CommandHandler('start', start_msg))



app.run_polling()
