import pandas as pd

REQUIRED_COLUMNS = {
    "match_id",
    "match_date",
    "home_team",
    "away_team",
    "home_goals",
    "away_goals",
}

def transform_matches(matches: pd.DataFrame) -> pd.DataFrame:
    transformed = matches.copy()

    missing_columns = REQUIRED_COLUMNS - set(transformed.columns)

    if missing_columns:
        raise ValueError(
            f"CSVファイルに必要な列が不足しています: {', '.join(sorted(missing_columns))}"
        )

    if transformed.duplicated(subset=["match_id"]).any():
        duplicate_ids = (
            transformed.loc[
                transformed.duplicated(), "match_id",
            ]
            .astype(str)
            .tolist()
        )

        raise ValueError(f"CSVファイルに重複するmatch_idがあります。重複するID: {', '.join(duplicate_ids)}")

    for column in ["home_goals", "away_goals"]:
        transformed[column] = pd.to_numeric(transformed[column], errors="raise")

        if (transformed[column] < 0).any():
            raise ValueError(f"列 '{column}' に負の値が含まれています。")

    transformed["season"] = (transformed["match_date"].dt.year)
    transformed["match_date"] = (transformed["match_date"].dt.date)

    return transformed