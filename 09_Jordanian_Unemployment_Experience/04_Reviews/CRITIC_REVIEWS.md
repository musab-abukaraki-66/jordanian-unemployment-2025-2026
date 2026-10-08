# Critic reviews (six independent read-only agents; synthesis by lead)

## 1 Data truth
- Blocker: age lens 36/30/24/10 was wrong. Fixed to 35/30/25/10 (largest remainder of 35.65 / 29.93 / 24.65 / 9.78).
- Blocker: six female quarterly points and the Q2 2026 all-resident / non-Jordanian / all-women rates were not in the evidence table. Fixed by `02_Data/quarterly_series_provenance.csv` and `02_Data/evidence_additions_Q2_2026.csv`. Four points exist only as DoS chart labels (male and female, 2023 Q2 and 2024 Q2); they are drawn hollow and footnoted.
- Fix: removed the garbled "labour force grew faster" sentence; "flat line" now refers to 2024–2026 only; D headline "every figure is correct" dropped in the final set; rate-vs-people labels now say "in the labour force"; y-axis start (15%) is stated.
- Note: Ma'an 23.2 to 28.8 and Aqaba labour force +22% in one year suggest small-sample noise; DoS publishes no sampling error. Stated on page 3.
## 2 Storytelling
- Strongest revelation: C (18 of 100 men, 33 of 100 women unemployed, yet 66 of 100 unemployed are men). A second. B is a chart, D an appendix.
- Order: 1 the number (B + 3-row D), 2 the people (C), 3 the places (flat A + evidence).
- Cut: 3D spires, annual bars, World Bank row, 8-row ledger page.
## 3 Visual design
- Ranked B, C, D, A. Keep B's headline and line, C's dot-people, D's highlight row, A's flat choropleth. Kill A's spires and leader lines, B's stacked bars.
- One masthead system; clay only for "the thing to read"; 48px margin; min 11px text.
## 4 Power BI feasibility
- Low risk: C lens, B lines, D ledger. Medium: map hotspot alignment (calibrate in data, ~27px offset measured). Fragile: hover (use selection), fonts off-Windows, mobile. Drop Bahnschrift.
## 5 Usability
- Needs visible affordances ("click a governorate"), segmented lens control, clear-selection chip, 11px+ dark secondary text (#5A4F44), distinct hues for age/education, chapter strip + "Next" button instead of a side menu, question-style titles.
## 6 Performance
- Model is tiny; cost is image visuals. Budget: <=4 SVG image visuals, 1 scatter, 1 slicer per page; SVG <=20k chars; precompute geometry and circle fragments in Python.
