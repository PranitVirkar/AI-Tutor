from utils import get_response

def generate_code(topic, language):
    """
    Generates a code snippet for a given topic and programming language.
    """

    if not topic or not language:
        return "⚠️ Topic and language must be provided."

    try:
        system_msg = (
              "You are an expert competitive programming assistant. "
              "Provide optimal and clean solutions with explanation."
              )

        user_msg = (
            f"Solve the following problem in {language}:\n\n"
            f"{topic}\n\n"
            "Steps:\n"
            "1. Explain approach first.\n"
            "2. Then provide well-commented code.\n"
            "3. Provide time and space complexity.\n"
            )

        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ]

        return get_response(messages)

    except Exception as e:
        return f"⚠️ Error in code generation: {e}"