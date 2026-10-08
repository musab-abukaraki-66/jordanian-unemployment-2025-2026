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
EV=_o.path.join(REPO, *r"08_Jordanian_Unemployment_Truth".split("\\"))
GEO=json.load(open(EV+r"\04_Staging\design_geo.json"))
PAPER="#F1ECE2";INK="#1C1B19";CLAY="#B5472E";DEEP="#6E2417";SAND="#D8C8A8";STONE="#8C8577";SLATE="#3E4C52";MIST="#E6DFD0";RULE="#CFC6B3"
SERIF="Georgia, serif";SANS="'Segoe UI', sans-serif";MONO="Consolas, monospace"
# quarterly Jordanians 15+, 2022Q1..2026Q2 (DoS bulletins; see 02_Data/quarterly_series.csv for provenance)
QL=[f"{y} Q{q}" for y in range(2022,2027) for q in range(1,5)][:18]
TOT=[22.8,22.6,23.1,22.9,21.9,22.3,22.3,21.4,21.4,21.4,21.5,21.3,21.3,21.3,21.4,21.2,21.1,21.0]
MALE=[20.5,20.7,20.5,20.6,19.6,20.0,19.8,18.9,17.4,18.9,18.3,18.2,18.6,18.1,18.0,17.2,17.9,18.5]
FEM=[31.5,29.4,33.1,31.7,30.7,30.9,31.7,29.8,34.7,31.0,33.3,32.2,31.2,32.8,33.9,34.8,32.7,30.3]
ANN={2020:(404105,1338308),2021:(435549,1371932),2022:(419837,1418821),2023:(418365,1485675),2024:(429682,1576448),2025:(431675,1594162)}
def esc(s): return str(s).replace("&","&amp;").replace("<","&lt;")
class S:
    def __init__(s,w=1440,h=900,bg=PAPER): s.w,s.h=w,h;s.o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="{w}" height="{h}" fill="{bg}"/>']
    def add(s,x): s.o.append(x)
    def text(s,x,y,t,size=14,fill=INK,font=SANS,weight=400,anchor="start",ls=0,op=1,style=""):
        s.o.append(f'<text x="{x}" y="{y}" font-family="{font}" font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}" opacity="{op}" {style}>{esc(t)}</text>')
    def line(s,x1,y1,x2,y2,c=RULE,w=1,dash=None):
        d=f' stroke-dasharray="{dash}"' if dash else ""
        s.o.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c}" stroke-width="{w}"{d}/>')
    def rect(s,x,y,w,h,fill,op=1,stroke=None,sw=1):
        st=f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
        s.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" opacity="{op}"{st}/>')
    def circ(s,x,y,r,fill,op=1): s.o.append(f'<circle cx="{x}" cy="{y}" r="{r}" fill="{fill}" opacity="{op}"/>')
    def path(s,d,fill="none",stroke=None,sw=1,op=1,join="round"):
        st=f' stroke="{stroke}" stroke-width="{sw}" stroke-linejoin="{join}"' if stroke else ""
        s.o.append(f'<path d="{d}" fill="{fill}" opacity="{op}"{st}/>')
    def save(s,p): open(p,"w",encoding="utf8").write("\n".join(s.o)+"</svg>")
def mix(a,b,t):
    a=[int(a[i:i+2],16) for i in (1,3,5)];b=[int(b[i:i+2],16) for i in (1,3,5)]
    return "#%02X%02X%02X"%tuple(round(a[i]+(b[i]-a[i])*t) for i in range(3))
def ramp(rate,lo=15,hi=29):
    t=max(0,min(1,(rate-lo)/(hi-lo)))
    return mix(SAND,CLAY,t*1.0) if t<.75 else mix(CLAY,DEEP,(t-.75)/.25)
def furniture(s,n,title,right="08_Jordanian_Unemployment_Truth  ·  DoS Labour Force Survey  ·  Jordanian citizens 15+"):
    s.line(48,52,1392,52,INK,1)
    s.text(48,40,n,12,INK,MONO,600,ls=1.5)
    s.text(1392,40,right,11,STONE,MONO,anchor="end")
    s.text(48,876,title,11,STONE,MONO)
    s.line(48,858,1392,858,RULE,1)
