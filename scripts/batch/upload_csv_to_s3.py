import boto3
from pathlib import Path
from datetime import datetime

BUCKET_NAME = "sales-analytics-lakehouse-thana"
LOCAL_FILE = Path("data/sample/superstore_cleaned.csv")

def main():
    ingestion_date = datetime.now().strftime("%Y-%m-%d")
    s3_key = f"raw/batch/superstore/ingestion_date={ingestion_date}/superstore_cleaned.csv"

    s3 = boto3.client("s3")
    s3.upload_file(str(LOCAL_FILE), BUCKET_NAME, s3_key)

    print(f"Uploaded to s3://{BUCKET_NAME}/{s3_key}")

if __name__ == "__main__":
    main()