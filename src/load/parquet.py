import shutil
from pathlib import Path

import pandas as pd

def save_as_partitioned_parquet(
        data: pd.DataFrame,
        output_path: Path,
) -> None:
    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
        )
    data.to_parquet(
        output_path,
        index=False,
        partition_cols=["season"],
        )

def save_as_deterministic_partitioned_parquet(
    data: pd.DataFrame,
    output_path: Path,
) -> None:
    if output_path.exists():
        shutil.rmtree(output_path)

    output_path.mkdir(
        parents=True,
        exist_ok=True,
    )

    for season, partition in data.groupby("season"):
        partition_directory = (
            output_path
            / f"season={season}"
        )

        partition_directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        file_path = (
            partition_directory
            / "matches.parquet"
        )

        parquet_data = partition.drop(
            columns=["season"]
        )

        parquet_data.to_parquet(
            file_path,
            index=False,
        )
