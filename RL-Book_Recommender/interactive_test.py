from envs.book_rec_env import BookRecEnv
from utils.data_loader import load_goodbooks_data
import pandas as pd
import os
from stable_baselines3 import DQN


def interactive_session(top_n_books=50):
    print("Loading Goodbooks-10k dataset...")
    data = load_goodbooks_data(top_n_books=top_n_books, min_user_ratings=10)

    env = BookRecEnv(df=data, num_candidates=top_n_books)
    book_map = env.book_map
    inv_book_map = {v: k for k, v in book_map.items()}

    script_dir = os.path.dirname(os.path.abspath(__file__))
    books_path = os.path.join(script_dir, "data", "books.csv")
    books_df = pd.read_csv(books_path)

    def get_book_title(action_id):
        raw_book_id = inv_book_map[action_id]
        match = books_df[books_df["book_id"] == raw_book_id]
        return match.iloc[0]["title"] if not match.empty else f"Book #{raw_book_id}"

    print("\nTraining DQN agent for testing...")
    model = DQN("MlpPolicy", env, verbose=0, learning_rate=1e-3)
    model.learn(total_timesteps=5000)

    print("\n" + "=" * 50)
    print(" 📚 INTERACTIVE BOOK RECOMMENDER TEST ")
    print("=" * 50)
    print("Each round, the agent recommends a book to a real, sampled user")
    print("from the dataset. You can rate it too, just to compare your taste")
    print("against that user's actual historical rating.")
    print("Type 'q' to quit at any time.\n")

    for round_num in range(1, 11):
        obs, _ = env.reset()
        action, _ = model.predict(obs, deterministic=True)
        action = int(action)
        book_title = get_book_title(action)

        print(f"\n[Round {round_num}/10] User context (avg rating, activity): {obs}")
        print(f"📖  \033[1m{book_title}\033[0m")

        _, reward, _, _, _ = env.step(action)
        print(f"-> That sampled user's actual reaction (reward signal): {reward:+.1f}")

        user_input = input("Your own rating, just for comparison (1-5, or 'q' to quit): ").strip()
        if user_input.lower() == "q":
            print("Exiting session.")
            break
        try:
            rating = max(1.0, min(5.0, float(user_input)))
            print(f"-> You rated it {rating}⭐")
        except ValueError:
            print("Invalid input, skipping.")

    print("\n================ Session Complete ================")


if __name__ == "__main__":
    interactive_session(top_n_books=50)
