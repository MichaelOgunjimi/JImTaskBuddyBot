import sqlite3
from uuid import uuid4
import re
from bot.logger import log_info, log_error
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext

# from datetime import datetime

conn = sqlite3.connect('C:/Users/michaelO/Desktop/Projects/JimTaskBuddy/data/tasks_manager.db')
cursor = conn.cursor()

# Create the tasks table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id TEXT PRIMARY KEY,
        user_id INTEGER,
        text TEXT,
        description TEXT,
        status INTEGER,
        create_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        complete_date TIMESTAMP
    )
''')

conn.commit()


# def dummy():
#     from datetime import datetime
#
#     tasks_data = [
#         {
#             'text': 'Buy groceries',
#             'description': 'Buy fruits, vegetables, and milk'
#         },
#         {
#             'text': 'Clean the house',
#             'description': 'Vacuum the floors and dust the furniture'
#         },
#         {
#             'text': 'Finish homework',
#             'description': 'Complete math and science assignments'
#         },
#         {
#             'text': 'Call mom',
#             'description': 'Check in with mom and catch up on news'
#         },
#         {
#             'text': 'Go for a run',
#             'description': 'Run 5 kilometers in the park'
#         },
#         {
#             'text': 'Read a book',
#             'description': 'Start reading "The Great Gatsby"'
#         },
#         {
#             'text': 'Write a blog post',
#             'description': 'Choose a topic and write a 500-word blog post'
#         },
#         {
#             'text': 'Attend a meeting',
#             'description': 'Join the team meeting at 2 PM'
#         },
#         {
#             'text': 'Plan a trip',
#             'description': 'Research destinations and create an itinerary'
#         },
#         {
#             'text': 'Fix the leaky faucet',
#             'description': 'Repair the kitchen faucet'
#         }
#     ]
#
#     # Generate a unique user ID
#     user_id = 1513847681
#
#     for task_data in tasks_data:
#         task_id = str(uuid4())
#         task_text = task_data['text']
#         task_description = task_data['description']
#         status = 0  # Set the status to 0 (incomplete)
#         create_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Get current date and time
#
#         # Ensure the generated task ID is unique
#         while task_id in cursor:
#             task_id = str(uuid4())
#
#         cursor.execute(
#             "INSERT INTO tasks (id, user_id, text, description, status, create_date) VALUES (?, ?, ?, ?, ?, ?)",
#             (task_id, user_id, task_text, task_description, status, create_date))
#         conn.commit()
#
#         # Print the task details
#         print(f"Task_id: {task_id}\nTask_text: {task_text}\nTask_description: {task_description}")
#
#     print("Dummy tasks added successfully!")
#

async def add_task_command(update, context):
    try:
        user_id = update.effective_user.id

        # Extract the task text and description from the user's message
        task_args = context.args
        if len(task_args) == 0:
            await context.bot.send_message(chat_id=update.effective_chat.id,
                                           text='Please provide a task text. Example: /addtask Buy groceries')
            return

        task_text = ' '.join(task_args)
        task_description = None

        # Check if a description is provided in the message
        description_keywords = ['description:', 'description=', 'description']
        for keyword in description_keywords:
            if keyword in task_args:
                keyword_index = task_args.index(keyword)
                if keyword_index < len(task_args) - 1:
                    task_text = ' '.join(task_args[:keyword_index]).strip()
                    task_description = ' '.join(task_args[keyword_index + 1:]).strip()
                break

        # Generate a unique task ID
        task_id = str(uuid4())
        while task_id in cursor:
            task_id = str(uuid4())

        print(f"Task_id: {task_id}\nTask_text: {task_text}\nTask_description: {task_description}")

        # Insert the task into the database with a status of 0 (incomplete)
        cursor.execute(
            "INSERT INTO tasks (id, user_id, text, description, status, create_date) VALUES (?, ?, ?, ?, 0, CURRENT_TIMESTAMP)",
            (task_id, user_id, task_text, task_description))

        conn.commit()

        await context.bot.send_message(chat_id=update.effective_chat.id, text='Task added successfully!')

        # Logging an informational message
        log_info("Task added successfully.")

    except Exception as e:
        # Logging an error message
        log_error("An error occurred while adding a task: {}".format(str(e)))

        # Sending an error message to the user
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='An error occurred while adding a task. Please try again.')


async def complete_task_command(update: Update, context: CallbackContext):
    try:
        user_id = update.effective_user.id

        cursor.execute('SELECT id, text FROM tasks WHERE user_id = ? AND status = 0', (user_id,))
        task_rows = cursor.fetchall()

        if task_rows:
            keyboard = []
            for task in task_rows:
                task_id = task[0]
                task_text = task[1]

                button_text = f'{task_text}'
                keyboard.append([InlineKeyboardButton(button_text, callback_data=f"complete_task_{task_id}")])

            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(chat_id=update.effective_chat.id, text='Select a task to complete:',
                                           reply_markup=reply_markup)
            log_info("Tasks displayed.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='No incomplete tasks found!')
            log_info("No incomplete tasks found.")

    except Exception as e:
        log_error("An error occurred while showing tasks: {}".format(str(e)))
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='An error occurred while showing tasks. Please try again.')


async def delete_task_command(update: Update, context: CallbackContext):
    try:
        user_id = update.effective_user.id

        cursor.execute('SELECT id, text, status FROM tasks WHERE user_id = ?', (user_id,))
        task_rows = cursor.fetchall()

        if task_rows:
            keyboard = []
            for task in task_rows:
                task_id = task[0]
                task_text = task[1]

                button_text = f'{task_text}'
                keyboard.append([InlineKeyboardButton(button_text, callback_data=f"delete_task_{task_id}")])

            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(chat_id=update.effective_chat.id, text='Select a task to delete:',
                                           reply_markup=reply_markup)
            log_info("Tasks displayed.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='No tasks found!')
            log_info("No tasks found.")

    except Exception as e:
        log_error("An error occurred while showing tasks: {}".format(str(e)))
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='An error occurred while showing tasks. Please try again.')


async def show_tasks_command(update: Update, context):
    try:
        user_id = update.effective_user.id

        cursor.execute('SELECT id, text, status FROM tasks WHERE user_id = ?', (user_id,))
        task_rows = cursor.fetchall()

        if task_rows:
            keyboard = []
            for task in task_rows:
                task_id = task[0]
                task_text = task[1]
                task_status = "completed" if task[2] == 1 else "incomplete"
                button_text = f"{task_text} - {task_status}"
                button = InlineKeyboardButton(button_text, callback_data="dummy_value")
                keyboard.append([button])

            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(chat_id=update.effective_chat.id, text='Your tasks are:',
                                           reply_markup=reply_markup)
            log_info("Tasks displayed.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='No tasks found!')
            log_info("No tasks found.")

    except Exception as e:
        log_error("An error occurred while showing tasks: {}".format(str(e)))
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='An error occurred while showing tasks. Please try again.')


# async def edit_task(update: Update, context: CallbackContext):
#     try:
#         user_id = update.effective_user.id
#
#         cursor.execute('SELECT id, text, description FROM tasks WHERE user_id = ?', (user_id,))
#         task_rows = cursor.fetchall()
#
#         if task_rows:
#             keyboard = []
#             for task in task_rows:
#                 task_id = task[0]
#                 task_text = task[1]
#                 task_description = task[2]
#
#                 button_text = f'{task_text} - {task_description}'
#                 button = InlineKeyboardButton(button_text, callback_data=f"edit_task_{task_id}")
#                 keyboard.append([button])
#
#             reply_markup = InlineKeyboardMarkup(keyboard)
#
#             await context.bot.send_message(chat_id=update.effective_chat.id, text='Select a task to edit:',
#                                            reply_markup=reply_markup)
#             log_info("Tasks displayed.")
#         else:
#             await context.bot.send_message(chat_id=update.effective_chat.id, text='No tasks found!')
#             log_info("No tasks found.")
#
#     except Exception as e:
#         log_error("An error occurred while showing tasks: {}".format(str(e)))
#         await context.bot.send_message(chat_id=update.effective_chat.id,
#                                        text='An error occurred while showing tasks. Please try again.')


# Handler for /edittask command
async def edit_task_command(update: Update, context: CallbackContext):
    try:
        user_id = update.effective_user.id

        # Fetch the tasks for the user
        cursor.execute('SELECT id, text, description FROM tasks WHERE user_id = ?', (user_id,))
        task_rows = cursor.fetchall()

        if task_rows:
            keyboard = []
            for task in task_rows:
                task_id = task[0]
                task_text = task[1]
                task_description = task[2]

                button_text = f'{task_text} - {task_description}'
                button = InlineKeyboardButton(button_text, callback_data=f"edit_task_{task_id}")
                keyboard.append([button])

            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(chat_id=update.effective_chat.id, text='Select a task to edit:',
                                           reply_markup=reply_markup)
            log_info("Tasks displayed.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='No tasks found!')
            log_info("No tasks found.")

    except Exception as e:
        log_error("An error occurred while showing tasks: {}".format(str(e)))
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='An error occurred while showing tasks. Please try again.')

