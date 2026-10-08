from common import *
import math
s=S(); furniture(s,"CONCEPT A  —  THE RELIEF","Unemployed Jordanians by governorate, 2025 annual. Derived from DoS PxWeb person counts (EMPALL1, EMPALL). Boundaries: geoBoundaries (CC BY 2.5). Spire positions: governorate capital cities.")
SC=720; OX=470; OY=190; SH=0.10; SQ=0.58; HS=0.0017
def P(x,y,h=0): return (OX+(x-SH*y)*SC, OY+y*SC*SQ-h)
# governorate capital (lon,lat) for spire base -> normalised using same transform as design_geo (lat0=31)
import json
raw=json.load(open(EV+r"\01_Raw\geo\geoBoundaries-JOR-ADM1.geojson",encoding="utf8"))
allp=[(x*math.cos(math.radians(31.0)),y) for f in raw["features"] for x,y in f["geometry"]["coordinates"][0]]
# replicate normalisation used in prep (min/max over simplified pts is slightly different) -> use simplified pts extremes
xs=[p[0] for p in allp];ys=[p[1] for p in allp];X0,Y0,Y1=min(xs),min(ys),max(ys)
def N(lon,lat): return ((lon*math.cos(math.radians(31.0))-X0)/(Y1-Y0),(Y1-lat)/(Y1-Y0))
CAP={"Amman":(35.93,31.95),"Irbid":(35.85,32.55),"Zarqa":(36.09,32.07),"Balqa":(35.73,32.04),"Madaba":(35.79,31.72),"Mafraq":(36.21,32.34),"Jerash":(35.90,32.28),"Ajloun":(35.75,32.33),"Karak":(35.70,31.18),"Tafilah":(35.60,30.84),"Ma'an":(35.73,30.19),"Aqaba":(35.00,29.53)}
for g in GEO["gov"]:
    d="M"+" L".join(f"{P(x,y)[0]:.1f},{P(x,y)[1]:.1f}" for x,y in g["pts"])+"Z"
    s.path(d,fill=ramp(g["rate"]),stroke=PAPER,sw=1.6)
tips={}
G=sorted(GEO["gov"],key=lambda g:CAP[g["name"]][1],reverse=True)  # north first
for g in G:
    bx,by=P(*N(*CAP[g["name"]])); h=g["u"]*HS; w=11
    s.add(f'<ellipse cx="{bx:.1f}" cy="{by+2:.1f}" rx="{w+4}" ry="{(w+4)*.42:.1f}" fill="{INK}" opacity=".18"/>')
    s.rect(bx-w,by-h,w,h,"#2A2927"); s.rect(bx,by-h,w,h,"#0E0D0C")
    s.add(f'<ellipse cx="{bx:.1f}" cy="{by-h:.1f}" rx="{w}" ry="{w*.42:.1f}" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>')
    tips[g["name"]]=(bx,by-h)
# ledger on right (sorted by people), leader lines
L=sorted(GEO["gov"],key=lambda g:tips[g["name"]][1])
y0=140; gap=47
for i,g in enumerate(L):
    ty=y0+i*gap; tx,tyy=tips[g["name"]]
    s.path(f"M{tx:.1f},{tyy:.1f} L{1090-14:.1f},{ty-4:.1f} L1090,{ty-4:.1f}",stroke=INK,sw=.6,op=.65)
    s.text(1100,ty-8,g["name"].upper(),10.5,INK,SANS,600,ls=1.2)
    s.text(1100,ty+13,f'{g["rate"]:.1f}%',17,CLAY if g["rate"]>=23 else INK,SERIF,700)
    s.text(1160,ty+12,f'{g["u"]:,} unemployed',11,STONE,SANS)
    s.rect(1300,ty-6,0.0014*g["u"]*0+g["u"]/155900*92,10,INK)
# editorial column
s.text(48,100,"THE RELIEF  ·  GOVERNORATE ATLAS",11,CLAY,MONO,600,ls=1.8)
for i,l in enumerate(["Where the rate","is highest is not","where the people are."]):
    s.text(48,150+i*46,l,38,INK,SERIF,700)
for i,l in enumerate(["Ground colour is the unemployment rate.","Spire height is the number of unemployed","Jordanians. The two tell different stories."]): s.text(48,308+i*21,l,13.5,SLATE)
s.line(48,380,330,380,INK,1)
for k,(lab,big,col,sub) in enumerate([("HIGHEST RATE","28.8%",CLAY,"Ma'an  ·  12,749 unemployed Jordanians"),("MOST PEOPLE","155,900",INK,"Amman  ·  rate 19.1%  ·  36% of the national total"),("THREE GOVERNORATES","70%",INK,"Amman, Irbid and Zarqa hold 7 in 10 of the unemployed")]):
    y=412+k*112
    s.text(48,y,lab,10,STONE,MONO,600,ls=1.5); s.text(48,y+44,big,42,col,SERIF,700); s.text(48,y+66,sub,12,SLATE)
lx,ly=48,770
s.text(lx,ly-10,"GROUND  ·  RATE",10,STONE,MONO,600,ls=1.2)
for i in range(15): s.rect(lx+i*12,ly,12,10,ramp(15+i))
s.text(lx,ly+26,"15%",10,STONE,MONO); s.text(lx+180,ly+26,"29%",10,STONE,MONO,anchor="end")
s.text(48,818,"Rates are derived annual 2025: unemployed ÷ (unemployed + employed), DoS counts. Not a DoS-published governorate rate.",11,STONE,MONO)
s.save("concepts/A_relief.svg")
