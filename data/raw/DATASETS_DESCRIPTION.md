# Raw Datasets Description

Updated: 2026-05-05

## What This File Contains
This document is a practical reference for the raw SORS CSV files currently stored in this folder.

For each dataset it describes:
- what the dataset appears to represent
- how many data records it contains
- what time period it covers
- what columns it has
- what each column means
- what value format is used in each column

Notes:
- record counts below mean data rows only, without the header row
- all files are semicolon-separated CSV files
- raw values are stored as text in CSV, even when they represent numbers

## Folder Summary
- total CSV datasets: `39`
- duplicate raw datasets found: `0`
- duplicate raw datasets deleted: `0`

## Core Files For The Current Portfolio Phase
These are the six most important files for the municipality earnings workflow already implemented in the project:

- `avg_monthly_net_earnings_municipality_residence.csv`
- `avg_monthly_gross_earnings_municipality_residence.csv`
- `annual_avg_monthly_net_earnings_municipality_residence.csv`
- `annual_avg_monthly_gross_earnings_municipality_residence.csv`
- `registered_employment_by_sex_municipality_residence.csv`
- `registered_employment_by_sex_municipality_residence_quarterly.csv`

Why these six matter now:
- the four earnings files provide the actual wage values
- the two registered-employment files provide weights for grouped regional comparisons

## Common Value Conventions

### Time Fields
- `god`
  meaning: calendar year
  format: `YYYY`
  examples: `1963`, `2018`, `2025`

- `mes`
  meaning: month code inside the year
  format:
  - monthly files: `01` to `12`
  - annual files: `00`
  examples: `01`, `09`, `12`, `00`

### Territory Fields
- `IDTer`
  meaning: territorial code used by SORS
  format: alphanumeric code
  examples:
  - republic level: `RS`
  - macro region: `RS1`
  - oblast: `RS123`
  - municipality: `70017`
  - city aggregate: `89010`

- `nTer`
  meaning: territory name corresponding to `IDTer`
  format: text
  examples: `REPUBLIC OF SERBIA`, `Aleksandrovac`, `Grad Novi Sad`

### Value Fields
- `vrednost`
  meaning: measured value
  format:
  - most earnings datasets: integer-like numeric text in `RSD`
  - index dataset: decimal numeric text
  - some historical gross datasets: empty string where value is unavailable
  examples: `50048`, `69218`, `207.9`, ``

- `idJedinicaMere`
  meaning: measurement unit code
  format: text code
  examples: `RSD`, `NR`, `I_PPYR`

- `nJedinicaMere`
  meaning: measurement unit label
  format: text
  examples: `RSD`, `number`, `index, previous year = 100`

### Metadata Fields
- `idindikator`
  meaning: SORS indicator identifier
  format: alphanumeric code
  examples: `2403040103IND01`, `2403040403IND02`

- `Indikator`
  meaning: human-readable indicator label
  format: text
  examples: `Average net earnings`, `Median gross earnings`

- `nIzvorI`
  meaning: source organization label
  format: text
  examples: `SORS`

- `IDStatusPodatka`
  meaning: data status code
  format: short text code
  examples:
  - `A` = normal value
  - `L` = missing value, data exist but were not collected
  - `M` = missing value, data cannot exist

- `nStatusPodatka`
  meaning: text explanation of the data status
  format: text
  examples: `Normal value`, `Missing value - data cannot exist`

### Classification Fields
- `IDPol`
  meaning: sex classification code
  format: text or numeric-like text
  examples: `0`, `1`, `2`

- `nPol`
  meaning: sex classification label
  format: text
  examples: `Total`, `Male`, `Female`

- `IDKD08`
  meaning: activity classification code
  format: text or numeric-like text
  examples: `0`, `01`

- `nkd08`
  meaning: activity classification label
  format: text
  examples: `Total`, `Crop and animal production, hunting and related service activities`

- `IDJavniSEK`
  meaning: public sector category code
  format: text or numeric-like text
  examples: `0`, `1`, `2`

- `nJavniSEK`
  meaning: public sector category label
  format: text
  examples: `Total`

- `IDModalitetZarZap`
  meaning: employment modality code
  format: text or numeric-like text
  examples: `0`, `1`

- `nModalitetZarZap`
  meaning: employment modality label
  format: text
  examples: `Total`

- `IDModalitetRegZap`
  meaning: registered-employment modality code
  format: text or numeric-like text
  examples: `0`, `01`, `02`, `03`

- `nModalitetRegZap`
  meaning: registered-employment modality label
  format: text
  examples:
  - `Registered employment - total`
  - `Employees at legal entities...`
  - `Entrepreneurs and their employees...`
  - `Registered individual agricultural producers (farmers)`

- `IDZarStatusPS`
  meaning: business entity status code used in the wage dataset
  format: text or numeric-like text
  examples: `0`, `1`

- `nZarStatusPS`
  meaning: business entity status label
  format: text
  examples: `Total`, `Salaries and wages of employees at legal entities`

- `IDIndeksZarada`
  meaning: wage index type code
  format: text or numeric-like text
  examples: `1`, `2`

- `nIndeksZarada`
  meaning: wage index type label
  format: text
  examples: `Nominal wage indices`, `Real wage indices`

## Schema Families

### Schema A: Basic Territory Earnings Schema
Typical columns:
- `idindikator`
- `IDTer`
- `nTer`
- `mes`
- `god`
- `vrednost`
- `idJedinicaMere`
- `nJedinicaMere`
- `nIzvorI`
- `Indikator`
- `IDStatusPodatka`
- `nStatusPodatka`

Meaning:
- one measurement by territory and time

Used by:
- republic totals
- municipality residence files
- annual republic files
- annual municipality files

### Schema B: Basic Territory Earnings Schema With Reordered Time
Typical columns:
- `idindikator`
- `mes`
- `god`
- `IDTer`
- `nTer`
- `vrednost`
- `idJedinicaMere`
- `nJedinicaMere`
- `nIzvorI`
- `Indikator`
- `IDStatusPodatka`
- `nStatusPodatka`

Meaning:
- same business meaning as Schema A
- only the column order differs

Used by:
- municipality annual and monthly files
- median files
- annual average annual earnings files

### Schema C: Activity Classification Schema
Typical columns:
- `idindikator`
- `IDTer` or `mes` first depending on file
- `nTer`
- `IDKD08`
- `nkd08`
- `mes`
- `god`
- `vrednost`
- `idJedinicaMere`
- `nJedinicaMere`
- `nIzvorI`
- `Indikator`
- `IDStatusPodatka`
- `nStatusPodatka`

Meaning:
- one measurement by activity class and time

### Schema D: Public Sector Schema
Typical columns:
- `idindikator`
- `IDTer`
- `nTer`
- `IDJavniSEK`
- `nJavniSEK`
- `mes`
- `god`
- `vrednost`
- `idJedinicaMere`
- `nJedinicaMere`
- `nIzvorI`
- `Indikator`
- `IDStatusPodatka`
- `nStatusPodatka`

Meaning:
- one measurement by public sector category and time

### Schema E: Employment Modality Schema
Typical columns:
- `idindikator`
- `IDTer`
- `nTer`
- `IDModalitetZarZap`
- `nModalitetZarZap`
- `mes`
- `god`
- `vrednost`
- `idJedinicaMere`
- `nJedinicaMere`
- `nIzvorI`
- `Indikator`
- `IDStatusPodatka`
- `nStatusPodatka`

Meaning:
- one measurement by employment modality and time

### Schema F: Business Entity Status Schema
Typical columns:
- `idindikator`
- `IDTer`
- `nTer`
- `IDZarStatusPS`
- `nZarStatusPS`
- `mes`
- `god`
- `vrednost`
- `idJedinicaMere`
- `nJedinicaMere`
- `nIzvorI`
- `Indikator`
- `IDStatusPodatka`
- `nStatusPodatka`

Meaning:
- one measurement by business entity status and time

### Schema G: Wage Index Schema
Typical columns:
- `idindikator`
- `IDIndeksZarada`
- `nIndeksZarada`
- `IDTer`
- `nTer`
- `mes`
- `god`
- `vrednost`
- `idJedinicaMere`
- `nJedinicaMere`
- `nIzvorI`
- `Indikator`
- `IDStatusPodatka`
- `nStatusPodatka`

Meaning:
- one index value by index type and year

### Schema H: Employment By Sex And Territory Schema
Typical columns:
- `idindikator`
- `IDTer`
- `nTer`
- `mes`
- `god`
- `IDPol`
- `nPol`
- `vrednost`
- `idJedinicaMere`
- `nJedinicaMere`
- `nIzvorI`
- `Indikator`
- `IDStatusPodatka`
- `nStatusPodatka`

Meaning:
- one employment count by territory, time, and sex
- `IDPol = 0` / `nPol = Total` is the most useful slice for weighting grouped earnings

### Schema I: Employment By Modality And Territory Schema
Typical columns:
- `idindikator`
- `mes`
- `god`
- `IDModalitetRegZap`
- `nModalitetRegZap`
- `IDTer`
- `nTer`
- `vrednost`
- `idJedinicaMere`
- `nJedinicaMere`
- `nIzvorI`
- `Indikator`
- `IDStatusPodatka`
- `nStatusPodatka`

Meaning:
- one employment count by territory, time, and registered-employment modality
- useful when we need workplace-based employment totals or modality-specific weighting

## Detailed Dataset Reference

### `avg_monthly_net_earnings_republic.csv`
- dataset meaning: average monthly net earnings, republic-level total
- records: `590`
- time period:
  - years: `1977-2026`
  - months present: `01-12`
- grain: one row per `territory + month + year`
- schema family: `Schema A`
- columns:
  - `idindikator`: indicator id, alphanumeric text
  - `IDTer`: territory code, text, here usually `RS`
  - `nTer`: territory name, text
  - `mes`: month code, two-digit text
  - `god`: year, four-digit text
  - `vrednost`: net earnings value, numeric text in `RSD`
  - `idJedinicaMere`: unit code, text, usually `RSD`
  - `nJedinicaMere`: unit label, text, usually `RSD`
  - `nIzvorI`: source label, text
  - `Indikator`: indicator label, text
  - `IDStatusPodatka`: status code, text
  - `nStatusPodatka`: status description, text

### `avg_monthly_gross_earnings_republic.csv`
- dataset meaning: average monthly gross earnings, republic-level total
- records: `590`
- time period:
  - years: `1977-2026`
  - months present: `01-12`
- grain: one row per `territory + month + year`
- schema family: `Schema A`
- special note: some early `vrednost` values are empty and marked with status `L`
- columns: same column set and formats as `avg_monthly_net_earnings_republic.csv`

### `avg_monthly_net_earnings_municipality_residence.csv`
- dataset meaning: average monthly net earnings by municipality of residence of employees
- records: `20022`
- time period:
  - years: `2018-2026`
  - months present: `01-12`
- grain: one row per `municipality or higher territory code + month + year`
- schema family: `Schema B`
- columns:
  - `idindikator`: indicator id, alphanumeric text
  - `mes`: month code, two-digit text
  - `god`: year, four-digit text
  - `IDTer`: territory code, text
  - `nTer`: territory name, text
  - `vrednost`: net earnings value, numeric text in `RSD`
  - `idJedinicaMere`: unit code, text
  - `nJedinicaMere`: unit label, text
  - `nIzvorI`: source label, text
  - `Indikator`: indicator label, text
  - `IDStatusPodatka`: status code, text
  - `nStatusPodatka`: status description, text

### `avg_monthly_gross_earnings_activity_division.csv`
- dataset meaning: average monthly gross earnings by activity division
- records: `32634`
- time period:
  - years: `2000-2026`
  - months present: `01-12`
- grain: one row per `territory + activity division + month + year`
- schema family: `Schema C`
- columns:
  - `idindikator`: indicator id, alphanumeric text
  - `IDTer`: territory code, text
  - `nTer`: territory name, text
  - `IDKD08`: activity code, text
  - `nkd08`: activity label, text
  - `mes`: month code, two-digit text
  - `god`: year, four-digit text
  - `vrednost`: gross earnings value, numeric text in `RSD`
  - `idJedinicaMere`: unit code, text
  - `nJedinicaMere`: unit label, text
  - `nIzvorI`: source label, text
  - `Indikator`: indicator label, text
  - `IDStatusPodatka`: status code, text
  - `nStatusPodatka`: status description, text

### `avg_monthly_gross_earnings_municipality_residence.csv`
- dataset meaning: average monthly gross earnings by municipality of residence of employees
- records: `20022`
- time period:
  - years: `2018-2026`
  - months present: `01-12`
- grain: one row per `municipality or higher territory code + month + year`
- schema family: `Schema B`
- columns: same column set and formats as `avg_monthly_net_earnings_municipality_residence.csv`

### `registered_employment_by_sex_municipality_residence.csv`
- dataset meaning: registered employment by sex and municipalities of residence (`NSTJ`), annual level
- records: `6174`
- time period:
  - years: `2016-2025`
  - periods present: annual only, `mes = 00`
- grain: one row per `territory + year + sex`
- schema family: `Schema H`
- why it matters in this project:
  - this is currently the best raw source for `weighted average` calculations in grouped territorial earnings views
  - it matches the `municipality of residence` geography used by the core earnings files
  - the project uses `IDPol = 0` / `nPol = Total` as the weight slice
- important note:
  - the dataset contains one extra aggregate-like code `70000 Retained`, which does not appear in the current earnings files and should be excluded when building weights
- columns:
  - `idindikator`: indicator id, alphanumeric text
  - `IDTer`: territory code, text
  - `nTer`: territory name, text
  - `mes`: period code, annual file uses `00`
  - `god`: year, four-digit text
  - `IDPol`: sex code, text
  - `nPol`: sex label, text
  - `vrednost`: registered employment count, numeric text in `number`
  - `idJedinicaMere`: unit code, here `NR`
  - `nJedinicaMere`: unit label, here `number`
  - `nIzvorI`: source label, text
  - `Indikator`: indicator label, text
  - `IDStatusPodatka`: status code, text
  - `nStatusPodatka`: status description, text

### `registered_employment_by_sex_municipality_residence_quarterly.csv`
- dataset meaning: registered employment by sex and municipalities of residence (`NSTJ`), quarterly level
- records: `25293`
- time period:
  - years: `2016-2026`
  - quarters present: `K1-K4`
- grain: one row per `territory + quarter + year + sex`
- schema family: `Schema H`
- why it matters in this project:
  - it can support quarter-aligned weighting later if we decide to weight `territory × quarter` comparisons instead of annual grouped views only
  - it uses the same residence-based territorial logic as the core municipality earnings files
- columns:
  - `idindikator`: indicator id, alphanumeric text
  - `IDTer`: territory code, text
  - `nTer`: territory name, text
  - `mes`: quarter code, here values such as `K1`, `K2`, `K3`, `K4`
  - `god`: year, four-digit text
  - `IDPol`: sex code, text
  - `nPol`: sex label, text
  - `vrednost`: registered employment count, numeric text in `number`
  - `idJedinicaMere`: unit code, here `NR`
  - `nJedinicaMere`: unit label, here `number`
  - `nIzvorI`: source label, text
  - `Indikator`: indicator label, text
  - `IDStatusPodatka`: status code, text
  - `nStatusPodatka`: status description, text

### `registered_employment_by_municipality_work.csv`
- dataset meaning: registered employment by municipalities of work (`NSTJ`), annual level
- records: `9016`
- time period:
  - years: `2015-2025`
  - periods present: annual only, `mes = 00`
- grain: one row per `territory + year + registered-employment modality`
- schema family: `Schema I`
- why it is useful:
  - it is a strong employment source, but it is based on `municipality of work`, not `municipality of residence`
  - because the current core earnings files are residence-based, this file is not the first choice for weighting the existing Block 1 grouped earnings views
- columns:
  - `idindikator`: indicator id, alphanumeric text
  - `mes`: period code, annual file uses `00`
  - `god`: year, four-digit text
  - `IDModalitetRegZap`: registered-employment modality code, text
  - `nModalitetRegZap`: registered-employment modality label, text
  - `IDTer`: territory code, text
  - `nTer`: territory name, text
  - `vrednost`: employment count, numeric text in `number`
  - `idJedinicaMere`: unit code, here `NR`
  - `nJedinicaMere`: unit label, here `number`
  - `nIzvorI`: source label, text
  - `Indikator`: indicator label, text
  - `IDStatusPodatka`: status code, text
  - `nStatusPodatka`: status description, text

### `employed_by_regions_work.csv`
- dataset meaning: employed by regions (`NSTJ` based on municipality of work), quarterly level
- records: `1312`
- time period:
  - years: `2016-2026`
  - quarters present: `K1-K4`
- grain: one row per `region + quarter + year + registered-employment modality`
- schema family: `Schema I`
- why it is useful:
  - this is helpful for macro-region and regional context
  - but it is still `municipality/region of work` based, so it is not the cleanest direct weight source for residence-based earnings files
- columns:
  - `idindikator`: indicator id, alphanumeric text
  - `IDTer`: territory code, text
  - `nTer`: territory name, text
  - `mes`: quarter code, values such as `K1`, `K2`, `K3`, `K4`
  - `god`: year, four-digit text
  - `IDModalitetRegZap`: registered-employment modality code, text
  - `nModalitetRegZap`: registered-employment modality label, text
  - `vrednost`: employment count, numeric text in `number`
  - `idJedinicaMere`: unit code, here `NR`
  - `nJedinicaMere`: unit label, here `number`
  - `nIzvorI`: source label, text
  - `Indikator`: indicator label, text
  - `IDStatusPodatka`: status code, text
  - `nStatusPodatka`: status description, text

### `avg_monthly_net_earnings_public_sector.csv`
- dataset meaning: average monthly net earnings in the public sector
- records: `3614`
- time period:
  - years: `2003-2026`
  - months present: `01-12`
- grain: one row per `territory + public sector category + month + year`
- schema family: `Schema D`
- columns:
  - `idindikator`: indicator id, alphanumeric text
  - `IDTer`: territory code, text
  - `nTer`: territory name, text
  - `mes`: month code, two-digit text
  - `god`: year, four-digit text
  - `IDJavniSEK`: public sector category code, text
  - `nJavniSEK`: public sector category label, text
  - `vrednost`: net earnings value, numeric text in `RSD`
  - `idJedinicaMere`: unit code, text
  - `nJedinicaMere`: unit label, text
  - `nIzvorI`: source label, text
  - `Indikator`: indicator label, text
  - `IDStatusPodatka`: status code, text
  - `nStatusPodatka`: status description, text

### `avg_monthly_gross_earnings_public_sector.csv`
- dataset meaning: average monthly gross earnings in the public sector
- records: `3614`
- time period:
  - years: `2003-2026`
  - months present: `01-12`
- grain: one row per `territory + public sector category + month + year`
- schema family: `Schema D`
- columns: same column set and formats as `avg_monthly_net_earnings_public_sector.csv`

### `avg_monthly_net_earnings_employment_modality.csv`
- dataset meaning: average monthly net earnings by employment modality
- records: `294`
- time period:
  - years: `2018-2026`
  - months present: `01-12`
- grain: one row per `territory + modality + month + year`
- schema family: `Schema E`
- columns:
  - `idindikator`: indicator id, alphanumeric text
  - `IDTer`: territory code, text
  - `nTer`: territory name, text
  - `IDModalitetZarZap`: modality code, text
  - `nModalitetZarZap`: modality label, text
  - `mes`: month code, two-digit text
  - `god`: year, four-digit text
  - `vrednost`: net earnings value, numeric text in `RSD`
  - `idJedinicaMere`: unit code, text
  - `nJedinicaMere`: unit label, text
  - `nIzvorI`: source label, text
  - `Indikator`: indicator label, text
  - `IDStatusPodatka`: status code, text
  - `nStatusPodatka`: status description, text

### `avg_monthly_gross_earnings_employment_modality.csv`
- dataset meaning: average monthly gross earnings by employment modality
- records: `294`
- time period:
  - years: `2018-2026`
  - months present: `01-12`
- grain: one row per `territory + modality + month + year`
- schema family: `Schema E`
- columns: same column set and formats as `avg_monthly_net_earnings_employment_modality.csv`

### `avg_monthly_net_earnings_business_entity_status.csv`
- dataset meaning: average monthly net earnings by business entity status
- records: `294`
- time period:
  - years: `2018-2026`
  - months present: `01-12`
- grain: one row per `territory + business entity status + month + year`
- schema family: `Schema F`
- columns:
  - `idindikator`: indicator id, alphanumeric text
  - `IDTer`: territory code, text
  - `nTer`: territory name, text
  - `IDZarStatusPS`: business entity status code, text
  - `nZarStatusPS`: business entity status label, text
  - `mes`: month code, two-digit text
  - `god`: year, four-digit text
  - `vrednost`: net earnings value, numeric text in `RSD`
  - `idJedinicaMere`: unit code, text
  - `nJedinicaMere`: unit label, text
  - `nIzvorI`: source label, text
  - `Indikator`: indicator label, text
  - `IDStatusPodatka`: status code, text
  - `nStatusPodatka`: status description, text

### `avg_monthly_gross_earnings_business_entity_status.csv`
- dataset meaning: average monthly gross earnings by business entity status
- records: `294`
- time period:
  - years: `2018-2026`
  - months present: `01-12`
- grain: one row per `territory + business entity status + month + year`
- schema family: `Schema F`
- columns: same column set and formats as `avg_monthly_net_earnings_business_entity_status.csv`

### `median_monthly_net_earnings_republic.csv`
- dataset meaning: median monthly net earnings at republic level
- records: `98`
- time period:
  - years: `2018-2026`
  - months present: `01-12`
- grain: one row per `territory + month + year`
- schema family: `Schema B`
- columns: same column set and formats as `avg_monthly_net_earnings_municipality_residence.csv`

### `median_monthly_gross_earnings_republic.csv`
- dataset meaning: median monthly gross earnings at republic level
- records: `98`
- time period:
  - years: `2018-2026`
  - months present: `01-12`
- grain: one row per `territory + month + year`
- schema family: `Schema B`
- columns: same column set and formats as `avg_monthly_net_earnings_municipality_residence.csv`

### `ytd_avg_net_earnings_activity_division.csv`
- dataset meaning: year-to-date average net earnings by activity division
- records: `10080`
- time period:
  - years: `2018-2026`
  - months present: `01-12`
- grain: one row per `territory + activity division + month + year`
- schema family: `Schema C`
- note: values are cumulative from January to the given month
- columns: same column set and formats as `avg_monthly_gross_earnings_activity_division.csv`

### `ytd_avg_gross_earnings_activity_division.csv`
- dataset meaning: year-to-date average gross earnings by activity division
- records: `10080`
- time period:
  - years: `2018-2026`
  - months present: `01-12`
- grain: one row per `territory + activity division + month + year`
- schema family: `Schema C`
- note: values are cumulative from January to the given month
- columns: same column set and formats as `avg_monthly_gross_earnings_activity_division.csv`

### `ytd_avg_gross_earnings_municipality_residence.csv`
- dataset meaning: year-to-date average gross earnings by municipality of residence of employees
- records: `20022`
- time period:
  - years: `2018-2026`
  - months present: `01-12`
- grain: one row per `municipality or higher territory code + month + year`
- schema family: `Schema B`
- note: values are cumulative from January to the given month
- columns: same column set and formats as `avg_monthly_net_earnings_municipality_residence.csv`

### `ytd_avg_net_earnings_public_sector.csv`
- dataset meaning: year-to-date average net earnings in the public sector
- records: `1274`
- time period:
  - years: `2018-2026`
  - months present: `01-12`
- grain: one row per `territory + public sector category + month + year`
- schema family: `Schema D`
- note: values are cumulative from January to the given month
- columns: same column set and formats as `avg_monthly_net_earnings_public_sector.csv`

### `ytd_avg_gross_earnings_public_sector.csv`
- dataset meaning: year-to-date average gross earnings in the public sector
- records: `1274`
- time period:
  - years: `2018-2026`
  - months present: `01-12`
- grain: one row per `territory + public sector category + month + year`
- schema family: `Schema D`
- note: values are cumulative from January to the given month
- columns: same column set and formats as `avg_monthly_net_earnings_public_sector.csv`

### `ytd_avg_net_earnings_employment_modality.csv`
- dataset meaning: year-to-date average net earnings by employment modality
- records: `294`
- time period:
  - years: `2018-2026`
  - months present: `01-12`
- grain: one row per `territory + modality + month + year`
- schema family: `Schema E`
- note: values are cumulative from January to the given month
- columns: same column set and formats as `avg_monthly_net_earnings_employment_modality.csv`

### `ytd_avg_gross_earnings_employment_modality.csv`
- dataset meaning: year-to-date average gross earnings by employment modality
- records: `294`
- time period:
  - years: `2018-2026`
  - months present: `01-12`
- grain: one row per `territory + modality + month + year`
- schema family: `Schema E`
- note: values are cumulative from January to the given month
- columns: same column set and formats as `avg_monthly_net_earnings_employment_modality.csv`

### `annual_avg_monthly_net_earnings_republic.csv`
- dataset meaning: annual average of monthly net earnings at republic level
- records: `63`
- time period:
  - years: `1963-2025`
  - month code present: `00`
- grain: one row per `territory + year`
- schema family: `Schema A`
- note: `mes = 00` marks annual data rather than a real month
- columns: same column set and formats as `avg_monthly_net_earnings_republic.csv`

### `annual_avg_monthly_gross_earnings_republic.csv`
- dataset meaning: annual average of monthly gross earnings at republic level
- records: `63`
- time period:
  - years: `1963-2025`
  - month code present: `00`
- grain: one row per `territory + year`
- schema family: `Schema A`
- note: some early `vrednost` values are empty and marked with status `M`
- columns: same column set and formats as `avg_monthly_net_earnings_republic.csv`

### `annual_avg_monthly_net_earnings_activity_division.csv`
- dataset meaning: annual average of monthly net earnings by activity division
- records: `840`
- time period:
  - years: `2018-2025`
  - month code present: `00`
- grain: one row per `territory + activity division + year`
- schema family: `Schema C`
- columns: same column set and formats as `avg_monthly_gross_earnings_activity_division.csv`

### `annual_avg_monthly_gross_earnings_activity_division.csv`
- dataset meaning: annual average of monthly gross earnings by activity division
- records: `840`
- time period:
  - years: `2018-2025`
  - month code present: `00`
- grain: one row per `territory + activity division + year`
- schema family: `Schema C`
- columns: same column set and formats as `avg_monthly_gross_earnings_activity_division.csv`

### `annual_avg_monthly_net_earnings_municipality_residence.csv`
- dataset meaning: annual average of monthly net earnings by municipality of residence of employees
- records: `1634`
- time period:
  - years: `2018-2025`
  - month code present: `00`
- grain: one row per `municipality or higher territory code + year`
- schema family: `Schema B`
- columns: same column set and formats as `avg_monthly_net_earnings_municipality_residence.csv`

### `annual_avg_monthly_gross_earnings_municipality_residence.csv`
- dataset meaning: annual average of monthly gross earnings by municipality of residence of employees
- records: `1634`
- time period:
  - years: `2018-2025`
  - month code present: `00`
- grain: one row per `municipality or higher territory code + year`
- schema family: `Schema B`
- columns: same column set and formats as `avg_monthly_net_earnings_municipality_residence.csv`

### `annual_avg_monthly_net_earnings_public_sector.csv`
- dataset meaning: annual average of monthly net earnings in the public sector
- records: `299`
- time period:
  - years: `2003-2025`
  - month code present: `00`
- grain: one row per `territory + public sector category + year`
- schema family: `Schema D`
- columns: same column set and formats as `avg_monthly_net_earnings_public_sector.csv`

### `annual_avg_monthly_gross_earnings_public_sector.csv`
- dataset meaning: annual average of monthly gross earnings in the public sector
- records: `299`
- time period:
  - years: `2003-2025`
  - month code present: `00`
- grain: one row per `territory + public sector category + year`
- schema family: `Schema D`
- columns: same column set and formats as `avg_monthly_net_earnings_public_sector.csv`

### `annual_avg_monthly_net_earnings_employment_modality.csv`
- dataset meaning: annual average of monthly net earnings by employment modality
- records: `24`
- time period:
  - years: `2018-2025`
  - month code present: `00`
- grain: one row per `territory + modality + year`
- schema family: `Schema E`
- columns: same column set and formats as `avg_monthly_net_earnings_employment_modality.csv`

### `annual_avg_monthly_gross_earnings_employment_modality.csv`
- dataset meaning: annual average of monthly gross earnings by employment modality
- records: `24`
- time period:
  - years: `2018-2025`
  - month code present: `00`
- grain: one row per `territory + modality + year`
- schema family: `Schema E`
- columns: same column set and formats as `avg_monthly_net_earnings_employment_modality.csv`

### `annual_avg_monthly_net_earnings_business_entity_status.csv`
- dataset meaning: annual average of monthly net earnings by business entity status
- records: `24`
- time period:
  - years: `2018-2025`
  - month code present: `00`
- grain: one row per `territory + business entity status + year`
- schema family: `Schema F`
- columns: same column set and formats as `avg_monthly_net_earnings_business_entity_status.csv`

### `annual_avg_monthly_gross_earnings_business_entity_status.csv`
- dataset meaning: annual average of monthly gross earnings by business entity status
- records: `24`
- time period:
  - years: `2018-2025`
  - month code present: `00`
- grain: one row per `territory + business entity status + year`
- schema family: `Schema F`
- columns: same column set and formats as `avg_monthly_net_earnings_business_entity_status.csv`

### `annual_avg_annual_net_earnings_republic.csv`
- dataset meaning: annual average annual net earnings at republic level
- records: `63`
- time period:
  - years: `1963-2025`
  - month code present: `00`
- grain: one row per `territory + year`
- schema family: `Schema B`
- note: unit is `NR / number`, so this file should be interpreted carefully before analytical use
- columns: same column set and formats as `avg_monthly_net_earnings_municipality_residence.csv`

### `annual_avg_annual_gross_earnings_republic.csv`
- dataset meaning: annual average annual gross earnings at republic level
- records: `63`
- time period:
  - years: `1963-2025`
  - month code present: `00`
- grain: one row per `territory + year`
- schema family: `Schema B`
- note: unit is `NR / number`; many early values are empty and marked with status `M`
- columns: same column set and formats as `avg_monthly_net_earnings_municipality_residence.csv`

### `annual_net_earnings_indices_republic.csv`
- dataset meaning: annual indices of net earnings at republic level
- records: `62`
- time period:
  - years: `1995-2025`
  - month code present: `00`
- grain: one row per `territory + index type + year`
- schema family: `Schema G`
- columns:
  - `idindikator`: indicator id, alphanumeric text
  - `IDIndeksZarada`: wage index type code, text
  - `nIndeksZarada`: wage index type label, text
  - `IDTer`: territory code, text
  - `nTer`: territory name, text
  - `mes`: annual marker, text, always `00`
  - `god`: year, four-digit text
  - `vrednost`: index value, decimal numeric text
  - `idJedinicaMere`: unit code, text, here `I_PPYR`
  - `nJedinicaMere`: unit label, text
  - `nIzvorI`: source label, text
  - `Indikator`: indicator label, text
  - `IDStatusPodatka`: status code, text
  - `nStatusPodatka`: status description, text

## Practical Conclusion
The raw folder is now documented at two levels:
- high-level business meaning for each file
- low-level structural metadata for columns, formats, record counts, and periods

For the current project phase, the most important operational datasets remain:
- `avg_monthly_net_earnings_municipality_residence.csv`
- `avg_monthly_gross_earnings_municipality_residence.csv`
- `annual_avg_monthly_net_earnings_municipality_residence.csv`
- `annual_avg_monthly_gross_earnings_municipality_residence.csv`
