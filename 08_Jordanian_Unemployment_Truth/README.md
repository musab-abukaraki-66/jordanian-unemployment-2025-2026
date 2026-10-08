# 08 - Jordanian Unemployment Truth (2025-2026)

Data acquisition and verification project. No dashboard, model or further analysis.

## Objective
Establish the source-backed unemployment picture for **Jordanian citizens only** in 2025-2026, with 2020-2024 context. Every statistic carries `Population = Jordanian citizens`. Total-population, non-Jordanian and modeled figures are excluded from all headline numbers.

## Source hierarchy
1. **Primary - Jordan Department of Statistics (DoS)**: quarterly/annual Labour Force Survey (LFS) press releases (`dosweb.dos.gov.jo`), PxWeb database tables of Jordanian unemployed/employed persons (`jorinfo.dos.gov.jo`), DoS metadata workbook.
2. **Secondary - World Bank/ILO modeled estimate**: cross-check only (total population, not Jordanian).

Manifest: `02_Metadata/SOURCES.csv` / `.json` (filename, URL, retrieval time, size, SHA-256, status). Raw files in `01_Raw` are unmodified.

## Headline results (Jordanians, age 15+)
| Period | Total | Male | Female |
| ------ | ----: | ---: | -----: |
| 2025 Q1 | 21.3 | 18.6 | 31.2 |
| 2025 Q2 | 21.3 | 18.1 | 32.8 |
| 2025 Q3 | 21.4 | 18.0 | 33.9 |
| 2025 Q4 | 21.2 | 17.2 | 34.8 |
| 2025 annual (derived) | 21.3 | 17.95 | 33.21 |
| 2026 Q1 | 21.1 | 17.9 | 32.7 |
| 2026 Q2 (latest) | 21.0 | 18.5 | 30.3 |

Full table with notes: `03_Audit/TRUTH_TABLE.md`. Evidence per figure: `03_Audit/EVIDENCE_TABLE.md`.

### 2025 picture
The Jordanian rate held in a 21.2-21.4% band across all four quarters. The 2025 annual rate is 21.31%, computed from DoS annual person counts (431,675 unemployed; 2,025,837 labour force). It is not an average of quarters and DoS has not published a 2025 annual press release. 2024 was 21.4%, 2023 was 22.0%.

### 2026 latest
Q1 2026: 21.1%. Q2 2026: 21.0% (DoS release 7 Sep 2026), 0.3 pp below Q2 2025. Revised participation rate of Jordanians: 34.3% (Q2 2026) vs 33.5% (Q2 2025). Employment rate (employed share of the labour force): 79.0%.

### Male / female
Male rate fell from 18.6% (Q1 2025) to 17.2% (Q4 2025), then 17.9% and 18.5% in 2026. Female rate is about 1.6-2 times the male rate: 31.2% to 34.8% during 2025, then 32.7% and 30.3%. The female labour force is small (revised participation rate 14.7% in Q2 2026 vs 53.6% for males), and about 70% of it holds a bachelor degree or higher, so female rates move more per person.

### Youth
DoS quarterly releases do not publish a Jordanian 15-24 rate. They publish age 24+ (Q2 2026: 18.0%; males 15.4%, females 27.1%). From official annual counts, the derived 2025 rate for Jordanians aged 15-24 is 47.2% (15-19: 55.6%; 20-24: 45.8%), versus 46.6% in 2024. These age bands have small labour forces.

### Historical trend (Jordanians)
Quarterly peak 25.0% (Q1 2021) after 19.3% (Q1 2020). Gradual decline to 21.4% in 2024, then flat at 21.0-21.4% through Q2 2026. Annual (derived/published): 2020 23.2, 2021 24.1, 2022 22.8, 2023 22.0, 2024 21.4, 2025 21.3. Series: `04_Staging/`.

## Methodology and definitions
- Source survey: DoS Labour Force Survey, 16,560 households per quarter, interview mid-quarter, job search over the previous four weeks.
- **Unemployment rate (UNRATE/UERATE)** = unemployed / (employed + unemployed), persons 15+.
- **Jordanian**: citizens only; DoS releases separate sections for total population, Jordanians, non-Jordanians. Only the Jordanian section was used.
- **Revised economic participation rate**: labour force / population 15+. **Employment rate (DoS)**: employed / labour force (not employment-to-population).
- Annual rates in this project are labelled *published* or *derived*; derived = unemployed/(unemployed+employed) from official DoS annual person counts.
- Missing items are blank, never estimated.

## Why public numbers differ
| Figure seen | What it is |
| ----------- | ---------- |
| ~16.1-16.5% | All residents (Jordanians + non-Jordanians); non-Jordanian rate is 8.2-9.2% and lowers the total |
| 21.0-21.4% | Jordanians aged 15+ |
| 17.2-18.0% | Jordanians aged 24+ (a different age base) |
| 30.3-34.8% | Jordanian female rate; "all females" is 19.9-21.3%, a different population |
| 16.5% (World Bank 2025) | Modeled ILO estimate for all residents, not observed Jordanian survey rate |
| 21.3% for Q1 2025 or 2024 annual 21.4% | DoS texts that do not name the population; they match the Jordanian series |

Quarterly vs annual: annual values are not averages of quarters; compare same-quarter year-on-year to remove seasonality (Q3 rises as graduates enter the labour force, per DoS Q3 2025 release).

## Limitations
- No DoS 2025 annual release, no Q2 2025 standalone release, no quarterly Jordanian youth rate, no Jordanian underutilisation indicator found.
- Q2 2025 male/female are implied from stated changes in later DoS bulletins (two sources agree).
- Governorate and education breakdowns: DoS releases give extremes and shares (Q2 2026: highest Ma'an 33.2%, lowest Aqaba 14.7%; 57.3% of unemployed hold secondary or higher). Annual counts by governorate/education/age are in `01_Raw/PX_*.json` (derived rates in `04_Staging/jordanian_annual_rates_derived.csv`).
- A few DoS texts contain internal inconsistencies (see `03_Audit/AUDIT_SUMMARY.md`); headline figures were cross-checked across bulletins.
- LFS sample error is not published in the releases used.
