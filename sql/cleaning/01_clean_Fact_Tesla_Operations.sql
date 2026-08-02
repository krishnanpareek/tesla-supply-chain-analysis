-- Cleaning / load notes for Fact_Tesla_Operations
-- Source files: data/raw/tesla_ir/tesla_production_deliveries_*.htm (untouched)
-- Extractor: scripts/extract_fact_tesla_operations.py
-- Output: data/processed/Fact_Tesla_Operations.csv
--
-- Documented transformation steps:
-- 1. Parse SEC 8-K Exhibit 99.1 HTML text (cell separators normalized).
-- 2. Repair digit sequences split by markup (e.g., "258,5 8 0" -> 258580) — Q2 2022 Total Production.
-- 3. Take the FIRST quarterly Production|Deliveries table only; ignore later full-year tables in Q4 releases.
-- 4. Keep Vehicle_Group labels AS REPORTED (Model S/X vs Other Models not merged).
-- 5. Energy_Storage_GWh:
--      - null when not disclosed
--      - MWh / 1000 when disclosed in MWh (Q1 2024) — metric_label = calculated
--      - GWh as reported otherwise — metric_label = reported
--      - populated on Total rows only
-- 6. Production_Delivery_Gap = Vehicles_Produced - Vehicles_Delivered (calculated).
-- 7. Delivery_Conversion_Rate = Vehicles_Delivered / Vehicles_Produced (calculated).
-- 8. No silent interpolation of missing values.
--
-- Example load (PostgreSQL):
--   COPY Fact_Tesla_Operations FROM 'data/processed/Fact_Tesla_Operations.csv' CSV HEADER;
--
-- Example load (SQLite):
--   .mode csv
--   .import data/processed/Fact_Tesla_Operations.csv Fact_Tesla_Operations

-- Sanity checks after load
SELECT Period_ID, Vehicle_Group, Vehicles_Produced, Vehicles_Delivered, Energy_Storage_GWh
FROM Fact_Tesla_Operations
ORDER BY Period_ID, Vehicle_Group;

-- Segment sums should equal Total for each period
SELECT
    s.Period_ID,
    SUM(s.Vehicles_Produced) AS segment_produced,
    t.Vehicles_Produced AS total_produced,
    SUM(s.Vehicles_Delivered) AS segment_delivered,
    t.Vehicles_Delivered AS total_delivered
FROM Fact_Tesla_Operations s
JOIN Fact_Tesla_Operations t
  ON t.Period_ID = s.Period_ID AND t.Vehicle_Group = 'Total'
WHERE s.Vehicle_Group <> 'Total'
GROUP BY s.Period_ID, t.Vehicles_Produced, t.Vehicles_Delivered
HAVING SUM(s.Vehicles_Produced) <> t.Vehicles_Produced
    OR SUM(s.Vehicles_Delivered) <> t.Vehicles_Delivered;
