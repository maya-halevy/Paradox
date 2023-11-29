"""
This file runs the entire program (main), simply run the script and the chat will begin in the console.
"""

import openai
import constants
import sys
import os

# store registration info (not utilized because script is to demonstrate chatbots)
registration_info = {}


def call_router_chatbot(input_message):
    """
    Calls the router model to get a classification if the user is ready to register or not.
    :param: input_message: (str): The message from the user.
    :return: str: True or False
    Exception: If an error occurs during the API call.
    """
    try:
        conversation_history = [{"role": "system", "content": constants.ROUTER_MODEL_PERSONA}]
        conversation_history.extend(
            constants.ROUTER_TRAINING_SAMPLES + [{"role": "user", "content": input_message}])

        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=conversation_history
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e} call_registration_chatbot")
        sys.exit(1)


def handle_registration():
    """
    Handle the process of user registration. Prompts the user to enter necessary details like parent's name,
    child's name, phone number, etc., and stores this information. :return: dict: A dictionary containing the
    camper's registration information.
    """
    print("\nLet's get you registered! \nWe will just need you to fill out some details.\n")
    # Note: add data integrity checks if time permits
    parent_name = input("Enter your full name: ")
    child_name = input("Enter your child's full name: ")
    phone_number = input("Enter your phone number: ")
    email = input("Enter your email: ")
    child_age = input("Enter your child's age in years: ")
    additional_info = input("Enter any additional info we should know?: ")

    # Save registration info
    # Note: child name is used as a key only for demo purposes
    registration_info[child_name] = {
        "Parent Name": parent_name,
        "Phone Number": phone_number,
        "Email": email,
        "Child Age": child_age,
        "Notes": additional_info
    }
    print(f"\nThat's it! We will contact you shortly at {email} to complete the registration process.")
    return registration_info


def call_inquiry_chatbot(input_message):
    """
    Calls the chatbot model to get a response to the user's input.
    :param: input_message: (str): The message from the user to which the chatbot will respond.
    :return: str: The chatbot's response to the input message.
    Exception: If an error occurs during the API call.
    """
    try:
        conversation_history = [{"role": "system", "content": constants.INQUIRY_MODEL_PERSONA}]
        conversation_history.extend(constants.INQUIRY_TRAINING_SAMPLES + [{"role": "user", "content": input_message}])

        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=conversation_history
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e} call_inquiry_chatbot")
        sys.exit(1)


def main():
    """
    Main function to run the chatbot interface. Manages the user interaction with the chatbot, handling registration
    and responding to queries. Continues running until the user decides to exit. :return:
    """
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        sys.exit(1)
    openai.api_key = api_key

    print("\n*** Welcome to GenAI Summer Camp! *** \n\nTo leave the conversation, type 'exit' at any time."
          "\n\nHi there! I'm Jennifer, how can I help you today?\n")

    while True:

        user_input = input().strip()
        while not user_input:
            user_input = input('Please enter a question\n').strip()

        # opportunity to exit program
        if user_input in ['exit', 'quit']:
            break

        # run chatbots
        else:
            # router chatbot to check if user is ready to register
            if call_router_chatbot(user_input).strip() == 'True':
                # register camper
                handle_registration()
                break  # exit program after camper is registered
            else:
                # inquiry chatbot
                response = call_inquiry_chatbot(user_input)
                print('\nJennifer:', response, '\n')

    print('Thank you!')
    sys.exit(1)


if __name__ == "__main__":
    main()
