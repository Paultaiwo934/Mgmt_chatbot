# 🎓 AI-Powered Academic Chatbot for Professors

Live Chatbots:
- **Chatbot 1 (Dialogflow + RAG):** [Launch](https://app.chatgptbuilder.io/webchat/?p=1686335&id=EXJ5ESfZJ5uTgYPj)
- **Chatbot 2 (OpenAI API):** [Launch](https://mgmtchatbot.web.app)

---

## 📘 Project Overview
This project consists of two AI-powered academic chatbots designed to help professors enhance student engagement and streamline access to course information. By leveraging **Large Language Models (LLMs)** and **Retrieval-Augmented Generation (RAG)**, these bots can answer questions based on unstructured academic content such as syllabi, lecture notes, and course descriptions.

---

## 🤖 Chatbot Architectures

### 🔹 Chatbot 1 – RAG with Google Dialogflow
- Built using **Google Dialogflow ES** for natural language understanding
- Trained on academic datasets and syllabus content
- Uses **ChatGPTBuilder.io** for deployment and UI customization
- Ideal for FAQs, syllabus lookups, and resource navigation

### 🔹 Chatbot 2 – Custom Bot with OpenAI API
- Built using **OpenAI's GPT-3.5/4 API**
- **Frontend:** HTML/CSS deployed via Google Firebase Console
- **Backend:** Python Flask API deployed on **Render.com**
- Integrates with RAG pipeline for document-aware response generation

---

## ⚙️ Features
- ✅ LLM-powered natural language understanding
- ✅ Supports RAG for context-aware, document-based Q&A
- ✅ Processes unstructured data like syllabi, lecture slides, and course materials
- ✅ Cloud deployment (Firebase for frontend, Render for backend)
- ✅ Built-in intent recognition, fallback handling, and semantic search

---

## 🛠️ Tech Stack
- **LLMs:** OpenAI GPT
- **RAG:** Custom document embedding + vector search
- **Frontend:** HTML, CSS (Firebase Hosting)
- **Backend:** Python (Flask on Render)
- **Cloud Services:** Google Dialogflow ES, Render, Firebase

---

## 🚀 Getting Started
### Prerequisites:
- Python 3.8+
- OpenAI API key (for Chatbot 2)
- Firebase account (for frontend deployment)
- Render.com account (for backend deployment)

### Local Setup (Chatbot 2):
```bash
git clone https://github.com/your-username/academic-chatbot.git
cd academic-chatbot/backend
pip install -r requirements.txt
export OPENAI_API_KEY='your-api-key'
python app.py
```

### Frontend Deployment:
Upload your HTML/CSS files to [Firebase Hosting](https://firebase.google.com/docs/hosting).

---
