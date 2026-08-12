from pathlib import Path

from config import PROJECT_ROOT, get_postgres_settings
from extract.matches import extract_matches
from load.matches import load_matches
from transform.matches import transform_matches

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
