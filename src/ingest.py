from pathlib import Path


RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"


def main() -> None:
    files = sorted(
        path for path in RAW_DIR.iterdir() if path.is_file() and not path.name.startswith(".")
    )
    print("Raw data directory:", RAW_DIR)

    if not files:
        print("No raw files found. Add source datasets into data/raw first.")
        return

    print("Discovered raw files:")
    for file_path in files:
        print(f"- {file_path.name}")


if __name__ == "__main__":
    main()
