-- Fact_Tesla_Operations
-- Grain: one row per Reporting_Period x Vehicle_Group (as reported in Tesla IR 8-K EX-99.1)
-- Primary key: (Period_ID, Vehicle_Group)
-- Source: data/processed/Fact_Tesla_Operations.csv
-- Traceability: data/reference/Fact_Tesla_Operations_extraction_log.csv
-- Format breaks: documentation/fact_tesla_operations_format_changes.md

CREATE TABLE IF NOT EXISTS Fact_Tesla_Operations (
    Period_ID                   VARCHAR(8)      NOT NULL,  -- e.g., 2022Q1
    Reporting_Period            VARCHAR(32)     NOT NULL,  -- e.g., 2022-01-01 to 2022-03-31
    Vehicle_Group               VARCHAR(32)     NOT NULL,  -- as reported: Model 3/Y | Model S/X | Other Models | Total
    Vehicles_Produced           INTEGER         NULL,      -- reported
    Vehicles_Delivered          INTEGER         NULL,      -- reported
    Energy_Storage_GWh          DECIMAL(12, 4)  NULL,      -- reported GWh, or calculated from MWh; Total rows only
    Production_Delivery_Gap     INTEGER         NULL,      -- calculated: Produced - Delivered
    Delivery_Conversion_Rate    DECIMAL(12, 6)  NULL,      -- calculated: Delivered / Produced
    Publication_Date            DATE            NULL,      -- SEC 8-K filing date
    Source_File                 VARCHAR(255)    NOT NULL,
    Source_ID                   VARCHAR(64)     NOT NULL,
    Vehicle_Group_As_Reported   VARCHAR(32)     NOT NULL,
    Format_Flags                VARCHAR(512)    NULL,
    Metric_Notes                VARCHAR(1024)   NULL,
    CONSTRAINT PK_Fact_Tesla_Operations PRIMARY KEY (Period_ID, Vehicle_Group)
);

-- Optional FK placeholders (dimensions built in later phases)
-- ALTER TABLE Fact_Tesla_Operations
--   ADD CONSTRAINT FK_Ops_DimDate FOREIGN KEY (Period_ID) REFERENCES Dim_Date(Period_ID);
-- ALTER TABLE Fact_Tesla_Operations
--   ADD CONSTRAINT FK_Ops_DimSource FOREIGN KEY (Source_ID) REFERENCES Dim_Source(Source_ID);
--
-- Note: Production_Delivery_Gap is NOT unsold inventory; see methodology/limitations.