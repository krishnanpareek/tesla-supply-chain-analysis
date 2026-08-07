"""Enrich Fact_Financials with citation fields and calculated KPIs used on Page 3."""
from __future__ import annotations

import csv
import json
import re
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FACT = ROOT / "data" / "processed" / "Fact_Financials.csv"
LOG = ROOT / "data" / "reference" / "download_log.md"
OUT_JS = ROOT / "dashboard" / "data" / "fact_financials.js"
OUT_JSON = ROOT / "dashboard" / "data" / "Fact_Financials.json"


def parse_sec_index(md: str) -> dict[str, dict]:
    out: dict[str, dict] = {}
    for line in md.splitlines():
        if "`10-" not in line:
            continue
        m = re.search(
            r"\|\s*(SRC-SEC-[^|]+)\s*\|\s*(10-[QK])\s*\|\s*`([^`]+)`\s*\|\s*([^|]+)\|\s*([^|]+)\|\s*([^|]+)\|\s*(https://[^|]+)\|",
            line,
        )
        if not m:
            continue
        sid, form, fname, _period_end, pub, accession, url = [x.strip() for x in m.groups()]
        out[fname] = {
            "Source_ID": sid,
            "Publication_Date": pub,
            "Accession": accession,
            "Source_URL": url,
        }
    return out


def days_in_reporting_period(period: str) -> int:
    a, b = [x.strip() for x in period.split(" to ")]
    d0 = datetime.strptime(a, "%Y-%m-%d").date()
    d1 = datetime.strptime(b, "%Y-%m-%d").date()
    return (d1 - d0).days + 1


def fnum(x):
    if x is None or x == "":
        return None
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def cash_label(basis: str) -> str:
    return {
        "quarter_equals_ytd": "reported (Q1 YTD = quarter)",
        "quarter_calculated_from_ytd": "calculated (YTD − prior YTD)",
        "quarter_calculated_from_annual_minus_9mo": "calculated (annual − 9-mo YTD)",
    }.get(basis, basis or "")


def main() -> None:
    index = parse_sec_index(LOG.read_text(encoding="utf-8"))
    raw_rows = list(csv.DictReader(FACT.open(encoding="utf-8")))
    clean = []
    for r in raw_rows:
        # Re-enrich from base extract columns if already enriched
        base_keys = [
            "Period_ID", "Reporting_Period", "Form", "Report_Date",
            "Total_Revenue", "Automotive_Revenue", "Cost_of_Automotive_Revenue",
            "Automotive_Gross_Margin", "Inventory", "Accounts_Payable",
            "Capital_Expenditures", "Operating_Cash_Flow", "Net_Income",
            "CashFlow_Basis", "Unit", "Source_File",
        ]
        row = {k: r.get(k) for k in base_keys}
        src = index.get(row["Source_File"], {})
        inv = fnum(row.get("Inventory"))
        cogs = fnum(row.get("Cost_of_Automotive_Revenue"))
        ocf = fnum(row.get("Operating_Cash_Flow"))
        capex = fnum(row.get("Capital_Expenditures"))
        auto = fnum(row.get("Automotive_Revenue"))
        margin = fnum(row.get("Automotive_Gross_Margin"))
        days = days_in_reporting_period(row["Reporting_Period"])
        gp = (auto - cogs) if auto is not None and cogs is not None else None
        inv_days = (inv / (cogs / days)) if inv is not None and cogs and days else None
        fcf = (ocf - capex) if ocf is not None and capex is not None else None
        clean.append(
            {
                "Period_ID": row["Period_ID"],
                "Reporting_Period": row["Reporting_Period"],
                "Form": row["Form"],
                "Report_Date": row["Report_Date"],
                "Total_Revenue": fnum(row["Total_Revenue"]),
                "Automotive_Revenue": auto,
                "Cost_of_Automotive_Revenue": cogs,
                "Automotive_Gross_Profit": gp,
                "Automotive_Gross_Margin": margin,
                "Inventory": inv,
                "Accounts_Payable": fnum(row.get("Accounts_Payable")),
                "Capital_Expenditures": capex,
                "Operating_Cash_Flow": ocf,
                "Free_Cash_Flow": fcf,
                "Net_Income": fnum(row.get("Net_Income")),
                "Inventory_Days_Estimate": inv_days,
                "Days_In_Period": days,
                "CashFlow_Basis": row["CashFlow_Basis"],
                "OCF_Capex_Metric_Label": cash_label(row["CashFlow_Basis"]),
                "Unit": row["Unit"],
                "Source_File": row["Source_File"],
                "Source_ID": src.get("Source_ID", ""),
                "Source_Accession": src.get("Accession", ""),
                "Source_URL": src.get("Source_URL", ""),
                "Publication_Date": src.get("Publication_Date", ""),
                "Enriched_On": date.today().isoformat(),
            }
        )

    fieldnames = list(clean[0].keys())
    with FACT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(clean)

    OUT_JS.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(clean, indent=2), encoding="utf-8")
    OUT_JS.write_text(
        "window.FACT_FINANCIALS = " + json.dumps(clean) + ";\n",
        encoding="utf-8",
    )
    print(f"Enriched {len(clean)} rows -> {FACT}")
    print(f"Embed -> {OUT_JS}")
    last = clean[-1]
    print(
        f"{last['Period_ID']} FCF={last['Free_Cash_Flow']} "
        f"InvDays={last['Inventory_Days_Estimate']:.2f} "
        f"Source_URL={'yes' if last['Source_URL'] else 'NO'}"
    )
    missing = [r["Period_ID"] for r in clean if not r["Source_URL"]]
    if missing:
        print("Missing Source_URL for:", missing)


if __name__ == "__main__":
    main()
