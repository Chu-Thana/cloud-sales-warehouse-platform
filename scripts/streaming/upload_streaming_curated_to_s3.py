from __future__ import annotations

import os
from pathlib import Path

import boto3


PROJECT_ROOT = Path(__file__).resolve().parents[2]

S3_BUCKET = os.getenv(
    "S3_BUCKET",
    "your-s3-bucket-name",
)

S3_PREFIX = os.getenv(
    "S3_PREFIX",
    "data-platform/vendor-payments",
)

CURATED_CSV_FILE = (
    PROJECT_ROOT
    / "data"
    / "streaming"
    / "curated"
    / "vendor_payments_streaming_events.csv"
)

S3_KEY = (
    f"{S3_PREFIX}/streaming/curated/"
    f"{CURATED_CSV_FILE.name}"
)


def upload_streaming_curated_to_s3() -> None:
    if S3_BUCKET == "your-s3-bucket-name":
        raise ValueError(
            "Please set S3_BUCKET before running this script."
        )

    if not CURATED_CSV_FILE.exists():
        raise FileNotFoundError(
            f"Streaming curated CSV not found: "
            f"{CURATED_CSV_FILE}"
        )

    if CURATED_CSV_FILE.stat().st_size == 0:
        raise ValueError(
            f"Streaming curated CSV is empty: "
            f"{CURATED_CSV_FILE}"
        )

    s3_client = boto3.client("s3")

    print(
        f"Uploading {CURATED_CSV_FILE.name}\n"
        f"-> s3://{S3_BUCKET}/{S3_KEY}"
    )

    s3_client.upload_file(
        Filename=str(CURATED_CSV_FILE),
        Bucket=S3_BUCKET,
        Key=S3_KEY,
    )

    print(
        "Streaming curated CSV upload completed successfully."
    )


def main() -> None:
    upload_streaming_curated_to_s3()


if __name__ == "__main__":
    main()