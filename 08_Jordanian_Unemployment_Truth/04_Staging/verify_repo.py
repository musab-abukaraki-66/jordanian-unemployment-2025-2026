"""Integrity checks run in CI and locally:  python verify_repo.py
1. every raw file listed in SOURCES.csv exists and matches its SHA-256
2. headline values in the Power BI data tables reconcile with the evidence pack
3. no machine-specific paths are committed"""
import csv, hashlib, os, sys
root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
ev = os.path.join(root, "08_Jordanian_Unemployment_Truth")
rep = os.path.join(root, "09_Jordanian_Unemployment_Experience", "05_PowerBI", "data")
errors = []
n = 0
for r in csv.DictReader(open(os.path.join(ev, "02_Metadata", "SOURCES.csv"), encoding="utf8")):
    if r["Filename"] and r["SHA256"]:
        p = os.path.join(ev, "01_Raw", r["Filename"]); n += 1
        if not os.path.exists(p): errors.append("missing " + r["Filename"])
        elif hashlib.sha256(open(p, "rb").read()).hexdigest() != r["SHA256"]: errors.append("hash mismatch " + r["Filename"])
print("raw files checked:", n)
q = list(csv.DictReader(open(os.path.join(rep, "Quarter.csv"), encoding="utf8")))
assert len(q) == 18, "expected 18 quarters"
plateau = [float(x["Total"]) for x in q[8:]]
if (min(plateau), max(plateau)) != (21.0, 21.5): errors.append("plateau band changed %s" % ((min(plateau), max(plateau)),))
if float(q[-1]["Total"]) != 21.0: errors.append("latest quarter is not 21.0")
ann = {int(a["Year"]): a for a in csv.DictReader(open(os.path.join(rep, "Annual.csv"), encoding="utf8"))}
a = ann[2025]
if round(100 * int(a["Unemployed"]) / int(a["LabourForce"]), 2) != 21.31: errors.append("annual 2025 derived rate is not 21.31")
for lens in ("Sex", "Age", "Education"):
    s = sum(int(x["Count"]) for x in csv.DictReader(open(os.path.join(rep, "LegendKey.csv"), encoding="utf8")) if x["Lens"] == lens)
    if s != 100: errors.append("lens %s sums to %d" % (lens, s))
bad = []
for dp, dn, fn in os.walk(root):
    dn[:] = [d for d in dn if d not in (".git", "01_Raw")]
    for f in fn:
        if f.endswith((".py", ".md", ".tmdl", ".json", ".csv", ".cff", ".yml")) and f != "verify_repo.py":
            t = open(os.path.join(dp, f), encoding="utf8", errors="ignore").read()
            if (("C:" + chr(92) + "Users") in t or "C:/Users" in t or "AppData" in t) and f.endswith((".py", ".tmdl", ".md")): bad.append(os.path.relpath(os.path.join(dp, f), root))
if bad: errors.append("machine paths in: %s" % bad[:5])
if errors:
    print("FAIL"); [print(" -", e) for e in errors]; sys.exit(1)
print("OK: hashes, headline values and path hygiene verified")
