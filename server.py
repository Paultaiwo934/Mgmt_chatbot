from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os

app = Flask(__name__)

# Enable CORS for all domains (for local testing)
CORS(app)

openai_client = openai.OpenAI(api_key="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")

@app.route("/")
def home():
    return "Chatbot API is running! Use /ask to send messages."

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("question", "")

    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot assistant for Professor John Upson’s classes at the University of West Georgia. Your job is to assist students by answering questions about course materials, assignments, deadlines, and university policies. Refer to the course syllabus, reading materials, and lecture notes to provide accurate answers."},
            {"role": "user", "content": user_message}
        ]
    )

    chatbot_reply = response.choices[0].message.content

    # Explicitly set CORS headers in the response
    response_data = jsonify({"answer": chatbot_reply})
    response_data.headers.add("Access-Control-Allow-Origin", "*")
    response_data.headers.add("Access-Control-Allow-Headers", "Content-Type,Authorization")
    response_data.headers.add("Access-Control-Allow-Methods", "POST,OPTIONS")

    return response_data

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Default to 5000 if PORT isn't set
    app.run(host="0.0.0.0", port=port)
