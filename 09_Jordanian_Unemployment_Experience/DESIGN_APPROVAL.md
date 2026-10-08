# Design Approval Package — Jordanian Unemployment 2025–2026

Status: **STOPPED AT DESIGN GATE.** No final Power BI report has been built.
Evidence authority: `..\08_Jordanian_Unemployment_Truth` (unchanged).

## 1. Story discovered
One number hides three things.
1. **Persistence.** Jordanian unemployment has sat between 21.0% and 21.5% for ten quarters (2024 Q1 – 2026 Q2). Same quarter, three answers: all residents 16.1%, Jordanians 21.0%, Jordanian women 30.3%.
2. **Rate vs people.** 18 of 100 Jordanian men and 33 of 100 Jordanian women in the labour force are unemployed (2025, derived), yet 66 of every 100 unemployed Jordanians are men, because only 14.7 in 100 women are in the labour force (Q2 2026). Two in three unemployed are under 30; 45 in 100 hold a bachelor degree or higher.
3. **Place.** The highest derived 2025 rate is Ma'an (28.8%, 12,749 people). Amman has 19.1% but 155,900 people (36%); Amman, Irbid and Zarqa hold 70%.

## 2. Recommended direction: "The Number and the People" (3 pages, 1440×900)
Frames: `01_Design/concepts/F1_number.png`, `F2_people.png`, `F3_places.png`.
| Page | Question | Core object |
|---|---|---|
| 1 The number | What does 21% mean and has it moved? | Georgia headline, 18-quarter line with the 10-quarter plateau, three-row reconciliation ruler |
| 2 The people | Who is behind the rate? | 100-dot unit chart with Sex / Age / Education lens beside the rate-per-100 grids |
| 3 The places | Where? | Flat governorate map (colour = rate, disc area = people) + clickable ledger + evidence chips |
Navigation: chapter strip (top) + "Next question" button; no side menu. Evidence chips on every page: DoS PUBLISHED / DERIVED / LIMITED EVIDENCE.

## 3. Concepts explored (all frames use real data)
`concepts/A_relief` governorate spires (killed: occlusion, fake-3D feel) · `B_treadmill` persistence (kept: line, headline; bars killed) · `C_hundred` 100 Jordanians (kept, lead of page 2) · `D_evidence` ledger (kept as 3-row ruler on page 1).
Honest 3D verdict: a true relief map is not analytically honest here (polygon area ≠ people; tall spires occlude). The flat map with proportional discs gives two encodings without distortion.

## 4. Type, palette
Georgia (display, numerals) · Segoe UI / Segoe UI Semibold (UI, body) · Consolas (source metadata only). All tested rendering inside SVG in Desktop 2.158. Bahnschrift dropped. Paper #F1ECE2, ink #1C1B19, clay #B5472E, deep clay #6E2417, sand #D8C8A8, slate #3E4C52, secondary text #5A4F44.

## 5. Feasibility tested in Power BI Desktop 2.158 (prototype `03_Feasibility/pbip`)
PASS: DAX SVG atlas (7.6k chars; 65k proven earlier) · Georgia/Segoe UI/Consolas/Bahnschrift in SVG · slicer-driven 100-dot lens (Sex/Age/Education) · transparent scatter hotspot selects a governorate, others dim, caption updates · model loads and computes in 0.5 s.
NEEDS WORK: hotspot markers sat ~27 px below SVG targets → calibrate in data; first click only focuses a visual → "Click a governorate" cue + clear chip.
NOT RETESTED (proven in Project 05): drill-through, page navigation buttons, bookmarks. Deneb not used (needs sign-in).
Screenshot: `03_Feasibility/screenshots/feasibility_desktop_selection_education.jpg`.

## 6. Honest limits and decisions you should know
- **Figma:** file created (`Jordan Unemployment - Design Concepts`, key xMKMkUl4U9oUXOcEwG00Yh) but the Starter plan MCP call limit was hit after 6 calls, so it holds no frames. Concepts were built as real-data SVG/PNG instead (rendered with the actual Power BI fonts). If you upgrade or the limit resets, they can be imported.
- Youth rate exists only as a derived annual figure (47.2%, small base); quarterly youth is not published.
- Governorate rates are derived from annual counts, not DoS-published rates; DoS publishes no sampling error.
- Map boundaries: geoBoundaries (CC BY 2.5), a basemap not statistical data.
- Mobile: desktop-first (1440×900 fit-to-page).

## 7. Decisions needed from you
1. Approve the 3-page direction (or pick a different mix of A–D).
2. Accept flat map + discs instead of a 3D relief.
3. Accept "derived" governorate and annual figures shown with chips.
