import openai
import constants
import sys
import os

registration_info = {}


def call_chatbot(input_message):
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


def handle_registration():
    print("\nLet's get you registered! We will just need you to give us some details.\n")
    # could add data integrity catches
    parent_name = input("Enter your full name: ")
    child_name = input("Enter your child's full name: ")
    phone_number = input("Enter your phone number: ")
    email = input("Enter your email: ")
    child_age = input("Enter your child's age in years: ")
    additional_info = input("Enter any additional info we should know: ")

    # Save registration info
    registration_info[child_name] = {
        "Parent Name": parent_name,
        "Phone Number": phone_number,
        "Email": email,
        "Child Age": child_age,
        "Notes": additional_info
    }
    print(f"\nThat's it! We will contact you shortly at {email} to complete the registration process.")
    return registration_info


def check_for_registration_intent(user_input):
    keywords = ['register', 'registration', 'sign-up', 'sign up', 'sign', 'application', 'apply', 'enroll']
    return any(word in user_input for word in keywords)


def main():
    print("\n*** Welcome to GenAI Summer Camp! ***")
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        sys.exit(1)
    openai.api_key = api_key
    print("\nTo leave the conversation, type 'exit' at any time.\n\nHi there! I'm Jennifer, I'm happy to answer any "
          "questions you have regarding our summer camp.\n")
    while True:
        user_input = input().strip()
        while not user_input:
            user_input = input('Please enter a question\n').strip()

        if user_input in ['exit', 'quit']:
            break
        elif check_for_registration_intent(user_input):
            if input("\nProceed to registration? Type 'yes': ").strip().lower() == 'yes':
                handle_registration()
                print("\nDo you have any additional questions? \n\nIf not, simply type 'exit'.")
            else:
                print("Okay, what can I help you with today?")
                continue

        else:
            response = call_chatbot(user_input)
            print('\n-> ', response, '\n')

    print('Thank you!')
    sys.exit(1)


if __name__ == "__main__":
    main()
