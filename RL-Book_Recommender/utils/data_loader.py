import os
import numpy as np
import pandas as pd


def load_goodbooks_data(
    data_dir="data", top_n_books=50, min_user_ratings=10
):
    """Loads ratings.csv, filters for top N books and active users,

    and maps book IDs to contiguous action indices [0, top_n_books - 1].
    """
    ratings_path = os.path.join(data_dir, "ratings.csv")

    if not os.path.exists(ratings_path):
        raise FileNotFoundError(
            f"Could not find ratings.csv in '{data_dir}/'. Please place your Goodbooks-10k CSV files in the data directory."
        )

    df = pd.read_csv(ratings_path)

    # 1. Filter for top N most popular books (bounds action space size)
    top_books = (
        df["book_id"].value_counts().head(top_n_books).index.tolist()
    )
    df_filtered = df[df["book_id"].isin(top_books)].copy()

    # 2. Filter for active users with sufficient interaction history
    user_counts = df_filtered["user_id"].value_counts()
    active_users = user_counts[
        user_counts >= min_user_ratings
    ].index.tolist()
    df_filtered = df_filtered[df_filtered["user_id"].isin(active_users)]

    # 3. Map book_ids to zero-indexed candidate actions [0, top_n_books - 1]
    book_map = {book_id: idx for idx, book_id in enumerate(top_books)}
    df_filtered["action_id"] = df_filtered["book_id"].map(book_map)

    print(
        f"✅ Loaded Goodbooks-10k: {len(df_filtered)} ratings across "
        f"{df_filtered['user_id'].nunique()} users for top {top_n_books} books."
    )
    return df_filtered, book_map