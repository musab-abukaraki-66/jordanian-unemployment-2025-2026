from common import *
s=S(); furniture(s,"CONCEPT C  —  ONE HUNDRED JORDANIANS","2025 annual shares of unemployed Jordanians (15+), from DoS PxWeb person counts, rounded to whole people per 100 (largest-remainder). Derived; not DoS-published shares.")
s.text(48,100,"ONE HUNDRED JORDANIANS  ·  WHO IS BEHIND THE RATE",11,CLAY,MONO,600,ls=1.8)
for i,l in enumerate(["Take 100 unemployed","Jordanians.","Who are they?"]): s.text(48,150+i*46,l,38,INK if i<2 else CLAY,SERIF,700)
for i,l in enumerate(["The rate says one thing. The people say","another. Switch the lens and the same","hundred dots reorganise."]): s.text(48,320+i*21,l,13.5,SLATE)
def grid(x0,y0,groups,r=10,gap=26,labels=True):
    seq=[c for n,c in groups for _ in range(n)]
    for i,c in enumerate(seq):
        s.circ(x0+(i%10)*gap+r,y0+(i//10)*gap+r,r,c)
lens=[("SEX",[(66,SLATE),(34,CLAY)],[("66 men",SLATE),("34 women",CLAY)],"Two in three unemployed Jordanians are men."),
      ("AGE",[(35,CLAY),(30,mix(CLAY,SAND,.35)),(25,mix(CLAY,SAND,.7)),(10,SAND)],[("35  aged 15–24",CLAY),("30  aged 25–29",mix(CLAY,SAND,.35)),("25  aged 30–39",mix(CLAY,SAND,.7)),("10  aged 40+",STONE)],"Two in three are under 30."),
      ("EDUCATION",[(45,DEEP),(8,CLAY),(8,mix(CLAY,SAND,.5)),(39,SAND)],[("45  bachelor or higher",DEEP),("8  diploma",CLAY),("8  secondary",mix(CLAY,SAND,.5)),("39  below secondary",STONE)],"Nearly half hold a bachelor degree or higher.")]
for k,(nm,gr,leg,cap) in enumerate(lens):
    x=440+k*320; act=(k==0)
    s.text(x,172,nm,11,CLAY if act else STONE,MONO,600,ls=1.6)
    s.line(x,180,x+260,180,INK if act else RULE,1.5 if act else 1)
    grid(x,198,gr)
    for j,(t,c) in enumerate(leg):
        s.circ(x+6,478+j*20,5,c); s.text(x+18,482+j*20,t,12,INK,SANS)
    s.text(x,580,cap,12.5,SLATE,SANS,600)
s.line(440,606,1340,606,INK,1)
s.text(440,634,"BUT THE RATE TELLS THE OPPOSITE STORY  ·  IN EVERY 100 PEOPLE IN THE LABOUR FORCE",10,STONE,MONO,600,ls=1.2)
def g2(x,y,n,c):
    for i in range(100): s.circ(x+(i%10)*15+5,y+(i//10)*15+5,5,c if i<n else MIST)
g2(440,660,18,SLATE); s.text(610,700,"18",44,SLATE,SERIF,700); s.text(610,724,"of 100 Jordanian men",12,SLATE); s.text(610,740,"are unemployed",12,SLATE)
g2(800,660,33,CLAY); s.text(970,700,"33",44,CLAY,SERIF,700); s.text(970,724,"of 100 Jordanian women",12,SLATE); s.text(970,740,"are unemployed",12,SLATE)
s.text(1130,672,"Why both are true",11,INK,SANS,700)
for i,l in enumerate(["Only about 15 in 100 Jordanian","women are in the labour force,","against 54 in 100 men. A high","rate on a small base is fewer","people than a lower rate on a","large one."]): s.text(1130,692+i*18,l,12,SLATE)
s.text(48,818,"Rates (18 / 33) are 2025 derived annual: men 17.95%, women 33.21%. Participation (Q2 2026, DoS): women 14.7%, men 53.6%.",11,STONE,MONO)
s.save("concepts/C_hundred.svg")
