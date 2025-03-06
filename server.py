import json
import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import openai

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Get the directory of server.py
DATA_PATH = os.path.join(BASE_DIR, "course_data.json")  # Construct absolute path

with open(DATA_PATH, "r") as file:
    course_data = json.load(file)

openai_client = openai.OpenAI(api_key=os.getenv("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"))  # Use environment variable for security


def find_answer(question):
    """
    Searches for an answer in the course_data.json file.
    If no exact match is found, returns None.
    """
    for course, details in course_data["courses"].items():
        if "question" in details:
            for q, answer in details["question"].items():
                if question.lower() == q.lower():
                    return answer
    return None


@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_question = data.get("question", "").strip()

    # Check if the question exists in the JSON file
    answer = find_answer(user_question)
    if answer:
        return jsonify({"answer": answer})

    # If no match found, fallback to OpenAI
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a chatbot assistant for Professor John Upson’s classes at the University of West Georgia. Your job is to assist students by answering questions about course materials, assignments, deadlines, and university policies."},
            {"role": "user", "content": user_question}
        ]
    )

    chatbot_reply = response.choices[0].message.content
    return jsonify({"answer": chatbot_reply})


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
