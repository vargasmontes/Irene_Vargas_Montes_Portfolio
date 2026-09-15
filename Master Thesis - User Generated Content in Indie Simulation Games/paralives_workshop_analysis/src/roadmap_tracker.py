"""
Build a roadmap tracker dataset based on workshop item descriptions and predefined keywords.
"""
import pandas as pd
from pathlib import Path 

def build_tracker(df, output_path=Path(__file__).parent.parent / "data" / "paralives_roadmap_tracker.csv"):
    roadmap = [
        # IN GAME at launch
        {"feature": "Build Mode",         "category": "Build Mode",  "status": "In Game",         "keywords": ["furniture", "decor", "architectural", "door", "window", "roof", "wall", "floor"]},
        {"feature": "Paramaker",          "category": "Paramaker",   "status": "In Game",         "keywords": ["clothing", "hair", "tattoo", "skin", "makeup", "accessory", "outfit"]},
        {"feature": "Live Mode",          "category": "Live Mode",   "status": "In Game",         "keywords": ["interaction", "animation", "skill", "emotion", "career", "job", "need"]},
        {"feature": "Open World Town",    "category": "Live Mode",   "status": "In Game",         "keywords": ["town", "lot", "house", "residence", "household"]},
        {"feature": "Personality Traits", "category": "Live Mode",   "status": "In Game",         "keywords": ["trait", "personality", "character"]},
        {"feature": "Steam Workshop",     "category": "General",     "status": "In Game",         "keywords": ["mod", "modpack", "workshop"]},

        # Q4 2026 — First major update
        {"feature": "Live Mode Improvements", "category": "Live Mode", "status": "Q4 2026",       "keywords": ["phone", "chat", "shop", "activity", "orientation"]},
        {"feature": "More Traits & Emotions", "category": "Live Mode", "status": "Q4 2026",       "keywords": ["emotion", "want", "trait", "moodlet"]},
        {"feature": "More Jobs",              "category": "Live Mode", "status": "Q4 2026",       "keywords": ["job", "career", "occupation", "work"]},
        {"feature": "Bug Fixes & Polish",     "category": "General",   "status": "Q4 2026",       "keywords": ["fix", "bug", "glitch", "patch", "update"]},

        # WITHIN 2 YEARS
        {"feature": "Weather & Seasons",  "category": "Live Mode",   "status": "Within 2 Years", "keywords": ["weather", "season", "rain", "snow", "winter", "summer"]},
        {"feature": "Pets",               "category": "Live Mode",   "status": "Within 2 Years", "keywords": ["pet", "dog", "cat", "horse", "animal"]},
        {"feature": "Vehicles",           "category": "Live Mode",   "status": "Within 2 Years", "keywords": ["car", "bike", "vehicle", "boat"]},
        {"feature": "Pools & Swimming",   "category": "Build Mode",  "status": "Within 2 Years", "keywords": ["pool", "swimming", "swim"]},
        {"feature": "Gardening & Fishing","category": "Live Mode",   "status": "Within 2 Years", "keywords": ["garden", "plant", "flower", "fish", "pond"]},
        {"feature": "Social Events",      "category": "Live Mode",   "status": "Within 2 Years", "keywords": ["wedding", "party", "event", "calendar"]},
        {"feature": "Family Tree",        "category": "Live Mode",   "status": "Within 2 Years", "keywords": ["family tree", "genealogy", "ancestor"]},
        {"feature": "Story Progression",  "category": "Live Mode",   "status": "Within 2 Years", "keywords": ["story", "progression", "npc", "townie"]},
        {"feature": "Town Editing Tools", "category": "Build Mode",  "status": "Within 2 Years", "keywords": ["town", "edit", "create", "world"]},
        {"feature": "Boats & Houseboats", "category": "Build Mode",  "status": "Within 2 Years", "keywords": ["boat", "houseboat", "water"]},
    ]

    results = []
    for item in roadmap:
        pattern = "|".join([r"\b" + kw + r"\b" for kw in item["keywords"]])
        mask = df["description"].str.lower().str.contains(pattern, na=False, regex=True)
        matching = df[mask]

        results.append({
            "feature":            item["feature"],
            "category":           item["category"],
            "status":             item["status"],
            "workshop_items":     len(matching),
            "avg_subscriptions":  round(matching["subscriptions"].mean(), 0) if len(matching) > 0 else 0,
            "total_subscriptions": matching["subscriptions"].sum(),
            "community_interest": round(len(matching) * matching["subscriptions"].mean(), 0) if len(matching) > 0 else 0,
        })

    roadmap_df = pd.DataFrame(results)

    # Sorting
    status_order = {"In Game": 1, "Q4 2026": 2, "Within 2 Years": 3}
    roadmap_df["status_order"] = roadmap_df["status"].map(status_order)
    roadmap_df = roadmap_df.sort_values(["status_order", "community_interest"], ascending=[True, False])

    roadmap_df.to_csv(output_path, index=False)
    print(f"Tracker saved to {output_path}.")
    return roadmap_df

if __name__ == "__main__":
    input_df = pd.read_csv("data/paralives_workshop_data.csv")
    build_tracker(input_df)
