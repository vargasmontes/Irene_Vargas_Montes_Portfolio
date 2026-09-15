"""
Extracts keywords from the 'description' column of the DataFrame using TF-IDF.
Saves the exploded keywords dataset to a CSV file.

Parameters:
- df: pandas DataFrame containing the workshop data.
- output_path: Path to save the exploded keywords dataset.
"""

import pandas as pd
from pathlib import Path
from sklearn.feature_extraction.text import TfidfVectorizer

def extract_keywords(df, output_path=Path(__file__).parent.parent / "data" / "keywords_extracted.csv"):
    df["description"] = df["description"].fillna("").astype(str)

    # Configure TF-IDF
    vectorizer = TfidfVectorizer(
        stop_words="english",
        ngram_range=(1, 2),
        max_features=5000,
    )

    # Generate TF-IDF matrix
    tfidf_matrix = vectorizer.fit_transform(df["description"])
    feature_names = vectorizer.get_feature_names_out()

    # Keywords extraction
    def extract_row_keywords(matrix, features, top_n=5):
        keywords_list = []
        for row in matrix.toarray():
            top_indices = row.argsort()[-top_n:][::-1]
            top_words = [features[i] for i in top_indices if row[i] > 0]
            keywords_list.append(top_words) 
        return keywords_list

    df["keywords"] = extract_row_keywords(tfidf_matrix, feature_names, top_n=5)

    id_col = "ID" if "ID" in df.columns else "id"
    output_df = df[[id_col, "keywords"]].explode("keywords")

    # No empty rows or whitespace
    output_df = output_df.dropna(subset=["keywords"])
    output_df["keywords"] = output_df["keywords"].str.strip()
    output_df = output_df[output_df["keywords"] != ""]

    output_df.to_csv(output_path, index=False)

    print(f"Keywords saved to '{output_path}'.")
    return output_df

if __name__ == "__main__":
    input_df = pd.read_csv("data/paralives_workshop_data.csv")
    extract_keywords(input_df)
