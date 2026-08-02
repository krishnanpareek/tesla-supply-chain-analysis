# scripts/

Helper scripts used during data acquisition. They do not hardcode credentials.

| Script | Purpose |
|--------|---------|
| `write_ir_from_cdp.py` | Persist Tesla IR exhibit HTML from a browser CDP JSON capture |
| `write_sec_from_cdp.py` | Persist SEC 10-Q/10-K HTML from a browser CDP JSON capture |
| `build_download_log.py` | Build `data/reference/download_log.md` from download meta JSON |
| `extract_fact_tesla_operations.py` | Extract `Fact_Tesla_Operations` + extraction log from IR exhibits |

Related: regenerate Page 2 embed with  
`python -c "import json,pathlib; p=pathlib.Path('data/processed/Fact_Tesla_Operations.csv'); ..."`  
or re-run the export steps documented in `powerbi/README.md` when the fact table changes.
