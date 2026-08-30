from __future__ import annotations

import os
import sys
import re
import time
from pathlib import Path
from typing import Any

import boto3


PROJECT_ROOT = Path(__file__).resolve().parents[2]

AWS_REGION = os.getenv(
    "AWS_REGION",
    "ap-southeast-1",
)

REDSHIFT_WORKGROUP = os.getenv(
    "REDSHIFT_WORKGROUP",
    "default-workgroup",
)

REDSHIFT_DATABASE = os.getenv(
    "REDSHIFT_DATABASE",
    "dev",
)

POLL_INTERVAL_SECONDS = 1
STATEMENT_TIMEOUT_SECONDS = 300

def wait_for_statement(
    client: Any,
    statement_id: str,
) -> dict[str, Any]:
    started_at = time.monotonic()

    while True:
        response = client.describe_statement(
            Id=statement_id,
        )
        status = response["Status"]

        if status == "FINISHED":
            return response

        if status in {"FAILED", "ABORTED"}:
            error_message = response.get(
                "Error",
                "Unknown Redshift statement error",
            )
            raise RuntimeError(
                f"Redshift statement {status.lower()}: "
                f"{error_message}"
            )

        elapsed_seconds = (
            time.monotonic() - started_at
        )

        if elapsed_seconds > STATEMENT_TIMEOUT_SECONDS:
            raise TimeoutError(
                "Redshift statement exceeded "
                f"{STATEMENT_TIMEOUT_SECONDS} seconds."
            )

        time.sleep(POLL_INTERVAL_SECONDS)


def render_sql_environment_variables(
    sql: str,
) -> str:
    """Replace ${ENV_VAR} placeholders with environment values."""
    pattern = re.compile(r"\$\{([A-Z0-9_]+)\}")

    def replace(match: re.Match[str]) -> str:
        variable_name = match.group(1)
        value = os.getenv(variable_name)

        if value is None:
            raise ValueError(
                "Required SQL environment variable is not set: "
                f"{variable_name}"
            )

        return value

    return pattern.sub(
        replace,
        sql,
    )


def get_statement_results(
    client: Any,
    statement_id: str,
) -> list[dict[str, str | None]]:
    response = client.get_statement_result(
        Id=statement_id,
    )

    columns = response.get(
        "ColumnMetadata",
        [],
    )

    records = response.get(
        "Records",
        [],
    )

    column_names = [
        column["name"]
        for column in columns
    ]

    results: list[dict[str, str | None]] = []

    for record in records:
        row: dict[str, str | None] = {}

        for index, column_name in enumerate(
            column_names
        ):
            value = None

            if index < len(record):
                field = record[index]

                if "stringValue" in field:
                    value = field["stringValue"]
                elif "longValue" in field:
                    value = str(
                        field["longValue"]
                    )
                elif "doubleValue" in field:
                    value = str(
                        field["doubleValue"]
                    )
                elif "booleanValue" in field:
                    value = str(
                        field["booleanValue"]
                    )

            row[column_name] = value

        results.append(row)

    return results


def execute_sql_file(
    client: Any,
    sql_file: Path,
) -> str:
    if not sql_file.exists():
        raise FileNotFoundError(
            f"SQL file not found: {sql_file}"
        )

    sql = sql_file.read_text(
        encoding="utf-8",
    )

    sql = render_sql_environment_variables(
        sql
    )

    if not sql.strip():
        raise ValueError(
            f"SQL file is empty: {sql_file}"
        )

    response = client.execute_statement(
        WorkgroupName=REDSHIFT_WORKGROUP,
        Database=REDSHIFT_DATABASE,
        Sql=sql,
    )

    statement_id = response["Id"]

    wait_for_statement(
        client=client,
        statement_id=statement_id,
    )

    return statement_id

def main() -> None:
    if len(sys.argv) != 2:
        raise ValueError(
            "Usage: python run_redshift_sql.py "
            "<sql_file_path>"
        )

    sql_file = Path(sys.argv[1])

    if not sql_file.is_absolute():
        sql_file = PROJECT_ROOT / sql_file

    client = boto3.client(
        "redshift-data",
        region_name=AWS_REGION,
    )

    print(f"Running Redshift SQL: {sql_file}")

    statement_id = execute_sql_file(
        client=client,
        sql_file=sql_file,
    )

    statement = client.describe_statement(
        Id=statement_id,
    )

    if statement.get("HasResultSet", False):
        results = get_statement_results(
            client=client,
            statement_id=statement_id,
        )

        if results:
            print("Redshift query results:")

            for row in results:
                print(row)

    print(
        "Redshift SQL execution completed successfully."
    )


if __name__ == "__main__":
    main()