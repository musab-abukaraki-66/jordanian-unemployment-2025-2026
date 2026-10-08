# Jordanian Unemployment 2025–2026 — Power BI report

Open `pbip/JordanUnemployment.pbip` in Power BI Desktop (2.158). After opening, the model is empty until you press **Refresh** (data = `data/*.csv`, path parameter `DataFolder`; change it if the folder moves).

## Pages (1440×900, three chapters)
1. **The number** — "Unemployment among Jordanians has not moved in ten quarters." 18-quarter Jordanian line (click a point to read any quarter), the 10-quarter plateau computed from data, three-row reconciliation (all residents 16.1 / Jordanians 21.0 / Jordanian women 30.3), and the people behind the rate (+255,854 employed, +27,570 unemployed, 2020→2025).
2. **The people** — 100 unemployed Jordanians by Sex / Age / Education (lens switch) beside the rate per 100 in the labour force (18 men, 33 women).
3. **The places** — flat governorate map (colour = derived 2025 rate, disc area = people), clickable ledger, panel that explains the selected governorate. Select again to clear.
Navigation: chapter strip + "Next" button. In Desktop edit mode use **Ctrl+click** on buttons; in Reading view / Service a normal click works.

## Truth rules
Population is Jordanian citizens only. Every number comes from `data/` (built from `08_Jordanian_Unemployment_Truth` by `scripts/b01_data.py`). Labels on screen: DoS PUBLISHED · DERIVED FROM DoS COUNTS · LIMITED EVIDENCE · NOT A DoS-PUBLISHED GOVERNORATE RATE. Hollow chart points are DoS chart labels only. Provenance: `../02_Data/quarterly_series_provenance.csv`, `../02_Data/evidence_additions_Q2_2026.csv`.

## How it is built
`scripts/b01_data.py` (tables) → `b03_model.py` (TMDL, 13 DAX measures, SVG via data URIs) → `b02_art.py` (static chrome wallpapers) → `b04_report.py` (PBIR). Native visuals: 9 image tables (SVG measures), 3 transparent-style scatters (click targets), 1 slicer, action buttons. Fonts: Georgia, Segoe UI, Segoe UI Semibold. Generated files are never hand-edited; rerun the scripts (close Desktop first).
