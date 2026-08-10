from __future__ import annotations

import os
from pathlib import Path

import boto3


BATCH_ETL_ROOT = Path(
    os.getenv(
        "VENDOR_BATCH_ETL_CONTAINER_PATH",
        r"E:\dev\vendor-payments-etl-analytics",
    )
)

S3_BUCKET = os.getenv(
    "S3_BUCKET",
    "your-s3-bucket-name",
)

S3_PREFIX = os.getenv(
    "S3_PREFIX",
    "data-platform/vendor-payments",
)

FULL_GOLD_DIR = (
    BATCH_ETL_ROOT
    / "data"
    / "processed"
    / "gold"
)

EXPECTED_GOLD_FILES = (
    "mart_spending_by_fiscal_year.csv",
    "mart_spending_by_department.csv",
    "mart_spending_by_supplier_top_n.csv",
    "mart_fund_category_summary.csv",
    "mart_pending_by_department.csv",
)


def build_upload_plan() -> list[tuple[Path, str]]:
    """Build the full Gold mart upload plan for Redshift."""

    upload_plan: list[tuple[Path, str]] = []

    for file_name in EXPECTED_GOLD_FILES:
        local_path = FULL_GOLD_DIR / file_name
        table_name = local_path.stem

        s3_key = (
            f"{S3_PREFIX}/gold/full/"
            f"{table_name}/{file_name}"
        )

        upload_plan.append(
            (
                local_path,
                s3_key,
            )
        )

    return upload_plan


def validate_upload_plan(
    upload_plan: list[tuple[Path, str]],
) -> None:
    """Ensure every required Gold mart exists and is not empty."""

    missing_files = [
        local_path
        for local_path, _ in upload_plan
        if not local_path.exists()
    ]

    if missing_files:
        missing_list = "\n".join(
            str(path)
            for path in missing_files
        )

        raise FileNotFoundError(
            "Missing required full Gold files:\n"
            f"{missing_list}"
        )

    empty_files = [
        local_path
        for local_path, _ in upload_plan
        if local_path.stat().st_size == 0
    ]

    if empty_files:
        empty_list = "\n".join(
            str(path)
            for path in empty_files
        )

        raise ValueError(
            "Empty full Gold files found:\n"
            f"{empty_list}"
        )


def upload_files_to_s3(
    upload_plan: list[tuple[Path, str]],
) -> None:
    """Upload full Gold marts to their Redshift source prefixes."""

    s3_client = boto3.client("s3")

    for local_path, s3_key in upload_plan:
        print(
            f"Uploading {local_path.name}\n"
            f"-> s3://{S3_BUCKET}/{s3_key}"
        )

        s3_client.upload_file(
            Filename=str(local_path),
            Bucket=S3_BUCKET,
            Key=s3_key,
        )

    print(
        "Full Gold mart upload completed successfully."
    )


def main() -> None:
    if S3_BUCKET == "your-s3-bucket-name":
        raise ValueError(
            "Please set S3_BUCKET before running this script."
        )

    upload_plan = build_upload_plan()
    validate_upload_plan(upload_plan)

    print("Vendor Payments full Gold upload plan:")

    for local_path, s3_key in upload_plan:
        print(
            f"- {local_path.name}"
            f" -> s3://{S3_BUCKET}/{s3_key}"
        )

    upload_files_to_s3(upload_plan)


if __name__ == "__main__":
    main()