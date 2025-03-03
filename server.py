from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import json

app = Flask(__name__)
CORS(app)

openai_client = openai.OpenAI(api_key="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")

# Load course data from JSON file
with open("course_data.json", "r") as file:
    course_data = json.load(file)["courses"]

@app.route("/")
def home():
    return "Chatbot API is running! Use /ask to send messages."

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("question", "").lower()
    course_name = data.get("course", "").strip()  # Expecting course name from frontend

    # Check if the provided course exists
    if course_name not in course_data:
        return jsonify({"answer": f"Sorry, I don’t have information on {course_name}."})

    # Check if the question matches an FAQ entry
    course_info = course_data[course_name]
    if user_message in course_info["faq"]:
        return jsonify({"answer": course_info["faq"][user_message]})

    # If not found, send to OpenAI
    response = openai_client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": f"You are a chatbot assistant for {course_name} taught by {course_info.get('professor', 'an instructor')} at the University of West Georgia. Your job is to assist students by answering questions about course materials, assignments, deadlines, and university policies. Refer to the course syllabus, reading materials, and lecture notes to provide accurate answers."},
            {"role": "user", "content": user_message}
        ]
    )

    chatbot_reply = response.choices[0].message.content
    return jsonify({"answer": chatbot_reply})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
