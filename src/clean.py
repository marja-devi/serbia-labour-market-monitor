"""
Build staging outputs for the municipality earnings files currently used by the project.
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable


RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
STAGING_DIR = Path(__file__).resolve().parent.parent / "data" / "staging"

MONTHLY_FILES = {
    "avg_monthly_net_earnings_municipality_residence.csv": "net",
    "avg_monthly_gross_earnings_municipality_residence.csv": "gross",
}

ANNUAL_FILES = {
    "annual_avg_monthly_net_earnings_municipality_residence.csv": "net",
    "annual_avg_monthly_gross_earnings_municipality_residence.csv": "gross",
}


def quarter_from_month(month: int) -> str:
    return f"Q{((month - 1) // 3) + 1}"


def read_semicolon_csv(file_path: Path) -> list[dict[str, str]]:
    with file_path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


def write_csv(file_path: Path, fieldnames: list[str], rows: Iterable[dict[str, object]]) -> None:
    with file_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_monthly_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for file_name, earnings_type in MONTHLY_FILES.items():
        raw_rows = read_semicolon_csv(RAW_DIR / file_name)

        for raw_row in raw_rows:
            month = int(raw_row["mes"])
            year = int(raw_row["god"])
            value_rsd = int(raw_row["vrednost"])

            rows.append(
                {
                    "source_file": file_name,
                    "indicator_code": raw_row["idindikator"],
                    "indicator_name": raw_row["Indikator"],
                    "earnings_type": earnings_type,
                    "municipality_code": raw_row["IDTer"],
                    "municipality_name": raw_row["nTer"],
                    "year": year,
                    "month": month,
                    "quarter": quarter_from_month(month),
                    "year_month": f"{year}-{month:02d}",
                    "value_rsd": value_rsd,
                    "unit_code": raw_row["idJedinicaMere"],
                    "unit_name": raw_row["nJedinicaMere"],
                    "status_code": raw_row["IDStatusPodatka"],
                    "status_name": raw_row["nStatusPodatka"],
                    "source_org": raw_row["nIzvorI"],
                }
            )

    return rows


def build_annual_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []

    for file_name, earnings_type in ANNUAL_FILES.items():
        raw_rows = read_semicolon_csv(RAW_DIR / file_name)

        for raw_row in raw_rows:
            year = int(raw_row["god"])
            value_rsd = int(raw_row["vrednost"])

            rows.append(
                {
                    "source_file": file_name,
                    "indicator_code": raw_row["idindikator"],
                    "indicator_name": raw_row["Indikator"],
                    "earnings_type": earnings_type,
                    "municipality_code": raw_row["IDTer"],
                    "municipality_name": raw_row["nTer"],
                    "year": year,
                    "value_rsd": value_rsd,
                    "unit_code": raw_row["idJedinicaMere"],
                    "unit_name": raw_row["nJedinicaMere"],
                    "status_code": raw_row["IDStatusPodatka"],
                    "status_name": raw_row["nStatusPodatka"],
                    "source_org": raw_row["nIzvorI"],
                }
            )

    return rows


def build_municipality_dimension(
    monthly_rows: list[dict[str, object]], annual_rows: list[dict[str, object]]
) -> list[dict[str, object]]:
    seen: dict[str, str] = {}

    for row in monthly_rows + annual_rows:
        seen[str(row["municipality_code"])] = str(row["municipality_name"])

    return [
        {"municipality_code": code, "municipality_name": name}
        for code, name in sorted(seen.items(), key=lambda item: item[0])
    ]


def main() -> None:
    STAGING_DIR.mkdir(parents=True, exist_ok=True)

    monthly_rows = build_monthly_rows()
    annual_rows = build_annual_rows()
    municipality_rows = build_municipality_dimension(monthly_rows, annual_rows)

    write_csv(
        STAGING_DIR / "stg_earnings_monthly.csv",
        [
            "source_file",
            "indicator_code",
            "indicator_name",
            "earnings_type",
            "municipality_code",
            "municipality_name",
            "year",
            "month",
            "quarter",
            "year_month",
            "value_rsd",
            "unit_code",
            "unit_name",
            "status_code",
            "status_name",
            "source_org",
        ],
        monthly_rows,
    )

    write_csv(
        STAGING_DIR / "stg_earnings_annual.csv",
        [
            "source_file",
            "indicator_code",
            "indicator_name",
            "earnings_type",
            "municipality_code",
            "municipality_name",
            "year",
            "value_rsd",
            "unit_code",
            "unit_name",
            "status_code",
            "status_name",
            "source_org",
        ],
        annual_rows,
    )

    write_csv(
        STAGING_DIR / "dim_municipality_from_earnings.csv",
        ["municipality_code", "municipality_name"],
        municipality_rows,
    )

    print("Staging files created:")
    print(f"- {STAGING_DIR / 'stg_earnings_monthly.csv'} ({len(monthly_rows)} rows)")
    print(f"- {STAGING_DIR / 'stg_earnings_annual.csv'} ({len(annual_rows)} rows)")
    print(f"- {STAGING_DIR / 'dim_municipality_from_earnings.csv'} ({len(municipality_rows)} rows)")


if __name__ == "__main__":
    main()
