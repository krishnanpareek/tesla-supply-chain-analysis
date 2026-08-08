# Tesla Production, Delivery, Inventory, Quality, and Supply Chain Risk Analysis

Public-data portfolio project analyzing Tesla's production and delivery trends, financial and inventory health, vehicle quality/recalls, EV market position, and battery-material supply risk.

**Audience:** Supply Chain Analyst, Demand Planning Analyst, Inventory Analyst, Procurement Analyst, Operations Analyst, and Business Analyst roles.

**Primary deliverable:** Multi-page HTML dashboard in [`dashboard/`](dashboard/) — not a Power BI `.pbix`. DAX measures are documented under [`powerbi/dax/`](powerbi/dax/) as analytical reference only.

**Data policy:** Only real, verifiable public sources (Tesla Investor Relations, SEC EDGAR, NHTSA, California Energy Commission, USGS). No fabricated values. Every externally sourced number is logged with URL, publication/filing date, and reporting period. Metrics are labeled **reported**, **calculated**, **estimated**, or **modeled**.

## View the dashboard

Open [`dashboard/page01_executive_overview.html`](dashboard/page01_executive_overview.html) in a browser. Sticky nav links all six pages.

| Page | File |
|------|------|
| 1 Executive Overview | `dashboard/page01_executive_overview.html` |
| 2 Production & Delivery | `dashboard/page02_production_delivery_performance.html` |
| 3 Financial & Inventory | `dashboard/page03_financial_inventory_health.html` |
| 4 Quality & Recall Risk | `dashboard/page04_quality_recall_risk.html` |
| 5 EV Market & Infrastructure | `dashboard/page05_ev_market_infrastructure.html` |
| 6 Battery Material Risk | `dashboard/page06_battery_material_risk.html` |

## Fact tables

| Fact | Source | Status |
|------|--------|--------|
| `Fact_Tesla_Operations` | Tesla IR / SEC 8-K EX-99.1 | Complete |
| `Fact_Financials` | SEC 10-Q / 10-K iXBRL | Complete |
| `Fact_Recalls` / `Fact_Complaints` / `Fact_NHTSA_*` | NHTSA vehicle APIs | Complete |
| `Fact_EV_Market` / `Fact_EV_Chargers_CA` | CEC ZEV & charger files | Complete |
| `Fact_Raw_Materials` | USGS MCS 2026 CSV | Complete |

## Structure

```
dashboard/          HTML dashboard (primary deliverable) + design system
data/raw/           Untouched source files (large files gitignored; URLs documented)
data/processed/     Cleaned / transformed fact tables
data/reference/     Download logs and extraction citation logs
sql/schema/         Star-schema DDL
sql/analysis/       Analysis queries
powerbi/dax/        DAX measure reference (documentation only)
powerbi/pages/      Page design specs
documentation/      Source inventory, methodology, limitations
scripts/            Extractors and embed builders
```

## License / disclaimer

This project uses publicly available data for educational and portfolio purposes. It does not claim access to Tesla internal systems, supplier contracts, or confidential factory data.
