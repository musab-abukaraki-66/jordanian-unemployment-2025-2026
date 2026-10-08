import os as _o
def _find_repo():
    d = _o.path.dirname(_o.path.abspath(__file__))
    while d and not _o.path.isdir(_o.path.join(d, "08_Jordanian_Unemployment_Truth")):
        nd = _o.path.dirname(d)
        if nd == d: break
        d = nd
    return d
REPO = _o.environ.get("REPO_ROOT") or _find_repo()
"""Static page chrome (wallpapers, 1440x900). Only words and rules live here; every number on the report comes from the model."""
import sys, csv, os, subprocess
sys.path.insert(0, _o.path.join(REPO, *r"09_Jordanian_Unemployment_Experience\01_Design".split("\\")))
from final_common import *
ART = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "art")
_orig_text = S.text
def _scaled(self, x, y, t, size=14, *a, **k): return _orig_text(self, x, y, t, size if size >= 18 else round(size * 1.13, 1), *a, **k)
S.text = _scaled
F = {r["Key"]: float(r["Value"]) for r in csv.DictReader(open(os.path.join(ART, "..", "data", "Facts.csv"), encoding="utf8"))}
def page(i, name, build, next_label):
    s = S(); chapter_strip(s, i); build(s)
    s.line(48, 846, 1392, 846, RULE, 1)
    s.rect(1160, 852, 232, 34, INK); s.text(1276, 874, next_label, 12, PAPER, SANS, 600, "middle", .4)
    s.save(os.path.join(ART, name + ".svg"))
def p1(s):
    s.text(48, 100, "THE NUMBER  ·  WHAT 21 PERCENT MEANS", 11.5, CLAY, SANS, 700, ls=1.8)
    for k, l in enumerate(["Unemployment among", "Jordanians has not moved", "in ten quarters."]): s.text(48, 152 + k * 50, l, 44, INK, SERIF, 700)
    s.text(70, 456, "JORDANIAN UNEMPLOYMENT RATE BY QUARTER, Q1 2022 – Q2 2026  ·  AXIS STARTS AT 15%  ·  SELECT A POINT TO READ A QUARTER", 11, MUTE, SANS, 700, ls=.9)
    s.text(993, 112, "THE SAME QUARTER, THREE ANSWERS", 11.5, MUTE, SANS, 700, ls=1.2)
    s.line(993, 628, 1392, 628, RULE, 1)
    s.text(993, 646, "THE PEOPLE BEHIND THE RATE  ·  2020 → 2025", 11.5, MUTE, SANS, 700, ls=1.2)
    s.text(48, 870, "Source: DoS press releases (Jordanian section); PxWeb counts 2020, 2025. Hollow points: read from DoS chart labels only.", 11.5, MUTE)
def p2(s):
    s.text(48, 100, "THE PEOPLE  ·  WHO IS BEHIND THE RATE", 11.5, CLAY, SANS, 700, ls=1.8)
    for k, l in enumerate(["The rate and the people", "tell opposite stories."]): s.text(48, 152 + k * 50, l, 44, INK, SERIF, 700)
    s.text(48, 246, "Two lenses on the same Jordanians. Switch the lens on the left; compare it with the rate on the right.", 14, MUTE)
    s.text(48, 322, "LENS", 11, MUTE, SANS, 700, ls=1.4)
    s.text(48, 364, "100 UNEMPLOYED JORDANIANS, 2025", 11.5, INK, SANS, 700, ls=1.2)
    s.text(760, 364, "UNEMPLOYED IN EVERY 100 IN THE LABOUR FORCE  ·  DERIVED, 2025", 11.5, INK, SANS, 700, ls=1.0)
    s.text(760, 772, "Why both are true", 14, INK, SERIF, 700)
    s.text(760, 796, f"Only {F['PartW']:.1f} in 100 Jordanian women are in the labour force, against {F['PartM']:.1f} in 100 men (Q2 2026).", 12.5, MUTE)
    s.text(760, 818, "A higher rate on a small base is fewer people than a lower rate on a large one.", 12.5, MUTE)
    x = chip(s, 48, 790, "DERIVED", "der"); chip(s, x, 790, "LIMITED EVIDENCE: SMALL BASE", "lim")
    s.text(48, 818, f"Youth (15–24): {F['Youth1524']:.1f}% in 2025, from annual counts. DoS publishes age 24+ only ({F['Age24Plus']:.1f}% in Q2 2026).", 12.5, MUTE)
    s.text(48, 870, "Source: DoS PxWeb counts EMPALL1/EMPALL (2025 annual, Jordanians 15+); participation from the DoS Q2 2026 release. Shares rounded to whole people per 100.", 11.5, MUTE)
def p3(s):
    s.text(48, 100, "THE PLACES  ·  GOVERNORATES", 11.5, CLAY, SANS, 700, ls=1.8)
    for k, l in enumerate(["The highest rate and the", "most people are in", "different places."]): s.text(48, 152 + k * 50, l, 44, INK, SERIF, 700)
    s.text(48, 284, "Ground colour = rate  ·  Disc area = number of unemployed Jordanians  ·  Select a disc", 12, MUTE)
    s.text(812, 112, "GOVERNORATE LEDGER  ·  2025 ANNUAL, DERIVED", 11.5, MUTE, SANS, 700, ls=1.2)
    s.text(812+262+5, 146, "RATE", 11, MUTE, SANS, 700, "end"); s.text(812+396+5, 146, "UNEMPLOYED", 11, MUTE, SANS, 700, "end"); s.text(812+556+5, 146, "SHARE", 11, MUTE, SANS, 700, "end")
    s.text(48, 870, "Source: DoS PxWeb EMPALL1/EMPALL, 2025 annual (Jordanians 15+); Q2 2026 release for Ma'an 33.2%. Boundaries: geoBoundaries (CC BY 2.5).", 11.5, MUTE)
page(0, "bg_p1", p1, "NEXT: WHO ARE THEY?  →"); page(1, "bg_p2", p2, "NEXT: WHERE ARE THEY?  →"); page(2, "bg_p3", p3, "BACK TO THE NUMBER  ↺")
EDGE = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"
for n in ("bg_p1", "bg_p2", "bg_p3"):
    subprocess.run([EDGE, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1", "--window-size=1440,900", f"--screenshot={os.path.abspath(os.path.join(ART, n + '.png'))}", "file:///" + os.path.abspath(os.path.join(ART, n + '.svg')).replace("\\", "/")], capture_output=True)
print("art ok", sorted(f for f in os.listdir(ART)))
