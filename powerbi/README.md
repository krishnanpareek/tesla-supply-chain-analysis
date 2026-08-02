# powerbi/

Power BI dashboard artifacts for the six-page report.

## Page 2 — Production & Delivery Performance (built)

| Artifact | Path |
|----------|------|
| Page design spec | `pages/page02_production_delivery_performance.md` |
| DAX measures + tooltip citation templates | `dax/Page02_Production_Delivery_Measures.md` |
| Browser prototype (demoable now) | `page02_production_delivery_performance.html` |
| Embedded fact JSON for prototype | `_embed_data.js`, `data/Fact_Tesla_Operations.json` |

### How to view Page 2 today

Open `page02_production_delivery_performance.html` in a browser (double-click or Live Server). Hover KPIs/chart points for Source_File citations.

### How to build the .pbix in Power BI Desktop

1. Load `../data/processed/Fact_Tesla_Operations.csv`
2. Implement measures from `dax/Page02_Production_Delivery_Measures.md`
3. Follow layout/filters/tooltips in `pages/page02_production_delivery_performance.md`
4. Save as `Tesla_Supply_Chain_Analysis.pbix` in this folder
5. Export a PNG to `../visuals/page02_production_delivery_performance.png`

`*.pbix.bak` files are gitignored.

## Remaining pages

3 Financial · 4 Quality · 5 EV Market · 6 Battery Materials · 1 Executive Overview (last)
