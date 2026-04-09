from pathlib import Path
import pandas as pd

INPUT_PATH = Path("data/sample/superstore_cleaned.csv")
OUTPUT_PATH = Path("data/sample/superstore_cleaned.parquet")

def main():
    print("📥 Reading CSV...")
    df = pd.read_csv(INPUT_PATH)

    print(f"Rows: {len(df)}")

    # force schema ให้ตรงกับ Redshift table
    df["row_id"] = df["row_id"].astype("int64")
    df["order_id"] = df["order_id"].astype("string")
    df["order_date"] = pd.to_datetime(df["order_date"]).dt.normalize()
    df["ship_date"] = pd.to_datetime(df["ship_date"]).dt.normalize()
    df["ship_mode"] = df["ship_mode"].astype("string")
    df["customer_id"] = df["customer_id"].astype("string")
    df["customer_name"] = df["customer_name"].astype("string")
    df["segment"] = df["segment"].astype("string")
    df["country"] = df["country"].astype("string")
    df["city"] = df["city"].astype("string")
    df["state"] = df["state"].astype("string")
    df["postal_code"] = df["postal_code"].astype("string")
    df["region"] = df["region"].astype("string")
    df["product_id"] = df["product_id"].astype("string")
    df["category"] = df["category"].astype("string")
    df["sub_category"] = df["sub_category"].astype("string")
    df["product_name"] = df["product_name"].astype("string")
    df["sales"] = pd.to_numeric(df["sales"]).astype("float64")
    df["quantity"] = df["quantity"].astype("int64")
    df["discount"] = pd.to_numeric(df["discount"]).astype("float64")
    df["profit"] = pd.to_numeric(df["profit"]).astype("float64")
    df["flag_negative_profit"] = df["flag_negative_profit"].astype("bool")
    df["flag_high_discount"] = df["flag_high_discount"].astype("bool")

    print(df.dtypes)

    print("🔄 Converting to Parquet...")
    df.to_parquet(OUTPUT_PATH, index=False)

    print(f"✅ Saved to {OUTPUT_PATH}")

if __name__ == "__main__":
    main()