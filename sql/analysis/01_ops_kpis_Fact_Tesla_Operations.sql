-- KPI queries for Production & Delivery Performance (Power BI Page 2 precursors)
-- Metric labels: see Fact_Tesla_Operations.Metric_Notes / extraction log

-- 1) Quarterly totals: production, deliveries, gap, conversion
SELECT
    Period_ID,
    Reporting_Period,
    Vehicles_Produced,                 -- reported
    Vehicles_Delivered,                -- reported
    Production_Delivery_Gap,           -- calculated
    Delivery_Conversion_Rate,          -- calculated
    Energy_Storage_GWh                 -- reported/calculated/null
FROM Fact_Tesla_Operations
WHERE Vehicle_Group = 'Total'
ORDER BY Period_ID;

-- 2) QoQ growth in total deliveries (calculated)
SELECT
    Period_ID,
    Vehicles_Delivered,
    LAG(Vehicles_Delivered) OVER (ORDER BY Period_ID) AS Prior_Deliveries,
    ROUND(
        1.0 * (Vehicles_Delivered - LAG(Vehicles_Delivered) OVER (ORDER BY Period_ID))
        / NULLIF(LAG(Vehicles_Delivered) OVER (ORDER BY Period_ID), 0)
    , 4) AS QoQ_Delivery_Growth
FROM Fact_Tesla_Operations
WHERE Vehicle_Group = 'Total'
ORDER BY Period_ID;

-- 3) YoY growth in total deliveries (calculated; lag 4 quarters)
SELECT
    Period_ID,
    Vehicles_Delivered,
    LAG(Vehicles_Delivered, 4) OVER (ORDER BY Period_ID) AS Deliveries_YoY_Base,
    ROUND(
        1.0 * (Vehicles_Delivered - LAG(Vehicles_Delivered, 4) OVER (ORDER BY Period_ID))
        / NULLIF(LAG(Vehicles_Delivered, 4) OVER (ORDER BY Period_ID), 0)
    , 4) AS YoY_Delivery_Growth
FROM Fact_Tesla_Operations
WHERE Vehicle_Group = 'Total'
ORDER BY Period_ID;

-- 4) Mix share by as-reported vehicle group (excludes Total)
-- WARNING: Model S/X and Other Models are incompatible labels across the Q4 2023 break.
SELECT
    Period_ID,
    Vehicle_Group,
    Vehicles_Delivered,
    ROUND(
        1.0 * Vehicles_Delivered
        / NULLIF(SUM(Vehicles_Delivered) OVER (PARTITION BY Period_ID), 0)
    , 4) AS Delivery_Mix_Share
FROM Fact_Tesla_Operations
WHERE Vehicle_Group <> 'Total'
ORDER BY Period_ID, Vehicle_Group;

-- 5) 4-quarter rolling average of total deliveries (calculated)
SELECT
    Period_ID,
    Vehicles_Delivered,
    ROUND(AVG(Vehicles_Delivered) OVER (
        ORDER BY Period_ID
        ROWS BETWEEN 3 PRECEDING AND CURRENT ROW
    ), 1) AS Deliveries_4Q_Rolling_Avg
FROM Fact_Tesla_Operations
WHERE Vehicle_Group = 'Total'
ORDER BY Period_ID;

-- 6) Production-delivery gap trend (calculated; interpret with caveats)
SELECT
    Period_ID,
    Production_Delivery_Gap,
    CASE
        WHEN Production_Delivery_Gap > 0 THEN 'Production > Deliveries'
        WHEN Production_Delivery_Gap < 0 THEN 'Deliveries > Production'
        ELSE 'Equal'
    END AS Gap_Direction
FROM Fact_Tesla_Operations
WHERE Vehicle_Group = 'Total'
ORDER BY Period_ID;
