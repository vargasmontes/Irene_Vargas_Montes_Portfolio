import gymnasium as gym
from gymnasium import spaces
import numpy as np
import pandas as pd


class BookRecEnv(gym.Env):
    def __init__(self, df, num_candidates=50):
        super(BookRecEnv, self).__init__()

        self.num_candidates = num_candidates

        top_books = df["book_id"].value_counts().head(num_candidates).index
        self.book_map = {book_id: i for i, book_id in enumerate(top_books)}

        self.df = df[df["book_id"].isin(self.book_map)].copy()
        self.df["action_id"] = self.df["book_id"].map(self.book_map)

        user_stats = self.df.groupby("user_id")["rating"].agg(["mean", "count"])
        self.user_context = {
            uid: np.array(
                [row["mean"] / 5.0, min(row["count"] / 20.0, 1.0)],
                dtype=np.float32,
            )
            for uid, row in user_stats.iterrows()
        }
        self.user_ids = list(self.user_context.keys())

        self.observation_space = spaces.Box(
            low=0.0, high=1.0, shape=(2,), dtype=np.float32
        )
        self.action_space = spaces.Discrete(self.num_candidates)

        self.current_user = None
        self.user_ratings = {}

    def reset(self, seed=None, options=None):
        super().reset(seed=seed)

        self.current_user = np.random.choice(self.user_ids)
        user_df = self.df[self.df["user_id"] == self.current_user]
        self.user_ratings = dict(zip(user_df["action_id"], user_df["rating"]))

        context = self.user_context[self.current_user].copy()
        return context, {}

    def step(self, action):
        if action in self.user_ratings:
            actual_rating = self.user_ratings[action]
            if actual_rating >= 4:
                reward = actual_rating - 3.0
            else:
                reward = actual_rating - 3.5
        else:
            reward = -0.5

        terminated = True
        truncated = False
        context = self.user_context[self.current_user].copy()

        return context, reward, terminated, truncated, {}