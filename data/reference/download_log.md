# Download Log

Exact local file inventory for Phase 3 raw downloads.

**Access / download date:** 2026-08-02

**Scope:** Tesla IR quarterly production/delivery releases Q1 2022–Q2 2026, and corresponding SEC Forms 10-Q / 10-K for the same window.

**Important:** No fact values were extracted into `Fact_Tesla_Operations` in this phase. This log is provenance only.

## Method notes

- Tesla IR production/delivery press releases are filed with the SEC as Form **8-K Exhibit 99.1** (Item 2.02). Local copies are those filed HTML exhibits (same operational figures published via Tesla IR).
- `Publication_Date` for IR rows = SEC **filing date** of the related 8-K (verified via EDGAR company filings atom feed).
- `Reporting_Period` for IR rows = calendar quarter covered by the release title / narrative.
- SEC financial rows use EDGAR filing date as `Publication_Date` and the form period end as `Reporting_Period_End`.
- Large SEC HTML filings under `data/raw/sec_edgar/` are gitignored; URLs below are the source of truth for re-download.

---

## A. Tesla IR — Production / Deliveries / Deployments (8-K EX-99.1)

| Source_ID | Local_Filename | Reporting_Period | Publication_Date (SEC filing date) | Accession | Source_URL | HTTP_Status | Bytes |
|-----------|----------------|------------------|------------------------------------|-----------|------------|-------------|-------|
| SRC-TESLA-IR-001-Q1_2022 | `tesla_production_deliveries_Q1_2022_2022-04-04_tsla-ex991_6.htm` | 2022-01-01 to 2022-03-31 (Q1 2022) | 2022-04-04 | 0001564590-22-013264 | https://www.sec.gov/Archives/edgar/data/1318605/000156459022013264/tsla-ex991_6.htm | 200 | 14161 |
| SRC-TESLA-IR-001-Q1_2023 | `tesla_production_deliveries_Q1_2023_2023-04-03_tsla-ex991_7.htm` | 2023-01-01 to 2023-03-31 (Q1 2023) | 2023-04-03 | 0001564590-23-005126 | https://www.sec.gov/Archives/edgar/data/1318605/000156459023005126/tsla-ex991_7.htm | 200 | 13776 |
| SRC-TESLA-IR-001-Q1_2024 | `tesla_production_deliveries_Q1_2024_2024-04-02_tsla-ex99_1.htm` | 2024-01-01 to 2024-03-31 (Q1 2024) | 2024-04-02 | 0000950170-24-040274 | https://www.sec.gov/Archives/edgar/data/1318605/000095017024040274/tsla-ex99_1.htm | 200 | 18696 |
| SRC-TESLA-IR-001-Q1_2025 | `tesla_production_deliveries_Q1_2025_2025-04-02_exhibit9911.htm` | 2025-01-01 to 2025-03-31 (Q1 2025) | 2025-04-02 | 0001628280-25-016070 | https://www.sec.gov/Archives/edgar/data/1318605/000162828025016070/exhibit9911.htm | 200 | 13783 |
| SRC-TESLA-IR-001-Q1_2026 | `tesla_production_deliveries_Q1_2026_2026-04-02_exhibit9911111.htm` | 2026-01-01 to 2026-03-31 (Q1 2026) | 2026-04-02 | 0001628280-26-022956 | https://www.sec.gov/Archives/edgar/data/1318605/000162828026022956/exhibit9911111.htm | 200 | 13242 |
| SRC-TESLA-IR-001-Q2_2022 | `tesla_production_deliveries_Q2_2022_2022-07-05_tsla-ex991_6.htm` | 2022-04-01 to 2022-06-30 (Q2 2022) | 2022-07-05 | 0001564590-22-025153 | https://www.sec.gov/Archives/edgar/data/1318605/000156459022025153/tsla-ex991_6.htm | 200 | 13794 |
| SRC-TESLA-IR-001-Q2_2023 | `tesla_production_deliveries_Q2_2023_2023-07-03_tsla-ex99_1.htm` | 2023-04-01 to 2023-06-30 (Q2 2023) | 2023-07-03 | 0000950170-23-031241 | https://www.sec.gov/Archives/edgar/data/1318605/000095017023031241/tsla-ex99_1.htm | 200 | 20368 |
| SRC-TESLA-IR-001-Q2_2024 | `tesla_production_deliveries_Q2_2024_2024-07-02_exhibit991.htm` | 2024-04-01 to 2024-06-30 (Q2 2024) | 2024-07-02 | 0001628280-24-030714 | https://www.sec.gov/Archives/edgar/data/1318605/000162828024030714/exhibit991.htm | 200 | 11831 |
| SRC-TESLA-IR-001-Q2_2025 | `tesla_production_deliveries_Q2_2025_2025-07-02_exhibit99111.htm` | 2025-04-01 to 2025-06-30 (Q2 2025) | 2025-07-02 | 0001628280-25-033842 | https://www.sec.gov/Archives/edgar/data/1318605/000162828025033842/exhibit99111.htm | 200 | 12900 |
| SRC-TESLA-IR-001-Q2_2026 | `tesla_production_deliveries_Q2_2026_2026-07-02_exhibit99111111.htm` | 2026-04-01 to 2026-06-30 (Q2 2026) | 2026-07-02 | 0001628280-26-046717 | https://www.sec.gov/Archives/edgar/data/1318605/000162828026046717/exhibit99111111.htm | 200 | 13243 |
| SRC-TESLA-IR-001-Q3_2022 | `tesla_production_deliveries_Q3_2022_2022-10-03_tsla-ex991_6.htm` | 2022-07-01 to 2022-09-30 (Q3 2022) | 2022-10-03 | 0001564590-22-033053 | https://www.sec.gov/Archives/edgar/data/1318605/000156459022033053/tsla-ex991_6.htm | 200 | 14850 |
| SRC-TESLA-IR-001-Q3_2023 | `tesla_production_deliveries_Q3_2023_2023-10-02_tsla-ex99_1.htm` | 2023-07-01 to 2023-09-30 (Q3 2023) | 2023-10-02 | 0000950170-23-050938 | https://www.sec.gov/Archives/edgar/data/1318605/000095017023050938/tsla-ex99_1.htm | 200 | 18295 |
| SRC-TESLA-IR-001-Q3_2024 | `tesla_production_deliveries_Q3_2024_2024-10-02_ex991.htm` | 2024-07-01 to 2024-09-30 (Q3 2024) | 2024-10-02 | 0001628280-24-041816 | https://www.sec.gov/Archives/edgar/data/1318605/000162828024041816/ex991.htm | 200 | 11365 |
| SRC-TESLA-IR-001-Q3_2025 | `tesla_production_deliveries_Q3_2025_2025-10-02_exhibit991111.htm` | 2025-07-01 to 2025-09-30 (Q3 2025) | 2025-10-02 | 0001628280-25-043530 | https://www.sec.gov/Archives/edgar/data/1318605/000162828025043530/exhibit991111.htm | 200 | 13300 |
| SRC-TESLA-IR-001-Q4_2022 | `tesla_production_deliveries_Q4_2022_2023-01-03_tsla-ex991_6.htm` | 2022-10-01 to 2022-12-31 (Q4 2022) | 2023-01-03 | 0001564590-23-000002 | https://www.sec.gov/Archives/edgar/data/1318605/000156459023000002/tsla-ex991_6.htm | 200 | 21870 |
| SRC-TESLA-IR-001-Q4_2023 | `tesla_production_deliveries_Q4_2023_2024-01-02_tsla-ex99_1.htm` | 2023-10-01 to 2023-12-31 (Q4 2023) | 2024-01-02 | 0000950170-24-000282 | https://www.sec.gov/Archives/edgar/data/1318605/000095017024000282/tsla-ex99_1.htm | 200 | 23365 |
| SRC-TESLA-IR-001-Q4_2024 | `tesla_production_deliveries_Q4_2024_2025-01-02_exhibit991.htm` | 2024-10-01 to 2024-12-31 (Q4 2024) | 2025-01-02 | 0001628280-25-000007 | https://www.sec.gov/Archives/edgar/data/1318605/000162828025000007/exhibit991.htm | 200 | 18186 |
| SRC-TESLA-IR-001-Q4_2025 | `tesla_production_deliveries_Q4_2025_2026-01-02_exhibit9914.htm` | 2025-10-01 to 2025-12-31 (Q4 2025) | 2026-01-02 | 0001628280-26-000016 | https://www.sec.gov/Archives/edgar/data/1318605/000162828026000016/exhibit9914.htm | 200 | 18153 |

**IR file count:** 18 (expected 18)

---

## B. SEC EDGAR — Forms 10-Q / 10-K

| Source_ID | Form | Local_Filename | Reporting_Period_End | Publication_Date (filing date) | Accession | Source_URL | HTTP_Status | Bytes |
|-----------|------|----------------|----------------------|--------------------------------|-----------|------------|-------------|-------|
| SRC-SEC-10-Q-Q1_2022 | 10-Q | `10-Q_Q1_2022_2022-03-31_tsla-20220331.htm` | 2022-03-31 | 2022-04-25 | 0000950170-22-006034 | https://www.sec.gov/Archives/edgar/data/1318605/000095017022006034/tsla-20220331.htm | 200 | 3736851 |
| SRC-SEC-10-Q-Q2_2022 | 10-Q | `10-Q_Q2_2022_2022-06-30_tsla-20220630.htm` | 2022-06-30 | 2022-07-25 | 0000950170-22-012936 | https://www.sec.gov/Archives/edgar/data/1318605/000095017022012936/tsla-20220630.htm | 200 | 5293087 |
| SRC-SEC-10-Q-Q3_2022 | 10-Q | `10-Q_Q3_2022_2022-09-30_tsla-20220930.htm` | 2022-09-30 | 2022-10-24 | 0000950170-22-019867 | https://www.sec.gov/Archives/edgar/data/1318605/000095017022019867/tsla-20220930.htm | 200 | 5602175 |
| SRC-SEC-10-K-FY_2022 | 10-K | `10-K_FY_2022_2022-12-31_tsla-20221231.htm` | 2022-12-31 | 2023-01-31 | 0000950170-23-001409 | https://www.sec.gov/Archives/edgar/data/1318605/000095017023001409/tsla-20221231.htm | 200 | 7964288 |
| SRC-SEC-10-Q-Q1_2023 | 10-Q | `10-Q_Q1_2023_2023-03-31_tsla-20230331.htm` | 2023-03-31 | 2023-04-24 | 0000950170-23-013890 | https://www.sec.gov/Archives/edgar/data/1318605/000095017023013890/tsla-20230331.htm | 200 | 3393247 |
| SRC-SEC-10-Q-Q2_2023 | 10-Q | `10-Q_Q2_2023_2023-06-30_tsla-20230630.htm` | 2023-06-30 | 2023-07-24 | 0000950170-23-033872 | https://www.sec.gov/Archives/edgar/data/1318605/000095017023033872/tsla-20230630.htm | 200 | 4619228 |
| SRC-SEC-10-Q-Q3_2023 | 10-Q | `10-Q_Q3_2023_2023-09-30_tsla-20230930.htm` | 2023-09-30 | 2023-10-23 | 0001628280-23-034847 | https://www.sec.gov/Archives/edgar/data/1318605/000162828023034847/tsla-20230930.htm | 200 | 1553218 |
| SRC-SEC-10-K-FY_2023 | 10-K | `10-K_FY_2023_2023-12-31_tsla-20231231.htm` | 2023-12-31 | 2024-01-29 | 0001628280-24-002390 | https://www.sec.gov/Archives/edgar/data/1318605/000162828024002390/tsla-20231231.htm | 200 | 2672746 |
| SRC-SEC-10-Q-Q1_2024 | 10-Q | `10-Q_Q1_2024_2024-03-31_tsla-20240331.htm` | 2024-03-31 | 2024-04-24 | 0001628280-24-017503 | https://www.sec.gov/Archives/edgar/data/1318605/000162828024017503/tsla-20240331.htm | 200 | 1179047 |
| SRC-SEC-10-Q-Q2_2024 | 10-Q | `10-Q_Q2_2024_2024-06-30_tsla-20240630.htm` | 2024-06-30 | 2024-07-24 | 0001628280-24-032662 | https://www.sec.gov/Archives/edgar/data/1318605/000162828024032662/tsla-20240630.htm | 200 | 1487943 |
| SRC-SEC-10-Q-Q3_2024 | 10-Q | `10-Q_Q3_2024_2024-09-30_tsla-20240930.htm` | 2024-09-30 | 2024-10-24 | 0001628280-24-043486 | https://www.sec.gov/Archives/edgar/data/1318605/000162828024043486/tsla-20240930.htm | 200 | 1502670 |
| SRC-SEC-10-K-FY_2024 | 10-K | `10-K_FY_2024_2024-12-31_tsla-20241231.htm` | 2024-12-31 | 2025-01-30 | 0001628280-25-003063 | https://www.sec.gov/Archives/edgar/data/1318605/000162828025003063/tsla-20241231.htm | 200 | 2596459 |
| SRC-SEC-10-Q-Q1_2025 | 10-Q | `10-Q_Q1_2025_2025-03-31_tsla-20250331.htm` | 2025-03-31 | 2025-04-23 | 0001628280-25-018911 | https://www.sec.gov/Archives/edgar/data/1318605/000162828025018911/tsla-20250331.htm | 200 | 1225850 |
| SRC-SEC-10-Q-Q2_2025 | 10-Q | `10-Q_Q2_2025_2025-06-30_tsla-20250630.htm` | 2025-06-30 | 2025-07-24 | 0001628280-25-035806 | https://www.sec.gov/Archives/edgar/data/1318605/000162828025035806/tsla-20250630.htm | 200 | 1518452 |
| SRC-SEC-10-Q-Q3_2025 | 10-Q | `10-Q_Q3_2025_2025-09-30_tsla-20250930.htm` | 2025-09-30 | 2025-10-23 | 0001628280-25-045968 | https://www.sec.gov/Archives/edgar/data/1318605/000162828025045968/tsla-20250930.htm | 200 | 1573631 |
| SRC-SEC-10-K-FY_2025 | 10-K | `10-K_FY_2025_2025-12-31_tsla-20251231.htm` | 2025-12-31 | 2026-01-29 | 0001628280-26-003952 | https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm | 200 | 2391529 |
| SRC-SEC-10-Q-Q1_2026 | 10-Q | `10-Q_Q1_2026_2026-03-31_tsla-20260331.htm` | 2026-03-31 | 2026-04-23 | 0001628280-26-026673 | https://www.sec.gov/Archives/edgar/data/1318605/000162828026026673/tsla-20260331.htm | 200 | 1240759 |
| SRC-SEC-10-Q-Q2_2026 | 10-Q | `10-Q_Q2_2026_2026-06-30_tsla-20260630.htm` | 2026-06-30 | 2026-07-23 | 0001628280-26-049270 | https://www.sec.gov/Archives/edgar/data/1318605/000162828026049270/tsla-20260630.htm | 200 | 1573323 |

**SEC file count:** 18 (expected 18: fourteen 10-Q + four 10-K)

### Period coverage map

| Ops quarter | IR release publication | Matching SEC form for financials |
|-------------|------------------------|----------------------------------|
| Q1 2022 | 2022-04-04 | 10-Q period ended 2022-03-31 (filed 2022-04-25) |
| Q2 2022 | 2022-07-05 | 10-Q period ended 2022-06-30 (filed 2022-07-25) |
| Q3 2022 | 2022-10-03 | 10-Q period ended 2022-09-30 (filed 2022-10-24) |
| Q4 2022 | 2023-01-03 | 10-K year ended 2022-12-31 (filed 2023-01-31) |
| Q1 2023 | 2023-04-03 | 10-Q period ended 2023-03-31 (filed 2023-04-24) |
| Q2 2023 | 2023-07-03 | 10-Q period ended 2023-06-30 (filed 2023-07-24) |
| Q3 2023 | 2023-10-02 | 10-Q period ended 2023-09-30 (filed 2023-10-23) |
| Q4 2023 | 2024-01-02 | 10-K year ended 2023-12-31 (filed 2024-01-29) |
| Q1 2024 | 2024-04-02 | 10-Q period ended 2024-03-31 (filed 2024-04-24) |
| Q2 2024 | 2024-07-02 | 10-Q period ended 2024-06-30 (filed 2024-07-24) |
| Q3 2024 | 2024-10-02 | 10-Q period ended 2024-09-30 (filed 2024-10-24) |
| Q4 2024 | 2025-01-02 | 10-K year ended 2024-12-31 (filed 2025-01-30) |
| Q1 2025 | 2025-04-02 | 10-Q period ended 2025-03-31 (filed 2025-04-23) |
| Q2 2025 | 2025-07-02 | 10-Q period ended 2025-06-30 (filed 2025-07-24) |
| Q3 2025 | 2025-10-02 | 10-Q period ended 2025-09-30 (filed 2025-10-23) |
| Q4 2025 | 2026-01-02 | 10-K year ended 2025-12-31 (filed 2026-01-29) |
| Q1 2026 | 2026-04-02 | 10-Q period ended 2026-03-31 (filed 2026-04-23) |
| Q2 2026 | 2026-07-02 | 10-Q period ended 2026-06-30 (filed 2026-07-23) |

## Limitations

- Local IR copies are SEC-filed HTML exhibits, not the ir.tesla.com PDF mirror (Akamai blocked automated PDF pulls from this environment). Figures are the same company-reported release content.
- SEC primary documents are iXBRL HTML; presentation markup is verbose. Extraction scripts must target reported line items carefully.
- No values from these files have been loaded into fact tables yet.
