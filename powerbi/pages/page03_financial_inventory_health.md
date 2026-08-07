# Page 3 — Financial & Inventory Health

**Deliverable:** `dashboard/page03_financial_inventory_health.html`  
**Fact table:** `data/processed/Fact_Financials.csv`  
**DAX reference:** `powerbi/dax/Page03_Financial_Inventory_Measures.md`

## Purpose

Show Tesla’s public financial and inventory health using SEC 10-Q / 10-K extracts, with full citation on every displayed number.

## Layout

1. Period selector + filing / cash-flow basis pills  
2. KPI row 1: Total Revenue, Automotive Revenue, Automotive Gross Margin, Net Income  
3. KPI row 2: Inventory, Inventory Days (Est.), Operating Cash Flow, Free Cash Flow  
4. Charts: Revenue (total vs auto), Auto GM, Inventory, OCF/CapEx/FCF  
5. Detail table with Source_File  
6. Callout: inventory ≠ vehicle units; Q4/YTD calculation basis

## Metric labels

| Metric | Label |
|--------|-------|
| Revenue, Auto revenue, Inventory, AP | Reported (Q4 P&L calculated) |
| Auto GM, GP, FCF | Calculated |
| Inventory days | Estimated |
| OCF / CapEx | Per `OCF_Capex_Metric_Label` |
