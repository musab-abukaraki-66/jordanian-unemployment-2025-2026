from final_common import *
import math,json
s=S(); chapter_strip(s,2)
s.text(48,100,"THE PLACES  ·  GOVERNORATES",11.5,CLAY,SANS,700,ls=1.8)
for i,l in enumerate(["The highest rate and the","most people are in","different places."]): s.text(48,152+i*50,l,44,INK,SERIF,700)
SC=480;OX=60;OY=322
def P(x,y): return (OX+x*SC,OY+y*SC)
raw=json.load(open(EV+r"\01_Raw\geo\geoBoundaries-JOR-ADM1.geojson",encoding="utf8"))
allp=[(x*math.cos(math.radians(31.0)),y) for f in raw["features"] for x,y in f["geometry"]["coordinates"][0]]
X0=min(p[0] for p in allp);Y1=max(p[1] for p in allp);Y0=min(p[1] for p in allp)
def N(lon,lat): return ((lon*math.cos(math.radians(31.0))-X0)/(Y1-Y0),(Y1-lat)/(Y1-Y0))
CAP={"Amman":(35.93,31.95),"Irbid":(35.85,32.55),"Zarqa":(36.09,32.07),"Balqa":(35.73,32.04),"Madaba":(35.79,31.72),"Mafraq":(36.21,32.34),"Jerash":(35.90,32.28),"Ajloun":(35.75,32.33),"Karak":(35.70,31.18),"Tafilah":(35.60,30.84),"Ma'an":(35.73,30.19),"Aqaba":(35.00,29.53)}
SEL="Ma'an"
for g in GEO["gov"]:
    d="M"+" L".join(f"{P(x,y)[0]:.1f},{P(x,y)[1]:.1f}" for x,y in g["pts"])+"Z"
    sel=g["name"]==SEL
    s.path(d,fill=ramp(g["rate"]),stroke=INK if sel else PAPER,sw=2.6 if sel else 1.4,op=1 if sel else .92)
for g in sorted(GEO["gov"],key=lambda g:-g["u"]):
    bx,by=P(*N(*CAP[g["name"]])); r=math.sqrt(g["u"])*0.053
    s.circ(bx,by,r+2,PAPER,.9); s.circ(bx,by,r,INK,.88)
s.text(48,296,"Ground colour = rate · Disc area = number of unemployed Jordanians",12,MUTE)
# legend
s.text(440,730,"RATE",11,MUTE,SANS,700,ls=1.2)
for i in range(15): s.rect(484+i*12,720,12,10,ramp(15+i))
s.text(484,746,"15%",11,MUTE); s.text(664,746,"29%",11,MUTE,anchor="end")
s.circ(448,780,4,INK); s.circ(472,780,9,INK); s.text(492,784,"5k / 20k people",11,MUTE)
# ledger = click targets
rx=800; s.line(rx-40,100,rx-40,820,RULE,1)
s.text(rx,112,"GOVERNORATE LEDGER  ·  2025 ANNUAL, DERIVED",11.5,MUTE,SANS,700,ls=1.2)
s.text(rx+250,134,"RATE",11,MUTE,SANS,700,anchor="end"); s.text(rx+400,134,"UNEMPLOYED",11,MUTE,SANS,700,anchor="end"); s.text(rx+592,134,"SHARE",11,MUTE,SANS,700,anchor="end")
L=sorted(GEO["gov"],key=lambda g:-g["u"]); tot=sum(g["u"] for g in L)
for i,g in enumerate(L):
    y=168+i*36; sel=g["name"]==SEL
    if sel: s.rect(rx-16,y-20,624,32,SAND,.7)
    s.rect(rx,y-10,12,12,ramp(g["rate"]))
    s.text(rx+22,y+1,g["name"],14,INK,SANS,700 if sel else 400)
    s.text(rx+250,y+2,f'{g["rate"]:.1f}%',16,CLAY if g["rate"]>=24 else INK,SERIF,700,"end")
    s.text(rx+400,y+1,f'{g["u"]:,}',13,INK,SANS,anchor="end")
    s.rect(rx+420,y-8,max(2,g["u"]/tot*172*3.0*0+g["u"]/155900*100),9,INK); s.text(rx+592,y+1,f'{100*g["u"]/tot:.0f}%',13,MUTE,SANS,anchor="end")
# selected caption
s.rect(rx-16,612,624,160,PAPER,stroke=INK,sw=1)
s.text(rx,640,"SELECTED  ·  MA'AN",11.5,CLAY,SANS,700,ls=1.4)
s.text(rx,684,"28.8%",40,CLAY,SERIF,700); s.text(rx+150,670,"highest derived rate in 2025",13,INK,SANS,600); s.text(rx+150,690,"12,749 unemployed Jordanians (3% of all)",13,MUTE)
s.text(rx,722,"DoS published Ma'an's Q2 2026 quarterly rate separately: 33.2%. Different period and basis; not comparable.",12,MUTE)
s.text(rx,758,"DoS publishes no sampling error; small governorates can move several points year to year.",12,MUTE)
s.text(rx,742,"Amman: 19.1%, but 155,900 people (36%). Amman, Irbid and Zarqa hold 70%.",12,MUTE)
x=chip(s,rx,800,"DERIVED FROM DoS COUNTS","der"); x=chip(s,x,800,"NOT A DoS-PUBLISHED GOVERNORATE RATE","lim")
foot(s,"Source: DoS PxWeb EMPALL1/EMPALL, 2025 annual (Jordanians 15+); Q2 2026 release for Ma'an 33.2%. Boundaries: geoBoundaries (CC BY 2.5).","BACK TO THE NUMBER  ↺")
s.save("concepts/F3_places.svg")
