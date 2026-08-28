import pandas as pd

from data_engineering_study.load.parquet import save_as_partitioned_parquet

def test_save_as_partitioned_parquet(tmp_path):
    # テスト用のDataFrameを作成
    data = pd.DataFrame(
        {
            "match_id": [1, 2],
            "match_date": ["2026-07-01", "2026-07-08"],
            "home_team": ["Sapporo", "Iwata"],
            "away_team": ["Sendai", "Chiba"],
            "home_goals": [3, 2],
            "away_goals": [1, 2],
            "season": [2025, 2026],
        }
    )

    # 一時ディレクトリに保存するパスを指定
    output_path = tmp_path / "matches"

    # save_as_partitioned_parquet関数を呼び出す
    save_as_partitioned_parquet(data, output_path)

    assert (output_path / "season=2025").exists()
    assert (output_path / "season=2026").exists()

    # 保存されたParquetファイルを読み込む
    loaded = pd.read_parquet(
        output_path,
        filters=[
            ("season", "=", 2026),
        ]
    )

    assert len(loaded) == 1
    assert loaded.iloc[0]["match_id"] == 2

