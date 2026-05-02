from __future__ import annotations

import csv
from pathlib import Path


RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
SUPPORTED_SUFFIXES = {".csv", ".tsv"}


def detect_delimiter(file_path: Path) -> str:
    with file_path.open("r", encoding="utf-8-sig", newline="") as handle:
        sample = handle.read(4096)
        try:
            dialect = csv.Sniffer().sniff(sample, delimiters=",;\t|")
            return dialect.delimiter
        except csv.Error:
            return ","


def preview_file(file_path: Path) -> None:
    suffix = file_path.suffix.lower()
    print(f"\n=== {file_path.name} ===")

    if suffix not in SUPPORTED_SUFFIXES:
        print("Skipped: unsupported preview format.")
        return

    delimiter = detect_delimiter(file_path)

    with file_path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle, delimiter=delimiter)
        rows = []
        for index, row in enumerate(reader):
            rows.append(row)
            if index >= 5:
                break

    if not rows:
        print("File is empty.")
        return

    header = rows[0]
    print(f"Delimiter: {repr(delimiter)}")
    print("Columns:")
    for column in header:
        print(f"- {column}")

    print("\nSample rows:")
    for row in rows[1:]:
        print(row)


def main() -> None:
    files = sorted(
        path for path in RAW_DIR.iterdir() if path.is_file() and path.suffix.lower() in SUPPORTED_SUFFIXES
    )

    if not files:
        print("No supported raw files found in data/raw.")
        return

    for file_path in files:
        preview_file(file_path)


if __name__ == "__main__":
    main()
