from dateutil import parser
import schedule
import time
import datetime


def schedule_task_timer(task_id, time_input):
    print("schedule_task_timer called")
    print(time_input)
    try:
        # Parse the natural language time input using dateutil.parser.parse
        time_delta = parser.parse(time_input, default=datetime.datetime.utcnow()) - datetime.datetime.utcnow()
        # Convert the time delta to seconds
        time_seconds = int(time_delta.total_seconds())
        if time_seconds <= 0:
            raise ValueError("Invalid time input. Please specify a future time.")

        # Schedule the task timer using the `schedule` library
        schedule.every(time_seconds).seconds.do(send_task_reminder, task_id)

        return True  # Successfully scheduled the task
    except Exception as e:
        print("Error scheduling task:", str(e))
        return False  # Failed to schedule the task


def send_task_reminder(task_id):
    pass
    # Implement the code to send a task reminder to the user
    # You can use your preferred method to send notifications (e.g., Telegram message)
    # Get the task details from the database using the `task_id`, and send the reminder to the user


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
        # Check for state transitions
