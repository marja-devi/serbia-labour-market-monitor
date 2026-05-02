"""
Run focused quality checks for the municipality earnings workflow.
"""

from __future__ import annotations

import csv
from collections import Counter, defaultdict
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent.parent / "data"
QUARTERLY_MART_FILE = "territory_quarter_earnings.csv"
ANNUAL_VALIDATION_FILE = "territory_annual_validation.csv"


def read_csv(file_path: Path) -> list[dict[str, str]]:
    with file_path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def summarize() -> str:
    monthly = read_csv(DATA_DIR / "staging" / "stg_earnings_monthly.csv")
    annual = read_csv(DATA_DIR / "staging" / "stg_earnings_annual.csv")
    quarterly = read_csv(DATA_DIR / "marts" / QUARTERLY_MART_FILE)
    validation = read_csv(DATA_DIR / "marts" / ANNUAL_VALIDATION_FILE)

    monthly_keys = [(r["municipality_code"], r["year"], r["month"], r["earnings_type"]) for r in monthly]
    annual_keys = [(r["municipality_code"], r["year"], r["earnings_type"]) for r in annual]
    quarterly_keys = [(r["municipality_code"], r["year"], r["quarter"], r["earnings_type"]) for r in quarterly]

    name_conflicts = defaultdict(set)
    for row in monthly + annual:
        name_conflicts[row["municipality_code"]].add(row["municipality_name"])

    monthly_net = {(r["municipality_code"], r["year"], r["month"]) for r in monthly if r["earnings_type"] == "net"}
    monthly_gross = {(r["municipality_code"], r["year"], r["month"]) for r in monthly if r["earnings_type"] == "gross"}
    annual_net = {(r["municipality_code"], r["year"]) for r in annual if r["earnings_type"] == "net"}
    annual_gross = {(r["municipality_code"], r["year"]) for r in annual if r["earnings_type"] == "gross"}

    incomplete_quarters = Counter(
        (r["year"], r["quarter"], r["earnings_type"]) for r in quarterly if r["is_complete_quarter"] == "False"
    )

    complete_validation = [
        r for r in validation if r["is_complete_year"] == "True" and r["annual_file_value_rsd"]
    ]
    abs_diffs = [abs(float(r["difference_rsd"])) for r in complete_validation]
    top_outliers = sorted(complete_validation, key=lambda r: abs(float(r["difference_rsd"])), reverse=True)[:5]

    lines = [
        "Municipality earnings quality report",
        f"Monthly staging rows: {len(monthly)}",
        f"Annual staging rows: {len(annual)}",
        f"Quarter mart rows: {len(quarterly)}",
        f"Annual validation rows: {len(validation)}",
        "",
        "Key integrity",
        f"- Monthly duplicate business keys: {sum(c - 1 for c in Counter(monthly_keys).values() if c > 1)}",
        f"- Annual duplicate business keys: {sum(c - 1 for c in Counter(annual_keys).values() if c > 1)}",
        f"- Quarter mart duplicate business keys: {sum(c - 1 for c in Counter(quarterly_keys).values() if c > 1)}",
        f"- Municipality name conflicts by code: {sum(1 for names in name_conflicts.values() if len(names) > 1)}",
        "",
        "Net/gross parity",
        f"- Monthly net keys missing in gross: {len(monthly_net - monthly_gross)}",
        f"- Monthly gross keys missing in net: {len(monthly_gross - monthly_net)}",
        f"- Annual net keys missing in gross: {len(annual_net - annual_gross)}",
        f"- Annual gross keys missing in net: {len(annual_gross - annual_net)}",
        "",
        "Coverage",
        f"- Incomplete quarter rows: {sum(1 for r in quarterly if r['is_complete_quarter'] == 'False')}",
        f"- Incomplete year validation rows: {sum(1 for r in validation if r['is_complete_year'] == 'False')}",
        f"- Incomplete quarter breakdown: {dict(sorted(incomplete_quarters.items()))}",
        "",
        "Annual comparison",
        f"- Complete annual comparison rows: {len(complete_validation)}",
        f"- Average absolute difference (RSD): {round(sum(abs_diffs) / len(abs_diffs), 2)}",
        f"- Maximum absolute difference (RSD): {round(max(abs_diffs), 2)}",
        "",
        "Largest annual comparison outliers",
    ]

    for row in top_outliers:
        lines.append(
            f"- {row['municipality_code']} {row['municipality_name']} {row['year']} {row['earnings_type']}: {row['difference_rsd']} RSD"
        )

    return "\n".join(lines)


def main() -> None:
    print(summarize())


if __name__ == "__main__":
    main()
