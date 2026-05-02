"""
Validate staged and mart outputs for the municipality earnings workflow.
"""

from __future__ import annotations

import csv
from pathlib import Path


STAGING_DIR = Path(__file__).resolve().parent.parent / "data" / "staging"
MARTS_DIR = Path(__file__).resolve().parent.parent / "data" / "marts"
QUARTERLY_MART_FILE = "territory_quarter_earnings.csv"
ANNUAL_VALIDATION_FILE = "territory_annual_validation.csv"


def read_csv(file_path: Path) -> list[dict[str, str]]:
    with file_path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def validate_staging(monthly_rows: list[dict[str, str]], annual_rows: list[dict[str, str]]) -> None:
    require(monthly_rows, "Monthly staging file is empty.")
    require(annual_rows, "Annual staging file is empty.")
    require(
        all(row["earnings_type"] in {"net", "gross"} for row in monthly_rows),
        "Monthly staging file contains unexpected earnings_type values.",
    )
    require(
        all(row["quarter"] in {"Q1", "Q2", "Q3", "Q4"} for row in monthly_rows),
        "Monthly staging file contains invalid quarter values.",
    )
    require(
        all(row["status_code"] == "A" for row in monthly_rows + annual_rows),
        "Expected only status_code A in the core municipality earnings files.",
    )


def validate_mart_rows(quarterly_rows: list[dict[str, str]], validation_rows: list[dict[str, str]]) -> None:
    require(quarterly_rows, "Quarterly mart file is empty.")
    require(validation_rows, "Annual validation file is empty.")
    require(
        all(row["territory_level"] for row in quarterly_rows + validation_rows),
        "Territory enrichment fields are missing in mart outputs.",
    )
    require(
        any(row["territory_level"] == "local_unit" for row in quarterly_rows),
        "Quarterly mart should include local-unit rows.",
    )
    require(
        all(int(row["months_in_quarter"]) in {1, 2, 3} for row in quarterly_rows),
        "Quarterly mart contains invalid months_in_quarter values.",
    )
    require(
        any(row["is_complete_quarter"] == "False" for row in quarterly_rows),
        "Expected at least one incomplete quarter because 2026 data is partial.",
    )
    require(
        any(row["is_complete_year"] == "False" for row in validation_rows),
        "Expected at least one incomplete year because 2026 data is partial.",
    )


def summarize_validation(validation_rows: list[dict[str, str]]) -> dict[str, float]:
    complete_rows = [row for row in validation_rows if row["is_complete_year"] == "True" and row["annual_file_value_rsd"]]
    diffs = [abs(float(row["difference_rsd"])) for row in complete_rows]

    return {
        "complete_year_rows": len(complete_rows),
        "avg_abs_diff_rsd": round(sum(diffs) / len(diffs), 2),
        "max_abs_diff_rsd": round(max(diffs), 2),
    }


def main() -> None:
    monthly_rows = read_csv(STAGING_DIR / "stg_earnings_monthly.csv")
    annual_rows = read_csv(STAGING_DIR / "stg_earnings_annual.csv")
    quarterly_rows = read_csv(MARTS_DIR / QUARTERLY_MART_FILE)
    validation_rows = read_csv(MARTS_DIR / ANNUAL_VALIDATION_FILE)

    validate_staging(monthly_rows, annual_rows)
    validate_mart_rows(quarterly_rows, validation_rows)
    summary = summarize_validation(validation_rows)

    print("Validation checks passed.")
    print(f"Monthly staging rows: {len(monthly_rows)}")
    print(f"Annual staging rows: {len(annual_rows)}")
    print(f"Quarter mart rows: {len(quarterly_rows)}")
    print(f"Complete annual check rows: {summary['complete_year_rows']}")
    print(f"Average absolute annual diff (RSD): {summary['avg_abs_diff_rsd']}")
    print(f"Maximum absolute annual diff (RSD): {summary['max_abs_diff_rsd']}")


if __name__ == "__main__":
    main()
