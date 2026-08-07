"""
Build Fact_Recalls from NHTSA ODI recalls flat files (SRC-NHTSA-001).

Primary inputs (local, gitignored ZIPs):
  data/raw/nhtsa/FLAT_RCL_PRE_2010.zip
  data/raw/nhtsa/FLAT_RCL_POST_2010.zip

Filter: MAKETXT == TESLA (case-insensitive).
POTAFF -> Potential_Units_Affected (reported potential units, not repairs completed).
"""
from __future__ import annotations

import csv
import zipfile
from collections import Counter, defaultdict
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "nhtsa"
PROC = ROOT / "data" / "processed"
REF = ROOT / "data" / "reference"

ZIPS = [
    ("FLAT_RCL_PRE_2010.zip", "https://static.nhtsa.gov/odi/ffdd/rcl/FLAT_RCL_PRE_2010.zip"),
    ("FLAT_RCL_POST_2010.zip", "https://static.nhtsa.gov/odi/ffdd/rcl/FLAT_RCL_POST_2010.zip"),
]

# Field positions from RCL.txt (1-indexed in docs → 0-indexed here)
F = {
    "RECORD_ID": 0,
    "CAMPNO": 1,
    "MAKETXT": 2,
    "MODELTXT": 3,
    "YEARTXT": 4,
    "MFGCAMPNO": 5,
    "COMPNAME": 6,
    "MFGNAME": 7,
    "RCLTYPECD": 10,
    "POTAFF": 11,
    "ODATE": 12,
    "INFLUENCED_BY": 13,
    "RCDATE": 15,
    "DESC_DEFECT": 19,
    "CONEQUENCE_DEFECT": 20,
    "CORRECTIVE_ACTION": 21,
    "NOTES": 22,
    "DO_NOT_DRIVE": 27,
    "PARK_OUTSIDE": 28,
}


def parse_ymd(s: str) -> str | None:
    s = (s or "").strip()
    if len(s) != 8 or not s.isdigit():
        return None
    try:
        return datetime.strptime(s, "%Y%m%d").date().isoformat()
    except ValueError:
        return None


def parse_int(s: str) -> int | None:
    s = (s or "").strip().replace(",", "")
    if not s:
        return None
    try:
        return int(float(s))
    except ValueError:
        return None


def iter_tesla_rows(zip_path: Path):
    with zipfile.ZipFile(zip_path) as zf:
        name = zf.namelist()[0]
        with zf.open(name) as fh:
            for raw in fh:
                line = raw.decode("latin-1", errors="replace").rstrip("\n").rstrip("\r")
                if not line:
                    continue
                parts = line.split("\t")
                # Pad short rows (older schema may lack trailing fields)
                if len(parts) < 23:
                    parts.extend([""] * (23 - len(parts)))
                make = (parts[F["MAKETXT"]] or "").strip().upper()
                if make != "TESLA":
                    continue
                yield name, parts


def main() -> None:
    snap = date.today().isoformat()
    PROC.mkdir(parents=True, exist_ok=True)
    REF.mkdir(parents=True, exist_ok=True)

    rows = []
    events = []
    source_counts = Counter()

    for zip_name, url in ZIPS:
        path = RAW / zip_name
        if not path.exists():
            raise FileNotFoundError(f"Missing {path}; download from {url}")
        for txt_name, parts in iter_tesla_rows(path):
            camp = (parts[F["CAMPNO"]] or "").strip()
            model = (parts[F["MODELTXT"]] or "").strip()
            year_s = (parts[F["YEARTXT"]] or "").strip()
            year = parse_int(year_s)
            potaff = parse_int(parts[F["POTAFF"]])
            rcdate = parse_ymd(parts[F["RCDATE"]])
            source_file = f"{zip_name}::{txt_name}"
            source_counts[zip_name] += 1
            row = {
                "Record_ID": parse_int(parts[F["RECORD_ID"]]),
                "Campaign_Number": camp,
                "Make": "TESLA",
                "Model": model,
                "Model_Year": year if year != 9999 else None,
                "Component": (parts[F["COMPNAME"]] or "").strip(),
                "Manufacturer_Campaign_Number": (parts[F["MFGCAMPNO"]] or "").strip(),
                "Recall_Type_Code": (parts[F["RCLTYPECD"]] or "").strip(),
                "Potential_Units_Affected": potaff,
                "Owner_Notify_Date": parse_ymd(parts[F["ODATE"]]),
                "Report_Received_Date": rcdate,
                "Influenced_By": (parts[F["INFLUENCED_BY"]] or "").strip(),
                "Summary": (parts[F["DESC_DEFECT"]] or "").strip().replace("\n", " ")[:4000],
                "Consequence": (parts[F["CONEQUENCE_DEFECT"]] or "").strip().replace("\n", " ")[:2000],
                "Remedy": (parts[F["CORRECTIVE_ACTION"]] or "").strip().replace("\n", " ")[:4000],
                "Notes": (parts[F["NOTES"]] or "").strip().replace("\n", " ")[:2000],
                "Do_Not_Drive": (parts[F["DO_NOT_DRIVE"]] if len(parts) > F["DO_NOT_DRIVE"] else "").strip(),
                "Park_Outside": (parts[F["PARK_OUTSIDE"]] if len(parts) > F["PARK_OUTSIDE"] else "").strip(),
                "Source_File": source_file,
                "Source_Zip": zip_name,
                "Source_URL": url,
                "Source_ID": "SRC-NHTSA-001",
                "Dictionary_File": "RCL.txt",
                "Snapshot_Date": snap,
                "Metric_Label": "reported",
                "Units_Note": "POTAFF = potential units affected as reported to NHTSA; not confirmed repairs completed",
            }
            rows.append(row)
            events.append(
                {
                    "Campaign_Number": camp,
                    "Model": model,
                    "Model_Year": year,
                    "Field_Name": "Potential_Units_Affected",
                    "Field_Value": potaff,
                    "Metric_Label": "reported",
                    "Source_File": source_file,
                    "Source_URL": url,
                    "Notes": "Flat-file field POTAFF",
                }
            )

    rows.sort(
        key=lambda r: (
            r["Report_Received_Date"] or "",
            r["Campaign_Number"] or "",
            r["Model"] or "",
            r["Model_Year"] or 0,
        )
    )

    out_path = PROC / "Fact_Recalls.csv"
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    with (REF / "Fact_Recalls_extraction_log.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(events[0].keys()))
        w.writeheader()
        w.writerows(events)

    # Campaign-level and model checks
    camps = {r["Campaign_Number"] for r in rows}
    null_units = sum(1 for r in rows if r["Potential_Units_Affected"] is None)
    models = Counter(r["Model"].upper() for r in rows)
    roadster = [r for r in rows if "ROADSTER" in (r["Model"] or "").upper()]
    m3_2024 = [r for r in rows if (r["Model"] or "").upper() in ("MODEL 3", "MODEL3") and r["Model_Year"] == 2024]

    print(f"Wrote {len(rows)} Tesla rows -> {out_path}")
    print(f"Distinct campaigns: {len(camps)}")
    print(f"Null POTAFF rows: {null_units}")
    print(f"By zip: {dict(source_counts)}")
    print(f"Model counts: {dict(models)}")
    print(f"ROADSTER rows: {len(roadster)}")
    print(f"ROADSTER distinct campaigns: {len({r['Campaign_Number'] for r in roadster})}")
    if roadster:
        for r in sorted(roadster, key=lambda x: x["Report_Received_Date"] or "")[:10]:
            print(
                f"  {r['Campaign_Number']} {r['Report_Received_Date']} "
                f"year={r['Model_Year']} units={r['Potential_Units_Affected']} "
                f"{(r['Component'] or '')[:50]}"
            )
    print(f"MODEL 3 2024 rows: {len(m3_2024)}")
    print(f"MODEL 3 2024 campaigns: {len({r['Campaign_Number'] for r in m3_2024})}")

    # Rebuild annual aggregate from flat file
    camp_meta = {}
    for r in rows:
        c = r["Campaign_Number"]
        u = r["Potential_Units_Affected"] or 0
        d = r["Report_Received_Date"] or ""
        if c not in camp_meta:
            camp_meta[c] = {"date": d, "units": u}
        else:
            camp_meta[c]["units"] = max(camp_meta[c]["units"], u)
            if d and (not camp_meta[c]["date"] or d < camp_meta[c]["date"]):
                camp_meta[c]["date"] = d

    by_year = defaultdict(lambda: {"camps": set(), "units": 0})
    for c, meta in camp_meta.items():
        y = (meta["date"] or "")[:4]
        if not y:
            continue
        by_year[y]["camps"].add(c)
        by_year[y]["units"] += meta["units"]

    annual = []
    for y in sorted(by_year.keys()):
        annual.append(
            {
                "Year": int(y),
                "Recall_Campaign_Count": len(by_year[y]["camps"]),
                "Potential_Units_Affected_Sum": by_year[y]["units"],
                "Source_ID": "SRC-NHTSA-001",
                "Snapshot_Date": snap,
                "Metric_Label": "reported",
                "Notes": "Campaigns attributed to earliest Report_Received_Date year; units = max POTAFF per campaign",
            }
        )
    with (PROC / "Fact_NHTSA_Annual.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(annual[0].keys()) if annual else ["Year"])
        w.writeheader()
        w.writerows(annual)
    print(f"Annual years: {len(annual)}")


if __name__ == "__main__":
    main()
