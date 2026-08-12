from pathlib import Path

import numpy as np
import pandas as pd

from config import PROJECT_ROOT

OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "raw" / "matches_large.csv"
)

ROW_COUNT = 1_000_000

def main() -> None:
    rng = np.random.default_rng(seed=42)

    dates = pd.date_range(
        start="2022-01-01",
        end="2026-12-31",
        freq="D",
    )

    teams = [
        "Sapporo",
        "Sendai",
        "Chiba",
        "Iwata",
        "Omiya",
        "Mito",
        "Yamagata",
        "Kofu",
    ]

    matches = pd.DataFrame(
        {
            "match_id": np.arange(
                1,
                ROW_COUNT + 1,
            ),
            "match_date": rng.choice(
                dates,
                ROW_COUNT,
            ),
            "home_team": rng.choice(
                teams,
                ROW_COUNT,
            ),
            "away_team": rng.choice(
                teams,
                ROW_COUNT,
            ),
            "home_goals": rng.integers(
                0,
                6,
                ROW_COUNT,
            ),
            "away_goals": rng.integers(
                0,
                6,
                ROW_COUNT,
            ),
        }
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    matches.to_csv(
        OUTPUT_PATH,
        index=False,
    )

    print(f"{ROW_COUNT:,}件を生成しました")
    print(f"保存先: {OUTPUT_PATH}")


if __name__ == "__main__":
    main()
