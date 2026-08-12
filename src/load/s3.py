from pathlib import Path

import boto3

def upload_file_to_s3(
        file_path: Path,
        bucket: str,
        key: str,
        region: str,
) -> None:
    s3_client = boto3.client(
        "s3",
        region_name=region
    )
    s3_client.upload_file(
        str(file_path),
        bucket,
        key
    )

def upload_directory_to_s3(
        directory: Path,
        bucket: str,
        prefix: str,
        region: str,
) -> None:
    s3_client = boto3.client(
        "s3",
        region_name=region
    )

    files = list(
        directory.rglob("*.parquet")
    )

    print(f"{len(files)}個のParquetファイルをS3にアップロードします。")

    for file_path in files:
        relative_path = (
            file_path
            .relative_to(directory)
            .as_posix()
        )

        key = (
            f"{prefix.rstrip('/')}/"
            f"{relative_path}"
        )

        print(
            f"{key}をS3にアップロード中... "
        )

        s3_client.upload_file(
            str(file_path),
            bucket,
            key,
        )