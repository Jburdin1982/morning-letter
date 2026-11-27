from comiclib import *
sky='<rect width="330" height="355" fill="url(#h6)"/>'
ground=lambda y: f'<path d="M0,{y} H330 V355 H0 Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
def coin(x,y,r=9): return f'<g {ST}><circle cx="{x}" cy="{y}" r="{r}" fill="{PAPER}"/><circle cx="{x}" cy="{y}" r="{r*.55:.1f}" fill="url(#h1)" stroke-width="1.2"/></g>'
def sack(x,y): return f'<g {ST}><path d="M{x-22},{y} q-6,-30,10,-42 l-4,-8 h32 l-4,8 q16,12,10,42 Z" fill="url(#h2)"/><path d="M{x-8},{y-50} h16" fill="none"/></g>'
def shine(x,y): return ''.join(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y-9}" stroke="{INK}" stroke-width="1.6" transform="rotate({a} {x} {y+14})"/>' for a in (-50,-25,0,25,50))
# P1: the gift
p1=sky+ground(300)+grass(300,300,3)+alien(60,300,.85,True,"flat")+sack(170,300)+coin(128,292)+coin(214,293)+coin(232,295,7)+alien(270,302,.68,False,"happy",arms="up")
p1+=bubble(8,34,286,66,["GIFT: MONEY.","TRADE INSTEAD OF GRAB."],(70,96,90,96),(64,176))
# P2: Grog finds a coin
p2=sky+ground(300)+rock(40,302,1.1)+coin(120,292,10)+caveman(200,300,.9,look="s",mood="confused")
p2+=f'<text x="200" y="170" class="big" text-anchor="middle" style="font-size:40px">?</text>'
# P3: coin necklace
p3=sky+ground(300)+tree(276,300,.8)+caveman(140,300,.95,look="s",mood="happy")
p3+=f'<path d="M122,{300-95*.95+12} q18,44,36,0" fill="none" stroke="{INK}" stroke-width="2.2"/>'+coin(140,300-95*.95+36,8)+shine(140,300-95*.95+28)
p3+=bubble(30,40,250,52,["GROG SHINY!"],(130,92,148,92),(142,170))
# P4: dawn line
p4=sky+moon(300,190,13)+ground(300)+caveman(105,300,.72,look="s",mood="happy")+caveman(185,300,.68,look="s",mood="flat")+caveman(258,300,.64,look="s",mood="flat")
p4+=alien(36,300,.58,False,"worried")
p4+=bubble(4,30,210,58,["THEY CAMPED ALL NIGHT","FOR MORE SHINY."],(34,88,48,88),(38,250))
p4+=bubble(150,104,176,46,["GROG FIRST IN LINE!"],(130+30,150,150+30,150),(110,212))
open("today.svg","w").write(strip([panel(0,p1,"EARTH, 25,000 B.C."),panel(1,p2,"NEXT MORNING"),panel(2,p3,"THAT AFTERNOON"),panel(3,p4,"FRIDAY, BEFORE DAWN")]))
