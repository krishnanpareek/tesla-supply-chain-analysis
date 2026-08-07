-- Fact_Financials
-- Grain: one row per fiscal quarter (Period_ID)
-- Units: USD millions (iXBRL scale="6")
-- Source: SEC EDGAR 10-Q / 10-K HTML in data/raw/sec_edgar/
-- Extraction: scripts/extract_fact_financials.py
-- Enrichment: scripts/enrich_fact_financials.py
-- Citation log: data/reference/Fact_Financials_extraction_log.csv

CREATE TABLE Fact_Financials (
    Period_ID                      VARCHAR(6)    NOT NULL,  -- e.g. 2026Q2
    Reporting_Period               VARCHAR(40)   NOT NULL,  -- YYYY-MM-DD to YYYY-MM-DD
    Form                           VARCHAR(8)    NOT NULL,  -- 10-Q or 10-K
    Report_Date                    DATE          NOT NULL,  -- period end

    Total_Revenue                  DECIMAL(18,2) NULL,
    Automotive_Revenue             DECIMAL(18,2) NULL,
    Cost_of_Automotive_Revenue     DECIMAL(18,2) NULL,
    Automotive_Gross_Profit        DECIMAL(18,2) NULL,  -- calculated
    Automotive_Gross_Margin        DECIMAL(9,6)  NULL,  -- calculated

    Inventory                      DECIMAL(18,2) NULL,  -- period-end BS (reported)
    Accounts_Payable               DECIMAL(18,2) NULL,
    Capital_Expenditures           DECIMAL(18,2) NULL,  -- positive = cash outflow magnitude
    Operating_Cash_Flow            DECIMAL(18,2) NULL,
    Free_Cash_Flow                 DECIMAL(18,2) NULL,  -- calculated: OCF - CapEx
    Net_Income                     DECIMAL(18,2) NULL,

    Inventory_Days_Estimate        DECIMAL(12,4) NULL,  -- calculated: Inv / (Auto COGS / days)
    Days_In_Period                 INT           NULL,

    CashFlow_Basis                 VARCHAR(60)   NULL,
    OCF_Capex_Metric_Label         VARCHAR(80)   NULL,
    Unit                           VARCHAR(20)   NOT NULL,  -- USD_millions

    Source_File                    VARCHAR(260)  NOT NULL,
    Source_ID                      VARCHAR(64)   NULL,
    Source_Accession               VARCHAR(32)   NULL,
    Source_URL                     VARCHAR(500)  NULL,
    Publication_Date               DATE          NULL,
    Enriched_On                    DATE          NULL,

    CONSTRAINT PK_Fact_Financials PRIMARY KEY (Period_ID)
);
