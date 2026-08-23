from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]


def test_required_project_directories_exist():
    required_dirs = [
        ROOT_DIR / "assets",
        ROOT_DIR / "scripts" / "batch",
    ]

    for dir_path in required_dirs:
        assert dir_path.exists(), f"Missing required directory: {dir_path}"


def test_required_project_files_exist():
    required_files = [
        ROOT_DIR / "README.md",
        ROOT_DIR / "requirements.txt",
        ROOT_DIR / ".env.example",
        ROOT_DIR / "scripts" / "batch" / "convert_to_parquet.py",
        ROOT_DIR / "scripts" / "batch" / "upload_csv_to_s3.py",
        ROOT_DIR / "scripts" / "batch" / "upload_to_s3.py",
    ]

    for file_path in required_files:
        assert file_path.exists(), f"Missing required file: {file_path}"


def test_architecture_assets_exist():
    required_assets = [
        ROOT_DIR
        / "assets"
        / "redshift"
        / "00_cloud_data_platform_architecture.png",

        ROOT_DIR
        / "assets"
        / "redshift"
        / "01_s3_full_gold_marts.png",

        ROOT_DIR
        / "assets"
        / "redshift"
        / "02_athena_batch_query.png",

        ROOT_DIR
        / "assets"
        / "redshift"
        / "03_athena_streaming_validation.png",

        ROOT_DIR
        / "assets"
        / "redshift"
        / "04_redshift_batch_landing.png",

        ROOT_DIR
        / "assets"
        / "redshift"
        / "05_redshift_batch_analytics.png",

        ROOT_DIR
        / "assets"
        / "redshift"
        / "06_redshift_streaming_validation.png",

        ROOT_DIR
        / "assets"
        / "redshift"
        / "07_redshift_runtime_metadata.png",

        ROOT_DIR
        / "assets"
        / "redshift"
        / "08_cloud_tests_and_lint.png",

        ROOT_DIR
        / "assets"
        / "redshift"
        / "09_cloud_ci_success.png",
    ]

    for asset_path in required_assets:
        assert asset_path.exists(), f"Missing required asset: {asset_path}"

    for asset_path in required_assets:
        assert asset_path.exists(), f"Missing required asset: {asset_path}"