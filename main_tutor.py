import json
import random
import time

def load_questions(file_path=r'questions.json'):
    """
    Load questions from a JSON file.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:  # Specify UTF-8 encoding
            questions = json.load(file)
        return questions
    except FileNotFoundError:
        print("❌ Error: Questions file not found.")
        return []
    except json.JSONDecodeError:
        print("❌ Error: Failed to decode JSON file.")
        return []

def ask_question(questions, current_difficulty, user_performance):
    """
    Ask a question based on the current difficulty level and provide personalized suggestions.
    """
    if not questions:
        print("⚠️ No questions available.")
        return current_difficulty

    # Filter questions by difficulty
    filtered_questions = [q for q in questions if q["difficulty"] == current_difficulty]
    if not filtered_questions:
        print(f"⚠️ No questions available for difficulty level: {current_difficulty}.")
        return current_difficulty

    question = random.choice(filtered_questions)
    print(f"\n🧠 Difficulty: {current_difficulty}")
    print("🧠 Question:")
    print(question["question"])
    for option in question["options"]:
        print(option)

    # Start timing
    start_time = time.time()

    user_answer = input("\nYour answer (e.g., a, b, c, d): ").strip().lower()

    # End timing
    end_time = time.time()
    time_taken = end_time - start_time
    print(f"⏱️ Time taken: {time_taken:.2f} seconds")

    if user_answer == question["answer"]:
        print("✅ Correct!")
        print("💡 Tip: Great job! Keep up the good work.")
        user_performance["correct"] += 1
        feedback = 1  # Correct answer
    else:
        print(f"❌ Incorrect. The correct answer is: {question['answer']}")
        print(f"💡 Tip: {question.get('tip', 'Review the related topic for better understanding.')}")
        user_performance["incorrect"] += 1
        feedback = 0  # Incorrect answer

    # Provide personalized suggestions
    total_attempts = user_performance["correct"] + user_performance["incorrect"]
    if total_attempts > 0:
        accuracy = (user_performance["correct"] / total_attempts) * 100
        print(f"\n📊 Your accuracy so far: {accuracy:.2f}%")
        if accuracy < 50:
            print("🔍 Suggestion: Focus on reviewing the basics to improve your understanding.")
        elif accuracy < 80:
            print("👍 Suggestion: You're doing well! Keep practicing to reach mastery.")
        else:
            print("🌟 Suggestion: Excellent work! Consider trying harder questions for a challenge.")

    # Adjust difficulty based on feedback
    difficulty_map = {"easy": "medium", "medium": "hard", "hard": "medium"}
    if feedback == 1:  # Correct answer
        next_difficulty = difficulty_map.get(current_difficulty, "medium")
    else:  # Incorrect answer
        reverse_difficulty_map = {"medium": "easy", "hard": "medium"}
        next_difficulty = reverse_difficulty_map.get(current_difficulty, "easy")

    # Display the next predicted difficulty level
    print(f"\n🔮 The next question will be at '{next_difficulty}' difficulty.")

    return next_difficulty

def main():
    print("Welcome to the Adaptive AI Tutor!")

    # Load questions from JSON
    questions = load_questions(
        r'questions.json')  # Adjust the path if needed

    if not questions:
        print("⚠️ No questions loaded. Exiting.")
        return

    # Start with an initial difficulty level
    current_difficulty = "easy"
    user_performance = {"correct": 0, "incorrect": 0}  # Track user performance

    while True:
        # Ask a question and get the next difficulty level
        current_difficulty = ask_question(questions, current_difficulty, user_performance)

        # Exit option
        choice = input("\n❓ Do you want to answer another question? (y/n): ").strip().lower()
        if choice != 'y':
            print("👋 Goodbye!")
            break

if __name__ == "__main__":
    main()
