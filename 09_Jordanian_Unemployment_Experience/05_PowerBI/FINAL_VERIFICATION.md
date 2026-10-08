# Final verification (2026-10-08, Power BI Desktop 2.158.1177.0)

| Check | Result |
|---|---|
| Model loads, refresh Full | PASS (7 tables, 13 measures; all 9 SVG measures compute; largest 12.2k chars) |
| Plateau computed from data | 21.0–21.5, 10 quarters |
| Latest Jordanian rate | 21.0% (Q2 2026) |
| Employed / unemployed change 2020→2025 | +255,854 / +27,570 |
| National derived annual 2025 rate | 21.31% |
| Governorate shares: top 3 | 70.3% (Amman, Irbid, Zarqa); governorate counts sum to 431,677 vs national 431,675 (2-person rounding in the PxWeb breakdown) |
| Ma'an derived 2025 rate | 28.82% |
| 100-dot lenses | Sex 66/34, Age 35/30/25/10, Education 45/8/8/39, each sums to 100 |
| Click a quarter (P1) | PASS: hero, chart marker and caption update |
| Lens switch (P2) | PASS: Sex, Age, Education re-colour the grid and labels |
| Select governorate by disc or ledger row, select again to clear (P3) | PASS: map dims others, row highlights, panel updates, nationwide state returns |
| Navigation buttons and chapter strip | PASS (Ctrl+click in edit mode) |
| No scrollbars / clipping after padding fix | PASS |
| PDF export of all three pages | PASS (`screens/desktop_export_*.png`, 144 dpi) |

## Known limitations
- Governorate rates, annual 2025 rate and youth rate are derived from DoS counts, not DoS-published rates; DoS gives no sampling error.
- Four quarterly points (male and female, 2023 Q2 and 2024 Q2) are DoS chart labels only (hollow markers).
- Scatter click targets are calibrated to the 100 % canvas of Desktop (insets 5/10/29/30 px); the Service may differ by a few pixels.
- Georgia and Segoe UI come from the viewer's system (Windows); other platforms may substitute fonts.
- No mobile layout: desktop 1440×900, fit to page.
- Page-level text (headlines) is static artwork by design; all figures are data-driven.
- Deneb, bookmarks and drill-through were not used.
