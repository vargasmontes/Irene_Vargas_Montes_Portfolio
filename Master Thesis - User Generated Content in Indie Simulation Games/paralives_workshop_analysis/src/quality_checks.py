"""
Runs quality checks on the DataFrame and prints a summary of the results.

Parameters:
- df: pandas DataFrame containing the workshop data.
"""
import pandas as pd

def run_check(df):
    print("\n--- Summary of Data Quality for paralives_workshop_data.csv ---")

    # Duplicated Items
    duplicates = df[df.duplicated(subset=['id'])]
    print(f"· Uniqueness: ")
    print(f"    Duplicated items: {len(duplicates)} ({len(duplicates)/len(df)*100:.2f}%)")

    # Completeness
    print(f"\n· Completeness:")
    missing_title = df[df["title"].isna() | (df["title"].str.strip() == "")]
    print(f"    Items missing Title: {len(missing_title)} ({len(missing_title)/len(df)*100:.2f}%)")

    missing_description = df[df["description"].isna() | (df["description"].str.strip() == "")]
    print(f"    Items missing Description: {len(missing_description)} ({len(missing_description)/len(df)*100:.2f}%)")

    missing_tag = df[df["tags"].isna() | (df["tags"].str.strip() == "")] 
    print(f"    Items missing Tags: {len(missing_tag)} ({len(missing_tag)/len(df)*100:.2f}%)")

    # Timeliness
    last_refresh = str(df["created_date"].max())
    print(f"\n· Timeliness:")
    print(f"    Last Refresh Date: {last_refresh[:10]}")

    return duplicates, missing_title, missing_description, missing_tag, last_refresh

if __name__ == "__main__":
    input_df = pd.read_csv("data/paralives_workshop_data.csv")
    run_check(input_df)
