# Page 4 — Quality & Recall Risk

**Deliverable:** `dashboard/page04_quality_recall_risk.html`  
**Facts:** `Fact_Recalls` + `Fact_NHTSA_Annual` (SRC-NHTSA-001); `Fact_Complaints` (SRC-NHTSA-002)  
**DAX reference:** `powerbi/dax/Page04_Quality_Recall_Measures.md`  
**Extracts:** `scripts/extract_fact_recalls_flat.py`; `scripts/extract_fact_complaints_flat.py`

## Purpose

Surface Tesla-related NHTSA recall campaign activity with populated POTAFF, plus consumer complaint volume from the **complaints flat file** (not the vehicle API).

## Layout

1. Focus year + table mode + snapshot / source pills  
2. KPIs: Campaigns, Potential units affected, Complaints, Crash share  
3. Charts: campaigns, POTAFF, complaints, crash share, by-model  
4. Campaigns table (focus-year or 25 most recent) with POTAFF + Source_Zip  
5. Callouts: POTAFF ≠ repairs; complaints ≠ defects; Roadster included in both domains

## Notes

- Recalls: `MAKETXT=TESLA` from pre/post-2010 RCL flat files.  
- Complaints: `MAKETXT=TESLA` from `FLAT_CMPL.zip`; fact grain = distinct **ODINO**.  
- Roadster complaints: verify against flat file (`ROADSTER` / `ROADSTER2`) — API snapshot previously under-counted (0).  
- Do not treat rising complaints as defect incidence without fleet denominator.
