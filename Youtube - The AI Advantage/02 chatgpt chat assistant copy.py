import openai

# Set your API key
client = openai.OpenAI(api_key="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")

# Initialize the chatbot with a system message
messages = []
system_msg = input("What type of chatbot would you like to create?\n")
messages.append({"role": "system", "content": system_msg})

print("Your new assistant is ready!")
while True:
    user_input = input()
    if user_input.lower() == "quit()":  # Exit condition
        break

    messages.append({"role": "user", "content": user_input})

    # Make request to OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    # Extract the chatbot's response
    reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": reply})

    print("\n" + reply + "\n")
