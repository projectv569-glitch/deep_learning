# File: src/train_rl_agent.py
import os
import matplotlib.pyplot as plt
from stable_baselines3 import DQN
from stable_baselines3.common.callbacks import BaseCallback
from rl_env import AdaptiveLearningEnv

# Path to save the trained model (relative to project root)
SAVE_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), '..', 'model', 'adaptive_difficulty_dqn_v4.zip')
)

class HistoryCallback(BaseCallback):
    def __init__(self, verbose=0):
        super().__init__(verbose)

    def _on_step(self) -> bool:
        # Access the VecEnv and unwrap the Monitor wrapper to the base env
        vec_env = self.training_env
        wrapped_env = vec_env.envs[0]
        # Unwrap Monitor or any other wrappers
        if hasattr(wrapped_env, 'env'):
            base_env = wrapped_env.env
        else:
            base_env = wrapped_env
        # Append (difficulty, reward) from the base env
        base_env.history.append((base_env.current_difficulty, base_env.last_reward))
        return True


def train():
    print("⚙️ Initializing Environment...")
    env = AdaptiveLearningEnv()

    print("🚀 Starting Training...")
    model = DQN(policy='MlpPolicy', env=env, verbose=1)
    callback = HistoryCallback()

    model.learn(total_timesteps=5000, callback=callback)

    # Ensure 'model' directory exists
    os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)
    model.save(SAVE_PATH)
    print(f"✅ Model saved at {SAVE_PATH}")

    # Visualize training history from the base env
    # Access the history directly from the unwrapped env
    history = env.history
    if not history:
        print("❌ No training data to visualize.")
        return

    difficulties, rewards = zip(*history)
    plt.figure(figsize=(10, 5))
    plt.plot(difficulties, label="Difficulty")
    plt.plot(rewards, label="Reward")
    plt.xlabel("Step")
    plt.ylabel("Value")
    plt.title("Training History: Difficulty & Reward over Time")
    plt.legend()
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    train()

