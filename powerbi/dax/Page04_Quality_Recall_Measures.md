# Page 4 — DAX Measures (Quality & Recall Risk)

**Model tables:** `Fact_Recalls`, `Fact_NHTSA_Annual`, `Fact_Complaints`, `Fact_NHTSA_By_Model`  
**Recall source:** NHTSA ODI flat files (`SRC-NHTSA-001`) — `FLAT_RCL_PRE_2010.zip` / `FLAT_RCL_POST_2010.zip`  
**Complaint source:** NHTSA ODI complaints flat file (`SRC-NHTSA-002`) — `FLAT_CMPL.zip`  
**Status:** Reference documentation only — analytical logic for the HTML dashboard.

## Citation discipline (required)

| Tooltip field | Source |
|---------------|--------|
| Value | measure |
| Metric label | Reported / Calculated |
| Snapshot date | `Snapshot_Date` |
| Source ID | `SRC-NHTSA-001` (recalls) / `SRC-NHTSA-002` (complaints) |
| Source file / URL | `Source_Zip` / `Source_URL` |

**Hard rules for narrative:**
- Complaints are **allegations**, not confirmed defects.
- Complaint grain is **distinct ODINO** (component rows collapsed).
- `Potential_Units_Affected` (POTAFF) is potential population reported to NHTSA — **not** completed repairs.
- Do not infer supplier causation from component free text.
- Do not compute “defect rates” without a verified vehicles-in-operation denominator.
- Do **not** use `SRC-NHTSA-003` vehicle APIs for Page 4 KPIs (API path omitted POTAFF on recalls and under-counted Roadster complaints vs flat file).

---

## Recall KPIs (flat-file)

```dax
Recall Campaign Count =
SUM ( Fact_NHTSA_Annual[Recall_Campaign_Count] )
-- Metric label: Reported
```

```dax
Potential Units Affected =
SUM ( Fact_NHTSA_Annual[Potential_Units_Affected_Sum] )
-- Metric label: Reported
-- max POTAFF per campaign, then sum within year — not repairs completed
```

---

## Complaint KPIs (FLAT_CMPL)

```dax
Complaint Count =
DISTINCTCOUNT ( Fact_Complaints[ODI_Number] )
-- Metric label: Reported (allegations)
-- Equivalent to SUM of annual rollup Complaint_Count
```

```dax
Crash Flagged Complaints =
CALCULATE (
    DISTINCTCOUNT ( Fact_Complaints[ODI_Number] ),
    Fact_Complaints[Crash] = 1
)
```

```dax
Crash Share of Complaints =
DIVIDE ( [Crash Flagged Complaints], [Complaint Count] )
-- Metric label: Calculated
```
