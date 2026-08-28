from pathlib import Path

from data_engineering_study.config import PROJECT_ROOT, get_postgres_settings
from data_engineering_study.extract.matches import extract_matches
from data_engineering_study.load.matches import load_matches
from data_engineering_study.transform.matches import transform_matches

CSV_PATH = (
    PROJECT_ROOT / "data" / "raw" / "matches.csv"
)

def main() -> None:
    settings = get_postgres_settings()
    matches = extract_matches(CSV_PATH)
    transformed_matches = transform_matches(matches)

    if transformed_matches.empty:
        print("登録対象の試合データがありません。")
        return

    load_matches(transformed_matches, settings)

    print(f"登録・更新対象の試合データ件数: {len(transformed_matches)}")

if __name__ == "__main__":
    main()
