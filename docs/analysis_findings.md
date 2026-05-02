# Earnings Mart Findings

Analysis date: 2026-04-28

## Scope
These findings use the municipality-quarter earnings mart built from the four core municipality earnings files.

## Portfolio-Ready Findings

### 1. Municipality ranking: the highest-paying local units in 2025 are concentrated in Belgrade
Top 2025 net municipality ranking:
- Stari grad: 187799.09 RSD
- Vračar: 181668.0 RSD
- Novi Beograd: 174887.08 RSD
- Savski venac: 174393.34 RSD
- Voždovac: 142552.08 RSD

Top 2025 gross municipality ranking:
- Stari grad: 255513.83 RSD
- Vračar: 247682.58 RSD
- Novi Beograd: 239526.67 RSD
- Savski venac: 237108.84 RSD
- Voždovac: 196543.25 RSD

### 2. Municipality ranking: the lowest-paying local units in 2025 form a distinct lower tier
Bottom 2025 net municipality ranking:
- Preševo: 73897.67 RSD
- Bojnik: 75009.75 RSD
- Vlasotince: 76484.08 RSD
- Vranjska Banja: 77137.25 RSD
- Lebane: 78426.0 RSD

Bottom 2025 gross municipality ranking:
- Preševo: 102237.25 RSD
- Bojnik: 103278.58 RSD
- Vlasotince: 105433.75 RSD
- Vranjska Banja: 106333.92 RSD
- Lebane: 108228.67 RSD

### 3. Some municipalities show very strong earnings growth from 2018 to 2025
Top net growth 2018-2025:
- Savski venac: 159.84% (67111.0 -> 174381.0 RSD)
- Stari grad: 152.63% (74332.0 -> 187785.0 RSD)
- Svrljig: 148.03% (32152.0 -> 79747.0 RSD)
- Vranjska Banja: 140.21% (32135.0 -> 77192.0 RSD)
- Bor: 138.47% (53023.0 -> 126444.0 RSD)

Top gross growth 2018-2025:
- Savski venac: 155.33% (92859.0 -> 237093.0 RSD)
- Stari grad: 148.55% (102793.0 -> 255495.0 RSD)
- Svrljig: 147.61% (44181.0 -> 109396.0 RSD)
- Vranjska Banja: 140.01% (44334.0 -> 106405.0 RSD)
- Bor: 138.88% (73589.0 -> 175793.0 RSD)

### 4. Quarter-over-quarter outliers exist and should be treated as analysis signals, not automatic conclusions
Largest quarter-over-quarter changes:
- Titel net 2019 Q3 -> 2019 Q4: 21.4%
- Titel gross 2019 Q3 -> 2019 Q4: 20.02%
- Doljevac gross 2020 Q3 -> 2020 Q4: 19.8%
- Doljevac net 2020 Q3 -> 2020 Q4: 19.55%
- Titel net 2020 Q1 -> 2020 Q2: -19.47%
- Titel gross 2020 Q1 -> 2020 Q2: -18.65%
- Lučani gross 2024 Q3 -> 2024 Q4: 18.62%
- Žitorađa gross 2020 Q3 -> 2020 Q4: 18.59%
- Žitorađa net 2020 Q3 -> 2020 Q4: 18.53%
- Lučani gross 2023 Q3 -> 2023 Q4: 18.36%

### 5. Net and gross earnings should be read together because the gap changes over time
- 2018: net 49650.0 RSD, gross 68629.0 RSD, gap 18979.0 RSD
- 2025: net 109462.0 RSD, gross 151086.0 RSD, gap 41624.0 RSD
- net-to-gross ratio moved from 72.35% to 72.45%

### 6. Belgrade and Novi Sad can be compared on one net-gross timeline, but with different aggregation logic
- Grad Beograd 2025: net 123940.0 RSD, gross 171190.0 RSD, gap 47250.0 RSD
- Grad Novi Sad 2025: net 126469.0 RSD, gross 174469.0 RSD, gap 48000.0 RSD
- Belgrade is shown as the median across city municipalities because the raw data do not contain one aggregate Belgrade row.
- Novi Sad is shown from the official city row `89010 Grad Novi Sad`.

### 7. The same mart can now be read at macro-region, district, and city drill-down level
Group median of municipality averages: 2025 net earnings by macro region:
- SRBIJA – SEVER: 93173.25 RSD
- SRBIJA – JUG: 86425.75 RSD

Group median of municipality averages: top districts by 2025 net earnings:
- Beogradski region: 123943.83 RSD
- Borska oblast: 104041.67 RSD
- Sremska oblast: 97131.92 RSD
- Moravička oblast: 95928.88 RSD
- Kolubarska oblast: 93862.08 RSD

City drill-down municipality ranking: top 2025 net local units:
- Grad Beograd / Stari grad: 187799.09 RSD
- Grad Beograd / Vračar: 181668.0 RSD
- Grad Beograd / Novi Beograd: 174887.08 RSD
- Grad Beograd / Savski venac: 174393.34 RSD
- Grad Beograd / Voždovac: 142552.08 RSD

## Interpretation Notes
- `2026` is partial and should not be used for full-year comparisons.
- 2018-2019 include separate rows for `Novi Sad` and `Petrovaradin`, while later years use `Grad Novi Sad`, so long-run comparisons around that area need special care.
- Annual validation differences are small enough that the mart is suitable for portfolio storytelling.
- Group median views use the median of municipality averages, not a weighted regional mean, because the current source files do not include employment weights.
- Belgrade vs Novi Sad is aligned to one construction: median across available city-group members for both cities.
- For Novi Sad, the current city group contains a single city-level row, so its median equals that row.

## Suggested First Charts
- Municipality ranking: top 10 local units by 2025 net earnings
- Municipality ranking: bottom 10 local units by 2025 net earnings
- Net and gross together on one line chart for Republic, Belgrade, or Novi Sad
- Group median of municipality averages by macro region or district
- 2018 vs 2025 growth comparison for selected municipalities
- Quarter-over-quarter volatility spotlight for a few outlier municipalities
