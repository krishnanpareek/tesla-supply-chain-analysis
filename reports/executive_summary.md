# Executive Summary

**Project:** Tesla Production, Delivery, Inventory, Quality, and Supply Chain Risk Analysis  
**Deliverable:** Six-page HTML / CSS / JavaScript dashboard (`dashboard/`)  
**Data:** Public sources only (Tesla IR / SEC, NHTSA ODI flat files, CEC, USGS)  
**Audience:** Supply chain, demand planning, inventory, procurement, operations, and business analyst roles

## Problem

Tesla’s public disclosures span operations updates, SEC filings, safety databases, state EV sales statistics, and mineral commodity summaries. Recruiters and analysts need a **traceable** view that connects these signals without inventing internal factory, supplier, or SKU-level data — and without mislabeling timing gaps as inventory or allegations as confirmed defects.

## Approach

1. Inventory public sources with URL, publication/filing date, and reporting period (`documentation/source_inventory.md`).
2. Extract star-schema fact tables into `data/processed/` with field-level **reported / calculated / estimated** labels.
3. Build a browser-native dashboard that surfaces the same facts with hover citations (`Source_File`, `Source_ID`, dates).
4. Document definitional edge cases that fail interviews if handled carelessly (gap ≠ inventory; public ports ≠ all CEC ports; USGS 2025 often estimated; NHTSA API under-counts vs flat files).

## Dashboard pages

| Page | Business question | Primary facts |
|------|-------------------|---------------|
| 1 Executive Overview | What changed recently across ops, finance, quality, CA market, and materials? | Aggregates Pages 2–6 |
| 2 Production & Delivery | How do production and deliveries move by quarter? | `Fact_Tesla_Operations` |
| 3 Financial & Inventory | How do auto revenue, margin, inventory $, and FCF move? | `Fact_Financials` |
| 4 Quality & Recall Risk | What do NHTSA recalls and complaints show over time? | `Fact_Recalls`, `Fact_Complaints` |
| 5 EV Market & Infrastructure | What is Tesla’s CA ZEV share and public charging availability? | `Fact_EV_Market`, `Fact_EV_Chargers_CA` |
| 6 Battery Material Risk | Where is mine production concentrated, and how import-reliant is the U.S.? | `Fact_Raw_Materials` |

## Selected latest snapshots (illustrative — see dashboard for citations)

Figures below are the latest periods loaded in the processed facts used by the dashboard; always verify on the page tooltip.

- **2026Q2 operations (Total):** ~480k delivered, ~452k produced, gap ≈ −28k (calculated; not inventory); energy storage ~13.5 GWh reported.
- **2026Q2 financials:** Automotive revenue ~$20.5B; auto gross margin ~17% (calculated); inventory ~$13.8B reported; FCF calculated from OCF − CapEx.
- **2026 quality YTD (flat files):** Recall campaigns and POTAFF from SRC-NHTSA-001; complaint counts from SRC-NHTSA-002 (allegations).
- **2026Q2 California ZEV:** Tesla ≈ 52% of CA ZEV sales (calculated from CEC reported counts); geography is California only.
- **Dec 2025 CA chargers:** ~183k **public** charging ports (reported ports); CEC workbook total also includes shared-private and is not the public-availability KPI.
- **USGS MCS 2026 / year 2025:** Lithium world mine production 290kt and Australia 92kt are **estimated**; U.S. lithium net import reliance published as >50% (**estimated**).

## Skills demonstrated (accurate framing)

- Public-source research and source inventory discipline  
- Python extraction / cleaning into analysis-ready fact tables  
- Metric labeling (reported vs calculated vs estimated)  
- HTML / CSS / JavaScript dashboarding with citation UX  
- Definitional rigor on inventory, quality, infrastructure, and mineral statistics  
- Documentation: data dictionary, limitations, methodology notes  

**Not claimed for this project:** Power BI Desktop model authoring, DAX measure deployment in a `.pbix`, or Tesla-confidential data access. DAX-style notes in-repo are documentation of KPI logic only.

## Limitations (summary)

Public data cannot identify Tesla’s suppliers, cell chemistry mix, SKU inventory, or plant-level constraints. California ZEV sales are not national deliveries. NHTSA complaints are allegations. USGS 2025 mineral figures are often preliminary estimates. Full list: [`documentation/limitations.md`](../documentation/limitations.md).

## How to review

1. Open `dashboard/page01_executive_overview.html`.  
2. Hover KPIs for source citations.  
3. Drill to Pages 2–6 for charts and filters.  
4. Cross-check disputed numbers against `documentation/source_inventory.md` and raw files under `data/raw/` (where retained).
