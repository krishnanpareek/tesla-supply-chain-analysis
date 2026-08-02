# Data Dictionary

## Fact_Tesla_Operations

**Grain:** one row per `Period_ID` × `Vehicle_Group`  
**Primary key:** (`Period_ID`, `Vehicle_Group`)  
**Source family:** SRC-TESLA-IR-001 (SEC 8-K Exhibit 99.1)  
**Processed file:** `data/processed/Fact_Tesla_Operations.csv`  
**Extraction log:** `data/reference/Fact_Tesla_Operations_extraction_log.csv`

| Field | Type | Metric label | Definition | Null policy |
|-------|------|--------------|------------|-------------|
| Period_ID | string | calculated | Quarter key `YYYYQn` derived from reporting period | never null |
| Reporting_Period | string | calculated | Inclusive calendar-quarter date range | never null |
| Vehicle_Group | string | reported | As printed in source table: `Model 3/Y`, `Model S/X`, `Other Models`, or `Total` | never null |
| Vehicles_Produced | integer | reported | Vehicles produced in the quarter for the group | null only if missing in source (none in current window) |
| Vehicles_Delivered | integer | reported | Vehicles delivered in the quarter for the group | same |
| Energy_Storage_GWh | decimal | reported or calculated | Energy storage deployed (GWh). On `Total` only. MWh disclosures converted by /1000 (calculated). | null when release does not disclose; null on non-Total rows |
| Production_Delivery_Gap | integer | calculated | `Vehicles_Produced - Vehicles_Delivered`. **Not** unsold inventory. | null if either input null |
| Delivery_Conversion_Rate | decimal | calculated | `Vehicles_Delivered / Vehicles_Produced` | null if produced is 0/null |
| Publication_Date | date | reported | SEC 8-K filing date for the release | never null in current extract |
| Source_File | string | — | Local raw filename | never null |
| Source_ID | string | — | Inventory key, e.g. `SRC-TESLA-IR-001-Q1_2022` | never null |
| Vehicle_Group_As_Reported | string | reported | Same as Vehicle_Group; retained to emphasize no silent remapping | never null |
| Format_Flags | string | — | Pipe-delimited format tags for the release | may be empty |
| Metric_Notes | string | — | Short label summary for the row | may be empty |

### Incompatible categories (do not merge silently)

- `Model S/X` (Q1 2022–Q3 2023) vs `Other Models` (Q4 2023–Q2 2026): see `documentation/fact_tesla_operations_format_changes.md`.
