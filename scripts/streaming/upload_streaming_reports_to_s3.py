import os
from pathlib import Path

import boto3


STREAMING_PIPELINE_ROOT = Path(
    os.getenv(
        "STREAMING_PIPELINE_ROOT",
        r"E:\dev\vendor-payments-streaming-pipeline",
    )
)

ORCHESTRATION_OUTPUT_ROOT = Path(
    os.getenv(
        "ORCHESTRATION_OUTPUT_ROOT",
        r"E:\dev\vendor-payments-airflow-orchestration\output",
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


STREAMING_SUMMARY_REPORT = (
    STREAMING_PIPELINE_ROOT
    / "output"
    / "reports"
    / "streaming_summary_report.json"
)

AIRFLOW_ORCHESTRATION_SUMMARY = (
    ORCHESTRATION_OUTPUT_ROOT
    / "reports"
    / "airflow_orchestration_summary.json"
)


def build_upload_plan() -> list[tuple[Path, str]]:
    return [
        (
            STREAMING_SUMMARY_REPORT,
            f"{S3_PREFIX}/streaming/reports/"
            f"{STREAMING_SUMMARY_REPORT.name}",
        ),
        (
            AIRFLOW_ORCHESTRATION_SUMMARY,
            f"{S3_PREFIX}/streaming/reports/"
            f"{AIRFLOW_ORCHESTRATION_SUMMARY.name}",
        ),
    ]


def validate_upload_plan(
    upload_plan: list[tuple[Path, str]],
) -> None:
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
            f"Missing required files:\n{missing_list}"
        )


def upload_files_to_s3(
        upload_plan: list[tuple[Path, str]],
) -> None:
    s3_client = boto3.client("s3")

    for local_path, s3_key in upload_plan:
        print(f"Uploading {local_path}")
        print(
            f"-> s3://{S3_BUCKET}/{s3_key}"
        )

        s3_client.upload_file(
            Filename=str(local_path),
            Bucket=S3_BUCKET,
            Key=s3_key,
        )

    print(
        "Streaming reports upload completed successfully."
    )


def main() -> None:
    if S3_BUCKET == "your-s3-bucket-name":
        raise ValueError(
            "Please set S3_BUCKET environment variable "
            "before running this script."
        )

    upload_plan = build_upload_plan()

    validate_upload_plan(
        upload_plan
    )

    print(
        "Vendor Payments streaming reports "
        "upload plan:"
    )

    for local_path, s3_key in upload_plan:
        print(
            f"- {local_path.name} "
            f"-> s3://{S3_BUCKET}/{s3_key}"
        )

    upload_files_to_s3(
        upload_plan
    )


if __name__ == "__main__":
    main()