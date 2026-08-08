# Dashboard (primary deliverable)

Interactive six-page HTML dashboard for the Tesla supply-chain portfolio project.

**Design system:** IBM Plex Sans / IBM Plex Mono / Newsreader; dark teal–blue palette (`assets/dashboard.css`).

**Citation standard:** Every displayed number traces to a processed fact row (`Source_File`, `Source_ID`, `Source_URL` / publication date) via hover tooltips.

## Pages

| Page | File | Status |
|------|------|--------|
| 1 Executive Overview | `page01_executive_overview.html` | In review |
| 2 Production & Delivery | `page02_production_delivery_performance.html` | Live |
| 3 Financial & Inventory | `page03_financial_inventory_health.html` | Live |
| 4 Quality & Recall Risk | `page04_quality_recall_risk.html` | Live |
| 5 EV Market & Infrastructure | `page05_ev_market_infrastructure.html` | Live |
| 6 Battery Material Risk | `page06_battery_material_risk.html` | Live |

## How to view

Open any live page in a browser. Sticky nav links all six pages.

## Regenerate embeds

```bash
python scripts/extract_fact_ev_market.py
python scripts/extract_fact_raw_materials.py
python scripts/build_dashboard_embeds.py
```

## DAX reference

Analytical measure logic (not executed) lives under `../powerbi/dax/`.
