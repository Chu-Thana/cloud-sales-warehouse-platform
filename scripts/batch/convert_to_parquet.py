import pandas as pd
from pathlib import Path

# path
INPUT_PATH = Path("data/sample/superstore_cleaned.csv")
OUTPUT_PATH = Path("data/sample/superstore_cleaned.parquet")

def main():
    print("📥 Reading CSV...")
    df = pd.read_csv(INPUT_PATH)

    print(f"Rows: {len(df)}")

    print("🔄 Converting to Parquet...")
    df.to_parquet(OUTPUT_PATH, index=False)

    print(f"✅ Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()