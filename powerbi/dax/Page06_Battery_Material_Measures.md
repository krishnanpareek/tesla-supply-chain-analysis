# Page 6 — DAX Measures (Battery Material Risk)

**Table:** `Fact_Raw_Materials` (from USGS MCS 2026 CSV · SRC-USGS-002)  
**Primary year:** **2025**  
**Status:** Reference documentation for HTML dashboard KPIs.

## Citation discipline

Expose Commodity, Year, Source_File (`MCS2026_Commodities_Data.csv`), Source_URL (ScienceBase item), Publication_Date (`2026-02-06`), DOI (`10.5066/P1WKQ63T`).

**Metric labels are field-level:** `Metric_Label=estimated` when USGS `Notes` contain “Estimated”; otherwise `reported`. Do **not** label all Page 6 KPIs as reported.

For MCS 2026, world mine production and U.S. net import reliance for **2025** are estimated for lithium, cobalt, nickel, and natural graphite.

## Measures

```dax
US Net Import Reliance 2025 =
CALCULATE (
    SELECTEDVALUE ( Fact_Raw_Materials[Value] ),
    Fact_Raw_Materials[Country] = "United States",
    CONTAINSSTRING ( Fact_Raw_Materials[Statistics], "import reliance" ),
    Fact_Raw_Materials[Year] = 2025
)
-- Metric label: use Fact_Raw_Materials[Metric_Label] (estimated for 2025 in MCS 2026)
-- Lithium may be a range string (e.g. >50)

World Mine Production 2025 =
CALCULATE (
    SUM ( Fact_Raw_Materials[Value_Numeric] ),
    Fact_Raw_Materials[Statistics] = "Production",
    CONTAINSSTRING ( Fact_Raw_Materials[Section], "World Mine Production" ),
    Fact_Raw_Materials[Country] = "World total",
    Fact_Raw_Materials[Year] = 2025
)
-- Metric label: estimated (2025)

Top Producer Output 2025 =
CALCULATE (
    MAX ( Fact_Raw_Materials[Value_Numeric] ),
    Fact_Raw_Materials[Statistics] = "Production",
    CONTAINSSTRING ( Fact_Raw_Materials[Section], "World Mine Production" ),
    Fact_Raw_Materials[Year] = 2025,
    NOT CONTAINSSTRING ( Fact_Raw_Materials[Country], "World" )
)
-- Metric label: estimated (2025 country mine production)

Top Producer Share of World =
DIVIDE ( [Top Producer Output 2025], [World Mine Production 2025] )
-- Metric label: calculated
```

## Guardrails

- Not Tesla purchase volumes or supplier identities.
- Concentration is a market-structure signal only.
- Prefer year **2025** as the newest MCS 2026 year; do not silently substitute 2024 reported values for 2025 KPIs.
