import boto3
from pathlib import Path

# config
BUCKET_NAME = "sales-analytics-lakehouse-thana"  
LOCAL_FILE = Path("data/sample/superstore_cleaned.parquet")
S3_KEY = "raw/batch/superstore/superstore_cleaned.parquet"

def main():
    print("🚀 Connecting to S3...")
    s3 = boto3.client("s3")

    print("📤 Uploading file...")
    s3.upload_file(str(LOCAL_FILE), BUCKET_NAME, S3_KEY)

    print(f"✅ Uploaded to s3://{BUCKET_NAME}/{S3_KEY}")

if __name__ == "__main__":
    main()