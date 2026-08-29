from __future__ import annotations

import argparse
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


def upload_streaming_curated_to_s3(
    input_file: str,
    window_id: str,
) -> str:
    input_path = Path(input_file)

    s3_key = (
        f"{S3_PREFIX}/streaming/curated/"
        f"{window_id}/"
        f"{input_path.name}"
    )

    if S3_BUCKET == "your-s3-bucket-name":
        raise ValueError(
            "Please set S3_BUCKET before running this script."
        )

    if not input_path.exists():
        raise FileNotFoundError(
            f"Streaming curated CSV not found: {input_path}"
        )

    if input_path.stat().st_size == 0:
        raise ValueError(
            f"Streaming curated CSV is empty: {input_path}"
        )

    s3_client = boto3.client("s3")

    print(
        f"Uploading {input_path.name}\n"
        f"-> s3://{S3_BUCKET}/{s3_key}"
    )

    s3_client.upload_file(
        Filename=str(input_path),
        Bucket=S3_BUCKET,
        Key=s3_key,
    )

    print(
        "Streaming curated CSV upload completed successfully."
    )

    return f"s3://{S3_BUCKET}/{s3_key}"


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input-file",
        required=True,
    )

    parser.add_argument(
        "--window-id",
        required=True,
    )

    args = parser.parse_args()

    s3_uri = upload_streaming_curated_to_s3(
        input_file=args.input_file,
        window_id=args.window_id,
    )

    print(
        f"Streaming curated CSV uploaded: {s3_uri}"
    )


if __name__ == "__main__":
    main()


if __name__ == "__main__":
    main()