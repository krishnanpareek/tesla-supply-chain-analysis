# Fact_Financials notes

## Units
All monetary fields are in **USD millions**, matching Tesla’s iXBRL `scale="6"` presentation.

## Period grain
One row per calendar quarter `YYYYQn` for Q1 2022–Q2 2026.

## Pipeline
1. `scripts/extract_fact_financials.py` — parse iXBRL facts from local `data/raw/sec_edgar/` 10-Q/10-K HTML  
2. `scripts/enrich_fact_financials.py` — add Source_ID/URL/Publication_Date from `download_log.md`, plus calculated KPIs  
3. `scripts/build_dashboard_embeds.py` — write `dashboard/data/fact_financials.js`

## Reported vs calculated
- **Reported:** line items from 10-Q three-month columns or balance-sheet period-end; Q1 OCF/CapEx (YTD = quarter).
- **Calculated:**
  - Q2/Q3 `Operating_Cash_Flow` and `Capital_Expenditures` = current YTD − prior quarter YTD
  - Q4 P&L and cash-flow fields = fiscal-year 10-K total − nine-month YTD from Q3 10-Q
  - `Automotive_Gross_Profit` = Automotive_Revenue − Cost_of_Automotive_Revenue
  - `Automotive_Gross_Margin` = GP / Automotive_Revenue
  - `Free_Cash_Flow` = Operating_Cash_Flow − Capital_Expenditures  
    (CapEx stored as **positive outflow magnitude**)
- **Estimated:**
  - `Inventory_Days_Estimate` = Inventory ÷ (Cost_of_Automotive_Revenue ÷ Days_In_Period)

## Automotive taxonomy fallbacks
Newer filings use `RevenueFromContractWithCustomerExcludingAssessedTax` + `AutomotiveRevenuesMember`.  
Older filings (early 2022–mid 2023) may use `tsla:AutomotiveRevenues` / `tsla:AutomotiveCostOfRevenues`. The extractor tries both.

## Caveats
- Inventory is consolidated balance-sheet dollars — **not** finished-vehicle units and **not** the production–delivery gap.
- Inventory days use automotive COGS as a flow proxy only.
- Missing iXBRL matches are left null and logged — never interpolated.
- Citation log: `data/reference/Fact_Financials_extraction_log.csv`
