"""Write SEC 10-Q/10-K primary HTML files from a browser CDP JSON response."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "raw" / "sec_edgar"
META_PATH = ROOT / "data" / "reference" / "_tmp_sec_meta.json"


def main(cdp_path: str) -> None:
    raw = json.loads(Path(cdp_path).read_text(encoding="utf-8"))
    items = json.loads(raw["result"]["value"])
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    existing = []
    if META_PATH.exists():
        existing = json.loads(META_PATH.read_text(encoding="utf-8"))

    by_name = {m["filename"]: m for m in existing}
    for it in items:
        path = OUT_DIR / it["filename"]
        path.write_text(it["content"], encoding="utf-8", newline="")
        meta = {k: it[k] for k in ["form", "period", "reportDate", "filingDate", "accession", "url", "status", "bytes", "filename"]}
        by_name[it["filename"]] = meta
        print(f"OK {it['filename']} ({it['bytes']} bytes)")

    META_PATH.write_text(json.dumps(list(by_name.values()), indent=2), encoding="utf-8")
    print(f"total meta rows: {len(by_name)}")


if __name__ == "__main__":
    main(sys.argv[1])
