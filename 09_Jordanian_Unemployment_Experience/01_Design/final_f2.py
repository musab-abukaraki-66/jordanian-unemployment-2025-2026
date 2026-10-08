from final_common import *
s=S(); chapter_strip(s,1)
s.text(48,100,"THE PEOPLE  ·  WHO IS BEHIND THE RATE",11.5,CLAY,SANS,700,ls=1.8)
for i,l in enumerate(["The rate and the people","tell opposite stories."]): s.text(48,152+i*50,l,44,INK,SERIF,700)
s.text(48,246,"Two lenses on the same Jordanians. Switch the lens on the left; compare it with the rate on the right.",14,MUTE)
# lens control
s.text(48,288,"LENS",11,MUTE,SANS,700,ls=1.4)
for i,t in enumerate(["Sex","Age","Education"]):
    x=100+i*104; a=(i==0)
    s.rect(x,272,98,26,INK if a else PAPER,stroke=INK,sw=1); s.text(x+49,290,t,12,PAPER if a else INK,SANS,600,"middle")
# left: 100 unemployed grid by sex, ordered blocks, direct labels
s.text(48,330,"100 UNEMPLOYED JORDANIANS, 2025",11.5,INK,SANS,700,ls=1.2)
R=11;G=29;gx,gy=48,350
seq=[SLATE]*66+[CLAY]*34
for i,c in enumerate(seq): s.circ(gx+(i%10)*G+R,gy+(i//10)*G+R,R,c)
lx=gx+10*G+24
s.text(lx,gy+40,"66",44,SLATE,SERIF,700); s.text(lx+70,gy+40,"are men",15,INK,SANS,600)
s.text(lx,gy+240,"34",44,CLAY,SERIF,700); s.text(lx+70,gy+240,"are women",15,INK,SANS,600)
s.text(gx,gy+316,"Of every 100 unemployed Jordanians, two in three are men.",12.5,MUTE)
# right: rate lens
rx=760; s.line(rx-44,310,rx-44,820,RULE,1)
s.text(rx,330,"THE RATE, 2025: UNEMPLOYED IN EVERY 100 WORKERS AND JOB-SEEKERS",11.5,INK,SANS,700,ls=1.2)
R2=9;G2=24
def g2(x,y,n,c,lab,sub):
    for i in range(100): s.circ(x+(i%10)*G2+R2,y+(i//10)*G2+R2,R2,c if i<n else MIST)
    s.text(x,y+G2*10+34,str(n),48,c,SERIF,700); s.text(x+64,y+G2*10+16,lab,14,INK,SANS,600); s.text(x+64,y+G2*10+34,sub,12,MUTE)
g2(rx,350,18,SLATE,"of 100 men in the labour force","are unemployed: 17.95% (derived annual)")
g2(rx+300,350,33,CLAY,"of 100 women in the labour force","are unemployed: 33.21% (derived annual)")
s.text(rx,664+48,"",12)
# why both true
s.rect(rx,722,560,0.01,INK)
s.text(rx,740,"Why both are true",14,INK,SERIF,700)
for i,l in enumerate(["Only 14.7 in 100 Jordanian women are in the labour force, against 53.6 in 100 men (Q2 2026).","A higher rate on a small base is fewer people than a lower rate on a large one."]): s.text(rx,762+i*20,l,12.5,MUTE)
# youth note
x=chip(s,48,758,"DERIVED","der"); x=chip(s,x,758,"LIMITED EVIDENCE: SMALL BASE","lim")
s.text(48,790,"Youth (15–24): 47.2% in 2025, from annual counts. DoS publishes age 24+ only (18.0% in Q2 2026).",12.5,MUTE)
foot(s,"Source: DoS PxWeb counts EMPALL1/EMPALL (2025 annual, Jordanians 15+); participation from DoS Q2 2026 release. Shares rounded to whole people per 100.","NEXT: WHERE ARE THEY?  →")
s.save("concepts/F2_people.svg")
