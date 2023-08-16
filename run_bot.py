import threading

from telegram.ext import Application, CallbackContext
import config
from bot.tasks import check_reminders_sync
from bot.task_bot import register_handlers


def start_checking_reminders(app: Application):
    # Create an instance of CallbackContext
    context = CallbackContext(app, None)

    reminders_thread = threading.Thread(target=check_reminders_sync, args=(context,))
    reminders_thread.daemon = True
    reminders_thread.start()


def main():
    app = Application.builder().token(config.BOT_TOKEN).build()

    # Register command handlers
    register_handlers(app)

    # Start the reminders checking function in a separate
    start_checking_reminders(app)

    # Run the bot
    print("Starting Bot...")
    app.run_polling(poll_interval=3)


if __name__ == '__main__':
    main()
