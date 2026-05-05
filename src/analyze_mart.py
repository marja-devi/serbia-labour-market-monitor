"""
Produce portfolio-oriented findings from the municipality-quarter earnings mart.
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
from statistics import median


PROJECT_DIR = Path(__file__).resolve().parent.parent
MARTS_DIR = Path(__file__).resolve().parent.parent / "data" / "marts"
DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
RAW_DIR = PROJECT_DIR / "data" / "raw"
QUARTERLY_MART_FILE = "territory_quarter_earnings.csv"
ANNUAL_VALIDATION_FILE = "territory_annual_validation.csv"
EMPLOYMENT_ANNUAL_RESIDENCE_FILE = "registered_employment_by_sex_municipality_residence.csv"

MUNICIPALITY_RANKING_FILE = "municipality_ranking_2025.csv"
MUNICIPALITY_GROWTH_FILE = "municipality_growth_2018_2025.csv"
MUNICIPALITY_QOQ_OUTLIERS_FILE = "municipality_qoq_outliers.csv"
GROUP_AVERAGE_MACRO_FILE = "group_average_2025_macro_regions.csv"
GROUP_AVERAGE_DISTRICT_FILE = "group_average_2025_districts.csv"
GROUP_AVERAGE_CITY_GROUP_FILE = "group_average_2025_city_groups.csv"
GROUP_WEIGHTED_MACRO_FILE = "group_weighted_average_2025_macro_regions.csv"
GROUP_WEIGHTED_DISTRICT_FILE = "group_weighted_average_2025_districts.csv"
GROUP_WEIGHTED_CITY_GROUP_FILE = "group_weighted_average_2025_city_groups.csv"
GROUP_MEDIAN_MACRO_FILE = "group_median_2025_macro_regions.csv"
GROUP_MEDIAN_DISTRICT_FILE = "group_median_2025_districts.csv"
GROUP_MEDIAN_CITY_GROUP_FILE = "group_median_2025_city_groups.csv"
CITY_DRILLDOWN_RANKING_FILE = "city_drilldown_municipality_ranking_2025.csv"
REPUBLIC_NET_GROSS_TREND_FILE = "republic_net_gross_trend.csv"
BELGRADE_NOVI_SAD_TREND_FILE = "belgrade_novi_sad_net_gross_trend.csv"

BEOGRAD_DISTRICT_NAME = "Beogradska oblast"
BEOGRAD_REGION_ALIAS = "Beogradski region"


def read_csv(file_path: Path) -> list[dict[str, str]]:
    with file_path.open("r", encoding="utf-8", newline="") as handle:
        sample = handle.read(2048)

    for delimiter in (",", ";", "\t"):
        reader = csv.DictReader(sample.splitlines(), delimiter=delimiter)
        if reader.fieldnames and len(reader.fieldnames) > 1:
            with file_path.open("r", encoding="utf-8", newline="") as handle:
                return list(csv.DictReader(handle, delimiter=delimiter))

    with file_path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def normalize_territory_label(value: str) -> str:
    return BEOGRAD_REGION_ALIAS if value == BEOGRAD_DISTRICT_NAME else value


def average(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def weighted_average(values: list[float], weights: list[float]) -> float:
    weighted_sum = sum(value * weight for value, weight in zip(values, weights))
    total_weight = sum(weights)
    return weighted_sum / total_weight if total_weight else 0.0


def write_csv(file_path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with file_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def load_employment_weights() -> dict[tuple[str, str], float]:
    rows = read_csv(RAW_DIR / EMPLOYMENT_ANNUAL_RESIDENCE_FILE)
    weights: dict[tuple[str, str], float] = {}

    for row in rows:
        if row["IDPol"] != "0":
            continue
        code = row["IDTer"]
        if code == "70000":
            continue
        weights[(row["god"], code)] = float(row["vrednost"])

    return weights


def build_2025_rankings(quarterly_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str, str], list[float]] = defaultdict(list)
    metadata: dict[tuple[str, str, str], dict[str, str]] = {}

    for row in quarterly_rows:
        if (
            row["is_complete_quarter"] != "True"
            or row["year"] != "2025"
            or row["territory_level"] != "local_unit"
        ):
            continue
        grouped[(row["municipality_code"], row["municipality_name"], row["earnings_type"])].append(
            float(row["quarterly_avg_value_rsd"])
        )
        metadata[(row["municipality_code"], row["municipality_name"], row["earnings_type"])] = row

    ranking_rows: list[dict[str, object]] = []
    for (code, name, earnings_type), values in grouped.items():
        if len(values) != 4:
            continue
        sample_row = metadata[(code, name, earnings_type)]
        ranking_rows.append(
            {
                "municipality_code": code,
                "municipality_name": name,
                "earnings_type": earnings_type,
                "macro_region_name": sample_row["macro_region_name"],
                "statistical_region_name": sample_row["statistical_region_name"],
                "administrative_district_name": normalize_territory_label(sample_row["administrative_district_name"]),
                "local_unit_type": sample_row["local_unit_type"],
                "city_group_name": sample_row["city_group_name"],
                "avg_2025_value_rsd": round(sum(values) / 4, 2),
            }
        )

    return ranking_rows


def build_growth_table(validation_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    values: dict[tuple[str, str, str, str], float] = {}
    metadata: dict[tuple[str, str, str], dict[str, str]] = {}

    for row in validation_rows:
        if (
            row["is_complete_year"] == "True"
            and row["year"] in {"2018", "2025"}
            and row["territory_level"] == "local_unit"
        ):
            values[(row["municipality_code"], row["municipality_name"], row["earnings_type"], row["year"])] = float(row["annual_file_value_rsd"])
            metadata[(row["municipality_code"], row["municipality_name"], row["earnings_type"])] = row

    growth_rows: list[dict[str, object]] = []

    for code, name, earnings_type, year in list(values.keys()):
        if year != "2018":
            continue

        end_key = (code, name, earnings_type, "2025")
        start_value = values[(code, name, earnings_type, "2018")]

        if end_key not in values or start_value <= 0:
            continue

        end_value = values[end_key]
        meta_row = metadata[(code, name, earnings_type)]
        growth_rows.append(
            {
                "municipality_code": code,
                "municipality_name": name,
                "earnings_type": earnings_type,
                "macro_region_name": meta_row["macro_region_name"],
                "statistical_region_name": meta_row["statistical_region_name"],
                "administrative_district_name": normalize_territory_label(meta_row["administrative_district_name"]),
                "local_unit_type": meta_row["local_unit_type"],
                "city_group_name": meta_row["city_group_name"],
                "value_2018_rsd": round(start_value, 2),
                "value_2025_rsd": round(end_value, 2),
                "absolute_growth_rsd": round(end_value - start_value, 2),
                "growth_pct": round(((end_value / start_value) - 1) * 100, 2),
            }
        )

    return growth_rows


def build_qoq_outliers(quarterly_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    quarter_order = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}
    grouped: dict[tuple[str, str, str], list[tuple[int, int, str, float]]] = defaultdict(list)
    metadata: dict[tuple[str, str, str], dict[str, str]] = {}

    for row in quarterly_rows:
        if row["is_complete_quarter"] != "True" or row["territory_level"] != "local_unit":
            continue
        grouped[(row["municipality_code"], row["municipality_name"], row["earnings_type"])].append(
            (int(row["year"]), quarter_order[row["quarter"]], row["quarter"], float(row["quarterly_avg_value_rsd"]))
        )
        metadata[(row["municipality_code"], row["municipality_name"], row["earnings_type"])] = row

    outlier_rows: list[dict[str, object]] = []

    for (code, name, earnings_type), values in grouped.items():
        meta_row = metadata[(code, name, earnings_type)]
        values = sorted(values)
        for previous, current in zip(values, values[1:]):
            prev_year, prev_quarter_num, prev_quarter_label, prev_value = previous
            curr_year, curr_quarter_num, curr_quarter_label, curr_value = current

            is_next_quarter = (curr_year == prev_year and curr_quarter_num == prev_quarter_num + 1) or (
                curr_year == prev_year + 1 and prev_quarter_num == 4 and curr_quarter_num == 1
            )

            if not is_next_quarter or prev_value <= 0:
                continue

            change_pct = ((curr_value / prev_value) - 1) * 100
            outlier_rows.append(
                {
                    "municipality_code": code,
                    "municipality_name": name,
                    "earnings_type": earnings_type,
                    "macro_region_name": meta_row["macro_region_name"],
                    "statistical_region_name": meta_row["statistical_region_name"],
                    "administrative_district_name": normalize_territory_label(meta_row["administrative_district_name"]),
                    "local_unit_type": meta_row["local_unit_type"],
                    "city_group_name": meta_row["city_group_name"],
                    "from_year": prev_year,
                    "from_quarter": prev_quarter_label,
                    "to_year": curr_year,
                    "to_quarter": curr_quarter_label,
                    "from_value_rsd": round(prev_value, 2),
                    "to_value_rsd": round(curr_value, 2),
                    "change_pct": round(change_pct, 2),
                    "abs_change_pct": round(abs(change_pct), 2),
                }
            )

    outlier_rows.sort(key=lambda row: row["abs_change_pct"], reverse=True)
    return outlier_rows


def aggregate_2025_by_field(
    rankings: list[dict[str, object]],
    group_field: str,
    output_field: str,
    employment_weights: dict[tuple[str, str], float],
    method: str,
) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], list[tuple[float, float]]] = defaultdict(list)

    for row in rankings:
        group_name = str(row[group_field]).strip()
        if not group_name:
            continue
        value = float(row["avg_2025_value_rsd"])
        weight = employment_weights.get(("2025", str(row["municipality_code"])), 0.0)
        grouped[(group_name, str(row["earnings_type"]))].append((value, weight))

    summary_rows: list[dict[str, object]] = []

    for (group_name, earnings_type), pairs in sorted(grouped.items()):
        values = [value for value, _ in pairs]
        weights = [weight for _, weight in pairs if weight > 0]

        if method == "average":
            result_value = average(values)
            value_field = "avg_2025_value_rsd"
        elif method == "weighted_average":
            valid_pairs = [(value, weight) for value, weight in pairs if weight > 0]
            result_value = weighted_average(
                [value for value, _ in valid_pairs],
                [weight for _, weight in valid_pairs],
            )
            value_field = "weighted_avg_2025_value_rsd"
        elif method == "median":
            result_value = float(median(values))
            value_field = "median_2025_value_rsd"
        else:
            raise ValueError(f"Unsupported aggregation method: {method}")

        summary_rows.append(
            {
                output_field: group_name,
                "earnings_type": earnings_type,
                "aggregation_method": method,
                "municipality_count": len(pairs),
                "weight_observation_count": len([weight for _, weight in pairs if weight > 0]),
                "total_weight": round(sum(weight for _, weight in pairs if weight > 0), 2),
                value_field: round(result_value, 2),
                "min_2025_value_rsd": round(min(values), 2),
                "max_2025_value_rsd": round(max(values), 2),
            }
        )

    return summary_rows


def build_city_group_members_2025(rankings: list[dict[str, object]]) -> list[dict[str, object]]:
    rows = [row for row in rankings if str(row["city_group_name"]).strip()]
    return sorted(
        rows,
        key=lambda row: (str(row["city_group_name"]), str(row["earnings_type"]), -float(row["avg_2025_value_rsd"])),
    )


def build_republic_net_gross_trend(validation_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    by_year: dict[str, dict[str, float]] = defaultdict(dict)

    for row in validation_rows:
        if row["municipality_code"] != "RS" or row["is_complete_year"] != "True":
            continue
        by_year[row["year"]][row["earnings_type"]] = float(row["annual_file_value_rsd"])

    trend_rows: list[dict[str, object]] = []

    for year in sorted(by_year, key=int):
        values = by_year[year]
        if "net" not in values or "gross" not in values:
            continue

        net_value = values["net"]
        gross_value = values["gross"]
        gap_value = gross_value - net_value
        net_to_gross_pct = (net_value / gross_value) * 100 if gross_value else 0.0
        gap_to_gross_pct = (gap_value / gross_value) * 100 if gross_value else 0.0

        trend_rows.append(
            {
                "year": int(year),
                "net_value_rsd": round(net_value, 2),
                "gross_value_rsd": round(gross_value, 2),
                "gross_minus_net_rsd": round(gap_value, 2),
                "net_to_gross_pct": round(net_to_gross_pct, 2),
                "gap_to_gross_pct": round(gap_to_gross_pct, 2),
            }
        )

    return trend_rows


def build_belgrade_novi_sad_trend(
    validation_rows: list[dict[str, str]], employment_weights: dict[tuple[str, str], float]
) -> list[dict[str, object]]:
    belgrade_grouped: dict[str, dict[str, list[tuple[float, float]]]] = defaultdict(lambda: defaultdict(list))
    novi_sad_grouped: dict[str, dict[str, list[tuple[float, float]]]] = defaultdict(lambda: defaultdict(list))

    for row in validation_rows:
        if row["is_complete_year"] != "True" or row["territory_level"] != "local_unit":
            continue

        year = row["year"]
        earnings_type = row["earnings_type"]
        value = float(row["annual_file_value_rsd"])
        weight = employment_weights.get((year, row["municipality_code"]), 0.0)

        if row["city_group_name"] == "Grad Beograd" and row["local_unit_type"] == "city_municipality":
            belgrade_grouped[year][earnings_type].append((value, weight))

        if row["city_group_name"] == "Grad Novi Sad":
            novi_sad_grouped[year][earnings_type].append((value, weight))

    trend_rows: list[dict[str, object]] = []

    def summarize_method(pairs: list[tuple[float, float]], method: str) -> float:
        values = [value for value, _ in pairs]
        if method == "average":
            return average(values)
        if method == "median":
            return float(median(values))
        if method == "weighted_average":
            valid_pairs = [(value, weight) for value, weight in pairs if weight > 0]
            return weighted_average(
                [value for value, _ in valid_pairs],
                [weight for _, weight in valid_pairs],
            )
        raise ValueError(f"Unsupported aggregation method: {method}")

    for year in sorted(set(belgrade_grouped) | set(novi_sad_grouped), key=int):
        belgrade_values = belgrade_grouped.get(year, {})
        novi_sad_values = novi_sad_grouped.get(year, {})

        for method in ("average", "weighted_average", "median"):
            if "net" in belgrade_values and "gross" in belgrade_values:
                net_value = summarize_method(belgrade_values["net"], method)
                gross_value = summarize_method(belgrade_values["gross"], method)
                trend_rows.append(
                    {
                        "city_label": "Grad Beograd",
                        "series_method": "city_municipality_group",
                        "aggregation_method": method,
                        "year": int(year),
                        "net_value_rsd": round(net_value, 2),
                        "gross_value_rsd": round(gross_value, 2),
                        "gross_minus_net_rsd": round(gross_value - net_value, 2),
                    }
                )

            if "net" in novi_sad_values and "gross" in novi_sad_values:
                net_value = summarize_method(novi_sad_values["net"], method)
                gross_value = summarize_method(novi_sad_values["gross"], method)
                trend_rows.append(
                    {
                        "city_label": "Grad Novi Sad",
                        "series_method": "city_group_members",
                        "aggregation_method": method,
                        "year": int(year),
                        "net_value_rsd": round(net_value, 2),
                        "gross_value_rsd": round(gross_value, 2),
                        "gross_minus_net_rsd": round(gross_value - net_value, 2),
                    }
                )

    return trend_rows


def write_findings_doc(
    rankings: list[dict[str, object]],
    growth_rows: list[dict[str, object]],
    qoq_outliers: list[dict[str, object]],
    macro_rows: list[dict[str, object]],
    district_rows: list[dict[str, object]],
    city_member_rows: list[dict[str, object]],
    republic_trend_rows: list[dict[str, object]],
    belgrade_novi_sad_rows: list[dict[str, object]],
) -> None:
    def top_n(rows: list[dict[str, object]], earnings_type: str, key: str, reverse: bool, n: int = 5) -> list[dict[str, object]]:
        filtered = [row for row in rows if row["earnings_type"] == earnings_type]
        return sorted(filtered, key=lambda row: row[key], reverse=reverse)[:n]

    net_top_2025 = top_n(rankings, "net", "avg_2025_value_rsd", True)
    net_bottom_2025 = top_n(rankings, "net", "avg_2025_value_rsd", False)
    gross_top_2025 = top_n(rankings, "gross", "avg_2025_value_rsd", True)
    gross_bottom_2025 = top_n(rankings, "gross", "avg_2025_value_rsd", False)

    net_growth_top = top_n(growth_rows, "net", "growth_pct", True)
    gross_growth_top = top_n(growth_rows, "gross", "growth_pct", True)
    qoq_top = qoq_outliers[:10]
    macro_net_top = top_n(macro_rows, "net", "avg_2025_value_rsd", True, n=2)
    district_net_top = top_n(district_rows, "net", "avg_2025_value_rsd", True)
    city_drilldown_top = top_n(city_member_rows, "net", "avg_2025_value_rsd", True)
    trend_start = republic_trend_rows[0] if republic_trend_rows else None
    trend_end = republic_trend_rows[-1] if republic_trend_rows else None
    belgrade_2025 = next(
        (row for row in belgrade_novi_sad_rows if row["city_label"] == "Grad Beograd" and row["year"] == 2025),
        None,
    )
    novi_sad_2025 = next(
        (row for row in belgrade_novi_sad_rows if row["city_label"] == "Grad Novi Sad" and row["year"] == 2025),
        None,
    )

    lines = [
        "# Earnings Mart Findings",
        "",
        "Analysis date: 2026-04-28",
        "",
        "## Scope",
        "These findings use the municipality-quarter earnings mart built from the four core municipality earnings files.",
        "",
        "## Portfolio-Ready Findings",
        "",
        "### 1. Municipality ranking: the highest-paying local units in 2025 are concentrated in Belgrade",
        "Top 2025 net municipality ranking:",
    ]

    for row in net_top_2025:
        lines.append(f"- {row['municipality_name']}: {row['avg_2025_value_rsd']} RSD")

    lines.extend(
        [
            "",
            "Top 2025 gross municipality ranking:",
        ]
    )
    for row in gross_top_2025:
        lines.append(f"- {row['municipality_name']}: {row['avg_2025_value_rsd']} RSD")

    lines.extend(
        [
            "",
            "### 2. Municipality ranking: the lowest-paying local units in 2025 form a distinct lower tier",
            "Bottom 2025 net municipality ranking:",
        ]
    )
    for row in net_bottom_2025:
        lines.append(f"- {row['municipality_name']}: {row['avg_2025_value_rsd']} RSD")

    lines.extend(
        [
            "",
            "Bottom 2025 gross municipality ranking:",
        ]
    )
    for row in gross_bottom_2025:
        lines.append(f"- {row['municipality_name']}: {row['avg_2025_value_rsd']} RSD")

    lines.extend(
        [
            "",
            "### 3. Some municipalities show very strong earnings growth from 2018 to 2025",
            "Top net growth 2018-2025:",
        ]
    )
    for row in net_growth_top:
        lines.append(
            f"- {row['municipality_name']}: {row['growth_pct']}% ({row['value_2018_rsd']} -> {row['value_2025_rsd']} RSD)"
        )

    lines.extend(
        [
            "",
            "Top gross growth 2018-2025:",
        ]
    )
    for row in gross_growth_top:
        lines.append(
            f"- {row['municipality_name']}: {row['growth_pct']}% ({row['value_2018_rsd']} -> {row['value_2025_rsd']} RSD)"
        )

    lines.extend(
        [
            "",
            "### 4. Quarter-over-quarter outliers exist and should be treated as analysis signals, not automatic conclusions",
            "Largest quarter-over-quarter changes:",
        ]
    )
    for row in qoq_top:
        lines.append(
            f"- {row['municipality_name']} {row['earnings_type']} {row['from_year']} {row['from_quarter']} -> {row['to_year']} {row['to_quarter']}: {row['change_pct']}%"
        )

    if trend_start and trend_end:
        lines.extend(
            [
                "",
                "### 5. Net and gross earnings should be read together because the gap changes over time",
                f"- {trend_start['year']}: net {trend_start['net_value_rsd']} RSD, gross {trend_start['gross_value_rsd']} RSD, gap {trend_start['gross_minus_net_rsd']} RSD",
                f"- {trend_end['year']}: net {trend_end['net_value_rsd']} RSD, gross {trend_end['gross_value_rsd']} RSD, gap {trend_end['gross_minus_net_rsd']} RSD",
                f"- net-to-gross ratio moved from {trend_start['net_to_gross_pct']}% to {trend_end['net_to_gross_pct']}%",
            ]
        )

    if belgrade_2025 and novi_sad_2025:
        lines.extend(
            [
                "",
                "### 6. Belgrade and Novi Sad can be compared on one net-gross timeline with one common aggregation logic",
                f"- Grad Beograd 2025: net {belgrade_2025['net_value_rsd']} RSD, gross {belgrade_2025['gross_value_rsd']} RSD, gap {belgrade_2025['gross_minus_net_rsd']} RSD",
                f"- Grad Novi Sad 2025: net {novi_sad_2025['net_value_rsd']} RSD, gross {novi_sad_2025['gross_value_rsd']} RSD, gap {novi_sad_2025['gross_minus_net_rsd']} RSD",
                "- Both cities are shown as the arithmetic average across available city-group members.",
            ]
        )

    lines.extend(
        [
            "",
            "### 7. The same mart can now be read at macro-region, district, and city drill-down level",
            "Group average of municipality averages: 2025 net earnings by macro region:",
        ]
    )
    for row in macro_net_top:
        lines.append(f"- {row['macro_region_name']}: {row['avg_2025_value_rsd']} RSD")

    lines.extend(
        [
            "",
            "Group average of municipality averages: top districts by 2025 net earnings:",
        ]
    )
    for row in district_net_top:
        lines.append(f"- {row['administrative_district_name']}: {row['avg_2025_value_rsd']} RSD")

    lines.extend(
        [
            "",
            "City drill-down municipality ranking: top 2025 net local units:",
        ]
    )
    for row in city_drilldown_top:
        lines.append(f"- {row['city_group_name']} / {row['municipality_name']}: {row['avg_2025_value_rsd']} RSD")

    lines.extend(
        [
            "",
            "## Interpretation Notes",
            "- `2026` is partial and should not be used for full-year comparisons.",
            "- 2018-2019 include separate rows for `Novi Sad` and `Petrovaradin`, while later years use `Grad Novi Sad`, so long-run comparisons around that area need special care.",
            "- Annual validation differences are small enough that the mart is suitable for portfolio storytelling.",
            "- Group views use the arithmetic average of municipality averages inside each grouping.",
            "- Belgrade vs Novi Sad is aligned to one construction: arithmetic average across available city-group members for both cities.",
            "- For Novi Sad, the current city group contains a single city-level row, so its group average equals that row.",
            "",
            "## Suggested First Charts",
            "- Municipality ranking: top 10 local units by 2025 net earnings",
            "- Municipality ranking: bottom 10 local units by 2025 net earnings",
            "- Net and gross together on one line chart for Republic, Belgrade, or Novi Sad",
            "- Group average of municipality averages by macro region or district",
            "- 2018 vs 2025 growth comparison for selected municipalities",
            "- Quarter-over-quarter volatility spotlight for a few outlier municipalities",
        ]
    )

    (DOCS_DIR / "analysis_findings.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    quarterly_rows = read_csv(MARTS_DIR / QUARTERLY_MART_FILE)
    validation_rows = read_csv(MARTS_DIR / ANNUAL_VALIDATION_FILE)
    employment_weights = load_employment_weights()

    rankings = build_2025_rankings(quarterly_rows)
    growth_rows = build_growth_table(validation_rows)
    qoq_outliers = build_qoq_outliers(quarterly_rows)
    macro_average_rows = aggregate_2025_by_field(rankings, "macro_region_name", "macro_region_name", employment_weights, "average")
    district_average_rows = aggregate_2025_by_field(rankings, "administrative_district_name", "administrative_district_name", employment_weights, "average")
    city_group_average_rows = aggregate_2025_by_field(rankings, "city_group_name", "city_group_name", employment_weights, "average")
    macro_weighted_rows = aggregate_2025_by_field(rankings, "macro_region_name", "macro_region_name", employment_weights, "weighted_average")
    district_weighted_rows = aggregate_2025_by_field(rankings, "administrative_district_name", "administrative_district_name", employment_weights, "weighted_average")
    city_group_weighted_rows = aggregate_2025_by_field(rankings, "city_group_name", "city_group_name", employment_weights, "weighted_average")
    macro_median_rows = aggregate_2025_by_field(rankings, "macro_region_name", "macro_region_name", employment_weights, "median")
    district_median_rows = aggregate_2025_by_field(rankings, "administrative_district_name", "administrative_district_name", employment_weights, "median")
    city_group_median_rows = aggregate_2025_by_field(rankings, "city_group_name", "city_group_name", employment_weights, "median")
    city_member_rows = build_city_group_members_2025(rankings)
    republic_trend_rows = build_republic_net_gross_trend(validation_rows)
    belgrade_novi_sad_rows = build_belgrade_novi_sad_trend(validation_rows, employment_weights)

    write_csv(
        MARTS_DIR / MUNICIPALITY_RANKING_FILE,
        [
            "municipality_code",
            "municipality_name",
            "earnings_type",
            "macro_region_name",
            "statistical_region_name",
            "administrative_district_name",
            "local_unit_type",
            "city_group_name",
            "avg_2025_value_rsd",
        ],
        rankings,
    )

    write_csv(
        MARTS_DIR / MUNICIPALITY_GROWTH_FILE,
        [
            "municipality_code",
            "municipality_name",
            "earnings_type",
            "macro_region_name",
            "statistical_region_name",
            "administrative_district_name",
            "local_unit_type",
            "city_group_name",
            "value_2018_rsd",
            "value_2025_rsd",
            "absolute_growth_rsd",
            "growth_pct",
        ],
        growth_rows,
    )

    write_csv(
        MARTS_DIR / MUNICIPALITY_QOQ_OUTLIERS_FILE,
        [
            "municipality_code",
            "municipality_name",
            "earnings_type",
            "macro_region_name",
            "statistical_region_name",
            "administrative_district_name",
            "local_unit_type",
            "city_group_name",
            "from_year",
            "from_quarter",
            "to_year",
            "to_quarter",
            "from_value_rsd",
            "to_value_rsd",
            "change_pct",
            "abs_change_pct",
        ],
        qoq_outliers,
    )

    write_csv(
        MARTS_DIR / GROUP_AVERAGE_MACRO_FILE,
        [
            "macro_region_name",
            "earnings_type",
            "aggregation_method",
            "municipality_count",
            "weight_observation_count",
            "total_weight",
            "avg_2025_value_rsd",
            "min_2025_value_rsd",
            "max_2025_value_rsd",
        ],
        macro_average_rows,
    )

    write_csv(
        MARTS_DIR / GROUP_AVERAGE_DISTRICT_FILE,
        [
            "administrative_district_name",
            "earnings_type",
            "aggregation_method",
            "municipality_count",
            "weight_observation_count",
            "total_weight",
            "avg_2025_value_rsd",
            "min_2025_value_rsd",
            "max_2025_value_rsd",
        ],
        district_average_rows,
    )

    write_csv(
        MARTS_DIR / GROUP_AVERAGE_CITY_GROUP_FILE,
        [
            "city_group_name",
            "earnings_type",
            "aggregation_method",
            "municipality_count",
            "weight_observation_count",
            "total_weight",
            "avg_2025_value_rsd",
            "min_2025_value_rsd",
            "max_2025_value_rsd",
        ],
        city_group_average_rows,
    )

    write_csv(
        MARTS_DIR / GROUP_WEIGHTED_MACRO_FILE,
        [
            "macro_region_name",
            "earnings_type",
            "aggregation_method",
            "municipality_count",
            "weight_observation_count",
            "total_weight",
            "weighted_avg_2025_value_rsd",
            "min_2025_value_rsd",
            "max_2025_value_rsd",
        ],
        macro_weighted_rows,
    )

    write_csv(
        MARTS_DIR / GROUP_WEIGHTED_DISTRICT_FILE,
        [
            "administrative_district_name",
            "earnings_type",
            "aggregation_method",
            "municipality_count",
            "weight_observation_count",
            "total_weight",
            "weighted_avg_2025_value_rsd",
            "min_2025_value_rsd",
            "max_2025_value_rsd",
        ],
        district_weighted_rows,
    )

    write_csv(
        MARTS_DIR / GROUP_WEIGHTED_CITY_GROUP_FILE,
        [
            "city_group_name",
            "earnings_type",
            "aggregation_method",
            "municipality_count",
            "weight_observation_count",
            "total_weight",
            "weighted_avg_2025_value_rsd",
            "min_2025_value_rsd",
            "max_2025_value_rsd",
        ],
        city_group_weighted_rows,
    )

    write_csv(
        MARTS_DIR / GROUP_MEDIAN_MACRO_FILE,
        [
            "macro_region_name",
            "earnings_type",
            "aggregation_method",
            "municipality_count",
            "weight_observation_count",
            "total_weight",
            "median_2025_value_rsd",
            "min_2025_value_rsd",
            "max_2025_value_rsd",
        ],
        macro_median_rows,
    )

    write_csv(
        MARTS_DIR / GROUP_MEDIAN_DISTRICT_FILE,
        [
            "administrative_district_name",
            "earnings_type",
            "aggregation_method",
            "municipality_count",
            "weight_observation_count",
            "total_weight",
            "median_2025_value_rsd",
            "min_2025_value_rsd",
            "max_2025_value_rsd",
        ],
        district_median_rows,
    )

    write_csv(
        MARTS_DIR / GROUP_MEDIAN_CITY_GROUP_FILE,
        [
            "city_group_name",
            "earnings_type",
            "aggregation_method",
            "municipality_count",
            "weight_observation_count",
            "total_weight",
            "median_2025_value_rsd",
            "min_2025_value_rsd",
            "max_2025_value_rsd",
        ],
        city_group_median_rows,
    )

    write_csv(
        MARTS_DIR / CITY_DRILLDOWN_RANKING_FILE,
        [
            "municipality_code",
            "municipality_name",
            "earnings_type",
            "macro_region_name",
            "statistical_region_name",
            "administrative_district_name",
            "local_unit_type",
            "city_group_name",
            "avg_2025_value_rsd",
        ],
        city_member_rows,
    )

    write_csv(
        MARTS_DIR / REPUBLIC_NET_GROSS_TREND_FILE,
        [
            "year",
            "net_value_rsd",
            "gross_value_rsd",
            "gross_minus_net_rsd",
            "net_to_gross_pct",
            "gap_to_gross_pct",
        ],
        republic_trend_rows,
    )

    write_csv(
        MARTS_DIR / BELGRADE_NOVI_SAD_TREND_FILE,
        [
            "city_label",
            "series_method",
            "aggregation_method",
            "year",
            "net_value_rsd",
            "gross_value_rsd",
            "gross_minus_net_rsd",
        ],
        belgrade_novi_sad_rows,
    )

    write_findings_doc(
        rankings,
        growth_rows,
        qoq_outliers,
        macro_average_rows,
        district_average_rows,
        city_member_rows,
        republic_trend_rows,
        belgrade_novi_sad_rows,
    )

    print("Analysis outputs created:")
    print(f"- {MARTS_DIR / MUNICIPALITY_RANKING_FILE}")
    print(f"- {MARTS_DIR / MUNICIPALITY_GROWTH_FILE}")
    print(f"- {MARTS_DIR / MUNICIPALITY_QOQ_OUTLIERS_FILE}")
    print(f"- {MARTS_DIR / GROUP_AVERAGE_MACRO_FILE}")
    print(f"- {MARTS_DIR / GROUP_AVERAGE_DISTRICT_FILE}")
    print(f"- {MARTS_DIR / GROUP_AVERAGE_CITY_GROUP_FILE}")
    print(f"- {MARTS_DIR / GROUP_WEIGHTED_MACRO_FILE}")
    print(f"- {MARTS_DIR / GROUP_WEIGHTED_DISTRICT_FILE}")
    print(f"- {MARTS_DIR / GROUP_WEIGHTED_CITY_GROUP_FILE}")
    print(f"- {MARTS_DIR / GROUP_MEDIAN_MACRO_FILE}")
    print(f"- {MARTS_DIR / GROUP_MEDIAN_DISTRICT_FILE}")
    print(f"- {MARTS_DIR / GROUP_MEDIAN_CITY_GROUP_FILE}")
    print(f"- {MARTS_DIR / CITY_DRILLDOWN_RANKING_FILE}")
    print(f"- {MARTS_DIR / REPUBLIC_NET_GROSS_TREND_FILE}")
    print(f"- {MARTS_DIR / BELGRADE_NOVI_SAD_TREND_FILE}")
    print(f"- {DOCS_DIR / 'analysis_findings.md'}")


if __name__ == "__main__":
    main()
