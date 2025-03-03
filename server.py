from flask import Flask, request, jsonify
from flask_cors import CORS
import openai
import os
import json
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)
CORS(app)

# Load OpenAI API key from environment variable (recommended for security)
openai_api_key = os.getenv("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")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY environment variable is not set.")

openai_client = openai.OpenAI(api_key="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")

# Load course data from JSON file
 try:
with open("course_data.json", "r") as file:
    course_data = json.load(file)["courses"]
    print("Loaded course data:", course_data)

except Exception as e:
    print(f"Error loading course data: {e}")
    course_data = {}

# Function to fetch syllabus data from a URL
def fetch_syllabus_data(url):
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an error for bad status codes
        soup = BeautifulSoup(response.text, "html.parser")
        
        # Extract relevant data from the syllabus page
        syllabus_content = soup.get_text()  # Get all text from the page
        return syllabus_content
    except Exception as e:
        print(f"Error fetching syllabus data: {e}")
        return None

@app.route("/")
def home():
    return "Chatbot API is running! Use /ask to send messages."

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    user_message = data.get("question", "").lower()
    course_name = data.get("course", "").strip()

    # Debugging: Log the received data
    print("Received data:", data)

    # Check if the provided course exists
    if course_name not in course_data:
        return jsonify({"answer": f"Sorry, I don’t have information on {course_name}."})

    course_info = course_data[course_name]

       # Check if the question matches an FAQ entry (case-insensitive)
    for key, value in course_info["question"].items():
        if user_message == key.lower():
            return jsonify({"answer": value})

    # Check if the question is about the syllabus
    if "syllabus" in user_message:
        syllabus_link = course_info.get("syllabus_link")
        if syllabus_link:
            syllabus_data = fetch_syllabus_data(syllabus_link)
            if syllabus_data:
                # Use OpenAI to answer questions based on the syllabus data
                response = openai_client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": f"You are a chatbot assistant for {course_name}. Here is the syllabus data: {syllabus_data}"},
                        {"role": "user", "content": user_message}
                    ]
                )
                chatbot_reply = response.choices[0].message.content
                return jsonify({"answer": chatbot_reply})
            else:
                return jsonify({"answer": "Sorry, I couldn't fetch the syllabus data."})
        else:
            return jsonify({"answer": "No syllabus link available for this course."})

    # If not found, send to OpenAI
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": f"You are a chatbot assistant for {course_name} taught by {course_info.get('professor', 'an instructor')} at the University of West Georgia. Your job is to assist students by answering questions about course materials, assignments, deadlines, and university policies. Refer to the course syllabus, reading materials, and lecture notes to provide accurate answers."},
                {"role": "user", "content": user_message}
            ]
        )
        chatbot_reply = response.choices[0].message.content
        return jsonify({"answer": chatbot_reply})
    except Exception as e:
        return jsonify({"answer": f"An error occurred while processing your request: {str(e)}"})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)