import csv
import json
import os
import argparse
from pathlib import Path
from typing import Any


STREAMING_PIPELINE_ROOT = Path(
    os.getenv(
        "VENDOR_STREAMING_CONTAINER_PATH",
        r"E:\dev\vendor-payments-streaming-pipeline",
    )
)


def flatten_record(
    record: dict[str, Any],
    parent_key: str = "",
    separator: str = "_",
) -> dict[str, Any]:
    """Flatten nested JSON records into a single-level dictionary."""
    flattened: dict[str, Any] = {}

    for key, value in record.items():
        clean_key = f"{parent_key}{separator}{key}" if parent_key else key

        if isinstance(value, dict):
            flattened.update(flatten_record(value, clean_key, separator))
        elif isinstance(value, list):
            flattened[clean_key] = json.dumps(value, ensure_ascii=False)
        else:
            flattened[clean_key] = value

    return flattened


def read_jsonl_records(input_path: Path) -> list[dict[str, Any]]:
    """Read JSONL records from a local streaming staging file."""
    if not input_path.exists():
        raise FileNotFoundError(f"Input JSONL file not found: {input_path}")

    records: list[dict[str, Any]] = []

    with input_path.open("r", encoding="utf-8") as file:
        for line_number, line in enumerate(file, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                record = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(
                    f"Invalid JSON at line {line_number}: {input_path}"
                ) from exc

            if not isinstance(record, dict):
                raise ValueError(
                    f"Expected JSON object at line {line_number}: {input_path}"
                )

            records.append(flatten_record(record))

    return records


def infer_fieldnames(records: list[dict[str, Any]]) -> list[str]:
    """Infer CSV columns from all flattened JSONL records."""
    fieldnames: set[str] = set()

    for record in records:
        fieldnames.update(record.keys())

    return sorted(fieldnames)


def write_csv(records: list[dict[str, Any]], output_path: Path) -> None:
    """Write flattened records to CSV."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = infer_fieldnames(records)

    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)


def convert_jsonl_to_csv(
    input_path: Path,
    output_path: Path,
) -> Path:
    """Convert one streaming window JSONL file to curated CSV."""
    records = read_jsonl_records(input_path)

    if not records:
        raise ValueError(
            f"No records found in input JSONL file: {input_path}"
        )

    write_csv(
        records,
        output_path,
    )

    return output_path


def main() -> None:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input-file",
        required=True,
    )

    parser.add_argument(
        "--output-file",
        required=True,
    )

    args = parser.parse_args()

    output_path = convert_jsonl_to_csv(
        input_path=Path(args.input_file),
        output_path=Path(args.output_file),
    )

    print(
        f"Streaming curated CSV created: {output_path}"
    )


if __name__ == "__main__":
    main()