import os
import sqlite3
from dotenv import load_dotenv
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from telegram import ReplyKeyboardMarkup, KeyboardButton

load_dotenv()
TOKEN = os.getenv("TELEGRAM_TOKEN")
app = Application.builder().token(TOKEN).build()

conn = sqlite3.connect('tasks.db')
cursor = conn.cursor()


#---db funks---
def add_task_to_db(user_id, task_text):
    cursor.execute('INSERT INTO tasks (user_id, task_text) VALUES (?, ?)', (user_id, task_text))
    conn.commit()


def get_tasks_from_db(user_id):
    cursor.execute('SELECT task_text FROM tasks WHERE user_id = ?', (user_id,))
    return [row[0] for row in cursor.fetchall()]


#---tg funks---
async def start(update, context):
    user_name = update.message.from_user.first_name
    await update.message.reply_text(f'Hi, {user_name}, im a simple Telegram bot for managing to-do tasks.')

    keyboard = [
        [KeyboardButton("Add Task"), KeyboardButton("Show Tasks")]
    ]
    buttons = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text("Choose an action:", reply_markup=buttons)


async def add_task(update, context, text):
    task = text.strip()
    if task:
        user_id = update.message.from_user.id
        add_task_to_db(user_id, task)
        await update.message.reply_text(f'Task added: {task}')
    else:
        await update.message.reply_text('Empty task not added.')


async def show_tasks(update, context):
    user_id = update.message.from_user.id
    tasks = get_tasks_from_db(user_id)

    if tasks:
        tasks_list = "\n".join([f"{i + 1}. {task}" for i, task in enumerate(tasks)])
        await update.message.reply_text(f"📝 Your tasks ({len(tasks)} total):\n{tasks_list}")
    else:
        await update.message.reply_text("📝 You don't have any tasks yet.")


async def message_handler(update, context):
    text = update.message.text

    if text == "Add Task":
        context.user_data['adding_task'] = True
        await update.message.reply_text("Please type the task you want to add:")
    elif text == "Show Tasks":
        await show_tasks(update, context)
    elif context.user_data.get('adding_task'):
        context.user_data['adding_task'] = False
        await add_task(update, context, text)
    else:
        await update.message.reply_text('Please choose an action from menu.')


#---handlers reg---
app.add_handler(CommandHandler('start', start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))


#---bot run---
app.run_polling()
