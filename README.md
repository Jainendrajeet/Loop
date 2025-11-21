# Loop AI – Voice-Enabled Hospital Assistant

Loop AI is a voice-activated conversational assistant that helps users query information about hospitals using natural speech.  
The system converts **voice → text**, sends the query to the backend, and gets an LLM-generated answer using **Gemini**, **Groq**, or **OpenAI**.

This project demonstrates how to combine:

- Browser-based **Speech-to-Text**
- FastAPI backend for processing
- LLM-powered hospital query answering
- A clean UI with microphone interaction

---

## 🚀 Features

### 🎤 Voice Input  
Uses the browser’s built-in `webkitSpeechRecognition` API to capture audio and transcribe speech to text.

### 🤖 AI Response Generation  
Backend supports pluggable LLMs:
- **Google Gemini** (default)
- **Groq**
- **OpenAI**

### 🏥 Hospital Search Engine  
Searches a local CSV file (`hospitals.csv`) and answers questions like:
- “Give me 3 hospitals near Mumbai”
- “Which hospitals have emergency facilities?”

### 💬 Chat UI  
Beautiful chat interface showing:
- System message  
- User message  
- AI response  

---

## How to Run ?

## Install dependencies
pip install -r requirements.txt

## Add your API Key
Gemini (recommended)
export GEMINI_API_KEY="your-key-here"

OpenAI
export OPENAI_API_KEY="your-key-here"

Groq
export GROQ_API_KEY="your-key-here"

## Run the Backend Server
uvicorn app.main:app --reload --port 8001


## Server will start at:
👉 http://127.0.0.1:8001

