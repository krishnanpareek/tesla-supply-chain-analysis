# Portfolio Materials

Use these as copy-ready starting points. Keep the accuracy constraints:

- Deliverable is an **HTML / CSS / JavaScript** dashboard (not Power BI / not a `.pbix`).
- **Public data only** — no Tesla-confidential access.
- Do not claim DAX / Power BI skills *from this project*; in-repo DAX notes are documentation of KPI logic only.

---

## Resume bullets (pick 3–5)

- Built a six-page interactive HTML/CSS/JS supply-chain dashboard analyzing Tesla production, deliveries, SEC financials/inventory, NHTSA recalls & complaints, California ZEV market share, and USGS battery-mineral concentration — using **public data only** with field-level reported/calculated/estimated labels.
- Engineered Python extracts into analysis-ready fact tables (operations, financials, NHTSA flat files, CEC ZEV/chargers, USGS MCS) with source-file citations on every KPI for interview-ready traceability.
- Defined and enforced metric guardrails that prevent common misreads: production–delivery gap ≠ inventory; CEC charger totals split into public vs shared-private **ports**; NHTSA complaints treated as allegations; USGS 2025 mineral figures labeled estimated when Notes say “Estimated.”
- Reconciled conflicting public sources (e.g., CEC export revisions vs press totals; NHTSA API under-counts vs ODI flat files) and documented limitations so headline numbers survive technical interview scrutiny.
- Produced portfolio documentation (executive summary, data dictionary, limitations, source inventory) suitable for supply chain / demand planning / inventory / procurement analyst applications.

**Skills line (accurate):** Python, data cleaning, public financial & regulatory data, HTML/CSS/JavaScript, metric design, documentation, supply-chain analytics framing.

**Do not list for this project alone:** Power BI, DAX, Tableau (unless used elsewhere), “Tesla intern tools,” or confidential supplier data.

---

## LinkedIn post

Built a public-data Tesla supply-chain analytics dashboard — six pages covering production & deliveries, SEC financial/inventory health, NHTSA recall & complaint risk, California ZEV market position, and USGS battery-material concentration.

What I cared about most wasn’t a flashy chart. It was **definitional accuracy**:

- Production–delivery gap is not unsold inventory  
- California ZEV share is not national deliveries  
- Charging KPIs are public **ports**, not stations and not shared-private totals  
- NHTSA complaints are allegations (flat-file backed)  
- USGS 2025 mineral stats are often estimated — and labeled that way  

Stack: Python fact extracts → CSV star-schema tables → HTML/CSS/JS dashboard with hover citations to source files. No Tesla-confidential data. No fabricated numbers.

Live dashboard: https://krishnanpareek.github.io/tesla-supply-chain-analysis/  
Code: https://github.com/krishnanpareek/tesla-supply-chain-analysis

If you work in supply chain, demand planning, inventory, or procurement analytics and like projects that survive “where did that number come from?” — I’d love feedback.

#SupplyChain #DataAnalytics #Python #PublicData #PortfolioProject

---

## Two-minute interview explanation

**0:00–0:25 — Hook**  
“I built a six-page public-data dashboard on Tesla supply-chain signals — production and deliveries, financial inventory health, quality/recalls, California EV market, and battery-material risk. Everything is from public sources only: Tesla IR and SEC filings, NHTSA flat files, the California Energy Commission, and USGS. There’s no confidential Tesla data.”

**0:25–0:55 — What you built**  
“The primary deliverable is an HTML, CSS, and JavaScript dashboard you can open in a browser. Behind it, Python scripts extract fact tables — operations, financials, recalls, complaints, CA ZEV sales, charging ports, and mineral statistics — and every KPI hover shows the source file and date. Metrics are labeled reported, calculated, or estimated.”

**0:55–1:25 — Why it’s credible**  
“I focused on definitions that usually trip people up. The production–delivery gap is produced minus delivered, not inventory. Charging figures are public ports, because the CEC total also includes shared-private ports and would roughly double a public-availability number. Complaints come from NHTSA flat files as allegations. USGS 2025 lithium production and import reliance are estimated, and the dashboard says so.”

**1:25–1:50 — Business angle**  
“For a supply-chain or demand-planning role, the point isn’t predicting Tesla’s next quarter — it’s showing I can integrate messy public sources, keep a clean metric dictionary, and present numbers that survive scrutiny. Page 1 is the executive snapshot; Pages 2 through 6 are the detail.”

**1:50–2:00 — Close**  
“Happy to walk through any page or a specific source lineage — for example how the 183,000 California public ports figure is built, or why lithium is labeled estimated.”

### Likely follow-ups (short answers)

| Question | Answer |
|----------|--------|
| Why not Power BI? | “I shipped a portable HTML dashboard so reviewers don’t need Desktop. I documented KPI logic in measure notes, but I’m not claiming a `.pbix` for this repo.” |
| Is the gap inventory? | “No. It’s produced minus delivered. Inventory dollars are a separate SEC line on Page 3.” |
| Are you saying Tesla has a cobalt shortage? | “No. USGS shows market concentration and U.S. import reliance — structural risk signals, not Tesla purchase volumes.” |
| Why California only for EV share? | “That’s what CEC publishes as new ZEV sales. I label it California and don’t call it national share.” |
