from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json
import random
import pickle

app = Flask(__name__)
app.secret_key = "adaptive_ai_tutor_secret_key"

def load_questions(file_path='questions.json'):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading questions: {e}")
        return []

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/main_tutor', methods=['GET', 'POST'])
def main_tutor():
    if 'current_difficulty' not in session:
        session['current_difficulty'] = "easy"
    if 'user_performance' not in session:
        session['user_performance'] = {"correct": 0, "incorrect": 0}
    if 'language' not in session:
        session['language'] = 'en'

    if request.method == 'POST':
        selected_language = request.form.get('language')
        if selected_language in ['en', 'fr', 'de']:
            session['language'] = selected_language
        return redirect(url_for('main_tutor'))

    questions = load_questions()
    if not questions:
        return render_template('main_tutor.html', error="No questions loaded.")

    filtered_questions = [
        q for q in questions
        if q.get("language") == session['language'] and q.get("difficulty") == session['current_difficulty']
    ]

    if not filtered_questions:
        return render_template('main_tutor.html', error="No questions available for this language/difficulty.")

    question = random.choice(filtered_questions)

    return render_template(
        'main_tutor.html',
        question=question,
        difficulty=session['current_difficulty'],
        performance=session['user_performance'],
        selected_language=session['language']
    )

@app.route('/submit_answer', methods=['POST'])
def submit_answer():
    user_answer = request.form.get('answer', '').strip().lower()
    correct_answer = request.form.get('correct_answer', '').strip().lower()
    tip = request.form.get('tip', 'Review the related topic for better understanding.')

    if 'user_performance' not in session:
        session['user_performance'] = {"correct": 0, "incorrect": 0}

    if user_answer == correct_answer:
        session['user_performance']["correct"] += 1
        feedback = 1
        result = "correct"
    else:
        session['user_performance']["incorrect"] += 1
        feedback = 0
        result = "incorrect"

    correct = session['user_performance']["correct"]
    incorrect = session['user_performance']["incorrect"]
    total = correct + incorrect
    accuracy = (correct / total) * 100 if total > 0 else 0

    if accuracy < 50:
        suggestion = "Focus on reviewing the basics."
    elif accuracy < 80:
        suggestion = "You're doing well! Keep practicing."
    else:
        suggestion = "Excellent! Try harder questions."

    current_difficulty = session.get('current_difficulty', "easy")
    increase = {"easy": "medium", "medium": "hard", "hard": "hard"}
    decrease = {"hard": "medium", "medium": "easy", "easy": "easy"}

    next_difficulty = increase[current_difficulty] if feedback else decrease[current_difficulty]
    session['current_difficulty'] = next_difficulty

    return jsonify({
        'result': result,
        'correct_answer': correct_answer,
        'tip': tip,
        'accuracy': f"{accuracy:.2f}%",
        'suggestion': suggestion,
        'next_difficulty': next_difficulty
    })

@app.route('/reset_main_tutor')
def reset_main_tutor():
    session.pop('current_difficulty', None)
    session.pop('user_performance', None)
    return redirect(url_for('main_tutor'))

if __name__ == '__main__':
    app.run(debug=True)
