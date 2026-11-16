from comiclib import *
sky='<rect width="330" height="355" fill="url(#h6)"/>'
def compass(x,y,s=1,ang=0):
    return (f'<g transform="translate({x},{y}) scale({s})" {ST}><circle r="16" fill="{PAPER}"/><circle r="12" fill="none" stroke-width="1.2"/>'
            f'<text x="0" y="-5" text-anchor="middle" class="s" style="font-size:8px;stroke:none">N</text>'
            f'<g transform="rotate({ang})"><path d="M0,-11 L3,0 L-3,0 Z" fill="{INK}" stroke-width="1"/><path d="M0,11 L3,0 L-3,0 Z" fill="{PAPER}" stroke-width="1"/></g></g>')
def qmark(x,y): return f'<text x="{x}" y="{y}" text-anchor="middle" class="s" style="font-size:38px">?</text>'
def snow(n,seed,y0=40,y1=330):
    import random as R; r=R.Random(seed)
    return "".join(f'<circle cx="{r.randint(6,324)}" cy="{r.randint(y0,y1)}" r="{r.choice([1.6,2,2.6])}" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>' for _ in range(n))
# P1: aliens with the gift
p1=sky+hills(292)+grass(270,312,3)+alien(70,300,.9,True,"flat",arms="down")+alien(185,302,.72,False,"happy",arms="up")+compass(222,226,1.1,0)
p1+=bubble(10,26,310,80,["GIFT: THE COMPASS.","HE'LL NEVER BE LOST AGAIN."],(160,104,182,104),(178,206))
# P2: Grog gets it
p2=sky+hills(296)+caveman(150,326,.95,look="s",mood="confused")+compass(108,236,1.2,0)+qmark(150,186)
p2+=bubble(14,24,300,70,["SHINY ARROW SAY...","THAT WAY!"],(140,92,162,92),(150,140))
# P3: Grog marching north, aliens peek
p3=sky+mountains(250)+hills(318)+caveman(232,330,.72,look="side",mood="happy")+speedlines(190,300,3,18,180)+compass(272,262,.9,0)
p3+=alien(40,332,.62,True,"flat")+alien(96,334,.5,False,"worried")
p3+=bubble(6,26,170,56,["IT ONLY","POINTS NORTH."],(50,80,66,80),(42,196))
p3+=bubble(150,96,176,56,["HOW FAR NORTH","IS NORTH?"],(150,148,170,148),(100,262))
# P4: snowy north
cold='<rect width="330" height="355" fill="url(#h4)" opacity=".35"/>'
p4=cold+mountains(240)+hills(316)+snow(40,11)+caveman(225,330,.8,look="s",mood="shocked")+compass(268,252,1,0)
p4+=alien(52,332,.62,True,"tired")+alien(112,334,.5,False,"happy")
p4+=bubble(150,26,174,64,["GROG NOT LOST.","GROG COLD."],(226,88,246,88),(232,170))
p4+=bubble(4,110,170,60,["WELL... IT DID","WORK."],(96,168,116,168),(112,262))
open("today.svg","w").write(strip([panel(0,p1,"EARTH — 9,000 B.C."),panel(1,p2),panel(2,p3,"THREE DAYS LATER"),panel(3,p4,"THE FAR NORTH")]))
