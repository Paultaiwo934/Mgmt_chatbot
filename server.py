from flask import Flask, request, jsonify
import openai
import json
import os

app = Flask(__name__)

# Load OpenAI API Key from environment variable
OPENAI_API_KEY = os.getenv("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")

# Load courses data
COURSES_FILE = "courses.json"

try:
    with open(COURSES_FILE, "r") as file:
        courses_data = json.load(file)
except Exception as e:
    courses_data = {}
    print(f"Error loading courses.json: {e}")

# Function to find an answer from courses.json
def find_answer(question):
    question_lower = question.lower()
    
    for course, details in courses_data.items():
        if "sections" in details:
            for section, sec_details in details["sections"].items():
                for key, value in sec_details.items():
                    if isinstance(value, str) and question_lower in key.lower():
                        return value
                    elif isinstance(value, list) and any(question_lower in str(item).lower() for item in value):
                        return ", ".join(value)
        if "notes" in details and question_lower in details["notes"].lower():
            return details["notes"]
        if "due_dates" in details:
            for due in details["due_dates"]:
                if question_lower in due["title"].lower():
                    return f"{due['title']} is due on {due['due_date']}."

    return None  # No match found in courses.json

# OpenAI API Call
def ask_chatgpt(question):
    if not OPENAI_API_KEY:
        return "Error: OpenAI API key is missing."
    
    openai.api_key = OPENAI_API_KEY

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "system", "content": "You are an AI assistant for Professor John Upson’s classes at the University of West Georgia. Your job is to assist students by answering questions about course materials, assignments, deadlines, and university policies."},
                      {"role": "user", "content": question}],
            temperature=0.7,
            max_tokens=200
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        return f"Error fetching response from OpenAI: {str(e)}"

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    question = data.get("input", "").strip()

    if not question:
        return jsonify({"error": "Input cannot be empty."})

    # Check for an answer in courses.json
    answer = find_answer(question)
    if answer:
        return jsonify({"response": answer})

    # If not found, ask OpenAI
    response = ask_chatgpt(question)
    return jsonify({"response": response})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
