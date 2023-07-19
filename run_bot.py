from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import config
from bot.task_bot import register_handlers, start, error


def main():
    app = Application.builder().token(config.BOT_TOKEN).build()

    # Register command handlers
    register_handlers(app)

    # Error
    app.add_error_handler(error)

    print("Starting Bot...")
    app.run_polling(poll_interval=3)


if __name__ == '__main__':
    main()
