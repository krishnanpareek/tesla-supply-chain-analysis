# Page 3 — DAX Measures (Financial & Inventory Health)

**Model table:** `Fact_Financials`  
**Grain:** one row per `Period_ID` (fiscal quarter).  
**Units:** USD millions unless noted.  
**Status:** Reference documentation only — analytical logic for the HTML dashboard KPIs. Not executed in a live Power BI model.

## Citation discipline (required)

Any card, data label, or tooltip that shows a specific figure must expose:

| Tooltip field | Source column / measure |
|---------------|-------------------------|
| Value | measure result |
| Metric label | Reported / Calculated / Estimated |
| Reporting period | `Fact_Financials[Reporting_Period]` |
| Publication / filing date | `Fact_Financials[Publication_Date]` |
| Source file | `Fact_Financials[Source_File]` |
| Source ID | `Fact_Financials[Source_ID]` |
| Source URL | `Fact_Financials[Source_URL]` |

Suggested tooltip title:

`{Period_ID} · {Metric name} ({Reported|Calculated|Estimated})`

---

## Core reported metrics

```dax
Total Revenue =
SUM ( Fact_Financials[Total_Revenue] )
-- Metric label: Reported (Q4 may be calculated — see Q4 basis notes)
```

```dax
Automotive Revenue =
SUM ( Fact_Financials[Automotive_Revenue] )
-- Metric label: Reported (AutomotiveRevenuesMember / legacy tsla:AutomotiveRevenues)
```

```dax
Cost of Automotive Revenue =
SUM ( Fact_Financials[Cost_of_Automotive_Revenue] )
-- Metric label: Reported (or calculated for Q4)
```

```dax
Inventory =
SUM ( Fact_Financials[Inventory] )
-- Metric label: Reported (period-end balance sheet)
-- Note: consolidated $ inventory, not vehicle units; not production–delivery gap
```

```dax
Accounts Payable =
SUM ( Fact_Financials[Accounts_Payable] )
-- Metric label: Reported
```

```dax
Operating Cash Flow =
SUM ( Fact_Financials[Operating_Cash_Flow] )
-- Metric label: see Fact_Financials[OCF_Capex_Metric_Label]
-- Q1: often reported (YTD = quarter)
-- Q2/Q3: calculated as current YTD − prior YTD
-- Q4: calculated as annual − 9-mo YTD
```

```dax
Capital Expenditures =
SUM ( Fact_Financials[Capital_Expenditures] )
-- Metric label: same basis as OCF
-- Stored as positive cash-outflow magnitude
```

```dax
Net Income =
SUM ( Fact_Financials[Net_Income] )
-- Metric label: Reported for Q1–Q3 three-month; Calculated for Q4
```

---

## Calculated / estimated metrics

```dax
Automotive Gross Profit =
SUM ( Fact_Financials[Automotive_Gross_Profit] )
-- Equivalent:
-- SUM ( Fact_Financials[Automotive_Revenue] ) - SUM ( Fact_Financials[Cost_of_Automotive_Revenue] )
-- Metric label: Calculated
```

```dax
Automotive Gross Margin =
DIVIDE (
    [Automotive Gross Profit],
    [Automotive Revenue]
)
-- Metric label: Calculated
```

```dax
Free Cash Flow =
[Operating Cash Flow] - [Capital Expenditures]
-- Metric label: Calculated
-- Requires CapEx stored as positive outflow (as in Fact_Financials)
```

```dax
Inventory Days Estimate =
DIVIDE (
    [Inventory],
    DIVIDE (
        [Cost of Automotive Revenue],
        SELECTEDVALUE ( Fact_Financials[Days_In_Period] )
    )
)
-- Metric label: Estimated
-- Proxy only: uses automotive COGS as flow; not finished-goods days
```

```dax
Inventory to Automotive Revenue =
DIVIDE ( [Inventory], [Automotive Revenue] )
-- Metric label: Calculated
```

---

## Context measures (optional join to ops)

Do **not** treat production–delivery gap as unsold inventory.

```dax
Ops Deliveries (Total) =
CALCULATE (
    SUM ( Fact_Tesla_Operations[Vehicles_Delivered] ),
    Fact_Tesla_Operations[Vehicle_Group] = "Total"
)
```

```dax
Revenue per Delivery (Est.) =
DIVIDE (
    [Automotive Revenue] * 1000000,  -- convert $M to $
    [Ops Deliveries (Total)]
)
-- Metric label: Estimated
-- Automotive revenue includes credits/leasing mix; not ASP
```

---

## Basis / disclosure measures

```dax
Cash Flow Basis Label =
SELECTEDVALUE ( Fact_Financials[OCF_Capex_Metric_Label] )
```

```dax
Filing Form =
SELECTEDVALUE ( Fact_Financials[Form] )
```

```dax
Source File =
SELECTEDVALUE ( Fact_Financials[Source_File] )
```
