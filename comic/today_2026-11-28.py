from comiclib import *
sky='<rect width="330" height="355" fill="url(#h6)"/>'
ground=lambda y: f'<path d="M0,{y} H330 V355 H0 Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
def abacus(x,y,rot=0,s=1):
    g=f'<g transform="translate({x},{y}) rotate({rot}) scale({s})" {ST}><rect x="-30" y="-24" width="60" height="48" fill="{PAPER}" stroke-width="3"/>'
    for i,ry in enumerate((-14,-2,10)):
        g+=f'<line x1="-30" y1="{ry}" x2="30" y2="{ry}" stroke-width="1.4"/>'
        for k in range(4): g+=f'<circle cx="{-24+k*9+(i%2)*14}" cy="{ry}" r="4.2" fill="url(#h2)" stroke-width="1.2"/>'
    return g+'</g>'
def itch(x,y): return ''.join(f'<path d="M{x+dx},{y+dy} l6,-4 l-4,-4 l6,-4" fill="none" stroke="{INK}" stroke-width="1.6"/>' for dx,dy in ((0,0),(14,10),(-12,14)))
p1=sky+ground(300)+grass(260,300,3)+alien(60,300,.85,True,"flat")+alien(178,302,.7,False,"happy",arms="up")+abacus(236,272,0,.9)
p1+=bubble(6,30,306,70,["GIFT: THE ABACUS.","COUNT YOUR TRADE GOODS!"],(104,98,124,98),(80,180))
p2=sky+ground(300)+rock(276,302,1.1)+abacus(70,286,-8,.8)+caveman(170,300,1.0,look="s",mood="confused")
p2+=f'<text x="170" y="168" class="big" text-anchor="middle" style="font-size:40px">?</text>'
p3=sky+ground(300)+tree(286,300,.75)+caveman(140,300,1.0,look="s",mood="happy")+abacus(178,250,-25,.7)+itch(204,262)
p3+=bubble(20,34,250,62,["AHHH.","GROG SCRATCH!"],(120,96,138,96),(138,168))
p4=sky+ground(300)+alien(60,300,.85,True,"flat")+caveman(240,300,.95,look="s",mood="happy")+abacus(276,240,-30,.6)
p4+=bubble(6,110,180,56,["THINGS COUNTED:","ZERO."],(56,166,74,166),(64,196))
p4+=bubble(130,30,190,56,["ITCHES COUNTED:","ALSO ZERO!"],(226,86,244,86),(240,176))
open("today.svg","w").write(strip([panel(0,p1,"EARTH, 3,000 B.C."),panel(1,p2,"NEXT MORNING"),panel(2,p3,"MARKET DAY"),panel(3,p4,"CLOSING TIME")]))
