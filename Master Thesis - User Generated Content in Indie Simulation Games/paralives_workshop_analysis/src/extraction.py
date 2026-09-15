"""
Extraction functions for fetching and parsing workshop data from the Steam API.
"""
import pandas as pd
import requests
from dotenv import load_dotenv
import os
import time
from pathlib import Path

parent_dir = Path(__file__).parent.parent

# Load API key & select game
env_path = parent_dir / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("STEAM_API_KEY")
APP_ID = 1118520

data_dir = parent_dir / "data"
data_dir.mkdir(parents=True, exist_ok=True)
output_file = data_dir / "paralives_workshop_data.csv"

def parse_item(item):
    """
    Parses a single workshop item from the Steam API response into a structured dictionary.
    """
    tags = item.get("tags", [])
    tag_list = [t["tag"] for t in tags]
    
    current_subs = item.get("subscriptions", 0)             
    lifetime_subs = item.get("lifetime_subscriptions", 0)   
    current_favs = item.get("favorited", 0)                 
    lifetime_favs = item.get("lifetime_favorited", 0)       
    views = item.get("views", 0)                            
    votes_up = item.get("vote_data", {}).get("votes_up", 0)         
    votes_down = item.get("vote_data", {}).get("votes_down", 0)     
    total_votes = votes_up + votes_down                             

    return {
        "id":                    item.get("publishedfileid"),
        "creator_id":            item.get("creator"),
        "title":                 item.get("title"),
        "description":           item.get("short_description", ""),
        "tags":                  ", ".join(tag_list),
        "file_size_kb":          round(int(item.get("file_size", 0)) / 1024, 2),
        "created_date":          pd.to_datetime(item.get("time_created"), unit="s"),
        "updated_date":          pd.to_datetime(item.get("time_updated"), unit="s"),
        "update_count":          item.get("revision_change_number", 0),
        "subscriptions":         current_subs,
        "lifetime_subscriptions": lifetime_subs,
        "sub_churn":             lifetime_subs - current_subs,
        "favourites":            current_favs,
        "lifetime_favourites":   lifetime_favs,
        "fav_churn":             lifetime_favs - current_favs,
        "views":                 views,
        "conversion_rate_pct":   round(current_subs / views * 100, 2) if views > 0 else 0,
        "comments":              item.get("num_comments_public", 0),
        "num_dependencies":      item.get("num_children", 0),
        "votes_up":              votes_up,
        "votes_down":            votes_down,
        "upvote_ratio_pct":      round(votes_up / total_votes * 100, 2) if total_votes > 0 else 0,
        "vote_score":            item.get("vote_data", {}).get("score", 0),
        "has_adult_content":     item.get("maybe_inappropriate_sex", False),
    }

def fetch_and_parse():
    """
    Fetches the workshop data from the Steam API.
    """
    url = "https://api.steampowered.com/IPublishedFileService/QueryFiles/v1/"
    all_parsed = []
    cursor = "*"
    page = 1

    while True:
        print(f"Fetching page {page} ({len(all_parsed)} items so far)...")

        params = {
            "key": API_KEY,
            "appid": APP_ID,
            "query_type": 0,
            "numperpage": 100,
            "cursor": cursor,
            "return_vote_data": True,
            "return_tags": True,
            "return_short_description": True,
            "return_children": True,    
        }

        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
            data = response.json()["response"]
        except Exception as e:
            print(f"Error on page {page}: {e}")
            print("Waiting 10 seconds before retrying...")
            time.sleep(10)
            continue

        items = data.get("publishedfiledetails", [])

        if not items:
            print("Status: No more items, finished.")
            break

        for item in items:
            all_parsed.append(parse_item(item))

        next_cursor = data.get("next_cursor")
        if not next_cursor or next_cursor == cursor:
            print("Status: Last page, finished.")
            break

        cursor = next_cursor
        page += 1
        time.sleep(0.5)

    df = pd.DataFrame(all_parsed)
    
    # Add primary_tag
    df["tags"] = df["tags"].fillna("Untagged")
    df["primary_tag"] = df["tags"].str.split(",").str[0].str.strip()

    df.to_csv(output_file, index=False)

   # Provide information about the process: 
    print(f"Parsed through {page} pages to collect {len(df)} items. Saved in {output_file}.")

    return df

if __name__ == "__main__":
    df = fetch_and_parse()
