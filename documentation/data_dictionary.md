# Data Dictionary

Metric labels used across facts:

| Label | Meaning |
|-------|---------|
| reported | Taken directly from the source disclosure or dataset cell |
| calculated | Derived from reported inputs with an explicit formula |
| estimated | Source marks the value as estimated/preliminary, or project derives a proxy and labels it estimated |
| modeled | Reserved for scored/model outputs (not primary in current dashboard KPIs) |

---

## Fact_Tesla_Operations

**Grain:** one row per `Period_ID` × `Vehicle_Group`  
**Primary key:** (`Period_ID`, `Vehicle_Group`)  
**Source family:** SRC-TESLA-IR-001 (SEC 8-K Exhibit 99.1)  
**Processed file:** `data/processed/Fact_Tesla_Operations.csv`  
**Extraction log:** `data/reference/Fact_Tesla_Operations_extraction_log.csv`

| Field | Type | Metric label | Definition | Null policy |
|-------|------|--------------|------------|-------------|
| Period_ID | string | calculated | Quarter key `YYYYQn` | never null |
| Reporting_Period | string | calculated | Inclusive calendar-quarter date range | never null |
| Vehicle_Group | string | reported | As printed: `Model 3/Y`, `Model S/X`, `Other Models`, or `Total` | never null |
| Vehicles_Produced | integer | reported | Vehicles produced in the quarter for the group | null only if missing in source |
| Vehicles_Delivered | integer | reported | Vehicles delivered in the quarter for the group | same |
| Energy_Storage_GWh | decimal | reported or calculated | Energy storage deployed (GWh), `Total` only; MWh→GWh via /1000 is calculated | null when undisclosed; null on non-Total |
| Production_Delivery_Gap | integer | calculated | `Vehicles_Produced − Vehicles_Delivered`. **Not** unsold inventory | null if either input null |
| Delivery_Conversion_Rate | decimal | calculated | `Vehicles_Delivered / Vehicles_Produced` | null if produced 0/null |
| Publication_Date | date | reported | SEC 8-K filing date | never null in current extract |
| Source_File / Source_ID | string | — | Local raw file + inventory key | never null |
| Vehicle_Group_As_Reported | string | reported | Emphasizes no silent remapping | never null |
| Format_Flags / Metric_Notes | string | — | Format tags / short notes | may be empty |

**Incompatible categories:** `Model S/X` (through Q3 2023) vs `Other Models` (from Q4 2023) — see `fact_tesla_operations_format_changes.md`.

---

## Fact_Financials

**Grain:** one row per `Period_ID` (quarter)  
**Source family:** SRC-SEC-10-Q / SRC-SEC-10-K (iXBRL)  
**Processed file:** `data/processed/Fact_Financials.csv`  
**Unit:** USD millions unless noted

| Field | Metric label | Definition |
|-------|--------------|------------|
| Total_Revenue / Automotive_Revenue / Cost_of_Automotive_Revenue | reported (with Q4 carve-out rules) | From 10-Q / 10-K; Q4 often annual − 9-mo YTD where documented |
| Automotive_Gross_Profit / Automotive_Gross_Margin | calculated | Profit = Auto rev − Auto COGS; Margin = Profit / Auto rev |
| Inventory / Accounts_Payable | reported | Balance-sheet line items |
| Operating_Cash_Flow / Capital_Expenditures | reported or calculated | Basis in `CashFlow_Basis` / `OCF_Capex_Metric_Label` (Q1 YTD = quarter; later quarters may be YTD − prior YTD) |
| Free_Cash_Flow | calculated | OCF − CapEx for the quarter basis used |
| Net_Income | reported / calculated per filing basis | As extracted |
| Inventory_Days_Estimate | estimated | Proxy using inventory and automotive COGS / days-in-period |
| Source_File / Source_Accession / Source_URL / Publication_Date | — | EDGAR citation fields |

---

## Fact_Recalls

**Grain:** recall flat-file rows for Tesla make (may be multiple rows per campaign × model/year/component)  
**Source:** NHTSA ODI recall flat file · SRC-NHTSA-001  
**Processed file:** `data/processed/Fact_Recalls.csv`

| Field | Metric label | Definition |
|-------|--------------|------------|
| Campaign_Number | reported | NHTSA campaign id |
| Model / Model_Year / Component | reported | As in flat file |
| Potential_Units_Affected | reported | POTAFF; rollups use max per campaign then sum by year |
| Report_Received_Date / Owner_Notify_Date | reported | Dating fields; annual attribution uses earliest report-received year |
| Summary / Consequence / Remedy | reported | Narrative fields |
| Source_Zip / Source_File / Source_URL | — | Flat-file provenance |

**Units note:** POTAFF is potential exposure, not repairs completed.

---

## Fact_Complaints

**Grain:** one allegation case (distinct `ODI_Number` / ODINO) after component-row collapse rules in extract  
**Source:** NHTSA FLAT_CMPL · SRC-NHTSA-002  
**Processed file:** `data/processed/Fact_Complaints.csv`

| Field | Metric label | Definition |
|-------|--------------|------------|
| ODI_Number | reported | Allegation identifier |
| Model / Model_Year / Component | reported | As filed |
| Crash / Fire / Injured / Deaths | reported | Flags / counts as in flat file |
| Date_Complaint_Filed / Date_Incident | reported | Dating fields |
| Notes | — | States allegations ≠ confirmed defects |

---

## Fact_NHTSA_Annual / Fact_NHTSA_By_Model

**Annual:** calendar year recall campaign counts + summed POTAFF (from recalls flat file).  
**By model:** recall campaign counts (SRC-NHTSA-001) joined to complaint counts (SRC-NHTSA-002).  

Complaint totals for the dashboard come from the complaints annual embed built from `Fact_Complaints`, not from the vehicle API alone.

---

## Fact_EV_Market

**Grain:** one row per quarter (`Period_ID`)  
**Geography:** California  
**Source:** CEC New ZEV Sales + LDV Sales workbooks · SRC-CEC-001  
**Processed file:** `data/processed/Fact_EV_Market.csv`

| Field | Metric label | Definition |
|-------|--------------|------------|
| Tesla_ZEV_Sales_CA / Total_ZEV_Sales_CA | reported | Aggregated from CEC county sheet |
| Tesla_Share_of_ZEV_Sales | calculated | Tesla ÷ Total ZEV |
| Total_LDV_Sales_CA | reported | From LDV workbook statewide |
| ZEV_Share_of_LDV_Sales | calculated | Total ZEV ÷ Total LDV |
| Data_As_Of | reported | CEC export as-of date (prefer over press) |
| Source_File_ZEV / Source_File_LDV + URLs | — | Citation pair |

---

## Fact_EV_Chargers_CA

**Grain:** one row per CEC snapshot sheet (e.g. `Dec 2025`)  
**Unit:** `charging_ports` (not stations)  
**Source:** CEC EV Chargers workbook · SRC-CEC-002  
**Processed file:** `data/processed/Fact_EV_Chargers_CA.csv`

| Field | Metric label | Definition |
|-------|--------------|------------|
| Public_Level_1 / Public_Level_2 / Public_DC_Fast | reported | Public ports by power class |
| Public_Ports_Total | reported (sum of public classes) | **Page 5 / Page 1 primary infrastructure KPI** |
| Shared_Private_* / Shared_Private_Ports_Total | reported | Workplaces / multi-family / fleets — not residential |
| All_Sectors_Ports_Total | reported | CEC `Total` = public + shared-private |
| Notes | — | Documents public vs shared-private vs residential exclusion |

---

## Fact_Raw_Materials

**Grain:** USGS MCS commodity statistic cell (commodity × country × statistic × year)  
**Commodities kept:** Lithium, Cobalt, Nickel, Graphite (Natural)  
**Source:** MCS 2026 commodities CSV · SRC-USGS-002 (DOI 10.5066/P1WKQ63T)  
**Processed file:** `data/processed/Fact_Raw_Materials.csv`  
**Primary dashboard year:** 2025

| Field | Metric label | Definition |
|-------|--------------|------------|
| Value / Value_Numeric | reported or estimated | Numeric when parseable; ranges like `>50` kept as text in Value |
| Metric_Label | derived from Notes | `estimated` if Notes contain “Estimated”; else `reported` |
| Statistics / Statistics_Detail / Section | reported | USGS taxonomy (e.g. World Mine Production) |
| Year | reported | Prefer 2025 for KPIs |
| Source_File / Source_URL / Publication_Date / DOI | — | ScienceBase citation |

**Dashboard KPI note:** Top-producer share of world = top country mine production ÷ world total (**calculated**).

---

## Citation fields (common)

Across facts, tooltips expect some subset of: `Source_ID`, `Source_File`, `Source_URL`, `Publication_Date` / `Data_As_Of` / `Snapshot_Date`, and `Metric_Label`.
