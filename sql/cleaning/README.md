# sql/cleaning/

Data cleaning and transformation queries.

Each script should:

1. Reference the Source_ID(s) from the source inventory
2. Document null-handling rules (no silent interpolation)
3. Label derived fields as calculated / estimated / modeled where applicable
4. Write outputs conceptually to `data/processed/` (or load targets documented in methodology)
