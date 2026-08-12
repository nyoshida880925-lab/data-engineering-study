from __future__ import annotations

import os
from pathlib import Path

import pandas as pd
import psycopg
from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / "docker" / "postgres" / ".env"
CSV_PATH = PROJECT_ROOT / "data" / "raw" / "matches.csv"

REQUIRED_COLUMNS = {
    "match_id",
    "match_date",
    "home_team",
    "away_team",
    "home_goals",
    "away_goals",
}

UPSERT_SQL = """
INSERT INTO matches (match_id, match_date, home_team, away_team, home_goals, away_goals)
VALUES (%s, %s, %s, %s, %s, %s)
ON CONFLICT (match_id) DO UPDATE SET
    match_date = EXCLUDED.match_date,
    home_team = EXCLUDED.home_team,
    away_team = EXCLUDED.away_team,
    home_goals = EXCLUDED.home_goals,
    away_goals = EXCLUDED.away_goals;
"""

def load_matches_settings() -> dict[str, str]:
    load_dotenv(ENV_PATH)
    required_settings = {
        "POSTGRES_HOST",
        "POSTGRES_PORT",
        "POSTGRES_USER",
        "POSTGRES_PASSWORD",
        "POSTGRES_DB",
    }

    missing_settings = [
        setting for setting in required_settings if setting not in os.environ
    ]
    if missing_settings:
        raise RuntimeError(
            f"環境変数が不足しています: {', '.join(sorted(missing_settings))}"
        )

    return {setting: os.environ[setting] for setting in required_settings}

def read_and_validate_matches() -> pd.DataFrame:
    matches = pd.read_csv(CSV_PATH)

    missing_columns = REQUIRED_COLUMNS - set(matches.columns)
    if missing_columns:
        raise ValueError(
            f"CSVファイルに必要な列が不足しています: {', '.join(sorted(missing_columns))}"
        )

    if matches.duplicated(subset=["match_id"]).any():
        raise ValueError("CSVファイルに重複するmatch_idがあります。")

    for column in ["home_goals", "away_goals"]:
        matches[column] = pd.to_numeric(matches[column], errors="coerce")

        if (matches[column].isnull().any()):
            raise ValueError(f"列 '{column}' に数値以外の値が含まれています。")

        if (matches[column] < 0).any():
            raise ValueError(f"列 '{column}' に負の値が含まれています。")

    matches["match_date"] = pd.to_datetime(matches["match_date"], errors="coerce")
    if matches["match_date"].isnull().any():
        raise ValueError("列 'match_date' に無効な日付が含まれています。")

    return matches

def convert_to_records(matches: pd.DataFrame) -> list[tuple[int, object, str, str, int, int]]:
    return [
        (
            int(row.match_id),
            row.match_date,
            str(row.home_team),
            str(row.away_team),
            int(row.home_goals),
            int(row.away_goals),
        )
        for row in matches.itertuples(index=False)
    ]

def load_matches(
        settings: dict[str, str],
        records: list[tuple[int, object, str, str, int, int]]
) -> None:
    connection_string = (
        f"postgresql://{settings['POSTGRES_USER']}:{settings['POSTGRES_PASSWORD']}"
        f"@{settings['POSTGRES_HOST']}:{settings['POSTGRES_PORT']}/{settings['POSTGRES_DB']}"
    )

    with psycopg.connect(connection_string) as conn:
        with conn.cursor() as cur:
            cur.executemany(UPSERT_SQL, records)
            conn.commit()

def main() -> None:
    settings = load_matches_settings()
    matches = read_and_validate_matches()
    if matches.empty:
        print("CSVファイルに有効なマッチデータがありません。")
        return
    
    records = convert_to_records(matches)
    load_matches(settings, records)
    print(f"{len(records)}件の試合データを登録・更新しました。")

if __name__ == "__main__":
    main()