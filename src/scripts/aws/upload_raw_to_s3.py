import boto3

from data_engineering_study.config import PROJECT_ROOT, get_s3_settings
from data_engineering_study.load.s3 import upload_file_to_s3

RAW_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "matches_large.csv"
)

S3_KEY = "raw/python/matches_large.csv"

def main() -> None:
    settings = get_s3_settings()

    print(f"{RAW_FILE}をS3へアップロードします。")

    s3_client = boto3.client("s3", region_name=settings["AWS_REGION"])

    upload_file_to_s3(
        file_path=RAW_FILE,
        bucket=settings["S3_BUCKET"],
        key=S3_KEY,
        s3_client=s3_client,
    )

    print(
        "アップロード完了: "
        f"s3://{settings['S3_BUCKET']}/{S3_KEY}"
    )

if __name__ == "__main__":
    main()
