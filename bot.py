import os
from email.policy import default

from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import ReplyKeyboardMarkup, KeyboardButton

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
app = Application.builder().token(TOKEN).build()



async def start(update, context):
    user_name = update.message.from_user.first_name
    await update.message.reply_text(f'Hi, {user_name}, im a simple Telegram bot for managing to-do tasks')

    keyboard = [
        [KeyboardButton("Add Task"), KeyboardButton("Show Tasks")]
    ]
    buttons = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Choose an action:", reply_markup=buttons)

async def reply_button_handler(update, context):
    text = update.message.text

    if text == "Add Task":
        context.user_data['adding_task'] = True
        await update.message.reply_text("Please type the task you want to add:")
    elif text == "Show Tasks":
        await update.message.reply_text("Here are your tasks (not implemented yet)")


app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_button_handler))



app.run_polling()
