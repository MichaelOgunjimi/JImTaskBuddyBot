from bot.tasks import cursor, conn, log_error, log_info
from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler, CallbackContext
from config import BOT_USERNAME
from bot.response import get_response
import re
from bot.scheduler import schedule_task_timer


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
    print("Handling edit task input or messages...")  # Add this print statement
    try:
        if 'edit_task_id' in context.user_data:
            print("Editing task input in progress")
            # Editing task input is in progress, handle it
            await handle_edit_task_input(update, context)
        elif 'set_timer_task_id' in context.user_data:
            print("Setting timer input in progress")
            # Setting timer input is in progress, handle it
            return handle_timer_input(update, context)
        else:
            print("No editing task input in progress")
            # No editing task input in progress, handle other text messages
            await handle_messages(update, context)

    except Exception as e:
        print(f"An error occurred in handle_edit_task_input_or_messages: {str(e)}")
        log_error("An error occurred in handle_edit_task_input_or_messages: {}".format(str(e)))
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

        log_info("Bot: " + response)
        await update.message.reply_text(response)

    except Exception as e:
        log_error("An error occurred while handling messages: {}".format(str(e)))
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


async def handle_set_timer_query(update: Update, context: CallbackContext):
    query = update.callback_query
    try:
        task_id = query.data.replace("setreminder_", "")

        # Ask the user for the time input using a message
        context.user_data['set_timer_task_id'] = task_id
        await query.message.reply_text("Please enter the time for the reminder using natural language (e.g., 2 hours, 4 days):")

        # Set the next state to handle_timer_input
        context.set_next_state("handle_timer_input")

    except Exception as e:
        log_error("An error occurred while handling the set_timer callback: {}".format(str(e)))
        await query.message.reply_text('An error occurred while handling the set_timer callback. Please try again.')


async def handle_timer_input(update: Update, context: CallbackContext):
    try:
        time_input = update.message.text
        task_id = context.user_data['set_timer_task_id']
        success = schedule_task_timer(task_id, time_input)

        if success:
            await update.message.reply_text(f"Reminder set successfully for the task with ID {task_id}.")
        else:
            await update.message.reply_text("Failed to set the reminder. Please try again.")

        # Clear the user_data to mark the end of the timer input
        context.user_data.pop('set_timer_task_id')

        # Return to handling other messages
        await handle_messages(update, context)

    except Exception as e:
        log_error("An error occurred while handling the timer input: {}".format(str(e)))
        await update.message.reply_text('An error occurred while handling the timer input. Please try again.')
        # Clear the user_data to mark the end of the timer input
        context.user_data.pop('set_timer_task_id')