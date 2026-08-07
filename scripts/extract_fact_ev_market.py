"""Build Fact_EV_Market from CEC New ZEV Sales, LDV sales/shares, and EV chargers."""
from __future__ import annotations

import csv
import re
from datetime import date
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
CEC = ROOT / "data" / "raw" / "cec"
PROC = ROOT / "data" / "processed"
REF = ROOT / "data" / "reference"

ZEV_FILE = "New_ZEV_Sales_Last_updated_07-17-2026_ada.xlsx"
LDV_FILE = "LDV_Sales_and_Shares_Last_updated_07-17-2026_ada.xlsx"
CHG_FILE = "EV_Chargers_Last_updated_04-21-2026_ada.xlsx"

ZEV_URL = "https://www.energy.ca.gov/filebrowser/download/9805?fid=9805"
LDV_URL = "https://www.energy.ca.gov/filebrowser/download/9806?fid=9806"
CHG_URL = "https://www.energy.ca.gov/filebrowser/download/9662?fid=9662"
HUB = "https://www.energy.ca.gov/files/zev-and-infrastructure-stats-data"


def period_id(year: int, quarter: int) -> str:
    return f"{year}Q{quarter}"


def main() -> None:
    snap = date.today().isoformat()
    zev_path = CEC / ZEV_FILE
    readme = pd.read_excel(zev_path, sheet_name="Readme", header=None)
    data_as_of = None
    for v in readme[0].dropna().astype(str):
        if "Data as of" in v:
            data_as_of = v.replace("Data as of", "").strip(" :")
            break

    county = pd.read_excel(zev_path, sheet_name="County")
    county.columns = [str(c).strip() for c in county.columns]
    # Aggregate statewide by year/quarter/make
    county["Number of Vehicles"] = pd.to_numeric(county["Number of Vehicles"], errors="coerce").fillna(0)
    county["Data Year"] = county["Data Year"].astype(int)
    county["Quarter"] = county["Quarter"].astype(int)

    # Filter to project window optional — keep full history for charts, page can filter
    g = county.groupby(["Data Year", "Quarter", "MAKE"], as_index=False)["Number of Vehicles"].sum()
    zev_tot = county.groupby(["Data Year", "Quarter"], as_index=False)["Number of Vehicles"].sum()
    zev_tot = zev_tot.rename(columns={"Number of Vehicles": "Total_ZEV_Sales"})
    tesla = g[g["MAKE"].str.upper() == "TESLA"].rename(columns={"Number of Vehicles": "Tesla_ZEV_Sales", "MAKE": "_m"})
    merged = zev_tot.merge(
        tesla[["Data Year", "Quarter", "Tesla_ZEV_Sales"]],
        on=["Data Year", "Quarter"],
        how="left",
    )
    merged["Tesla_ZEV_Sales"] = merged["Tesla_ZEV_Sales"].fillna(0)

    ldv = pd.read_excel(CEC / LDV_FILE, sheet_name="Data")
    ldv.columns = [str(c).strip() for c in ldv.columns]
    for col in ["ZEV Sales", "Total LDV Sales"]:
        ldv[col] = pd.to_numeric(ldv[col], errors="coerce").fillna(0)
    ldv_q = ldv.groupby(["Data Year", "Quarter"], as_index=False).agg(
        {"ZEV Sales": "sum", "Total LDV Sales": "sum"}
    )
    ldv_q = ldv_q.rename(columns={"ZEV Sales": "LDV_ZEV_Sales", "Total LDV Sales": "Total_LDV_Sales"})

    out = merged.merge(ldv_q, on=["Data Year", "Quarter"], how="left")
    rows = []
    events = []
    for _, r in out.iterrows():
        y, q = int(r["Data Year"]), int(r["Quarter"])
        tesla_n = int(r["Tesla_ZEV_Sales"])
        zev_n = int(r["Total_ZEV_Sales"])
        ldv_zev = int(r["LDV_ZEV_Sales"]) if pd.notna(r["LDV_ZEV_Sales"]) else None
        ldv_tot = int(r["Total_LDV_Sales"]) if pd.notna(r["Total_LDV_Sales"]) else None
        tesla_share = (tesla_n / zev_n) if zev_n else None
        zev_share = (ldv_zev / ldv_tot) if ldv_tot else None
        pid = period_id(y, q)
        row = {
            "Period_ID": pid,
            "Data_Year": y,
            "Quarter": q,
            "Tesla_ZEV_Sales_CA": tesla_n,
            "Total_ZEV_Sales_CA": zev_n,
            "Tesla_Share_of_ZEV_Sales": tesla_share,
            "Total_LDV_Sales_CA": ldv_tot,
            "ZEV_Share_of_LDV_Sales": zev_share,
            "Geography": "California",
            "Data_As_Of": data_as_of or "",
            "Source_File_ZEV": ZEV_FILE,
            "Source_File_LDV": LDV_FILE,
            "Source_URL_ZEV": ZEV_URL,
            "Source_URL_LDV": LDV_URL,
            "Source_ID": "SRC-CEC-001",
            "Hub_URL": HUB,
            "Snapshot_Date": snap,
            "Metric_Label_Sales": "reported",
            "Metric_Label_Shares": "calculated",
            "Notes": "CEC new ZEV sales inferred from DMV registrations; methodology updated 2023 and 2025 — YoY compare with care",
        }
        rows.append(row)
        events.append(
            {
                "Period_ID": pid,
                "Field_Name": "Tesla_ZEV_Sales_CA",
                "Field_Value": tesla_n,
                "Metric_Label": "reported",
                "Source_File": ZEV_FILE,
                "Source_URL": ZEV_URL,
                "Notes": f"Sum of County sheet Number of Vehicles where MAKE=Tesla; Data as of {data_as_of}",
            }
        )

    # Chargers: statewide totals by snapshot sheet
    chg_path = CEC / CHG_FILE
    xl = pd.ExcelFile(chg_path)
    charger_rows = []
    for sheet in xl.sheet_names:
        if sheet.lower() in ("info", "readme"):
            continue
        df = pd.read_excel(chg_path, sheet_name=sheet)
        df.columns = [str(c).strip() for c in df.columns]
        if "Total" not in df.columns:
            continue
        # Drop possible statewide duplicate rows named Total
        dff = df[~df["County"].astype(str).str.lower().isin(["total", "statewide", "nan"])].copy()
        for col in df.columns:
            if col == "County":
                continue
            dff[col] = pd.to_numeric(dff[col], errors="coerce").fillna(0)
        total = int(dff["Total"].sum())
        pub_l2 = int(dff.get("Public Level 2", pd.Series([0])).sum()) if "Public Level 2" in dff else None
        pub_dc = int(dff.get("Public DC Fast", pd.Series([0])).sum()) if "Public DC Fast" in dff else None
        charger_rows.append(
            {
                "Snapshot_Label": sheet,
                "Public_Level_2": pub_l2,
                "Public_DC_Fast": pub_dc,
                "Total_Chargers": total,
                "Geography": "California",
                "Source_File": CHG_FILE,
                "Source_URL": CHG_URL,
                "Source_ID": "SRC-CEC-002",
                "Hub_URL": HUB,
                "Data_As_Of_File": "December 31, 2025 (Info sheet)",
                "Snapshot_Date": snap,
                "Metric_Label": "reported",
            }
        )

    PROC.mkdir(parents=True, exist_ok=True)
    REF.mkdir(parents=True, exist_ok=True)
    with (PROC / "Fact_EV_Market.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: (r["Data_Year"], r["Quarter"])))
    with (PROC / "Fact_EV_Chargers_CA.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(charger_rows[0].keys()))
        w.writeheader()
        w.writerows(charger_rows)
    with (REF / "Fact_EV_Market_extraction_log.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(events[0].keys()))
        w.writeheader()
        w.writerows(events)

    # recent window print
    recent = [r for r in rows if r["Data_Year"] >= 2022]
    print(f"Fact_EV_Market {len(rows)} quarters (2022+ {len(recent)})")
    print(f"Chargers snapshots {len(charger_rows)}")
    last = sorted(rows, key=lambda r: (r["Data_Year"], r["Quarter"]))[-1]
    print(
        f"Latest {last['Period_ID']} Tesla {last['Tesla_ZEV_Sales_CA']} / ZEV {last['Total_ZEV_Sales_CA']} "
        f"share {last['Tesla_Share_of_ZEV_Sales']:.3f}" if last["Tesla_Share_of_ZEV_Sales"] else last
    )


if __name__ == "__main__":
    main()
