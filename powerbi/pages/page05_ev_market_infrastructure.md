# Page 5 — EV Market & Infrastructure

**Deliverable:** `dashboard/page05_ev_market_infrastructure.html`  
**Facts:** `Fact_EV_Market` (SRC-CEC-001), `Fact_EV_Chargers_CA` (SRC-CEC-002)  
**DAX reference:** `powerbi/dax/Page05_EV_Market_Measures.md`  
**Extract:** `scripts/extract_fact_ev_market.py`

## Purpose

Show Tesla’s California ZEV market position and **public** charging-port availability using CEC downloads — not national Tesla deliveries.

## Layout

1. Focus period + Data as of / geography / source pills  
2. Sales KPIs: Tesla ZEV, Total ZEV, Tesla share, ZEV share of LDV  
3. Public charger KPIs: Public ports total, Public L2, Public DCFC (+ note shared-private is excluded)  
4. Charts: Tesla vs total ZEV, Tesla share, ZEV/LDV share, **public** ports over snapshots  
5. Callouts: CA-only; ports not stations; public vs shared-private; 2025Q2 press revision

## Charger definition (critical)

| Field | Meaning |
|-------|---------|
| Public_* | Publicly available charging **ports** |
| Shared_Private_* | Workplace / multi-family / fleet / other non-public shared ports (not residential) |
| All_Sectors_Ports_Total | Sum of public + shared private (= CEC `Total` column) |

Primary Page 5 infrastructure KPI = `Public_Ports_Total` (aligns with ~public infrastructure narrative). Do not headline `All_Sectors_Ports_Total` as “public chargers.”

## Notes

- ZEV sales Data as of **June 30, 2026**.  
- 2025Q2 total ZEV in export = **101,623** (press 100,671 — later revision).  
- Chargers workbook data-as-of Dec 31, 2025 (`EV_Chargers_Last_updated_04-21-2026_ada.xlsx`).
