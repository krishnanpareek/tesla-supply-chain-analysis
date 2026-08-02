# data/processed/

Cleaned and transformed datasets ready for SQL load and Power BI.

## Rules

- All transformations from `data/raw/` are documented (SQL cleaning scripts and/or methodology notes).
- Never silently interpolate missing values; leave nulls and flag gaps.
- Prefer open formats (CSV, Parquet) with stable column names matching the data dictionary.
