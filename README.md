# Serbia Labour Market Monitor

## Project Overview
This repository is a local analytics portfolio project built on official Serbian SORS open data.

The current phase focuses on earnings analysis:
- monthly net and gross earnings by municipality of residence
- quarter-level transformation for analysis
- annual validation against separate annual source files
- portfolio-ready rankings, grouped views, and a local HTML report

This is not a personal portfolio website repository. It is a data pipeline and analytics project.

## Analytical Scope
Current main grain:
- `territory × quarter × earnings_type`

Current scope:
- clean and standardize municipality earnings files
- build a quarter-level mart
- attach territory hierarchy for grouping and drill-down
- generate analytical CSV outputs and a visual report

Future scope, once more source files are added:
- employment joins
- gender and territory dimensions
- broader labour-market analysis beyond earnings

## Data
Primary raw files currently used:
1. `avg_monthly_net_earnings_municipality_residence.csv`
2. `avg_monthly_gross_earnings_municipality_residence.csv`
3. `annual_avg_monthly_net_earnings_municipality_residence.csv`
4. `annual_avg_monthly_gross_earnings_municipality_residence.csv`

These files are stored in [data/raw](/Users/kinsa/Desktop/Поиск%20работы/Project/data/raw).

Supporting raw files are also available for later expansion:
- republic-level earnings series
- activity-based earnings series
- public-sector earnings series
- employment-modality series
- business-status series
- median earnings and wage-index files

Detailed raw-file descriptions:
- [DATASETS_DESCRIPTION.md](/Users/kinsa/Desktop/Поиск%20работы/Project/data/raw/DATASETS_DESCRIPTION.md)
- [data_dictionary.md](/Users/kinsa/Desktop/Поиск%20работы/Project/data_dictionary.md)

## Methods
Pipeline:
`raw -> staging -> marts -> analysis -> report`

Main transformation logic:
- parse monthly municipality earnings
- derive `quarter` from `month`
- keep `net` and `gross` as separate measures
- compare monthly-derived annual averages against annual source files
- enrich outputs with territory hierarchy fields

Important modeling rule:
- municipality rankings use direct local-unit values
- grouped regional views use the `median of municipality averages`
- grouped views are intentionally not presented as weighted regional means, because the current sources do not include employment weights

## Outputs
### Main Tables
- [territory_quarter_earnings.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/territory_quarter_earnings.csv)
  The main quarter-level mart with territory hierarchy fields already attached.

- [territory_annual_validation.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/territory_annual_validation.csv)
  Validation table comparing monthly-derived annual averages with annual source values.

- [territory_mart_summary.txt](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/territory_mart_summary.txt)
  Short text summary of row counts and completeness.

### Municipality-Level Analysis
- [republic_net_gross_trend.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/republic_net_gross_trend.csv)
  Republic-level annual net and gross trend with the explicit gross-minus-net gap.

- [belgrade_novi_sad_net_gross_trend.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/belgrade_novi_sad_net_gross_trend.csv)
  City comparison trend for Belgrade and Novi Sad, showing net and gross on one timeline.

- [municipality_ranking_2025.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/municipality_ranking_2025.csv)
  Municipality ranking for 2025.

- [municipality_growth_2018_2025.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/municipality_growth_2018_2025.csv)
  Municipality growth from 2018 to 2025.

- [municipality_qoq_outliers.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/municipality_qoq_outliers.csv)
  Largest quarter-over-quarter changes.

### Grouped Territorial Views
- [group_median_2025_macro_regions.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/group_median_2025_macro_regions.csv)
  Macro-region comparison using the median of municipality averages.

- [group_median_2025_districts.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/group_median_2025_districts.csv)
  District comparison using the median of municipality averages.

- [group_median_2025_city_groups.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/group_median_2025_city_groups.csv)
  City-group comparison using the median of municipality averages.

- [city_drilldown_municipality_ranking_2025.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/city_drilldown_municipality_ranking_2025.csv)
  Municipality ranking inside city drill-down groups such as Belgrade or Niš.

### Visual Report
- [earnings_report.html](/Users/kinsa/Desktop/Поиск%20работы/Project/app/earnings_report.html)
  Local HTML report built from the mart and analysis outputs.

## Territory Reference
Reference dictionary:
- [territory_dictionary.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/reference/territory_dictionary.csv)

This file connects local units to:
- macro regions
- statistical regions
- administrative districts
- city drill-down groups

Most useful columns:
- `territory_code`
- `territory_level`
- `macro_region_name`
- `administrative_district_name`
- `local_unit_type`
- `city_group_name`

Supporting documentation:
- [territory_dictionary.md](/Users/kinsa/Desktop/Поиск%20работы/Project/docs/territory_dictionary.md)

## How To Explore The Project
Recommended order:
1. open [territory_quarter_earnings.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/territory_quarter_earnings.csv)
2. open [territory_annual_validation.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/territory_annual_validation.csv)
3. open [republic_net_gross_trend.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/republic_net_gross_trend.csv) to inspect net vs gross over time
4. open [municipality_ranking_2025.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/municipality_ranking_2025.csv)
5. open one of the `group_median_*` files for grouped comparisons
6. open [earnings_report.html](/Users/kinsa/Desktop/Поиск%20работы/Project/app/earnings_report.html) for the portfolio-style view

How to interpret outputs:
- `municipality ranking` means direct comparison of local-unit values
- `group median of municipality averages` means median across local-unit averages inside a larger territorial grouping

## Repository Layout
- [data/raw](/Users/kinsa/Desktop/Поиск%20работы/Project/data/raw) source files
- [data/staging](/Users/kinsa/Desktop/Поиск%20работы/Project/data/staging) cleaned intermediate outputs
- [data/marts](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts) analytics-ready outputs
- [data/reference](/Users/kinsa/Desktop/Поиск%20работы/Project/data/reference) reusable reference dictionaries
- [docs](/Users/kinsa/Desktop/Поиск%20работы/Project/docs) project notes and design documents
- [src](/Users/kinsa/Desktop/Поиск%20работы/Project/src) pipeline code
- [sql](/Users/kinsa/Desktop/Поиск%20работы/Project/sql) analytical SQL
- [app](/Users/kinsa/Desktop/Поиск%20работы/Project/app) local visual outputs
- [notebooks](/Users/kinsa/Desktop/Поиск%20работы/Project/notebooks) exploration workspace

## How To Run
Main local flow:
1. put raw SORS files into [data/raw](/Users/kinsa/Desktop/Поиск%20работы/Project/data/raw)
2. run `python3 src/build_territory_dictionary.py`
3. run `python3 src/clean.py`
4. run `python3 src/build_marts.py`
5. run `python3 src/analyze_mart.py`
6. run `python3 src/validate.py`
7. run `python3 src/render_report.py`

Main generated outputs will appear in:
- [data/staging](/Users/kinsa/Desktop/Поиск%20работы/Project/data/staging)
- [data/marts](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts)
- [app](/Users/kinsa/Desktop/Поиск%20работы/Project/app)

## Limitations
- current grouped regional views are not weighted by employment
- `2026` is partial and should not be used for full-year comparison
- the Novi Sad area has a continuity issue across years:
  - `80284 Novi Sad`
  - `80519 Petrovaradin`
  - later `89010 Grad Novi Sad`
- employment and broader labour-market dimensions are not yet integrated

## Current Status
- raw wage datasets inspected
- data dictionary and territory dictionary prepared
- staging and mart pipeline implemented
- annual validation implemented
- analytical CSV outputs generated
- local HTML report generated
