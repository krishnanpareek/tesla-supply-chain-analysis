# data/processed/

Cleaned and transformed datasets ready for SQL load and Power BI.

## Current files

| File | Description |
|------|-------------|
| `Fact_Tesla_Operations.csv` | Quarterly production/delivery fact (Period × Vehicle_Group) |

## Rules

- All transformations from `data/raw/` are documented (SQL cleaning scripts and/or extractor scripts).
- Never silently interpolate missing values; leave nulls and flag gaps.
- Traceability for Fact_Tesla_Operations: `data/reference/Fact_Tesla_Operations_extraction_log.csv`.
