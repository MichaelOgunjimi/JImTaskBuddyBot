# JimTaskBuddy - Your Daily Task Assistant

<p align="center" style="border-radius: 20px;">
  <img src="images/JimTaskBuddyLogo.jpg" alt="JimTaskBuddy Logo" width="200" height="200">
</p>
<p align="center">
A bot designed to help you manage your daily tasks with ease.
</p>

<p align="center">
JimTaskBuddy is a Telegram bot created through the Telegram API, dedicated to improving your task management and productivity. Powered by Natural Language Processing, the bot intelligently understands your commands and responds accordingly. From adding and tracking tasks to setting reminders, JimTaskBuddy has got you covered!
</p>

## At a Glance

![JimTaskBuddy](/images/jimtaskbuddy.png)

## Features

### 1. AddTask

- Command: `/addtask <task_text> [description:<task_description>]`
- Description: Add a new task to your list with an optional description.

### 2. CompleteTask

- Command: `/completetask <task_id>`
- Description: Mark a task as completed to stay organized.

### 3. ShowTasks

- Command: `/showtasks`
- Description: View all your tasks in one place.

### 4. CompletedTasks

- Command: `/completedtasks`
- Description: See a list of your completed tasks.

### 5. IncompleteTasks

- Command: `/incompletetasks`
- Description: Check your pending tasks that need completion.

### 6. EditTask

- Command: `/edittask <task_id> <new_text>`
- Description: Modify the text of an existing task for better clarity.

### 7. DeleteTask

- Command: `/deletetask <task_id>`
- Description: Remove a task from your list when it's no longer needed.

### 8. SetReminder

- Command: `/setreminder <task_id> <reminder_time>`
- Description: Set a reminder for a task to stay on top of your schedule.

### 9. TaskDetails

- Command: `/taskdetails <task_id>`
- Description: Get detailed information about a specific task.

## Usage

### Table View

| Command          | Description                                                |
|------------------|------------------------------------------------------------|
| /addtask         | Add a new task to your list with an optional description.  |
| /completetask    | Mark a task as completed to stay organized.                |
| /showtasks       | View all your tasks in one place.                          |
| /completedtasks  | See a list of your completed tasks.                        |
| /incompletetasks | Check your pending tasks that need completion.             |
| /edittask        | Modify the text of an existing task for better clarity.    |
| /deletetask      | Remove a task from your list when it's no longer needed.   |
| /setreminder     | Set a reminder for a task to stay on top of your schedule. |
| /taskdetails     | Get detailed information about a specific task.            |

### How It Works

|                 Demo #1                 |                 Demo #2                 |
|:---------------------------------------:|:---------------------------------------:|
| ![JimTaskBuddy Demo](/images/demo1.jpg) | ![JimTaskBuddy Demo](/images/demo2.jpg) |

In the "How It Works" section, we have provided two demo images to showcase the functionality of JimTaskBuddy. These images demonstrate how the bot works in different scenarios.

## Get Started

1. Obtain your Telegram token from BotFather. More information can be found [here](https://core.telegram.org/bots).

2. Plug in your token at the top of the `index.py` file.

3. Clone this repository and install the required dependencies by running:

```sh
pip install -r requirements.txt
```

4. Run the bot:

```sh
python index.py
```

## Usage Video

![JimTaskBuddy](/images/dummyvideo.mp4)

With JimTaskBuddy as your daily task assistant, you can stay organized, focused, and productive throughout your day. Try
it out and simplify your task management today!