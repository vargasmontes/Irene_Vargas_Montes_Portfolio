import pandas as pd


def load_goodbooks_data(data_dir="data", top_n_books=50, min_user_ratings=10):
    ratings = pd.read_csv(f"{data_dir}/ratings.csv")

    # Keep most-rated books
    top_books = ratings["book_id"].value_counts().head(top_n_books).index
    ratings = ratings[ratings["book_id"].isin(top_books)].copy()

    # Drop users with too little signal
    user_counts = ratings["user_id"].value_counts()
    valid_users = user_counts[user_counts >= min_user_ratings].index
    ratings = ratings[ratings["user_id"].isin(valid_users)].copy()

    print(f"Loaded {len(ratings)} ratings, {ratings['user_id'].nunique()} users, "
          f"{ratings['book_id'].nunique()} books")

    return ratings
