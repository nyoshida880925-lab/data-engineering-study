from data_engineering_study.config import PROJECT_ROOT
from data_engineering_study.extract.matches import extract_matches
from data_engineering_study.load.parquet import save_as_partitioned_parquet
from data_engineering_study.transform.matches import transform_matches

CSV_PATH = (
    PROJECT_ROOT / "data" / "raw" / "matches.csv"
)
PARQUET_PATH = (
    PROJECT_ROOT / "data" / "processed" / "matches"
)

def main() -> None:
    matches = extract_matches(CSV_PATH)
    transformed_matches = transform_matches(matches)

    if transformed_matches.empty:
        print("登録対象の試合データがありません。")
        return

    save_as_partitioned_parquet(transformed_matches, PARQUET_PATH)

    print(
        f"{len(transformed_matches)}件を"
        f"{PARQUET_PATH}へ保存しました。"
    )

if __name__ == "__main__":
    main()
