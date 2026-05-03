"""
Render a lightweight local HTML report with SVG charts for the earnings project.
"""

from __future__ import annotations

import csv
import html
from collections import defaultdict
from pathlib import Path
from statistics import median


PROJECT_DIR = Path(__file__).resolve().parent.parent
MARTS_DIR = PROJECT_DIR / "data" / "marts"
REFERENCE_DIR = PROJECT_DIR / "data" / "reference"
DOCS_DIR = PROJECT_DIR / "docs"
APP_DIR = PROJECT_DIR / "app"
GITHUB_REPO_URL = "https://github.com/marja-devi/serbia-labour-market-monitor"

MUNICIPALITY_RANKING_FILE = "municipality_ranking_2025.csv"
MUNICIPALITY_GROWTH_FILE = "municipality_growth_2018_2025.csv"
MUNICIPALITY_QOQ_OUTLIERS_FILE = "municipality_qoq_outliers.csv"
GROUP_MEDIAN_MACRO_FILE = "group_median_2025_macro_regions.csv"
GROUP_MEDIAN_DISTRICT_FILE = "group_median_2025_districts.csv"
CITY_DRILLDOWN_RANKING_FILE = "city_drilldown_municipality_ranking_2025.csv"
REPUBLIC_NET_GROSS_TREND_FILE = "republic_net_gross_trend.csv"
BELGRADE_NOVI_SAD_TREND_FILE = "belgrade_novi_sad_net_gross_trend.csv"
TERRITORY_DICTIONARY_FILE = "territory_dictionary.csv"
ANNUAL_ACTIVITY_NET_FILE = "annual_avg_monthly_net_earnings_activity_division.csv"
BEOGRAD_DISTRICT_NAME = "Beogradska oblast"
BEOGRAD_REGION_ALIAS = "Beogradski region"

SVG_BG = "#f6eee3"
SVG_TEXT = "#3f332a"
SVG_MUTED = "#7d6f63"
SVG_GRID = "rgba(92, 74, 57, 0.16)"
SVG_TRACK = "rgba(137, 118, 99, 0.18)"

PASTEL_GOLD = "#d8b48a"
PASTEL_BLUE = "#a8bfd0"
PASTEL_GREEN = "#aacfb2"
PASTEL_ORANGE = "#ddb29c"
PASTEL_TEAL = "#9ecfc9"
PASTEL_PURPLE = "#cabbdc"
PASTEL_SKY = "#b6d9e6"
PASTEL_SAND = "#d8c3a4"
PASTEL_CORAL = "#d8a6a0"


def read_csv(file_path: Path) -> list[dict[str, str]]:
    delimiter = sniff_delimiter(file_path)
    with file_path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=delimiter))


def sniff_delimiter(file_path: Path) -> str:
    with file_path.open("r", encoding="utf-8", newline="") as handle:
        sample = handle.read(2048)
    try:
        dialect = csv.Sniffer().sniff(sample, delimiters=";,\t")
        return dialect.delimiter
    except csv.Error:
        return ";"


def format_rsd(value: float) -> str:
    return f"{int(round(value)):,} RSD".replace(",", " ")


def format_int(value: int) -> str:
    return f"{value:,}".replace(",", " ")


def shorten_label(text: str, max_len: int = 54) -> str:
    text = " ".join(text.split())
    if len(text) <= max_len:
        return text
    return text[: max_len - 1].rstrip() + "…"


def wrap_label_two_lines(text: str, max_line_len: int = 42) -> list[str]:
    words = " ".join(text.split()).split()
    if not words:
        return [""]

    lines: list[str] = []
    current: list[str] = []

    for word in words:
        trial = " ".join(current + [word])
        if current and len(trial) > max_line_len and len(lines) < 1:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)

    if current:
        lines.append(" ".join(current))

    if len(lines) <= 2:
        return lines

    merged = lines[:1] + [" ".join(lines[1:])]
    return merged[:2]


def normalize_territory_label(value: str) -> str:
    return BEOGRAD_REGION_ALIAS if value == BEOGRAD_DISTRICT_NAME else value


def summarize_raw_sources(raw_dir: Path) -> dict[str, int]:
    files = sorted(raw_dir.glob("*.csv"))
    total_rows = 0
    min_year: int | None = None
    max_year: int | None = None

    for file_path in files:
        delimiter = sniff_delimiter(file_path)
        with file_path.open("r", encoding="utf-8", newline="") as handle:
            reader = csv.DictReader(handle, delimiter=delimiter)
            for row in reader:
                total_rows += 1
                for key, value in row.items():
                    if key and key.lower() in {"god", "year"} and value:
                        try:
                            year = int(str(value).strip())
                        except ValueError:
                            continue
                        min_year = year if min_year is None or year < min_year else min_year
                        max_year = year if max_year is None or year > max_year else max_year

    return {
        "file_count": len(files),
        "row_count": total_rows,
        "min_year": min_year or 0,
        "max_year": max_year or 0,
    }


def summarize_csv_directory(directory: Path) -> dict[str, int]:
    files = sorted(directory.glob("*.csv"))
    row_count = 0

    for file_path in files:
        delimiter = sniff_delimiter(file_path)
        with file_path.open("r", encoding="utf-8", newline="") as handle:
            row_count += sum(1 for _ in csv.DictReader(handle, delimiter=delimiter))

    return {
        "file_count": len(files),
        "row_count": row_count,
    }


def markdownish_to_html_block(text: str) -> str:
    parts: list[str] = []
    in_list = False

    for raw_line in text.splitlines():
        line = raw_line.strip()

        if not line:
            if in_list:
                parts.append("</ul>")
                in_list = False
            continue

        if line.startswith("# "):
            if in_list:
                parts.append("</ul>")
                in_list = False
            parts.append(f"<h3>{html.escape(line[2:])}</h3>")
        elif line.startswith("## "):
            if in_list:
                parts.append("</ul>")
                in_list = False
            parts.append(f"<h4>{html.escape(line[3:])}</h4>")
        elif line.startswith("### "):
            if in_list:
                parts.append("</ul>")
                in_list = False
            parts.append(f"<h5>{html.escape(line[4:])}</h5>")
        elif line.startswith("- "):
            if not in_list:
                parts.append("<ul>")
                in_list = True
            parts.append(f"<li>{html.escape(line[2:])}</li>")
        else:
            if in_list:
                parts.append("</ul>")
                in_list = False
            parts.append(f"<p>{html.escape(line)}</p>")

    if in_list:
        parts.append("</ul>")

    return "".join(parts)


def build_territory_reference_html(rows: list[dict[str, str]]) -> str:
    local_units = [row for row in rows if row["territory_level"] == "local_unit"]
    by_macro: dict[str, dict[str, dict[str, list[dict[str, str]]]]] = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))

    for row in local_units:
        by_macro[row["macro_region_name"]][row["statistical_region_name"]][normalize_territory_label(row["administrative_district_name"])].append(row)

    parts = [
        '<div class="territory-reference">',
        '<p>This project uses the official territorial hierarchy from the local reference dictionary.</p>',
        '<ul>',
        '<li><strong>Country:</strong> Republic of Serbia</li>',
        '<li><strong>Macro regions:</strong> 2</li>',
        '<li><strong>Statistical regions:</strong> 4</li>',
        '<li><strong>Administrative districts:</strong> 25</li>',
        f'<li><strong>Local units in current reference:</strong> {len(local_units)}</li>',
        '</ul>',
        '<details open class="territory-details">',
        '<summary>Open territorial hierarchy</summary>',
    ]

    for macro_name in sorted(by_macro):
        stat_regions = by_macro[macro_name]
        district_count = sum(len(districts) for districts in stat_regions.values())
        local_count = sum(len(units) for districts in stat_regions.values() for units in districts.values())
        parts.append(
            f'<details class="territory-level territory-macro"><summary><strong>{html.escape(macro_name)}</strong> '
            f'({len(stat_regions)} statistical regions, {district_count} districts, {local_count} local units)</summary>'
        )
        for stat_name in sorted(stat_regions):
            districts = stat_regions[stat_name]
            local_count = sum(len(units) for units in districts.values())
            parts.append(
                f'<details class="territory-level territory-stat"><summary>{html.escape(stat_name)} '
                f'({len(districts)} districts, {local_count} local units)</summary>'
            )
            for district_name in sorted(districts):
                units = sorted(districts[district_name], key=lambda row: row["territory_name"])
                parts.append(
                    f'<details class="territory-level territory-district"><summary>{html.escape(district_name)} '
                    f'({len(units)} local units)</summary><ul class="territory-units">'
                )
                for unit in units:
                    city_tag = f' - {unit["city_group_name"]}' if unit.get("city_group_name") else ""
                    unit_type = unit["local_unit_type"].replace("_", " ")
                    parts.append(
                        f'<li>{html.escape(unit["territory_name"])} <span class="territory-meta">[{html.escape(unit_type)}{html.escape(city_tag)}]</span></li>'
                    )
                parts.append("</ul></details>")
            parts.append("</details>")
        parts.append("</details>")

    parts.append("</details></div>")
    return "".join(parts)


def top_n(rows: list[dict[str, str]], earnings_type: str, key: str, reverse: bool, n: int = 10) -> list[dict[str, str]]:
    filtered = [row for row in rows if row["earnings_type"] == earnings_type]
    return sorted(filtered, key=lambda row: float(row[key]), reverse=reverse)[:n]


def build_activity_division_rankings_2025(raw_rows: list[dict[str, str]]) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []

    for row in raw_rows:
        code = str(row.get("IDKD08", "")).strip()
        if (
            row.get("god") != "2025"
            or row.get("IDTer") != "RS"
            or not (code.isdigit() and len(code) == 2)
            or code == "96"
        ):
            continue

        name = str(row.get("nkd08", "")).strip()
        rows.append(
            {
                "activity_code": code,
                "activity_name": name,
                "activity_label": name,
                "avg_2025_value_rsd": row["vrednost"],
            }
        )

    return sorted(rows, key=lambda row: float(row["avg_2025_value_rsd"]), reverse=True)


def svg_bar_chart(
    rows: list[dict[str, str]],
    title: str,
    value_key: str,
    label_key: str,
    color: str,
    width: int = 840,
    bar_height: int = 38,
    gap: int = 18,
    left_pad: int = 266,
    right_pad: int = 150,
    top_pad: int = 72,
    bottom_pad: int = 30,
    title_font_size: int = 34,
    title_centered: bool = False,
    title_shift_x: int = 0,
    label_font_size: int = 22,
    value_font_size: int = 20,
    multiline_labels: bool = False,
    label_line_height: int = 20,
    value_formatter=format_rsd,
) -> str:
    if not rows:
        return "<p>No data available.</p>"

    max_value = max(float(row[value_key]) for row in rows)
    chart_height = top_pad + bottom_pad + len(rows) * (bar_height + gap)
    usable_width = width - left_pad - right_pad
    title_x = (left_pad + (usable_width / 2) if title_centered else left_pad) + title_shift_x
    title_anchor = "middle" if title_centered else "start"

    parts = [
        f'<svg viewBox="0 0 {width} {chart_height}" width="100%" role="img" aria-label="{html.escape(title)}">',
        f'<rect x="0" y="0" width="{width}" height="{chart_height}" rx="26" fill="{SVG_BG}"/>',
        f'<text x="{title_x:.2f}" y="42" text-anchor="{title_anchor}" fill="{SVG_TEXT}" font-size="{title_font_size}" font-weight="700" font-family="Arial, sans-serif">{html.escape(title)}</text>',
    ]

    for index, row in enumerate(rows):
        value = float(row[value_key])
        label = str(row[label_key])
        y = top_pad + index * (bar_height + gap)
        bar_width = (value / max_value) * usable_width
        value_text = value_formatter(value)

        label_parts = wrap_label_two_lines(label) if multiline_labels else [label]
        if len(label_parts) == 1:
            label_svg = (
                f'<text x="{left_pad - 12}" y="{y + 25}" text-anchor="end" '
                f'fill="{SVG_TEXT}" font-size="{label_font_size}" font-family="Arial, sans-serif">'
                f"{html.escape(label_parts[0])}</text>"
            )
        else:
            first_y = y + 17
            tspans = [
                f'<tspan x="{left_pad - 12}" y="{first_y + (line_index * label_line_height)}">{html.escape(part)}</tspan>'
                for line_index, part in enumerate(label_parts)
            ]
            label_svg = (
                f'<text x="{left_pad - 12}" text-anchor="end" fill="{SVG_TEXT}" '
                f'font-size="{label_font_size}" font-family="Arial, sans-serif">{"".join(tspans)}</text>'
            )

        parts.extend(
            [
                label_svg,
                f'<rect x="{left_pad}" y="{y}" width="{usable_width}" height="{bar_height}" rx="14" fill="{SVG_TRACK}"/>',
                f'<rect x="{left_pad}" y="{y}" width="{bar_width:.2f}" height="{bar_height}" rx="14" fill="{color}"/>',
                f'<text x="{left_pad + bar_width + 10:.2f}" y="{y + 25}" fill="{SVG_TEXT}" font-size="{value_font_size}" font-family="Arial, sans-serif">{html.escape(value_text)}</text>',
            ]
        )

    parts.append("</svg>")
    return "".join(parts)


def svg_column_chart(
    rows: list[dict[str, str]],
    title: str,
    value_key: str,
    label_key: str,
    color: str,
    width: int = 840,
    height: int = 420,
    left_pad: int = 88,
    right_pad: int = 88,
    top_pad: int = 84,
    bottom_pad: int = 104,
    title_font_size: int = 28,
    value_formatter=format_rsd,
) -> str:
    if not rows:
        return "<p>No data available.</p>"

    max_value = max(float(row[value_key]) for row in rows)
    usable_width = width - left_pad - right_pad
    usable_height = height - top_pad - bottom_pad
    slot_width = usable_width / len(rows)
    bar_width = min(160, slot_width * 0.5)

    parts = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" aria-label="{html.escape(title)}">',
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="26" fill="{SVG_BG}"/>',
        f'<text x="{width / 2:.2f}" y="42" text-anchor="middle" fill="{SVG_TEXT}" font-size="{title_font_size}" font-weight="700" font-family="Arial, sans-serif">{html.escape(title)}</text>',
        f'<line x1="{left_pad}" y1="{top_pad + usable_height:.2f}" x2="{width - right_pad}" y2="{top_pad + usable_height:.2f}" stroke="{SVG_GRID}" stroke-width="1.5"/>',
    ]

    for index, row in enumerate(rows):
        value = float(row[value_key])
        label = str(row[label_key])
        value_text = value_formatter(value)
        bar_height = 0 if max_value == 0 else (value / max_value) * usable_height
        center_x = left_pad + (slot_width * index) + (slot_width / 2)
        x = center_x - (bar_width / 2)
        y = top_pad + usable_height - bar_height

        parts.extend(
            [
                f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_width:.2f}" height="{bar_height:.2f}" rx="18" fill="{color}"/>',
                f'<text x="{center_x:.2f}" y="{y - 14:.2f}" text-anchor="middle" fill="{SVG_TEXT}" font-size="20" font-family="Arial, sans-serif">{html.escape(value_text)}</text>',
                f'<text x="{center_x:.2f}" y="{height - 44:.2f}" text-anchor="middle" fill="{SVG_TEXT}" font-size="18" font-family="Arial, sans-serif">{html.escape(label)}</text>',
            ]
        )

    parts.append("</svg>")
    return "".join(parts)


def svg_rotated_column_chart(
    rows: list[dict[str, str]],
    title: str,
    value_key: str,
    label_key: str,
    color: str,
    width: int = 840,
    height: int = 560,
    left_pad: int = 60,
    right_pad: int = 44,
    top_pad: int = 84,
    bottom_pad: int = 190,
    title_font_size: int = 28,
    value_formatter=format_rsd,
) -> str:
    if not rows:
        return "<p>No data available.</p>"

    max_value = max(float(row[value_key]) for row in rows)
    usable_width = width - left_pad - right_pad
    usable_height = height - top_pad - bottom_pad
    slot_width = usable_width / len(rows)
    bar_width = min(32, slot_width * 0.65)

    parts = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" aria-label="{html.escape(title)}">',
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="26" fill="{SVG_BG}"/>',
        f'<text x="{width / 2:.2f}" y="42" text-anchor="middle" fill="{SVG_TEXT}" font-size="{title_font_size}" font-weight="700" font-family="Arial, sans-serif">{html.escape(title)}</text>',
        f'<line x1="{left_pad}" y1="{top_pad + usable_height:.2f}" x2="{width - right_pad}" y2="{top_pad + usable_height:.2f}" stroke="{SVG_GRID}" stroke-width="1.5"/>',
    ]

    for index, row in enumerate(rows):
        value = float(row[value_key])
        label = str(row[label_key])
        value_text = value_formatter(value)
        bar_height = 0 if max_value == 0 else (value / max_value) * usable_height
        center_x = left_pad + (slot_width * index) + (slot_width / 2)
        x = center_x - (bar_width / 2)
        y = top_pad + usable_height - bar_height

        parts.extend(
            [
                f'<rect x="{x:.2f}" y="{y:.2f}" width="{bar_width:.2f}" height="{bar_height:.2f}" rx="12" fill="{color}"/>',
                f'<text x="{center_x:.2f}" y="{y - 10:.2f}" text-anchor="middle" fill="{SVG_TEXT}" font-size="14" font-family="Arial, sans-serif">{html.escape(value_text)}</text>',
                f'<text x="{center_x:.2f}" y="{height - 52:.2f}" transform="rotate(-42 {center_x:.2f} {height - 52:.2f})" text-anchor="end" fill="{SVG_TEXT}" font-size="17" font-family="Arial, sans-serif">{html.escape(label)}</text>',
            ]
        )

    parts.append("</svg>")
    return "".join(parts)


def _hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.lstrip("#")
    return tuple(int(value[index:index + 2], 16) for index in (0, 2, 4))


def _rgb_to_hex(rgb: tuple[int, int, int]) -> str:
    return "#" + "".join(f"{max(0, min(255, channel)):02x}" for channel in rgb)


def _interpolate_hex(start: str, end: str, fraction: float) -> str:
    start_rgb = _hex_to_rgb(start)
    end_rgb = _hex_to_rgb(end)
    rgb = tuple(round(s + (e - s) * fraction) for s, e in zip(start_rgb, end_rgb))
    return _rgb_to_hex(rgb)


def svg_belgrade_heatmap(rows: list[dict[str, str]], title: str, width: int = 840, height: int = 620) -> str:
    if not rows:
        return "<p>No data available.</p>"

    values = [float(row["avg_2025_value_rsd"]) for row in rows]
    min_value = min(values)
    max_value = max(values)
    value_range = max_value - min_value if max_value > min_value else 1.0

    title_y = 40
    plot_x = 36
    plot_y = 166
    plot_w = width - 72
    plot_h = height - 210

    sorted_rows = sorted(rows, key=lambda row: float(row["avg_2025_value_rsd"]), reverse=True)
    total_value = sum(float(row["avg_2025_value_rsd"]) for row in sorted_rows)
    row_target = total_value / 4
    treemap_rows: list[list[dict[str, str]]] = []
    current_row: list[dict[str, str]] = []
    current_sum = 0.0

    for index, row in enumerate(sorted_rows):
        value = float(row["avg_2025_value_rsd"])
        remaining_rows = 4 - len(treemap_rows)
        remaining_items = len(sorted_rows) - index
        force_break = remaining_items == remaining_rows
        if current_row and current_sum >= row_target and len(treemap_rows) < 3:
            treemap_rows.append(current_row)
            current_row = []
            current_sum = 0.0
        current_row.append(row)
        current_sum += value
        if force_break and len(treemap_rows) < 3:
            treemap_rows.append(current_row)
            current_row = []
            current_sum = 0.0

    if current_row:
        treemap_rows.append(current_row)

    def label_lines(name: str) -> list[str]:
        clean = name.replace(" (Beograd)", "")
        words = clean.split()
        if len(clean) <= 12 or len(words) == 1:
            return [clean]
        midpoint = max(1, len(words) // 2)
        return [" ".join(words[:midpoint]), " ".join(words[midpoint:])]

    parts = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" aria-label="{html.escape(title)}">',
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="26" fill="{SVG_BG}"/>',
        f'<text x="{width / 2:.2f}" y="{title_y}" text-anchor="middle" fill="{SVG_TEXT}" font-size="28" font-weight="700" font-family="Arial, sans-serif">{html.escape(title)}</text>',
        '<style>.district-cell .district-tooltip{opacity:0;transition:opacity .18s ease;pointer-events:none}.district-cell:hover .district-tooltip{opacity:1}.district-cell:hover .district-shape{stroke:#3f332a;stroke-width:3;filter:brightness(1.04)}</style>',
    ]

    y_cursor = plot_y
    gap = 8
    for row_group in treemap_rows:
        row_sum = sum(float(item["avg_2025_value_rsd"]) for item in row_group)
        row_h = plot_h * (row_sum / total_value)
        x_cursor = plot_x

        for item in row_group:
            name = item["municipality_name"]
            value = float(item["avg_2025_value_rsd"])
            fraction = (value - min_value) / value_range
            fill = _interpolate_hex("#dfeee8", "#58b7a4", fraction)
            w = plot_w * (value / row_sum)
            cx = x_cursor + (w / 2)
            cy = y_cursor + (row_h / 2)
            tooltip_y = max(title_y + 92, y_cursor - 14)
            text_lines = label_lines(name)

            font_size = 13
            if w > 170 and row_h > 84:
                font_size = 16
            elif w > 130 and row_h > 70:
                font_size = 15
            elif w < 110 or row_h < 62:
                font_size = 12

            parts.append('<g class="district-cell">')
            parts.append(
                f'<rect class="district-shape" x="{x_cursor + gap / 2:.2f}" y="{y_cursor + gap / 2:.2f}" '
                f'width="{max(40, w - gap):.2f}" height="{max(36, row_h - gap):.2f}" rx="16" '
                f'fill="{fill}" stroke="rgba(63, 51, 42, 0.18)" stroke-width="1.4"/>'
            )

            if len(text_lines) == 1:
                parts.append(
                    f'<text x="{cx:.2f}" y="{cy + 5:.2f}" text-anchor="middle" fill="{SVG_TEXT}" '
                    f'font-size="{font_size}" font-family="Arial, sans-serif">{html.escape(text_lines[0])}</text>'
                )
            else:
                parts.append(
                    f'<text x="{cx:.2f}" y="{cy - 4:.2f}" text-anchor="middle" fill="{SVG_TEXT}" '
                    f'font-size="{font_size}" font-family="Arial, sans-serif">'
                    f'<tspan x="{cx:.2f}" dy="0">{html.escape(text_lines[0])}</tspan>'
                    f'<tspan x="{cx:.2f}" dy="18">{html.escape(text_lines[1])}</tspan>'
                    f'</text>'
                )

            parts.extend(
                [
                    f'<rect class="district-tooltip" x="{max(22, cx - 96):.2f}" y="{tooltip_y - 24:.2f}" width="192" height="40" rx="12" fill="rgba(246, 238, 227, 0.96)" stroke="rgba(63, 51, 42, 0.18)" stroke-width="1"/>',
                    f'<text class="district-tooltip" x="{cx:.2f}" y="{tooltip_y:.2f}" text-anchor="middle" fill="{SVG_TEXT}" font-size="15" font-family="Arial, sans-serif">{html.escape(name)}: {html.escape(format_rsd(value))}</text>',
                    "</g>",
                ]
            )
            x_cursor += w
        y_cursor += row_h

    parts.extend(
        [
            '<text x="86" y="112" fill="#7d6f63" font-size="16" font-family="Arial, sans-serif">Lower</text>',
            '<rect x="138" y="98" width="156" height="18" rx="9" fill="url(#belgradeHeatGradient)"/>',
            '<text x="308" y="112" fill="#7d6f63" font-size="16" font-family="Arial, sans-serif">Higher earnings</text>',
            '<defs><linearGradient id="belgradeHeatGradient" x1="0%" y1="0%" x2="100%" y2="0%"><stop offset="0%" stop-color="#dfeee8"/><stop offset="100%" stop-color="#58b7a4"/></linearGradient></defs>',
        ]
    )

    parts.append("</svg>")
    return "".join(parts)


def build_city_collapsed_ranking_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    output_rows: list[dict[str, str]] = []

    for row in rows:
        city_group_name = str(row.get("city_group_name", "")).strip()
        if city_group_name:
            grouped[(city_group_name, row["earnings_type"])].append(row)
        else:
            output_rows.append({**row, "display_name": row["municipality_name"]})

    for (city_group_name, earnings_type), members in grouped.items():
        median_value = median(float(row["avg_2025_value_rsd"]) for row in members)
        template = members[0]
        output_rows.append(
            {
                **template,
                "municipality_code": f"GROUP_{city_group_name}",
                "municipality_name": city_group_name,
                "display_name": city_group_name,
                "local_unit_type": "city_group",
                "avg_2025_value_rsd": f"{median_value:.2f}",
                "aggregation_method": "median_of_city_group_members",
            }
        )

    return output_rows


def build_city_collapsed_growth_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    output_rows: list[dict[str, str]] = []

    for row in rows:
        city_group_name = str(row.get("city_group_name", "")).strip()
        if city_group_name:
            grouped[(city_group_name, row["earnings_type"])].append(row)
        else:
            output_rows.append({**row})

    for (city_group_name, earnings_type), members in grouped.items():
        median_growth = median(float(row["growth_pct"]) for row in members)
        template = members[0]
        output_rows.append(
            {
                **template,
                "municipality_code": f"GROUP_{city_group_name}",
                "municipality_name": city_group_name,
                "local_unit_type": "city_group",
                "growth_pct": f"{median_growth:.2f}",
                "aggregation_method": "median_of_city_group_members",
            }
        )

    return output_rows


def svg_grouped_city_bar_chart(
    rows: list[dict[str, str]],
    title: str,
    value_key: str,
    color: str,
    width: int = 840,
    left_pad: int = 266,
    right_pad: int = 150,
    top_pad: int = 72,
    bottom_pad: int = 30,
    group_gap: int = 16,
    member_gap: int = 14,
    member_height: int = 34,
) -> str:
    if not rows:
        return "<p>No data available.</p>"
    max_value = max(float(row[value_key]) for row in rows)
    usable_width = width - left_pad - right_pad
    chart_height = top_pad + bottom_pad + len(rows) * member_height + max(0, len(rows) - 1) * member_gap

    parts = [
        f'<svg viewBox="0 0 {width} {chart_height}" width="100%" role="img" aria-label="{html.escape(title)}">',
        f'<rect x="0" y="0" width="{width}" height="{chart_height}" rx="26" fill="{SVG_BG}"/>',
        f'<text x="{left_pad}" y="42" fill="{SVG_TEXT}" font-size="34" font-weight="700" font-family="Arial, sans-serif">{html.escape(title)}</text>',
    ]

    current_y = top_pad

    for row in rows:
        value = float(row[value_key])
        bar_width = (value / max_value) * usable_width
        display_name = str(row["display_name"])

        parts.extend(
            [
                f'<text x="{left_pad - 16}" y="{current_y + 23:.2f}" text-anchor="end" fill="{SVG_TEXT}" font-size="22" font-weight="700" font-family="Arial, sans-serif">{html.escape(display_name)}</text>',
                f'<rect x="{left_pad}" y="{current_y}" width="{usable_width}" height="{member_height}" rx="14" fill="{SVG_TRACK}"/>',
                f'<rect x="{left_pad}" y="{current_y}" width="{bar_width:.2f}" height="{member_height}" rx="14" fill="{color}"/>',
                f'<text x="{left_pad + bar_width + 10:.2f}" y="{current_y + 23}" fill="{SVG_TEXT}" font-size="20" font-family="Arial, sans-serif">{html.escape(format_rsd(value))}</text>',
            ]
        )

        current_y += member_height + member_gap

    parts.append("</svg>")
    return "".join(parts)


def svg_growth_chart(rows: list[dict[str, str]], title: str, color: str) -> str:
    def pct_formatter(value: float) -> str:
        return f"{value:.2f}%"

    return svg_bar_chart(
        rows=rows,
        title=title,
        value_key="growth_pct",
        label_key="municipality_name",
        color=color,
        left_pad=236,
        right_pad=142,
        title_font_size=30,
        title_centered=True,
        value_formatter=pct_formatter,
    )


def latest_full_quarter_net_increase_rows(rows: list[dict[str, str]], n: int = 10) -> tuple[list[dict[str, str]], str, str]:
    quarter_order = {"Q1": 1, "Q2": 2, "Q3": 3, "Q4": 4}

    net_rows = [
        row
        for row in rows
        if row["earnings_type"] == "net" and not (row["to_year"] == "2026" and row["to_quarter"] == "Q1")
    ]

    latest_to_year, latest_to_quarter = max(
        ((row["to_year"], row["to_quarter"]) for row in net_rows),
        key=lambda item: (int(item[0]), quarter_order[item[1]]),
    )

    latest_rows = [
        row
        for row in net_rows
        if row["to_year"] == latest_to_year and row["to_quarter"] == latest_to_quarter and float(row["change_pct"]) > 0
    ]

    latest_rows_sorted = sorted(latest_rows, key=lambda row: float(row["change_pct"]), reverse=True)[:n]
    return latest_rows_sorted, latest_to_year, latest_to_quarter


def previous_quarter_label(year: str, quarter: str) -> str:
    if quarter == "Q1":
        return f"Q4 {int(year) - 1}"
    previous = {"Q2": "Q1", "Q3": "Q2", "Q4": "Q3"}[quarter]
    return f"{previous} {year}"


def svg_signed_change_chart(rows: list[dict[str, str]], title: str, width: int = 840) -> str:
    if not rows:
        return "<p>No data available.</p>"

    rows = rows[:10]
    abs_max = max(abs(float(row["change_pct"])) for row in rows)
    bar_height = 38
    gap = 18
    left_pad = 272
    center_x = 470
    side_width = 150
    top_pad = 72
    bottom_pad = 28
    chart_height = top_pad + bottom_pad + len(rows) * (bar_height + gap)

    parts = [
        f'<svg viewBox="0 0 {width} {chart_height}" width="100%" role="img" aria-label="{html.escape(title)}">',
        f'<rect x="0" y="0" width="{width}" height="{chart_height}" rx="26" fill="{SVG_BG}"/>',
        f'<text x="{left_pad}" y="42" fill="{SVG_TEXT}" font-size="30" font-weight="700" font-family="Arial, sans-serif">{html.escape(title)}</text>',
        f'<line x1="{center_x}" y1="{top_pad - 10}" x2="{center_x}" y2="{chart_height - bottom_pad + 4}" stroke="{SVG_GRID}" stroke-width="2"/>',
    ]

    for index, row in enumerate(rows):
        change = float(row["change_pct"])
        label = str(row["municipality_name"])
        y = top_pad + index * (bar_height + gap)
        bar_width = (abs(change) / abs_max) * side_width
        fill = PASTEL_GOLD if change >= 0 else PASTEL_CORAL

        if change >= 0:
            x = center_x
            text_anchor = "start"
            text_x = x + bar_width + 8
        else:
            x = center_x - bar_width
            text_anchor = "start"
            text_x = center_x + 12

        parts.extend(
            [
                f'<text x="{left_pad - 12}" y="{y + 25}" text-anchor="end" fill="{SVG_TEXT}" font-size="22" font-family="Arial, sans-serif">{html.escape(label)}</text>',
                f'<rect x="{x:.2f}" y="{y}" width="{bar_width:.2f}" height="{bar_height}" rx="10" fill="{fill}"/>',
                f'<text x="{text_x:.2f}" y="{y + 25}" text-anchor="{text_anchor}" fill="{SVG_TEXT}" font-size="20" font-family="Arial, sans-serif">{change:.2f}%</text>',
            ]
        )

    parts.append("</svg>")
    return "".join(parts)


def svg_net_gross_trend_chart(rows: list[dict[str, str]], title: str, width: int = 840, height: int = 500) -> str:
    if not rows:
        return "<p>No data available.</p>"

    left_pad = 130
    right_pad = 84
    top_pad = 72
    bottom_pad = 146
    usable_width = width - left_pad - right_pad
    usable_height = height - top_pad - bottom_pad

    years = [int(row["year"]) for row in rows]
    gross_values = [float(row["gross_value_rsd"]) for row in rows]
    net_values = [float(row["net_value_rsd"]) for row in rows]
    max_value = max(gross_values)
    min_value = min(net_values)
    value_range = max_value - min_value if max_value > min_value else 1.0

    def x_pos(index: int) -> float:
        if len(rows) == 1:
            return left_pad + usable_width / 2
        return left_pad + (usable_width * index / (len(rows) - 1))

    def y_pos(value: float) -> float:
        return top_pad + usable_height - ((value - min_value) / value_range) * usable_height

    def line_path(values: list[float]) -> str:
        points = [f"{x_pos(i):.2f},{y_pos(value):.2f}" for i, value in enumerate(values)]
        return " ".join(points)

    parts = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" aria-label="{html.escape(title)}">',
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="26" fill="{SVG_BG}"/>',
        f'<text x="{left_pad}" y="42" fill="{SVG_TEXT}" font-size="34" font-weight="700" font-family="Arial, sans-serif">{html.escape(title)}</text>',
    ]

    for step in range(5):
        fraction = step / 4
        value = min_value + (value_range * (1 - fraction))
        y = top_pad + usable_height * fraction
        parts.extend(
            [
                f'<line x1="{left_pad}" y1="{y:.2f}" x2="{width - right_pad}" y2="{y:.2f}" stroke="{SVG_GRID}" stroke-width="1"/>',
                f'<text x="{left_pad - 12}" y="{y + 6:.2f}" text-anchor="end" fill="{SVG_MUTED}" font-size="18" font-family="Arial, sans-serif">{html.escape(format_rsd(value))}</text>',
            ]
        )

    for index, year in enumerate(years):
        x = x_pos(index)
        parts.append(f'<text x="{x:.2f}" y="{height - 58}" text-anchor="middle" fill="{SVG_MUTED}" font-size="18" font-family="Arial, sans-serif">{year}</text>')

    parts.append(f'<polyline fill="none" stroke="{PASTEL_ORANGE}" stroke-width="5" points="{line_path(gross_values)}"/>')
    parts.append(f'<polyline fill="none" stroke="{PASTEL_TEAL}" stroke-width="5" points="{line_path(net_values)}"/>')

    for index, row in enumerate(rows):
        x = x_pos(index)
        gross_value = float(row["gross_value_rsd"])
        net_value = float(row["net_value_rsd"])
        gap_value = float(row["gross_minus_net_rsd"])
        net_y = y_pos(net_value)
        gross_y = y_pos(gross_value)
        gap_text_y = max(top_pad + 18, ((gross_y + net_y) / 2) - 10)

        parts.extend(
            [
                '<g class="hover-gap">',
                f'<line x1="{x:.2f}" y1="{gross_y:.2f}" x2="{x:.2f}" y2="{net_y:.2f}" stroke="{PASTEL_SAND}" stroke-dasharray="5 5" stroke-width="2"/>',
                f'<line x1="{x:.2f}" y1="{gross_y:.2f}" x2="{x:.2f}" y2="{net_y:.2f}" stroke="transparent" stroke-width="22"/>',
                f'<circle cx="{x:.2f}" cy="{gross_y:.2f}" r="6" fill="{PASTEL_ORANGE}"/>',
                f'<circle cx="{x:.2f}" cy="{net_y:.2f}" r="6" fill="{PASTEL_TEAL}"/>',
                f'<text class="gap-hover-label" x="{x:.2f}" y="{gap_text_y:.2f}" text-anchor="middle" fill="{SVG_TEXT}" font-size="15" font-family="Arial, sans-serif">gap {html.escape(format_rsd(gap_value))}</text>',
                "</g>",
            ]
        )

    legend_width = 560
    legend_start_x = (width - legend_width) / 2

    parts.extend(
        [
            f'<rect x="{legend_start_x:.2f}" y="458" width="18" height="18" rx="5" fill="{PASTEL_ORANGE}"/>',
            f'<text x="{legend_start_x + 28:.2f}" y="473" fill="{SVG_TEXT}" font-size="17" font-family="Arial, sans-serif">Gross</text>',
            f'<rect x="{legend_start_x + 130:.2f}" y="458" width="18" height="18" rx="5" fill="{PASTEL_TEAL}"/>',
            f'<text x="{legend_start_x + 158:.2f}" y="473" fill="{SVG_TEXT}" font-size="17" font-family="Arial, sans-serif">Net</text>',
            f'<line x1="{legend_start_x + 238:.2f}" y1="467" x2="{legend_start_x + 260:.2f}" y2="467" stroke="{PASTEL_SAND}" stroke-dasharray="5 5" stroke-width="3"/>',
            f'<text x="{legend_start_x + 272:.2f}" y="473" fill="{SVG_MUTED}" font-size="17" font-family="Arial, sans-serif">Hover over dashed gap</text>',
        ]
    )

    parts.append("</svg>")
    return "".join(parts)


def svg_percent_trend_chart(
    rows: list[dict[str, str]],
    title: str,
    value_key: str,
    width: int = 840,
    height: int = 500,
    color: str = PASTEL_CORAL,
    y_label_suffix: str = "%",
) -> str:
    if not rows:
        return "<p>No data available.</p>"

    left_pad = 130
    right_pad = 84
    top_pad = 72
    bottom_pad = 126
    usable_width = width - left_pad - right_pad
    usable_height = height - top_pad - bottom_pad

    years = [int(row["year"]) for row in rows]
    values = [float(row[value_key]) for row in rows]
    max_value = max(values)
    min_value = min(values)
    if max_value == min_value:
        max_value += 0.5
        min_value -= 0.5
    value_range = max_value - min_value

    def x_pos(index: int) -> float:
        if len(rows) == 1:
            return left_pad + usable_width / 2
        return left_pad + (usable_width * index / (len(rows) - 1))

    def y_pos(value: float) -> float:
        return top_pad + usable_height - ((value - min_value) / value_range) * usable_height

    def line_path(series: list[float]) -> str:
        return " ".join(f"{x_pos(i):.2f},{y_pos(value):.2f}" for i, value in enumerate(series))

    parts = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" aria-label="{html.escape(title)}">',
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="26" fill="{SVG_BG}"/>',
        f'<text x="{left_pad}" y="42" fill="{SVG_TEXT}" font-size="34" font-weight="700" font-family="Arial, sans-serif">{html.escape(title)}</text>',
    ]

    for step in range(5):
        fraction = step / 4
        value = min_value + (value_range * (1 - fraction))
        y = top_pad + usable_height * fraction
        parts.extend(
            [
                f'<line x1="{left_pad}" y1="{y:.2f}" x2="{width - right_pad}" y2="{y:.2f}" stroke="{SVG_GRID}" stroke-width="1"/>',
                f'<text x="{left_pad - 12}" y="{y + 6:.2f}" text-anchor="end" fill="{SVG_MUTED}" font-size="18" font-family="Arial, sans-serif">{value:.2f}{html.escape(y_label_suffix)}</text>',
            ]
        )

    for index, year in enumerate(years):
        x = x_pos(index)
        parts.append(f'<text x="{x:.2f}" y="{height - 58}" text-anchor="middle" fill="{SVG_MUTED}" font-size="18" font-family="Arial, sans-serif">{year}</text>')

    parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="5" points="{line_path(values)}"/>')

    for index, value in enumerate(values):
        x = x_pos(index)
        y = y_pos(value)
        label_y = max(top_pad + 12, y - 12)
        parts.extend(
            [
                f'<circle cx="{x:.2f}" cy="{y:.2f}" r="6" fill="{color}"/>',
                f'<text x="{x:.2f}" y="{label_y:.2f}" text-anchor="middle" fill="{SVG_TEXT}" font-size="15" font-family="Arial, sans-serif">{value:.2f}%</text>',
            ]
        )

    parts.extend(
        [
            f'<rect x="86" y="458" width="18" height="18" rx="5" fill="{color}"/>',
            f'<text x="114" y="473" fill="{SVG_TEXT}" font-size="17" font-family="Arial, sans-serif">Gap share of gross earnings</text>',
        ]
    )

    parts.append("</svg>")
    return "".join(parts)


def svg_city_comparison_trend_chart(
    rows: list[dict[str, str]],
    title: str,
    metric: str,
    width: int = 840,
    height: int = 500,
) -> str:
    if not rows:
        return "<p>No data available.</p>"

    left_pad = 130
    right_pad = 84
    top_pad = 72
    bottom_pad = 146
    usable_width = width - left_pad - right_pad
    usable_height = height - top_pad - bottom_pad

    years = sorted({int(row["year"]) for row in rows})
    series_order = [
        ("Grad Beograd", metric, PASTEL_ORANGE),
        ("Grad Novi Sad", metric, PASTEL_TEAL),
    ]

    metric_name = metric
    metric_label = "gross" if metric_name == "gross" else "net"
    value_lookup = {
        (row["city_label"], int(row["year"]), metric_name): float(row[f"{metric_name}_value_rsd"])
        for row in rows
    }

    all_values = list(value_lookup.values())
    max_value = max(all_values)
    min_value = min(all_values)
    value_range = max_value - min_value if max_value > min_value else 1.0

    def x_pos(index: int) -> float:
        if len(years) == 1:
            return left_pad + usable_width / 2
        return left_pad + (usable_width * index / (len(years) - 1))

    def y_pos(value: float) -> float:
        return top_pad + usable_height - ((value - min_value) / value_range) * usable_height

    parts = [
        f'<svg viewBox="0 0 {width} {height}" width="100%" role="img" aria-label="{html.escape(title)}">',
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="26" fill="{SVG_BG}"/>',
        f'<text x="{left_pad}" y="42" fill="{SVG_TEXT}" font-size="34" font-weight="700" font-family="Arial, sans-serif">{html.escape(title)}</text>',
    ]

    for step in range(5):
        fraction = step / 4
        value = min_value + (value_range * (1 - fraction))
        y = top_pad + usable_height * fraction
        parts.extend(
            [
                f'<line x1="{left_pad}" y1="{y:.2f}" x2="{width - right_pad}" y2="{y:.2f}" stroke="{SVG_GRID}" stroke-width="1"/>',
                f'<text x="{left_pad - 12}" y="{y + 6:.2f}" text-anchor="end" fill="{SVG_MUTED}" font-size="18" font-family="Arial, sans-serif">{html.escape(format_rsd(value))}</text>',
            ]
        )

    for index, year in enumerate(years):
        x = x_pos(index)
        parts.append(f'<text x="{x:.2f}" y="{height - 58}" text-anchor="middle" fill="{SVG_MUTED}" font-size="18" font-family="Arial, sans-serif">{year}</text>')

    for city_label, metric, color in series_order:
        points = []
        for index, year in enumerate(years):
            key = (city_label, year, metric)
            if key not in value_lookup:
                continue
            points.append(f"{x_pos(index):.2f},{y_pos(value_lookup[key]):.2f}")
        if points:
            parts.append(f'<polyline fill="none" stroke="{color}" stroke-width="5" points="{" ".join(points)}"/>')

        for index, year in enumerate(years):
            key = (city_label, year, metric)
            if key not in value_lookup:
                continue
            x = x_pos(index)
            y = y_pos(value_lookup[key])
            parts.append(f'<circle cx="{x:.2f}" cy="{y:.2f}" r="6" fill="{color}"/>')

    legend = [
        (PASTEL_ORANGE, f"Beograd {metric_label}"),
        (PASTEL_TEAL, f"Novi Sad {metric_label}"),
    ]
    legend_x = 86
    for color, label in legend:
        parts.extend(
            [
                f'<rect x="{legend_x}" y="458" width="18" height="18" rx="5" fill="{color}"/>',
                f'<text x="{legend_x + 28}" y="473" fill="{SVG_TEXT}" font-size="17" font-family="Arial, sans-serif">{html.escape(label)}</text>',
            ]
        )
        legend_x += 220

    parts.append("</svg>")
    return "".join(parts)


def render_report() -> str:
    raw_summary = summarize_raw_sources(PROJECT_DIR / "data" / "raw")
    marts_summary = summarize_csv_directory(MARTS_DIR)
    rankings = read_csv(MARTS_DIR / MUNICIPALITY_RANKING_FILE)
    growth = read_csv(MARTS_DIR / MUNICIPALITY_GROWTH_FILE)
    qoq = read_csv(MARTS_DIR / MUNICIPALITY_QOQ_OUTLIERS_FILE)
    macro_regions = read_csv(MARTS_DIR / GROUP_MEDIAN_MACRO_FILE)
    districts = read_csv(MARTS_DIR / GROUP_MEDIAN_DISTRICT_FILE)
    city_members = read_csv(MARTS_DIR / CITY_DRILLDOWN_RANKING_FILE)
    territory_reference = read_csv(REFERENCE_DIR / TERRITORY_DICTIONARY_FILE)
    republic_trend = read_csv(MARTS_DIR / REPUBLIC_NET_GROSS_TREND_FILE)
    belgrade_novi_sad_trend = read_csv(MARTS_DIR / BELGRADE_NOVI_SAD_TREND_FILE)
    activity_division_net_raw = read_csv(PROJECT_DIR / "data" / "raw" / ANNUAL_ACTIVITY_NET_FILE)
    findings = (DOCS_DIR / "analysis_findings.md").read_text(encoding="utf-8")
    notes = (DOCS_DIR / "analysis_notes.md").read_text(encoding="utf-8")

    net_rankings = [row for row in rankings if row["earnings_type"] == "net"]
    net_growth_rows = [row for row in growth if row["earnings_type"] == "net"]

    top_2025_net_collapsed = sorted(
        build_city_collapsed_ranking_rows(net_rankings),
        key=lambda row: float(row["avg_2025_value_rsd"]),
        reverse=True,
    )[:10]
    bottom_2025_net_collapsed = sorted(
        build_city_collapsed_ranking_rows(net_rankings),
        key=lambda row: float(row["avg_2025_value_rsd"]),
    )[:10]
    top_growth_net_collapsed = sorted(
        build_city_collapsed_growth_rows(net_growth_rows),
        key=lambda row: float(row["growth_pct"]),
        reverse=True,
    )[:10]
    qoq_rows, latest_qoq_year, latest_qoq_quarter = latest_full_quarter_net_increase_rows(qoq, n=10)
    previous_qoq_label = previous_quarter_label(latest_qoq_year, latest_qoq_quarter)
    qoq_note = (
        f"Method note: this chart shows positive quarter-over-quarter net earnings growth from the previous quarter "
        f"to {latest_qoq_quarter} {latest_qoq_year}."
    )
    macro_net = top_n(macro_regions, "net", "median_2025_value_rsd", True, n=10)
    district_net = top_n(districts, "net", "median_2025_value_rsd", True, n=10)
    belgrade_district_rows = sorted(
        [
            {**row, "district_label": row["municipality_name"]}
            for row in city_members
            if row["earnings_type"] == "net" and row["city_group_name"] == "Grad Beograd"
        ],
        key=lambda row: float(row["avg_2025_value_rsd"]),
        reverse=True,
    )
    juznobacka_oblast_rows = sorted(
        build_city_collapsed_ranking_rows(
            [row for row in net_rankings if row["administrative_district_name"] == "Južnobačka oblast"]
        ),
        key=lambda row: float(row["avg_2025_value_rsd"]),
        reverse=True,
    )
    activity_division_rankings = build_activity_division_rankings_2025(activity_division_net_raw)
    activity_top_10 = activity_division_rankings[:10]
    activity_bottom_10 = sorted(activity_division_rankings, key=lambda row: float(row["avg_2025_value_rsd"]))[:10]

    city_member_chart_rows = [
        {**row, "drilldown_label": f"{row['city_group_name']} / {row['municipality_name']}"}
        for row in top_n(city_members, "net", "avg_2025_value_rsd", True, n=12)
    ]

    chart_top = svg_grouped_city_bar_chart(
        top_2025_net_collapsed,
        "Top 10 by Net Earnings, 2025",
        "avg_2025_value_rsd",
        PASTEL_GOLD,
    )
    chart_bottom = svg_grouped_city_bar_chart(
        bottom_2025_net_collapsed,
        "Bottom 10 by Net Earnings, 2025",
        "avg_2025_value_rsd",
        PASTEL_BLUE,
    )
    chart_growth = svg_growth_chart(top_growth_net_collapsed, "Net Earnings Growth 2018-2025", PASTEL_GREEN)
    chart_qoq = svg_bar_chart(
        qoq_rows,
        f"Net Earnings Growth {previous_qoq_label}-{latest_qoq_quarter} {latest_qoq_year}",
        "change_pct",
        "municipality_name",
        PASTEL_GOLD,
        left_pad=236,
        right_pad=142,
        title_font_size=30,
        title_centered=True,
        value_formatter=lambda value: f"{value:.2f}%",
    )
    chart_net_gross_trend = svg_net_gross_trend_chart(republic_trend, "Net & Gross Earnings Comparison")
    chart_gap_share_trend = svg_percent_trend_chart(
        republic_trend,
        "Gross-Net Gap, % of Gross",
        "gap_to_gross_pct",
        color=PASTEL_SAND,
    )
    chart_belgrade_novi_sad_gross = svg_city_comparison_trend_chart(
        belgrade_novi_sad_trend,
        "Belgrade vs Novi Sad Gross Earnings",
        "gross",
    )
    chart_belgrade_novi_sad_net = svg_city_comparison_trend_chart(
        belgrade_novi_sad_trend,
        "Belgrade vs Novi Sad Net Earnings",
        "net",
    )
    chart_macro = svg_column_chart(
        macro_net,
        "Macro Region Median Net Earnings, 2025",
        "median_2025_value_rsd",
        "macro_region_name",
        PASTEL_PURPLE,
    )
    chart_district = svg_bar_chart(
        district_net,
        "Top District Median Net Earnings, 2025",
        "median_2025_value_rsd",
        "administrative_district_name",
        PASTEL_ORANGE,
        title_font_size=28,
        title_centered=True,
    )
    chart_city = svg_belgrade_heatmap(
        belgrade_district_rows,
        "Belgrade District Net Earnings Treemap, 2025",
    )
    chart_juznobacka_oblast = svg_belgrade_heatmap(
        juznobacka_oblast_rows,
        "Južnobačka Oblast Treemap, 2025",
        height=460,
    )
    chart_activity_top = svg_bar_chart(
        activity_top_10,
        "Top 10 Activity Divisions by Net Earnings, 2025",
        "avg_2025_value_rsd",
        "activity_label",
        PASTEL_GOLD,
        bar_height=42,
        gap=24,
        left_pad=472,
        right_pad=124,
        title_font_size=28,
        title_centered=True,
        title_shift_x=-40,
        label_font_size=16,
        value_font_size=18,
        multiline_labels=True,
        label_line_height=18,
    )
    chart_activity_bottom = svg_bar_chart(
        activity_bottom_10,
        "Bottom 10 Activity Divisions by Net Earnings, 2025",
        "avg_2025_value_rsd",
        "activity_label",
        PASTEL_BLUE,
        bar_height=42,
        gap=24,
        left_pad=472,
        right_pad=124,
        title_font_size=28,
        title_centered=True,
        title_shift_x=-40,
        label_font_size=16,
        value_font_size=18,
        multiline_labels=True,
        label_line_height=18,
    )
    territory_reference_html = build_territory_reference_html(territory_reference)

    return f"""<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Serbia Labour Market Monitor | Earnings Report</title>
    <style>
      :root {{
        --bg: #d8cec0;
        --surface: rgba(242, 234, 223, 0.88);
        --surface-2: rgba(226, 214, 199, 0.92);
        --text: #342c24;
        --muted: #6f655b;
        --gold: #a9783f;
        --line: rgba(84, 66, 48, 0.12);
      }}
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0;
        font-family: Arial, sans-serif;
        color: var(--text);
        background:
          linear-gradient(135deg, rgba(92, 78, 63, 0.10), rgba(242, 236, 228, 0) 38%),
          linear-gradient(25deg, rgba(170, 150, 127, 0.18), rgba(216, 206, 192, 0) 44%),
          repeating-linear-gradient(
            115deg,
            rgba(122, 99, 76, 0.05) 0px,
            rgba(122, 99, 76, 0.05) 14px,
            rgba(226, 214, 199, 0.02) 14px,
            rgba(226, 214, 199, 0.02) 30px
          ),
          radial-gradient(circle at top left, rgba(161, 131, 101, 0.16), transparent 33%),
          radial-gradient(circle at 82% 18%, rgba(196, 176, 149, 0.20), transparent 24%),
          var(--bg);
      }}
      .wrap {{
        width: min(1180px, calc(100% - 32px));
        margin: 0 auto;
        padding: 32px 0 48px;
      }}
      .hero, .panel {{
        background: var(--surface);
        border: 1px solid rgba(102, 84, 63, 0.12);
        border-radius: 28px;
        padding: 28px;
        box-shadow: 0 22px 54px rgba(75, 58, 42, 0.14);
        backdrop-filter: blur(6px);
      }}
      .hero h1 {{
        margin: 0 0 10px;
        font-size: 46px;
        line-height: 1;
      }}
      .hero p {{
        margin: 10px 0 0;
        color: var(--muted);
        max-width: 820px;
        line-height: 1.65;
      }}
      .hero .contacts {{
        margin-top: 8px;
        font-weight: 600;
      }}
      .hero a {{
        color: var(--gold);
        text-decoration: none;
      }}
      .hero a:hover {{
        text-decoration: underline;
      }}
      .block-header {{
        padding: 18px 24px;
      }}
      .block-header h2 {{
        margin: 0 0 6px;
      }}
      .block-header p {{
        margin: 0;
        color: var(--muted);
      }}
      .grid {{
        display: grid;
        grid-template-columns: 1fr;
        gap: 20px;
        margin-top: 20px;
      }}
      .two-col {{
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 20px;
      }}
      h2 {{
        margin: 0 0 12px;
        font-size: 22px;
      }}
      h3 {{
        margin: 0 0 12px;
        font-size: 20px;
      }}
      h4 {{
        margin: 18px 0 10px;
        font-size: 17px;
      }}
      h5 {{
        margin: 16px 0 8px;
        font-size: 15px;
      }}
      .panel p {{
        color: var(--muted);
        line-height: 1.65;
      }}
      .panel svg {{
        display: block;
        margin: 0 auto;
      }}
      .hover-gap .gap-hover-label {{
        opacity: 0;
        transition: opacity 0.15s ease;
        pointer-events: none;
      }}
      .hover-gap:hover .gap-hover-label {{
        opacity: 1;
      }}
      .panel ul {{
        margin: 8px 0 14px 18px;
        padding: 0;
        color: var(--muted);
        line-height: 1.65;
      }}
      .panel li {{
        margin: 6px 0;
      }}
      .territory-reference ul {{
        margin: 8px 0 14px 18px;
        padding: 0;
      }}
      .territory-reference li {{
        margin: 4px 0;
      }}
      .territory-reference details {{
        margin: 8px 0;
      }}
      .territory-reference summary {{
        cursor: pointer;
        font-weight: 600;
        color: var(--text);
      }}
      .territory-level {{
        padding-left: 10px;
        border-left: 2px solid rgba(84, 66, 48, 0.10);
      }}
      .territory-units {{
        margin-top: 8px;
      }}
      .territory-meta {{
        color: var(--muted);
        font-size: 0.92em;
      }}
      .kpis {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: 14px;
        margin-top: 18px;
      }}
      .kpi {{
        background: var(--surface-2);
        border-radius: 18px;
        padding: 16px;
        border: 1px solid var(--line);
      }}
      .kpi strong {{
        display: block;
        font-size: 26px;
        color: var(--gold);
      }}
      .kpi span {{
        display: block;
        margin-top: 6px;
        color: var(--muted);
        font-size: 14px;
      }}
      @media (max-width: 900px) {{
        .two-col, .kpis {{
          grid-template-columns: 1fr;
        }}
        .hero h1 {{
          font-size: 34px;
        }}
      }}
    </style>
  </head>
  <body>
    <div class="wrap">
      <section class="hero">
        <h1>Serbia Labour Market Monitor</h1>
        <p>This project was created with Codex by Maria Mazaeva on the basis of official Serbian SORS open data from <a href="https://data.stat.gov.rs/" target="_blank" rel="noreferrer">data.stat.gov.rs</a>.</p>
        <p class="contacts">Author contacts: +381629614352 (Viber / WhatsApp), Telegram <a href="https://t.me/kinsec" target="_blank" rel="noreferrer">@kinsec</a>.</p>
        <p>The current municipality earnings report is built from 4 primary raw source files. The full raw-source catalog currently contains {raw_summary["file_count"]} CSV files and {format_int(raw_summary["row_count"])} raw records. You can review the file list in <a href="{GITHUB_REPO_URL}/tree/main/data/raw" target="_blank" rel="noopener noreferrer">data/raw</a> and the descriptions in <a href="{GITHUB_REPO_URL}/blob/main/data/raw/DATASETS_DESCRIPTION.md" target="_blank" rel="noopener noreferrer">DATASETS_DESCRIPTION.md</a>.</p>
        <div class="kpis">
          <div class="kpi"><strong>{raw_summary["file_count"]}</strong><span>Raw source files in <code>data/raw</code></span></div>
          <div class="kpi"><strong>{marts_summary["file_count"]}</strong><span>Analytical CSV tables in <code>data/marts</code></span></div>
          <div class="kpi"><strong>{format_int(marts_summary["row_count"])}</strong><span>Total rows across analytical tables</span></div>
          <div class="kpi"><strong>{raw_summary["min_year"]}-{raw_summary["max_year"]}</strong><span>Observed source years from min to max</span></div>
        </div>
      </section>
      <div class="grid">
        <section class="panel block-header">
          <h2>Block 1. Regional Slice</h2>
          <p>This block contains all current territorial views: municipality rankings, republic net-vs-gross comparison, city comparisons, growth, macro regions, districts, and regional drill-downs.</p>
        </section>
        <section class="two-col">
          <div class="panel">{chart_top}</div>
          <div class="panel">{chart_bottom}</div>
        </section>
        <section class="two-col">
          <div class="panel">{chart_net_gross_trend}</div>
          <div class="panel">
            {chart_gap_share_trend}
            <p>Method note: this is the share of the gross-minus-net gap in gross earnings. It is a useful proxy for the earnings wedge, but not a direct measure of tax-law changes.</p>
          </div>
        </section>
        <section class="two-col">
          <div class="panel">
            {chart_belgrade_novi_sad_gross}
            <p>Method note: both cities are shown as medians across available city-group members. For Novi Sad, that median currently equals the single city-level row.</p>
          </div>
          <div class="panel">
            {chart_belgrade_novi_sad_net}
            <p>Method note: both cities are shown as medians across available city-group members. For Novi Sad, that median currently equals the single city-level row.</p>
          </div>
        </section>
        <section class="two-col">
          <div class="panel">{chart_growth}</div>
          <div class="panel">
            {chart_qoq}
            <p>{html.escape(qoq_note)}</p>
          </div>
        </section>
        <section class="two-col">
          <div class="panel">{chart_macro}</div>
          <div class="panel">{chart_district}</div>
        </section>
        <section class="panel">
          <h2>Territorial Hierarchy Reference</h2>
          {territory_reference_html}
        </section>
        <section class="two-col">
          <div class="panel">
            {chart_city}
            <p>Method note: this view shows Belgrade as city municipalities only.</p>
          </div>
          <div class="panel">
            {chart_juznobacka_oblast}
            <p>Method note: `Grad Novi Sad` appears as one city tile inside `Južnobačka oblast`; the other tiles are the remaining municipalities of the district.</p>
          </div>
        </section>
        <section class="panel block-header">
          <h2>Block 2. Professional Slice</h2>
          <p>This block introduces earnings rankings by activity division and starts the profession-oriented view with the highest-paid and lowest-paid activity groups in 2025.</p>
        </section>
        <section class="two-col">
          <div class="panel">{chart_activity_top}</div>
          <div class="panel">{chart_activity_bottom}</div>
        </section>
      </div>
    </div>
  </body>
</html>
"""


def main() -> None:
    APP_DIR.mkdir(parents=True, exist_ok=True)
    output_path = APP_DIR / "earnings_report.html"
    output_path.write_text(render_report(), encoding="utf-8")
    print(f"Report created: {output_path}")


if __name__ == "__main__":
    main()
