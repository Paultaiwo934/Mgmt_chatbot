import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

# Load course data from JSON file
with open("course_data.txt", "r") as file:
    course_data = json.load(file)

# Initialize OpenAI client
openai.api_key = os.getenv("OPENAI_API_KEY")

def find_answer(question):
    """
    Searches for an answer in the course data.
    If no exact match is found, returns None.
    """
    # Iterate over courses in the loaded course_data
    for course, details in course_data.items():
        if "question" in details:
            for q, answer in details["question"].items():
                if question.lower() == q.lower():
                    return answer
    return None

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_question = data.get("question", "").strip()

    # Check if the question exists in the course data
    answer = find_answer(user_question)
    if answer:
        return jsonify({"answer": answer})

    # If no match is found, fallback to OpenAI (ChatGPT)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for Professor John Upson’s courses."},
            {"role": "user", "content": user_question}
        ]
    )

    chatbot_reply = response.choices[0].message['content']
    return jsonify({"answer": chatbot_reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
