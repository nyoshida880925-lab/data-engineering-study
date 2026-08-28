from pathlib import Path

import pandas as pd

def extract_matches(csv_path: Path) -> pd.DataFrame:
    return pd.read_csv(
        csv_path, 
        parse_dates=["match_date"],
    )
