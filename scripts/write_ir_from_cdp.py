"""Write Tesla IR production exhibit files from a browser CDP JSON response."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "data" / "raw" / "tesla_ir"


def main(cdp_path: str) -> None:
    raw = json.loads(Path(cdp_path).read_text(encoding="utf-8"))
    items = json.loads(raw["result"]["value"])
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for p in OUT_DIR.glob("test_*"):
        p.unlink()
    meta = []
    for it in items:
        path = OUT_DIR / it["filename"]
        path.write_text(it["content"], encoding="utf-8", newline="")
        meta.append({k: it[k] for k in ["period", "filingDate", "accession", "url", "status", "bytes", "filename"]})
        print(f"OK {it['filename']} ({it['bytes']} bytes)")
    meta_path = ROOT / "data" / "reference" / "_tmp_ir_meta.json"
    meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
    print(f"wrote {len(meta)} files; meta -> {meta_path}")


if __name__ == "__main__":
    main(sys.argv[1])
