# data/raw/

Untouched source downloads, one subfolder per organization/source family.

## Rules

- Do not edit, clean, or overwrite files in this folder after download.
- Prefer documenting the source URL in `documentation/source_inventory.md` rather than committing multi-MB files (large formats are gitignored).
- Keep a local copy for reproducibility; if a file is too large for git, record: Source_ID, exact download URL, access date, and file checksum when available.

## Subfolders

| Folder | Source family |
|--------|----------------|
| `tesla_ir/` | Tesla Investor Relations press releases and updates |
| `sec_edgar/` | SEC EDGAR 10-K / 10-Q (and related) filings |
| `nhtsa/` | NHTSA recalls and complaints flat files / API extracts |
| `cec/` | California Energy Commission ZEV / infrastructure stats |
| `doe_afdc/` | DOE Alternative Fuels Data Center station data |
| `usgs/` | USGS Mineral Commodity Summaries and related releases |
