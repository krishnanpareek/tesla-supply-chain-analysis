# Page 2 — Production & Delivery Performance

## Business objective

Show how Tesla’s reported vehicle production and deliveries moved from **Q1 2022 through Q2 2026**, quantify the **production–delivery gap** (without calling it unsold inventory), surface growth and rolling trends, and make every figure traceable to its IR source file.

**Primary audience:** Supply Chain / Demand Planning / Operations interview demos.

**Dataset:** `Fact_Tesla_Operations` (`data/processed/Fact_Tesla_Operations.csv`)

---

## Page layout (top → bottom)

1. **Header** — page title + last-selected period citation strip  
2. **KPI cards** (5)  
3. **Trend row** — Production vs Deliveries (Total) | Gap over time  
4. **Analysis row** — Delivery mix by vehicle group (with Q4 2023 break) | QoQ / YoY growth + 4Q rolling average  
5. **Detail table** — selected period breakdown with source file column  
6. **Footer callout** — gap interpretation + format-change note  

---

## KPI cards

| Card | Measure | Metric label | Default filter | Conditional formatting |
|------|---------|--------------|----------------|------------------------|
| Vehicles Produced | `[Vehicles Produced]` | Reported | Latest `Period_ID`, `Vehicle_Group = Total` | Neutral |
| Vehicles Delivered | `[Vehicles Delivered]` | Reported | Latest Total | Neutral |
| Production–Delivery Gap | `[Production Delivery Gap]` | Calculated | Latest Total | Blue if &gt;0 (prod ahead); amber if &lt;0 (deliveries ahead) — **not** red/green “good/bad” |
| Delivery Conversion Rate | `[Delivery Conversion Rate]` | Calculated | Latest Total | % format |
| Deliveries YoY Growth | `[Deliveries YoY Growth (by Period Sort)]` | Calculated | Latest Total | % format; blank if &lt;5 quarters history |

**Card tooltip fields (all required):** value, metric label, Reporting_Period, Publication_Date, Source_File, Source_ID, gap disclaimer when gap card is shown.

---

## Visuals

### 1) Production vs Deliveries — line chart
- **X:** `Period_ID` (sorted by `Period Sort`)  
- **Y:** `[Vehicles Produced]`, `[Vehicles Delivered]`  
- **Filter:** `Vehicle_Group = Total`  
- **Tooltip:** both series + citation fields  
- **Annotation:** optional constant line / text box at `2023Q4` — “Vehicle group taxonomy changes to Other Models (segment charts only)”

### 2) Production–Delivery Gap — column chart
- **X:** `Period_ID`  
- **Y:** `[Production Delivery Gap]`  
- **Filter:** Total  
- **Title must say** “Production–Delivery Gap (Calculated)” — never “Inventory”  
- **Tooltip:** Gap Direction + citation fields + disclaimer

### 3) Delivery mix — 100% stacked column or clustered bar
- **X:** `Period_ID`  
- **Legend:** `Vehicle_Group`  
- **Filter:** `Vehicle_Group <> Total`  
- **Hard rule:** show a **visual break / annotation at 2023Q4**; do not imply Model S/X ≡ Other Models  
- **Tooltip:** mix share (calculated) + produced/delivered (reported) + citation

### 4) Growth & rolling average — line + column combo
- Columns: `[Deliveries QoQ Growth (by Period Sort)]`  
- Line: `[Deliveries 4Q Rolling Avg]` (secondary axis) or separate small multiples  
- Filter: Total  
- Tooltip: citation for the period’s delivered base figure

### 5) Detail matrix / table
Columns: Period_ID, Vehicle_Group, Vehicles_Produced, Vehicles_Delivered, Production_Delivery_Gap, Delivery_Conversion_Rate, Energy_Storage_GWh, Publication_Date, Source_File  
Interactive with slicers.

---

## Filters / slicers

| Slicer | Field | Notes |
|--------|-------|-------|
| Period | `Period_ID` | Multi-select; default all or last 8 quarters |
| Vehicle group | `Vehicle_Group` | Include Total + segments |
| Taxonomy era | calculated group or Format_Flags contains | Optional: “Model S/X era” vs “Other Models era” |

---

## Drill-through

- **From:** any Total KPI or trend point  
- **To page (future):** period detail — keep fields Period_ID, Source_File, Reporting_Period  
- **Keep:** citation columns on drill-through target

---

## Conditional formatting

- Gap chart: diverging from zero (prod-ahead vs delivery-ahead), not RAG traffic lights  
- Conversion rate &lt; 0.95 or &gt; 1.05: subtle highlight (timing/mix signal, not “bad performance”)  
- Missing `Energy_Storage_GWh`: show “—” not zero

---

## Executive interpretation (page footnote)

> Tesla’s reported production and deliveries do not move in lockstep. Positive gaps (production &gt; deliveries) and negative gaps (deliveries &gt; production) both appear in the public series. The data indicates timing and logistics effects can dominate a single quarter (e.g., vehicles in transit); additional internal data would be required to attribute any quarter to demand, factory shutdowns, or mix. Vehicle-group labels change at Q4 2023 (`Model S/X` → `Other Models`) and must not be treated as one continuous segment without disclosure.

---

## Build checklist (Power BI Desktop)

1. Get Data → `data/processed/Fact_Tesla_Operations.csv`  
2. Set data types; mark `Period_ID` sort by `Period Sort` column (create in DAX or Power Query)  
3. Paste measures from `powerbi/dax/Page02_Production_Delivery_Measures.md`  
4. Build visuals above; attach report-page tooltip with citation fields  
5. Export page PNG to `visuals/page02_production_delivery_performance.png`  

## Demo without Desktop

Open `powerbi/page02_production_delivery_performance.html` in a browser (embedded fact data + citation tooltips).
