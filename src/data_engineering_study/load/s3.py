from pathlib import Path
from typing import Any

def upload_file_to_s3(
        file_path: Path,
        bucket: str,
        key: str,
        s3_client: Any,
) -> None:
    if not file_path.is_file():
        raise FileNotFoundError(f"{file_path}が見つかりません。")

    s3_client.upload_file(
        str(file_path),
        bucket,
        key
    )

def upload_directory_to_s3(
        directory: Path,
        bucket: str,
        prefix: str,
        s3_client: Any,
) -> None:
    if not directory.is_dir():
        raise FileNotFoundError(f"{directory}が見つかりません。")

    files = list(
        directory.rglob("*.parquet")
    )

    if not files:
        raise ValueError(f"{directory}にParquetファイルが見つかりません。")

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