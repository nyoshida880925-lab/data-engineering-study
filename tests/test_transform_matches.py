import pandas as pd
import pytest

from src.transform.matches import transform_matches

def test_transform_matches_success():
    matches = pd.DataFrame(
        [
            {
                "match_id": 1,
                "match_date": "2026-07-01",
                "home_team": "Sapporo",
                "away_team": "Sendai",
                "home_goals": "3",
                "away_goals": "1",
            }
        ]
    )

    matches["match_date"] = pd.to_datetime(
        matches["match_date"]
    )

    result = transform_matches(matches)

    assert result.iloc[0]["season"] == 2026
    assert result.iloc[0]["home_goals"] == 3
    assert result.iloc[0]["away_goals"] == 1

def test_transform_matches_negative_goal():
    matches = pd.DataFrame(
        [
            {
                "match_id": 1,
                "match_date": "2026-07-01",
                "home_team": "Sapporo",
                "away_team": "Sendai",
                "home_goals": "-1",
                "away_goals": "1",
            }
        ]
    )

    matches["match_date"] = pd.to_datetime(
        matches["match_date"]
    )

    with pytest.raises(ValueError, match="列 'home_goals' に負の値が含まれています。"):
        transform_matches(matches)
