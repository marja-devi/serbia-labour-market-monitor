# Serbia Labour Market Monitor

Live report:
- [https://marja-devi.github.io/serbia-labour-market-monitor/](https://marja-devi.github.io/serbia-labour-market-monitor/)

## Project Overview
This repository is a local analytics portfolio project built on official Serbian SORS open data.

## Open The Report
- Main visual report: [app/earnings_report.html](app/earnings_report.html)
- Main project description: [README.md](README.md)

The live version of the report is published via GitHub Pages at the link above.

The current phase focuses on earnings analysis:
- monthly net and gross earnings by municipality of residence
- quarter-level transformation for analysis
- annual validation against separate annual source files
- portfolio-ready rankings, grouped views, and a local HTML report

This repository is a data portfolio project: it combines a reproducible data pipeline, analytical tables, and a presentation-ready report built from official Serbian SORS open data.

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

These files are stored in [data/raw](data/raw).

Supporting raw files are also available for later expansion:
- republic-level earnings series
- activity-based earnings series
- public-sector earnings series
- employment-modality series
- business-status series
- median earnings and wage-index files

Detailed raw-file descriptions:
- [DATASETS_DESCRIPTION.md](data/raw/DATASETS_DESCRIPTION.md)
- [data_dictionary.md](data_dictionary.md)

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
- [territory_quarter_earnings.csv](data/marts/territory_quarter_earnings.csv)
  The main quarter-level mart with territory hierarchy fields already attached.

- [territory_annual_validation.csv](data/marts/territory_annual_validation.csv)
  Validation table comparing monthly-derived annual averages with annual source values.

- [territory_mart_summary.txt](data/marts/territory_mart_summary.txt)
  Short text summary of row counts and completeness.

### Municipality-Level Analysis
- [republic_net_gross_trend.csv](data/marts/republic_net_gross_trend.csv)
  Republic-level annual net and gross trend with the explicit gross-minus-net gap.

- [belgrade_novi_sad_net_gross_trend.csv](data/marts/belgrade_novi_sad_net_gross_trend.csv)
  City comparison trend for Belgrade and Novi Sad, showing net and gross on one timeline.

- [municipality_ranking_2025.csv](data/marts/municipality_ranking_2025.csv)
  Municipality ranking for 2025.

- [municipality_growth_2018_2025.csv](data/marts/municipality_growth_2018_2025.csv)
  Municipality growth from 2018 to 2025.

- [municipality_qoq_outliers.csv](data/marts/municipality_qoq_outliers.csv)
  Largest quarter-over-quarter changes.

### Grouped Territorial Views
- [group_average_2025_macro_regions.csv](data/marts/group_average_2025_macro_regions.csv)
  Macro-region comparison using the arithmetic average of municipality averages.

- [group_average_2025_districts.csv](data/marts/group_average_2025_districts.csv)
  District comparison using the arithmetic average of municipality averages.

- [group_average_2025_city_groups.csv](data/marts/group_average_2025_city_groups.csv)
  City-group comparison using the arithmetic average of municipality averages.

- [city_drilldown_municipality_ranking_2025.csv](data/marts/city_drilldown_municipality_ranking_2025.csv)
  Municipality ranking inside city drill-down groups such as Belgrade or Niš.

### Visual Report
- [earnings_report.html](app/earnings_report.html)
  Local HTML report built from the mart and analysis outputs.

## Territory Reference
Reference dictionary:
- [territory_dictionary.csv](data/reference/territory_dictionary.csv)

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
- [territory_dictionary.md](docs/territory_dictionary.md)

## How To Explore The Project
Recommended order:
1. open [territory_quarter_earnings.csv](data/marts/territory_quarter_earnings.csv)
2. open [territory_annual_validation.csv](data/marts/territory_annual_validation.csv)
3. open [republic_net_gross_trend.csv](data/marts/republic_net_gross_trend.csv) to inspect net vs gross over time
4. open [municipality_ranking_2025.csv](data/marts/municipality_ranking_2025.csv)
5. open one of the `group_average_*` files for grouped comparisons
6. open [earnings_report.html](app/earnings_report.html) for the portfolio-style view

How to interpret outputs:
- `municipality ranking` means direct comparison of local-unit values
- `group average of municipality averages` means arithmetic average across local-unit averages inside a larger territorial grouping

## Repository Layout
- [data/raw](data/raw) source files
- [data/staging](data/staging) cleaned intermediate outputs
- [data/marts](data/marts) analytics-ready outputs
- [data/reference](data/reference) reusable reference dictionaries
- [docs](docs) project notes and design documents
- [src](src) pipeline code
- [sql](sql) analytical SQL
- [app](app) local visual outputs
- [notebooks](notebooks) exploration workspace

## How To Run
Main local flow:
1. put raw SORS files into [data/raw](data/raw)
2. run `python3 src/build_territory_dictionary.py`
3. run `python3 src/clean.py`
4. run `python3 src/build_marts.py`
5. run `python3 src/analyze_mart.py`
6. run `python3 src/validate.py`
7. run `python3 src/render_report.py`

Main generated outputs will appear in:
- [data/staging](data/staging)
- [data/marts](data/marts)
- [app](app)

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
