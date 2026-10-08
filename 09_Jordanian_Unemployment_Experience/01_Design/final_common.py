from common import *
MUTE="#40372F"   # secondary text, >=4.5:1 on paper
def chapter_strip(s,active):
    items=[("1","The number"),("2","The people"),("3","The places")]
    s.line(48,52,1392,52,INK,1)
    x=48
    for i,(n,t) in enumerate(items):
        a=(i==active)
        w=150
        s.text(x,40,f"{n}  {t.upper()}",11.5,INK if a else MUTE,SANS,700 if a else 400,ls=1.4)
        if a: s.rect(x,44,w-20,3,CLAY)
        x+=w+10
    s.text(1392,40,"JORDANIAN CITIZENS  ·  DoS LABOUR FORCE SURVEY  ·  2025–2026",11,MUTE,SANS,400,"end",1.2)
def chip(s,x,y,label,kind):
    col={"pub":(INK,PAPER),"der":(CLAY,PAPER),"sec":(PAPER,MUTE),"lim":(SAND,INK)}[kind]
    w=len(label)*8.0+24
    if kind=="sec": s.rect(x,y-13,w,20,PAPER,stroke=MUTE,sw=1)
    else: s.rect(x,y-13,w,20,col[0])
    s.text(x+11,y+1,label,11,col[1] if kind!="lim" else INK,SANS,600,ls=.4)
    return x+w+8
def foot(s,src,nxt=None):
    s.line(48,846,1392,846,RULE,1)
    s.text(48,870,src,11.5,MUTE,SANS)
    if nxt:
        s.rect(1160,852,232,34,INK); s.text(1276,874,nxt,12,PAPER,SANS,600,"middle",.4)
