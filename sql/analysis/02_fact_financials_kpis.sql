-- KPI reference queries for Page 3 (Financial & Inventory Health)
-- Units: USD millions unless noted

-- Latest quarter snapshot
SELECT
    Period_ID,
    Total_Revenue,
    Automotive_Revenue,
    Automotive_Gross_Margin,
    Inventory,
    Inventory_Days_Estimate,
    Operating_Cash_Flow,
    CapEx,
    Free_Cash_Flow,
    Net_Income,
    Source_File_10Q_or_10K,
    Source_URL
FROM Fact_Financials
ORDER BY Period_End_Date DESC
LIMIT 1;

-- Trend series
SELECT
    Period_ID,
    Period_End_Date,
    Total_Revenue,
    Automotive_Revenue,
    Automotive_Gross_Margin,
    Inventory,
    Inventory_Days_Estimate,
    Operating_Cash_Flow,
    CapEx,
    Free_Cash_Flow
FROM Fact_Financials
ORDER BY Period_End_Date;

-- Inventory vs automotive revenue (liquidity / working capital view)
SELECT
    Period_ID,
    Inventory,
    Automotive_Revenue,
    CASE
        WHEN Automotive_Revenue IS NULL OR Automotive_Revenue = 0 THEN NULL
        ELSE Inventory / Automotive_Revenue
    END AS Inventory_to_Auto_Revenue
FROM Fact_Financials
ORDER BY Period_End_Date;

-- Join ops deliveries for context (do not treat gap as unsold inventory)
SELECT
    f.Period_ID,
    f.Inventory,
    f.Inventory_Days_Estimate,
    f.Automotive_Revenue,
    o.Total_Deliveries,
    o.Total_Production
FROM Fact_Financials f
LEFT JOIN (
    SELECT
        Period_ID,
        SUM(Deliveries) AS Total_Deliveries,
        SUM(Production) AS Total_Production
    FROM Fact_Tesla_Operations
    WHERE Vehicle_Group <> 'Total'
    GROUP BY Period_ID
) o ON o.Period_ID = f.Period_ID
ORDER BY f.Period_End_Date;
