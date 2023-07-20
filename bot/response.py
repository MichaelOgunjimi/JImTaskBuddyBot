import re
from bot.response_list import response_list


def process_message(message, response_array, response):
    # Splits the message and the punctuation into an array
    list_message = re.findall(r"[\w']+|[.,!?;]", message.lower())

    # Scores the amount of words in the message
    score = 0
    for word in list_message:
        if word in response_array:
            score = score + 1

    # Returns the response and the score of the response
    return [score, response]


def get_response(message):
    # Add your custom responses here
    processed_response_list = [

    ]
    for res in response_list:
        processed_response_list.append(process_message(message, res[0], " ".join(res[1])))

    # Checks all of the response scores and returns the best matching response
    response_scores = [response[0] for response in processed_response_list]

    # Get the max value for the best response and store it into a variable
    winning_response = max(response_scores)
    matching_response = processed_response_list[response_scores.index(winning_response)]

    # Return the matching response to the user
    if winning_response == 0:
        bot_response = 'I didn\'t understand what you wrote.'
    else:
        bot_response = matching_response[1]

    print('Bot response:', bot_response)

    return bot_response

# Test your system
# get_response('What is your name?') # Output: My name is MyTaskBuddy, nice to meet you!
# get_response('Can you help me with something please?') # Output: I will do my best to assist you!
# get_response('Add a new task for me.') # Output: You can use the /addtask command to add a task.
# get_response('How can I complete a task?') # Output: To complete a task, use the /completetask command.
# get_response('Show me my tasks.') # Output: To see your tasks, use the /showtasks command.
# get_response('Can I edit a task?') # Output: To edit a task, use the /edittask command.
# get_response('Delete a task from my list.') # Output: To delete a task, use the /deletetask command.
# get_response('Can you remind me about a task?') # Output: To set a task reminder, use the /setreminder command.
# get_response('Tell me the details of a task.') # Output: To get details about a task, use the /taskdetails command.
