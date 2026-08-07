-- Fact_Recalls from NHTSA ODI flat files (SRC-NHTSA-001)
-- Extraction: scripts/extract_fact_recalls_flat.py
-- Filter: MAKETXT = TESLA
-- POTAFF = Potential_Units_Affected (reported potential units, not repairs completed)

CREATE TABLE Fact_Recalls (
    Record_ID                      INT           NULL,
    Campaign_Number                VARCHAR(12)   NOT NULL,
    Make                           VARCHAR(40)   NOT NULL,
    Model                          VARCHAR(256)  NOT NULL,
    Model_Year                     INT           NULL,  -- null when YEARTXT=9999
    Component                      VARCHAR(256)  NULL,
    Manufacturer_Campaign_Number   VARCHAR(40)   NULL,
    Recall_Type_Code               VARCHAR(8)    NULL,
    Potential_Units_Affected       INT           NULL,  -- POTAFF
    Owner_Notify_Date              DATE          NULL,
    Report_Received_Date           DATE          NULL,  -- RCDATE
    Influenced_By                  VARCHAR(40)   NULL,
    Summary                        VARCHAR(4000) NULL,
    Consequence                    VARCHAR(2000) NULL,
    Remedy                         VARCHAR(4000) NULL,
    Notes                          VARCHAR(2000) NULL,
    Do_Not_Drive                   VARCHAR(8)    NULL,
    Park_Outside                   VARCHAR(8)    NULL,
    Source_File                    VARCHAR(260)  NOT NULL,  -- zip::txt member
    Source_Zip                     VARCHAR(80)   NOT NULL,
    Source_URL                     VARCHAR(500)  NOT NULL,
    Source_ID                      VARCHAR(32)   NOT NULL,  -- SRC-NHTSA-001
    Dictionary_File                VARCHAR(40)   NULL,
    Snapshot_Date                  DATE          NOT NULL,
    Metric_Label                   VARCHAR(20)   NOT NULL,
    Units_Note                     VARCHAR(200)  NULL
);

-- Optional annual rollup rebuilt from Fact_Recalls
CREATE TABLE Fact_NHTSA_Annual (
    Year                           INT          NOT NULL,
    Recall_Campaign_Count          INT          NULL,
    Potential_Units_Affected_Sum   INT          NULL,
    Source_ID                      VARCHAR(32)  NOT NULL,
    Snapshot_Date                  DATE         NOT NULL,
    Metric_Label                   VARCHAR(20)  NOT NULL,
    Notes                          VARCHAR(500) NULL,
    CONSTRAINT PK_Fact_NHTSA_Annual PRIMARY KEY (Year)
);
