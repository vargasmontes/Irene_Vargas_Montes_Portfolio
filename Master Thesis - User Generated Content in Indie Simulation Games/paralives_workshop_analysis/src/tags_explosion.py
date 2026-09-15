"""
Expands the tags column into separate rows.

Parameters:
- df: pandas DataFrame containing the workshop data.
- output_path: Path to save the exploded tags DataFrame.

Returns:
- pandas DataFrame with exploded tags.
"""

from pathlib import Path
import pandas as pd

def explode_tags(df, output_path=Path(__file__).parent.parent / "data" / "paralives_tags_exploded.csv"):
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    df = df[["id", "tags"]].copy()
    df = df[df["tags"].notna() & (df["tags"] != "")]
    
    df["tags"] = df["tags"].str.split(",")
    df["tags"] = df["tags"].apply(
        lambda tags: [t.strip() for t in tags] if isinstance(tags, list) else tags
    )

    # Remove the main tags from each item that has more than one
    def filter_tags(tags):
        main_tags = {"Paramaker", "Build Mode", "Live Mode", "Mod", "Modpacks"}
        if not isinstance(tags, list):
                return []
        if len(tags) > 1:
            filtered = [t for t in tags if t not in main_tags]
            return filtered if filtered else tags
        return tags

    df["tags"] = df["tags"].apply(filter_tags)

    df = df.explode("tags")
    df["tags"] = df["tags"].str.strip()
    df = df[df["tags"].notna() & (df["tags"] != "")]

    df.columns = ["id", "tag"]

    df.to_csv(output_path, index=False)
    print(f"Exploded tags saved to {output_path}.")
    return df

if __name__ == "__main__":
     input_df = pd.read_csv("data/paralives_workshop_data.csv")
     explode_tags(input_df)
