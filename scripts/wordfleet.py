"""Word Fleet generator. usage: python3 wordfleet.py words.json letter_text.html > fleet.json
words.json: {"date":"YYYY-MM-DD","words":[{"word":"CAMPING","hint":"..."},...]}
Verifies every word occurs in the letter text, places words (across/down) in a 9x9 grid, fills with random letters."""
import json,sys,random,re,html
N=10
cfg=json.load(open(sys.argv[1])); txt=open(sys.argv[2]).read() if len(sys.argv)>2 else ""
txt=re.sub(r'<style.*?</style>','',txt,flags=re.S); txt=re.sub(r'<svg.*?</svg>','',txt,flags=re.S); txt=html.unescape(re.sub(r'<[^>]+>',' ',txt)).lower()
have=set(re.findall(r"[a-z]+",txt))
W=[(w["word"].upper(),w["hint"]) for w in cfg["words"]]
if cfg.get("require_in_letter"):
    for w,_ in W: assert w.lower() in have, f"{w} not in letter"
rnd=random.Random(cfg["date"])
def place():
    g=[[None]*N for _ in range(N)]; out=[]
    for k,(w,h) in enumerate(sorted(W,key=lambda x:-len(x[0]))):
        for _ in range(400):
            d="A" if k<2 else "D"; r=rnd.randrange(N-(len(w)-1 if d=="D" else 0)); c=rnd.randrange(N-(len(w)-1 if d=="A" else 0))
            cells=[(r+(i if d=="D" else 0),c+(i if d=="A" else 0)) for i in range(len(w))]
            if all(g[a][b] in (None,w[i]) for i,(a,b) in enumerate(cells)) and not any(g[a][b] for a,b in cells[:0]):
                # avoid overlaps entirely: ships may not touch cells of other ships
                if any(g[a][b] is not None for a,b in cells): continue
                if d=="A" and any(0<=rr<N and 0<=cc<N and g[rr][cc] is not None for rr in (r-1,r+1) for cc in range(c-1,c+len(w)+1)): continue
                if d=="D" and any(0<=rr<N and 0<=cc<N and g[rr][cc] is not None for cc in (c-1,c+1) for rr in range(r-1,r+len(w)+1)): continue
                for i,(a,b) in enumerate(cells): g[a][b]=w[i]
                out.append(dict(word=w,hint=h,r=r,c=c,dir=d)); break
        else: return None
    return g,out
res=None
for _try in range(5000):
    res=place()
    if res: break
assert res, 'could not place words; use shorter words'
g,ships=res
mask=[[1 if g[r][c] else 0 for c in range(N)] for r in range(N)]
alpha="ABCDEFGHIJKLMNOPRSTUW"
for r in range(N):
    for c in range(N):
        if not g[r][c]: g[r][c]=rnd.choice(alpha)
# sanity: each ship word found exactly where placed
def lines(g):
    for r in range(N): yield "".join(g[r]),("A",r)
    for c in range(N): yield "".join(g[r][c] for r in range(N)),("D",c)
for s in ships:
    assert sum(l.count(s["word"]) for l,_ in lines(g))>=1
print(json.dumps(dict(date=cfg["date"],size=N,grid=["".join(r) for r in g],ships=sorted(ships,key=lambda s:s["word"])),indent=1))
