# data/raw/nhtsa/

Untouched NHTSA Office of Defects Investigation downloads. Large ZIPs are gitignored.

## Recalls flat files (SRC-NHTSA-001) — primary for Fact_Recalls

| Local file | Source_URL | Last-Modified (HTTP) | Access date |
|------------|------------|----------------------|-------------|
| `FLAT_RCL_PRE_2010.zip` | https://static.nhtsa.gov/odi/ffdd/rcl/FLAT_RCL_PRE_2010.zip | 2026-08-07 07:05:12 GMT | 2026-08-07 |
| `FLAT_RCL_POST_2010.zip` | https://static.nhtsa.gov/odi/ffdd/rcl/FLAT_RCL_POST_2010.zip | 2026-08-07 07:05:12 GMT | 2026-08-07 |
| `RCL.txt` | https://static.nhtsa.gov/odi/ffdd/rcl/RCL.txt | 2026-08-07 07:05:12 GMT | 2026-08-07 |
| `Import_Instructions_Recalls.pdf` | https://static.nhtsa.gov/odi/ffdd/rcl/Import_Instructions_Recalls.pdf | 2023-10-27 | 2026-08-07 |

Extract: `python scripts/extract_fact_recalls_flat.py` (filter `MAKETXT=TESLA`).

API extracts under this folder (if present) are secondary / superseded for Fact_Recalls.
