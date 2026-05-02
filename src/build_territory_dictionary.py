"""
Build a reusable territory hierarchy dictionary from the municipality earnings files.
"""

from __future__ import annotations

import csv
from pathlib import Path


RAW_DIR = Path(__file__).resolve().parent.parent / "data" / "raw"
REFERENCE_DIR = Path(__file__).resolve().parent.parent / "data" / "reference"

SOURCE_FILE = RAW_DIR / "avg_monthly_net_earnings_municipality_residence.csv"
OUTPUT_FILE = REFERENCE_DIR / "territory_dictionary.csv"

DISTRICT_LOCAL_CODES = {
    "RS110": [
        "70092",
        "70106",
        "70114",
        "70122",
        "70149",
        "70157",
        "70165",
        "70173",
        "70181",
        "70190",
        "70203",
        "70211",
        "70220",
        "70238",
        "70246",
        "70254",
        "71293",
    ],
    "RS121": ["80047", "80233", "80306", "80381"],
    "RS122": ["80039", "80098", "80128", "80217", "80225", "80292", "80314", "80349"],
    "RS123": ["80055", "80063", "80080", "80101", "80110", "80136", "80284", "80390", "80411", "80446", "80454", "80462", "80519", "89010"],
    "RS124": ["80012", "80195", "80209", "80276", "80365", "80489"],
    "RS125": ["80071", "80241", "80438"],
    "RS126": ["80144", "80152", "80250", "80268", "80373"],
    "RS127": ["80179", "80187", "80322", "80357", "80403", "80420", "80497"],
    "RS211": ["70041", "70068", "70629", "70866", "70955", "70971", "70980", "71072", "71145", "71234", "71366", "79065"],
    "RS212": ["70360", "70700", "70769", "70831", "70882", "71218"],
    "RS213": ["70289", "70408", "70637", "70661", "70734", "70777", "70793", "71269"],
    "RS214": ["70483", "70564", "70742", "71242"],
    "RS215": ["70491", "70904", "71030", "71048", "71056", "71200"],
    "RS216": ["70017", "70343", "70378", "70670", "71170", "71196"],
    "RS217": ["70653", "70874", "71021", "71188", "70459"],
    "RS218": ["70033", "70076", "70599", "70645", "71013", "71153", "71277"],
    "RS221": ["70327", "70572", "70785", "70840"],
    "RS222": ["70394", "70475", "70521", "70530", "70696", "70807", "70912", "70947", "71340", "79049"],
    "RS223": ["70319", "70556", "70602", "71129"],
    "RS224": ["70297", "70424", "70718", "70726", "70815", "71226"],
    "RS225": ["70025", "70467", "70513", "70823", "71005", "71064", "71285", "71307", "71315", "71323", "71331", "79022"],
    "RS226": ["70050", "70084", "70505", "70939"],
    "RS227": ["70386", "71099", "71102"],
    "RS228": ["70335", "70351", "70416", "70432", "70963", "71137", "71161", "71358", "79057"],
    "RS229": ["70262", "70548", "70688", "70998"],
}

CITY_MUNICIPALITY_CODES = {
    "70092",
    "70106",
    "70114",
    "70122",
    "70149",
    "70157",
    "70165",
    "70173",
    "70181",
    "70190",
    "70203",
    "70211",
    "70220",
    "70238",
    "70246",
    "70254",
    "71293",
    "71285",
    "71307",
    "71315",
    "71323",
    "71331",
    "70947",
    "71340",
    "70432",
    "71358",
    "71145",
    "71366",
    "80284",
    "80519",
}

CITY_CODES = {"79022", "79049", "79057", "79065", "89010"}

CITY_GROUPS = {
    "70092": ("CITY_BELGRADE", "Grad Beograd"),
    "70106": ("CITY_BELGRADE", "Grad Beograd"),
    "70114": ("CITY_BELGRADE", "Grad Beograd"),
    "70122": ("CITY_BELGRADE", "Grad Beograd"),
    "70149": ("CITY_BELGRADE", "Grad Beograd"),
    "70157": ("CITY_BELGRADE", "Grad Beograd"),
    "70165": ("CITY_BELGRADE", "Grad Beograd"),
    "70173": ("CITY_BELGRADE", "Grad Beograd"),
    "70181": ("CITY_BELGRADE", "Grad Beograd"),
    "70190": ("CITY_BELGRADE", "Grad Beograd"),
    "70203": ("CITY_BELGRADE", "Grad Beograd"),
    "70211": ("CITY_BELGRADE", "Grad Beograd"),
    "70220": ("CITY_BELGRADE", "Grad Beograd"),
    "70238": ("CITY_BELGRADE", "Grad Beograd"),
    "70246": ("CITY_BELGRADE", "Grad Beograd"),
    "70254": ("CITY_BELGRADE", "Grad Beograd"),
    "71293": ("CITY_BELGRADE", "Grad Beograd"),
    "71285": ("79022", "Grad Niš"),
    "71307": ("79022", "Grad Niš"),
    "71315": ("79022", "Grad Niš"),
    "71323": ("79022", "Grad Niš"),
    "71331": ("79022", "Grad Niš"),
    "79022": ("79022", "Grad Niš"),
    "70947": ("79049", "Grad Požarevac"),
    "71340": ("79049", "Grad Požarevac"),
    "79049": ("79049", "Grad Požarevac"),
    "70432": ("79057", "Grad Vranje"),
    "71358": ("79057", "Grad Vranje"),
    "79057": ("79057", "Grad Vranje"),
    "71145": ("79065", "Grad Užice"),
    "71366": ("79065", "Grad Užice"),
    "79065": ("79065", "Grad Užice"),
    "80284": ("89010", "Grad Novi Sad"),
    "80519": ("89010", "Grad Novi Sad"),
    "89010": ("89010", "Grad Novi Sad"),
}

LOCAL_NOTES = {
    "80284": "Present as a separate local unit in 2018-2019; later consolidated under 89010 Grad Novi Sad.",
    "80519": "Present as a separate local unit in 2018-2019; later consolidated under 89010 Grad Novi Sad.",
    "89010": "Aggregate city row used for later Novi Sad coverage in the source data.",
    "CITY_BELGRADE": "Synthetic grouping code used only in city_group_code because the raw data do not contain a single aggregate Belgrade row.",
}


def read_source_rows() -> list[dict[str, str]]:
    with SOURCE_FILE.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=";"))


def write_csv(file_path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    with file_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def build_local_lookup() -> dict[str, dict[str, str]]:
    lookup: dict[str, dict[str, str]] = {}

    for district_code, local_codes in DISTRICT_LOCAL_CODES.items():
        for code in local_codes:
            if code in lookup:
                raise ValueError(f"Duplicate local territory mapping for code {code}")
            lookup[code] = {"district_code": district_code}

    return lookup


def level_from_code(code: str) -> tuple[str, int]:
    if code == "RS":
        return "country", 1
    if code.startswith("RS") and len(code) == 3:
        return "macro_region", 2
    if code.startswith("RS") and len(code) == 4:
        return "statistical_region", 3
    if code.startswith("RS") and len(code) == 5:
        return "administrative_district", 4
    return "local_unit", 5


def local_unit_type(code: str) -> str:
    if code in CITY_CODES:
        return "city"
    if code in CITY_MUNICIPALITY_CODES:
        return "city_municipality"
    return "municipality"


def parent_code(code: str, local_lookup: dict[str, dict[str, str]]) -> str:
    if code == "RS":
        return ""
    if code.startswith("RS") and len(code) == 3:
        return "RS"
    if code.startswith("RS") and len(code) == 4:
        return code[:3]
    if code.startswith("RS") and len(code) == 5:
        return code[:4]
    return local_lookup[code]["district_code"]


def build_rows(source_rows: list[dict[str, str]]) -> list[dict[str, object]]:
    code_name_lookup = {
        row["IDTer"]: row["nTer"]
        for row in source_rows
    }
    local_lookup = build_local_lookup()

    observed_codes = set(code_name_lookup)
    expected_local_codes = set(local_lookup)
    observed_local_codes = {code for code in observed_codes if code[:1].isdigit()}

    missing_local_codes = sorted(observed_local_codes - expected_local_codes)
    unused_local_codes = sorted(expected_local_codes - observed_local_codes)

    if missing_local_codes:
        raise ValueError(f"Missing local territory mappings: {missing_local_codes}")
    if unused_local_codes:
        raise ValueError(f"Unused local territory mappings: {unused_local_codes}")

    rows: list[dict[str, object]] = []

    for code, name in sorted(code_name_lookup.items()):
        territory_level, territory_level_order = level_from_code(code)
        parent = parent_code(code, local_lookup) if code != "RS" else ""
        parent_name = code_name_lookup.get(parent, "")

        macro_region_code = ""
        statistical_region_code = ""
        administrative_district_code = ""
        city_group_code = ""
        city_group_name = ""
        local_type = ""
        note = ""

        if code.startswith("RS") and len(code) >= 3:
            macro_region_code = "RS" if code == "RS" else code[:3]
        if code.startswith("RS") and len(code) >= 4:
            statistical_region_code = code[:4]
        if code.startswith("RS") and len(code) == 5:
            administrative_district_code = code

        if code[:1].isdigit():
            administrative_district_code = local_lookup[code]["district_code"]
            statistical_region_code = administrative_district_code[:4]
            macro_region_code = administrative_district_code[:3]
            local_type = local_unit_type(code)

            if code in CITY_GROUPS:
                city_group_code, city_group_name = CITY_GROUPS[code]

            note = LOCAL_NOTES.get(code, "")

        rows.append(
            {
                "territory_code": code,
                "territory_name": name,
                "territory_level": territory_level,
                "territory_level_order": territory_level_order,
                "parent_territory_code": parent,
                "parent_territory_name": parent_name,
                "country_code": "RS",
                "country_name": code_name_lookup["RS"],
                "macro_region_code": macro_region_code,
                "macro_region_name": code_name_lookup.get(macro_region_code, ""),
                "statistical_region_code": statistical_region_code,
                "statistical_region_name": code_name_lookup.get(statistical_region_code, ""),
                "administrative_district_code": administrative_district_code,
                "administrative_district_name": code_name_lookup.get(administrative_district_code, ""),
                "local_unit_type": local_type,
                "city_group_code": city_group_code,
                "city_group_name": city_group_name,
                "is_in_raw_municipality_file": "True",
                "note": note,
            }
        )

    return rows


def main() -> None:
    REFERENCE_DIR.mkdir(parents=True, exist_ok=True)
    rows = build_rows(read_source_rows())

    write_csv(
        OUTPUT_FILE,
        [
            "territory_code",
            "territory_name",
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
            "is_in_raw_municipality_file",
            "note",
        ],
        rows,
    )

    print(f"Territory dictionary created: {OUTPUT_FILE}")
    print(f"Rows: {len(rows)}")


if __name__ == "__main__":
    main()
