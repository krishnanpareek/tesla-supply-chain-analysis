# Tesla Production, Delivery, Inventory, Quality, and Supply Chain Risk Analysis

Public-data portfolio project analyzing Tesla's production and delivery trends, financial and inventory health, vehicle quality/recalls, EV market position, and battery-material supply risk.

**Audience:** Supply Chain Analyst, Demand Planning Analyst, Inventory Analyst, Procurement Analyst, Operations Analyst, and Business Analyst roles.

**Data policy:** Only real, verifiable public sources (Tesla Investor Relations, SEC EDGAR, NHTSA, California Energy Commission, DOE AFDC, USGS). No fabricated values. Every externally sourced number is logged in the source inventory with URL, publication date, and reporting period.

## Repository status

Initial scaffold and source inventory are in progress. See `documentation/` for methodology and limitations as phases complete.

## Structure

```
data/raw/           Untouched source files (large files gitignored; URLs documented)
data/processed/     Cleaned / transformed datasets
data/reference/     Lookups and data dictionaries
sql/schema/         Star-schema DDL
sql/cleaning/       Transformation queries
sql/analysis/       Analysis queries
powerbi/            Dashboard and DAX documentation
documentation/      Source inventory, data dictionary, methodology, limitations
visuals/            Dashboard screenshots
reports/            Executive summary and insights
```

## License / disclaimer

This project uses publicly available data for educational and portfolio purposes. It does not claim access to Tesla internal systems, supplier contracts, or confidential factory data. Metrics are labeled as reported, calculated, estimated, or modeled.
