from comiclib import *
sky='<rect width="330" height="355" fill="url(#h6)"/>'
def umbrella(x,y,s=1,up=True,rot=0,berries=False):
    # (x,y) = tip of handle end; canopy above if up, below (bowl) if not
    g=f'<g transform="translate({x},{y}) rotate({rot if up else 180+rot}) scale({s})" {ST}>'
    g+=f'<path d="M0,0 v-70" fill="none" stroke-width="3"/><path d="M0,0 q0,8,-8,8 q-6,0,-6,-6" fill="none" stroke-width="3"/>'
    g+=f'<path d="M-50,-62 Q-48,-108,0,-112 Q48,-108,50,-62 q-12,-8,-25,0 q-12,-8,-25,0 q-12,-8,-25,0 q-12,-8,-25,0 Z" fill="{PAPER}"/>'
    g+=f'<path d="M-25,-62 Q-24,-96,0,-112 M25,-62 Q24,-96,0,-112" fill="none" stroke-width="1.8"/>'
    g+=f'<path d="M-46,-66 Q-44,-98,-14,-108 L-20,-70 Z" fill="url(#h1)" stroke="none"/>'
    g+=f'<path d="M0,-112 v-8" stroke-width="3"/>'
    g+='</g>'
    if berries:
        import random; r=random.Random(7)
        g+="".join(f'<circle cx="{x+r.randint(-40,40)*s:.0f}" cy="{y+ (100-6)*s - r.randint(0,10):.0f}" r="{6*s:.1f}" fill="url(#h4)" stroke="{INK}" stroke-width="1.6"/>' for _ in range(9))
    return g
def rain(seed,n=40):
    r=random.Random(seed); return "".join(f'<line x1="{(a:=r.randint(0,340))}" y1="{(b:=r.randint(30,340))}" x2="{a-6}" y2="{b+16}" stroke="{INK}" stroke-width="1.6" stroke-linecap="round"/>' for _ in range(n))
ground=lambda y: f'<path d="M0,{y} H330 V355 H0 Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
# P1: the gift
p1=sky+sun(290,70,18)+ground(300)+grass(250,300,3)+alien(70,300,.9,True,"flat",arms="down")+alien(196,302,.72,False,"happy",arms="up")+umbrella(221,224,.62)
p1+=bubble(8,32,240,66,["GIFT: THE UMBRELLA.","IT KEEPS YOU DRY."],(140,94,162,94),(178,218))
# P2: Grog's berry bowl in the sun
p2=sky+sun(50,70,18)+ground(304)+tree(285,304,.75)+umbrella(150,206,.85,up=False,berries=False)+caveman(222,304,.8,look="side",mood="happy")
p2+="".join(f'<circle cx="{cx}" cy="{cy}" r="6" fill="url(#h4)" stroke="{INK}" stroke-width="1.6"/>' for cx,cy in [(120,292),(134,290),(148,293),(162,290),(176,292),(128,282),(142,281),(156,282),(170,283),(149,272)])
p2+=bubble(84,36,236,62,["GROG BERRY BOWL!"],(212,94,232,94),(226,178))
# P3: the rain arrives
p3='<rect width="330" height="355" fill="url(#h5)" opacity=".35"/>'+cloud(40,70,1.6)+cloud(200,60,1.8)+rain(3,46)+ground(306)
p3+=caveman(236,306,.8,look="up",mood="happy")
p3+=alien(48,306,.62,True,"flat")+alien(110,306,.5,False,"worried")
p3+=bubble(10,92,190,66,["HE'S SOAKED.","USE IT, GROG..."],(60,154,80,154),(62,200))
# P4: berry soup
p4='<rect width="330" height="355" fill="url(#h5)" opacity=".35"/>'+rain(9,30)+ground(306)+umbrella(214,198,.7,up=False)
p4+='<path d="M180,262 Q214,276 248,262" fill="none" stroke="'+INK+'" stroke-width="1.8" stroke-dasharray="4 3"/>'
p4+=caveman(274,306,.72,look="side",mood="happy",flip=True)
p4+=alien(44,306,.6,True,"tired")+alien(104,306,.5,False,"happy")
p4+=bubble(150,30,176,66,["GROG MAKE","BERRY SOUP!"],(250,92,270,92),(268,150))
p4+=bubble(2,108,168,66,["A GIFT FOR","ALL WEATHER!"],(84,170,104,170),(104,218))
open("today.svg","w").write(strip([panel(0,p1,"EARTH, 9,000 B.C."),panel(1,p2,"A DRY WEEK"),panel(2,p3,"SUNDAY"),panel(3,p4,"LATER")]))
