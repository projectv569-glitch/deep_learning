import numpy as np
import torch
import pickle
from stable_baselines3 import DQN
from src.rl_env import AdaptiveLearningEnv
from src.nlp_feedback import correct_grammar

# Load ML model for predicting next difficulty
with open("model/next_difficulty_model.pkl", "rb") as f:
    ml_model = pickle.load(f)

# Load RL model
rl_model = DQN.load("model/adaptive_difficulty_dqn_v4.zip")

def simulate_tutor_session(user_features, sentence):
    print("\n✍️  Grammar Correction:")
    print(f"  Original : {sentence}")
    print(f"  Corrected: {correct_grammar(sentence)}")

    # Predict next difficulty using ML model
    predicted_difficulty = ml_model.predict([user_features])[0]
    print(f"\n🔮 Predicted Next Difficulty: {predicted_difficulty:.2f}")

    # Use RL model to decide difficulty level
    env = AdaptiveLearningEnv()
    obs, _ = env.reset()  # ✅ Unpack the tuple properly

    # Predict action from model
    action, _ = rl_model.predict(obs)
    if isinstance(action, np.ndarray):  # Fix for unhashable numpy array
        action = int(action.item())

    action_map = {0: "EASIER", 1: "SAME", 2: "HARDER"}
    print(f"🤖 RL Suggests to make it: **{action_map[action]}**")

if __name__ == "__main__":
    user_features = [0.2] * 18  # Dummy features matching model input size
    sentence = "He go to school every day"
    simulate_tutor_session(user_features, sentence)



