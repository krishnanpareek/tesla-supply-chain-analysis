# Limitations

This project uses **public data only**. It does not claim access to Tesla internal systems, supplier contracts, confidential factory data, dealer inventory feeds, or non-public cell / materials procurement.

## Standing constraints

1. **No Tesla-confidential access.** All figures come from Tesla IR / SEC filings, NHTSA public ODI datasets, CEC downloads, and USGS MCS releases.
2. **Production–delivery gap ≠ unsold inventory.** Gap = produced − delivered for the reported vehicle group and quarter. It can reflect transit timing, logistics, demand, shutdowns, mix, or reporting cutoffs.
3. **Balance-sheet inventory ≠ vehicle units.** SEC inventory is consolidated dollars, not finished-vehicle counts by model or factory.
4. **Inventory days are estimated.** Days-on-hand style metrics are derived proxies from reported financials, not Tesla’s internal DOH.
5. **California ZEV sales ≠ national deliveries.** CEC new ZEV sales are registration-based California statistics. Do not equate to Tesla’s global delivery total.
6. **CEC methodology changes.** ZEV sales inference from DMV registrations was updated in 2023 and 2025; long YoY spans need care. Prefer the export *Data as of* date over contemporaneous press totals when they diverge.
7. **Charging ports ≠ stations; public ≠ all sectors.** Page 5 headlines **public** charging **ports**. CEC workbook `Total` also includes shared-private ports (workplaces / multi-family / fleets) and excludes residential. Mislabeling the all-sectors total as “public chargers” roughly doubles the public figure.
8. **NHTSA complaints are allegations.** Distinct ODINO counts from FLAT_CMPL are consumer complaints, not confirmed defect rates or injury incidence.
9. **NHTSA API vs flat files.** Vehicle APIs can under-count relative to ODI flat files (especially low-volume models such as Roadster). This project treats flat files as authoritative for recalls/complaints extracts.
10. **Recall POTAFF ≠ repairs completed.** Potential units affected are campaign exposure figures (max POTAFF per campaign in rollups), not completion rates.
11. **USGS mineral statistics are market structure, not Tesla purchasing.** Production and import reliance do not identify Tesla’s suppliers, contract volumes, or chemistry mix.
12. **Many USGS 2025 cells are estimated.** `Metric_Label=estimated` when USGS Notes contain “Estimated.” Do not present 2025 world mine production or U.S. net import reliance as final reported actuals.
13. **Correlation ≠ causation.** Narrative insights use qualified language; public time series alone cannot prove why a gap, margin, or complaint spike occurred.
14. **Missing values stay null.** No silent interpolation of undisclosed energy storage, withheld (“W”) mineral cells, or absent quarters.
15. **Dashboard technology scope.** The live deliverable is HTML / CSS / JavaScript. In-repo `powerbi/dax/` files document measure logic for reviewers; they are not an executed Power BI model and should not be cited as Power BI project experience.

## What this project can support in interviews

- Traceability from KPI → fact row → source file / URL / date  
- Clear metric labels and definitional guardrails  
- Reproducible extracts (Python scripts + processed CSVs)  
- Cross-domain supply-chain framing (ops, finance, quality, market, materials)

## What this project cannot answer

- Which suppliers Tesla uses for cells or cathode materials  
- Factory-level bottleneck root cause  
- True finished-goods inventory by SKU or region  
- Warranty cost true-ups beyond public disclosures  
- Real-time charger uptime or Tesla Supercharger-only network stats (CEC is broader public/shared infrastructure reporting)
