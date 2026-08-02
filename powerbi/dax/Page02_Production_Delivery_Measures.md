# Page 2 — DAX Measures (Production & Delivery Performance)

**Model table:** `Fact_Tesla_Operations`  
**Grain reminder:** filter to `Vehicle_Group = "Total"` for company-level KPIs unless a visual is intentionally sliced by group.

## Citation discipline (required)

Any card, data label, or tooltip that shows a specific figure must expose:

| Tooltip field | Source column / measure |
|---------------|-------------------------|
| Value | measure result |
| Metric label | Reported / Calculated |
| Reporting period | `Fact_Tesla_Operations[Reporting_Period]` |
| Publication date | `Fact_Tesla_Operations[Publication_Date]` |
| Source file | `Fact_Tesla_Operations[Source_File]` |
| Source ID | `Fact_Tesla_Operations[Source_ID]` |

Suggested tooltip title template:

`{Period_ID} · {Vehicle_Group} · {Metric name} ({Reported|Calculated})`

Suggested tooltip body template:

```
Value: {formatted value}
Reporting period: {Reporting_Period}
Published: {Publication_Date}
Source file: {Source_File}
Source ID: {Source_ID}
Note: Production–delivery gap is not unsold inventory.
```

---

## Filter / helper measures

```dax
Selected Vehicle Group =
SELECTEDVALUE ( Fact_Tesla_Operations[Vehicle_Group], "Total" )
```

```dax
Is Total Group =
SELECTEDVALUE ( Fact_Tesla_Operations[Vehicle_Group] ) = "Total"
```

```dax
Format Break Flag =
VAR flags = SELECTEDVALUE ( Fact_Tesla_Operations[Format_Flags] )
RETURN
    IF (
        CONTAINSSTRING ( flags, "vehicle_group_label=Other_Models" ),
        "Other Models taxonomy",
        IF (
            CONTAINSSTRING ( flags, "vehicle_group_label=Model_S_X" ),
            "Model S/X taxonomy",
            BLANK ()
        )
    )
```

---

## Core reported metrics

```dax
Vehicles Produced =
SUM ( Fact_Tesla_Operations[Vehicles_Produced] )
-- Metric label: Reported
```

```dax
Vehicles Delivered =
SUM ( Fact_Tesla_Operations[Vehicles_Delivered] )
-- Metric label: Reported
```

```dax
Energy Storage GWh =
SUM ( Fact_Tesla_Operations[Energy_Storage_GWh] )
-- Metric label: Reported (GWh) or Calculated (from MWh in Q1 2024 only); null when undisclosed
```

---

## Core calculated metrics

```dax
Production Delivery Gap =
SUM ( Fact_Tesla_Operations[Production_Delivery_Gap] )
-- Metric label: Calculated = Produced - Delivered
-- Do NOT label as unsold inventory in titles/tooltips
```

```dax
Delivery Conversion Rate =
DIVIDE (
    [Vehicles Delivered],
    [Vehicles Produced]
)
-- Metric label: Calculated
```

```dax
Gap Direction =
VAR g = [Production Delivery Gap]
RETURN
    SWITCH (
        TRUE (),
        g > 0, "Production > Deliveries",
        g < 0, "Deliveries > Production",
        g = 0, "Equal",
        BLANK ()
    )
```

---

## Growth & rolling KPIs (Total group visuals)

Use a visual- or page-level filter `Vehicle_Group = "Total"` for these, or wrap with `CALCULATE ( ..., Fact_Tesla_Operations[Vehicle_Group] = "Total" )`.

```dax
Deliveries QoQ Growth =
VAR curr = [Vehicles Delivered]
VAR prev =
    CALCULATE (
        [Vehicles Delivered],
        DATEADD ( Dim_Date[Period_End], -1, QUARTER )  -- if Dim_Date exists
    )
RETURN
    DIVIDE ( curr - prev, prev )
-- Until Dim_Date exists, compute QoQ in Power Query or use Period_ID sort index below
```

### Period sort index (no Dim_Date yet)

Add a calculated column on `Fact_Tesla_Operations`:

```dax
Period Sort =
VAR y = VALUE ( LEFT ( Fact_Tesla_Operations[Period_ID], 4 ) )
VAR q = VALUE ( RIGHT ( Fact_Tesla_Operations[Period_ID], 1 ) )
RETURN y * 10 + q
```

Then:

```dax
Deliveries QoQ Growth (by Period Sort) =
VAR currSort = SELECTEDVALUE ( Fact_Tesla_Operations[Period Sort] )
VAR curr = [Vehicles Delivered]
VAR prev =
    CALCULATE (
        [Vehicles Delivered],
        Fact_Tesla_Operations[Period Sort] = currSort - 1,
        REMOVEFILTERS ( Fact_Tesla_Operations[Period_ID] )
    )
RETURN
    DIVIDE ( curr - prev, prev )
-- Metric label: Calculated
```

```dax
Deliveries YoY Growth (by Period Sort) =
VAR currSort = SELECTEDVALUE ( Fact_Tesla_Operations[Period Sort] )
VAR curr = [Vehicles Delivered]
VAR prev =
    CALCULATE (
        [Vehicles Delivered],
        Fact_Tesla_Operations[Period Sort] = currSort - 4,
        REMOVEFILTERS ( Fact_Tesla_Operations[Period_ID] )
    )
RETURN
    DIVIDE ( curr - prev, prev )
-- Metric label: Calculated
```

```dax
Deliveries 4Q Rolling Avg =
VAR currSort = SELECTEDVALUE ( Fact_Tesla_Operations[Period Sort] )
RETURN
    AVERAGEX (
        FILTER (
            ALLSELECTED ( Fact_Tesla_Operations[Period Sort] ),
            Fact_Tesla_Operations[Period Sort] <= currSort
                && Fact_Tesla_Operations[Period Sort] > currSort - 4
        ),
        CALCULATE ( [Vehicles Delivered] )
    )
-- Metric label: Calculated
```

---

## Mix share (segment visuals only)

```dax
Delivery Mix Share =
DIVIDE (
    [Vehicles Delivered],
    CALCULATE (
        [Vehicles Delivered],
        REMOVEFILTERS ( Fact_Tesla_Operations[Vehicle_Group] ),
        Fact_Tesla_Operations[Vehicle_Group] <> "Total"
    )
)
-- Metric label: Calculated
-- WARNING: do not chart Model S/X and Other Models as one continuous series without a break annotation at 2023Q4
```

---

## Citation measures for tooltips

```dax
Tooltip Source File =
SELECTEDVALUE ( Fact_Tesla_Operations[Source_File] )
```

```dax
Tooltip Publication Date =
SELECTEDVALUE ( Fact_Tesla_Operations[Publication_Date] )
```

```dax
Tooltip Source ID =
SELECTEDVALUE ( Fact_Tesla_Operations[Source_ID] )
```

```dax
Tooltip Reporting Period =
SELECTEDVALUE ( Fact_Tesla_Operations[Reporting_Period] )
```

```dax
Tooltip Metric Notes =
SELECTEDVALUE ( Fact_Tesla_Operations[Metric_Notes] )
```
