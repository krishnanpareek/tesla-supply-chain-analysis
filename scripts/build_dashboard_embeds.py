"""Build dashboard/data/*.js embeds from processed CSVs."""
from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dashboard" / "data"


def load_csv(path: Path) -> list[dict]:
    rows = list(csv.DictReader(path.open(encoding="utf-8")))
    out = []
    for r in rows:
        o = {}
        for k, v in r.items():
            if v is None or v == "":
                o[k] = None
                continue
            try:
                if any(ch in v for ch in ".eE") or v.isdigit() or (v.startswith("-") and v[1:].replace(".", "", 1).isdigit()):
                    o[k] = float(v)
                else:
                    o[k] = v
            except ValueError:
                o[k] = v
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


def unique_recalls(rows: list[dict]) -> list[dict]:
    seen = set()
    out = []
    for r in sorted(rows, key=lambda x: x.get("Report_Received_Date") or "", reverse=True):
        c = r.get("Campaign_Number")
        if c in seen:
            continue
        seen.add(c)
        out.append(r)
    return out


def main() -> None:
    ops = load_csv(ROOT / "data" / "processed" / "Fact_Tesla_Operations.csv")
    write_js("fact_tesla_operations", "FACT_TESLA_OPS", ops)

    fin = load_csv(ROOT / "data" / "processed" / "Fact_Financials.csv")
    write_js("fact_financials", "FACT_FINANCIALS", fin)

    annual = load_csv(ROOT / "data" / "processed" / "Fact_NHTSA_Annual.csv")
    write_js("fact_nhtsa_annual", "FACT_NHTSA_ANNUAL", annual)

    by_model = load_csv(ROOT / "data" / "processed" / "Fact_NHTSA_By_Model.csv")
    write_js("fact_nhtsa_by_model", "FACT_NHTSA_BY_MODEL", by_model)

    recalls = unique_recalls(load_csv(ROOT / "data" / "processed" / "Fact_Recalls.csv"))
    write_js("fact_recalls", "FACT_RECALLS", recalls)


if __name__ == "__main__":
    main()
