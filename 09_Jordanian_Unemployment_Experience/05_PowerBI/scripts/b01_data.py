import os as _o
def _find_repo():
    d = _o.path.dirname(_o.path.abspath(__file__))
    while d and not _o.path.isdir(_o.path.join(d, "08_Jordanian_Unemployment_Truth")):
        nd = _o.path.dirname(d)
        if nd == d: break
        d = nd
    return d
REPO = _o.environ.get("REPO_ROOT") or _find_repo()
"""Curated tables for the final report. Every number comes from 08_Jordanian_Unemployment_Truth or 02_Data additions; nothing is typed in twice."""
import csv, json, math, os, sys
sys.path.insert(0, _o.path.join(REPO, *r"09_Jordanian_Unemployment_Experience\01_Design".split("\\")))
from common import GEO, EV, ramp, mix, QL, TOT, MALE, FEM
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, "..", "data"); os.makedirs(OUT, exist_ok=True)
EXP = _o.path.join(REPO, *r"09_Jordanian_Unemployment_Experience".split("\\"))
def rgb(h): return "rgb(%d,%d,%d)" % tuple(int(h[i:i+2], 16) for i in (1, 3, 5))
def wr(name, rows):
    with open(f"{OUT}/{name}.csv", "w", newline="", encoding="utf8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys())); w.writeheader(); w.writerows(rows)
# ---- Quarter (basis from provenance csv)
prov = {}
for r in csv.DictReader(open(EXP + r"\02_Data\quarterly_series_provenance.csv", encoding="utf8")):
    prov[(r["Quarter"], r["Series"])] = r["Basis"]
Q = []
for i, q in enumerate(QL):
    y, qq = q.split(" ")
    lab = f"{qq} {y}"
    Q.append(dict(Order=i + 1, Label=lab, Key=q, Total=TOT[i], Male=MALE[i], Female=FEM[i], HotX=round(22 + i * 718 / 17, 1), HotY=round(344 - (314 - (TOT[i] - 15) * 290 / 21), 1),
                  MaleBasis="chart label" if "CHART" in prov[(q, "Male")] else ("implied" if prov[(q, "Male")].startswith("implied") else "published"),
                  FemaleBasis="chart label" if "CHART" in prov[(q, "Female")] else ("implied" if prov[(q, "Female")].startswith("implied") else "published")))
wr("Quarter", Q)
# ---- Annual counts
A = []
for r in csv.DictReader(open(EV + r"\04_Staging\jordanian_annual_history_2020_2025.csv", encoding="utf8")):
    A.append(dict(Year=int(r["Year"]), Unemployed=int(r["Unemployed"]), Employed=int(r["Employed"]), LabourForce=int(r["LabourForce"]), RateDerived=float(r["Rate_derived"])))
wr("Annual", A)
# ---- Governorates: flat map in a 700x500 box
SC = 480; OX = 20; OY = 10
def P(x, y): return (OX + x * SC, OY + y * SC)
raw = json.load(open(EV + r"\01_Raw\geo\geoBoundaries-JOR-ADM1.geojson", encoding="utf8"))
allp = [(x * math.cos(math.radians(31.0)), y) for f in raw["features"] for x, y in f["geometry"]["coordinates"][0]]
X0 = min(p[0] for p in allp); Y0 = min(p[1] for p in allp); Y1 = max(p[1] for p in allp)
def N(lon, lat): return ((lon * math.cos(math.radians(31.0)) - X0) / (Y1 - Y0), (Y1 - lat) / (Y1 - Y0))
CAP = {"Amman": (35.93, 31.95), "Irbid": (35.85, 32.55), "Zarqa": (36.09, 32.07), "Balqa": (35.73, 32.04), "Madaba": (35.79, 31.72), "Mafraq": (36.21, 32.34), "Jerash": (35.90, 32.28), "Ajloun": (35.75, 32.33), "Karak": (35.70, 31.18), "Tafilah": (35.60, 30.84), "Ma'an": (35.73, 30.19), "Aqaba": (35.00, 29.53)}
tot_u = sum(g["u"] for g in GEO["gov"])
G = []
for g in sorted(GEO["gov"], key=lambda g: -g["u"]):
    d = "M" + " L".join(f"{P(x, y)[0]:.1f},{P(x, y)[1]:.1f}" for x, y in g["pts"]) + "Z"
    bx, by = P(*N(*CAP[g["name"]]))
    note1 = "DoS published Ma'an's Q2 2026 quarterly rate separately: 33.2&%2337;." if g["name"] == "Ma'an" else ""
    note2 = "Different period and basis; not comparable with the 2025 derived rate." if g["name"] == "Ma'an" else ""
    G.append(dict(Order=len(G) + 1, Code=g["code"], Name=g["name"], Unemployed=g["u"], LabourForce=g["lf"], Rate=g["rate"], Share=round(g["u"] / tot_u, 4),
                  PathD=d, Fill=rgb(ramp(g["rate"])), CX=round(bx, 1), CY=round(by, 1), RowY=20 + len(G) * 34, HotRowX=14, HotMapY=round(500 - by, 1), HotRowY=round(412 - (20 + len(G) * 34), 1), R=round(math.sqrt(g["u"]) * 0.05, 1), Note1=note1, Note2=note2))
wr("DimGov", G)
# ---- Dots (shares of 100 unemployed, largest remainder, 2025 derived)
def shares(counts):
    tot = sum(counts); raw_ = [c / tot * 100 for c in counts]; fl = [int(x) for x in raw_]
    for i in sorted(range(len(raw_)), key=lambda i: -(raw_[i] - fl[i]))[:100 - sum(fl)]: fl[i] += 1
    return fl
cnt = {}
for r in csv.DictReader(open(EV + r"\04_Staging\dos_pxweb_jordanian_counts_long.csv", encoding="utf8")):
    cnt[(r["measure"], r["breakdown"], r["code"], r["year"])] = int(r["persons"])
u = lambda dim, c: cnt[("unemployed", dim, c, "2025")]
SLATE, CLAY, SAND, DEEP = "#3E4C52", "#B5472E", "#D8C8A8", "#6E2417"
lens = {
 "Sex": ([("men", u("SEX", "M"), SLATE, "are men"), ("women", u("SEX", "F"), CLAY, "are women")], "Two in three unemployed Jordanians are men."),
 "Age": ([("15-24", u("AGE", "A1519") + u("AGE", "A2024"), CLAY, "aged 15-24"), ("25-29", u("AGE", "A2529"), mix(CLAY, SAND, .38), "aged 25-29"), ("30-39", u("AGE", "A3039"), SLATE, "aged 30-39"), ("40+", sum(u("AGE", c) for c in ("A4049", "A5059", "A60M")), SAND, "aged 40 and over")], "About two in three are under 30."),
 "Education": ([("Bachelor+", u("EDU", "9"), DEEP, "bachelor or higher"), ("Diploma", u("EDU", "8"), CLAY, "diploma"), ("Secondary", u("EDU", "7"), SLATE, "secondary"), ("Below", sum(u("EDU", str(c)) for c in range(1, 7)), SAND, "below secondary")], "Nearly half hold a bachelor degree or higher."),
}
dots, leg, lens_rows = [], [], []
for k, (ln, (grp, cap)) in enumerate(lens.items()):
    sh = shares([g[1] for g in grp]); lens_rows.append(dict(Lens=ln, LensOrder=k + 1, Caption=cap))
    i = 0
    for go, ((nm, c, col, lab), n) in enumerate(zip(grp, sh)):
        leg.append(dict(Lens=ln, GroupOrder=go + 1, Group=nm, Label=lab, Count=n, Rgb=rgb(col), TextRgb=rgb(mix(col, "#1C1B19", .3)), MidY=round(((i + n / 2) / 10 - 0.5) * 29 + 11, 1)))
        for _ in range(n): dots.append(dict(Lens=ln, Idx=i + 1, Row=i // 10, Col=i % 10, Group=nm, Rgb=rgb(col))); i += 1
    assert i == 100, (ln, i)
for ln in lens:
    rows_ = [r for r in leg if r["Lens"] == ln]; prev = None
    for r in rows_:
        if prev is not None and r["MidY"] < prev + 48: r["MidY"] = round(prev + 48, 1)
        prev = r["MidY"]
wr("Dots", dots); wr("LegendKey", leg); wr("Lens", lens_rows)
# ---- Facts
ratio = lambda a, b: round(100 * u("SEX", a) / (u("SEX", a) + cnt[("employed", "SEX", a, "2025")]), 2)
men_rate, wom_rate = ratio("M", 0), ratio("F", 0)
FR = [("AllRes", 16.1, "All residents, Q2 2026", "DoS published", "unemp_Q2_2026_en.pdf item 1"),
      ("Jord", 21.0, "Jordanians 15+, Q2 2026", "DoS published", "unemp_Q2_2026_en.pdf Second: Unemployment among Jordanians"),
      ("JordWomen", 30.3, "Jordanian women, Q2 2026", "DoS published", "unemp_Q2_2026_en.pdf"),
      ("NonJord", 8.2, "Non-Jordanian residents, Q2 2026", "DoS published", "unemp_Q2_2026_en.pdf item 8"),
      ("ExpatShare", 42.2, "Expatriate workers share of employed, Q2 2026", "DoS published", "unemp_Q2_2026_en.pdf"),
      ("PartW", 14.7, "Participation Jordanian women, Q2 2026", "DoS published", "unemp_Q2_2026_en.pdf"),
      ("PartM", 53.6, "Participation Jordanian men, Q2 2026", "DoS published", "unemp_Q2_2026_en.pdf"),
      ("MenRate", men_rate, "Jordanian men 2025 annual", "Derived from DoS counts", "PxWeb EMPALL1/EMPALL"),
      ("WomenRate", wom_rate, "Jordanian women 2025 annual", "Derived from DoS counts", "PxWeb EMPALL1/EMPALL"),
      ("Youth1524", round(100 * (u("AGE", "A1519") + u("AGE", "A2024")) / (u("AGE", "A1519") + u("AGE", "A2024") + cnt[("employed", "AGE", "A1519", "2025")] + cnt[("employed", "AGE", "A2024", "2025")]), 1), "Jordanians 15-24, 2025 annual", "Derived from DoS counts (small base)", "PxWeb age bands"),
      ("Age24Plus", 18.0, "Jordanians 24+, Q2 2026", "DoS published", "unemp_Q2_2026_en.pdf"),
      ("MaanQ2", 33.2, "Ma'an Jordanians, Q2 2026", "DoS published", "unemp_Q2_2026_en.pdf")]
wr("Facts", [dict(Key=k, Value=v, Label=l, Basis=b, Source=s) for k, v, l, b, s in FR])
print("data ok", len(Q), len(A), len(G), len(dots), "men/women", men_rate, wom_rate, [ (r['Lens'],r['Group'],r['Count']) for r in leg])
