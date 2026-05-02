# Territory Dictionary

Updated: 2026-04-30

## Purpose
This document explains the territory hierarchy dictionary used for grouping and ungrouping charts, tables, and future drill-down views.

The dictionary itself is stored in [territory_dictionary.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/reference/territory_dictionary.csv).

## Why This Dictionary Exists
The raw municipality earnings files mix several territorial levels in one column:
- Serbia as a whole
- macro regions such as `SRBIJA – SEVER`
- statistical regions such as `Region Vojvodine`
- administrative districts such as `Nišavska oblast`
- local units such as municipalities, cities, and city municipalities

That is useful analytically, but not convenient for chart logic. A dedicated dictionary lets us:
- aggregate local rows to district, region, or macro-region level
- filter only true municipalities
- split out city municipalities when needed
- roll some local units back up to city groups such as `Grad Niš` or `Grad Novi Sad`

## Hierarchy Used

### Level 1. Country
- code example: `RS`
- label example: `REPUBLIC OF SERBIA`

### Level 2. Macro region
- code examples: `RS1`, `RS2`
- labels:
  - `SRBIJA – SEVER`
  - `SRBIJA – JUG`

### Level 3. Statistical region
- code examples: `RS11`, `RS12`, `RS21`, `RS22`
- labels:
  - `Beogradski region`
  - `Region Vojvodine`
  - `Region Šumadije i Zapadne Srbije`
  - `Region Južne i Istočne Srbije`

### Level 4. Administrative district
- code examples: `RS110`, `RS123`, `RS225`
- labels:
  - `Beogradski region` (project display alias for `Beogradska oblast`)
  - `Južnobačka oblast`
  - `Nišavska oblast`

### Level 5. Local unit
- numeric code examples: `70645`, `79022`, `89010`
- local unit types:
  - `municipality`
  - `city`
  - `city_municipality`

## Column Dictionary

### Identity columns
- `territory_code`
  meaning: unique territory key
  format:
  - `RS`
  - `RS...` for higher aggregate levels
  - five-digit numeric code for local units

- `territory_name`
  meaning: display name from the source file
  format: text

### Hierarchy columns
- `territory_level`
  meaning: named hierarchy level
  allowed values:
  - `country`
  - `macro_region`
  - `statistical_region`
  - `administrative_district`
  - `local_unit`

- `territory_level_order`
  meaning: numeric sort order of the hierarchy
  format: integer `1`-`5`

- `parent_territory_code`
  meaning: direct parent code
  examples:
  - parent of `RS12` is `RS1`
  - parent of `RS225` is `RS22`
  - parent of `70645` is `RS218`

- `parent_territory_name`
  meaning: direct parent label

### Denormalized roll-up columns
- `country_code`, `country_name`
  meaning: top-level Serbia identifiers

- `macro_region_code`, `macro_region_name`
  meaning: the macro region each row belongs to

- `statistical_region_code`, `statistical_region_name`
  meaning: the statistical region each row belongs to

- `administrative_district_code`, `administrative_district_name`
  meaning: the district each row belongs to
  note: filled for districts themselves and for local units; blank for higher levels above district

### Local unit columns
- `local_unit_type`
  meaning: subtype of local units
  allowed values:
  - `municipality`
  - `city`
  - `city_municipality`
  - blank for non-local aggregate levels

- `city_group_code`
  meaning: optional grouping key for city-level roll-up
  examples:
  - `79022` for `Grad Niš`
  - `79049` for `Grad Požarevac`
  - `89010` for `Grad Novi Sad`
  - `CITY_BELGRADE` for Belgrade city municipalities

- `city_group_name`
  meaning: optional city-level grouping label
  examples:
  - `Grad Niš`
  - `Grad Vranje`
  - `Grad Beograd`

### Utility columns
- `is_in_raw_municipality_file`
  meaning: whether the code was observed in the municipality earnings source file
  current expected value: `True` for all rows in this dictionary

- `note`
  meaning: free-text clarification for edge cases
  used now for:
  - the Novi Sad continuity change
  - the synthetic Belgrade city group

## Coverage In The Current Dictionary
- country rows: `1`
- macro regions: `2`
- statistical regions: `4`
- administrative districts: `25`
- local units: `174`
- total rows: `206`

## Grouping Examples

### Group all local rows to district level
Use:
- filter `territory_level = local_unit`
- group by `administrative_district_name`

### Group all local rows to Vojvodina vs other large regions
Use:
- filter `territory_level = local_unit`
- group by `macro_region_name` or `statistical_region_name`

If you want Vojvodina specifically as a large grouping, `statistical_region_name = Region Vojvodine` is usually the cleanest choice.

### Separate city municipalities from standard municipalities
Use:
- filter `territory_level = local_unit`
- split by `local_unit_type`

### Rebuild city-level totals for urban drill-down
Use:
- local rows with non-empty `city_group_code`
- group by `city_group_name`

This is especially useful for:
- Belgrade city municipalities
- Niš and its city municipalities
- Požarevac and Kostolac
- Vranje and Vranjska Banja
- Užice and Sevojno
- historical Novi Sad and Petrovaradin

## Important Caveats
- `CITY_BELGRADE` is a synthetic grouping key added for analytics convenience. It does not exist as a raw `IDTer` code.
- `89010 Grad Novi Sad` overlaps analytically with earlier separate rows `80284 Novi Sad` and `80519 Petrovaradin`. Time-series analysis should treat that continuity carefully.
- The current dictionary is based on the territory codes actually observed in the municipality earnings source file. If later datasets introduce new territorial entities, the dictionary should be regenerated and extended.
