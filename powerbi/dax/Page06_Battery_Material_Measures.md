# Page 6 — DAX Measures (Battery Material Risk)

**Table:** `Fact_Raw_Materials` (from USGS MCS 2026 CSV)  
**Status:** Reference documentation for HTML dashboard KPIs.

## Citation discipline

Expose Commodity, Year, Source_File (`MCS2026_Commodities_Data.csv`), Source_URL (ScienceBase item), Publication_Date (`2026-02-06`), DOI.

## Measures

```dax
US Net Import Reliance =
CALCULATE (
    SELECTEDVALUE ( Fact_Raw_Materials[Value] ),
    Fact_Raw_Materials[Country] = "United States",
    CONTAINSSTRING ( Fact_Raw_Materials[Statistics], "import reliance" )
)
-- Metric label: Reported (may be a range string such as >50)

World Production by Country =
CALCULATE (
    SUM ( Fact_Raw_Materials[Value_Numeric] ),
    Fact_Raw_Materials[Statistics] = "Production"
)
-- Metric label: Reported
```

**Guardrails:** Not Tesla purchase volumes or supplier identities. Concentration is a market structure signal only.
