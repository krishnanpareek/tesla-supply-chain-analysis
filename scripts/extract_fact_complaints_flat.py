"""
Build Fact_Complaints from NHTSA ODI complaints flat file (SRC-NHTSA-002).

Primary input (local, large, gitignored):
  data/raw/nhtsa/FLAT_CMPL.zip

Filter: MAKETXT == TESLA (case-insensitive).
Grain: one row per ODINO (complaint case). Component rows for the same ODINO
are collapsed; Crash/Fire are Y if any component row is Y.
Complaint counts on dashboards must use distinct ODINO — not raw CMPLID rows.
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

ZIP_NAME = "FLAT_CMPL.zip"
ZIP_URL = "https://static.nhtsa.gov/odi/ffdd/cmpl/FLAT_CMPL.zip"
DICT_NAME = "CMPL.txt"
DICT_URL = "https://static.nhtsa.gov/odi/ffdd/cmpl/CMPL.txt"

# Field positions from CMPL.txt (1-indexed in docs → 0-indexed here)
F = {
    "CMPLID": 0,
    "ODINO": 1,
    "MFR_NAME": 2,
    "MAKETXT": 3,
    "MODELTXT": 4,
    "YEARTXT": 5,
    "CRASH": 6,
    "FAILDATE": 7,
    "FIRE": 8,
    "INJURED": 9,
    "DEATHS": 10,
    "COMPDESC": 11,
    "DATEA": 15,
    "LDATE": 16,
    "CDESCR": 19,
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


def yn_to_flag(s: str) -> int:
    return 1 if (s or "").strip().upper() == "Y" else 0


def iter_tesla_rows(zip_path: Path):
    with zipfile.ZipFile(zip_path) as zf:
        # Prefer FLAT_CMPL.txt if present
        names = zf.namelist()
        name = next((n for n in names if n.upper().endswith(".TXT")), names[0])
        with zf.open(name) as fh:
            for raw in fh:
                line = raw.decode("latin-1", errors="replace").rstrip("\n").rstrip("\r")
                if not line:
                    continue
                parts = line.split("\t")
                if len(parts) < 20:
                    parts.extend([""] * (20 - len(parts)))
                make = (parts[F["MAKETXT"]] or "").strip().upper()
                if make != "TESLA":
                    continue
                yield name, parts


def main() -> None:
    snap = date.today().isoformat()
    zip_path = RAW / ZIP_NAME
    if not zip_path.exists():
        raise FileNotFoundError(f"Missing {zip_path}; download from {ZIP_URL}")

    PROC.mkdir(parents=True, exist_ok=True)
    REF.mkdir(parents=True, exist_ok=True)

    # Aggregate component-level flat rows to ODINO grain
    by_odi: dict[str, dict] = {}
    component_rows = 0
    model_counter = Counter()

    for txt_name, parts in iter_tesla_rows(zip_path):
        component_rows += 1
        odi = (parts[F["ODINO"]] or "").strip()
        if not odi:
            continue
        model = (parts[F["MODELTXT"]] or "").strip()
        year = parse_int(parts[F["YEARTXT"]])
        if year == 9999:
            year = None
        crash = yn_to_flag(parts[F["CRASH"]])
        fire = yn_to_flag(parts[F["FIRE"]])
        injured = parse_int(parts[F["INJURED"]]) or 0
        deaths = parse_int(parts[F["DEATHS"]]) or 0
        comp = (parts[F["COMPDESC"]] or "").strip()
        ldate = parse_ymd(parts[F["LDATE"]])
        fail = parse_ymd(parts[F["FAILDATE"]])
        cmplid = (parts[F["CMPLID"]] or "").strip()

        if odi not in by_odi:
            by_odi[odi] = {
                "ODI_Number": odi,
                "Make": "TESLA",
                "Model": model,
                "Model_Year": year,
                "Components": set([comp]) if comp else set(),
                "Crash": crash,
                "Fire": fire,
                "Injured": injured,
                "Deaths": deaths,
                "Date_Complaint_Filed": ldate,
                "Date_Incident": fail,
                "CMPLID_Primary": cmplid,
                "Component_Row_Count": 1,
                "Source_File": f"{ZIP_NAME}::{txt_name}",
                "Source_Zip": ZIP_NAME,
                "Source_URL": ZIP_URL,
                "Source_ID": "SRC-NHTSA-002",
                "Dictionary_File": DICT_NAME,
                "Snapshot_Date": snap,
                "Metric_Label": "reported",
                "Notes": (
                    "Allegation filed with NHTSA; not a confirmed defect. "
                    "ODINO grain — multiple CMPLID/component rows collapsed."
                ),
            }
        else:
            d = by_odi[odi]
            d["Component_Row_Count"] += 1
            if comp:
                d["Components"].add(comp)
            d["Crash"] = max(d["Crash"], crash)
            d["Fire"] = max(d["Fire"], fire)
            d["Injured"] = max(d["Injured"], injured)
            d["Deaths"] = max(d["Deaths"], deaths)
            # Prefer earliest received date if multiple
            if ldate and (
                not d["Date_Complaint_Filed"] or ldate < d["Date_Complaint_Filed"]
            ):
                d["Date_Complaint_Filed"] = ldate
            if not d["Model"] and model:
                d["Model"] = model
            if d["Model_Year"] is None and year is not None:
                d["Model_Year"] = year

    rows = []
    for odi, d in by_odi.items():
        comps = sorted(c for c in d["Components"] if c)
        model = d["Model"]
        model_counter[model.upper() if model else "(blank)"] += 1
        rows.append(
            {
                "ODI_Number": d["ODI_Number"],
                "Make": d["Make"],
                "Model": model,
                "Model_Year": d["Model_Year"],
                "Component": ", ".join(comps),
                "Crash": d["Crash"],
                "Fire": d["Fire"],
                "Injured": d["Injured"],
                "Deaths": d["Deaths"],
                "Date_Complaint_Filed": d["Date_Complaint_Filed"],
                "Date_Incident": d["Date_Incident"],
                "Component_Row_Count": d["Component_Row_Count"],
                "CMPLID_Primary": d["CMPLID_Primary"],
                "Source_File": d["Source_File"],
                "Source_Zip": d["Source_Zip"],
                "Source_URL": d["Source_URL"],
                "Source_ID": d["Source_ID"],
                "Dictionary_File": d["Dictionary_File"],
                "Snapshot_Date": d["Snapshot_Date"],
                "Metric_Label": d["Metric_Label"],
                "Notes": d["Notes"],
            }
        )

    rows.sort(
        key=lambda r: (
            r["Date_Complaint_Filed"] or "",
            r["ODI_Number"],
        )
    )

    out_path = PROC / "Fact_Complaints.csv"
    fields = list(rows[0].keys()) if rows else []
    with out_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    log_path = REF / "Fact_Complaints_extraction_log.csv"
    with log_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "ODI_Number",
                "Model",
                "Model_Year",
                "Date_Complaint_Filed",
                "Crash",
                "Fire",
                "Field_Value_Note",
                "Metric_Label",
                "Source_File",
                "Source_URL",
                "Source_ID",
            ],
        )
        w.writeheader()
        for r in rows:
            w.writerow(
                {
                    "ODI_Number": r["ODI_Number"],
                    "Model": r["Model"],
                    "Model_Year": r["Model_Year"],
                    "Date_Complaint_Filed": r["Date_Complaint_Filed"],
                    "Crash": r["Crash"],
                    "Fire": r["Fire"],
                    "Field_Value_Note": "ODINO-level allegation; components collapsed",
                    "Metric_Label": "reported",
                    "Source_File": r["Source_File"],
                    "Source_URL": r["Source_URL"],
                    "Source_ID": "SRC-NHTSA-002",
                }
            )

    # Roadster verification (do not assume API zero)
    roadster_odi = [
        r
        for r in rows
        if "ROADSTER" in (r.get("Model") or "").upper()
    ]
    roadster_models = Counter((r.get("Model") or "") for r in roadster_odi)

    print(f"Component-level Tesla rows scanned: {component_rows}")
    print(f"Distinct ODINO (Fact_Complaints rows): {len(rows)} -> {out_path}")
    print(f"Extraction log: {log_path}")
    print("Top models by distinct ODINO:")
    for m, n in model_counter.most_common(12):
        print(f"  {m}: {n}")
    print("--- Roadster verification (flat file) ---")
    print(f"Distinct ODINO with MODELTXT containing ROADSTER: {len(roadster_odi)}")
    for m, n in roadster_models.most_common():
        print(f"  model label {m!r}: {n}")
    if roadster_odi:
        for r in roadster_odi[:10]:
            print(
                f"  ODINO={r['ODI_Number']} year={r['Model_Year']} "
                f"filed={r['Date_Complaint_Filed']} crash={r['Crash']} "
                f"comp={r['Component'][:60]!r}"
            )
    else:
        print("  No Roadster ODINO rows found in FLAT_CMPL Tesla extract.")


if __name__ == "__main__":
    main()
