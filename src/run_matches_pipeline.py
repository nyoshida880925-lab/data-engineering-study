import boto3

from config import (
    PROJECT_ROOT,
    get_s3_settings,
)

from extract.matches import extract_matches
from load.parquet import (
    save_as_deterministic_partitioned_parquet,
)
from load.s3 import (
    upload_directory_to_s3,
    upload_file_to_s3,
)
from transform.matches import transform_matches

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "matches_large.csv"
)

PROCESSED_DIRECTORY = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "pipeline_matches"
)

RAW_S3_KEY = (
    "raw/python-pipeline/"
    "matches_large.csv"
)

PROCESSED_S3_PREFIX = (
    "processed/python-pipeline/matches"
)

def main() -> None:
    settings = get_s3_settings()

    bucket = settings["S3_BUCKET"]
    region = settings["AWS_REGION"]
    s3_client = boto3.client("s3", region_name=region)

    print("=== Matches Pipeline Start ===")

    # 1. RawデータをS3へ保存
    print()
    print(f"[1/4] {RAW_FILE}をS3へアップロードします。")

    upload_file_to_s3(
        file_path=RAW_FILE,
        bucket=bucket,
        key=RAW_S3_KEY,
        s3_client=s3_client,
    )

    print(
        "アップロード完了: "
        f"s3://{bucket}/{RAW_S3_KEY}"
    )

    # 2. Extract
    print(f"[2/4] {RAW_FILE}から試合データを抽出します。")

    matches = extract_matches(RAW_FILE)

    # 3. Transform+Parquet
    print()
    print("[3/4] Transformを実行します")
    transformed_matches = transform_matches(matches)

    if transformed_matches.empty:
        print("登録対象の試合データがありません。")
        return

    save_as_deterministic_partitioned_parquet(
        transformed_matches,
        PROCESSED_DIRECTORY,
    )

    print(
        f"{len(transformed_matches)}件を"
        f"{PROCESSED_DIRECTORY}へ保存しました。"
    )

    # 4. S3へアップロード
    print()
    print(
        "[4/4] Processedデータを"
        "S3へ保存します"
    )

    upload_directory_to_s3(
        directory=PROCESSED_DIRECTORY,
        bucket=bucket,
        prefix=PROCESSED_S3_PREFIX,
        s3_client=s3_client,
    )

    print()
    print("=== Matches Pipeline Complete ===")

    print(
        "アップロード完了: "
        f"s3://{bucket}/{PROCESSED_S3_PREFIX}"
    )

if __name__ == "__main__":
    main()