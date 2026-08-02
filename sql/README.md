# sql/

SQL assets for the star-schema warehouse and analysis layer.

| Subfolder | Purpose |
|-----------|---------|
| `schema/` | DDL for fact and dimension tables |
| `cleaning/` | Transformation / cleaning queries from raw to processed |
| `analysis/` | Analytic queries (trends, growth, risk, etc.) |

No credentials should appear in any SQL script. Connection details stay local.
