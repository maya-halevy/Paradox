import openai
import constants

registration_info = {}

def call_chatbot(input_message):
    # initialize model history with its persona and training samples
    conversation_history = [{"role": "system", "content": constants.model_persona}]
    conversation_history.extend(constants.training_samples + [{"role": "user", "content": input_message}])

    completion = openai.ChatCompletion.create(
        model='gpt-3.5-turbo',
        messages=conversation_history  # Using the updated conversation history
    )
    return completion.choices[0].message.content


def handle_registration():
    print("I need to get some info for your registration, this won't take long.")
    parent_name = input("Please enter your full name: ")
    child_name = input("Please enter your child's full name: ")
    phone_number = input("Please enter your phone number: ")
    email = input("Please enter your email: ")
    child_age = int(input("Please enter your child's age: "))

    # Save registration info
    registration_info[child_name] = {
        "Parent Name": parent_name,
        "Phone Number": phone_number,
        "Email": email,
        "Child Age": child_age
    }
    print(f"That's it! We will contact you shortly at {email} to complete the registration process.")
    return None


print("\nThank your for your interest in GenAI summer camp!\n")
openai.api_key = input('To get started, please enter your API key: ')
print("\nIf you would like to register for our camp, simply type 'register'. \nOtherwise, I am happy "
      "to answer any questions regarding our summer camp. \nTo exit, type 'exit'.\n")
while True:
    user_input = input()
    if user_input.strip().lower() == 'exit' or user_input.strip().lower() == 'quit':
        break
    elif user_input.strip().lower() == 'register':
        print("Let's get you registered! We will just need you to give us some details.\n")
        handle_registration()
        print("Do you have any additional questions about the camp? If not, simply type 'exit'." )
    else:
        reply = call_chatbot(user_input)
        print(reply)
print('Thank you!')

