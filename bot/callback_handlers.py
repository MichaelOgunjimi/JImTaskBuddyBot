from bot.tasks import cursor, conn, log_error, log_info
from telegram import Update
from telegram.ext import ContextTypes, CallbackContext
from config import BOT_USERNAME
from bot.response import get_response
from bot.tasks import get_task_by_id
import re


def extract_text_and_description(input_string):
    # Check if both text and description are present
    if "description:" in input_string:
        # Extract text using regex
        text_match = re.search(r'^(.*?)\sdescription:', input_string)
        if text_match:
            text = text_match.group(1).strip()
        else:
            text = None

        # Extract description using regex
        description_match = re.search(r'description:\s(.*)$', input_string)
        if description_match:
            description = description_match.group(1).strip()
        else:
            description = None

    else:
        # Only text is provided
        text = input_string.strip()
        description = None

    return text, description


async def handle_edit_task_input_or_messages(update: Update, context: CallbackContext):
    try:
        if 'edit_task_id' in context.user_data:
            print("User editing task input in progress")
            # Editing task input is in progress, handle it
            await handle_edit_task_input(update, context)
        else:
            print("User normal input in progress")
            # No editing task input in progress, handle other text messages
            bot_response = await handle_messages(update, context)
            user_id = update.message.chat.id
            log_info(f"User ({user_id}) - Bot Response: {bot_response}")

    except Exception as e:
        log_error(f"An error occurred in handle_edit_task_input_or_messages: {str(e)}")
        await update.message.reply_text('An error occurred. Please try again.')


async def handle_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        message_type = update.message.chat.type
        text = update.message.text
        user_id = update.message.chat.id

        log_info(f"User ({user_id}) in {message_type}: {text}")

        if message_type == 'group':
            if BOT_USERNAME in text:
                new_text = text.replace(BOT_USERNAME, '').strip()
                response = get_response(new_text)
            else:
                return
        else:
            response = get_response(text)

        log_info(f"Bot: {response}")
        await update.message.reply_text(response)

        return response  # Return the bot response for use in handle_edit_task_input_or_messages

    except Exception as e:
        log_error(f"An error occurred while handling messages: {str(e)}")
        await update.message.reply_text('An error occurred while handling messages. Please try again.')


async def handle_complete_query(update: Update, context: CallbackContext):
    user_id = update.effective_user.id
    query = update.callback_query
    try:
        task_id = query.data.replace("complete_task_", "")

        # Update the task status as completed
        cursor.execute('''
            UPDATE tasks SET status = 1, complete_date = CURRENT_TIMESTAMP
            WHERE id = ? AND user_id = ?
        ''', (task_id, user_id))

        conn.commit()

        await context.bot.send_message(chat_id=query.message.chat_id, text='Task marked as completed!')
        log_info("Task marked as completed.")

    except Exception as e:
        log_error("An error occurred while completing the task: {}".format(str(e)))
        await context.bot.send_message(chat_id=query.message.chat_id,
                                       text='An error occurred while completing the task. Please try again.')


async def handle_delete_query(update: Update, context: CallbackContext):
    try:
        task_id = update.callback_query.data.replace("delete_task_", "")
        user_id = update.effective_user.id

        cursor.execute('DELETE FROM tasks WHERE id = ? AND user_id = ?', (task_id, user_id))
        conn.commit()

        if cursor.rowcount > 0:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Task deleted successfully!')
            log_info("Task deleted successfully.")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text='Task not found!')
            log_info("Task not found.")

    except Exception as e:
        log_error("An error occurred while deleting a task: {}".format(str(e)))
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text='An error occurred while deleting a task. Please try again.')


async def handle_edit_task_query(update: Update, context: CallbackContext):
    try:
        query = update.callback_query
        task_id = query.data.replace("edit_task_", "")

        context.user_data['edit_task_id'] = task_id

        await query.message.reply_text(
            "You have selected a task to edit. Please provide the updated task text or description.")
        log_info("Task selected for editing.")

    except Exception as e:
        log_error("An error occurred while handling the edit task query: {}".format(str(e)))


# Message handler for editing task text or description
async def handle_edit_task_input(update: Update, context: CallbackContext):
    try:
        print(context.user_data)
        if 'edit_task_id' in context.user_data:
            input_text = update.message.text
            task_id = context.user_data['edit_task_id']
            user_id = update.effective_user.id
            current_text = context.user_data.get('edit_task_text')
            current_description = context.user_data.get('edit_task_description')

            # Extract task_text and task_description using the extract_text_and_description function
            task_text, task_description = extract_text_and_description(input_text)

            if task_text or task_description:
                # Update the task with the new text and/or description
                if task_text and task_text != current_text:
                    cursor.execute('UPDATE tasks SET text = ? WHERE id = ? AND user_id = ?',
                                   (task_text, task_id, user_id))
                    conn.commit()
                    await update.message.reply_text('Task text updated successfully!')
                    log_info("Task text updated successfully.")

                if task_description and task_description != current_description:
                    cursor.execute('UPDATE tasks SET description = ? WHERE id = ? AND user_id = ?',
                                   (task_description, task_id, user_id))
                    conn.commit()
                    await update.message.reply_text('Task description updated successfully!')
                    log_info("Task description updated successfully.")

                context.user_data.pop('edit_task_id')
                context.user_data.pop('edit_task_text', None)  # Use None as the default value to avoid KeyError
                context.user_data.pop('edit_task_description', None)  # Use None as the default value to avoid KeyError

                return  # Stop further processing after completing the edit

            else:
                await update.message.reply_text(
                    'Invalid command format. Please provide the updated task text and/or description.')
                log_info("Invalid command format.")

        else:
            await update.message.reply_text('Invalid command. Please use the /edittask command first.')
            log_info("Invalid command.")

            return  # Stop further processing if no editing is in progress

        # await handle_messages(update, context)

    except Exception as e:
        print(f"An error occurred while handling the edit task input: {str(e)}")
        log_error("An error occurred while handling the edit task input: {}".format(str(e)))
        await update.message.reply_text('An error occurred while handling the edit task input. Please try again.')


async def handle_task_details_command(update: Update, context: CallbackContext):
    query = update.callback_query
    try:
        task_id = query.data.replace("task_", "")

        # Get the task details from the database using the task_id
        task_details = get_task_by_id(task_id)  # Implement this function to fetch details from the database

        # Format the details and send them to the user
        details_message = f"Task ID: {task_details['id']}\nTask Text: {task_details['text']}\n"
        details_message += f"Description: {task_details['description']}\nStatus: {'Completed' if task_details['status'] == 1 else 'Incomplete'}\n"
        details_message += f"Create Date: {task_details['create_date']}\nComplete Date: {task_details['complete_date']}\n"
        details_message += f"Reminder Time: {task_details['reminder_time']}\nReminder Status: {'Set' if task_details['reminder_status'] == 1 else 'Not Set'}"

        await query.message.reply_text(details_message)

    except Exception as e:
        log_error("An error occurred while handling the task details: {}".format(str(e)))
        await query.message.reply_text('An error occurred while handling the task details. Please try again.')
