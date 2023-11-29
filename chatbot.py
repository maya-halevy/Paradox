import openai
import constants

registration_info = {}


def call_chatbot(input_message):
    try:
        conversation_history = [{"role": "system", "content": constants.model_persona}]
        conversation_history.extend(constants.training_samples + [{"role": "user", "content": input_message}])

        completion = openai.ChatCompletion.create(
            model='gpt-3.5-turbo',
            messages=conversation_history
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"An error occurred: {e}")
        return "Sorry, something went wrong."


def handle_registration():
    print("Let's get you registered! We will just need you to give us some details.\n")
    parent_name = input("Please enter your full name: ")
    child_name = input("Please enter your child's full name: ")
    phone_number = input("Please enter your phone number: ")
    email = input("Please enter your email: ")
    child_age = input("Please enter your child's age in years: ")

    # Save registration info
    registration_info[child_name] = {
        "Parent Name": parent_name,
        "Phone Number": phone_number,
        "Email": email,
        "Child Age": child_age
    }
    print(f"That's it! We will contact you shortly at {email} to complete the registration process.")
    return registration_info


def check_for_registration_intent(user_input):
    keywords = ['register', 'registration', 'sign-up', 'sign up', 'sign', 'application', 'apply']
    return any(word in user_input for word in keywords)


def main():
    print("\nWelcome to GenAI Summer Camp!\n")
    openai.api_key = input('Enter your API key: ').strip()
    print("\nIf you would like to register for our camp, simply type 'register'. \nOtherwise, I am happy "
          "to answer any questions regarding our summer camp. \nTo exit, type 'exit'.\n")

    while True:
        user_input = input("\nType 'register' to sign up, ask a question, or 'exit' to quit:\n").strip().lower()

        if user_input in ['exit', 'quit']:
            break
        elif user_input == 'register':
            handle_registration()
        elif check_for_registration_intent(user_input):
            if input("Proceed to registration? Type 'yes': ").strip().lower() == 'yes':
                handle_registration()
            else:
                continue
        else:
            response = call_chatbot(user_input)
            print(response)

    print('Thank you! Goodbye')


if __name__ == "__main__":
    main()

