"""
Main pipeline for Paralives Workshop Analysis.
Runs extraction, cleaning, and enrichment steps in sequence.
"""
from src import extraction, tags_explosion, keywords_extraction, roadmap_tracker, quality_checks

def main():
    print("\nSTEP 1: Extracting workshop data from Steam API.")
    df = extraction.fetch_and_parse()

    print("\nSTEP 2: Checking data quality.")
    quality_checks.run_check(df)

    print("\nSTEP 3: Exploding tags.")
    tags_explosion.explode_tags(df)

    print("\nSTEP 4: Extracting keywords from descriptions.")
    keywords_extraction.extract_keywords(df)

    print("\nSTEP 5: Building roadmap tracker dataset.")
    roadmap_tracker.build_tracker(df)

    print("\nPIPELINE COMPLETE")

if __name__ == "__main__":
    main()
