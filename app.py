from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json
import random
import time
import os
from transformers import pipeline
import numpy as np
import pickle
import torch
from src.rl_env import AdaptiveLearningEnv
from src.nlp_feedback import correct_grammar
from src.data_loader import load_dataset

app = Flask(__name__)
app.secret_key = "adaptive_ai_tutor_secret_key"  # For session management

# Load questions from JSON file
def load_questions(file_path='questions.json'):
    """Load questions from a JSON file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            questions = json.load(file)
        return questions
    except FileNotFoundError:
        print("❌ Error: Questions file not found.")
        return []
    except json.JSONDecodeError:
        print("❌ Error: Failed to decode JSON file.")
        return []

# Load ML model for predicting next difficulty
def load_ml_model():
    try:
        with open("model/next_difficulty_model.pkl", "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        print("❌ Error: ML model file not found.")
        return None

# Load RL model
def load_rl_model():
    try:
        from stable_baselines3 import DQN
        return DQN.load("model/adaptive_difficulty_dqn_v4.zip")
    except FileNotFoundError:
        print("❌ Error: RL model file not found.")
        return None
    except Exception as e:
        print(f"❌ Error loading RL model: {e}")
        return None

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

# Main Tutor routes
@app.route('/main_tutor', methods=['GET', 'POST'])
def main_tutor():
    if 'current_difficulty' not in session:
        session['current_difficulty'] = "easy"
    if 'user_performance' not in session:
        session['user_performance'] = {"correct": 0, "incorrect": 0}
    if 'language' not in session:
        session['language'] = 'en'  # Default language

    if request.method == 'POST':
        selected_language = request.form.get('language')
        if selected_language in ['en', 'fr', 'de']:
            session['language'] = selected_language
            session.modified = True
        return redirect(url_for('main_tutor'))

    questions = load_questions()
    if not questions:
        return render_template('main_tutor.html', error="No questions loaded. Please check questions.json file.")

    filtered_questions = [q for q in questions if q["language"] == session['language'] and q["difficulty"] == session['current_difficulty']]
    if not filtered_questions:
        return render_template('main_tutor.html', error=f"No questions available for language {session['language']} and difficulty level: {session['current_difficulty']}.")

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
    question_text = request.form.get('question_text', '')
    tip = request.form.get('tip', 'Review the related topic for better understanding.')
    
    # Update user performance
    if 'user_performance' not in session:
        session['user_performance'] = {"correct": 0, "incorrect": 0}
    
    if user_answer == correct_answer:
        session['user_performance']["correct"] += 1
        feedback = 1  # Correct answer
        result = "correct"
    else:
        session['user_performance']["incorrect"] += 1
        feedback = 0  # Incorrect answer
        result = "incorrect"
    
    # Calculate accuracy
    total_attempts = session['user_performance']["correct"] + session['user_performance']["incorrect"]
    accuracy = 0
    suggestion = ""
    if total_attempts > 0:
        accuracy = (session['user_performance']["correct"] / total_attempts) * 100
        if accuracy < 50:
            suggestion = "Focus on reviewing the basics to improve your understanding."
        elif accuracy < 80:
            suggestion = "You're doing well! Keep practicing to reach mastery."
        else:
            suggestion = "Excellent work! Consider trying harder questions for a challenge."
    
    # Adjust difficulty based on feedback
    current_difficulty = session.get('current_difficulty', "easy")
    difficulty_map = {"easy": "medium", "medium": "hard", "hard": "medium"}
    reverse_difficulty_map = {"medium": "easy", "hard": "medium"}
    
    if feedback == 1:  # Correct answer
        next_difficulty = difficulty_map.get(current_difficulty, "medium")
    else:  # Incorrect answer
        next_difficulty = reverse_difficulty_map.get(current_difficulty, "easy")
    
    session['current_difficulty'] = next_difficulty
    session.modified = True
    
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
    session.pop('language', None)  # Reset language to default
    return redirect(url_for('main_tutor'))

# Interactive Tutor routes
@app.route('/interactive_tutor')
def interactive_tutor():
    return render_template('interactive_tutor.html')

@app.route('/correct_grammar', methods=['POST'])
def correct_grammar_route():
    sentence = request.form.get('sentence', '').strip()
    
    if not sentence:
        return jsonify({'error': 'Please enter a valid sentence.'})
    
    try:
        corrected = correct_grammar(sentence)
        return jsonify({
            'original': sentence,
            'corrected': corrected
        })
    except Exception as e:
        return jsonify({'error': f'Error during grammar correction: {str(e)}'})

# Simulate Tutor routes
@app.route('/simulate_tutor')
def simulate_tutor():
    return render_template('simulate_tutor.html')

@app.route('/run_simulation', methods=['POST'])
def run_simulation():
    sentence = request.form.get('sentence', '').strip()
    
    if not sentence:
        return jsonify({'error': 'Please enter a valid sentence.'})
    
    try:
        # Correct grammar
        corrected = correct_grammar(sentence)
        
        # Load models
        ml_model = load_ml_model()
        rl_model = load_rl_model()
        
        if not ml_model or not rl_model:
            return jsonify({
                'original': sentence,
                'corrected': corrected,
                'error': 'Could not load ML or RL models.' 
            })
        
        # Create dummy user features for demonstration
        user_features = [0.2] * 18
        
        # Predict next difficulty using ML model
        predicted_difficulty = ml_model.predict([user_features])[0]
        
        # Use RL model to decide difficulty level
        env = AdaptiveLearningEnv()
        obs, _ = env.reset()  # Unpack the tuple properly
        
        # Predict action from model
        action, _ = rl_model.predict(obs)
        if isinstance(action, np.ndarray):
            action = int(action.item())
        
        action_map = {0: "EASIER", 1: "SAME", 2: "HARDER"}
        action_result = action_map[action]
        
        return jsonify({
            'original': sentence,
            'corrected': corrected,
            'predicted_difficulty': f"{float(predicted_difficulty):.2f}",
            'rl_suggestion': action_result
        })
    except Exception as e:
        return jsonify({
            'original': sentence,
            'corrected': corrected if 'corrected' in locals() else None,
            'error': f'Error during simulation: {str(e)}'
        })

if __name__ == '__main__':
    app.run(debug=True)
