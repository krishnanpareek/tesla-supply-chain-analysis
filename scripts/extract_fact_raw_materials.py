"""Build Fact_Raw_Materials from USGS MCS 2026 commodities CSV."""
from __future__ import annotations

import csv
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "usgs" / "MCS2026_Commodities_Data.csv"
OUT = ROOT / "data" / "processed" / "Fact_Raw_Materials.csv"
LOG = ROOT / "data" / "reference" / "Fact_Raw_Materials_extraction_log.csv"

COMMODITIES = {"Lithium", "Cobalt", "Nickel", "Graphite (Natural)"}
SOURCE_ID = "SRC-USGS-002"  # ScienceBase MCS 2026 commodities CSV (PDF chapters = SRC-USGS-001)
SOURCE_URL = (
    "https://www.sciencebase.gov/catalog/item/69837e43b66b01367d7ec7c7"
)
SOURCE_FILE = "MCS2026_Commodities_Data.csv"
PUBLICATION_DATE = "2026-02-06"


def main() -> None:
    text = RAW.read_bytes()
    for enc in ("utf-8-sig", "cp1252", "latin-1"):
        try:
            rows = list(csv.DictReader(text.decode(enc).splitlines()))
            break
        except UnicodeDecodeError:
            continue
    else:
        raise RuntimeError("Unable to decode MCS CSV")
    kept = [r for r in rows if (r.get("Commodity") or "") in COMMODITIES]
    out = []
    log = []
    for r in kept:
        year = (r.get("Year") or "").strip()
        val = (r.get("Value") or "").strip()
        notes = (r.get("Notes") or "").strip()
        # USGS MCS marks preliminary/estimated cells in Notes (e.g. "Estimated.")
        metric_label = "estimated" if "estimated" in notes.lower() else "reported"
        num = None
        if val not in ("", "NA", "N/A", "W", "—", "-"):
            try:
                num = float(val.replace(",", ""))
            except ValueError:
                num = None
        row = {
            "Commodity": r.get("Commodity"),
            "Country": r.get("Country"),
            "Section": r.get("Section"),
            "Statistics": r.get("Statistics"),
            "Statistics_Detail": r.get("Statistics_detail"),
            "Unit": r.get("Unit"),
            "Year": int(year) if year.isdigit() else year,
            "Value": num if num is not None else val,
            "Value_Numeric": num,
            "Notes": notes,
            "Is_Critical_Mineral_2025": r.get("Is critical mineral 2025"),
            "Source_File": SOURCE_FILE,
            "Source_ID": SOURCE_ID,
            "Source_URL": SOURCE_URL,
            "Publication_Date": PUBLICATION_DATE,
            "Snapshot_Date": date.today().isoformat(),
            "Metric_Label": metric_label,
            "DOI": "https://doi.org/10.5066/P1WKQ63T",
        }
        out.append(row)
        log.append(
            {
                "Commodity": row["Commodity"],
                "Country": row["Country"],
                "Statistics": row["Statistics"],
                "Year": row["Year"],
                "Field_Value": row["Value"],
                "Metric_Label": metric_label,
                "Source_File": SOURCE_FILE,
                "Source_URL": SOURCE_URL,
                "Notes": row["Notes"],
            }
        )

    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)
    with LOG.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(log[0].keys()))
        w.writeheader()
        w.writerows(log)

    # KPI-friendly pivot subset: US net import reliance + world production leaders
    print(f"Wrote {len(out)} rows -> {OUT}")
    for c in sorted(COMMODITIES):
        n = sum(1 for r in out if r["Commodity"] == c)
        print(f"  {c}: {n}")


if __name__ == "__main__":
    main()
