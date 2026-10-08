import os
def _find_repo():
    d = os.path.dirname(os.path.abspath(__file__))
    while d and not os.path.isdir(os.path.join(d, "08_Jordanian_Unemployment_Truth")):
        nd = os.path.dirname(d)
        if nd == d: break
        d = nd
    return d
REPO = os.environ.get("REPO_ROOT") or _find_repo()
import json,urllib.request,hashlib,datetime,os,sys
A="https://jorinfo.dos.gov.jo/Databank/api/v1/en/DOS_Database/12/"
RAW=os.path.join(REPO, "08_Jordanian_Unemployment_Truth", "01_Raw")
def q(tbl,dim):
    # dim: None for total, else a variable code to break down by
    body={"query":[{"code":"TIME","selection":{"filter":"all","values":["*"]}}],"response":{"format":"json-stat"}}
    if dim: body["query"].append({"code":dim,"selection":{"filter":"all","values":["*"]}})
    r=urllib.request.Request(A+tbl,data=json.dumps(body).encode(),headers={"Content-Type":"application/json","User-Agent":"Mozilla/5.0"})
    try:
        d=urllib.request.urlopen(r,timeout=120).read()
    except Exception as e:
        return None,str(e)[:200]+(e.read().decode()[:300] if hasattr(e,'read') else '')
    return d,None
out=[]
for tbl in ("EMPALL1","EMPALL"):
    for dim in (None,"SEX","AGE","EDU","GOV"):
        d,err=q(tbl,dim)
        fn=f"PX_{tbl}_{dim or 'TOTAL'}.json"
        if d is None: print("FAIL",fn,err); continue
        open(os.path.join(RAW,fn),"wb").write(d)
        m=dict(filename=fn,title=f"DoS PxWeb {tbl} by {dim or 'total'} x Time",url=A+tbl,retrieved=datetime.datetime.now().astimezone().isoformat(timespec="seconds"),size=len(d),sha256=hashlib.sha256(d).hexdigest(),status="OK")
        open(os.path.join(RAW,fn+".meta.json"),"w").write(json.dumps(m,indent=1))
        print("OK",fn,len(d))
