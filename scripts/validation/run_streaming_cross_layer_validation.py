from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import boto3

from scripts.athena.run_athena_query import (
    execute_query_file,
    get_query_results,
)
from scripts.validation.compare_streaming_metrics import (
    compare_streaming_metrics,
)
from scripts.warehouse.run_redshift_sql import (
    execute_sql_file,
    get_statement_results,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

AWS_REGION = os.getenv(
    "AWS_REGION",
    "ap-southeast-1",
)

ATHENA_SET_LOCATION_SQL = (
    PROJECT_ROOT
    / "sql"
    / "athena"
    / "08_set_streaming_window_location.sql"
)

ATHENA_VALIDATE_SQL = (
    PROJECT_ROOT
    / "sql"
    / "athena"
    / "09_validate_streaming_window.sql"
)

REDSHIFT_VALIDATE_SQL = (
    PROJECT_ROOT
    / "sql"
    / "redshift"
    / "10_validate_streaming_window_metrics.sql"
)


def get_single_result(
    results: list[dict[str, str | None]],
    source_name: str,
) -> dict[str, str]:
    if len(results) != 1:
        raise ValueError(
            f"{source_name} validation expected exactly one row, "
            f"got {len(results)}."
        )

    result = results[0]

    required_columns = {
        "row_count",
        "distinct_event_count",
        "total_payment_amount",
    }

    missing_columns = required_columns - result.keys()

    if missing_columns:
        raise ValueError(
            f"{source_name} validation is missing columns: "
            f"{sorted(missing_columns)}"
        )

    normalized: dict[str, str] = {}

    for column in required_columns:
        value = result[column]

        if value is None:
            raise ValueError(
                f"{source_name} validation returned NULL "
                f"for {column}."
            )

        normalized[column] = value

    return normalized


def run_validation() -> None:
    athena_client: Any = boto3.client(
        "athena",
        region_name=AWS_REGION,
    )

    redshift_client: Any = boto3.client(
        "redshift-data",
        region_name=AWS_REGION,
    )

    print("Updating Athena Streaming window location...")

    execute_query_file(
        client=athena_client,
        sql_file=ATHENA_SET_LOCATION_SQL,
    )

    print("Reading Athena S3 metrics...")

    athena_query_id = execute_query_file(
        client=athena_client,
        sql_file=ATHENA_VALIDATE_SQL,
    )

    athena_metrics = get_single_result(
        get_query_results(
            client=athena_client,
            query_execution_id=athena_query_id,
        ),
        source_name="Athena",
    )

    print("Reading Redshift Landing metrics...")

    redshift_statement_id = execute_sql_file(
        client=redshift_client,
        sql_file=REDSHIFT_VALIDATE_SQL,
    )

    redshift_metrics = get_single_result(
        get_statement_results(
            client=redshift_client,
            statement_id=redshift_statement_id,
        ),
        source_name="Redshift",
    )

    print(f"Athena metrics: {athena_metrics}")
    print(f"Redshift metrics: {redshift_metrics}")

    compare_streaming_metrics(
        athena_metrics=athena_metrics,
        redshift_metrics=redshift_metrics,
    )


def main() -> None:
    required_environment_variables = [
        "ATHENA_OUTPUT_LOCATION",
        "STREAMING_CURATED_S3_LOCATION",
        "STREAMING_WINDOW_ID",
    ]

    missing_variables = [
        variable
        for variable in required_environment_variables
        if not os.getenv(variable)
    ]

    if missing_variables:
        raise ValueError(
            "Required environment variables are not set: "
            + ", ".join(missing_variables)
        )

    run_validation()


if __name__ == "__main__":
    main()