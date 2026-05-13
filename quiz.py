from utils import get_response
import time



# GENERATE QUIZ


def generate_quiz(
    topics,
    level,
    grade,
    board,
    num_questions=10
):

    topic_str = ", ".join(topics)

    prompt = f"""
Generate EXACTLY {num_questions} MCQs.

Student Level: {level}
Grade: {grade}
Board: {board}

Topics: {topic_str}

STRICT RULES:
- Must generate EXACTLY {num_questions} questions
- Questions must match syllabus level
- Use simple language for school students
- Include 4 options
- Mention correct answer
- Do not skip questions

Format strictly:

Q1. Question
a) option
b) option
c) option
d) option
Answer: correct_option
"""

    messages = [
        {
            "role": "system",
            "content": "You are a strict exam paper generator."
        },
        {
            "role": "user",
            "content": prompt
        }
    ]

    return get_response(messages)



# PARSE QUIZ


def parse_quiz(response):

    questions = []

    lines = response.split("\n")

    q = {}

    for line in lines:

        line = line.strip()

        if line.startswith("Q"):

            if q:

                questions.append(q)

                q = {}

            q["question"] = line

            q["options"] = []

        elif line.startswith(("a)", "b)", "c)", "d)")):

            q["options"].append(line)

        elif "Answer:" in line:

            q["answer"] = line.split("Answer:")[-1].strip()

    if q:

        questions.append(q)

    return questions



# START QUIZ


def start_quiz(questions):

    user_answers = []

    start_time = time.time()

    for q in questions:

        print(q["question"])

        for opt in q["options"]:

            print(opt)

        ans = input("Your answer (a/b/c/d): ")

        user_answers.append(ans)

    end_time = time.time()

    total_time = end_time - start_time

    return user_answers, total_time



# EVALUATE QUIZ


def evaluate_quiz(
    questions,
    user_answers
):

    score = 0

    for i, q in enumerate(questions):

        correct = q["answer"].lower()

        user = user_answers[i].lower()

        if user in correct:

            score += 1

    return score



# RUN QUIZ


def run_quiz(
    topics,
    level,
    grade,
    board
):

    raw_quiz = generate_quiz(
        topics=topics,
        level=level,
        grade=grade,
        board=board
    )

    questions = parse_quiz(raw_quiz)

    user_answers, total_time = start_quiz(questions)

    score = evaluate_quiz(
        questions,
        user_answers
    )

    return {

        "score": score,

        "total_questions": len(questions),

        "time_taken": total_time

    }