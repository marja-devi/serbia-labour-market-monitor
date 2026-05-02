# Dataset Selection

## Current Direction
The raw folder currently gives us a strong wage-analysis starting point, but not yet the full labour-market dataset mix.

Available now:
- monthly municipality earnings
- annual municipality earnings
- national totals
- activity, public-sector, modality, status, median, and index series

Missing for the originally planned full mart:
- employment by sex and municipality
- municipality reference data
- territory hierarchy
- gender reference data

## Why the Main Grain Is Still `municipality × quarter`
The current files already support a useful municipality-quarter mart on the earnings side.

Available wage grain:
- earnings: monthly by municipality

Target modeling step:
- aggregate monthly municipality earnings to quarter

This preserves the original target grain and keeps the project expandable once employment files arrive.

## Selected Core Datasets For The Current Phase

### 1. `avg_monthly_net_earnings_municipality_residence.csv`
Purpose:
- main municipality-level net earnings fact source

Expected handling:
- inspect and standardize municipality code and name
- derive quarter from month
- aggregate monthly net earnings to municipality-quarter

### 2. `avg_monthly_gross_earnings_municipality_residence.csv`
Purpose:
- main municipality-level gross earnings fact source

Expected handling:
- inspect and standardize municipality code and name
- derive quarter from month
- aggregate monthly gross earnings to municipality-quarter

### 3. `annual_avg_monthly_net_earnings_municipality_residence.csv`
Purpose:
- annual municipality-level net earnings validation layer

Expected handling:
- compare annual averages against quarterly/monthly aggregation results
- use for sanity checks and portfolio summary views

### 4. `annual_avg_monthly_gross_earnings_municipality_residence.csv`
Purpose:
- annual municipality-level gross earnings validation layer

Expected handling:
- validate gross earnings rollups and long-form summaries

## Secondary Supporting Datasets Already Present

### National benchmark series
- `avg_monthly_net_earnings_republic.csv`
- `avg_monthly_gross_earnings_republic.csv`
- `annual_avg_monthly_net_earnings_republic.csv`
- `annual_avg_monthly_gross_earnings_republic.csv`

### Activity-based context
- `avg_monthly_gross_earnings_activity_division.csv`
- `ytd_avg_net_earnings_activity_division.csv`
- `ytd_avg_gross_earnings_activity_division.csv`
- `annual_avg_monthly_net_earnings_activity_division.csv`
- `annual_avg_monthly_gross_earnings_activity_division.csv`

### Public-sector context
- `avg_monthly_net_earnings_public_sector.csv`
- `avg_monthly_gross_earnings_public_sector.csv`
- `ytd_avg_net_earnings_public_sector.csv`
- `ytd_avg_gross_earnings_public_sector.csv`
- `annual_avg_monthly_net_earnings_public_sector.csv`
- `annual_avg_monthly_gross_earnings_public_sector.csv`

### Modality and business-status context
- `avg_monthly_net_earnings_employment_modality.csv`
- `avg_monthly_gross_earnings_employment_modality.csv`
- `avg_monthly_net_earnings_business_entity_status.csv`
- `avg_monthly_gross_earnings_business_entity_status.csv`
- `ytd_avg_net_earnings_employment_modality.csv`
- `ytd_avg_gross_earnings_employment_modality.csv`
- `annual_avg_monthly_net_earnings_employment_modality.csv`
- `annual_avg_monthly_gross_earnings_employment_modality.csv`
- `annual_avg_monthly_net_earnings_business_entity_status.csv`
- `annual_avg_monthly_gross_earnings_business_entity_status.csv`

### Distribution and index context
- `median_monthly_net_earnings_republic.csv`
- `median_monthly_gross_earnings_republic.csv`
- `annual_avg_annual_net_earnings_republic.csv`
- `annual_avg_annual_gross_earnings_republic.csv`
- `annual_net_earnings_indices_republic.csv`

## Deferred Datasets
These are still needed for the broader labour-market scope but are not yet in the raw folder.

### Registered employment by sex and municipalities of residence (NSTJ)
Purpose:
- main employment fact source for the full labour-market mart

### Municipalities and cities
Purpose:
- municipality reference dimension

### Territory - NSTJ
Purpose:
- territorial hierarchy and regional context

### Gender
Purpose:
- readable gender labels for employment analysis

## Modeling Direction
Planned outputs after schema inspection:
- `stg_earnings_monthly`
- `stg_earnings_annual`
- `territory_quarter_earnings`
- optional benchmark and context tables from national and activity-level files
- future extension tables for employment and dimensions when those files are added

## Important Note
All table names above are placeholders for planning only. Final names and logic should still be confirmed against the raw files during implementation.
