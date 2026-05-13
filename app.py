from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3
import json
import os

from explain import explain_topic
from mcq import generate_mcqs
from writting import writing_helper
from code_helper import generate_code
from quiz import generate_quiz, parse_quiz
from leaderboard import save_result

app = Flask(__name__)
CORS(app)

# ---------------- DATABASE CONNECTION ---------------- #

def get_db_connection():
    conn = sqlite3.connect("aitutor.db")
    conn.row_factory = sqlite3.Row
    return conn


# ---------------- REGISTER USER ---------------- #

@app.route('/register', methods=['POST'])
def register():

    data = request.json

    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    conn = None

    try:

        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (username, email, password)
            VALUES (?, ?, ?)
        """, (username, email, password))

        conn.commit()

        return jsonify({
            "message": "✅ User registered successfully!"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

    finally:

        if conn:
            conn.close()


# ---------------- EXPLAIN API ---------------- #

@app.route('/explain', methods=['POST'])
def explain():

    data = request.json

    result = explain_topic(
        data.get('topic'),
        data.get('level'),
        data.get('grade'),
        data.get('board')
    )

    return jsonify({
        'result': result
    })


# ---------------- MCQ API ---------------- #

@app.route('/mcq', methods=['POST'])
def mcq():

    data = request.json

    result = generate_mcqs(
        data.get('topic'),
        data.get('level'),
        data.get('n', 5),
        data.get('grade'),
        data.get('board')
    )

    return jsonify({
        'result': result
    })


# ---------------- WRITING API ---------------- #

@app.route('/write', methods=['POST'])
def write():

    data = request.json

    result = writing_helper(
        data.get('topic'),
        data.get('writing_type'),
        data.get('language'),
        data.get('grade'),
        data.get('board')
    )

    return jsonify({
        'result': result
    })


# ---------------- CODE GENERATION API ---------------- #

@app.route('/code', methods=['POST'])
def code():

    data = request.json

    result = generate_code(
        data.get('question'),
        data.get('language')
    )

    return jsonify({
        'result': result
    })


# ---------------- QUIZ API ---------------- #

@app.route('/quiz', methods=['POST'])
def quiz():

    data = request.json

    raw = generate_quiz(
        data.get('topics', []),
        data.get('grade')
    )

    questions = parse_quiz(raw)

    return jsonify({
        'questions': questions
    })


# ---------------- SAVE QUIZ RESULT ---------------- #

@app.route('/save-result', methods=['POST'])
def save_quiz_result():

    data = request.json

    try:

        save_result(
            data.get("name"),
            data.get("result"),
            data.get("topics"),
            data.get("grade")
        )

        return jsonify({
            "message": "✅ Result saved successfully!"
        })

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


# ---------------- LEADERBOARD API ---------------- #

@app.route('/leaderboard', methods=['GET'])
def leaderboard():

    try:

        leaderboard_file = "leaderboard.json"

        if not os.path.exists(leaderboard_file):

            return jsonify([])

        with open(leaderboard_file, "r", encoding="utf-8") as f:

            leaderboard_data = json.load(f)

        sorted_board = sorted(
            leaderboard_data,
            key=lambda x: (
                -x.get("percentage", 0),
                x.get("time_taken", float('inf'))
            )
        )

        return jsonify(sorted_board)

    except Exception as e:

        return jsonify({
            "error": str(e)
        })


# ---------------- HOME ROUTE ---------------- #

@app.route('/')
def home():

    return jsonify({
        "message": "✅ SyntaxSensei Backend Running Successfully!"
    })


# ---------------- RUN APP ---------------- #

if __name__ == '__main__':

    app.run(debug=True, port=5000)