from unittest.mock import Mock, call
import pytest

from data_engineering_study.load.s3 import (
    upload_directory_to_s3,
    upload_file_to_s3,
)

def test_upload_file_to_s3(tmp_path):
    file_path = tmp_path / "matches.csv"

    file_path.write_text(
        "match_id,home_team\n1,Sapporo\n",
        encoding="utf-8",
    )

    s3_client = Mock()

    upload_file_to_s3(
        file_path=file_path,
        bucket="test-bucket",
        key="raw/matches.csv",
        s3_client=s3_client,
    )

    s3_client.upload_file.assert_called_once_with(
        str(file_path),
        "test-bucket",
        "raw/matches.csv",
    )

def test_upload_directory_to_s3(tmp_path):
    directory = tmp_path / "matches"

    season_2025 = directory / "season=2025"
    season_2026 = directory / "season=2026"

    season_2025.mkdir(parents=True)
    season_2026.mkdir(parents=True)

    file_2025 = season_2025 / "matches.parquet"
    file_2026 = season_2026 / "matches.parquet"

    file_2025.write_bytes(b"test")
    file_2026.write_bytes(b"test")

    s3_client = Mock()

    upload_directory_to_s3(
        directory=directory,
        bucket="test-bucket",
        prefix="processed/matches",
        s3_client=s3_client,
    )

    assert s3_client.upload_file.call_count == 2

    s3_client.upload_file.assert_has_calls(
        [
            call(
                str(file_2025),
                "test-bucket",
                (
                    "processed/matches/"
                    "season=2025/matches.parquet"
                ),
            ),
            call(
                str(file_2026),
                "test-bucket",
                (
                    "processed/matches/"
                    "season=2026/matches.parquet"
                ),
            ),
        ],
        any_order=True,
    )

def test_upload_directory_without_parquet(tmp_path):
    directory = tmp_path / "matches"
    directory.mkdir()

    s3_client = Mock()

    with pytest.raises(
        ValueError,
        match=f"{directory}にParquetファイルが見つかりません。",
    ):
        upload_directory_to_s3(
            directory=directory,
            bucket="test-bucket",
            prefix="processed/matches",
            s3_client=s3_client,
        )

    s3_client.upload_file.assert_not_called()
