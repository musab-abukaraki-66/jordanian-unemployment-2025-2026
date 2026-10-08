import os as _o
def _find_repo():
    d = _o.path.dirname(_o.path.abspath(__file__))
    while d and not _o.path.isdir(_o.path.join(d, "08_Jordanian_Unemployment_Truth")):
        nd = _o.path.dirname(d)
        if nd == d: break
        d = nd
    return d
REPO = _o.environ.get("REPO_ROOT") or _find_repo()
"""Builds SOURCES, evidence table, truth table, history from raw files. Run with: python -I build_deliverables.py
Raw files are only read. Values are typed in from DoS press releases and each is page-verified against pdftotext output."""
import os, re, json, csv, hashlib, subprocess, datetime, glob

ROOT = _o.path.join(REPO, *r"08_Jordanian_Unemployment_Truth".split("\\"))
RAW, META, AUD, STG = [os.path.join(ROOT, d) for d in ("01_Raw", "02_Metadata", "03_Audit", "04_Staging")]
PDFTOTEXT = "pdftotext"

def pages(fn):
    p = os.path.join(RAW, fn)
    out = subprocess.run([PDFTOTEXT, "-enc", "UTF-8", "-layout", p, "-"], capture_output=True, text=True, encoding="utf8", errors="replace").stdout
    return [re.sub(r"\s+", " ", x) for x in out.split("\f")]
_cache = {}
def find(fn, needle):
    if fn not in _cache: _cache[fn] = pages(fn)
    norm = lambda x: re.sub(r"[^A-Za-z0-9.,%]+", "", x)
    n = norm(needle)
    for i, t in enumerate(_cache[fn]):
        if n in norm(t): return i + 1
    return None

JP = "Jordanian citizens"
F = {  # short key -> filename
 "Q1_25": "unemp_Q1_en_2025.pdf", "Q3_25": "unemp_Q3_2025_en.pdf", "Q4_25": "unemp_Q4_2025_en.pdf",
 "Q1_26": "unemp_Q1_2026_en.pdf", "Q2_26": "unemp_Q2_2026_en.pdf", "A24": "unemp_2024_en.pdf"}
SEC = "Section 'Second: Unemployment among Jordanians'"
# (period, indicator, value, unit, key, needle, section, crosscheck, verified)
E = [
 ("2025 Q1","Unemployment rate (15+)",21.3,"%","Q1_25","reached 21,3% in Q1 2025","Headline bullet 1 (population not stated in text)","Q1_26: Jordanians 21.3% in Q1 2025 (explicit Jordanian section)","Yes"),
 ("2025 Q1","Male unemployment rate",18.6,"%","Q1_25","Males' UNRATE reached 18,6%","Headline bullet 3","Q1_26: male 17.9% = 0.7 pp below Q1 2025","Yes"),
 ("2025 Q1","Female unemployment rate",31.2,"%","Q1_25","Females UNRATE reached 31,2%","Headline bullet 4","Q1_26: female 32.7% = +1.5 pp vs Q1 2025","Yes"),
 ("2025 Q1","Revised economic participation rate (LFPR)",32.9,"%","Q1_26","compared to 32.9% in Q1 2025",SEC+" / Labor Force","Q1_25 reports 32.9% (population not stated)","Yes"),
 ("2025 Q2","Unemployment rate (15+)",21.3,"%","Q3_25","when it stood at 21.3%",SEC,"Q2_26: 'compared to Q2 2025, when it stood at 21.3%'","Yes"),
 ("2025 Q2","Male unemployment rate",18.1,"%","Q2_26","increase of 0.4 percentage points compared to Q2 2025","Implied: 18.5 - 0.4","Q3_25: male 18.0% = 0.1 pp below Q2 2025 -> 18.1","Yes (implied by stated change; 2 bulletins agree)"),
 ("2025 Q2","Female unemployment rate",32.8,"%","Q3_25","an increase of 1.1 percentage points compared to Q2 2025",SEC+" (33.9 - 1.1)","Q2_26: 30.3% = -2.5 pp vs Q2 2025 -> 32.8","Yes (implied by stated change; 2 bulletins agree)"),
 ("2025 Q2","Revised economic participation rate (LFPR)",33.5,"%","Q2_26","compared to 33.5% in Q2 2025",SEC+" / Labor Force","none","Yes"),
 ("2025 Q3","Unemployment rate (15+)",21.4,"%","Q3_25","Jordanians UNRATE reached 21.4%",SEC,"Q4_25: 'a decrease of 0.2 pp compared to Q3 2025, when it was 21.4%'","Yes"),
 ("2025 Q3","Male unemployment rate",18.0,"%","Q3_25","UNRATE among males reached 18.0%",SEC,"Q4_25: 17.2% = -0.8 pp vs Q3 2025","Yes"),
 ("2025 Q3","Female unemployment rate",33.9,"%","Q3_25","Females UNRATE reached 33.9%",SEC,"Q4_25: 34.8% = +0.9 pp vs Q3 2025","Yes"),
 ("2025 Q3","Unemployment rate, age 24+",17.2,"%","Q3_25","UNRATE for Jordanians aged","Headline bullet 5 and Characteristics of Unemployed Jordanians (males 13.5, females 30.1)","none","Yes"),
 ("2025 Q3","Revised economic participation rate (LFPR)",33.4,"%","Q3_25","reached 33.4% in Q3 2025",SEC+" / Labor Force","none","Yes"),
 ("2025 Q3","Employment rate (employed / labour force)",78.6,"%","Q3_25","reached 78.6% during Q3 2025",SEC+" / Employed","none","Yes"),
 ("2025 Q4","Unemployment rate (15+)",21.2,"%","Q4_25","Jordanians' UNRATE reached 21.2%",SEC,"Q1_26: 'a decrease of 0.1 pp compared to Q4 of 2025, when it was 21.2%'","Yes"),
 ("2025 Q4","Male unemployment rate",17.2,"%","Q4_25","Among males, UNRATE reached 17.2%",SEC,"Headline bullet 1","Yes"),
 ("2025 Q4","Female unemployment rate",34.8,"%","Q4_25","Among females, UNRATE reached 34.8%",SEC,"Q1_26: 32.7% = -2.1 pp vs Q4 2025","Yes"),
 ("2025 Q4","Unemployment rate, age 24+",17.7,"%","Q4_25","UNRATE for the age group +24 years reached 17.7%",SEC+" (males 13.6, females 31.3)","none","Yes"),
 ("2025 Q4","Revised economic participation rate (LFPR)",34.5,"%","Q4_25","reached 34.5% in Q4 2025",SEC+" / Labor Force","none","Yes"),
 ("2025 Q4","Employment rate (employed / labour force)",78.8,"%","Q4_25","reached 78.8% during Q4 2025",SEC+" / Employed","none","Yes"),
 ("2026 Q1","Unemployment rate (15+)",21.1,"%","Q1_26","Jordanians' UNRATE reached 21.1% during Q1 2026",SEC,"Summary table 'first round of 2026'","Yes"),
 ("2026 Q1","Male unemployment rate",17.9,"%","Q1_26","Among males, UNRATE reached 17.9%",SEC,"Summary table","Yes"),
 ("2026 Q1","Female unemployment rate",32.7,"%","Q1_26","Among females, UNRATE reached 32.7%",SEC,"Q2_26: 30.3% = -2.4 pp vs Q1 2026","Yes"),
 ("2026 Q1","Unemployment rate, age 24+",17.7,"%","Q1_26","UNRATE for the age group +24 years reached 17.7%",SEC+" (males 14.4, females 29.0)","none","Yes"),
 ("2026 Q1","Revised economic participation rate (LFPR)",34.5,"%","Q1_26","reached 34.5% in Q1 2026",SEC+" / Labor Force","Summary table","Yes"),
 ("2026 Q1","Employment rate (employed / labour force)",78.9,"%","Q1_26","reached 78.9% during Q1 2026",SEC+" / Employed","none","Yes"),
 ("2026 Q2","Unemployment rate (15+)",21.0,"%","Q2_26","Jordanians' UERATE reached 21.0% during Q2 2026",SEC,"Summary table 'second round of 2026'","Yes"),
 ("2026 Q2","Male unemployment rate",18.5,"%","Q2_26","Among males, UERATE reached 18.5%",SEC,"Summary table","Yes"),
 ("2026 Q2","Female unemployment rate",30.3,"%","Q2_26","Among females, UERATE reached 30.3%",SEC,"Summary table","Yes"),
 ("2026 Q2","Unemployment rate, age 24+",18.0,"%","Q2_26","UERATE for the age group +24 years reached 18.0%",SEC+" (males 15.4, females 27.1)","Headline bullet 3","Yes"),
 ("2026 Q2","Revised economic participation rate (LFPR)",34.3,"%","Q2_26","reached 34.3% in Q2 2026",SEC+" / Labor Force","Summary table","Yes"),
 ("2026 Q2","Employment rate (employed / labour force)",79.0,"%","Q2_26","reached 79.0% during Q2 2026",SEC+" / Employed","none","Yes"),
 ("2026 Q2","Highest governorate rate (Ma'an)",33.2,"%","Q2_26","highest UERATE among Jordanians was recorded in Ma'an governorate",SEC+" / Characteristics of Unemployed (lowest Aqaba 14.7)","none","Yes"),
 ("2024 Annual","Unemployment rate (15+)",21.4,"%","A24","reached 21.4% in 2024","Bullet 1 (population not stated in text)","PxWeb counts give 21.42%; Q2_26 Fig.8 annual 2024 = 21.4","Yes (Jordanian status inferred from 2 cross-checks)"),
 ("2024 Annual","Male / Female unemployment rate","18.2 / 32.9","%","A24","18.2% in 2024, compared to 32.9% for females","Bullet 2","PxWeb counts give 18.21 / 32.85","Yes"),
 ("2023 Annual","Unemployment rate (15+)",22.0,"%","A24","from 22.0% in 2023","Bullet 1","PxWeb counts give 21.97%","Yes"),
]
rows = []
for per, ind, val, unit, k, needle, sec, cc, ver in E:
    pg = find(F[k], needle)
    rows.append(dict(Period=per, Indicator=ind, Value=val, Unit=unit, Population=JP, Source="DoS Press Release - "+F[k],
                     Page_Table=f"p.{pg}; {sec}" if pg else "NOT LOCATED; "+sec, Cross_check=cc, Verified=ver if pg else "NO - needle not found"))
miss = [r for r in rows if r["Verified"].startswith("NO")]

# PxWeb annual counts (official counts of Jordanians aged 15+)
cnt = {}
for r in csv.DictReader(open(os.path.join(STG, "dos_pxweb_jordanian_counts_long.csv"), encoding="utf8")):
    cnt[(r["measure"], r["breakdown"], r["code"], r["year"])] = int(r["persons"])
def fig(dim, code, y):
    u, e = cnt[("unemployed", dim, code, y)], cnt[("employed", dim, code, y)]
    return u, e, u + e, round(100 * u / (u + e), 2)
for y in ("2025",):
    u, e, lf, r = fig("TOTAL", "ALL", y)
    for ind, val, unit, sec in (("Jordanian unemployed persons (annual)", u, "persons", "EMPALL1 all dims, TIME=2025"),
                                ("Jordanian employed persons (annual)", e, "persons", "EMPALL all dims, TIME=2025"),
                                ("Jordanian labour force = unemployed + employed (annual)", lf, "persons", "DERIVED sum"),
                                ("Unemployment rate (annual, derived from counts)", r, "%", "DERIVED u/(u+e); same method reproduces published 2023 (21.97 vs 22.0) and 2024 (21.42 vs 21.4)")):
        rows.append(dict(Period="2025 Annual", Indicator=ind, Value=val, Unit=unit, Population="Jordanian citizens aged 15+",
                         Source="DoS PxWeb DOS_Database/12 (tables EMPALL1, EMPALL; API updated 2026-10-07)", Page_Table=sec,
                         Cross_check="Sex split sums to total (283,579 + 148,096 = 431,675)", Verified="Yes (official counts)" if "DERIVED" not in sec else "Derived (method validated on 2023-24)"))
    for code, lab in (("M", "Male"), ("F", "Female")):
        u, e, lf, r = fig("SEX", code, y)
        rows.append(dict(Period="2025 Annual", Indicator=f"{lab} unemployment rate (annual, derived from counts)", Value=r, Unit="%", Population="Jordanian citizens aged 15+",
                         Source="DoS PxWeb DOS_Database/12 (EMPALL1, EMPALL)", Page_Table="DERIVED u/(u+e) by sex", Cross_check="Method reproduces published 2024 male 18.2 / female 32.9", Verified="Derived (method validated on 2024)"))
    u, e, lf, r = fig("AGE", "A1519", y); u2, e2, lf2, _ = fig("AGE", "A2024", y)
    rows.append(dict(Period="2025 Annual", Indicator="Youth (15-24) unemployment rate (annual, derived from counts)", Value=round(100*(u+u2)/(lf+lf2), 2), Unit="%",
                     Population="Jordanian citizens aged 15-24", Source="DoS PxWeb DOS_Database/12 (EMPALL1, EMPALL)", Page_Table="DERIVED: age bands 15-19 + 20-24",
                     Cross_check="No DoS-published Jordanian youth rate for 2025 found", Verified="Derived (official counts)"))
with open(os.path.join(AUD, "EVIDENCE_TABLE.csv"), "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
with open(os.path.join(AUD, "EVIDENCE_TABLE.md"), "w", encoding="utf8") as f:
    f.write("| Period | Indicator | Value | Population | Source | Page/Table | Verified |\n| ------ | --------- | ----: | ---------- | ------ | ---------- | -------- |\n")
    for r in rows:
        f.write(f"| {r['Period']} | {r['Indicator']} | {r['Value']}{r['Unit'] if r['Unit']=='%' else ' '+r['Unit']} | {r['Population']} | {r['Source']} | {r['Page_Table']} | {r['Verified']} |\n")
print("evidence rows", len(rows), "unlocated", [(r['Period'], r['Indicator']) for r in miss])

# Annual history derived (2020-2025) + published quarterly 2020-2026
hist = []
for y in range(2020, 2026):
    ys = str(y); u, e, lf, r = fig("TOTAL", "ALL", ys)
    _, _, _, rm = fig("SEX", "M", ys); _, _, _, rf = fig("SEX", "F", ys)
    hist.append(dict(Year=y, Unemployed=u, Employed=e, LabourForce=lf, Rate_derived=r, Male_derived=rm, Female_derived=rf,
                     Published_annual_rate={2023: 22.0, 2024: 21.4}.get(y, "")))
with open(os.path.join(STG, "jordanian_annual_history_2020_2025.csv"), "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=list(hist[0].keys())); w.writeheader(); w.writerows(hist)
Q = [  # year,q,total,male,female,source
 (2020,1,19.3,18.1,24.4,"DoS post Q1 2020"),(2020,2,23.0,21.5,28.6,"DoS post Q2 2020"),(2020,3,23.9,21.2,33.6,"DoS post Q3 2020"),(2020,4,24.7,22.6,32.8,"Emp_Q4_2020.pdf"),
 (2021,1,25.0,"","","chart label, Q1 2024 bulletin Fig.1"),(2021,2,24.8,22.7,"","title / Q2 2026 text (male)"),(2021,3,23.2,21.2,30.8,"Q3_2021.pdf"),(2021,4,23.3,21.4,30.7,"Q4_2021.pdf"),
 (2022,1,22.8,20.5,31.5,"Emp_Q12022.pdf"),(2022,2,22.6,20.7,29.4,"Emp_Q2_2022.pdf"),(2022,3,23.1,20.5,"","Emp_Q32022.pdf / series"),(2022,4,22.9,20.6,"","Q4_e_2023 comparison / series"),
 (2023,1,21.9,19.6,"","series, Q1-Q3 2025/26 bulletins"),(2023,2,22.3,20.0,"","series"),(2023,3,22.3,19.8,31.7,"unemp_Q3_2023_en.pdf"),(2023,4,21.4,18.9,29.8,"unemp_Q4_e_2023.pdf"),
 (2024,1,21.4,17.4,34.7,"unemp_Q1_2024_en.pdf"),(2024,2,21.4,18.9,"","series / Q2 2024 title"),(2024,3,21.5,18.3,"","series / Q3 2024"),(2024,4,21.3,18.2,32.2,"Q4_25 comparisons"),
 (2025,1,21.3,18.6,31.2,"unemp_Q1_en_2025.pdf"),(2025,2,21.3,18.1,32.8,"implied, see evidence"),(2025,3,21.4,18.0,33.9,"unemp_Q3_2025_en.pdf"),(2025,4,21.2,17.2,34.8,"unemp_Q4_2025_en.pdf"),
 (2026,1,21.1,17.9,32.7,"unemp_Q1_2026_en.pdf"),(2026,2,21.0,18.5,30.3,"unemp_Q2_2026_en.pdf")]
with open(os.path.join(STG, "jordanian_quarterly_history_2020_2026.csv"), "w", newline="", encoding="utf8") as f:
    w = csv.writer(f); w.writerow(["Year", "Quarter", "Jordanian_rate", "Jordanian_male", "Jordanian_female", "Source", "Population"])
    for r in Q: w.writerow(list(r) + [JP + " (15+)"])

# SOURCES
DESC = {
 "unemp_Q2_2026_en.pdf": ("Press Release Q2 2026 (7 Sep 2026)", "Q2 2026", "Quarterly", "Primary", "Latest quarter. Contains total, Jordanian and non-Jordanian sections; only Jordanian section used."),
 "unemp_Q1_2026_en.pdf": ("Press Release Q1 2026 (17 Jun 2026)", "Q1 2026", "Quarterly", "Primary", "Jordanian section used."),
 "unemp_Q4_2025_en.pdf": ("Press Release Q4 2025 (15 Apr 2026)", "Q4 2025", "Quarterly", "Primary", "Jordanian section used."),
 "unemp_Q3_2025_en.pdf": ("Press Release Q3 2025 (2 Dec 2025)", "Q3 2025", "Quarterly", "Primary", "Jordanian section used; also confirms Q2 2025 values."),
 "unemp_Q1_en_2025.pdf": ("Press Release Q1 2025 (15 Jun 2025)", "Q1 2025", "Quarterly", "Primary", "Population not named in text; confirmed Jordanian via later bulletins."),
 "unemp_2024_en.pdf": ("Press Release annual 2024 (19 Mar 2025)", "2024", "Annual", "Primary", "Population not named in text; confirmed Jordanian via PxWeb counts and Q2 2026 Fig.8."),
 "unemp_Q3_2024_en.pdf": ("Press Release Q3 2024", "Q3 2024", "Quarterly", "Primary", "Context."),
 "unemp_Q2_2024_en.pdf": ("Press Release Q2 2024", "Q2 2024", "Quarterly", "Primary", "Context."),
 "unemp_Q1_2024_en.pdf": ("Press Release Q1 2024", "Q1 2024", "Quarterly", "Primary", "Context; Fig.1 supplies Q1 2021 value."),
 "unemp_Q4_e_2023.pdf": ("Press Release Q4 2023", "Q4 2023", "Quarterly", "Primary", "Context; includes Jordanian-era age-group rates (15-19, 20-24, 25-29)."),
 "unemp_Q3_2023_en.pdf": ("Press Release Q3 2023", "Q3 2023", "Quarterly", "Primary", "Context."),
 "Emp_Q32022.pdf": ("Press Release Q3 2022", "Q3 2022", "Quarterly", "Primary", "Legacy dos.gov.jo host."),
 "Emp_Q2_2022.pdf": ("Press Release Q2 2022", "Q2 2022", "Quarterly", "Primary", "Legacy dos.gov.jo host."),
 "Emp_Q12022.pdf": ("Press Release Q1 2022", "Q1 2022", "Quarterly", "Primary", "Legacy dos.gov.jo host."),
 "Q4_2021.pdf": ("Press Release Q4 2021", "Q4 2021", "Quarterly", "Primary", "Legacy dos.gov.jo host."),
 "Q3_2021.pdf": ("Press Release Q3 2021", "Q3 2021", "Quarterly", "Primary", "Legacy dos.gov.jo host."),
 "Emp_Q4_2020.pdf": ("Press Release Q4 2020", "Q4 2020", "Quarterly", "Primary", "Legacy dos.gov.jo host."),
 "Emp_unemp.xlsx": ("Employment and Unemployment - metadata workbook", "n/a", "n/a", "Primary", "Official DoS methodology/metadata (definitions, survey design)."),
}
SRC = []
for mp in sorted(glob.glob(os.path.join(RAW, "*.meta.json"))):
    m = json.load(open(mp, encoding="utf8")); fn = m["filename"]
    if fn.startswith("PX_"):
        tb = "EMPALL1 (Jordanians unemployed 15+)" if "EMPALL1" in fn else "EMPALL (Jordanians employed 15+)"
        d = ("DoS PxWeb database - " + tb, "2017-2025", "Annual", "Primary", "JSON-stat API extract; breakdown: " + fn.split("_")[-1][:-5] + " x Time. Persons.")
        pub, ind = "Department of Statistics (PxWeb, Labour Market)", "Persons unemployed/employed (Jordanians 15+)"
    else:
        if fn not in DESC: continue
        d = DESC[fn]; pub, ind = "Department of Statistics, Jordan", "Unemployment rate; participation; sex/age/governorate (Labour Force Survey)"
    SRC.append(dict(Source="DoS", Publisher=pub, Dataset_Publication=d[0], Indicator=ind, Population=JP if fn != "Emp_unemp.xlsx" else "n/a (methodology)",
        Period=d[1], Frequency=d[2], Unit="% / persons", Geography="Jordan (governorate breakdowns)", URL=m["url"], Retrieved=m["retrieved"],
        Filename=fn, Size_bytes=m["size"], SHA256=m["sha256"], Status="Downloaded", Primary_Secondary=d[3], Notes=d[4]))
for fn, t, per, u in (("DoS_post_Q1_2020.html", "Press release web page Q1 2020", "Q1 2020", "https://dosweb.dos.gov.jo/unemp_q12020/"),
                      ("DoS_post_Q2_2020.html", "Press release web page Q2 2020", "Q2 2020", "https://dosweb.dos.gov.jo/23-0-unemployment-rate-during-the-second-quarter-of-2020/"),
                      ("DoS_post_Q3_2020.html", "Press release web page Q3 2020", "Q3 2020", "https://dosweb.dos.gov.jo/23-9-unemployment-rate-during-the-third-quarter-of-2020-2/")):
    b = open(os.path.join(RAW, fn), "rb").read()
    SRC.append(dict(Source="DoS", Publisher="Department of Statistics, Jordan", Dataset_Publication=t, Indicator="Unemployment rate, male/female", Population=JP, Period=per, Frequency="Quarterly",
        Unit="%", Geography="Jordan", URL=u, Retrieved=datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(RAW, fn))).astimezone().isoformat(timespec="seconds"),
        Filename=fn, Size_bytes=len(b), SHA256=hashlib.sha256(b).hexdigest(), Status="Downloaded (web page; no PDF link)", Primary_Secondary="Primary", Notes="HTML page saved as-is; context only."))
b = open(os.path.join(RAW, "WB_SL.UEM.TOTL.ZS_JOR.json"), "rb").read()
SRC.append(dict(Source="World Bank", Publisher="World Bank (ILO modelled estimate)", Dataset_Publication="WDI SL.UEM.TOTL.ZS Jordan", Indicator="Unemployment, total (% of labour force), modeled ILO estimate",
    Population="NOT Jordanian-only (all residents, modeled)", Period="2019-2025", Frequency="Annual", Unit="%", Geography="Jordan",
    URL="https://api.worldbank.org/v2/country/JOR/indicator/SL.UEM.TOTL.ZS?format=json&date=2019:2026&per_page=50", Retrieved=datetime.datetime.fromtimestamp(os.path.getmtime(os.path.join(RAW, "WB_SL.UEM.TOTL.ZS_JOR.json"))).astimezone().isoformat(timespec="seconds"),
    Filename="WB_SL.UEM.TOTL.ZS_JOR.json", Size_bytes=len(b), SHA256=hashlib.sha256(b).hexdigest(), Status="Downloaded", Primary_Secondary="Secondary",
    Notes="Cross-check only; excluded from every Jordanian statistic."))
SRC.append(dict(Source="DoS", Publisher="Department of Statistics, Jordan", Dataset_Publication="Standalone press release Q2 2025", Indicator="Unemployment rate", Population=JP, Period="Q2 2025", Frequency="Quarterly", Unit="%",
    Geography="Jordan", URL="https://dosweb.dos.gov.jo/category/news/unemployment-rate/feed/", Retrieved="", Filename="", Size_bytes="", SHA256="", Status="Not published / not found",
    Primary_Secondary="Primary", Notes="Not in DoS press-release feed (no Q2 2025 or Q4 2024 or annual-2025 release). Q2 2025 values taken from Q3 2025, Q2 2026 bulletins."))
SRC.append(dict(Source="DoS", Publisher="Department of Statistics, Jordan", Dataset_Publication="Annual 2025 unemployment press release", Indicator="Unemployment rate", Population=JP, Period="2025", Frequency="Annual", Unit="%",
    Geography="Jordan", URL="https://dosweb.dos.gov.jo/category/news/unemployment-rate/feed/", Retrieved="", Filename="", Size_bytes="", SHA256="", Status="Not published as of 2026-10-08 (not found)",
    Primary_Secondary="Primary", Notes="2025 annual rate derived instead from official PxWeb person counts; flagged as derived."))
with open(os.path.join(META, "SOURCES.csv"), "w", newline="", encoding="utf8") as f:
    w = csv.DictWriter(f, fieldnames=list(SRC[0].keys())); w.writeheader(); w.writerows(SRC)
json.dump(SRC, open(os.path.join(META, "SOURCES.json"), "w", encoding="utf8"), indent=1, ensure_ascii=False)
dl = [s for s in SRC if s["Status"].startswith("Downloaded")]
print("sources", len(SRC), "downloaded", len(dl), "bytes", sum(int(s["Size_bytes"]) for s in dl))
