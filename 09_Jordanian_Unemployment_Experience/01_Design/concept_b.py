from common import *
s=S(); furniture(s,"CONCEPT B  —  THE TREADMILL","Quarterly: DoS Labour Force Survey press releases (Jordanian section). Annual 2020-2025: person counts from DoS PxWeb; annual rates derived (unemployed ÷ labour force).")
s.text(48,100,"THE TREADMILL  ·  PERSISTENCE",11,CLAY,MONO,600,ls=1.8)
s.text(48,160,"Ten quarters.",52,INK,SERIF,700); s.text(48,214,"One number.",52,CLAY,SERIF,700)
s.text(48,252,"The Jordanian unemployment rate has stayed between 21.0% and 21.5% since the start of 2024.",14,SLATE)
X0,X1,Y0,Y1=70,930,300,560  # chart box
def cx(i): return X0+(X1-X0)*i/17
def cy(v): return Y1-(Y1-Y0)*(v-15)/(36-15)
for v in (15,20,25,30,35):
    s.line(X0,cy(v),X1,cy(v),RULE,.8); s.text(X0-12,cy(v)+4,f"{v}",11,STONE,MONO,anchor="end")
s.rect(cx(8),cy(21.5),cx(17)-cx(8),cy(21.0)-cy(21.5),SAND,.9)
s.text(cx(8),cy(21.5)-44,"21.0 – 21.5%",12,INK,MONO,600)
s.line(cx(8),cy(21.5)-34,cx(17),cy(21.5)-34,INK,1); s.line(cx(8),cy(21.5)-38,cx(8),cy(21.5)-30,INK,1); s.line(cx(17),cy(21.5)-38,cx(17),cy(21.5)-30,INK,1)
s.text(cx(12.5),cy(21.5)-42,"10 consecutive quarters",11,STONE,SANS,anchor="middle")
def pl(vals,col,w,dash=None):
    d="M"+" L".join(f"{cx(i):.1f},{cy(v):.1f}" for i,v in enumerate(vals))
    s.path(d,stroke=col,sw=w)
pl(FEM,CLAY,1.8); pl(MALE,SLATE,1.8); pl(TOT,INK,3.4)
s.circ(cx(17),cy(TOT[-1]),5,INK); s.circ(cx(17),cy(FEM[-1]),4,CLAY); s.circ(cx(17),cy(MALE[-1]),4,SLATE)
s.text(cx(17)+14,cy(FEM[-1])+4,"Women 30.3",12,CLAY,SANS,600); s.text(cx(17)+14,cy(TOT[-1])+4,"All Jordanians 21.0",12,INK,SANS,700); s.text(cx(17)+14,cy(MALE[-1])+4,"Men 18.5",12,SLATE,SANS,600)
for i in range(0,18,2): s.text(cx(i),Y1+20,QL[i].replace(" "," "),10,STONE,MONO,anchor="middle")
s.text(X0,Y0-24,"JORDANIAN UNEMPLOYMENT RATE, QUARTERLY, Q1 2022 – Q2 2026",10,STONE,MONO,600,ls=1.2)
# right: the numbers behind
rx=1090
s.line(rx-30,100,rx-30,560,RULE,1)
s.text(rx,112,"BENEATH THE FLAT LINE · 2020 → 2025",10,STONE,MONO,600,ls=1.2)
s.text(rx,170,"+255,854",44,INK,SERIF,700); s.text(rx,194,"more Jordanians in work (+19.1%)",13,SLATE)
s.text(rx,262,"+27,570",44,CLAY,SERIF,700); s.text(rx,286,"more Jordanians unemployed (+6.8%)",13,SLATE)
s.text(rx,354,"+16.3%",44,INK,SERIF,700); s.text(rx,378,"growth in the Jordanian labour force",13,SLATE)
s.text(rx,430,"The labour force grew faster than the number",12.5,SLATE); s.text(rx,448,"of people the rate was measured against.",12.5,SLATE)
s.text(rx,486,"Rate 2020: 23.2%  →  2025: 21.3%  (derived)",11,STONE,MONO)
# bottom: ground strip
s.line(48,590,1392,590,INK,1)
s.text(48,614,"THE GROUND KEEPS MOVING  ·  JORDANIAN LABOUR FORCE, ANNUAL (derived rate printed above each column)",10,STONE,MONO,600,ls=1.2)
base=842; sc=170/2_030_000; bw=96; gx=70
for k,y in enumerate(range(2020,2026)):
    u,e=ANN[y]; x=gx+k*(bw+58)
    he=e*sc; hu=u*sc
    s.rect(x,base-he,bw,he,SLATE,.88); s.rect(x,base-he-hu,bw,hu,CLAY)
    r=100*u/(u+e)
    s.text(x+bw/2,base-he-hu-10,f"{r:.1f}%",17,INK,SERIF,700,"middle"); s.text(x+bw/2,base+18,str(y),11,STONE,MONO,anchor="middle")
    s.text(x+bw/2,base-he-hu/2+4,f"{u/1000:.0f}k",10.5,PAPER,SANS,600,"middle")
s.text(x+bw+22,base-20,"employed",11,SLATE,SANS,600); s.text(x+bw+22,base-he-hu/2+4,"unemployed",11,CLAY,SANS,600)
s.text(1090,700,"2025 annual rate 21.31% is derived,",11,STONE,MONO); s.text(1090,716,"not published by DoS as an annual",11,STONE,MONO); s.text(1090,732,"press-release figure.",11,STONE,MONO)
s.save("concepts/B_treadmill.svg")
