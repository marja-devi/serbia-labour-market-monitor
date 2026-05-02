# Analysis Notes

## Municipality Count Change
The municipality coverage changes across years:
- 2018-2019: `206`
- 2020-2025: `204`

The direct difference identified in the current source files:
- present in 2018-2019 but not later:
  - `80284 Novi Sad`
  - `80519 Petrovaradin`
- present across later years:
  - `89010 Grad Novi Sad`

Interpretation:
- this likely reflects an administrative or reporting-structure change in the SORS source data
- comparisons involving the Novi Sad area across the full 2018-2025 period should be treated carefully

## Practical Modeling Rule
For now:
- keep the source municipality codes as-is
- do not manually merge these municipality identities yet
- mention this continuity issue clearly in portfolio analysis

Later, when official territory or municipality reference tables are added, we can design a proper harmonization rule.
