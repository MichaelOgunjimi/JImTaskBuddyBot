from telegram import Update
from telegram.ext import CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
from bot.tasks import add_task_command, complete_task_command, delete_task_command, show_tasks_command, \
    show_tasks_detail_command, set_reminder_command, \
    edit_task_command, show_completed_tasks_command, show_incomplete_tasks_command
from bot.callback_handlers import handle_complete_query, handle_delete_query, handle_task_details_command, \
    handle_edit_task_query, \
    handle_edit_task_input_or_messages, handle_set_reminder_query
from bot.logger import log_info, log_error


def register_handlers(app):
    print("Registering handlers...")  # Add this print statement
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))

    app.add_handler(CommandHandler("addtask", add_task_command))
    app.add_handler(CommandHandler("showtasks", show_tasks_command))

    app.add_handler(CommandHandler("completedtasks", show_completed_tasks_command))
    app.add_handler(CommandHandler("incompletedtasks", show_incomplete_tasks_command))

    # Register the command and callback query handlers
    app.add_handler(CommandHandler("taskdetails", show_tasks_detail_command))
    app.add_handler(CallbackQueryHandler(handle_task_details_command, pattern=r"^task_"))

    app.add_handler(CommandHandler("completetask", complete_task_command))
    app.add_handler(CallbackQueryHandler(handle_complete_query, pattern=r"^complete_task_"))

    app.add_handler(CommandHandler("deletetask", delete_task_command))
    app.add_handler(CallbackQueryHandler(handle_delete_query, pattern=r"^delete_task_"))

    # Add the handlers to the dispatcher
    app.add_handler(CommandHandler("edittask", edit_task_command))
    app.add_handler(CallbackQueryHandler(handle_edit_task_query, pattern=r"^edit_task_"))

    app.add_handler(CommandHandler("setreminder", set_reminder_command))
    app.add_handler(CallbackQueryHandler(handle_set_reminder_query, pattern=r"^reminder_task_"))

    # Register the combined MessageHandler for handling edit task input and other text messages
    app.add_handler(MessageHandler(filters.TEXT, handle_edit_task_input_or_messages))

    # Error
    app.add_error_handler(error)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Logging an informational message
        log_info("Bot started.")

        await update.message.reply_text(
            "Hello! Thanks for chatting with me. I will be helping you manage your tasks. You can add, edit, and mark tasks as completed.")

    except Exception as e:
        log_error("An error occurred while starting the bot: {}".format(str(e)))
        await update.message.reply_text('An error occurred while starting the bot. Please try again.')


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Define the list of available commands and their descriptions
        commands = [
            "/start - Start the bot",
            "/addtask - Add a new task",
            "/completetask - Mark a task as completed",
            "/showtasks - Show all tasks",
            "/help - Get help information",
            "/edittask - Edit a task",
            "/setreminder - Set a reminder for a task",
            "/taskdetails - View the details of a task",
            "/completedtasks - Show all completed tasks",
            "/incompletedtasks - Show all incomplete tasks"
            # Add more commands and descriptions as needed
        ]

        # Generate the help message
        help_message = "Here are the available commands:\n\n"
        help_message += "\n".join(commands)

        await update.message.reply_text(help_message)

    except Exception as e:
        log_error("An error occurred while handling the help command: {}".format(str(e)))
        await update.message.reply_text('An error occurred while handling the help command. Please try again.')


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        # Logging an error message
        log_error("An error occurred: {}".format(context.error))
        print(f"Update {update} caused error {context.error}")

    except Exception as e:
        log_error("An error occurred while handling an error: {}".format(str(e)))
        await update.message.reply_text('An error occurred. Please try again later.')


