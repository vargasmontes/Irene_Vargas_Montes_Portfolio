import csv, os

from envs.book_rec_env import BookRecEnv
from utils.data_loader import load_goodbooks_data
from stable_baselines3 import DQN

# 1. Load real Goodbooks-10k data
data = load_goodbooks_data(data_dir="data", top_n_books=50, min_user_ratings=10)

# 2. Instantiate RL Environment (contextual bandit: 1 step per episode)
env = BookRecEnv(df=data, num_candidates=50)

# 3. Train
print("Training DQN Recommendation Agent...")
model = DQN("MlpPolicy", env, verbose=1, learning_rate=1e-3, buffer_size=10000)
model.learn(total_timesteps=5000)

# 4. Evaluate over several episodes (one recommendation each) and average
n_eval_episodes = 100
total_reward = 0
for _ in range(n_eval_episodes):
    obs, _ = env.reset()
    action, _ = model.predict(obs, deterministic=True)
    obs, reward, terminated, truncated, _ = env.step(int(action))
    total_reward += reward

dqn_score = total_reward / n_eval_episodes
print(f"\nAverage reward per recommendation over {n_eval_episodes} episodes: {dqn_score:.2f}")

# 5. Baseline comparison 
def evaluate_baseline(env, policy_fn, n_episodes=100):
    total_reward = 0
    for _ in range(n_episodes):
        obs, _ = env.reset()
        action = policy_fn(env, obs)
        _, reward, _, _, _ = env.step(action)
        total_reward += reward
    return total_reward / n_episodes

most_popular_action = data["book_id"].map(env.book_map).value_counts().idxmax()
popular_score = evaluate_baseline(env, lambda e, o: most_popular_action)
random_score = evaluate_baseline(env, lambda e, o: env.action_space.sample())

print(f"Most-popular baseline: {popular_score:.2f}")
print(f"Random baseline:       {random_score:.2f}")
print(f"DQN agent:             {dqn_score:.2f}")

# 6. Log results to CSV
row = {"run_label": "50-popular-books", "dqn": dqn_score, "popularity": popular_score, "random": random_score}
csv_path = "outputs/results_log.csv"
file_exists = os.path.exists(csv_path)
with open(csv_path, "a", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=row.keys())
    if not file_exists:
        writer.writeheader()
    writer.writerow(row)
