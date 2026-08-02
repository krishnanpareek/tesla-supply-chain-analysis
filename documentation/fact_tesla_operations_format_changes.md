# Fact_Tesla_Operations — Release Format Changes

Do **not** silently merge incompatible vehicle-group categories across periods.

## Vehicle group taxonomy break

| Periods | As-reported groups | Notes |
|---------|--------------------|-------|
| Q1 2022 – Q3 2023 | `Model S/X`, `Model 3/Y`, `Total` | Non-3/Y vehicles labeled **Model S/X** |
| Q4 2023 – Q2 2026 | `Model 3/Y`, `Other Models`, `Total` | Non-3/Y vehicles labeled **Other Models** (may include Cybertruck and other non-3/Y products; source does not itemize) |

**Implication:** `Model S/X` and `Other Models` are **not treated as identical series** in analysis without an explicit, documented mapping assumption. Trend charts by vehicle group should either (a) keep labels separate, or (b) show a clear break annotation at Q4 2023.

## Energy storage disclosure

| Periods | Disclosure | Handling |
|---------|------------|----------|
| Q1 2022 – Q4 2023 | Not in these production releases | `Energy_Storage_GWh` = null on all rows |
| Q1 2024 | Reported in **MWh** (4,053 MWh) | Stored as **calculated** GWh = MWh/1000 on Total row only |
| Q2 2024 – Q2 2026 | Reported in **GWh** | Stored as **reported** GWh on Total row only |

## Release title / packaging

- Earlier: “Vehicle Production & Deliveries and Date for Financial Results & Webcast …”
- Later (from ~Q3 2024): “Production, Deliveries & Deployments”

## Per-quarter flags

| Period_ID | Publication_Date | Format_Flags | Validation |
|-----------|------------------|--------------|------------|
| 2022Q1 | 2022-04-04 | `vehicle_group_label=Model_S_X;release_title=Vehicle_Production_Deliveries;energy_storage=not_disclosed_in_release` | Validation OK: segment sums equal Total row |
| 2022Q2 | 2022-07-05 | `vehicle_group_label=Model_S_X;release_title=Vehicle_Production_Deliveries;energy_storage=not_disclosed_in_release` | Validation OK: segment sums equal Total row |
| 2022Q3 | 2022-10-03 | `vehicle_group_label=Model_S_X;release_title=Vehicle_Production_Deliveries;energy_storage=not_disclosed_in_release` | Validation OK: segment sums equal Total row |
| 2022Q4 | 2023-01-03 | `vehicle_group_label=Model_S_X;release_title=Vehicle_Production_Deliveries;energy_storage=not_disclosed_in_release` | Validation OK: segment sums equal Total row |
| 2023Q1 | 2023-04-03 | `vehicle_group_label=Model_S_X;release_title=Vehicle_Production_Deliveries;energy_storage=not_disclosed_in_release` | Validation OK: segment sums equal Total row |
| 2023Q2 | 2023-07-03 | `vehicle_group_label=Model_S_X;release_title=Vehicle_Production_Deliveries;energy_storage=not_disclosed_in_release` | Validation OK: segment sums equal Total row |
| 2023Q3 | 2023-10-02 | `vehicle_group_label=Model_S_X;release_title=Vehicle_Production_Deliveries;energy_storage=not_disclosed_in_release` | Validation OK: segment sums equal Total row |
| 2023Q4 | 2024-01-02 | `vehicle_group_label=Other_Models;release_title=Vehicle_Production_Deliveries;energy_storage=not_disclosed_in_release` | Validation OK: segment sums equal Total row |
| 2024Q1 | 2024-04-02 | `vehicle_group_label=Other_Models;release_title=Vehicle_Production_Deliveries;energy_unit=MWh` | Validation OK: segment sums equal Total row |
| 2024Q2 | 2024-07-02 | `vehicle_group_label=Other_Models;release_title=Vehicle_Production_Deliveries;energy_unit=GWh` | Validation OK: segment sums equal Total row |
| 2024Q3 | 2024-10-02 | `vehicle_group_label=Other_Models;release_title=Production_Deliveries_Deployments;energy_unit=GWh` | Validation OK: segment sums equal Total row |
| 2024Q4 | 2025-01-02 | `vehicle_group_label=Other_Models;release_title=Production_Deliveries_Deployments;energy_unit=GWh` | Validation OK: segment sums equal Total row |
| 2025Q1 | 2025-04-02 | `vehicle_group_label=Other_Models;release_title=Production_Deliveries_Deployments;energy_unit=GWh` | Validation OK: segment sums equal Total row |
| 2025Q2 | 2025-07-02 | `vehicle_group_label=Other_Models;release_title=Production_Deliveries_Deployments;energy_unit=GWh` | Validation OK: segment sums equal Total row |
| 2025Q3 | 2025-10-02 | `vehicle_group_label=Other_Models;release_title=Production_Deliveries_Deployments;energy_unit=GWh` | Validation OK: segment sums equal Total row |
| 2025Q4 | 2026-01-02 | `vehicle_group_label=Other_Models;release_title=Production_Deliveries_Deployments;energy_unit=GWh` | Validation OK: segment sums equal Total row |
| 2026Q1 | 2026-04-02 | `vehicle_group_label=Other_Models;release_title=Production_Deliveries_Deployments;energy_unit=GWh` | Validation OK: segment sums equal Total row |
| 2026Q2 | 2026-07-02 | `vehicle_group_label=Other_Models;release_title=Production_Deliveries_Deployments;energy_unit=GWh` | Validation OK: segment sums equal Total row |
