"""Build download_log.md from IR/SEC meta JSON written during Phase 3 downloads."""
from __future__ import annotations

import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
IR_META = ROOT / "data" / "reference" / "_tmp_ir_meta.json"
SEC_META = ROOT / "data" / "reference" / "_tmp_sec_meta.json"
OUT = ROOT / "data" / "reference" / "download_log.md"

PERIOD_BOUNDS = {
    "Q1": ("01-01", "03-31"),
    "Q2": ("04-01", "06-30"),
    "Q3": ("07-01", "09-30"),
    "Q4": ("10-01", "12-31"),
}


def ir_reporting_period(period_key: str) -> str:
    # period_key like Q1_2022
    q, year = period_key.split("_")
    start_md, end_md = PERIOD_BOUNDS[q]
    return f"{year}-{start_md} to {year}-{end_md} ({q} {year})"


def main() -> None:
    ir = json.loads(IR_META.read_text(encoding="utf-8"))
    sec = json.loads(SEC_META.read_text(encoding="utf-8"))
    access = date.today().isoformat()

    lines = [
        "# Download Log",
        "",
        "Exact local file inventory for Phase 3 raw downloads.",
        "",
        f"**Access / download date:** {access}",
        "",
        "**Scope:** Tesla IR quarterly production/delivery releases Q1 2022–Q2 2026, and corresponding SEC Forms 10-Q / 10-K for the same window.",
        "",
        "**Important:** No fact values were extracted into `Fact_Tesla_Operations` in this phase. This log is provenance only.",
        "",
        "## Method notes",
        "",
        "- Tesla IR production/delivery press releases are filed with the SEC as Form **8-K Exhibit 99.1** (Item 2.02). Local copies are those filed HTML exhibits (same operational figures published via Tesla IR).",
        "- `Publication_Date` for IR rows = SEC **filing date** of the related 8-K (verified via EDGAR company filings atom feed).",
        "- `Reporting_Period` for IR rows = calendar quarter covered by the release title / narrative.",
        "- SEC financial rows use EDGAR filing date as `Publication_Date` and the form period end as `Reporting_Period_End`.",
        "- Large SEC HTML filings under `data/raw/sec_edgar/` are gitignored; URLs below are the source of truth for re-download.",
        "",
        "---",
        "",
        "## A. Tesla IR — Production / Deliveries / Deployments (8-K EX-99.1)",
        "",
        "| Source_ID | Local_Filename | Reporting_Period | Publication_Date (SEC filing date) | Accession | Source_URL | HTTP_Status | Bytes |",
        "|-----------|----------------|------------------|------------------------------------|-----------|------------|-------------|-------|",
    ]

    for row in sorted(ir, key=lambda r: r["period"]):
        lines.append(
            "| {sid} | `{fn}` | {rp} | {pub} | {acc} | {url} | {st} | {b} |".format(
                sid=f"SRC-TESLA-IR-001-{row['period']}",
                fn=row["filename"],
                rp=ir_reporting_period(row["period"]),
                pub=row["filingDate"],
                acc=row["accession"],
                url=row["url"],
                st=row["status"],
                b=row["bytes"],
            )
        )

    lines.extend(
        [
            "",
            f"**IR file count:** {len(ir)} (expected 18)",
            "",
            "---",
            "",
            "## B. SEC EDGAR — Forms 10-Q / 10-K",
            "",
            "| Source_ID | Form | Local_Filename | Reporting_Period_End | Publication_Date (filing date) | Accession | Source_URL | HTTP_Status | Bytes |",
            "|-----------|------|----------------|----------------------|--------------------------------|-----------|------------|-------------|-------|",
        ]
    )

    for row in sorted(sec, key=lambda r: r["reportDate"]):
        lines.append(
            "| {sid} | {form} | `{fn}` | {rd} | {pub} | {acc} | {url} | {st} | {b} |".format(
                sid=f"SRC-SEC-{row['form']}-{row['period']}",
                form=row["form"],
                fn=row["filename"],
                rd=row["reportDate"],
                pub=row["filingDate"],
                acc=row["accession"],
                url=row["url"],
                st=row["status"],
                b=row["bytes"],
            )
        )

    lines.extend(
        [
            "",
            f"**SEC file count:** {len(sec)} (expected 18: fourteen 10-Q + four 10-K)",
            "",
            "### Period coverage map",
            "",
            "| Ops quarter | IR release publication | Matching SEC form for financials |",
            "|-------------|------------------------|----------------------------------|",
            "| Q1 2022 | 2022-04-04 | 10-Q period ended 2022-03-31 (filed 2022-04-25) |",
            "| Q2 2022 | 2022-07-05 | 10-Q period ended 2022-06-30 (filed 2022-07-25) |",
            "| Q3 2022 | 2022-10-03 | 10-Q period ended 2022-09-30 (filed 2022-10-24) |",
            "| Q4 2022 | 2023-01-03 | 10-K year ended 2022-12-31 (filed 2023-01-31) |",
            "| Q1 2023 | 2023-04-03 | 10-Q period ended 2023-03-31 (filed 2023-04-24) |",
            "| Q2 2023 | 2023-07-03 | 10-Q period ended 2023-06-30 (filed 2023-07-24) |",
            "| Q3 2023 | 2023-10-02 | 10-Q period ended 2023-09-30 (filed 2023-10-23) |",
            "| Q4 2023 | 2024-01-02 | 10-K year ended 2023-12-31 (filed 2024-01-29) |",
            "| Q1 2024 | 2024-04-02 | 10-Q period ended 2024-03-31 (filed 2024-04-24) |",
            "| Q2 2024 | 2024-07-02 | 10-Q period ended 2024-06-30 (filed 2024-07-24) |",
            "| Q3 2024 | 2024-10-02 | 10-Q period ended 2024-09-30 (filed 2024-10-24) |",
            "| Q4 2024 | 2025-01-02 | 10-K year ended 2024-12-31 (filed 2025-01-30) |",
            "| Q1 2025 | 2025-04-02 | 10-Q period ended 2025-03-31 (filed 2025-04-23) |",
            "| Q2 2025 | 2025-07-02 | 10-Q period ended 2025-06-30 (filed 2025-07-24) |",
            "| Q3 2025 | 2025-10-02 | 10-Q period ended 2025-09-30 (filed 2025-10-23) |",
            "| Q4 2025 | 2026-01-02 | 10-K year ended 2025-12-31 (filed 2026-01-29) |",
            "| Q1 2026 | 2026-04-02 | 10-Q period ended 2026-03-31 (filed 2026-04-23) |",
            "| Q2 2026 | 2026-07-02 | 10-Q period ended 2026-06-30 (filed 2026-07-23) |",
            "",
            "## Limitations",
            "",
            "- Local IR copies are SEC-filed HTML exhibits, not the ir.tesla.com PDF mirror (Akamai blocked automated PDF pulls from this environment). Figures are the same company-reported release content.",
            "- SEC primary documents are iXBRL HTML; presentation markup is verbose. Extraction scripts must target reported line items carefully.",
            "- No values from these files have been loaded into fact tables yet.",
            "",
        ]
    )

    OUT.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {OUT}")


if __name__ == "__main__":
    main()
