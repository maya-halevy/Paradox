"""
This file runs the entire program (main), simply run the script and the chat will begin in the console.
"""

import openai
import constants
import sys
import os

# store registration info
registration_info = {}


def check_for_registration_intent(user_input):
    """
    Check if the user's input indicates an intent to register.
    :param user_input: (str): The input text from the user.
    :return: bool: True if the input includes keywords related to registration, False otherwise.
    """
    keywords = ['register', 'registration', 'sign-up', 'sign up', 'sign', 'application', 'apply', 'enroll']
    return any(word in user_input for word in keywords)


def handle_registration():
    """
    Handle the process of user registration. Prompts the user to enter necessary details like parent's name,
    child's name, phone number, etc., and stores this information. :return: dict: A dictionary containing the
    camper's registration information.
    """
    print("\nLet's get you registered! We will just need you to give us some details.\n")
    # Note: add data integrity checks if time permits
    parent_name = input("Enter your full name: ")
    child_name = input("Enter your child's full name: ")
    phone_number = input("Enter your phone number: ")
    email = input("Enter your email: ")
    child_age = input("Enter your child's age in years: ")
    additional_info = input("Enter any additional info we should know: ")

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


def call_chatbot(input_message):
    """
    Calls the chatbot model to get a response to the user's input.
    :param: input_message: (str): The message from the user to which the chatbot will respond.
    :return: str: The chatbot's response to the input message.
    Exception: If an error occurs during the API call.
    """
    try:
        conversation_history = [{"role": "system", "content": constants.MODEL_PERSONA}]
        conversation_history.extend(constants.TRAINING_SAMPLES + [{"role": "user", "content": input_message}])

        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=conversation_history
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
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
          "\n\nHi there! I'm Jennifer, I'm happy to answer any questions you have regarding our summer camp.\n")

    while True:
        # get user input
        user_input = input().strip()
        while not user_input:
            user_input = input('Please enter a question\n').strip()

        # exit program
        if user_input in ['exit', 'quit']:
            break

        # see if user wants to register
        elif check_for_registration_intent(user_input):
            if input("\nProceed to registration? Type 'yes': ").strip().lower() == 'yes':
                handle_registration()
                print("\nDo you have any additional questions? \n\nIf not, simply type 'exit'.")
            else:
                print("Okay, what can I help you with today?")
                continue

        # run chatbot
        else:
            response = call_chatbot(user_input)
            print('\nJennifer:', response, '\n')

    print('Thank you!')
    sys.exit(1)


if __name__ == "__main__":
    main()
