from common import *
s=S(); furniture(s,"CONCEPT D  —  THE EVIDENCE LEDGER","DoS press release Q2 2026 (7 Sep 2026), 'UERATE by sex and nationality' table and text. Secondary: World Bank WDI SL.UEM.TOTL.ZS (modeled ILO estimate), 2025.")
s.text(48,100,"THE EVIDENCE LEDGER  ·  RECONCILIATION",11,CLAY,MONO,600,ls=1.8)
s.text(48,152,"One survey. One quarter.",40,INK,SERIF,700); s.text(48,198,"Eight different answers.",40,CLAY,SERIF,700)
s.text(48,232,"Every figure below is correct. They differ because each one counts a different group of people.",14,SLATE)
AX0,AX1=640,1340
def ax(v): return AX0+(AX1-AX0)*v/35
rows=[("Non-Jordanian residents","everyone living in Jordan who is not a citizen",8.2,"DoS published",SLATE),
 ("All residents","Jordanians and non-Jordanians together: the usual headline",16.1,"DoS published",SLATE),
 ("World Bank, 2025 (annual)","modeled ILO estimate for all residents",16.5,"Secondary · modeled",STONE),
 ("Jordanians aged 24+","citizens, older age base",18.0,"DoS published",INK),
 ("Jordanian men","citizens, 15+",18.5,"DoS published",INK),
 ("All women residents","Jordanian and non-Jordanian women",19.9,"DoS published",STONE),
 ("Jordanians 15+","citizens: the figure this project is about",21.0,"DoS published",CLAY),
 ("Jordanian women","citizens, 15+",30.3,"DoS published",INK)]
y0=290; rh=62
for v in (0,5,10,15,20,25,30,35):
    s.line(ax(v),y0-24,ax(v),y0+rh*len(rows)-24,RULE,.8); s.text(ax(v),y0-34,f"{v}%",10,STONE,MONO,anchor="middle")
for i,(a,b,v,tag,col) in enumerate(rows):
    y=y0+i*rh; hl=(col==CLAY)
    if hl: s.rect(40,y-24,1360,rh-6,SAND,.55)
    s.text(56,y+2,a,15,INK,SERIF,700 if hl else 400); s.text(56,y+22,b,11.5,SLATE)
    s.line(AX0,y+4,ax(v),y+4,col,2)
    s.circ(ax(v),y+4,8 if hl else 6,col)
    s.text(ax(v)+14,y+9,f"{v:.1f}%",18 if hl else 15,col if col!=STONE else INK,SERIF,700,"start")
    s.text(1392,y+22,tag,10,STONE,MONO,anchor="end")
s.text(48,818,"Jordanian rates are the DoS observed survey figures. The World Bank value is shown for reconciliation only and is never used for Jordanians.",11,STONE,MONO)
s.save("concepts/D_evidence.svg")
