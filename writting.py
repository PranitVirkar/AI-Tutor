from utils import get_response

def writing_helper(topic, writing_type, language, grade, board):
    prompt = (
        f"Write a {writing_type} on '{topic}' in {language} for a {grade} grade student "
        f"under {board} board. Keep it simple, syllabus-appropriate, and student-friendly."
    )

    messages = [
        {"role": "system", "content": prompt},
        {"role": "user", "content": f"{writing_type} on {topic} in {language} for {grade} grade ({board})"}
    ]
    return get_response(messages)
