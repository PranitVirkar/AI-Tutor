import json
import os
from datetime import datetime

LEADERBOARD_FILE = os.path.join(os.path.dirname(__file__), 'leaderboard.json')

def save_result(name, result, topics, grade):
    entry = {
        "player_name": name,
        "score": result.get("score", 0),
        "total_questions": result.get("total_questions", 0),
        "percentage": (result.get("score", 0) / result.get("total_questions", 1)) * 100 if result.get("total_questions", 0) > 0 else 0,
        "time_taken": round(result.get("time_taken", 0), 2),
        "topics": ", ".join(topics) if isinstance(topics, list) else topics,
        "grade": grade,
        "timestamp": datetime.now().isoformat()
    }

    leaderboard = []
    if os.path.exists(LEADERBOARD_FILE):
        try:
            with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
                leaderboard = json.load(f)
        except (json.JSONDecodeError, IOError):
            leaderboard = []

    leaderboard.append(entry)

    with open(LEADERBOARD_FILE, "w", encoding="utf-8") as f:
        json.dump(leaderboard, f, indent=4)

def show_leaderboard():
    if not os.path.exists(LEADERBOARD_FILE):
        print("No leaderboard data found yet.")
        return

    try:
        with open(LEADERBOARD_FILE, "r", encoding="utf-8") as f:
            leaderboard = json.load(f)
    except (json.JSONDecodeError, IOError):
        print("Error reading leaderboard data.")
        return

    if not leaderboard:
        print("Leaderboard is empty.")
        return

    # Sort entries by: (1) percentage descending, (2) time_taken ascending
    sorted_board = sorted(leaderboard, key=lambda x: (-x.get("percentage", 0), x.get("time_taken", float('inf'))))

    print("\n--- 🏆 LEADERBOARD 🏆 ---")
    print(f"{'Rank':<6} | {'Name':<15} | {'Score':<7} | {'%':<5} | {'Time (s)':<8} | {'Topic(s)':<20} | {'Grade':<8} | {'Date':<10}")
    print("-" * 105)

    for i, entry in enumerate(sorted_board):
        rank = i + 1
        rank_str = str(rank)
        if rank == 1:
            rank_str += " 🥇"
        elif rank == 2:
            rank_str += " 🥈"
        elif rank == 3:
            rank_str += " 🥉"

        name = str(entry.get('player_name', 'Unknown'))[:15]
        score = f"{entry.get('score', 0)}/{entry.get('total_questions', 0)}"
        percentage = f"{entry.get('percentage', 0):.1f}"
        time_taken = f"{entry.get('time_taken', 0):.2f}"
        topics = str(entry.get('topics', ''))[:20]
        grade = str(entry.get('grade', ''))[:8]
        date_str = entry.get('timestamp', '').split('T')[0] if 'timestamp' in entry else ''

        # Handling emojis width in alignment could be tricky, but basic string length padding is fine for terminals
        print(f"{rank_str:<6} | {name:<15} | {score:<7} | {percentage:<5} | {time_taken:<8} | {topics:<20} | {grade:<8} | {date_str:<10}")
    print("-" * 105 + "\n")
