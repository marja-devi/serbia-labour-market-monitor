# Data Quality Check

Inspection date: 2026-04-28

## Scope Checked
The quality check covers the first working local workflow:
- [data/raw/avg_monthly_net_earnings_municipality_residence.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/raw/avg_monthly_net_earnings_municipality_residence.csv)
- [data/raw/avg_monthly_gross_earnings_municipality_residence.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/raw/avg_monthly_gross_earnings_municipality_residence.csv)
- [data/raw/annual_avg_monthly_net_earnings_municipality_residence.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/raw/annual_avg_monthly_net_earnings_municipality_residence.csv)
- [data/raw/annual_avg_monthly_gross_earnings_municipality_residence.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/raw/annual_avg_monthly_gross_earnings_municipality_residence.csv)
- [data/staging/stg_earnings_monthly.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/staging/stg_earnings_monthly.csv)
- [data/staging/stg_earnings_annual.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/staging/stg_earnings_annual.csv)
- [data/marts/territory_quarter_earnings.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/territory_quarter_earnings.csv)
- [data/marts/territory_annual_validation.csv](/Users/kinsa/Desktop/Поиск%20работы/Project/data/marts/territory_annual_validation.csv)

## Main Result
The first municipality earnings pipeline looks trustworthy enough to continue.

Strong signals:
- no duplicate business keys in staging or mart outputs
- no null or non-positive values in the four core earnings files
- municipality code to municipality name mapping is consistent
- net and gross files have perfect key parity
- annual validation differences are small on average

## Row Counts
- monthly staging rows: `40,044`
- annual staging rows: `3,268`
- quarterly mart rows: `13,484`
- annual validation rows: `3,680`

Interpretation:
- monthly staging = `20,022 net + 20,022 gross`
- annual staging = `1,634 net + 1,634 gross`
- quarterly mart = `6,742 net + 6,742 gross`

## Key Integrity
- monthly duplicate business keys: `0`
- annual duplicate business keys: `0`
- quarterly mart duplicate business keys: `0`
- municipality code/name conflicts: `0`

Business keys used:
- monthly staging: `municipality_code + year + month + earnings_type`
- annual staging: `municipality_code + year + earnings_type`
- quarterly mart: `municipality_code + year + quarter + earnings_type`

## Coverage Check
- complete monthly coverage exists for `2018-2025`
- `2026` currently contains only months `01` and `02`
- as a result, only `2026 Q1` is incomplete in the quarterly mart

Incomplete quarter rows:
- `408`

Breakdown:
- `2026 Q1 gross`: `204`
- `2026 Q1 net`: `204`

Incomplete annual validation rows:
- `412`

Interpretation:
- the incomplete rows are expected and come from partial 2026 source coverage, not from transformation errors

## Net/Gross Alignment
Monthly key comparison:
- monthly net keys missing in gross: `0`
- monthly gross keys missing in net: `0`

Annual key comparison:
- annual net keys missing in gross: `0`
- annual gross keys missing in net: `0`

Interpretation:
- the four core files can be safely modeled as the same fact structure with `earnings_type` as the differentiator

## Annual Validation Check
Comparison method:
- compute the average of the 12 monthly values for each municipality and earnings type
- compare it to the annual municipality file for the same municipality, year, and earnings type

Validation results for complete municipality-year rows:
- complete annual comparison rows: `3,268`
- average absolute difference: `16.33 RSD`
- maximum absolute difference: `583.75 RSD`

Interpretation:
- the average difference is very small relative to the size of wage values
- the differences are consistent with rounding or source publication conventions rather than obvious pipeline defects

Largest observed outliers:
- `80454 Titel 2019 gross`: `-583.75 RSD`
- `80454 Titel 2019 net`: `-436.42 RSD`
- `80225 Kovin 2019 gross`: `-219.5 RSD`
- `70548 Žitorađa 2020 gross`: `-213.83 RSD`
- `70548 Žitorađa 2025 gross`: `195.58 RSD`

## Quality Risks To Keep In Mind
- annual municipality files may use source-side rounding that does not equal a simple arithmetic average of displayed monthly values
- `2026` is partial and should not be treated as a complete year
- municipality names are consistent now, but future external reference tables may use different spelling or encoding conventions

## Practical Conclusion
The municipality earnings data is strong enough to continue with:
- analytical profiling
- municipality-quarter trend analysis
- portfolio charts and summary findings

The next quality-related improvement would be to add reference-table checks after municipality and territory dimensions are available.
