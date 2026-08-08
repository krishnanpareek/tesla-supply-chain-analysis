"""Build dashboard/data/*.js embeds from processed CSVs."""
from __future__ import annotations

import csv
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dashboard" / "data"

# Integers / plain decimals only — never coerce NHTSA IDs like 22E092000 via float().
_NUM_RE = re.compile(r"^-?\d+(?:\.\d+)?$")


def coerce_value(v: str):
    if v is None or v == "":
        return None
    if _NUM_RE.fullmatch(v):
        # Prefer int when the string is a whole number (years, counts, POTAFF).
        if "." not in v:
            return int(v)
        return float(v)
    return v


def load_csv(path: Path) -> list[dict]:
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    out = []
    for r in rows:
        o = {k: coerce_value(v) if isinstance(v, str) else v for k, v in r.items()}
        out.append(o)
    return out


def write_js(name: str, global_name: str, rows: list[dict]) -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / f"{name}.js").write_text(
        f"window.{global_name} = {json.dumps(rows)};\n",
        encoding="utf-8",
    )
    (OUT / f"{name}.json").write_text(json.dumps(rows, indent=2), encoding="utf-8")
    print(f"Wrote {len(rows)} rows -> {OUT / (name + '.js')}")


def campaign_summaries(rows: list[dict]) -> list[dict]:
    """One row per Campaign_Number from Fact_Recalls flat-file extract."""
    by_c: dict[str, dict] = {}
    for r in rows:
        c = r.get("Campaign_Number")
        if not c:
            continue
        units = r.get("Potential_Units_Affected")
        try:
            units_n = float(units) if units is not None else None
        except (TypeError, ValueError):
            units_n = None
        if c not in by_c:
            by_c[c] = {
                "Campaign_Number": c,
                "Models": {str(r.get("Model") or "")},
                "Model_Years": set(),
                "Component": r.get("Component"),
                "Potential_Units_Affected": units_n,
                "Owner_Notify_Date": r.get("Owner_Notify_Date"),
                "Report_Received_Date": r.get("Report_Received_Date"),
                "Influenced_By": r.get("Influenced_By"),
                "Summary": r.get("Summary"),
                "Consequence": r.get("Consequence"),
                "Remedy": r.get("Remedy"),
                "Do_Not_Drive": r.get("Do_Not_Drive"),
                "Park_Outside": r.get("Park_Outside"),
                "Source_File": r.get("Source_File"),
                "Source_Zip": r.get("Source_Zip"),
                "Source_URL": r.get("Source_URL"),
                "Source_ID": r.get("Source_ID"),
                "Dictionary_File": r.get("Dictionary_File"),
                "Snapshot_Date": r.get("Snapshot_Date"),
                "Metric_Label": r.get("Metric_Label") or "reported",
                "Units_Note": r.get("Units_Note"),
                "Row_Count": 1,
            }
            my = r.get("Model_Year")
            if my is not None:
                by_c[c]["Model_Years"].add(str(int(my)) if isinstance(my, float) else str(my))
        else:
            by_c[c]["Models"].add(str(r.get("Model") or ""))
            my = r.get("Model_Year")
            if my is not None:
                by_c[c]["Model_Years"].add(str(int(my)) if isinstance(my, float) else str(my))
            by_c[c]["Row_Count"] += 1
            if units_n is not None:
                prev = by_c[c]["Potential_Units_Affected"]
                if prev is None or units_n > prev:
                    by_c[c]["Potential_Units_Affected"] = units_n
            # Prefer non-empty component / summary if later rows fill gaps
            if not by_c[c]["Component"] and r.get("Component"):
                by_c[c]["Component"] = r.get("Component")
            if not by_c[c]["Summary"] and r.get("Summary"):
                by_c[c]["Summary"] = r.get("Summary")

    out = []
    for c, d in by_c.items():
        models = sorted(m for m in d["Models"] if m)
        years = sorted(d["Model_Years"])
        out.append(
            {
                **{k: v for k, v in d.items() if k not in ("Models", "Model_Years")},
                "Models": ", ".join(models),
                "Model_Year_Span": f"{years[0]}-{years[-1]}" if years else None,
            }
        )
    out.sort(key=lambda x: x.get("Report_Received_Date") or "", reverse=True)
    return out


def model_rollups(recall_rows: list[dict], complaint_rows: list[dict]) -> list[dict]:
    """Campaign counts from flat-file recalls; complaint counts from complaints extract."""
    camp_by_model: dict[str, set[str]] = defaultdict(set)
    for r in recall_rows:
        model = (r.get("Model") or "").strip().upper()
        if not model:
            continue
        # Normalize Roadster variants
        if model.startswith("ROADSTER"):
            model = "ROADSTER"
        camp_by_model[model].add(r.get("Campaign_Number"))

    complaints_by_model: dict[str, int] = defaultdict(int)
    for r in complaint_rows:
        model = (r.get("Model") or "").strip().upper()
        if not model:
            continue
        if model.startswith("ROADSTER"):
            model = "ROADSTER"
        complaints_by_model[model] += 1

    models = sorted(set(camp_by_model) | set(complaints_by_model))
    out = []
    for m in models:
        out.append(
            {
                "Model": m,
                "Recall_Campaign_Count": len(camp_by_model.get(m, set())),
                "Complaint_Count": complaints_by_model.get(m, 0),
                "Recall_Source_ID": "SRC-NHTSA-001",
                "Complaint_Source_ID": "SRC-NHTSA-002",
                "Metric_Label": "reported",
            }
        )
    out.sort(key=lambda x: (-x["Complaint_Count"], -x["Recall_Campaign_Count"], x["Model"]))
    return out


def complaint_annual(complaint_rows: list[dict]) -> list[dict]:
    by_y: dict[str, dict] = {}
    for r in complaint_rows:
        d = r.get("Date_Complaint_Filed") or ""
        y = str(d)[:4]
        if not y.isdigit():
            continue
        if y not in by_y:
            by_y[y] = {
                "Year": int(y),
                "Complaint_Count": 0,
                "Crash_Flagged_Complaints": 0,
                "Fire_Flagged_Complaints": 0,
                "Source_ID": r.get("Source_ID") or "SRC-NHTSA-003",
                "Snapshot_Date": r.get("Snapshot_Date"),
                "Metric_Label": "reported",
                "Notes": (
                    "Allegations from NHTSA FLAT_CMPL (SRC-NHTSA-002); distinct ODINO; "
                    "not confirmed defects"
                ),
            }
        by_y[y]["Complaint_Count"] += 1
        if str(r.get("Crash") or "0") not in ("0", "0.0", "None", ""):
            by_y[y]["Crash_Flagged_Complaints"] += 1
        if str(r.get("Fire") or "0") not in ("0", "0.0", "None", ""):
            by_y[y]["Fire_Flagged_Complaints"] += 1
    return [by_y[y] for y in sorted(by_y)]


def main() -> None:
    ops = load_csv(ROOT / "data" / "processed" / "Fact_Tesla_Operations.csv")
    write_js("fact_tesla_operations", "FACT_TESLA_OPS", ops)

    fin = load_csv(ROOT / "data" / "processed" / "Fact_Financials.csv")
    write_js("fact_financials", "FACT_FINANCIALS", fin)

    recalls_raw = load_csv(ROOT / "data" / "processed" / "Fact_Recalls.csv")
    write_js("fact_recalls", "FACT_RECALLS", campaign_summaries(recalls_raw))

    annual = load_csv(ROOT / "data" / "processed" / "Fact_NHTSA_Annual.csv")
    write_js("fact_nhtsa_annual", "FACT_NHTSA_ANNUAL", annual)

    complaints = load_csv(ROOT / "data" / "processed" / "Fact_Complaints.csv")
    # Full complaint grain stays in CSV only; page uses annual + model rollups.
    write_js("fact_complaints_annual", "FACT_COMPLAINTS_ANNUAL", complaint_annual(complaints))

    by_model = model_rollups(recalls_raw, complaints)
    write_js("fact_nhtsa_by_model", "FACT_NHTSA_BY_MODEL", by_model)

    # Keep processed rollup CSV aligned with dashboard embeds.
    by_model_path = ROOT / "data" / "processed" / "Fact_NHTSA_By_Model.csv"
    with by_model_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "Model",
                "Recall_Campaign_Count",
                "Complaint_Count",
                "Recall_Source_ID",
                "Complaint_Source_ID",
                "Metric_Label",
            ],
        )
        w.writeheader()
        w.writerows(by_model)
    print(f"Wrote {len(by_model)} rows -> {by_model_path}")

    ev = load_csv(ROOT / "data" / "processed" / "Fact_EV_Market.csv")
    write_js("fact_ev_market", "FACT_EV_MARKET", ev)

    chg = load_csv(ROOT / "data" / "processed" / "Fact_EV_Chargers_CA.csv")
    write_js("fact_ev_chargers", "FACT_EV_CHARGERS", chg)


if __name__ == "__main__":
    main()
