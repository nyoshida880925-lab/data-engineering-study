from time import perf_counter

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

def measure(
        name: str,
        loader,
) -> None:
    start = perf_counter()

    data = loader()

    elapsed_time = perf_counter() - start
    print(
        f"{name}: "
        f" {elapsed_time:.2f}秒 "
        f" ({len(data)}件)"
    )

def main() -> None:
    measure(
        "CSV 全件",
        lambda: pd.read_csv(
            CSV_PATH,
            usecols=[
                "match_id",
                "home_goals",
            ],
        ),
    )

    measure(
        "Parquet 全件",
        lambda: pd.read_parquet(
            PARQUET_PATH,
            columns=[
                "match_id",
                "home_goals",
            ],
        ),
    )

    measure(
        "Parquet 2026年のみ",
        lambda: pd.read_parquet(
            PARQUET_PATH,
            filters=[
                ("season", "=", 2026),
            ],
        ),
    )

if __name__ == "__main__":
    main()
