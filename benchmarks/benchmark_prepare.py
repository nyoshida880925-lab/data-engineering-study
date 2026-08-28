import pandas as pd

from config import PROJECT_ROOT

CSV_PATH = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "matches_large.csv"
)

PARQUET_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "matches_large"
)

def main() -> None:
    matches = pd.read_csv(
        CSV_PATH,
        parse_dates=["match_date"],
    )

    matches["season"] = (
        matches["match_date"]
        .dt.year
    )

    matches.to_parquet(
        PARQUET_PATH,
        index=False,
        partition_cols=["season"],
    )

    print(
        f"{len(matches)}件を"
        f"{PARQUET_PATH}へ変換しました。"
    )

if __name__ == "__main__":
    main()
