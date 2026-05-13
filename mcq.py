# mcq.py
from utils import get_response

def generate_mcqs(topic, level, n, grade=None, board=None):
    """
    topic: string
    level: "High School" or "Graduation"
    n: int number of MCQs
    grade/board: required if level == High School
    """
    try:
        if not topic or topic.strip() == "":
            return "⚠️ Please enter a topic."
        try:
            n = int(n)
            if n <= 0:
                return "⚠️ Number of MCQs must be at least 1."
        except:
            n = 5

        if level == "High School":
            if not grade or not board:
                return "⚠️ For High School, please select both Grade and Education Board."
            system_msg = (
                f"You are an exam paper setter for {board} board. Create {n} multiple-choice questions on '{topic}' for {grade} grade.\n"
                "- Keep questions aligned to the {board} style and grade level.\n"
                "- Format each question in Markdown like:\n\n"
                "Q1. Question text\n"
                "a) Option A\nb) Option B\nc) Option C\nd) Option D\n"
                "**Answer:** <Correct Option>\n"
            )
            user_msg = f"Generate {n} MCQs on {topic} for {grade} ({board})."
        else:
            system_msg = (
                f"You are a university professor. Create {n} MCQs on '{topic}' for graduation-level students.\n"
                "- Make questions analytical; if the topic is programming-related include code-snippet questions asking for output or error behavior.\n"
                "- Put any code in fenced triple-backtick blocks. Use the same Markdown Q/option format and add **Answer:** at the end.\n"
            )
            user_msg = f"Generate {n} MCQs on {topic} for Graduation-level students."

        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ]
        return get_response(messages)
    except Exception as e:
        return f"⚠️ Error in MCQ generation: {e}"
        