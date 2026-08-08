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

    raw = load_csv(ROOT / "data" / "processed" / "Fact_Raw_Materials.csv")
    write_js(
        "fact_raw_materials_kpi",
        "FACT_RAW_MATERIALS_KPI",
        raw_materials_kpis(raw, primary_year=2025),
    )
    write_js(
        "fact_raw_materials_production",
        "FACT_RAW_MATERIALS_PROD",
        raw_materials_production(raw),
    )


def _is_world_mine_production(r: dict) -> bool:
    section = str(r.get("Section") or "")
    stats = str(r.get("Statistics") or "")
    detail = str(r.get("Statistics_Detail") or "").lower()
    if "World Mine Production" not in section:
        return False
    if stats != "Production":
        return False
    # Prefer mine production rows; skip reserves.
    if "reserve" in detail:
        return False
    return "mine production" in detail or detail.startswith("mine")


def raw_materials_production(rows: list[dict]) -> list[dict]:
    """Country×year mine production series with USGS Metric_Label preserved."""
    out = []
    for r in rows:
        if not _is_world_mine_production(r):
            continue
        if r.get("Value_Numeric") is None:
            continue
        out.append(
            {
                "Commodity": r.get("Commodity"),
                "Country": r.get("Country"),
                "Year": r.get("Year"),
                "Value": r.get("Value_Numeric"),
                "Unit": r.get("Unit"),
                "Statistics_Detail": r.get("Statistics_Detail"),
                "Notes": r.get("Notes"),
                "Metric_Label": r.get("Metric_Label") or "reported",
                "Source_File": r.get("Source_File"),
                "Source_ID": r.get("Source_ID"),
                "Source_URL": r.get("Source_URL"),
                "Publication_Date": r.get("Publication_Date"),
                "DOI": r.get("DOI"),
            }
        )
    out.sort(key=lambda x: (x["Commodity"] or "", x["Country"] or "", x["Year"] or 0))
    return out


def raw_materials_kpis(rows: list[dict], primary_year: int = 2025) -> list[dict]:
    """Per-commodity KPI bundle for Page 6; prefer primary_year (2025 in MCS 2026)."""
    preferred = ["Lithium", "Cobalt", "Nickel", "Graphite (Natural)"]
    found = {r.get("Commodity") for r in rows if r.get("Commodity")}
    commodities = [c for c in preferred if c in found] + sorted(found - set(preferred))
    out = []
    for commodity in commodities:
        c_rows = [r for r in rows if r.get("Commodity") == commodity]
        nir_candidates = [
            r
            for r in c_rows
            if r.get("Country") == "United States"
            and "import reliance" in str(r.get("Statistics") or "").lower()
            and r.get("Year") == primary_year
        ]
        nir = nir_candidates[0] if nir_candidates else None

        prod_year = [
            r
            for r in c_rows
            if _is_world_mine_production(r) and r.get("Year") == primary_year and r.get("Value_Numeric") is not None
        ]
        prod_year.sort(key=lambda r: float(r["Value_Numeric"]), reverse=True)
        world = next((r for r in prod_year if str(r.get("Country") or "").lower().startswith("world")), None)
        countries = [r for r in prod_year if not str(r.get("Country") or "").lower().startswith("world")]
        top = countries[:5] if countries else []

        top_share = None
        if top and world and world.get("Value_Numeric"):
            top_share = float(top[0]["Value_Numeric"]) / float(world["Value_Numeric"])

        def producer(r: dict) -> dict:
            return {
                "Country": r.get("Country"),
                "Value": r.get("Value_Numeric"),
                "Unit": r.get("Unit"),
                "Metric_Label": r.get("Metric_Label") or "reported",
                "Notes": r.get("Notes"),
            }

        # Preserve USGS value text for range strings (e.g. lithium ">50").
        nir_value = None
        if nir is not None:
            nir_value = nir.get("Value") if nir.get("Value_Numeric") is None else nir.get("Value_Numeric")
            if isinstance(nir_value, str) and nir_value.replace(".", "", 1).isdigit():
                nir_value = float(nir_value)

        sample = nir or world or (top[0] if top else (c_rows[0] if c_rows else {}))
        out.append(
            {
                "Commodity": commodity,
                "Primary_Year": primary_year,
                "Net_Import_Reliance_US": nir_value,
                "Net_Import_Reliance_Year": nir.get("Year") if nir else None,
                "Net_Import_Reliance_Unit": nir.get("Unit") if nir else "percent",
                "Net_Import_Reliance_Metric_Label": (nir.get("Metric_Label") if nir else None) or "reported",
                "Net_Import_Reliance_Notes": nir.get("Notes") if nir else None,
                "World_Mine_Production": world.get("Value_Numeric") if world else None,
                "World_Mine_Production_Unit": world.get("Unit") if world else None,
                "World_Mine_Production_Metric_Label": (world.get("Metric_Label") if world else None) or "estimated",
                "World_Mine_Production_Notes": world.get("Notes") if world else None,
                "Top_Producers_Year": primary_year,
                "Top_Producers": [producer(r) for r in top],
                "Top_Producer_Share_of_World": top_share,
                "Top_Producer_Share_Metric_Label": "calculated",
                "Source_ID": sample.get("Source_ID"),
                "Source_File": sample.get("Source_File"),
                "Source_URL": sample.get("Source_URL"),
                "Publication_Date": sample.get("Publication_Date"),
                "DOI": sample.get("DOI"),
                "Metric_Label": "mixed",  # page uses field-level labels
                "Notes": (
                    f"Primary dashboard year {primary_year}. "
                    "World mine production and US net import reliance for 2025 are typically "
                    "USGS-estimated in MCS 2026; Metric_Label follows USGS Notes containing 'Estimated'."
                ),
            }
        )
    return out


if __name__ == "__main__":
    main()
