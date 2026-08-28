import pandas as pd
import psycopg

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

def load_matches(
        matches: pd.DataFrame,
        settings: dict[str, str],
) -> None:

    records = [
        (
            int(row.match_id),
            row.match_date,
            str(row.home_team),
            str(row.away_team),
            int(row.home_goals),
            int(row.away_goals)
        )
        for row in matches.itertuples(index=False)
    ]

    with psycopg.connect(
        host=settings["POSTGRES_HOST"],
        port=settings["POSTGRES_PORT"],
        user=settings["POSTGRES_USER"],
        password=settings["POSTGRES_PASSWORD"],
        dbname=settings["POSTGRES_DB"],
    ) as conn:
        with conn.cursor() as cur:
            cur.executemany(UPSERT_SQL, records)

