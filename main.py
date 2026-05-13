from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from explain import explain_topic
from code_helper import generate_code
from writting import writing_helper
from quiz import generate_quiz, parse_quiz

import sqlite3
import json

app = FastAPI()



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# DATABASE CONNECTION


conn = sqlite3.connect(
    "users.db",
    check_same_thread=False
)

cursor = conn.cursor()


# CREATE LEADERBOARD TABLE


cursor.execute("""
CREATE TABLE IF NOT EXISTS leaderboard (

    username TEXT PRIMARY KEY,

    score INTEGER DEFAULT 0

)
""")

conn.commit()


# CREATE CHAT HISTORY TABLE


cursor.execute("""
CREATE TABLE IF NOT EXISTS chat_history (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,

    question TEXT,

    response TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP

)
""")

conn.commit()


# CREATE USERS TABLE


cursor.execute("""
CREATE TABLE IF NOT EXISTS users (

    id INTEGER PRIMARY KEY AUTOINCREMENT,

    username TEXT,

    email TEXT UNIQUE,

    password TEXT

)
""")

conn.commit()

# HOME ROUTE


@app.get("/")
def home():

    return {
        "message": "SyntaxSensei Backend Running"
    }


# ASK AI API


@app.get("/ask-ai")
def ask_ai(
    question: str,
    username: str = "Guest",
    level: str = None,
    grade: str = None,
    board: str = None
):

    
    # GENERATE EXPLANATION
    

    explanation = explain_topic(
        topic=question,
        level=level,
        grade=grade,
        board=board
    )

   
    # SAVE CHAT HISTORY
    

    cursor.execute(
        """
        INSERT INTO chat_history
        (username, question, response)
        VALUES (?, ?, ?)
        """,
        (
            username,
            question,
            explanation
        )
    )

    conn.commit()

    
    # GENERATE QUIZ
    

    raw_quiz = generate_quiz(
        topics=[question],
        level=level,
        grade=grade,
        board=board,
        num_questions=5
    )

    parsed_quiz = parse_quiz(raw_quiz)

    
    # RETURN RESPONSE
    

    return {

        "question": question,

        "explanation": explanation,

        "quiz": parsed_quiz

    }


# MCQ GENERATOR API


@app.get("/generate-mcq")
def generate_mcq(
    topic: str,
    level: str,
    grade: str,
    board: str,
    num_questions: int = 5
):

   
    # GENERATE QUIZ
    

    raw_quiz = generate_quiz(
        topics=[topic],
        level=level,
        grade=grade,
        board=board,
        num_questions=num_questions
    )

    
    # PARSE QUIZ
    

    parsed_quiz = parse_quiz(raw_quiz)

    
    # RETURN RESPONSE
    

    return {

        "topic": topic,

        "level": level,

        "grade": grade,

        "board": board,

        "total_questions": num_questions,

        "quiz": parsed_quiz

    }


# WRITING ASSISTANT API


@app.get("/writing-helper")
def writing_assistant(
    topic: str,
    writing_type: str,
    language: str,
    grade: str,
    board: str
):

    response = writing_helper(
        topic=topic,
        writing_type=writing_type,
        language=language,
        grade=grade,
        board=board
    )

    return {

        "topic": topic,

        "response": response

    }


# CODE HELPER API


@app.get("/code-helper")
def code_helper_api(
    topic: str,
    language: str
):

    response = generate_code(
        topic=topic,
        language=language
    )

    return {

        "topic": topic,

        "response": response

    }


# PRACTICE QUIZ API


@app.get("/practice-quiz")
def practice_quiz_api(
    topic: str,
    level: str,
    grade: str,
    board: str,
    num_questions: int = 10
):

    raw_quiz = generate_quiz(
        topics=[topic],
        level=level,
        grade=grade,
        board=board,
        num_questions=num_questions
    )

    parsed_quiz = parse_quiz(raw_quiz)

    return {

        "topic": topic,

        "level": level,

        "grade": grade,

        "board": board,

        "total_questions": num_questions,

        "quiz": parsed_quiz

    }


# SUBMIT SCORE API


@app.post("/submit-score")
def submit_score(
    username: str,
    score: int
):

    cursor.execute(
        """
        SELECT score
        FROM leaderboard
        WHERE username = ?
        """,
        (username,)
    )

    existing_user = cursor.fetchone()

   
    # NEW USER
    

    if existing_user is None:

        cursor.execute(
            """
            INSERT INTO leaderboard
            (username, score)
            VALUES (?, ?)
            """,
            (
                username,
                score
            )
        )

    
    # UPDATE SCORE
    

    else:

        current_score = existing_user[0]

        updated_score = current_score + score

        cursor.execute(
            """
            UPDATE leaderboard
            SET score = ?
            WHERE username = ?
            """,
            (
                updated_score,
                username
            )
        )

    conn.commit()

    return {

        "message": "Leaderboard Updated"

    }


# LEADERBOARD API


@app.get("/leaderboard")
def leaderboard():

    cursor.execute("""
    SELECT username, score
    FROM leaderboard
    ORDER BY score DESC
    LIMIT 10
    """)

    data = cursor.fetchall()

    leaderboard_data = []

    for row in data:

        leaderboard_data.append({

            "username": row[0],

            "score": row[1]

        })

    return leaderboard_data


# CHAT HISTORY API


@app.get("/chat-history")
def get_chat_history(username: str):

    cursor.execute(
        """
        SELECT question, response, created_at
        FROM chat_history
        WHERE username = ?
        ORDER BY created_at DESC
        """,
        (username,)
    )

    rows = cursor.fetchall()

    history = []

    for row in rows:

        history.append({

            "question": row[0],

            "response": row[1],

            "created_at": row[2]

        })

    return history


# REGISTER API


@app.post("/register")
def register(
    username: str,
    email: str,
    password: str
):

    cursor.execute(
        """
        SELECT *
        FROM users
        WHERE email = ?
        """,
        (email,)
    )

    existing_user = cursor.fetchone()

    if existing_user:

        return {

            "success": False,

            "message": "Email already exists"

        }

    cursor.execute(
        """
        INSERT INTO users
        (username, email, password)
        VALUES (?, ?, ?)
        """,
        (
            username,
            email,
            password
        )
    )

    conn.commit()

    return {

        "success": True,

        "message": "Registration successful"

    }


# LOGIN API


@app.post("/login")
def login(
    email: str,
    password: str
):

    cursor.execute(
        """
        SELECT username
        FROM users
        WHERE email = ?
        AND password = ?
        """,
        (
            email,
            password
        )
    )

    user = cursor.fetchone()

    if user:

        return {

            "success": True,

            "username": user[0]

        }

    return {

        "success": False,

        "message": "Invalid email or password"

    }