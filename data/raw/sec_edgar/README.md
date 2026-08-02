# data/raw/sec_edgar/

Untouched Tesla SEC primary filings (Forms **10-Q** and **10-K**) covering reporting periods from **2022-03-31 through 2026-06-30**.

## What is stored here

Primary HTML documents (`tsla-YYYYMMDD.htm`) downloaded from EDGAR Archives.

Naming pattern:

`<FORM>_<PERIOD>_<REPORT_DATE>_<original_sec_filename>.htm`

## Git note

These files are multi-MB and are **gitignored**. Re-download using the URLs in `data/reference/download_log.md` if cloning a fresh copy of the repo.

Do not edit these files. Cleaning belongs in `data/processed/` / `sql/cleaning/`.
