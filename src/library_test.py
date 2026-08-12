from pathlib import Path

import pandas as pd

def main() -> None:
    output_directory = Path("data/processed")
    output_directory.mkdir(parents=True, exist_ok=True)

    matches = pd.DataFrame(
        [
            {"team": "Hokkaido Consadole Sapporo", "goals": 3},
            {"team": "Vegalta Sendai", "goals": 1},
        ]
    )

    output_path = output_directory / "matches.parquet"
    matches.to_parquet(output_path, index=False)

    loaded_matches = pd.read_parquet(output_path)

    print(loaded_matches)
    print(f"\n保存先: {output_path}")

    separator = "\n"

    print(repr(separator))
    print([hex(ord(character)) for character in separator])

if __name__ == "__main__":
    main()
