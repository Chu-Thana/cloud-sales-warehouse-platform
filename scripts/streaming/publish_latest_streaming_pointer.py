from __future__ import annotations

import argparse
import json
import os

import boto3


AWS_REGION = os.getenv(
    "AWS_REGION",
    "ap-southeast-1",
)

S3_BUCKET = os.getenv(
    "S3_BUCKET",
    "vendor-payments-data-platform-thana",
)

S3_PREFIX = os.getenv(
    "S3_PREFIX",
    "data-platform/vendor-payments",
)

LATEST_POINTER_S3_KEY = (
    f"{S3_PREFIX}/streaming/curated/latest.json"
)


def publish_latest_streaming_pointer(
    *,
    window_id: str,
    events_s3_key: str,
) -> str:
    if not window_id:
        raise ValueError(
            "window_id is required."
        )

    if not events_s3_key:
        raise ValueError(
            "events_s3_key is required."
        )

    pointer = {
        "window_id": window_id,
        "status": "completed",
        "events_s3_key": events_s3_key,
    }

    s3_client = boto3.client(
        "s3",
        region_name=AWS_REGION,
    )

    s3_client.put_object(
        Bucket=S3_BUCKET,
        Key=LATEST_POINTER_S3_KEY,
        Body=json.dumps(
            pointer,
            indent=2,
        ).encode("utf-8"),
        ContentType="application/json",
    )

    return (
        f"s3://{S3_BUCKET}/"
        f"{LATEST_POINTER_S3_KEY}"
    )


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--window-id",
        required=True,
    )

    parser.add_argument(
        "--events-s3-key",
        required=True,
    )

    args = parser.parse_args()

    pointer_uri = publish_latest_streaming_pointer(
        window_id=args.window_id,
        events_s3_key=args.events_s3_key,
    )

    print(
        "Latest Streaming pointer published: "
        f"{pointer_uri}"
    )


if __name__ == "__main__":
    main()