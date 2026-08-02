"""
Extract Fact_Tesla_Operations from Tesla IR 8-K Exhibit 99.1 HTML files.

Rules:
- Only use values present in source files; never invent or interpolate.
- Every extracted number is written to the extraction log with source file + section.
- Vehicle groups are stored AS REPORTED (Model S/X vs Other Models are not silently merged).
"""
from __future__ import annotations

import csv
import json
import re
import html
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw" / "tesla_ir"
PROCESSED_DIR = ROOT / "data" / "processed"
REF_DIR = ROOT / "data" / "reference"
DOC_DIR = ROOT / "documentation"

PERIOD_BOUNDS = {
    "Q1": ("01-01", "03-31"),
    "Q2": ("04-01", "06-30"),
    "Q3": ("07-01", "09-30"),
    "Q4": ("10-01", "12-31"),
}


@dataclass
class ExtractionEvent:
    period_id: str
    reporting_period: str
    vehicle_group: str
    field_name: str
    field_value: Optional[str]
    metric_label: str  # reported | calculated
    source_file: str
    source_section: str
    source_excerpt: str
    notes: str = ""


def period_from_filename(name: str) -> tuple[str, str, str, str]:
    # tesla_production_deliveries_Q1_2022_2022-04-04_...
    m = re.match(
        r"tesla_production_deliveries_(Q[1-4])_(\d{4})_(\d{4}-\d{2}-\d{2})_(.+)$",
        name,
    )
    if not m:
        raise ValueError(f"Unexpected filename: {name}")
    q, year, pub, rest = m.groups()
    start_md, end_md = PERIOD_BOUNDS[q]
    period_id = f"{year}{q}"
    reporting_period = f"{year}-{start_md} to {year}-{end_md}"
    return period_id, reporting_period, pub, rest


def html_to_text(raw: str) -> str:
    t = re.sub(r"<script[\s\S]*?</script>", " ", raw, flags=re.I)
    t = re.sub(r"<style[\s\S]*?</style>", " ", t, flags=re.I)
    t = re.sub(r"</t[dh]>", " | ", t, flags=re.I)
    t = re.sub(r"</tr>", "\n", t, flags=re.I)
    t = re.sub(r"<br\s*/?>", "\n", t, flags=re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    t = html.unescape(t)
    # Collapse whitespace but preserve newlines for row parsing
    t = re.sub(r"[ \t\f\v]+", " ", t)
    t = re.sub(r" *\n *", "\n", t)
    # Fix numbers split by markup: "258,5 8 0" -> "258,580"
    t = re.sub(r"(?<=\d)\s+(?=\d)", "", t)
    return t.strip()


def parse_int(num: str) -> int:
    return int(num.replace(",", "").replace(" ", ""))


def detect_format_flags(text: str) -> list[str]:
    flags = []
    if "Model S/X" in text:
        flags.append("vehicle_group_label=Model_S_X")
    if re.search(r"Other Models", text, re.I):
        flags.append("vehicle_group_label=Other_Models")
    if re.search(r"Production,\s*Deliveries\s*&\s*Deployments", text, re.I):
        flags.append("release_title=Production_Deliveries_Deployments")
    elif re.search(r"Vehicle Production\s*&\s*Deliveries", text, re.I):
        flags.append("release_title=Vehicle_Production_Deliveries")
    if re.search(r"\bGWh\b", text):
        flags.append("energy_unit=GWh")
    if re.search(r"\bMWh\b", text):
        flags.append("energy_unit=MWh")
    if not re.search(r"\b(?:GWh|MWh)\b", text):
        flags.append("energy_storage=not_disclosed_in_release")
    return flags


def excerpt(text: str, needle: str, pad: int = 60) -> str:
    i = text.lower().find(needle.lower())
    if i < 0:
        return needle[:120]
    a = max(0, i - pad)
    b = min(len(text), i + len(needle) + pad)
    return re.sub(r"\s+", " ", text[a:b]).strip()


def extract_quarterly_table(text: str) -> tuple[list[tuple[str, int, int]], Optional[tuple[int, int]], str]:
    """
    Returns:
      - list of (vehicle_group, produced, delivered) for segment rows (first quarterly table only)
      - total (produced, delivered) if found
      - section label used
    """
    # Prefer the first occurrence block after the title / before annual table markers
    # Annual tables in Q4 releases follow a year heading like "2023" / "2024" / "2025"
    # Strategy: find all segment rows, take first occurrence of each group + first Total.

    segment_pat = re.compile(
        r"(Model S/X|Model 3/Y|Other Models)\s*\|\s*([0-9][0-9,]*)\s*\|\s*([0-9][0-9,]*)",
        re.I,
    )
    total_pat = re.compile(
        r"\bTotal\s*\|\s*([0-9][0-9,]*)\s*\|\s*([0-9][0-9,]*)",
        re.I,
    )

    seen_groups = set()
    segments: list[tuple[str, int, int]] = []
    for m in segment_pat.finditer(text):
        group = re.sub(r"\s+", " ", m.group(1)).strip()
        # Normalize casing
        if group.lower() == "other models":
            group = "Other Models"
        elif group.lower() == "model s/x":
            group = "Model S/X"
        elif group.lower() == "model 3/y":
            group = "Model 3/Y"
        if group in seen_groups:
            # Second table is typically full-year; stop adding segments
            continue
        # Only accept first-pass groups before we've seen a second full set
        # If we already have 2 groups and encounter a repeat year table, skip
        produced = parse_int(m.group(2))
        delivered = parse_int(m.group(3))
        # Heuristic: annual totals are usually > 700k for Model 3/Y; quarterly rarely exceeds ~500k
        # But don't filter Model S/X annual (~70k) vs quarterly (~20k) solely that way.
        # Use order: first match per group = quarterly.
        seen_groups.add(group)
        segments.append((group, produced, delivered))
        if len(segments) >= 2:
            # Expect two segment rows in these releases
            pass

    total = None
    for m in total_pat.finditer(text):
        produced = parse_int(m.group(1))
        delivered = parse_int(m.group(2))
        # First Total is quarterly; subsequent often annual
        total = (produced, delivered)
        break

    section = (
        "Exhibit 99.1 quarterly production/deliveries table "
        "(first Production|Deliveries table; excludes later full-year table if present)"
    )
    return segments, total, section


def extract_energy_gwh(text: str) -> tuple[Optional[float], str, str, str]:
    """
    Returns (gwh_value_or_None, metric_label, section, excerpt/notes)
    """
    m = re.search(
        r"deployed\s+([0-9]+(?:,[0-9]{3})*(?:\.[0-9]+)?)\s*(GWh|MWh)\s+of\s+energy\s+storage",
        text,
        re.I,
    )
    if not m:
        # alternate phrasing
        m = re.search(
            r"deployed\s+([0-9]+(?:,[0-9]{3})*(?:\.[0-9]+)?)\s*(GWh|MWh)",
            text,
            re.I,
        )
    if not m:
        return None, "reported", "Exhibit 99.1 narrative (energy storage)", "Energy storage deployment not stated in this release"

    raw = m.group(1).replace(",", "")
    unit = m.group(2).upper()
    val = float(raw)
    ex = excerpt(text, m.group(0))
    if unit == "GWH":
        return val, "reported", "Exhibit 99.1 opening narrative — energy storage deployments (GWh)", ex
    # MWh -> GWh
    gwh = val / 1000.0
    return (
        gwh,
        "calculated",
        "Exhibit 99.1 opening narrative — energy storage deployments (MWh converted to GWh by /1000)",
        f"{ex} | conversion: {val} MWh / 1000 = {gwh} GWh",
    )


def validate_total(segments: list[tuple[str, int, int]], total: Optional[tuple[int, int]]) -> list[str]:
    notes = []
    if not total:
        notes.append("WARNING: quarterly Total row not found")
        return notes
    if not segments:
        notes.append("WARNING: segment rows not found")
        return notes
    sp = sum(s[1] for s in segments)
    sd = sum(s[2] for s in segments)
    if sp != total[0]:
        notes.append(f"WARNING: segment produced sum {sp} != Total produced {total[0]}")
    if sd != total[1]:
        notes.append(f"WARNING: segment delivered sum {sd} != Total delivered {total[1]}")
    if sp == total[0] and sd == total[1]:
        notes.append("Validation OK: segment sums equal Total row")
    return notes


def process_file(path: Path) -> tuple[list[dict], list[ExtractionEvent], dict]:
    period_id, reporting_period, pub_date, _ = period_from_filename(path.name)
    raw = path.read_text(encoding="utf-8", errors="ignore")
    text = html_to_text(raw)
    flags = detect_format_flags(text)
    segments, total, table_section = extract_quarterly_table(text)
    energy_gwh, energy_label, energy_section, energy_excerpt = extract_energy_gwh(text)
    validations = validate_total(segments, total)

    events: list[ExtractionEvent] = []
    rows: list[dict] = []

    def add_row(group: str, produced: int, delivered: int, energy: Optional[float], energy_lbl: Optional[str]):
        gap = produced - delivered
        conv = round(delivered / produced, 6) if produced else None
        rows.append(
            {
                "Period_ID": period_id,
                "Reporting_Period": reporting_period,
                "Vehicle_Group": group,
                "Vehicles_Produced": produced,
                "Vehicles_Delivered": delivered,
                "Energy_Storage_GWh": "" if energy is None else energy,
                "Production_Delivery_Gap": gap,
                "Delivery_Conversion_Rate": "" if conv is None else conv,
                "Publication_Date": pub_date,
                "Source_File": path.name,
                "Source_ID": f"SRC-TESLA-IR-001-{period_id[4:]}_{period_id[:4]}",
                "Vehicle_Group_As_Reported": group,
                "Format_Flags": "|".join(flags),
                "Metric_Notes": (
                    "Vehicles_Produced/Delivered=reported; "
                    "Production_Delivery_Gap=calculated(Produced-Delivered); "
                    "Delivery_Conversion_Rate=calculated(Delivered/Produced); "
                    f"Energy_Storage_GWh={'null' if energy is None else energy_lbl}"
                ),
            }
        )

        for field, value, label, section, ex, note in [
            (
                "Vehicles_Produced",
                produced,
                "reported",
                table_section + f" — row '{group}', Production column",
                excerpt(text, f"{group}"),
                "",
            ),
            (
                "Vehicles_Delivered",
                delivered,
                "reported",
                table_section + f" — row '{group}', Deliveries column",
                excerpt(text, f"{group}"),
                "",
            ),
            (
                "Production_Delivery_Gap",
                gap,
                "calculated",
                "Calculated field (not printed as gap in source)",
                f"{produced} - {delivered} = {gap}",
                "May reflect vehicles in transit, timing, logistics, demand, shutdowns, product mix, or reporting cutoffs — not labeled unsold inventory",
            ),
            (
                "Delivery_Conversion_Rate",
                conv,
                "calculated",
                "Calculated field (Delivered / Produced)",
                f"{delivered} / {produced} = {conv}",
                "",
            ),
        ]:
            events.append(
                ExtractionEvent(
                    period_id=period_id,
                    reporting_period=reporting_period,
                    vehicle_group=group,
                    field_name=field,
                    field_value=None if value is None else str(value),
                    metric_label=label,
                    source_file=path.name,
                    source_section=section,
                    source_excerpt=ex,
                    notes=note,
                )
            )

        if group == "Total":
            events.append(
                ExtractionEvent(
                    period_id=period_id,
                    reporting_period=reporting_period,
                    vehicle_group=group,
                    field_name="Energy_Storage_GWh",
                    field_value=None if energy is None else str(energy),
                    metric_label=energy_lbl or "reported",
                    source_file=path.name,
                    source_section=energy_section,
                    source_excerpt=energy_excerpt,
                    notes="Null when release does not disclose energy storage deployments",
                )
            )
        else:
            events.append(
                ExtractionEvent(
                    period_id=period_id,
                    reporting_period=reporting_period,
                    vehicle_group=group,
                    field_name="Energy_Storage_GWh",
                    field_value=None,
                    metric_label="reported",
                    source_file=path.name,
                    source_section="N/A — energy storage not disclosed by vehicle group",
                    source_excerpt="",
                    notes="Left null at vehicle-group grain; company-total energy stored on Total row only",
                )
            )

    for group, produced, delivered in segments:
        add_row(group, produced, delivered, None, None)

    if total:
        add_row("Total", total[0], total[1], energy_gwh, energy_label)
    else:
        # Still log missing total
        events.append(
            ExtractionEvent(
                period_id=period_id,
                reporting_period=reporting_period,
                vehicle_group="Total",
                field_name="Vehicles_Produced",
                field_value=None,
                metric_label="reported",
                source_file=path.name,
                source_section=table_section,
                source_excerpt="",
                notes="MISSING: Total row could not be parsed",
            )
        )

    meta = {
        "period_id": period_id,
        "reporting_period": reporting_period,
        "publication_date": pub_date,
        "source_file": path.name,
        "format_flags": flags,
        "validation": validations,
        "segment_groups": [s[0] for s in segments],
        "has_energy": energy_gwh is not None,
    }
    return rows, events, meta


def write_format_change_doc(metas: list[dict]) -> None:
    lines = [
        "# Fact_Tesla_Operations — Release Format Changes",
        "",
        "Do **not** silently merge incompatible vehicle-group categories across periods.",
        "",
        "## Vehicle group taxonomy break",
        "",
        "| Periods | As-reported groups | Notes |",
        "|---------|--------------------|-------|",
        "| Q1 2022 – Q3 2023 | `Model S/X`, `Model 3/Y`, `Total` | Non-3/Y vehicles labeled **Model S/X** |",
        "| Q4 2023 – Q2 2026 | `Model 3/Y`, `Other Models`, `Total` | Non-3/Y vehicles labeled **Other Models** (may include Cybertruck and other non-3/Y products; source does not itemize) |",
        "",
        "**Implication:** `Model S/X` and `Other Models` are **not treated as identical series** in analysis without an explicit, documented mapping assumption. Trend charts by vehicle group should either (a) keep labels separate, or (b) show a clear break annotation at Q4 2023.",
        "",
        "## Energy storage disclosure",
        "",
        "| Periods | Disclosure | Handling |",
        "|---------|------------|----------|",
        "| Q1 2022 – Q4 2023 | Not in these production releases | `Energy_Storage_GWh` = null on all rows |",
        "| Q1 2024 | Reported in **MWh** (4,053 MWh) | Stored as **calculated** GWh = MWh/1000 on Total row only |",
        "| Q2 2024 – Q2 2026 | Reported in **GWh** | Stored as **reported** GWh on Total row only |",
        "",
        "## Release title / packaging",
        "",
        "- Earlier: “Vehicle Production & Deliveries and Date for Financial Results & Webcast …”",
        "- Later (from ~Q3 2024): “Production, Deliveries & Deployments”",
        "",
        "## Per-quarter flags",
        "",
        "| Period_ID | Publication_Date | Format_Flags | Validation |",
        "|-----------|------------------|--------------|------------|",
    ]
    for m in sorted(metas, key=lambda x: x["period_id"]):
        lines.append(
            f"| {m['period_id']} | {m['publication_date']} | `{';'.join(m['format_flags'])}` | {'; '.join(m['validation'])} |"
        )
    lines.append("")
    out = DOC_DIR / "fact_tesla_operations_format_changes.md"
    out.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    REF_DIR.mkdir(parents=True, exist_ok=True)
    DOC_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(RAW_DIR.glob("tesla_production_deliveries_*.htm"))
    all_rows: list[dict] = []
    all_events: list[ExtractionEvent] = []
    metas: list[dict] = []

    for path in files:
        rows, events, meta = process_file(path)
        all_rows.extend(rows)
        all_events.extend(events)
        metas.append(meta)
        print(meta["period_id"], meta["segment_groups"], "energy" if meta["has_energy"] else "no-energy", ";", "; ".join(meta["validation"]))

    # Sort fact rows
    group_order = {"Model 3/Y": 1, "Model S/X": 2, "Other Models": 3, "Total": 9}
    all_rows.sort(key=lambda r: (r["Period_ID"], group_order.get(r["Vehicle_Group"], 5)))

    fact_path = PROCESSED_DIR / "Fact_Tesla_Operations.csv"
    fact_fields = [
        "Period_ID",
        "Reporting_Period",
        "Vehicle_Group",
        "Vehicles_Produced",
        "Vehicles_Delivered",
        "Energy_Storage_GWh",
        "Production_Delivery_Gap",
        "Delivery_Conversion_Rate",
        "Publication_Date",
        "Source_File",
        "Source_ID",
        "Vehicle_Group_As_Reported",
        "Format_Flags",
        "Metric_Notes",
    ]
    with fact_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fact_fields)
        w.writeheader()
        w.writerows(all_rows)

    log_path = REF_DIR / "Fact_Tesla_Operations_extraction_log.csv"
    log_fields = [
        "Period_ID",
        "Reporting_Period",
        "Vehicle_Group",
        "Field_Name",
        "Field_Value",
        "Metric_Label",
        "Source_File",
        "Source_Section",
        "Source_Excerpt",
        "Notes",
    ]
    with log_path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=log_fields)
        w.writeheader()
        for e in all_events:
            w.writerow(
                {
                    "Period_ID": e.period_id,
                    "Reporting_Period": e.reporting_period,
                    "Vehicle_Group": e.vehicle_group,
                    "Field_Name": e.field_name,
                    "Field_Value": e.field_value if e.field_value is not None else "",
                    "Metric_Label": e.metric_label,
                    "Source_File": e.source_file,
                    "Source_Section": e.source_section,
                    "Source_Excerpt": e.source_excerpt,
                    "Notes": e.notes,
                }
            )

    # Markdown summary log for portfolio readability
    md_path = REF_DIR / "Fact_Tesla_Operations_extraction_log.md"
    md = [
        "# Fact_Tesla_Operations Extraction Log",
        "",
        "Companion traceability log for `data/processed/Fact_Tesla_Operations.csv`.",
        "",
        "Every externally sourced or calculated value is listed with source file and section.",
        "",
        "See also: `documentation/fact_tesla_operations_format_changes.md`.",
        "",
        f"**Rows in fact table:** {len(all_rows)}  ",
        f"**Extraction events logged:** {len(all_events)}  ",
        "",
        "| Period_ID | Vehicle_Group | Field | Value | Label | Source_File | Source_Section |",
        "|-----------|---------------|-------|-------|-------|-------------|----------------|",
    ]
    for e in all_events:
        if e.field_name in {
            "Vehicles_Produced",
            "Vehicles_Delivered",
            "Energy_Storage_GWh",
            "Production_Delivery_Gap",
            "Delivery_Conversion_Rate",
        }:
            md.append(
                f"| {e.period_id} | {e.vehicle_group} | {e.field_name} | {e.field_value if e.field_value is not None else 'null'} | {e.metric_label} | `{e.source_file}` | {e.source_section} |"
            )
    md.append("")
    md_path.write_text("\n".join(md), encoding="utf-8")

    write_format_change_doc(metas)

    # machine-readable meta
    (REF_DIR / "Fact_Tesla_Operations_extract_meta.json").write_text(
        json.dumps(metas, indent=2), encoding="utf-8"
    )

    print(f"Wrote {fact_path} ({len(all_rows)} rows)")
    print(f"Wrote {log_path} ({len(all_events)} events)")
    print(f"Wrote {md_path}")
    print(f"Wrote {DOC_DIR / 'fact_tesla_operations_format_changes.md'}")


if __name__ == "__main__":
    main()
