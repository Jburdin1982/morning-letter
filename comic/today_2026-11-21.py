from comiclib import *
sky='<rect width="330" height="355" fill="url(#h6)"/>'
ground=lambda y: f'<path d="M0,{y} H330 V355 H0 Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
def candle(x,y,s=1,lit=True):
    o=f'<g transform="translate({x},{y}) scale({s})" {ST}><rect x="-6" y="-34" width="12" height="34" fill="{PAPER}"/><path d="M-6,-28 h12" stroke-width="1.4" fill="none"/><path d="M0,-34 v-6" fill="none" stroke-width="2"/>'
    if lit: o+=f'<path d="M0,-58 q8,10,4,16 q-4,4,-8,0 q-4,-6,4,-16 Z" fill="{PAPER}"/><path d="M0,-50 q3,4,1,7" fill="none" stroke-width="1.4"/>'
    return o+'</g>'
def cake(x,y,s=1):
    return f'<g transform="translate({x},{y}) scale({s})" {ST}><path d="M-34,0 q0,-26,34,-28 q34,2,34,28 Z" fill="url(#h2)"/><path d="M-30,-10 q30,8,60,0" fill="none" stroke-width="1.6"/><rect x="-40" y="0" width="80" height="8" fill="url(#h1)"/></g>'
def glow(x,y,r):
    return f'<circle cx="{x}" cy="{y}" r="{r}" fill="{PAPER}" stroke="{INK}" stroke-width="1.2" stroke-dasharray="3 5"/>'
night=f'<rect width="330" height="355" fill="url(#h4)"/>'
# P1 gift
p1=sky+ground(300)+grass(260,300,3)+alien(70,300,.9,True,"flat")+alien(200,302,.72,False,"happy",arms="up")+candle(262,300,1.1)
p1+=bubble(6,34,262,70,["GIFT: THE CANDLE.","LIGHT FOR THE LONG NIGHTS."],(112,102,132,102),(92,196))
# P2 dusk: Grog with mud cake and candle
p2=sky+moon(36,140,15)+ground(300)+rock(60,300,1.2)+cake(160,300,1.1)+candle(160,270,.9)+caveman(255,300,.85,look="side",mood="happy",flip=True)
p2+=bubble(70,40,220,64,["GROG KNOW!","MUD CAKE!"],(214,100,232,98),(246,188))
# P3 the wish
p3=night+glow(160,210,95)+ground(300)+cake(150,300,1.1)+candle(150,270,.9,lit=False)+caveman(225,300,.85,look="side",mood="happy",flip=True)
p3+=bubble(14,36,250,64,["MAKE WISH...","PFFFT!"],(176,98,196,96),(198,200))
p3+='<path d="M150,222 q-10,-14,4,-24 q12,-10,2,-26" fill="none" stroke="#3a2a14" stroke-width="2" stroke-dasharray="4 4"/>'
# P4 total dark: just eyes
eyes=lambda x,y,s=1: f'<g transform="translate({x},{y}) scale({s})"><ellipse cx="-8" cy="0" rx="7" ry="4" fill="{PAPER}" transform="rotate(20 -8 0)"/><ellipse cx="8" cy="0" rx="7" ry="4" fill="{PAPER}" transform="rotate(-20 8 0)"/></g>'
geyes=lambda x,y: f'<g><circle cx="{x-8}" cy="{y}" r="5" fill="{PAPER}"/><circle cx="{x+8}" cy="{y}" r="5" fill="{PAPER}"/><circle cx="{x-8}" cy="{y}" r="2" fill="{INK}"/><circle cx="{x+8}" cy="{y}" r="2" fill="{INK}"/></g>'
p4=f'<rect width="330" height="355" fill="{INK}"/>'+eyes(60,218,1.1)+eyes(130,248)+geyes(250,250)
p4+=bubble(10,40,170,58,["IT WENT OUT."],(80,96,98,96),(128,232))
p4+=bubble(140,112,184,66,["GROG WISH","FOR LIGHT!"],(236,174,256,172),(250,236))
open("today.svg","w").write(strip([panel(0,p1,"EARTH, 9,000 B.C."),panel(1,p2,"THAT EVENING"),panel(2,p3,"A MOMENT LATER"),panel(3,p4,"A MOMENT AFTER THAT")]))
