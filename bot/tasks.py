import time
import datetime
import sqlite3
from uuid import uuid4
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram import Update
from telegram.ext import CallbackContext, ContextTypes
from bot.logger import log_info, log_error
import threading
import asyncio
import os

# Specify the file path
db_file_path = r'C:\Users\michaelO\Desktop\GitHub Projects\JimTaskBuddy\data\tasks.db'


# Check if the database file exists, if not, create it
if not os.path.exists(db_file_path):
    open(db_file_path, 'w').close()

# Connect to the database
conn = sqlite3.connect(db_file_path)
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
        complete_date TIMESTAMP,
        reminder_time TIMESTAMP,
        reminder_status INTEGER DEFAULT 0
    )
''')

conn.commit()


def get_user_tasks(user_id):
    cursor.execute(
        'SELECT id, user_id, text, description, status, create_date, complete_date, reminder_time, reminder_status '
        'FROM tasks WHERE user_id = ?',
        (user_id,))
    task_rows = cursor.fetchall()
    return task_rows


def get_task_by_id(task_id):
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
    task_data = cursor.fetchone()

    if task_data:
        task_details = {
            'id': task_data[0],
            'user_id': task_data[1],
            'text': task_data[2],
            'description': task_data[3],
            'status': task_data[4],
            'create_date': task_data[5],
            'complete_date': task_data[6],
            'reminder_time': task_data[7],
            'reminder_status': task_data[8]
        }
        return task_details
    else:
        return None


# Define the asynchronous function to check reminders
async def check_reminders_async(context: CallbackContext):
    while True:
        try:
            current_datetime = datetime.datetime.now().isoformat()

            # Specify the file path
            db_path = r'C:\Users\michaelO\Desktop\GitHub Projects\JimTaskBuddy\data\tasks.db'

            # Check if the database file exists, if not, create it
            if not os.path.exists(db_path):
                open(db_path, 'w').close()

            # Connect to the database
            db_conn = sqlite3.connect(db_path)
            cursor2 = db_conn.cursor()

            cursor2.execute('SELECT id, user_id, text FROM tasks WHERE reminder_time <= ? AND reminder_status = ?',
                            (current_datetime, True))
            rows = cursor2.fetchall()

            if rows:
                for row in rows:
                    task_id = row[0]
                    user_id = row[1]
                    task_text = row[2]

                    # Send notification to the user
                    # You might need to obtain the bot instance here
                    await context.bot.send_message(chat_id=user_id, text=f"Reminder for task: {task_text} is due.")
                    print(f"Reminder for task: **{task_text.upper()}** is sent to user: {user_id}")

                    # Mark reminder as elapsed
                    cursor2.execute('UPDATE tasks SET reminder_status = ? WHERE id = ?', (False, task_id))
                    db_conn.commit()

            db_conn.close()
            time.sleep(30)  # Check for reminders every 30 seconds
            # print("STILL CHECKING REMINDERS...")

        except Exception as e:
            log_error(e)


# Synchronous wrapper function for starting the asynchronous function
def check_reminders_sync(context: CallbackContext):
    """
        Asynchronously checks for reminders in the tasks database and sends notifications to users if a reminder is due.
        @:param:
            context (CallbackContext): The context object that contains information about the current state of the program.
        Returns:
            None
    """

    asyncio.run(check_reminders_async(context))


# def dummy():
#     from datetime import datetime
#
#     tasks_data = [
#   {
#     "id": "80a98138-f423-4270-9e2d-3b7c60bf2117",
#     "user_id": 1513847681,
#     "text": "Buy Glory",
#     "description": "Buy fruits, vegetables, and milk",
#     "status": 1,
#     "create_date": "2023-07-20 02:14:54",
#     "complete_date": "2023-07-20 01:29:16",
#     "reminder_time": null,
#     "reminder_status": 0
#   },
#   {
#     "id": "e501f0ad-5be4-4520-867f-a85f8681aca9",
#     "user_id": 1513847681,
#     "text": "Clean the house",
#     "description": "Vacuum the floors and dust the furniture",
#     "status": 0,
#     "create_date": "2023-07-20 02:14:54",
#     "complete_date": null,
#     "reminder_time": null,
#     "reminder_status": 0
#   },
#   {
#     "id": "07d56d1a-21b2-43f2-9091-9f20dd1430b2",
#     "user_id": 1513847681,
#     "text": "Finish homework",
#     "description": "Complete math and science assignments",
#     "status": 0,
#     "create_date": "2023-07-20 02:14:54",
#     "complete_date": null,
#     "reminder_time": null,
#     "reminder_status": 0
#   },
#   {
#     "id": "12bb191b-62b7-45b7-873d-7b57967a5a9d",
#     "user_id": 1513847681,
#     "text": "Call mom",
#     "description": "Check in with mom and catch up on news",
#     "status": 0,
#     "create_date": "2023-07-20 02:14:54",
#     "complete_date": null,
#     "reminder_time": null,
#     "reminder_status": 0
#   },
#   {
#     "id": "ff68d7e6-d45f-4a44-b07c-b6753ae3e13d",
#     "user_id": 1513847681,
#     "text": "Go for a run",
#     "description": "Run 5 kilometers in the park",
#     "status": 0,
#     "create_date": "2023-07-20 02:14:54",
#     "complete_date": null,
#     "reminder_time": null,
#     "reminder_status": 0
#   },
#   {
#     "id": "a0aa0605-723f-47d3-b96c-d2737ca596dc",
#     "user_id": 1513847681,
#     "text": "Read a book",
#     "description": "Start reading \"The Great Gatsby\"",
#     "status": 0,
#     "create_date": "2023-07-20 02:14:54",
#     "complete_date": null,
#     "reminder_time": null,
#     "reminder_status": 0
#   },
#   {
#     "id": "83d4a9d8-bfd5-4dce-b94c-dc1b0d555d65",
#     "user_id": 1513847681,
#     "text": "Write a blog post",
#     "description": "Choose a topic and write a 500-word blog post",
#     "status": 0,
#     "create_date": "2023-07-20 02:14:54",
#     "complete_date": null,
#     "reminder_time": null,
#     "reminder_status": 0
#   },
#   {
#     "id": "e9bab18a-2c6a-42c6-9831-3fea8b65fe23",
#     "user_id": 1513847681,
#     "text": "Attend a meeting",
#     "description": "Join the team meeting at 2 PM",
#     "status": 0,
#     "create_date": "2023-07-20 02:14:54",
#     "complete_date": null,
#     "reminder_time": null,
#     "reminder_status": 0
#   },
#   {
#     "id": "1c8d3a5d-0254-4fb1-ac1e-77aaf88807dc",
#     "user_id": 1513847681,
#     "text": "Plan a trip",
#     "description": "Research destinations and create an itinerary",
#     "status": 0,
#     "create_date": "2023-07-20 02:14:54",
#     "complete_date": null,
#     "reminder_time": null,
#     "reminder_status": 0
#   },
#   {
#     "id": "d59d1b85-a662-408c-8fb5-0e9e5a34f7d7",
#     "user_id": 1513847681,
#     "text": "Fix the leaky faucet",
#     "description": "Repair the kitchen faucet",
#     "status": 0,
#     "create_date": "2023-07-20 02:14:54",
#     "complete_date": null,
#     "reminder_time": null,
#     "reminder_status": 0
#   }
# ]
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
#         # Set default values for the new columns
#         reminder_time = None
#         reminder_status = 0
#
#         cursor.execute(
#             "INSERT INTO tasks (id, user_id, text, description, status, create_date, reminder_time, reminder_status) "
#             "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
#             (task_id, user_id, task_text, task_description, status, create_date, reminder_time, reminder_status))
#         conn.commit()
#
#         # Print the task details
#         print(f"Task_id: {task_id}\nTask_text: {task_text}\nTask_description: {task_description}")
#
#     print("Dummy tasks added successfully!")


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

        # Insert the task into the database with a status of 0 (incomplete) and default values for reminder_time and reminder_status
        cursor.execute(
            "INSERT INTO tasks (id, user_id, text, description, status, create_date, reminder_time, reminder_status) "
            "VALUES (?, ?, ?, ?, 0, CURRENT_TIMESTAMP, NULL, 0)",
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

        task_rows = get_user_tasks(user_id)

        if task_rows:
            keyboard = []
            for task in task_rows:
                task_id = task[0]
                task_text = task[2]

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

        task_rows = get_user_tasks(user_id)

        if task_rows:
            keyboard = []
            for task in task_rows:
                task_id = task[0]
                task_text = task[2]

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

        task_rows = get_user_tasks(user_id)

        if task_rows:
            keyboard = []
            for task in task_rows:
                task_id = task[0]
                task_text = task[2]
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


async def edit_task_command(update: Update, context: CallbackContext):
    try:
        user_id = update.effective_user.id

        # Fetch the tasks for the user
        task_rows = get_user_tasks(user_id)

        if task_rows:
            keyboard = []
            for task in task_rows:
                task_id = task[0]
                task_text = task[2]
                task_description = task[3]

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


async def show_completed_tasks_command(update: Update, context: CallbackContext):
    try:
        user_id = update.effective_user.id

        task_rows = get_user_tasks(user_id)

        if task_rows:
            completed_tasks = []

            for task in task_rows:
                task_text = task[2]
                task_status = task[4]

                if task_status == 1:  # Completed task
                    completed_tasks.append(f"{task_text} - completed")

            if len(completed_tasks) == 0:
                await context.bot.send_message(chat_id=update.effective_chat.id, text='No completed tasks found!')
                log_info("No completed tasks found.")
                return

            completed_keyboard = []

            for completed_task in completed_tasks:
                button = InlineKeyboardButton(completed_task, callback_data="dummy_value")
                completed_keyboard.append([button])

            completed_reply_markup = InlineKeyboardMarkup(completed_keyboard)

            await context.bot.send_message(chat_id=update.effective_chat.id, text='Your completed tasks are:',
                                           reply_markup=completed_reply_markup)

            log_info("Completed tasks displayed.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='No completed tasks found!')
            log_info("No completed tasks found.")

    except Exception as e:
        log_error("An error occurred while showing completed tasks: {}".format(str(e)))
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='An error occurred while showing completed tasks. Please try again.')


async def show_incomplete_tasks_command(update: Update, context: CallbackContext):
    try:
        user_id = update.effective_user.id

        task_rows = get_user_tasks(user_id)

        if task_rows:
            incomplete_tasks = []

            for task in task_rows:
                task_text = task[2]
                task_status = task[4]

                if task_status == 0:  # Incomplete task
                    incomplete_tasks.append(f"{task_text} - incomplete")

            incomplete_keyboard = []
            for incomplete_task in incomplete_tasks:
                button = InlineKeyboardButton(incomplete_task, callback_data="dummy_value")
                incomplete_keyboard.append([button])

            incomplete_reply_markup = InlineKeyboardMarkup(incomplete_keyboard)

            await context.bot.send_message(chat_id=update.effective_chat.id, text='Your incomplete tasks are:',
                                           reply_markup=incomplete_reply_markup)

            log_info("Incomplete tasks displayed.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='No incomplete tasks found!')
            log_info("No incomplete tasks found.")

    except Exception as e:
        log_error("An error occurred while showing incomplete tasks: {}".format(str(e)))
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='An error occurred while showing incomplete tasks. Please try again.')


async def show_tasks_detail_command(update: Update, context: CallbackContext):
    try:
        user_id = update.effective_user.id

        task_rows = get_user_tasks(user_id)

        if task_rows:
            keyboard = []
            for task in task_rows:
                task_id = task[0]
                task_text = task[2]
                task_status = "completed" if task[4] == 1 else "incomplete"
                button_text = f"{task_text} - {task_status}"
                keyboard.append([InlineKeyboardButton(button_text, callback_data=f"task_{task_id}")])

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


async def set_reminder_command(update: Update, context: CallbackContext):
    try:
        user_id = update.effective_user.id
        task_rows = get_user_tasks(user_id)

        if task_rows:
            keyboard = []
            for task in task_rows:
                task_id = task[0]
                task_text = task[2]
                reminder_status = "Reminder set" if task[8] == 1 else "No reminder set"
                button_text = f"{task_text} - {reminder_status}"
                keyboard.append([InlineKeyboardButton(button_text, callback_data=f"reminder_task_{task_id}")])

            reply_markup = InlineKeyboardMarkup(keyboard)

            await context.bot.send_message(chat_id=update.effective_chat.id, text='Click on a task to set a reminder:',
                                           reply_markup=reply_markup)
            log_info("Tasks displayed waiting for reminder.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='No tasks found!')
            log_info("No tasks found.")

    except Exception as e:
        log_error("An error occurred while showing tasks: {}".format(str(e)))
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='An error occurred while showing tasks. Please try again.')
