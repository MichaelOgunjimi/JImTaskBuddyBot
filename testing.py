import re
import datetime
import time


def process_duration(message):
    # Regular expression to extract numeric values and time units from the input text
    duration_pattern = r'(\d+)\s*(seconds?|minutes?|hours?|days?|weeks?|months?|years?)'
    matches = re.findall(duration_pattern, message)

    # Create a dictionary to map time units to their corresponding values in seconds
    time_units = {
        'seconds': 1,
        'minutes': 60,
        'hours': 3600,
        'days': 86400,
        'weeks': 604800,
        'months': 2629746,
        'years': 31556952,
        'second': 1,
        'minute': 60,
        'hour': 3600,
        'day': 86400,
        'week': 604800,
        'month': 2629746,
        'year': 31556952
    }

    total_seconds = 0
    for value, unit in matches:
        total_seconds += int(value) * time_units.get(unit.lower(), 0)

    # Return the timedelta object and formatted datetime for the database
    duration_timedelta = datetime.timedelta(seconds=total_seconds)
    future_datetime = datetime.datetime.now() + duration_timedelta
    future_date_str = future_datetime.isoformat()

    return duration_timedelta, future_date_str


# Test the function with user input
user_input = "Set a reminder for 2 weeks, 3 days, 1 hour, and 45 minutes"
duration_timedelta, future_date_str = process_duration(user_input)
# Get the current date and time
current_datetime = datetime.datetime.now().isoformat()
# print("Duration Timedelta:", duration_timedelta)
print("Current Date and Time:", current_datetime)
print("Formatted Future Date for Database:", future_date_str)


def check_reminders():
    future_datetime = datetime.datetime.now() + datetime.timedelta(seconds=30)
    future_datetime = future_datetime.isoformat()

    while True:
        # Get the current date and time
        current_datetime = datetime.datetime.now().isoformat()

        # Compare with the future time for testing
        if future_datetime <= current_datetime:
            print("Reminder time has passed!")

        print("STILL CHECKING REMINDERS...")
        time.sleep(10)


# Call the function to start checking reminders
check_reminders()
