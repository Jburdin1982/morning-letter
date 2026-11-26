from comiclib import *
sky='<rect width="330" height="355" fill="url(#h6)"/>'
ground=lambda y: f'<path d="M0,{y} H330 V355 H0 Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
def rain(seed,n=34,y1=290,skip=None):
    r=random.Random(seed); out=""
    for _ in range(n):
        x=r.randint(6,326); y=r.randint(34,y1)
        if skip and skip[0]<x<skip[2] and skip[1]<y<skip[3]: continue
        out+=f'<line x1="{x}" y1="{y}" x2="{x-6}" y2="{y+16}" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>'
    return out
def table(x,y,w=200,h=104):
    # x = left edge, y = ground
    t=y-h
    return (f'<g {ST}><path d="M{x},{t} h{w} v12 h-{w} Z" fill="url(#h3)"/>'
            f'<path d="M{x+10},{t+12} v{h-12} h10 v-{h-12} M{x+w-20},{t+12} v{h-12} h10 v-{h-12}" fill="{PAPER}"/>'
            f'<path d="M{x+4},{t+4} h{w-8}" stroke-width="1.2" fill="none"/></g>')
# P1: the gift
p1=sky+ground(300)+grass(300,300,3)+alien(52,300,.85,True,"flat")+table(110,300,150,70)+alien(286,302,.68,False,"happy",arms="up")
p1+=bubble(8,34,260,66,["GIFT: THE TABLE.","GATHER THE TRIBE. SHARE."],(64,96,84,96),(56,176))
# P2: Grog finds it
p2=sky+ground(300)+rock(30,302,1.1)+table(60,300,150,70)+caveman(250,300,.9,look="s",mood="confused")
p2+=f'<text x="250" y="168" class="big" text-anchor="middle" style="font-size:40px">?</text>'
# P3: sleet; Grog dry under the table
p3=sky+rain(4,46,288,(60,186,270,300))+ground(300)+table(60,300,210,118)+caveman(165,300,.82,look="s",mood="happy")
p3+=bubble(30,40,270,58,["GROG HOUSE!","NO WET!"],(150,96,172,96),(166,180))
# P4: punchline
p4=sky+rain(11,46,288,(110,186,330,300))+ground(300)+table(112,300,212,118)+caveman(170,300,.78,look="s",mood="happy")+caveman(262,300,.74,look="s",mood="happy",flip=True)
p4+=alien(54,300,.8,True,"flat")
p4+=bubble(112,34,212,58,["GROG TRIBE","THANKFUL FOR ROOF!"],(196,90,214,90),(176,204))
p4+=bubble(4,112,148,50,["WELL... THEY","GATHERED."],(42,160,58,160),(52,196))
open("today.svg","w").write(strip([panel(0,p1,"EARTH, 30,000 B.C."),panel(1,p2,"THAT EVENING"),panel(2,p3,"THANKSGIVING SLEET"),panel(3,p4,"AN HOUR LATER")]))
