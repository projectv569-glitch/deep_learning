# deep_learning
# Adaptive AI Tutor

An AI-powered adaptive tutor that uses reinforcement learning, machine learning, and natural language processing to provide personalized learning experiences.

## Features
- **Grammar Correction**: Uses NLP models to correct grammar in sentences.
- **Adaptive Difficulty**: Predicts and adjusts the difficulty of questions based on user performance.
- **Interactive Tutor**: Simulates a tutor session for grammar correction and learning.

## Project Structure
adaptive_ai_tutor/ 
├── main_tutor.py 
├── simulate_tutor.py
├── interactive_tutor.py
├── train_ml_model.py 
├── train_rl_agent.py 
├── questions.json 
├── finall.csv 
├── model/ │ 
        ├── next_difficulty_model.pkl 
        │ └── adaptive_difficulty_dqn_v4.zip 
├── src/ │ 
├── rl_env.py │ 
|── nlp_feedback.py │ 
├── spaced_repetition.py │ 
├── data_loader.py │ 
└── predictor.py 
├── tests/ │
├── test_rl_env.py │ 
├── test_nlp_feedback.py │ 
└── test_data_loader.py 
├── README.md 
├── requirements.txt 
└── .gitignore

##Dependencies
pandas
numpy
gymnasium
stable-baselines3
transformers
xgboost
scikit-learn
matplotlib
joblib
torch
