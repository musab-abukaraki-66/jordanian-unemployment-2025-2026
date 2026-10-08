# Audit Summary - Jordanian Unemployment 2025-2026

Audit date: 2026-10-08. Scope: Jordanian citizens only.

## Result
- Evidence rows: 43 (`EVIDENCE_TABLE.md` / `.csv`). Every row traced to a file in `01_Raw` with page located by text search (`04_Staging/build_deliverables.py`).
- Directly published by DoS press releases (Jordanian figures): 36 rows. Of these 2 (Q2 2025 male and female) are implied by DoS-stated changes and agree across two bulletins. 
- Official person counts (PxWeb): 2 rows. Derived from official counts: 5 rows (flagged "Derived").
- Population check: every quarterly Q3 2025 - Q2 2026 value is taken from the section titled for Jordanians only. Total-population and non-Jordanian figures were not used.

## Findings
1. **Q1 2025 release and 2024 annual release do not name the population in text.** Their figures (21.3 and 21.4) match the Jordanian series in later bulletins (Q1 2026 text; Q2 2026 Fig.8) and PxWeb counts (21.42). Treated as Jordanian; flagged.
2. **No 2025 annual DoS press release.** RSS feed of the DoS "Unemployment rate" category (checked 2026-10-08) lists none (also none for Q2 2025 and Q4 2024). 2025 annual = 21.31% from official counts, labelled derived. Averaging quarters (21.30) gives the same figure to one decimal, but was not used.
3. **No Jordanian youth (15-24) rate in any quarterly 2025-26 press release.** Releases give age 24+ only. Annual youth rate 47.23% is derived from PxWeb age-band counts (15-19: 55.6%, 20-24: 45.8%).
4. **Revisions:** no revision found for Jordanian 2025 quarters. Q1 2025 (male 18.6, female 31.2) matches back-references in Q1 2026 bulletin. Q4 2024 Jordanian 21.3 is consistent between Q1 2025 chart series and Q4 2025 text.
5. **Internal DoS inconsistencies noted (no effect on headline figures):** Q2 2026 text gives "1.7 pp" and "1.6 pp" decline vs Q2 2022 for Jordanians; one sentence says 4.2 pp male decline "since Q1 2021" vs "Q2 2021"; Q2 2026 text states female participation "16.3% in Q2 2025 compared to 18.6% in Q2 2026" (swapped, total-population paragraph); Q1 2026 education shares sum to 99.4%; PxWeb table EMPALL1 'updated' tag reads 2025-05-14 while API returns 2026-10-07 data stamp.
6. **Tooling:** DoS HTML host `dos.gov.jo` refused connections (ECONNREFUSED); `dosweb.dos.gov.jo` and `jorinfo.dos.gov.jo` worked. Legacy 2021-22 PDFs retrieved from `http://dos.gov.jo/...` archive path (HTTP 200).

## Failed / unavailable
- Standalone Q2 2025 press release: not published (see 2).
- Standalone 2025 annual press release: not published as of audit date.
- Jordanian youth rate by quarter: not published.
- Jordanian underutilisation indicator: none found in any retrieved DoS source.
- Nothing failed twice on a URL that exists.

## Secondary cross-check (not used for any Jordanian figure)
World Bank/ILO modeled total-population rate: 2025 = 16.54%; DoS observed all-resident rates 2025 Q1-Q4 = 16.6 / 16.5 / 16.2 / 16.1. Different population and method.
