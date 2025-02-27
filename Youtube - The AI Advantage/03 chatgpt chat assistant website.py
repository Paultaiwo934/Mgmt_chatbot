import openai
import gradio as gr

# Set your API key
client = openai.OpenAI(api_key="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")

# Initial system message for context
messages = [{"role": "system", "content": "You are a Virtual Assistant for Professor John Upson's classes, he is a professor at the university of west georgia."}]

def CustomChatGPT(user_input):
    messages.append({"role": "user", "content": user_input})
    
    # Request completion from OpenAI API
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    
    # Extract chatbot response
    ChatGPT_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ChatGPT_reply})
    
    return ChatGPT_reply

# Create a Gradio interface
demo = gr.Interface(fn=CustomChatGPT, inputs="text", outputs="text", title="John Upson's Virtual Assistant")

# Launch the chatbot
demo.launch(share=True)

