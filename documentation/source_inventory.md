# Source Inventory

Traceability log for every externally sourced dataset in this project.

**Rules:** Every externally sourced number must map to a `Source_ID` below (URL, publication/update context, reporting period). If a field cannot be verified yet, it is marked **MANUAL LOCATE** — do not invent values. Access date for this inventory pass: **2026-08-02**.

**Metric labels used later in facts:** reported | calculated | estimated | modeled.

---

## Column definitions

| Column | Meaning |
|--------|---------|
| Source_ID | Stable project key |
| Dataset_Name | Human-readable dataset name |
| Organization | Publishing organization |
| Source_URL | Verified landing or download URL |
| Publication_Date | Publisher date when known; else null + note |
| Reporting_Period | Time coverage of the data |
| File_Format | Expected local format |
| Update_Frequency | How often the source refreshes |
| Data_Fields | Key fields relevant to this project |
| Data_Definition | What the dataset represents |
| Primary/Secondary | Primary = core fact input; Secondary = supporting/context |
| Access_Date | Date this inventory entry was verified |
| Reliability_Notes | Trust / quality notes |
| Limitations | Coverage gaps and misuse risks |
| Status | `URL verified` or `MANUAL LOCATE required` |

---

## Tesla Investor Relations

### SRC-TESLA-IR-001 — Quarterly Production, Deliveries & Deployments Updates

| Field | Value |
|-------|-------|
| Source_ID | SRC-TESLA-IR-001 |
| Dataset_Name | Tesla Quarterly Production, Deliveries & Deployments Press Updates |
| Organization | Tesla, Inc. — Investor Relations |
| Source_URL | https://ir.tesla.com/press |
| Example release URL (verified) | https://ir.tesla.com/press-release/tesla-second-quarter-2025-production-deliveries-deployments |
| Example PDF (verified content) | https://ir.tesla.com/_flysystem/s3/sec/000162828026000016/tsla-20260102-gen.pdf (Q4 2025 production/deliveries/deployments advisory) |
| Publication_Date | Per release (quarterly); example Q4 2025 advisory associated with early Jan 2026 posting — **record exact date from each PDF/HTML at download time** |
| Reporting_Period | Calendar quarter (e.g., Q1–Q4); vehicle groups as Tesla reports them (often Model 3/Y vs other models; energy storage GWh) |
| File_Format | HTML press release + PDF |
| Update_Frequency | Quarterly (plus ad hoc IR updates) |
| Data_Fields | Vehicles produced, vehicles delivered, energy storage deployed (GWh), vehicle group breakouts when disclosed |
| Data_Definition | Company-reported production, delivery, and energy storage deployment totals for the stated quarter |
| Primary/Secondary | Primary → `Fact_Tesla_Operations` |
| Access_Date | 2026-08-02 |
| Reliability_Notes | Official company disclosure; suitable as **reported** metrics. Vehicle group definitions may change over time — capture wording from each release. |
| Limitations | Not SKU-level or factory-level. Deliveries ≠ retail “sales” in all contexts. Production–delivery gap is **not** unsold inventory. Energy metrics are deployments, not vehicle inventory. |
| Status | URL verified. **Downloaded for Q1 2022–Q2 2026** as SEC 8-K EX-99.1 HTML under `data/raw/tesla_ir/`. Per-file publication dates and reporting periods: `data/reference/download_log.md`. |

### SRC-TESLA-IR-002 — Quarterly Shareholder / Financial Updates (context)

| Field | Value |
|-------|-------|
| Source_ID | SRC-TESLA-IR-002 |
| Dataset_Name | Tesla Quarterly Updates / Shareholder Deck PDFs |
| Organization | Tesla, Inc. — Investor Relations |
| Source_URL | https://ir.tesla.com/ |
| Example PDF (verified content present) | https://ir.tesla.com/_flysystem/s3/sec/000162828025045861/tsla-20251022-gen.pdf |
| Publication_Date | Per deck; **capture from each file** |
| Reporting_Period | Quarter and YTD as stated in each update |
| File_Format | PDF |
| Update_Frequency | Quarterly |
| Data_Fields | May include production/delivery charts, energy deployments, selected financial highlights |
| Data_Definition | Management-presented quarterly business update materials |
| Primary/Secondary | Secondary (cross-check / narrative context). Prefer SRC-TESLA-IR-001 for ops counts and SEC filings for GAAP financials. |
| Access_Date | 2026-08-02 |
| Reliability_Notes | Official IR materials; charts may round. Prefer tabular press figures or SEC line items when they conflict with rounded slides. |
| Limitations | Not a substitute for 10-K/10-Q line items. Some figures may be non-GAAP — label carefully. |
| Status | Hub URL verified; example deck URL returned content. **MANUAL LOCATE:** assemble the historical deck set you want to archive. |

---

## SEC EDGAR

### SRC-SEC-001 — Tesla Forms 10-K / 10-Q (company filings index)

| Field | Value |
|-------|-------|
| Source_ID | SRC-SEC-001 |
| Dataset_Name | Tesla, Inc. EDGAR Company Filings (CIK 0001318605) |
| Organization | U.S. Securities and Exchange Commission (EDGAR) |
| Source_URL | https://www.sec.gov/edgar/browse/?CIK=1318605 |
| Alternate company search | https://www.sec.gov/edgar/searchedgar/companysearch (search issuer **Tesla, Inc.** / CIK **0001318605**) |
| Publication_Date | Filing date per submission |
| Reporting_Period | Fiscal year (10-K) or fiscal quarter (10-Q); Tesla FY ends Dec 31 |
| File_Format | HTML, iXBRL, exhibits |
| Update_Frequency | Quarterly 10-Q; annual 10-K; amendments as filed |
| Data_Fields | Total revenue, automotive revenue, cost of automotive revenue, inventory, accounts payable, capital expenditures, operating cash flow, net income (exact captions as in statements) |
| Data_Definition | Audited/unaudited consolidated financial statements and notes filed with the SEC |
| Primary/Secondary | Primary → `Fact_Financials` |
| Access_Date | 2026-08-02 |
| Reliability_Notes | Highest-authority public financial source for Tesla as a registrant. Use statement line items as **reported**; ratios (e.g., inventory turns, margins) as **calculated**. |
| Limitations | Segment captions and inventory subcomponents vary by period. Capex and OCF may appear in cash flow statement / MD&A — cite exact statement and period. No SKU inventory. |
| Status | CIK and recent filing URLs verified (see examples below). |

### SRC-SEC-002 — Example annual / quarterly filings (seed list; expand at extract time)

| Source_ID | Form | Reporting period | Verified document URL | Status |
|-----------|------|------------------|-----------------------|--------|
| SRC-SEC-002a | 10-K | Year ended 2025-12-31 | https://www.sec.gov/Archives/edgar/data/1318605/000162828026003952/tsla-20251231.htm | URL verified |
| SRC-SEC-002b | 10-K | Year ended 2024-12-31 | https://www.sec.gov/Archives/edgar/data/1318605/000162828025003063/tsla-20241231.htm | URL verified |
| SRC-SEC-002c | 10-Q | Quarter ended 2026-06-30 | https://www.sec.gov/Archives/edgar/data/1318605/000162828026049270/tsla-20260630.htm | URL verified |
| SRC-SEC-002d | 10-Q | Quarter ended 2026-03-31 | https://www.sec.gov/Archives/edgar/data/1318605/000162828026026673/tsla-20260331.htm | URL verified |

| Field | Value (applies to SRC-SEC-002*) |
|-------|----------------------------------|
| Organization | SEC EDGAR / Tesla, Inc. filer |
| File_Format | HTML (iXBRL) |
| Update_Frequency | As filed |
| Data_Fields | Same financial fields as SRC-SEC-001 |
| Primary/Secondary | Primary |
| Access_Date | 2026-08-02 |
| Reliability_Notes | Document URLs verified via EDGAR archives on access date. |
| Limitations | Still need systematic extraction of each line item into `Fact_Financials` with period tags; do not copy numbers into this inventory until extraction with citation. |
| Status | Seed URLs verified. **Downloaded for report dates 2022-03-31 through 2026-06-30** (14× 10-Q + 4× 10-K) under `data/raw/sec_edgar/` (gitignored; URLs in `data/reference/download_log.md`). |

---

## NHTSA

### SRC-NHTSA-001 — Recalls flat files / datasets hub

| Field | Value |
|-------|-------|
| Source_ID | SRC-NHTSA-001 |
| Dataset_Name | NHTSA ODI Recalls Flat File Dataset |
| Organization | National Highway Traffic Safety Administration (NHTSA) |
| Source_URL | https://www.nhtsa.gov/nhtsa-datasets-and-apis |
| Flat-file directory (documented by NHTSA) | https://static.nhtsa.gov/odi/ffdd/rcl/ |
| Field dictionary / import notes | https://static.nhtsa.gov/odi/ffdd/rcl/Import_Instructions_Recalls.pdf |
| Publication_Date | Flat files updated on an ongoing / frequent refresh schedule (hub lists file “Updated” timestamps — capture at download) |
| Reporting_Period | Campaigns since 1967 (full history in combined files); filter to Make = TESLA for this project |
| File_Format | ZIP → tab-delimited TXT |
| Update_Frequency | Ongoing (check hub timestamps) |
| Data_Fields | CAMPNO, MAKETXT, MODELTXT, YEARTXT, COMPNAME, POTAFF, ODATE, RCLTYPECD, defect/consequence/remedy text fields (per RCL dictionary) |
| Data_Definition | Safety-related defect and noncompliance recall campaigns reported to NHTSA |
| Primary/Secondary | Primary → `Fact_Recalls` |
| Access_Date | 2026-08-02 |
| Reliability_Notes | Official U.S. safety regulator database. `POTAFF` is potential units affected as reported — treat as **reported**, not confirmed repairs completed. |
| Limitations | U.S.-centric. Component text is free-form. Do not assert supplier causation from component strings. Large files — gitignore; store locally under `data/raw/nhtsa/`. |
| Status | Downloaded 2026-08-07: `FLAT_RCL_PRE_2010.zip` + `FLAT_RCL_POST_2010.zip` (+ `RCL.txt`, import instructions). Last-Modified HTTP 2026-08-07 07:05:12 GMT. Primary extract path for `Fact_Recalls` via `scripts/extract_fact_recalls_flat.py`. |

### SRC-NHTSA-002 — Complaints flat files

| Field | Value |
|-------|-------|
| Source_ID | SRC-NHTSA-002 |
| Dataset_Name | NHTSA ODI Consumer Complaints Flat File Dataset |
| Organization | NHTSA |
| Source_URL | https://www.nhtsa.gov/nhtsa-datasets-and-apis |
| Complaints directory | https://static.nhtsa.gov/odi/ffdd/cmpl/ |
| Field dictionary | https://static.nhtsa.gov/odi/ffdd/cmpl/CMPL.txt |
| Publication_Date | Capture hub “Updated” timestamp at download (FLAT_CMPL.zip is large) |
| Reporting_Period | Complaints received since ~1995; filter to Tesla |
| File_Format | ZIP → tab-delimited TXT |
| Update_Frequency | Ongoing / daily-style refresh per NHTSA notes |
| Data_Fields | ODINO, MAKETXT, MODELTXT, YEARTXT, COMPDESC, CRASH, FIRE, INJURED, DEATHS, DATEA/LDATE, CDESCR, etc. |
| Data_Definition | Safety-related defect complaints submitted to NHTSA |
| Primary/Secondary | Primary → `Fact_Complaints` |
| Access_Date | 2026-08-02 |
| Reliability_Notes | Complaints are allegations, not confirmed defects. Useful for **reported** complaint volume / flags; not incidence rates without exposure denominators. |
| Limitations | Selection bias; duplicates possible; not normalized per vehicles in operation unless you add an external exposure metric (often unavailable publicly at model-year grain). |
| Status | Hub + CMPL.txt dictionary URL verified. **MANUAL LOCATE:** download FLAT_CMPL.zip (or year slices) and record size/timestamp; file is hundreds of MB — do not commit. |

### SRC-NHTSA-003 — Vehicle-level Recalls / Complaints API (optional extract path)

| Field | Value |
|-------|-------|
| Source_ID | SRC-NHTSA-003 |
| Dataset_Name | NHTSA Recalls and Complaints APIs (by make/model/year) |
| Organization | NHTSA |
| Source_URL | https://www.nhtsa.gov/nhtsa-datasets-and-apis |
| Recalls example syntax | `https://api.nhtsa.gov/recalls/recallsByVehicle?make=tesla&model={MODEL}&modelYear={YEAR}` |
| Complaints example syntax | `https://api.nhtsa.gov/complaints/complaintsByVehicle?make=tesla&model={MODEL}&modelYear={YEAR}` |
| Publication_Date | Live API; snapshot date = extract date |
| Reporting_Period | All campaigns/complaints returned for that make/model/year as of extract |
| File_Format | JSON (API) |
| Update_Frequency | Ongoing |
| Data_Fields | Campaign numbers, components, summaries, complaint ODI numbers, crash/fire/injury fields |
| Data_Definition | Same ODI domains as flat files, queried per vehicle key |
| Primary/Secondary | Secondary / alternate extract method for Tesla-only subsets |
| Access_Date | 2026-08-02 |
| Reliability_Notes | No API key required per NHTSA docs. Prefer flat files for bulk reproducibility; API useful for model-year targeted pulls. |
| Limitations | Must enumerate model + year combinations; pagination/completeness should be validated against flat-file counts. |
| Status | Documentation URL verified; example endpoint patterns documented by NHTSA. **MANUAL LOCATE:** finalize Tesla model name spellings as they appear in NHTSA (`MODEL 3`, `MODEL Y`, etc.) before scripting. |

---

## California Energy Commission (CEC)

### SRC-CEC-001 — New ZEV Sales in California (dashboard + stats collection)

| Field | Value |
|-------|-------|
| Source_ID | SRC-CEC-001 |
| Dataset_Name | New ZEV Sales in California |
| Organization | California Energy Commission |
| Source_URL | https://www.energy.ca.gov/data-reports/energy-almanac/zero-emission-vehicle-and-infrastructure-statistics-collection/new-zev |
| Collection hub | https://www.energy.ca.gov/data-reports/energy-almanac/zero-emission-vehicle-and-infrastructure-statistics-collection |
| Citation landing (CEC) | https://www.energy.ca.gov/zevstats |
| Publication_Date | Dashboard states update metadata on page (example observed in search snippet: data-as-of / dashboard-updated fields — **copy exact dates from page at download**) |
| Reporting_Period | Quarterly updates of DMV-based new ZEV registration analysis; geographic grain may include county / MSA / ZIP depending on view |
| File_Format | Dashboard export / downloadable tables (CSV/XLSX when offered) |
| Update_Frequency | Quarterly (CEC description) |
| Data_Fields | Manufacturer, model, fuel type (BEV/PHEV/FCEV), geography, period, vehicle counts |
| Data_Definition | CEC analysis of California DMV data to infer **new ZEV sales/registrations** (method documented by CEC; not a raw DMV dump) |
| Primary/Secondary | Primary → `Fact_EV_Market` (CA registrations / sales side) |
| Access_Date | 2026-08-02 |
| Reliability_Notes | Authoritative for **California** ZEV market stats. Methodology for “new sale” inference has changed over time — read CEC notes before YoY comparisons. |
| Limitations | California-only for this source. Not national Tesla deliveries. County/ZIP assignments use mailing address rules with exceptions. |
| Status | Page URLs verified. **MANUAL LOCATE:** use dashboard “download data” control and/or CEC file bundle (SRC-CEC-003) to obtain manufacturer/model-level tables; record exact export filename + data-as-of date. |

### SRC-CEC-002 — Light-Duty Vehicle Population & EV Chargers (same collection)

| Field | Value |
|-------|-------|
| Source_ID | SRC-CEC-002 |
| Dataset_Name | CEC Light-Duty Vehicle Population and EV Chargers Statistics |
| Organization | California Energy Commission |
| Source_URL | https://www.energy.ca.gov/data-reports/energy-almanac/zero-emission-vehicle-and-infrastructure-statistics-collection |
| Publication_Date | Per dashboard “Data as of” / “Dashboard last updated” |
| Reporting_Period | Point-in-time population and charger counts as labeled |
| File_Format | Dashboard / downloadable data |
| Update_Frequency | Periodic (see CEC page) |
| Data_Fields | Vehicle population by fuel type / geography; charger counts by region |
| Data_Definition | Registered light-duty ZEV population and publicly tracked charger counts in California |
| Primary/Secondary | Primary/Secondary mix → `Fact_EV_Market` (population & charging coverage context) |
| Access_Date | 2026-08-02 |
| Reliability_Notes | Good for CA infrastructure vs fleet context; do not claim chargers **caused** sales changes. |
| Limitations | Charger definitions (public vs private, L2 vs DCFC) must follow CEC field defs. |
| Status | Collection URL verified. **MANUAL LOCATE:** specific population and charger download files from the collection/dashboards. |

### SRC-CEC-003 — ZEV and Infrastructure Stats Data file bundle

| Field | Value |
|-------|-------|
| Source_ID | SRC-CEC-003 |
| Dataset_Name | ZEV and Infrastructure Stats Data (CEC file package) |
| Organization | California Energy Commission |
| Source_URL | https://www.energy.ca.gov/files/zev-and-infrastructure-stats-data |
| Publication_Date | **MANUAL LOCATE** from file metadata on the files page (page lists multiple files; ~13.78 MB package observed) |
| Reporting_Period | As stated inside each file |
| File_Format | Mixed downloadable files (verify extensions at download) |
| Update_Frequency | Tied to CEC ZEV stats updates |
| Data_Fields | ZEV sales/population/infrastructure fields as included in package |
| Data_Definition | Packaged download accompanying CEC ZEV & infrastructure statistics |
| Primary/Secondary | Primary (preferred bulk extract if tables match model needs) |
| Access_Date | 2026-08-02 |
| Reliability_Notes | Landing page verified; individual file names/dates must be logged when downloaded. |
| Limitations | Confirm whether manufacturer-level Tesla rows are present before relying on this bundle alone. |
| Status | Landing URL verified. **MANUAL LOCATE:** download each listed file, record filename, bytes, and any embedded “data as of” date. |

---

## DOE Alternative Fuels Data Center (AFDC) / NREL

### SRC-AFDC-001 — Alternative Fuel Stations data download

| Field | Value |
|-------|-------|
| Source_ID | SRC-AFDC-001 |
| Dataset_Name | Alternative Fueling Station Locator — Station Data Download |
| Organization | U.S. Department of Energy — Alternative Fuels Data Center (AFDC) |
| Source_URL | https://afdc.energy.gov/data_download |
| Field format documentation | https://afdc.energy.gov/data_download/alt_fuel_stations_format |
| Publication_Date | “Current” snapshot date = download date; historical snapshots available from 2014 forward per AFDC |
| Reporting_Period | Point-in-time station inventory (or chosen historical snapshot) |
| File_Format | CSV or JSON |
| Update_Frequency | Ongoing |
| Data_Fields | Station ID, fuel type code (`ELEC`), status, city/state/ZIP, lat/long, EVSE level counts, network, open_date, etc. |
| Data_Definition | Directory of alternative fuel stations, including electric vehicle charging locations |
| Primary/Secondary | Primary → `Fact_EV_Market` (Charging_Station_Count aggregations) |
| Access_Date | 2026-08-02 |
| Reliability_Notes | Widely used public station directory. Filter `fuel_type` / electric stations for this project. |
| Limitations | Coverage depends on network reporting; private home chargers largely out of scope. Station counts ≠ utilization. AFDC download form may request contact info — still public data use. |
| Status | Download hub + field docs verified. **MANUAL LOCATE:** export electric stations (current and/or historical) and save under `data/raw/doe_afdc/` with snapshot date in filename. |

### SRC-AFDC-002 — NREL Alternative Fuel Stations API

| Field | Value |
|-------|-------|
| Source_ID | SRC-AFDC-002 |
| Dataset_Name | NREL Alternative Fuel Stations API v1 |
| Organization | NREL / DOE (powers AFDC Station Locator) |
| Source_URL | https://developer.nrel.gov/docs/transportation/alt-fuel-stations-v1/ |
| CSV pattern (docs) | `GET /api/alt-fuel-stations/v1.csv` with query params (e.g., `fuel_type=ELEC`) |
| Publication_Date | Live API; snapshot = extract date |
| Reporting_Period | Point-in-time |
| File_Format | CSV / JSON / GeoJSON |
| Update_Frequency | Ongoing |
| Data_Fields | Same family as SRC-AFDC-001 |
| Data_Definition | Programmatic access to AFDC station database |
| Primary/Secondary | Secondary (automation path); prefer documenting API params used |
| Access_Date | 2026-08-02 |
| Reliability_Notes | **API key required** via NREL developer signup. Store key in gitignored `.env` (e.g., `NREL_API_KEY=...`). Never commit the key. Demo keys exist for trials but are rate-limited. |
| Limitations | Same coverage limits as AFDC download. |
| Status | Docs URL verified. **MANUAL LOCATE:** create free NREL API key when Phase (AFDC extract) starts; add `.env.example` without secrets. |

---

## USGS

### SRC-USGS-001 — Mineral Commodity Summaries (report series)

| Field | Value |
|-------|-------|
| Source_ID | SRC-USGS-001 |
| Dataset_Name | USGS Mineral Commodity Summaries (MCS) |
| Organization | U.S. Geological Survey — National Minerals Information Center |
| Source_URL | https://www.usgs.gov/centers/national-minerals-information-center/mineral-commodity-summaries |
| MCS 2026 publication page | https://pubs.usgs.gov/publication/mcs2026 |
| DOI | https://doi.org/10.3133/mcs2026 |
| Publication_Date | MCS 2026: 2026-02-06 (version history notes later revisions through May 2026 on pubs page) |
| Reporting_Period | Annual; salient statistics typically include a multi-year window ending in the prior calendar year (see each commodity sheet) |
| File_Format | PDF report (+ related data release) |
| Update_Frequency | Annual |
| Data_Fields | For lithium, cobalt, nickel, graphite (and others if added): U.S. production, world production, imports, exports, apparent consumption, unit value/price, major producing countries, net import reliance |
| Data_Definition | Earliest comprehensive USGS government compilation of nonfuel mineral statistics and industry notes |
| Primary/Secondary | Primary → `Fact_Raw_Materials` |
| Access_Date | 2026-08-02 |
| Reliability_Notes | Authoritative public minerals statistics. Some cells are USGS **estimates** within the MCS — preserve USGS footnotes; label as **reported** when published as USGS figures, and note USGS-estimated cells explicitly in the dictionary. |
| Limitations | National/global commodity grain — not Tesla-specific procurement. Do not claim lithium prices caused Tesla margin moves. |
| Status | Hub + MCS 2026 pubs URL verified. **MANUAL LOCATE:** download PDF and commodity sheets for Li, Co, Ni, graphite; prior MCS years if multi-year fact table desired. |

### SRC-USGS-002 — MCS machine-readable data release (CSV)

| Field | Value |
|-------|-------|
| Source_ID | SRC-USGS-002 |
| Dataset_Name | USGS Mineral Commodity Summaries Data Release (CSV entities) |
| Organization | U.S. Geological Survey |
| Source_URL | https://www.usgs.gov/centers/national-minerals-information-center/data |
| MCS 2025 data release (example catalog item) | https://www.sciencebase.gov/catalog/item/677eaf95d34e760b392c4970 |
| MCS 2025 data release landing (USGS) | https://www.usgs.gov/data/us-geological-survey-mineral-commodity-summaries-2025-data-release-ver-20-april-2025 |
| Publication_Date | Per release version (e.g., MCS 2025 data release ver. 2.0, April 2025) |
| Reporting_Period | Annual salient statistics / world production tables |
| File_Format | CSV (zipped packages) |
| Update_Frequency | Annual (versioned data releases) |
| Data_Fields | Production, imports, exports, apparent consumption, price/unit value, net import reliance, world production by country (as provided in entities) |
| Data_Definition | Tabular database companion to MCS narrative/PDF |
| Primary/Secondary | Primary (preferred for reproducible loads) |
| Access_Date | 2026-08-02 |
| Reliability_Notes | Use CSV entities when available for auditability; cross-check against PDF commodity sheets. |
| Limitations | Commodity naming and unit conventions must be normalized in Dim_Commodity. |
| Status | Data & Tools hub + 2025 ScienceBase item verified. **MANUAL LOCATE:** MCS 2026 data release ZIP link from the MCS 2026 page (“Data release for Mineral Commodity Summaries 2026”) and confirm lithium/cobalt/nickel/graphite tables. |

### SRC-USGS-003 — Individual commodity information pages

| Field | Value |
|-------|-------|
| Source_ID | SRC-USGS-003 |
| Dataset_Name | USGS Commodity Statistics and Information pages (Li, Co, Ni, Graphite) |
| Organization | USGS NMIC |
| Source_URL | https://www.usgs.gov/centers/national-minerals-information-center/commodity-statistics-and-information |
| Publication_Date | Per linked MCS sheet / yearbook |
| Reporting_Period | Annual |
| File_Format | HTML + PDF sheets |
| Update_Frequency | Annual / as updated |
| Data_Fields | Commodity-specific salient statistics |
| Data_Definition | Commodity landing pages linking to MCS and historical stats |
| Primary/Secondary | Secondary navigation aid |
| Access_Date | 2026-08-02 |
| Reliability_Notes | Use to find commodity-specific PDFs if bulk release lacks a field. |
| Limitations | Pages are indexes; cite the underlying MCS/yearbook table ultimately used. |
| Status | Hub URL pattern verified via USGS NMIC. **MANUAL LOCATE:** exact lithium, cobalt, nickel, and graphite page URLs + year-specific PDF filenames when extracting. |

---

## Inventory summary

| Source_ID | Organization | Maps to | Status |
|-----------|--------------|---------|--------|
| SRC-TESLA-IR-001 | Tesla IR | Fact_Tesla_Operations | Hub + examples verified; historical series MANUAL LOCATE |
| SRC-TESLA-IR-002 | Tesla IR | Context / cross-check | Example deck verified; archive set MANUAL LOCATE |
| SRC-SEC-001 / 002* | SEC EDGAR | Fact_Financials | Index + seed filings verified; full period set MANUAL LOCATE |
| SRC-NHTSA-001 | NHTSA | Fact_Recalls | Hub verified; ZIP selection MANUAL LOCATE |
| SRC-NHTSA-002 | NHTSA | Fact_Complaints | Hub verified; large ZIP MANUAL LOCATE |
| SRC-NHTSA-003 | NHTSA | Recalls/Complaints alternate | API docs verified; model spellings MANUAL LOCATE |
| SRC-CEC-001/002/003 | CEC | Fact_EV_Market | Pages verified; export files MANUAL LOCATE |
| SRC-AFDC-001/002 | DOE AFDC / NREL | Fact_EV_Market (chargers) | Hub/docs verified; snapshot + API key MANUAL LOCATE |
| SRC-USGS-001/002/003 | USGS | Fact_Raw_Materials | MCS hubs verified; commodity CSV/PDF extract MANUAL LOCATE |

---

## Manual action checklist (for you before data-load phases)

1. **Tesla IR:** DONE for Q1 2022–Q2 2026 — see `data/raw/tesla_ir/` and `data/reference/download_log.md`.
2. **SEC:** DONE for report dates 2022-03-31–2026-06-30 — local files in `data/raw/sec_edgar/` (gitignored); URLs in download log.
3. **NHTSA:** From https://www.nhtsa.gov/nhtsa-datasets-and-apis, download chosen recall/complaint ZIPs into `data/raw/nhtsa/` (do not commit large files).
4. **CEC:** Open https://www.energy.ca.gov/files/zev-and-infrastructure-stats-data and the New ZEV Sales dashboard; download tables and log data-as-of dates into `data/raw/cec/`.
5. **AFDC:** Use https://afdc.energy.gov/data_download for electric stations; if using API, create NREL key and local `.env`.
6. **USGS:** Download MCS PDF + CSV data release for target years into `data/raw/usgs/`; confirm lithium, cobalt, nickel, graphite fields.

No numeric fact values are recorded in this inventory yet — by design — until raw files are downloaded and extracted with citations.
