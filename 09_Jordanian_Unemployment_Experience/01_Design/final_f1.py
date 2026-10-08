from final_common import *
s=S(); chapter_strip(s,0)
s.text(48,100,"THE NUMBER  ·  WHAT 21 PERCENT MEANS",11.5,CLAY,SANS,700,ls=1.8)
for i,l in enumerate(["Unemployment among","Jordanians has not moved","in ten quarters."]): s.text(48,152+i*50,l,44,INK,SERIF,700)
# hero + chips
s.text(48,368,"21.0%",64,CLAY,SERIF,700); s.text(276,352,"of Jordanian citizens in the labour force",14,INK,SANS,600); s.text(276,372,"were unemployed in Q2 2026 (age 15+).",14,MUTE)
x=chip(s,48,402,"DoS PUBLISHED","pub"); x=chip(s,x,402,"JORDANIAN CITIZENS ONLY","lim")
# chart
X0,X1,Y0,Y1=70,820,470,760
def cx(i): return X0+(X1-X0)*i/17
def cy(v): return Y1-(Y1-Y0)*(v-15)/(36-15)
for v in (15,20,25,30,35):
    s.line(X0,cy(v),X1,cy(v),RULE,.8); s.text(X0-12,cy(v)+4,f"{v}",11.5,MUTE,SANS,anchor="end")
s.rect(cx(8),cy(21.5),cx(17)-cx(8),cy(21.0)-cy(21.5),SAND)
def pl(vals,col,w): s.path("M"+" L".join(f"{cx(i):.1f},{cy(v):.1f}" for i,v in enumerate(vals)),stroke=col,sw=w)
pl(FEM,CLAY,1.6); pl(MALE,SLATE,1.6); pl(TOT,INK,3.6)
s.circ(cx(17),cy(TOT[-1]),5.5,INK)
for ser,idx,col in ((FEM,5,CLAY),(FEM,9,CLAY),(MALE,5,SLATE),(MALE,9,SLATE)):
    s.add(f'<circle cx="{cx(idx):.1f}" cy="{cy(ser[idx]):.1f}" r="4" fill="{PAPER}" stroke="{col}" stroke-width="1.6"/>')
s.text(cx(17)+12,cy(FEM[-1])+4,"Women 30.3",12,CLAY,SANS,700); s.text(cx(17)+12,cy(TOT[-1])+4,"All Jordanians 21.0",12,INK,SANS,700); s.text(cx(17)+12,cy(MALE[-1])+4,"Men 18.5",12,SLATE,SANS,700)
by=cy(21.5)-38
s.line(cx(8),by,cx(17),by,INK,1); s.line(cx(8),by-5,cx(8),by+5,INK,1); s.line(cx(17),by-5,cx(17),by+5,INK,1)
s.text((cx(8)+cx(17))/2,by-10,"10 quarters between 21.0% and 21.5%",12,INK,SANS,700,"middle")
for i in range(0,18,3): s.text(cx(i),Y1+22,QL[i],11,MUTE,SANS,anchor="middle")
s.text(X0,Y0-30,"JORDANIAN UNEMPLOYMENT RATE BY QUARTER, Q1 2022 – Q2 2026  ·  AXIS STARTS AT 15%",11,MUTE,SANS,700,ls=1)
# right: ledger of three answers
rx=1000; s.line(rx-40,100,rx-40,820,RULE,1)
s.text(rx,112,"THE SAME QUARTER, THREE ANSWERS",11.5,MUTE,SANS,700,ls=1.2)
rows=[("All residents","Jordanians and non-Jordanians together",16.1,INK),("Jordanians","citizens, age 15+",21.0,CLAY),("Jordanian women","citizens, age 15+",30.3,INK)]
for i,(a,b,v,c) in enumerate(rows):
    y=170+i*128
    if c==CLAY: s.rect(rx-16,y-34,400,104,SAND,.6)
    s.text(rx,y,a,18,INK,SERIF,700); s.text(rx,y+20,b,12,MUTE)
    ax=lambda t: rx+ (360)*t/35
    s.line(rx,y+48,rx+360,y+48,RULE,1.2); s.line(rx,y+48,ax(v),y+48,c,3); s.circ(ax(v),y+48,7,c)
    s.text(rx+360,y+14,f"{v:.1f}%",24,c,SERIF,700,"end")
s.text(rx,562,"Non-Jordanian residents: 8.2%. Expatriate workers are 42% of the",12,MUTE); s.text(rx,580,"employed (Q2 2026); the all-resident rate is lower.",12,MUTE)
s.line(rx-40,620,1392,620,RULE,1)
s.text(rx,650,"THE PEOPLE BEHIND THE RATE  ·  2020 → 2025",11.5,MUTE,SANS,700,ls=1.2)
s.text(rx,692,"+255,854",34,INK,SERIF,700); s.text(rx+190,692,"more Jordanians employed",13,MUTE)
s.text(rx,736,"+27,570",34,CLAY,SERIF,700); s.text(rx+190,736,"more Jordanians unemployed",13,MUTE)
s.text(rx,764,"Rate over the same years: 23.2% to 21.3%.",12.5,MUTE)
x=chip(s,rx,792,"DERIVED FROM DoS COUNTS","der")
foot(s,"Source: DoS press releases (Jordanian section); PxWeb counts 2020, 2025. Hollow points: read from DoS chart labels only. Provenance: 02_Data/quarterly_series_provenance.csv","NEXT: WHO ARE THEY?  →")
s.save("concepts/F1_number.svg")
