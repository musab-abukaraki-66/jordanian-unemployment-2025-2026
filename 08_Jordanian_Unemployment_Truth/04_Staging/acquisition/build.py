import os
def _find_repo():
    d = os.path.dirname(os.path.abspath(__file__))
    while d and not os.path.isdir(os.path.join(d, "08_Jordanian_Unemployment_Truth")):
        nd = os.path.dirname(d)
        if nd == d: break
        d = nd
    return d
REPO = os.environ.get("REPO_ROOT") or _find_repo()
import json,os,csv,itertools
RAW=os.path.join(REPO, "08_Jordanian_Unemployment_Truth", "01_Raw")
ST=os.path.join(REPO, "08_Jordanian_Unemployment_Truth", "04_Staging")
def load(fn):
    d=json.load(open(os.path.join(RAW,fn),encoding="utf8"))["dataset"]
    ids=d["dimension"]["id"];sizes=d["dimension"]["size"];val=d["value"]
    labs={i:list(d["dimension"][i]["category"]["index"].keys()) for i in ids}
    texts={i:d["dimension"][i]["category"]["label"] for i in ids}
    rows=[]
    for k,combo in enumerate(itertools.product(*[range(s) for s in sizes])):
        rec={i:labs[i][c] for i,c in zip(ids,combo)}
        rec["value"]=val[k]; rows.append(rec)
    return rows,texts
rows=[]
cnt={}
for tbl,meas in (("EMPALL1","unemployed"),("EMPALL","employed")):
    for dim in ("TOTAL","SEX","AGE","EDU","GOV"):
        r,t=load(f"PX_{tbl}_{dim}.json")
        for x in r:
            y=x["TIME"]; key=x.get(dim,"ALL") if dim!="TOTAL" else "ALL"
            lab=t[dim].get(key,"All") if dim!="TOTAL" else "All"
            cnt[(meas,dim,key,y)]=x["value"]
            rows.append(dict(table=tbl,measure=meas,breakdown=dim,code=key,label=lab.strip(),year=y,persons=x["value"],population="Jordanian citizens aged 15+",source="DoS PxWeb DOS_Database/12/"+tbl))
w=csv.DictWriter(open(os.path.join(ST,"dos_pxweb_jordanian_counts_long.csv"),"w",newline="",encoding="utf8"),fieldnames=list(rows[0].keys()));w.writeheader();w.writerows(rows)
# derived annual rates
out=[]
def rate(dim,key,y,keysU=None):
    u=cnt.get(("unemployed",dim,key,y));e=cnt.get(("employed",dim,key,y))
    if u is None or e is None: return None
    return dict(unemployed=u,employed=e,labour_force=u+e,rate_pct=round(100*u/(u+e),2))
labels={}
for (m,dim,key,y),v in cnt.items(): pass
for dim in ("TOTAL","SEX","AGE","EDU","GOV"):
    keys=sorted({k for (m,d,k,y) in cnt if d==dim})
    for k in keys:
        for y in sorted({y for (m,d,kk,y) in cnt if d==dim}):
            r=rate(dim,k,y)
            if r: out.append(dict(breakdown=dim,code=k,year=y,**r,population="Jordanian citizens aged 15+",derivation="rate = unemployed/(unemployed+employed) from official DoS annual person counts; DERIVED, not a published rate"))
# youth 15-24
for y in sorted({y for (m,d,k,y) in cnt}):
    u=sum(cnt[("unemployed","AGE",a,y)] for a in ("A1519","A2024")); e=sum(cnt[("employed","AGE",a,y)] for a in ("A1519","A2024"))
    out.append(dict(breakdown="YOUTH_15_24",code="A1524",year=y,unemployed=u,employed=e,labour_force=u+e,rate_pct=round(100*u/(u+e),2),population="Jordanian citizens aged 15-24",derivation="sum of age bands 15-19 and 20-24; DERIVED from official counts"))
w=csv.DictWriter(open(os.path.join(ST,"jordanian_annual_rates_derived.csv"),"w",newline="",encoding="utf8"),fieldnames=list(out[0].keys()));w.writeheader();w.writerows(out)
for o in out:
    if o["breakdown"] in ("TOTAL","SEX","YOUTH_15_24","AGE") and o["year"] in ("2020","2021","2022","2023","2024","2025"): print(o["breakdown"],o["code"],o["year"],o["unemployed"],o["employed"],o["rate_pct"])
