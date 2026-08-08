# Page 1 — DAX Measures (Executive Overview)

Cross-page measures reuse Page 2–6 definitions. This file lists the executive card set only.

| Card | Source page / fact | Label |
|------|--------------------|-------|
| Vehicles delivered / produced | Page 2 · `Fact_Tesla_Operations` (Total) | Reported |
| Production–delivery gap | Page 2 | Calculated (not inventory) |
| Energy storage deployed | Page 2 (when present) | Reported |
| Automotive revenue | Page 3 · `Fact_Financials` | Reported |
| Auto gross margin | Page 3 | Calculated |
| Inventory | Page 3 | Reported |
| Inventory days | Page 3 | Estimated |
| Free cash flow | Page 3 | Calculated |
| Tesla share of CA ZEV / CA ZEV sales | Page 5 · `Fact_EV_Market` | Calculated / Reported |
| CA public charging ports | Page 5 · `Fact_EV_Chargers_CA` | Reported (ports; public only) |
| Recall campaigns / POTAFF | Page 4 · `Fact_NHTSA_Annual` | Reported |
| Complaints filed | Page 4 · `Fact_Complaints` annual (FLAT_CMPL) | Reported allegations |
| US lithium import reliance | Page 6 · `Fact_Raw_Materials` | **Estimated** for MCS year 2025 |
| Top lithium producer output | Page 6 | **Estimated** for 2025 |

Citation tooltips must still surface the underlying fact row’s `Source_File` / `Source_ID` / dates.

**Do not** pull complaint counts from the NHTSA vehicle API annual rollup alone — use FLAT_CMPL-backed `Fact_Complaints` / complaints annual embed (SRC-NHTSA-002).
