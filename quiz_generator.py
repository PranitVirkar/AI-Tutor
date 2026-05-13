from openai import OpenAI
import json
import sqlite3

# =========================
# OPENROUTER CLIENT
# =========================

client = OpenAI(
    api_key="ENter your API key",
    base_url="https://openrouter.ai/api/v1"
)

# =========================
# CONNECT TO EXISTING DATABASE
# =========================

# Replace with your existing database name
conn = sqlite3.connect("users.db")

cursor = conn.cursor()

# =========================
# CREATE LEADERBOARD TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS leaderboard (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    topic TEXT,
    score INTEGER
)
""")

conn.commit()

# =========================
# USER INPUT
# =========================

username = input("Enter your username: ")

topic = input("Enter quiz topic: ")

# =========================
# AI PROMPT
# =========================

prompt = f"""
Generate 5 MCQ questions on {topic}.

Return ONLY valid JSON in this format:

[
  {{
    "question": "Question here",
    "options": ["Option1", "Option2", "Option3", "Option4"],
    "answer": "Correct Option"
  }}
]

Do not write anything except JSON.
"""

# =========================
# GENERATE QUIZ
# =========================

response = client.chat.completions.create(
    model="openai/gpt-3.5-turbo",
    messages=[
        {
            "role": "user",
            "content": prompt
        }
    ]
)

# =========================
# CONVERT JSON RESPONSE
# =========================

quiz_data = json.loads(response.choices[0].message.content)

# =========================
# QUIZ LOGIC
# =========================

score = 0

for i, q in enumerate(quiz_data, start=1):

    print(f"\nQ{i}: {q['question']}")

    options = q['options']

    for idx, option in enumerate(options, start=1):
        print(f"{idx}. {option}")

    # VALIDATION
    while True:

        try:
            user_answer = int(input("Enter option number (1-4): "))

            if 1 <= user_answer <= 4:
                break
            else:
                print("Please enter a number between 1 and 4.")

        except:
            print("Invalid input. Enter numbers only.")

    selected_option = options[user_answer - 1]

    # CHECK ANSWER
    if selected_option == q['answer']:

        print("Correct! +10 points")

        score += 10

    else:

        print("Wrong!")

        print("Correct Answer:", q['answer'])

# =========================
# FINAL SCORE
# =========================

print("\nQuiz Finished!")

print("Your Final Score:", score)

# =========================
# SAVE SCORE TO DATABASE
# =========================

cursor.execute(
    "INSERT INTO leaderboard (username, topic, score) VALUES (?, ?, ?)",
    (username, topic, score)
)

conn.commit()

print("Score saved successfully!")

# =========================
# SHOW LEADERBOARD
# =========================

print("\n===== LEADERBOARD =====")

cursor.execute("""
SELECT username, topic, score
FROM leaderboard
ORDER BY score DESC
LIMIT 5
""")

leaderboard = cursor.fetchall()

for rank, row in enumerate(leaderboard, start=1):

    print(f"{rank}. {row[0]} | {row[1]} | {row[2]} points")

# =========================
# CLOSE DATABASE
# =========================

conn.close()
