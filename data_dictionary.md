# Data Dictionary

Updated: 2026-04-30

## Purpose
This file is the working data dictionary for the portfolio project. It explains the main tables we use now, the meaning of their columns, and how the raw SORS fields flow into staging, marts, and reference dimensions.

It is meant to answer three practical questions:
- what each table represents
- what each column means
- which columns are safe to use for joins, grouping, filtering, and chart drill-down

## Current Data Layers

### 1. Raw data
Location: [data/raw](/Users/kinsa/Desktop/Поиск%20работы/Project/data/raw)

This layer stores the original SORS CSV exports. Files are semicolon-separated, values are kept as text, and source naming is preserved as closely as possible.

Main raw families currently in the project:
- territory earnings
- activity division earnings
- public sector earnings
- employment modality earnings
- business entity status earnings
- republic median and index files

The most important raw files for the first portfolio phase are:
- [avg_monthly_net_earnings_municipality_residence.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/raw/avg_monthly_net_earnings_municipality_residence.csv)
- [avg_monthly_gross_earnings_municipality_residence.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/raw/avg_monthly_gross_earnings_municipality_residence.csv)
- [annual_avg_monthly_net_earnings_municipality_residence.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/raw/annual_avg_monthly_net_earnings_municipality_residence.csv)
- [annual_avg_monthly_gross_earnings_municipality_residence.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/raw/annual_avg_monthly_gross_earnings_municipality_residence.csv)

Full raw-file descriptions remain in [DATASETS_DESCRIPTION.md](/Users/kinsa/Desktop/Поиск%20работы/Project/data/raw/DATASETS_DESCRIPTION.md).

### 2. Staging
Location: [data/staging](/Users/kinsa/Desktop/Поиск%20работы/Project/data/staging)

This layer normalizes raw CSVs into analysis-friendly tables with consistent column names, typed time fields, and one clear business meaning per row.

### 3. Marts
Location: [data/marts](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts)

This layer stores analysis-ready outputs: quarter-level aggregates, validation tables, ranking tables, and derived slices used in the HTML report.

### 4. Reference dimensions
Location: [data/reference](/Users/kinsa/Desktop/Поиск%20работы/Project/data/reference)

This layer stores helper dictionaries that should stay stable across analyses. The first one is the territory hierarchy dictionary used for grouping and drill-down.

## Common Raw Fields

### Time fields
- `god`
  meaning: calendar year
  format: `YYYY`
  examples: `2018`, `2025`

- `mes`
  meaning: month code
  format:
  - monthly files: `01`-`12`
  - annual files: `00`
  note: `00` means the row is an annual summary, not a real month

### Territory fields
- `IDTer`
  meaning: SORS territory code
  format:
  - republic: `RS`
  - macro region: `RS1`, `RS2`
  - statistical region: `RS11`, `RS12`, `RS21`, `RS22`
  - administrative district: `RS110`, `RS121` ... `RS229`
  - local unit: five-digit numeric code such as `70645`, `79022`, `89010`

- `nTer`
  meaning: human-readable territory name
  format: text
  examples: `REPUBLIC OF SERBIA`, `Region Vojvodine`, `Nišavska oblast`, `Kragujevac`, `Grad Niš`

### Value fields
- `vrednost`
  meaning: measured value
  format:
  - wages: integer-like text in `RSD`
  - index file: decimal numeric text
  - some historical gross rows: empty string

- `idJedinicaMere`
  meaning: unit code
  examples: `RSD`, `I_PPYR`

- `nJedinicaMere`
  meaning: unit label
  examples: `RSD`, `index, previous year = 100`

### Metadata fields
- `idindikator`
  meaning: SORS indicator id
  format: alphanumeric text

- `Indikator`
  meaning: indicator label
  examples: `Average net earnings`, `Average gross earnings`

- `nIzvorI`
  meaning: source organization
  expected value now: `SORS`

- `IDStatusPodatka`
  meaning: data status code
  examples:
  - `A` normal value
  - `L` missing, should exist but not collected
  - `M` missing, cannot exist

- `nStatusPodatka`
  meaning: long status description

### Classification fields
- `IDKD08`, `nkd08`
  meaning: activity division code and label

- `IDJavniSEK`, `nJavniSEK`
  meaning: public-sector category code and label

- `IDModalitetZarZap`, `nModalitetZarZap`
  meaning: employment modality code and label

- `IDZarStatusPS`, `nZarStatusPS`
  meaning: business-entity-status code and label

- `IDIndeksZarada`, `nIndeksZarada`
  meaning: wage-index type code and label

## Staging Tables

### `stg_earnings_monthly`
File: [stg_earnings_monthly.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/staging/stg_earnings_monthly.csv)

Grain:
- one row per `source_file + municipality_code + year + month + earnings_type`

Columns:
- `source_file`
  meaning: raw CSV filename that produced the row
  type: text

- `indicator_code`
  meaning: raw `idindikator`
  type: text

- `indicator_name`
  meaning: raw `Indikator`
  type: text

- `earnings_type`
  meaning: normalized measure family
  type: text
  allowed values now: `net`, `gross`

- `municipality_code`
  meaning: raw `IDTer`
  type: text
  note: despite the name, this field currently also contains aggregate territory rows such as `RS12` and `RS225`

- `municipality_name`
  meaning: raw `nTer`
  type: text

- `year`
  meaning: normalized `god`
  type: integer

- `month`
  meaning: normalized `mes`
  type: integer
  allowed values: `1`-`12`

- `quarter`
  meaning: derived quarter label
  type: text
  allowed values: `Q1`, `Q2`, `Q3`, `Q4`

- `year_month`
  meaning: canonical year-month key
  type: text
  format: `YYYY-MM`

- `value_rsd`
  meaning: earnings value in dinars
  type: integer

- `unit_code`
  meaning: raw unit code
  type: text

- `unit_name`
  meaning: raw unit label
  type: text

- `status_code`
  meaning: raw status code
  type: text

- `status_name`
  meaning: raw status label
  type: text

- `source_org`
  meaning: raw source organization
  type: text

Typical uses:
- quarter aggregation
- monthly trend lines
- gap checks
- outlier detection

### `stg_earnings_annual`
File: [stg_earnings_annual.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/staging/stg_earnings_annual.csv)

Grain:
- one row per `source_file + municipality_code + year + earnings_type`

Columns:
- `source_file`, `indicator_code`, `indicator_name`, `earnings_type`, `municipality_code`, `municipality_name`, `unit_code`, `unit_name`, `status_code`, `status_name`, `source_org`
  meaning: same as in `stg_earnings_monthly`

- `year`
  meaning: normalized `god`
  type: integer

- `value_rsd`
  meaning: annual file value in dinars
  type: integer

Typical uses:
- reference benchmark for annual validation
- annual comparison tables

### `dim_municipality_from_earnings`
File: [dim_municipality_from_earnings.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/staging/dim_municipality_from_earnings.csv)

Grain:
- one row per distinct `municipality_code`

Columns:
- `municipality_code`
  meaning: observed territory code in the current earnings pipeline
  type: text

- `municipality_name`
  meaning: observed territory name
  type: text

Note:
- this was a first helper dimension; for grouping and hierarchy work, prefer the richer territory dictionary in `data/reference`

## Reference Dimension

### `territory_dictionary`
File: [territory_dictionary.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/reference/territory_dictionary.csv)

Grain:
- one row per distinct territory code observed in the municipality earnings raw file

Main purpose:
- group charts by large region
- drill down from country to district to local unit
- separate true municipalities from city aggregates and city municipalities

Important columns:
- `territory_code`
  join key to raw/staging/mart territory fields

- `territory_name`
  display label

- `territory_level`
  one of `country`, `macro_region`, `statistical_region`, `administrative_district`, `local_unit`

- `parent_territory_code`
  direct parent inside the hierarchy

- `macro_region_code`, `statistical_region_code`, `administrative_district_code`
  denormalized parent columns for simple grouping in charts

- `local_unit_type`
  one of `municipality`, `city`, `city_municipality`, blank for aggregate non-local levels

- `city_group_code`, `city_group_name`
  optional city roll-up used for urban drill-down
  note: `CITY_BELGRADE` is synthetic because the raw file has Belgrade municipalities but no single aggregate Belgrade row

Full field-by-field description is in [territory_dictionary.md](/Users/kinsa/Desktop/Поиск%20работы/Project/docs/territory_dictionary.md).

## Mart Tables

### `territory_quarter_earnings`
File: [territory_quarter_earnings.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/territory_quarter_earnings.csv)

Grain:
- one row per `municipality_code + year + quarter + earnings_type`

Columns:
- `municipality_code`
  meaning: territory code carried from staging
  type: text

- `municipality_name`
  meaning: territory name carried from staging
  type: text

- `year`
  meaning: year
  type: integer

- `quarter`
  meaning: quarter label
  type: text

- `earnings_type`
  meaning: `net` or `gross`
  type: text

- hierarchy fields copied from `territory_dictionary`
  columns:
  - `territory_level`
  - `territory_level_order`
  - `parent_territory_code`
  - `parent_territory_name`
  - `country_code`
  - `country_name`
  - `macro_region_code`
  - `macro_region_name`
  - `statistical_region_code`
  - `statistical_region_name`
  - `administrative_district_code`
  - `administrative_district_name`
  - `local_unit_type`
  - `city_group_code`
  - `city_group_name`
  meaning: pre-joined territory metadata used for grouping and drill-down without an extra join in charts

- `quarterly_avg_value_rsd`
  meaning: arithmetic mean of the three monthly values in the quarter
  type: decimal

- `months_in_quarter`
  meaning: how many monthly observations were available
  type: integer

- `is_complete_quarter`
  meaning: whether the quarter has all three months
  type: boolean-like text in CSV output

- `month_list`
  meaning: comma-separated list of source months used in the aggregate
  type: text
  example: `01,02,03`

- `min_month_value_rsd`
  meaning: minimum month value inside the quarter
  type: integer

- `max_month_value_rsd`
  meaning: maximum month value inside the quarter
  type: integer

Typical uses:
- quarter-over-quarter comparisons
- annualized 2025 rankings
- charting with complete-quarter filtering

### `territory_annual_validation`
File: [territory_annual_validation.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/territory_annual_validation.csv)

Grain:
- one row per `municipality_code + year + earnings_type`

Columns:
- `municipality_code`
  meaning: territory code

- `municipality_name`
  meaning: territory name

- `year`
  meaning: year

- `earnings_type`
  meaning: `net` or `gross`

- hierarchy fields copied from `territory_dictionary`
  meaning: same enrichment columns as in `territory_quarter_earnings`

- `monthly_observation_count`
  meaning: count of monthly rows available for the year

- `is_complete_year`
  meaning: whether all 12 months are present

- `monthly_avg_value_rsd`
  meaning: average computed from monthly staging rows

- `annual_file_value_rsd`
  meaning: value from the annual raw file

- `difference_rsd`
  meaning: `monthly_avg_value_rsd - annual_file_value_rsd`

Typical uses:
- quality checks
- documentation of data reliability

### Hierarchy analysis outputs
Files:
- [republic_net_gross_trend.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/republic_net_gross_trend.csv)
- [belgrade_novi_sad_net_gross_trend.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/belgrade_novi_sad_net_gross_trend.csv)
- [group_median_2025_macro_regions.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/group_median_2025_macro_regions.csv)
- [group_median_2025_districts.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/group_median_2025_districts.csv)
- [group_median_2025_city_groups.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/group_median_2025_city_groups.csv)
- [city_drilldown_municipality_ranking_2025.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/city_drilldown_municipality_ranking_2025.csv)

Purpose:
- compare annual republic-level net and gross earnings on one timeline and track the gap
- compare Belgrade and Novi Sad on one net-gross timeline using the best available construction for each city
- compare 2025 local-unit earnings after rolling them up to larger territorial levels
- support grouped charts and drill-down views

Interpretation labels to use in charts:
- `municipality ranking`: direct comparison of local-unit values
- `group median of municipality averages`: median across local-unit averages inside a larger grouping

Shared logic:
- source: `municipality_ranking_2025.csv`
- year scope: `2025`
- coverage: only complete local-unit rows
- aggregation:
  - `group_median_2025_macro_regions.csv`, `group_median_2025_districts.csv`, `group_median_2025_city_groups.csv` use the median of local-unit 2025 averages inside each grouping
  - this is intentionally not a weighted regional mean

Key grouping columns:
- `macro_region_name`
- `administrative_district_name`
- `city_group_name`
- `municipality_name` within city drill-down

## Join Guidance

Preferred joins right now:
- raw/staging/marts to territory dictionary:
  `municipality_code` or raw `IDTer` -> `territory_dictionary.territory_code`

- quarterly mart to annual validation:
  `municipality_code + year + earnings_type`

Safe grouping columns from `territory_dictionary`:
- `territory_level`
- `macro_region_name`
- `statistical_region_name`
- `administrative_district_name`
- `city_group_name`
- `local_unit_type`

## Caveats
- The column name `municipality_code` in current staging and mart files is historically convenient but slightly misleading, because the raw municipality file also contains aggregate rows for Serbia, macro regions, statistical regions, and administrative districts.
- `Grad Novi Sad` continuity changes across time: `Novi Sad` and `Petrovaradin` appear separately in earlier years, while later rows use `89010 Grad Novi Sad`.
- Belgrade municipalities are present individually, but the raw file does not contain a single city aggregate code for Belgrade. The territory dictionary adds a synthetic grouping label for that use case.
