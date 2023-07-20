from telegram.ext import Application
import config
from bot.task_bot import register_handlers


def main():
    app = Application.builder().token(config.BOT_TOKEN).build()

    # Register command handlers
    register_handlers(app)

    # Run the bot
    print("Starting Bot...")
    app.run_polling(poll_interval=3)


if __name__ == '__main__':
    main()
