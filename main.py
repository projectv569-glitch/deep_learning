import os
from stable_baselines3 import DQN
from rl_env import AdaptiveLearningEnv
import matplotlib.pyplot as plt

MODEL_PATH = "model/adaptive_difficulty_dqn_v4.zip"

def load_and_test_model():
    env = AdaptiveLearningEnv()

    if not os.path.exists(MODEL_PATH):
        print(f"❌ Model not found at {MODEL_PATH}")
        return

    model = DQN.load(MODEL_PATH)

    total_rewards = []
    for episode in range(10):
        # 👉 Unpack reset()
        obs, _ = env.reset()
        done = False
        total_reward = 0

        while not done:
            action, _states = model.predict(obs)
            # 👉 Unpack all five returns from step()
            obs, reward, terminated, truncated, info = env.step(action)
            done = terminated or truncated
            total_reward += reward

        total_rewards.append(total_reward)

    avg_reward = sum(total_rewards) / len(total_rewards)
    print(f"✅ Average reward over 10 episodes: {avg_reward}")

    plt.figure(figsize=(10, 5))
    plt.plot(total_rewards, label="Total Rewards per Episode")
    plt.xlabel("Episode")
    plt.ylabel("Reward")
    plt.title("Model Testing - Rewards per Episode")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    load_and_test_model()
