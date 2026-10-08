import os as _o
def _find_repo():
    d = _o.path.dirname(_o.path.abspath(__file__))
    while d and not _o.path.isdir(_o.path.join(d, "08_Jordanian_Unemployment_Truth")):
        nd = _o.path.dirname(d)
        if nd == d: break
        d = nd
    return d
REPO = _o.environ.get("REPO_ROOT") or _find_repo()
import json,csv,math
B=_o.path.join(REPO, *r"08_Jordanian_Unemployment_Truth".split("\\"))
gj=json.load(open(B+r"\01_Raw\geo\geoBoundaries-JOR-ADM1.geojson",encoding="utf8"))
def dp(pts,eps):
    if len(pts)<3: return pts
    a,b=pts[0],pts[-1]; dmax=0;idx=0
    for i in range(1,len(pts)-1):
        p=pts[i]; dx,dy=b[0]-a[0],b[1]-a[1]; L=math.hypot(dx,dy) or 1e-9
        d=abs(dy*p[0]-dx*p[1]+b[0]*a[1]-b[1]*a[0])/L
        if d>dmax: dmax,idx=d,i
    if dmax>eps: return dp(pts[:idx+1],eps)[:-1]+dp(pts[idx:],eps)
    return [a,b]
name2code={"Amman":"11","Balqa":"12","Zarqa":"13","Madaba":"14","Irbid":"21","Mafraq":"22","Jerash":"23","Ajloun":"24","Karak":"31","Tafilah":"32","Ma'an":"33","Aqaba":"34"}
rows=list(csv.DictReader(open(B+r"\04_Staging\jordanian_annual_rates_derived.csv",encoding="utf8")))
gov={}
for r in rows:
    if r["breakdown"]=="GOV": gov[(r["code"],r["year"])]=r
out=[]
for f in gj["features"]:
    n=f["properties"]["shapeName"]; ring=f["geometry"]["coordinates"][0]
    lat0=31.0; pts=[((x)*math.cos(math.radians(lat0)),y) for x,y in ring]
    s=dp(pts[:-1],0.012)
    c=name2code[n]; g=gov[(c,"2025")]; g21=gov[(c,"2021")]; g24=gov[(c,"2024")]
    out.append(dict(name=n,code=c,pts=s,u=int(g["unemployed"]),lf=int(g["labour_force"]),rate=float(g["rate_pct"]),rate21=float(g21["rate_pct"]),rate24=float(g24["rate_pct"])))
xs=[p[0] for o in out for p in o["pts"]];ys=[p[1] for o in out for p in o["pts"]]
x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys)
for o in out:
    o["pts"]=[[round((x-x0)/(y1-y0),4),round((y1-y)/(y1-y0),4)] for x,y in o["pts"]]
    print(o["name"],len(o["pts"]),o["u"],o["lf"],o["rate"])
json.dump(dict(gov=out,aspect=round((x1-x0)/(y1-y0),4)),open(B+r"\04_Staging\design_geo.json","w"))
print("aspect",(x1-x0)/(y1-y0), "unemp total",sum(o["u"] for o in out))
