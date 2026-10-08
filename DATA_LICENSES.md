# Data sources and licences

The MIT licence covers the code, report definition and documentation in this repository. Data keeps its publisher's terms.

| Data | Publisher | Use here | Terms |
|---|---|---|---|
| Labour Force Survey press releases and PxWeb tables (`08_Jordanian_Unemployment_Truth/01_Raw`) | Department of Statistics, Jordan (dos.gov.jo, jorinfo.dos.gov.jo) | Primary source for every Jordanian figure | Official public statistics; cite the source. Original files are unmodified, SHA-256 in `02_Metadata/SOURCES.csv` |
| Governorate boundaries (`01_Raw/geo`) | geoBoundaries (wmgeolab), gbOpen JOR ADM1 | Basemap only, no statistics | CC BY 2.5. Attribution: geoBoundaries |
| World Bank WDI `SL.UEM.TOTL.ZS` (`01_Raw/WB_*.json`) | World Bank / ILO modelled estimate | Reconciliation only, never used for a Jordanian figure | CC BY 4.0 |

Derived values (annual 2025 rate, governorate rates, youth rate) are computed here from DoS person counts and are labelled DERIVED wherever shown. They are not DoS-published rates.
