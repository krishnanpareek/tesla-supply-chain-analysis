# Page 5 — DAX Measures (EV Market & Infrastructure)

**Tables:** `Fact_EV_Market`, `Fact_EV_Chargers_CA`  
**Geography:** California only  
**Status:** Reference documentation for HTML dashboard KPIs.

## Citation discipline

Expose Period_ID / Snapshot_Label, Data_As_Of, Source_File, Source_URL, Source_ID on every figure.

## Measures

```dax
Tesla ZEV Sales CA = SUM ( Fact_EV_Market[Tesla_ZEV_Sales_CA] )  -- Reported
Total ZEV Sales CA = SUM ( Fact_EV_Market[Total_ZEV_Sales_CA] )  -- Reported
Tesla Share of ZEV = DIVIDE ( [Tesla ZEV Sales CA], [Total ZEV Sales CA] )  -- Calculated
ZEV Share of LDV = AVERAGE ( Fact_EV_Market[ZEV_Share_of_LDV_Sales] )  -- Calculated
Total Chargers CA = SUM ( Fact_EV_Chargers_CA[Total_Chargers] )  -- Reported inventory
Public DC Fast CA = SUM ( Fact_EV_Chargers_CA[Public_DC_Fast] )  -- Reported inventory
```

**Guardrails:** Not national Tesla deliveries. Charger counts ≠ utilization. CEC methodology changed in 2023 and 2025.
