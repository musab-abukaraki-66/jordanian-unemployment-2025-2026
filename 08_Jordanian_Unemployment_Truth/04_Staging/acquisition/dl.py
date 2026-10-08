import os
def _find_repo():
    d = os.path.dirname(os.path.abspath(__file__))
    while d and not os.path.isdir(os.path.join(d, "08_Jordanian_Unemployment_Truth")):
        nd = os.path.dirname(d)
        if nd == d: break
        d = nd
    return d
REPO = os.environ.get("REPO_ROOT") or _find_repo()
import sys,os,hashlib,json,datetime,urllib.request,time
raw=os.path.join(REPO, "08_Jordanian_Unemployment_Truth", "01_Raw")
B="https://dosweb.dos.gov.jo/DataBank/News/Unemployment/"
items=[l.split("|") for l in open(sys.argv[1],encoding="utf8").read().split("\n") if l.strip()]
log=[]
for url,title in items:
    fn=url.rsplit("/",1)[1]
    dest=os.path.join(raw,fn)
    if os.path.exists(dest): print("skip",fn); continue
    for a in (1,2):
        try:
            r=urllib.request.Request(url,headers={"User-Agent":"Mozilla/5.0"})
            d=urllib.request.urlopen(r,timeout=90).read()
            if not d.startswith(b"%PDF") and not d.startswith(b"PK"): raise Exception("not pdf/xlsx")
            open(dest,"wb").write(d)
            m=dict(filename=fn,title=title,url=url,retrieved=datetime.datetime.now().astimezone().isoformat(timespec="seconds"),size=len(d),sha256=hashlib.sha256(d).hexdigest(),status="OK")
            open(os.path.join(raw,fn+".meta.json"),"w").write(json.dumps(m,indent=1))
            print("OK",fn,len(d)); break
        except Exception as e:
            print("FAIL",a,fn,e); time.sleep(2)
    else:
        open(os.path.join(raw,fn+".FAILED.json"),"w").write(json.dumps(dict(filename=fn,title=title,url=url,status="FAILED",retrieved=datetime.datetime.now().astimezone().isoformat(timespec="seconds"))))
