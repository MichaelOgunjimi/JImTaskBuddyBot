import schedule
import time


def schedule_task_timer(task_id):
    pass
    # Schedule the task timer
    # ...


def send_task_reminder(task_id):
    pass
    # Send the task reminder
    # ...


def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(1)
