from __future__ import annotations

import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import boto3


PROJECT_ROOT = Path(__file__).resolve().parents[2]

AWS_REGION = os.getenv(
    "AWS_REGION",
    "ap-southeast-1",
)

ATHENA_DATABASE = os.getenv(
    "ATHENA_DATABASE",
    "vendor_payments_analytics",
)

ATHENA_OUTPUT_LOCATION = os.getenv(
    "ATHENA_OUTPUT_LOCATION",
)

POLL_INTERVAL_SECONDS = 1
QUERY_TIMEOUT_SECONDS = 300


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


def wait_for_query(
    client: Any,
    query_execution_id: str,
) -> dict[str, Any]:
    started_at = time.monotonic()

    while True:
        response = client.get_query_execution(
            QueryExecutionId=query_execution_id,
        )

        status = response[
            "QueryExecution"
        ]["Status"]["State"]

        if status == "SUCCEEDED":
            return response

        if status in {
            "FAILED",
            "CANCELLED",
        }:
            reason = response[
                "QueryExecution"
            ]["Status"].get(
                "StateChangeReason",
                "Unknown Athena query error",
            )

            raise RuntimeError(
                f"Athena query {status.lower()}: "
                f"{reason}"
            )

        elapsed_seconds = (
            time.monotonic() - started_at
        )

        if elapsed_seconds > QUERY_TIMEOUT_SECONDS:
            raise TimeoutError(
                "Athena query exceeded "
                f"{QUERY_TIMEOUT_SECONDS} seconds."
            )

        time.sleep(POLL_INTERVAL_SECONDS)


def execute_query_file(
    client: Any,
    sql_file: Path,
) -> str:
    if not sql_file.exists():
        raise FileNotFoundError(
            f"SQL file not found: {sql_file}"
        )

    if not ATHENA_OUTPUT_LOCATION:
        raise ValueError(
            "ATHENA_OUTPUT_LOCATION is not set."
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

    response = client.start_query_execution(
        QueryString=sql,
        QueryExecutionContext={
            "Database": ATHENA_DATABASE,
        },
        ResultConfiguration={
            "OutputLocation": ATHENA_OUTPUT_LOCATION,
        },
    )

    query_execution_id = response[
        "QueryExecutionId"
    ]

    wait_for_query(
        client=client,
        query_execution_id=query_execution_id,
    )

    return query_execution_id


def get_query_results(
    client: Any,
    query_execution_id: str,
) -> list[dict[str, str | None]]:
    response = client.get_query_results(
        QueryExecutionId=query_execution_id,
    )

    result_set = response["ResultSet"]
    rows = result_set.get(
        "Rows",
        [],
    )

    column_info = result_set[
        "ResultSetMetadata"
    ]["ColumnInfo"]

    column_names = [
        column["Name"]
        for column in column_info
    ]

    if len(rows) <= 1:
        return []

    results: list[dict[str, str | None]] = []

    for row in rows[1:]:
        values = row.get(
            "Data",
            [],
        )

        record: dict[str, str | None] = {}

        for index, column_name in enumerate(
            column_names
        ):
            value = None

            if index < len(values):
                value = values[index].get(
                    "VarCharValue"
                )

            record[column_name] = value

        results.append(record)

    return results


def main() -> None:
    if len(sys.argv) != 2:
        raise ValueError(
            "Usage: python run_athena_query.py "
            "<sql_file_path>"
        )

    sql_file = Path(
        sys.argv[1]
    )

    if not sql_file.is_absolute():
        sql_file = PROJECT_ROOT / sql_file

    client = boto3.client(
        "athena",
        region_name=AWS_REGION,
    )

    print(
        f"Running Athena SQL: {sql_file}"
    )

    query_execution_id = execute_query_file(
        client=client,
        sql_file=sql_file,
    )

    results = get_query_results(
        client=client,
        query_execution_id=query_execution_id,
    )

    if results:
        print("Athena query results:")

        for row in results:
            print(row)

    print(
        "Athena query completed successfully: "
        f"{query_execution_id}"
    )


if __name__ == "__main__":
    main()