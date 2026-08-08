# Tesla Production, Delivery, Inventory, Quality, and Supply Chain Risk Analysis

Public-data portfolio project analyzing Tesla’s production and delivery trends, financial and inventory health, vehicle quality/recalls, California EV market position, and battery-material supply concentration.

**Audience:** Supply Chain Analyst, Demand Planning Analyst, Inventory Analyst, Procurement Analyst, Operations Analyst, and Business Analyst roles.

**Primary deliverable:** A six-page interactive **HTML / CSS / JavaScript** dashboard in [`dashboard/`](dashboard/). Open any page in a browser — no BI desktop app required.

**What this is not:** Not a Power BI `.pbix`, not a live Tesla-internal dashboard, and not a claim of access to Tesla factories, supplier contracts, or confidential inventory systems. Analytical measure notes under [`powerbi/dax/`](powerbi/dax/) document KPI logic for portfolio reviewers; they are **not** an executed Power BI model in this repository.

**Data policy:** Only verifiable public sources (Tesla Investor Relations / SEC EDGAR, NHTSA ODI flat files, California Energy Commission, USGS Mineral Commodity Summaries). No fabricated values. Metrics are labeled **reported**, **calculated**, **estimated**, or **modeled**. Hover any KPI for `Source_File` / `Source_ID` / publication date.

## View the dashboard

Start here: [`dashboard/page01_executive_overview.html`](dashboard/page01_executive_overview.html)

| Page | File | Focus |
|------|------|--------|
| 1 Executive Overview | [`page01_…`](dashboard/page01_executive_overview.html) | Cross-page KPI snapshot |
| 2 Production & Delivery | [`page02_…`](dashboard/page02_production_delivery_performance.html) | IR production, deliveries, gap |
| 3 Financial & Inventory | [`page03_…`](dashboard/page03_financial_inventory_health.html) | SEC revenue, margin, inventory, FCF |
| 4 Quality & Recall Risk | [`page04_…`](dashboard/page04_quality_recall_risk.html) | NHTSA recalls & complaints |
| 5 EV Market & Infrastructure | [`page05_…`](dashboard/page05_ev_market_infrastructure.html) | CEC CA ZEV sales & **public** charging ports |
| 6 Battery Material Risk | [`page06_…`](dashboard/page06_battery_material_risk.html) | USGS Li / Co / Ni / graphite |

## What the analysis shows (high level)

- **Operations:** Quarterly production vs deliveries (Total group), with production–delivery gap defined as produced − delivered — **not** labeled as unsold inventory.
- **Financial / inventory:** Automotive revenue, gross margin, balance-sheet inventory, estimated inventory days, and free cash flow from SEC 10-Q / 10-K.
- **Quality:** Recall campaigns and potential units affected from NHTSA recall flat files; complaint counts from FLAT_CMPL (allegations, not confirmed defects).
- **CA market:** Tesla share of California ZEV sales (registration-based CEC data — not national deliveries) and **public** charging-port counts (ports, not stations; public only, not shared-private or residential).
- **Materials:** USGS 2025 mine production and U.S. net import reliance for battery minerals, with **estimated** vs **reported** labels taken from USGS notes.

See [`reports/executive_summary.md`](reports/executive_summary.md) for a recruiter-facing write-up and [`documentation/limitations.md`](documentation/limitations.md) for explicit scope limits.

## Fact tables

| Fact | Source | Status |
|------|--------|--------|
| `Fact_Tesla_Operations` | Tesla IR / SEC 8-K EX-99.1 | Complete |
| `Fact_Financials` | SEC 10-Q / 10-K iXBRL | Complete |
| `Fact_Recalls` / `Fact_Complaints` / `Fact_NHTSA_*` | NHTSA ODI flat files (primary) | Complete |
| `Fact_EV_Market` / `Fact_EV_Chargers_CA` | CEC ZEV & charger workbooks | Complete |
| `Fact_Raw_Materials` | USGS MCS 2026 commodities CSV | Complete |

Field definitions: [`documentation/data_dictionary.md`](documentation/data_dictionary.md)  
Source traceability: [`documentation/source_inventory.md`](documentation/source_inventory.md)

## Repository structure

```
dashboard/          HTML dashboard (primary deliverable) + design system
data/raw/           Untouched source files (large files gitignored; URLs documented)
data/processed/     Cleaned fact tables (CSV)
data/reference/     Download logs and extraction citation logs
scripts/            Python extractors and dashboard embed builders
sql/schema/         Star-schema DDL (analytical model documentation)
sql/analysis/       Analysis queries
powerbi/dax/        KPI measure notes (documentation only — not a .pbix)
powerbi/pages/      Page design specs
documentation/      Source inventory, data dictionary, methodology, limitations
reports/            Executive summary and portfolio talking points
```

## How to regenerate embeds

```bash
python scripts/extract_fact_ev_market.py
python scripts/extract_fact_raw_materials.py
python scripts/build_dashboard_embeds.py
```

Other fact extractors live under `scripts/` and are documented in `documentation/`.

## Portfolio materials

| File | Purpose |
|------|---------|
| [`reports/executive_summary.md`](reports/executive_summary.md) | One-page project summary |
| [`reports/portfolio_materials.md`](reports/portfolio_materials.md) | Resume bullets, LinkedIn post, 2-minute interview script |
| [`documentation/data_dictionary.md`](documentation/data_dictionary.md) | Field definitions and metric labels |
| [`documentation/limitations.md`](documentation/limitations.md) | What public data cannot answer |

## License / disclaimer

Public data for educational and portfolio purposes only. This project does **not** claim access to Tesla internal systems, supplier contracts, confidential factory data, or non-public inventory. Independent verification of headline figures against primary sources is encouraged.
