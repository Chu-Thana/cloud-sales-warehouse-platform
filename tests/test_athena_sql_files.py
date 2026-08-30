from pathlib import Path

# These tests validate the Athena SQL assets used in the cloud analytics layer.
# They check file structure and expected SQL content, but do not execute queries in Athena.

ATHENA_SQL_DIR = Path("sql/athena")

# Expected Athena SQL files for database setup, table DDL, and sample analytics queries.
EXPECTED_SQL_FILES = [
    "01_create_database.sql",
    "02_create_gold_tables.sql",
    "03_query_spending_by_fiscal_year.sql",
    "04_query_top_suppliers.sql",
    "05_query_pending_by_department.sql",
    "06_create_streaming_events_table.sql",
    "07_query_streaming_events.sql",
]


def test_athena_sql_directory_exists():
    assert ATHENA_SQL_DIR.exists(), f"Athena SQL directory not found: {ATHENA_SQL_DIR}"


def test_expected_athena_sql_files_exist():
    for file_name in EXPECTED_SQL_FILES:
        file_path = ATHENA_SQL_DIR / file_name
        assert file_path.exists(), f"Missing Athena SQL file: {file_path}"


def test_athena_sql_files_are_not_empty():
    for file_name in EXPECTED_SQL_FILES:
        file_path = ATHENA_SQL_DIR / file_name
        content = file_path.read_text(encoding="utf-8").strip()

        assert content, f"Athena SQL file is empty: {file_path}"


def test_create_gold_tables_contains_expected_tables():
    # Validate that the Athena DDL references the expected gold marts and S3 location.
    ddl_file = ATHENA_SQL_DIR / "02_create_gold_tables.sql"
    content = ddl_file.read_text(encoding="utf-8")

    assert "CREATE EXTERNAL TABLE" in content
    assert "mart_spending_by_fiscal_year" in content
    assert "mart_spending_by_supplier_top_n" in content
    assert "mart_pending_by_department" in content
    assert "data-platform/vendor-payments/gold/full" in content


def test_query_files_reference_vendor_payments_database():
    query_files = [
        "03_query_spending_by_fiscal_year.sql",
        "04_query_top_suppliers.sql",
        "05_query_pending_by_department.sql",
    ]

    for file_name in query_files:
        content = (ATHENA_SQL_DIR / file_name).read_text(encoding="utf-8")

        assert "vendor_payments_analytics" in content
        assert "SELECT" in content

def test_streaming_table_sql_contains_expected_location_and_columns():
    sql_file = ATHENA_SQL_DIR / "06_create_streaming_events_table.sql"
    content = sql_file.read_text(encoding="utf-8")

    assert "CREATE EXTERNAL TABLE" in content
    assert "vendor_payments_streaming_events" in content
    assert "${STREAMING_CURATED_S3_LOCATION}" in content
    assert "event_id" in content
    assert "event_timestamp" in content
    assert "payment_amount" in content
    assert "payload_window_id" in content
    assert "window_id" in content


def test_streaming_query_file_references_streaming_table():
    sql_file = ATHENA_SQL_DIR / "07_query_streaming_events.sql"
    content = sql_file.read_text(encoding="utf-8")

    assert "vendor_payments_analytics.vendor_payments_streaming_events" in content
    assert "COUNT(DISTINCT event_id)" in content
    assert "CAST(payment_amount AS DOUBLE)" in content