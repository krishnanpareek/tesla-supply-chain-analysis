"""
Extract Fact_Financials from local Tesla 10-Q / 10-K HTML (iXBRL).

Units: USD millions as presented in Tesla filings (ix scale="6").
Income-statement items use the three-month (quarterly) duration when available.
Cash-flow items are often YTD in 10-Qs; quarterly OCF/Capex are calculated by
differencing YTD figures and labeled accordingly in the extraction log.
"""
from __future__ import annotations

import csv
import json
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

ROOT = Path(__file__).resolve().parents[1]
RAW = ROOT / "data" / "raw" / "sec_edgar"
OUT = ROOT / "data" / "processed" / "Fact_Financials.csv"
LOG = ROOT / "data" / "reference" / "Fact_Financials_extraction_log.csv"
META = ROOT / "data" / "reference" / "Fact_Financials_extract_meta.json"
DOC = ROOT / "documentation" / "fact_financials_notes.md"

PERIOD_MAP = {
    "Q1": ("01-01", "03-31"),
    "Q2": ("04-01", "06-30"),
    "Q3": ("07-01", "09-30"),
    "Q4": ("10-01", "12-31"),
}


@dataclass
class Filing:
    path: Path
    form: str
    period_key: str  # Q1_2022 or FY_2022
    report_date: str
    filing_date: str


def parse_filename(p: Path) -> Filing:
    # 10-Q_Q1_2022_2022-03-31_tsla-20220331.htm
    # 10-K_FY_2022_2022-12-31_tsla-20221231.htm
    m = re.match(
        r"(10-Q|10-K)_(Q[1-4]|FY)_(\d{4})_(\d{4}-\d{2}-\d{2})_(.+)$", p.name
    )
    if not m:
        raise ValueError(p.name)
    form, q_or_fy, year, report_date, _ = m.groups()
    # filing date from download log would be better; approximate unknown here -> report_date end
    return Filing(p, form, f"{q_or_fy}_{year}", report_date, report_date)


def parse_number(raw: str, scale: int, sign: Optional[str]) -> float:
    v = float(raw.replace(",", "").replace(" ", ""))
    if sign == "-":
        v = -v
    # Keep in millions (scale 6 presentation)
    # If scale is 6, displayed number is already millions.
    # If scale is 0, convert to millions.
    if scale == 0:
        v = v / 1_000_000.0
    elif scale not in (6, 0):
        v = v * (10 ** scale) / 1_000_000.0
    return v


def load_xbrl(path: Path):
    t = path.read_text(encoding="utf-8", errors="ignore")
    contexts = {}
    for cid, body in re.findall(
        r'<xbrli:context[^>]*id="([^"]+)"[^>]*>([\s\S]*?)</xbrli:context>', t, re.I
    ):
        instant = re.search(r"<xbrli:instant>([^<]+)</xbrli:instant>", body, re.I)
        start = re.search(r"<xbrli:startDate>([^<]+)</xbrli:startDate>", body, re.I)
        end = re.search(r"<xbrli:endDate>([^<]+)</xbrli:endDate>", body, re.I)
        members = re.findall(r"explicitMember[^>]*>([^<]+)<", body, re.I)
        contexts[cid] = {
            "instant": instant.group(1) if instant else None,
            "start": start.group(1) if start else None,
            "end": end.group(1) if end else None,
            "members": tuple(members),
        }
    facts = []
    for attrs, val in re.findall(
        r"<ix:nonFraction\b([^>]*)>([^<]*)</ix:nonFraction>", t, re.I
    ):
        name = re.search(r'name="([^"]+)"', attrs, re.I)
        ctx = re.search(r'contextRef="([^"]+)"', attrs, re.I)
        scale = re.search(r'scale="([^"]+)"', attrs, re.I)
        sign = re.search(r'sign="([^"]+)"', attrs, re.I)
        if not name or not ctx or ctx.group(1) not in contexts:
            continue
        c = contexts[ctx.group(1)]
        try:
            num = parse_number(val.strip(), int(scale.group(1)) if scale else 0, sign.group(1) if sign else None)
        except ValueError:
            continue
        facts.append({"name": name.group(1), "value": num, "raw": val.strip(), **c})
    return facts, t


def pick(
    facts,
    name_endswith: str,
    *,
    start: Optional[str] = None,
    end: Optional[str] = None,
    instant: Optional[str] = None,
    member_contains: Optional[str] = None,
    require_no_member: bool = False,
):
    rows = []
    for f in facts:
        if not f["name"].endswith(name_endswith) and f["name"] != name_endswith:
            # allow exact or endswith
            if name_endswith not in f["name"]:
                continue
        if start and f["start"] != start:
            continue
        if end and f["end"] != end:
            continue
        if instant and f["instant"] != instant:
            continue
        members = f["members"]
        if require_no_member and members:
            continue
        if member_contains and not any(member_contains in m for m in members):
            continue
        rows.append(f)
    if not rows:
        return None
    # Prefer exact name match
    exact = [r for r in rows if r["name"].endswith(name_endswith)]
    chosen = exact[0] if exact else rows[0]
    return chosen


def quarter_window(year: int, q: str) -> tuple[str, str]:
    sm, em = PERIOD_MAP[q]
    return f"{year}-{sm}", f"{year}-{em}"


def ytd_start(year: int) -> str:
    return f"{year}-01-01"


def extract_from_10q(filing: Filing):
    facts, _ = load_xbrl(filing.path)
    q, year_s = filing.period_key.split("_")
    year = int(year_s)
    q_start, q_end = quarter_window(year, q)
    events = []
    row = {
        "Period_ID": f"{year}{q}",
        "Reporting_Period": f"{q_start} to {q_end}",
        "Form": "10-Q",
        "Report_Date": filing.report_date,
        "Source_File": filing.path.name,
        "Unit": "USD_millions",
    }

    def add(field, fact, label, section):
        if fact is None:
            row[field] = None
            events.append(
                {
                    "Period_ID": row["Period_ID"],
                    "Field_Name": field,
                    "Field_Value": "",
                    "Metric_Label": label,
                    "Source_File": filing.path.name,
                    "Source_Section": section,
                    "Notes": "NOT FOUND in iXBRL for this period filter",
                }
            )
            return
        row[field] = fact["value"]
        events.append(
            {
                "Period_ID": row["Period_ID"],
                "Field_Name": field,
                "Field_Value": fact["value"],
                "Metric_Label": label,
                "Source_File": filing.path.name,
                "Source_Section": section,
                "Notes": f"XBRL {fact['name']}; raw={fact['raw']}; start={fact['start']}; end={fact['end']}; instant={fact['instant']}; members={list(fact['members'])}",
            }
        )

    add(
        "Total_Revenue",
        pick(
            facts,
            "RevenueFromContractWithCustomerExcludingAssessedTax",
            start=q_start,
            end=q_end,
            require_no_member=True,
        )
        or pick(facts, "Revenues", start=q_start, end=q_end, require_no_member=True),
        "reported",
        "Consolidated statements of operations — Total revenues (three months)",
    )
    add(
        "Automotive_Revenue",
        pick(
            facts,
            "RevenueFromContractWithCustomerExcludingAssessedTax",
            start=q_start,
            end=q_end,
            member_contains="AutomotiveRevenuesMember",
        )
        or pick(
            facts,
            "AutomotiveRevenues",
            start=q_start,
            end=q_end,
            member_contains="AutomotiveRevenuesMember",
        )
        or pick(facts, "AutomotiveRevenues", start=q_start, end=q_end, require_no_member=True),
        "reported",
        "Revenue note — Automotive revenues (three months; us-gaap or tsla taxonomy)",
    )
    add(
        "Cost_of_Automotive_Revenue",
        pick(
            facts,
            "CostOfRevenue",
            start=q_start,
            end=q_end,
            member_contains="AutomotiveRevenuesMember",
        )
        or pick(
            facts,
            "AutomotiveCostOfRevenues",
            start=q_start,
            end=q_end,
            member_contains="AutomotiveRevenuesMember",
        )
        or pick(facts, "AutomotiveCostOfRevenues", start=q_start, end=q_end, require_no_member=True),
        "reported",
        "Cost of automotive revenues (three months; us-gaap or tsla taxonomy)",
    )
    add(
        "Inventory",
        pick(facts, "InventoryNet", instant=q_end, require_no_member=True),
        "reported",
        "Consolidated balance sheets — Inventory (period-end)",
    )
    add(
        "Accounts_Payable",
        pick(facts, "AccountsPayableCurrent", instant=q_end, require_no_member=True),
        "reported",
        "Consolidated balance sheets — Accounts payable (period-end)",
    )
    add(
        "Net_Income",
        pick(facts, "NetIncomeLoss", start=q_start, end=q_end, require_no_member=True),
        "reported",
        "Consolidated statements of operations — Net income (three months)",
    )

    # Cash flow: YTD in 10-Q
    ocf_ytd = pick(
        facts,
        "NetCashProvidedByUsedInOperatingActivities",
        start=ytd_start(year),
        end=q_end,
        require_no_member=True,
    )
    capex_ytd = pick(
        facts,
        "PaymentsToAcquirePropertyPlantAndEquipment",
        start=ytd_start(year),
        end=q_end,
        require_no_member=True,
    )
    row["_OCF_YTD"] = ocf_ytd["value"] if ocf_ytd else None
    row["_Capex_YTD"] = capex_ytd["value"] if capex_ytd else None
    if ocf_ytd:
        events.append(
            {
                "Period_ID": row["Period_ID"],
                "Field_Name": "Operating_Cash_Flow_YTD",
                "Field_Value": ocf_ytd["value"],
                "Metric_Label": "reported",
                "Source_File": filing.path.name,
                "Source_Section": "Cash flows — Net cash provided by operating activities (YTD)",
                "Notes": f"XBRL {ocf_ytd['name']}; {ocf_ytd['start']} to {ocf_ytd['end']}",
            }
        )
    if capex_ytd:
        events.append(
            {
                "Period_ID": row["Period_ID"],
                "Field_Name": "Capital_Expenditures_YTD",
                "Field_Value": capex_ytd["value"],
                "Metric_Label": "reported",
                "Source_File": filing.path.name,
                "Source_Section": "Cash flows — Purchases of property and equipment (YTD)",
                "Notes": f"XBRL {capex_ytd['name']}; {capex_ytd['start']} to {capex_ytd['end']}",
            }
        )

    if q == "Q1":
        # YTD == quarter
        row["Operating_Cash_Flow"] = row["_OCF_YTD"]
        row["Capital_Expenditures"] = row["_Capex_YTD"]
        row["CashFlow_Basis"] = "quarter_equals_ytd"
        for field, ytd_field in [
            ("Operating_Cash_Flow", "Operating_Cash_Flow_YTD"),
            ("Capital_Expenditures", "Capital_Expenditures_YTD"),
        ]:
            events.append(
                {
                    "Period_ID": row["Period_ID"],
                    "Field_Name": field,
                    "Field_Value": row[field] if row[field] is not None else "",
                    "Metric_Label": "reported",
                    "Source_File": filing.path.name,
                    "Source_Section": "Cash flow statement — Q1 YTD equals quarterly period",
                    "Notes": f"Copied from {ytd_field}",
                }
            )
    else:
        row["Operating_Cash_Flow"] = None  # filled later by differencing
        row["Capital_Expenditures"] = None
        row["CashFlow_Basis"] = "quarter_calculated_from_ytd"

    return row, events


def extract_from_10k(filing: Filing):
    facts, _ = load_xbrl(filing.path)
    _, year_s = filing.period_key.split("_")
    year = int(year_s)
    start, end = f"{year}-01-01", f"{year}-12-31"
    events = []
    row = {
        "Period_ID": f"{year}Q4",
        "Reporting_Period": f"{year}-10-01 to {year}-12-31",
        "Form": "10-K",
        "Report_Date": filing.report_date,
        "Source_File": filing.path.name,
        "Unit": "USD_millions",
        "CashFlow_Basis": "quarter_calculated_from_annual_minus_9mo",
        "_Annual_Start": start,
        "_Annual_End": end,
    }

    def add_annual(store_as, field_annual, name, member=None, require_no_member=True, section=""):
        fact = pick(
            facts,
            name,
            start=start,
            end=end,
            member_contains=member,
            require_no_member=require_no_member if member is None else False,
        )
        if member:
            fact = pick(facts, name, start=start, end=end, member_contains=member)
        row[field_annual] = fact["value"] if fact else None
        events.append(
            {
                "Period_ID": row["Period_ID"],
                "Field_Name": field_annual,
                "Field_Value": fact["value"] if fact else "",
                "Metric_Label": "reported",
                "Source_File": filing.path.name,
                "Source_Section": section,
                "Notes": (
                    f"XBRL {fact['name']}; annual {start} to {end}; members={list(fact['members'])}"
                    if fact
                    else "NOT FOUND"
                ),
            }
        )

    add_annual(
        None,
        "_Annual_Total_Revenue",
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        section="Statements of operations — Total revenues (annual)",
    )
    if row["_Annual_Total_Revenue"] is None:
        add_annual(None, "_Annual_Total_Revenue", "Revenues", section="Statements of operations — Revenues (annual)")

    add_annual(
        None,
        "_Annual_Automotive_Revenue",
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        member="AutomotiveRevenuesMember",
        require_no_member=False,
        section="Automotive revenues member (annual)",
    )
    if row["_Annual_Automotive_Revenue"] is None:
        add_annual(
            None,
            "_Annual_Automotive_Revenue",
            "AutomotiveRevenues",
            member="AutomotiveRevenuesMember",
            require_no_member=False,
            section="tsla:AutomotiveRevenues (annual)",
        )
    add_annual(
        None,
        "_Annual_Cost_Auto",
        "CostOfRevenue",
        member="AutomotiveRevenuesMember",
        require_no_member=False,
        section="Cost of automotive revenues member (annual)",
    )
    if row["_Annual_Cost_Auto"] is None:
        add_annual(
            None,
            "_Annual_Cost_Auto",
            "AutomotiveCostOfRevenues",
            member="AutomotiveRevenuesMember",
            require_no_member=False,
            section="tsla:AutomotiveCostOfRevenues (annual)",
        )
    add_annual(None, "_Annual_Net_Income", "NetIncomeLoss", section="Net income (annual)")
    add_annual(
        None,
        "_Annual_OCF",
        "NetCashProvidedByUsedInOperatingActivities",
        section="Operating cash flow (annual)",
    )
    add_annual(
        None,
        "_Annual_Capex",
        "PaymentsToAcquirePropertyPlantAndEquipment",
        section="Purchases of PPE (annual)",
    )

    inv = pick(facts, "InventoryNet", instant=end, require_no_member=True)
    ap = pick(facts, "AccountsPayableCurrent", instant=end, require_no_member=True)
    row["Inventory"] = inv["value"] if inv else None
    row["Accounts_Payable"] = ap["value"] if ap else None
    for field, fact, section in [
        ("Inventory", inv, "Balance sheet — Inventory at year-end"),
        ("Accounts_Payable", ap, "Balance sheet — Accounts payable at year-end"),
    ]:
        events.append(
            {
                "Period_ID": row["Period_ID"],
                "Field_Name": field,
                "Field_Value": fact["value"] if fact else "",
                "Metric_Label": "reported",
                "Source_File": filing.path.name,
                "Source_Section": section,
                "Notes": f"XBRL {fact['name']}" if fact else "NOT FOUND",
            }
        )

    # Q4 P&L / CF filled later using annual - 9mo YTD
    for f in [
        "Total_Revenue",
        "Automotive_Revenue",
        "Cost_of_Automotive_Revenue",
        "Net_Income",
        "Operating_Cash_Flow",
        "Capital_Expenditures",
    ]:
        row[f] = None

    return row, events


def finalize_cashflow_and_q4(rows: list[dict], events: list[dict]):
    by_id = {r["Period_ID"]: r for r in rows}

    # Q2/Q3 quarterly CF = YTD_q - YTD_{q-1}
    for pid, prev in [("2022Q2", "2022Q1"), ("2022Q3", "2022Q2"), ("2023Q2", "2023Q1"), ("2023Q3", "2023Q2"),
                      ("2024Q2", "2024Q1"), ("2024Q3", "2024Q2"), ("2025Q2", "2025Q1"), ("2025Q3", "2025Q2"),
                      ("2026Q2", "2026Q1")]:
        if pid not in by_id or prev not in by_id:
            continue
        r, p = by_id[pid], by_id[prev]
        for field, ytd in [
            ("Operating_Cash_Flow", "_OCF_YTD"),
            ("Capital_Expenditures", "_Capex_YTD"),
        ]:
            if r.get(ytd) is None or p.get(ytd) is None:
                continue
            val = r[ytd] - p[ytd]
            r[field] = val
            events.append(
                {
                    "Period_ID": pid,
                    "Field_Name": field,
                    "Field_Value": val,
                    "Metric_Label": "calculated",
                    "Source_File": f"{r['Source_File']} minus prior YTD from {p['Source_File']}",
                    "Source_Section": "Calculated quarterly cash-flow = current YTD − prior quarter YTD",
                    "Notes": f"{r[ytd]} - {p[ytd]} = {val}",
                }
            )

    # Q4 = Annual - Q3 YTD (from Q3 10-Q)
    for year in [2022, 2023, 2024, 2025]:
        q4 = f"{year}Q4"
        q3 = f"{year}Q3"
        if q4 not in by_id or q3 not in by_id:
            continue
        r, p = by_id[q4], by_id[q3]
        mapping = [
            ("Total_Revenue", "_Annual_Total_Revenue", "_YTD_Total_Revenue"),
            ("Automotive_Revenue", "_Annual_Automotive_Revenue", "_YTD_Automotive_Revenue"),
            ("Cost_of_Automotive_Revenue", "_Annual_Cost_Auto", "_YTD_Cost_Auto"),
            ("Net_Income", "_Annual_Net_Income", "_YTD_Net_Income"),
            ("Operating_Cash_Flow", "_Annual_OCF", "_OCF_YTD"),
            ("Capital_Expenditures", "_Annual_Capex", "_Capex_YTD"),
        ]
        # Need Q3 YTD P&L as well — extract from Q3 file if not present
        # For income statement, Q3 10-Q has six-month YTD contexts.
        pass

    return rows, events


def attach_q3_ytd_pnl(rows, events):
    """Load six-month YTD P&L from each Q3 10-Q for Q4 calculation."""
    by_id = {r["Period_ID"]: r for r in rows}
    for year in [2022, 2023, 2024, 2025]:
        q3_id = f"{year}Q3"
        q4_id = f"{year}Q4"
        if q3_id not in by_id or q4_id not in by_id:
            continue
        q3 = by_id[q3_id]
        path = RAW / q3["Source_File"]
        facts, _ = load_xbrl(path)
        start, end = f"{year}-01-01", f"{year}-09-30"

        def ytd(name, member=None):
            if member:
                return pick(facts, name, start=start, end=end, member_contains=member)
            return pick(facts, name, start=start, end=end, require_no_member=True)

        ytd_total = ytd("RevenueFromContractWithCustomerExcludingAssessedTax") or ytd("Revenues")
        ytd_auto = (
            ytd("RevenueFromContractWithCustomerExcludingAssessedTax", "AutomotiveRevenuesMember")
            or ytd("AutomotiveRevenues", "AutomotiveRevenuesMember")
            or ytd("AutomotiveRevenues")
        )
        ytd_cost = (
            ytd("CostOfRevenue", "AutomotiveRevenuesMember")
            or ytd("AutomotiveCostOfRevenues", "AutomotiveRevenuesMember")
            or ytd("AutomotiveCostOfRevenues")
        )
        ytd_ni = ytd("NetIncomeLoss")
        q3["_YTD_Total_Revenue"] = ytd_total["value"] if ytd_total else None
        q3["_YTD_Automotive_Revenue"] = ytd_auto["value"] if ytd_auto else None
        q3["_YTD_Cost_Auto"] = ytd_cost["value"] if ytd_cost else None
        q3["_YTD_Net_Income"] = ytd_ni["value"] if ytd_ni else None

        q4 = by_id[q4_id]
        for field, ann, ytdf in [
            ("Total_Revenue", "_Annual_Total_Revenue", "_YTD_Total_Revenue"),
            ("Automotive_Revenue", "_Annual_Automotive_Revenue", "_YTD_Automotive_Revenue"),
            ("Cost_of_Automotive_Revenue", "_Annual_Cost_Auto", "_YTD_Cost_Auto"),
            ("Net_Income", "_Annual_Net_Income", "_YTD_Net_Income"),
            ("Operating_Cash_Flow", "_Annual_OCF", "_OCF_YTD"),
            ("Capital_Expenditures", "_Annual_Capex", "_Capex_YTD"),
        ]:
            a, y = q4.get(ann), q3.get(ytdf)
            if a is None or y is None:
                continue
            val = a - y
            q4[field] = val
            events.append(
                {
                    "Period_ID": q4_id,
                    "Field_Name": field,
                    "Field_Value": val,
                    "Metric_Label": "calculated",
                    "Source_File": f"{q4['Source_File']} annual minus {q3['Source_File']} 9-mo YTD",
                    "Source_Section": "Q4 = fiscal year total − nine months ended Sep 30",
                    "Notes": f"{a} - {y} = {val}",
                }
            )
    return rows, events


def main():
    files = sorted(RAW.glob("10-*.htm"))
    rows = []
    events = []
    for p in files:
        filing = parse_filename(p)
        print("Processing", p.name)
        if filing.form == "10-Q":
            row, ev = extract_from_10q(filing)
        else:
            row, ev = extract_from_10k(filing)
        rows.append(row)
        events.extend(ev)

    rows, events = finalize_cashflow_and_q4(rows, events)
    rows, events = attach_q3_ytd_pnl(rows, events)

    # computed margins
    for r in rows:
        if r.get("Automotive_Revenue") and r.get("Cost_of_Automotive_Revenue") is not None:
            r["Automotive_Gross_Margin"] = (
                r["Automotive_Revenue"] - r["Cost_of_Automotive_Revenue"]
            ) / r["Automotive_Revenue"]
            events.append(
                {
                    "Period_ID": r["Period_ID"],
                    "Field_Name": "Automotive_Gross_Margin",
                    "Field_Value": r["Automotive_Gross_Margin"],
                    "Metric_Label": "calculated",
                    "Source_File": r["Source_File"],
                    "Source_Section": "(Automotive_Revenue - Cost_of_Automotive_Revenue) / Automotive_Revenue",
                    "Notes": "",
                }
            )
        else:
            r["Automotive_Gross_Margin"] = None

    fieldnames = [
        "Period_ID",
        "Reporting_Period",
        "Form",
        "Report_Date",
        "Total_Revenue",
        "Automotive_Revenue",
        "Cost_of_Automotive_Revenue",
        "Automotive_Gross_Margin",
        "Inventory",
        "Accounts_Payable",
        "Capital_Expenditures",
        "Operating_Cash_Flow",
        "Net_Income",
        "CashFlow_Basis",
        "Unit",
        "Source_File",
    ]
    rows_sorted = sorted(rows, key=lambda r: r["Period_ID"])
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows_sorted:
            w.writerow(r)

    log_fields = [
        "Period_ID",
        "Field_Name",
        "Field_Value",
        "Metric_Label",
        "Source_File",
        "Source_Section",
        "Notes",
    ]
    with LOG.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=log_fields)
        w.writeheader()
        w.writerows(events)

    META.write_text(json.dumps(rows_sorted, indent=2, default=str), encoding="utf-8")
    DOC.write_text(
        """# Fact_Financials notes

## Units
All monetary fields are in **USD millions**, matching Tesla’s iXBRL `scale=\"6\"` presentation.

## Period grain
One row per calendar quarter `YYYYQn` for Q1 2022–Q2 2026.

## Reported vs calculated
- **Reported:** line items taken directly from 10-Q three-month columns or balance-sheet period-end; Q1 OCF/Capex (YTD = quarter); 10-K annual totals (stored in extraction intermediates).
- **Calculated:**
  - Q2/Q3 `Operating_Cash_Flow` and `Capital_Expenditures` = current YTD − prior quarter YTD
  - Q4 P&L and cash-flow fields = fiscal-year 10-K total − nine-month YTD from Q3 10-Q
  - `Automotive_Gross_Margin` = (Automotive_Revenue − Cost_of_Automotive_Revenue) / Automotive_Revenue

## Caveats
- Automotive revenue uses the `AutomotiveRevenuesMember` axis (sales + leasing + credits as Tesla aggregates under automotive revenues).
- Cost of automotive revenue uses `CostOfRevenue` with `AutomotiveRevenuesMember`.
- Missing iXBRL matches are left null and logged — never interpolated.
""",
        encoding="utf-8",
    )
    print(f"Wrote {OUT} ({len(rows_sorted)} rows), {LOG} ({len(events)} events)")
    for r in rows_sorted:
        print(
            r["Period_ID"],
            "Rev",
            r.get("Total_Revenue"),
            "Auto",
            r.get("Automotive_Revenue"),
            "Inv",
            r.get("Inventory"),
            "OCF",
            r.get("Operating_Cash_Flow"),
            "NI",
            r.get("Net_Income"),
        )


if __name__ == "__main__":
    main()
