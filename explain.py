from utils import get_response


def explain_topic(topic, level, grade=None, board=None):
    """
    topic: string
    level: "High School" or "Graduation"
    grade: e.g. "5th", "6th" ... (required if level == High School)
    board: "CBSE"/"ICSE"/"SSC" (required if level == High School)
    """

    try:
        
        if not topic or topic.strip() == "":
            return "⚠️ Please enter a topic."

        topic_lower = topic.lower()

       
        coding_keywords = [
            "python",
            "java",
            "c++",
            "javascript",
            "react",
            "html",
            "css",
            "sql",
            "api",
            "array",
            "arrays",
            "linked list",
            "stack",
            "queue",
            "algorithm",
            "algorithms",
            "data structure",
            "database",
            "loop",
            "loops",
            "function",
            "functions",
            "class",
            "object",
            "oops",
            "django",
            "flask",
            "node",
            "express",
            "mongodb",
            "machine learning",
            "deep learning",
            "artificial intelligence"
        ]

        is_coding_topic = any(
            keyword in topic_lower for keyword in coding_keywords
        )

        
        non_coding_keywords = [
            "war",
            "history",
            "geography",
            "politics",
            "biology",
            "chemistry",
            "physics",
            "world war",
            "civilization",
            "economics"
        ]

        if any(word in topic_lower for word in non_coding_keywords):
            is_coding_topic = False

       
        if level == "High School":

            if not grade or not board:
                return "⚠️ For High School, please select both Grade and Education Board."

            
            if is_coding_topic:

                system_msg = (
                    f"You are a {board} school teacher.\n"
                    f"Explain '{topic}' to a {grade} grade student.\n\n"

                    "Rules:\n"
                    "- Use very simple language.\n"
                    "- Explain step-by-step.\n"
                    "- Include:\n"
                    "  1. Introduction\n"
                    "  2. Definition\n"
                    "  3. Important points\n"
                    "  4. Syntax (if applicable)\n"
                    "  5. One simple code example\n"
                    "  6. Conclusion\n"
                    "- Use headings and bullet points.\n"
                    "- Use fenced code blocks for code.\n"
                    "- Keep the explanation beginner-friendly."
                )

            
            else:

                system_msg = (
                    f"You are a {board} school teacher.\n"
                    f"Explain '{topic}' to a {grade} grade student.\n\n"

                    "Rules:\n"
                    "- Use simple and easy language.\n"
                    "- Include:\n"
                    "  1. Introduction\n"
                    "  2. Definition\n"
                    "  3. 3-5 important points\n"
                    "  4. One short real-life example\n"
                    "  5. Conclusion\n"
                    "- If the topic includes a process "
                    "(water cycle, digestion, photosynthesis, etc.), "
                    "explain it step-by-step.\n"
                    "- STRICTLY DO NOT include:\n"
                    "  - Syntax\n"
                    "  - Programming code\n"
                    "  - Coding examples\n"
                    "  - Technical implementation\n"
                    "- Keep the explanation syllabus-appropriate.\n"
                    "- Use Markdown headings and bullet points."
                )

            user_msg = (
                f"Explain '{topic}' for a {grade} grade High School student "
                f"(Board: {board})."
            )

        # =========================
        # GRADUATION
        # =========================
        else:

            # -------------------------
            # Coding Topic
            # -------------------------
            if is_coding_topic:

                system_msg = (
                    f"You are a university professor.\n"
                    f"Explain '{topic}' for a graduation-level student.\n\n"

                    "Rules:\n"
                    "- Provide an in-depth explanation with headings.\n"
                    "- Include:\n"
                    "  1. Introduction\n"
                    "  2. Definition\n"
                    "  3. Syntax\n"
                    "  4. Code examples\n"
                    "  5. Important concepts\n"
                    "  6. Practical applications\n"
                    "  7. Conclusion\n"
                    "- Use fenced code blocks for code.\n"
                    "- Explain technical concepts clearly.\n"
                    "- Keep examples short and runnable."
                )

            # -------------------------
            # Non-Coding Topic
            # -------------------------
            else:

                system_msg = (
                    f"You are a university professor.\n"
                    f"Explain '{topic}' for a graduation-level student.\n\n"

                    "Rules:\n"
                    "- Provide a detailed academic explanation.\n"
                    "- Include:\n"
                    "  1. Introduction\n"
                    "  2. Definition\n"
                    "  3. Key concepts\n"
                    "  4. Historical/scientific/theoretical background\n"
                    "  5. Real-world importance\n"
                    "  6. Conclusion\n"
                    "- STRICTLY DO NOT include:\n"
                    "  - Syntax\n"
                    "  - Programming code\n"
                    "  - Coding examples\n"
                    "  - Software implementation\n"
                    "- Use headings and bullet points.\n"
                    "- Keep the explanation clear and professional."
                )

            user_msg = (
                f"Explain '{topic}' for a Graduation-level student."
            )

        # =========================
        # CREATE MESSAGES
        # =========================
        messages = [
            {"role": "system", "content": system_msg},
            {"role": "user", "content": user_msg}
        ]

        # =========================
        # GET AI RESPONSE
        # =========================
        return get_response(messages)

    except Exception as e:
        return f"⚠️ Error in explanation: {e}"