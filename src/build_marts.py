"""
Build municipality-quarter earnings marts from staged SORS wage files.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean


STAGING_DIR = Path(__file__).resolve().parent.parent / "data" / "staging"
MARTS_DIR = Path(__file__).resolve().parent.parent / "data" / "marts"
REFERENCE_DIR = Path(__file__).resolve().parent.parent / "data" / "reference"
QUARTERLY_MART_FILE = "territory_quarter_earnings.csv"
ANNUAL_VALIDATION_FILE = "territory_annual_validation.csv"
MART_SUMMARY_FILE = "territory_mart_summary.txt"

TERRITORY_FIELDS = [
    "territory_level",
    "territory_level_order",
    "parent_territory_code",
    "parent_territory_name",
    "country_code",
    "country_name",
    "macro_region_code",
    "macro_region_name",
    "statistical_region_code",
    "statistical_region_name",
    "administrative_district_code",
    "administrative_district_name",
    "local_unit_type",
    "city_group_code",
    "city_group_name",
]


def read_csv(file_path: Path) -> list[dict[str, str]]:
    with file_path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(file_path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with file_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_territory_lookup() -> dict[str, dict[str, str]]:
    rows = read_csv(REFERENCE_DIR / "territory_dictionary.csv")
    return {row["territory_code"]: row for row in rows}


def territory_values(territory_lookup: dict[str, dict[str, str]], territory_code: str) -> dict[str, object]:
    territory_row = territory_lookup[territory_code]
    return {field: territory_row[field] for field in TERRITORY_FIELDS}


def build_quarterly_mart(
    monthly_rows: list[dict[str, str]], territory_lookup: dict[str, dict[str, str]]
) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, str, str, str], list[dict[str, str]]] = defaultdict(list)

    for row in monthly_rows:
        key = (
            row["municipality_code"],
            row["municipality_name"],
            row["year"],
            row["quarter"],
            row["earnings_type"],
        )
        grouped[key].append(row)

    mart_rows: list[dict[str, object]] = []

    for key in sorted(grouped):
        municipality_code, municipality_name, year, quarter, earnings_type = key
        rows = grouped[key]
        months = sorted(int(row["month"]) for row in rows)
        values = [int(row["value_rsd"]) for row in rows]

        mart_rows.append(
            {
                "municipality_code": municipality_code,
                "municipality_name": municipality_name,
                "year": int(year),
                "quarter": quarter,
                "earnings_type": earnings_type,
                **territory_values(territory_lookup, municipality_code),
                "quarterly_avg_value_rsd": round(mean(values), 2),
                "months_in_quarter": len(rows),
                "is_complete_quarter": len(rows) == 3,
                "month_list": ",".join(f"{month:02d}" for month in months),
                "min_month_value_rsd": min(values),
                "max_month_value_rsd": max(values),
            }
        )

    return mart_rows


def build_annual_validation(
    monthly_rows: list[dict[str, str]],
    annual_rows: list[dict[str, str]],
    territory_lookup: dict[str, dict[str, str]],
) -> list[dict[str, object]]:
    monthly_grouped: dict[tuple[str, str, str], list[int]] = defaultdict(list)
    annual_lookup: dict[tuple[str, str, str], int] = {}
    municipality_names: dict[str, str] = {}

    for row in monthly_rows:
        key = (row["municipality_code"], row["year"], row["earnings_type"])
        monthly_grouped[key].append(int(row["value_rsd"]))
        municipality_names[row["municipality_code"]] = row["municipality_name"]

    for row in annual_rows:
        key = (row["municipality_code"], row["year"], row["earnings_type"])
        annual_lookup[key] = int(row["value_rsd"])
        municipality_names[row["municipality_code"]] = row["municipality_name"]

    validation_rows: list[dict[str, object]] = []

    for key in sorted(monthly_grouped):
        municipality_code, year, earnings_type = key
        monthly_values = monthly_grouped[key]
        annual_value = annual_lookup.get(key)

        validation_rows.append(
            {
                "municipality_code": municipality_code,
                "municipality_name": municipality_names[municipality_code],
                "year": int(year),
                "earnings_type": earnings_type,
                **territory_values(territory_lookup, municipality_code),
                "monthly_observation_count": len(monthly_values),
                "is_complete_year": len(monthly_values) == 12,
                "monthly_avg_value_rsd": round(mean(monthly_values), 2),
                "annual_file_value_rsd": annual_value,
                "difference_rsd": round(mean(monthly_values) - annual_value, 2) if annual_value is not None else "",
            }
        )

    return validation_rows


def build_summary_report(
    quarterly_rows: list[dict[str, object]], validation_rows: list[dict[str, object]]
) -> str:
    complete_quarters = sum(1 for row in quarterly_rows if row["is_complete_quarter"])
    complete_years = sum(1 for row in validation_rows if row["is_complete_year"])
    total_quarters = len(quarterly_rows)
    total_years = len(validation_rows)

    return "\n".join(
        [
            "Municipality-quarter earnings mart summary",
            f"Quarter rows: {total_quarters}",
            f"Complete quarter rows: {complete_quarters}",
            f"Annual validation rows: {total_years}",
            f"Complete year validation rows: {complete_years}",
        ]
    )


def main() -> None:
    MARTS_DIR.mkdir(parents=True, exist_ok=True)

    monthly_rows = read_csv(STAGING_DIR / "stg_earnings_monthly.csv")
    annual_rows = read_csv(STAGING_DIR / "stg_earnings_annual.csv")
    territory_lookup = build_territory_lookup()

    quarterly_rows = build_quarterly_mart(monthly_rows, territory_lookup)
    validation_rows = build_annual_validation(monthly_rows, annual_rows, territory_lookup)
    summary_text = build_summary_report(quarterly_rows, validation_rows)

    write_csv(
        MARTS_DIR / QUARTERLY_MART_FILE,
        [
            "municipality_code",
            "municipality_name",
            "year",
            "quarter",
            "earnings_type",
            *TERRITORY_FIELDS,
            "quarterly_avg_value_rsd",
            "months_in_quarter",
            "is_complete_quarter",
            "month_list",
            "min_month_value_rsd",
            "max_month_value_rsd",
        ],
        quarterly_rows,
    )

    write_csv(
        MARTS_DIR / ANNUAL_VALIDATION_FILE,
        [
            "municipality_code",
            "municipality_name",
            "year",
            "earnings_type",
            *TERRITORY_FIELDS,
            "monthly_observation_count",
            "is_complete_year",
            "monthly_avg_value_rsd",
            "annual_file_value_rsd",
            "difference_rsd",
        ],
        validation_rows,
    )

    (MARTS_DIR / MART_SUMMARY_FILE).write_text(summary_text + "\n", encoding="utf-8")

    print("Mart files created:")
    print(f"- {MARTS_DIR / QUARTERLY_MART_FILE} ({len(quarterly_rows)} rows)")
    print(f"- {MARTS_DIR / ANNUAL_VALIDATION_FILE} ({len(validation_rows)} rows)")
    print(f"- {MARTS_DIR / MART_SUMMARY_FILE}")


if __name__ == "__main__":
    main()
