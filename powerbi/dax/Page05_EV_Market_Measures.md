# Page 5 — DAX Measures (EV Market & Infrastructure)

**Tables:** `Fact_EV_Market`, `Fact_EV_Chargers_CA`  
**Geography:** California only  
**Sources:** SRC-CEC-001 (ZEV/LDV sales), SRC-CEC-002 (chargers)  
**Status:** Reference documentation for HTML dashboard KPIs.

## Citation discipline

Expose `Period_ID` / `Snapshot_Label`, `Data_As_Of`, `Source_File`, `Source_URL`, `Source_ID` on every figure.

## Sales measures

```dax
Tesla ZEV Sales CA =
SUM ( Fact_EV_Market[Tesla_ZEV_Sales_CA] )
-- Metric label: Reported (CEC County MAKE=Tesla)
```

```dax
Total ZEV Sales CA =
SUM ( Fact_EV_Market[Total_ZEV_Sales_CA] )
-- Metric label: Reported
```

```dax
Tesla Share of ZEV =
DIVIDE ( [Tesla ZEV Sales CA], [Total ZEV Sales CA] )
-- Metric label: Calculated
```

```dax
ZEV Share of LDV =
AVERAGE ( Fact_EV_Market[ZEV_Share_of_LDV_Sales] )
-- Metric label: Calculated (from LDV workbook statewide sums)
```

## Charger measures (ports)

CEC workbook unit = **charging ports**, not stations.  
`All_Sectors_Ports_Total` = public + shared-private (workplaces / multi-family / fleets); **excludes residential**.  
Page 5 primary KPIs use **public ports only**.

```dax
Public Charging Ports CA =
SUM ( Fact_EV_Chargers_CA[Public_Ports_Total] )
-- = Public Level 1 + Public Level 2 + Public DC Fast
-- Metric label: Reported inventory snapshot
```

```dax
Public Level 2 Ports CA =
SUM ( Fact_EV_Chargers_CA[Public_Level_2] )
```

```dax
Public DC Fast Ports CA =
SUM ( Fact_EV_Chargers_CA[Public_DC_Fast] )
```

```dax
Shared Private Ports CA =
SUM ( Fact_EV_Chargers_CA[Shared_Private_Ports_Total] )
-- Context only — not the primary Page 5 availability KPI
```

## Guardrails

- Not national Tesla deliveries.  
- Do not label CEC `Total` as “public chargers” — it mixes public + shared private.  
- Charger counts ≠ utilization or Supercharger-only network.  
- CEC “new sale” inference methodology updated 2023 and 2025 — YoY with care.  
- Prefer export **Data as of** over contemporaneous press totals (e.g. 2025Q2 press 100,671 vs June 30, 2026 export 101,623).
