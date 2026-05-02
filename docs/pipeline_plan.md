# Pipeline Plan

## Objective
Build a reproducible portfolio project that transforms raw SORS wage data into analytics-ready tables and a final dashboard layer.

The plan now starts from the files already present, instead of assuming the full labour-market input set is available from day one.

## Phases

### 1. Ingest
- place original files into `data/raw`
- keep original filenames or document any renaming
- record file formats and encoding details

### 2. Inspect
- examine schemas, date fields, territory keys, and value formats
- identify how municipality and quarter can be derived consistently from the monthly earnings files
- separate direct monthly series from cumulative January-current-month series
- document unknowns before coding transformation logic

### 3. Stage
- clean source-specific wage data
- standardize types and naming
- standardize municipality-level monthly net and gross files first
- keep transformations traceable and conservative

### 4. Model
- build the municipality-quarter earnings mart first
- aggregate earnings to quarter
- keep net and gross metrics separate
- use annual municipality files as validation layers
- defer employment joins until those datasets are added

### 5. Analyze
- compare net and gross earnings trends by municipality
- identify top/bottom changes over time
- compare quarterly output against annual municipality files
- test regional rollups later if territory reference files are added

### 6. Present
- prepare portfolio-ready charts, narrative takeaways, and a dashboard

## Guardrails
- do not invent schema
- do not guess column names
- do not hard-code join logic until raw keys are confirmed
- do not confuse monthly series with January-current-month cumulative series
- prefer transparent intermediate outputs over over-engineered early abstractions
