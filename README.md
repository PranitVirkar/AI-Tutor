AI Tutor 📚🤖

An AI-powered learning assistant built using Python and FastAPI that helps students learn through explanations, quizzes, MCQs, writing assistance, and coding help.

Features
📖 AI-based topic explanation
🧠 MCQ generator
❓ Practice quizzes
💻 Coding helper
✍️ Writing improvement assistant
🏆 Leaderboard system
🔐 Authentication system
Technologies Used
Python
FastAPI
HTML
CSS
JavaScript
SQLite
Generative AI APIs


Project Structure

AI-Tutor/
│
├── main.py
├── app.py
├── explain.py
├── mcq.py
├── quiz.py
├── code_helper.py
├── writting.py
├── database.py
│
├── index.html
├── tutor.html
├── auth.html
│
├── style.css
├── script.js
│
├── requirements.txt
└── README.md


Installation

Go to project folder:

cd AI-Tutor

Install dependencies:

pip install -r requirements.txt

Create .env file:

GROQAPI_KEY=your_api_key

Run the server:

uvicorn main:app --reload

Open in browser:

http://127.0.0.1:8000
