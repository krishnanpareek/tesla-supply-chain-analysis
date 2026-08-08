# Methodology

## Source → fact → dashboard

1. **Inventory** each public source in `source_inventory.md` (URL, publication/filing date, reporting period, reliability notes).
2. **Download** raw files to `data/raw/` (large files may be gitignored; URLs remain authoritative).
3. **Extract** with Python scripts under `scripts/` into `data/processed/Fact_*.csv`, writing citation rows to `data/reference/*_extraction_log.csv` where applicable.
4. **Embed** selected facts as `dashboard/data/*.js` via `scripts/build_dashboard_embeds.py`.
5. **Present** in HTML pages under `dashboard/` with hover citations.

## Metric labeling

| Label | Rule |
|-------|------|
| reported | Copied from source cell / disclosure |
| calculated | Explicit formula from reported inputs (e.g., share, gap, FCF, margin) |
| estimated | USGS Notes contain “Estimated”, or project proxy (e.g., inventory days) |
| modeled | Reserved; not used as primary KPI label on current pages |

## Period alignment

- Operations & financials: calendar quarters (`Period_ID` = `YYYYQn`).
- NHTSA annual: calendar year of earliest `Report_Received_Date` (recalls) or complaint filed year.
- CEC chargers: snapshot labels from workbook sheets (e.g., `Dec 2025`).
- USGS: prefer year **2025** (newest MCS 2026 year) for Page 6 / Page 1 mineral KPIs.

## Definition standards (non-negotiable)

- Production–delivery gap = produced − delivered; **never** labeled unsold inventory.
- CA ZEV metrics stay California-scoped.
- Charger KPIs use **public ports**; retain all-sectors total only as context.
- Complaints = allegations from FLAT_CMPL; flat files override API zeros for coverage checks.
- Mineral KPIs carry USGS estimated/reported labels at cell level.

## Correlation language

Insights and interview narratives use qualified wording (“consistent with,” “may reflect,” “structural signal”). Public time series alone do not establish root cause.
