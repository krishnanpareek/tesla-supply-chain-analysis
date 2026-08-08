# Page 6 — Battery Material Risk

**Deliverable:** `dashboard/page06_battery_material_risk.html`  
**Fact:** `Fact_Raw_Materials` (SRC-USGS-002 · MCS 2026 CSV)  
**DAX reference:** `powerbi/dax/Page06_Battery_Material_Measures.md`  
**Extract:** `scripts/extract_fact_raw_materials.py`  
**Embeds:** `scripts/build_dashboard_embeds.py` → `fact_raw_materials_kpi.js`, `fact_raw_materials_production.js`

## Purpose

Show structural battery-material concentration and U.S. import reliance using USGS MCS 2026 — not Tesla supplier volumes.

## Layout

1. Commodity selector + publication / DOI / source pills  
2. KPIs: US NIR, world mine production, top producer, top output, share of world, **explicit 2025 estimated/reported labels**  
3. Charts: top producers (2025), multi-country production trend with per-point labels  
4. Snapshot table across Li / Co / Ni / natural graphite  
5. Callouts: not Tesla-specific; estimated vs reported rule

## Labeling rule (critical)

| Rule | Detail |
|------|--------|
| Source of truth | `Fact_Raw_Materials[Metric_Label]` |
| estimated | USGS `Notes` contain “Estimated” |
| reported | otherwise |
| calculated | Top producer ÷ world mine production |
| Primary year | **2025** |

Do not blanket-label Page 6 production / NIR KPIs as “reported.”
