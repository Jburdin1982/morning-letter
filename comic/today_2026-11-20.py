from comiclib import *
sky='<rect width="330" height="355" fill="url(#h6)"/>'
ground=lambda y: f'<path d="M0,{y} H330 V355 H0 Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
def netbundle(x,y,s=1):
    return f'<g transform="translate({x},{y}) scale({s})" {ST}><path d="M-30,0 q-6,-26,10,-34 q20,-10,40,0 q16,8,10,34 Z" fill="url(#x1)"/><path d="M-30,0 q30,8,60,0" fill="none"/><circle cx="-24" cy="2" r="3" fill="{PAPER}"/><circle cx="24" cy="2" r="3" fill="{PAPER}"/></g>'
def hammock(x1,x2,y,sag):
    xm=(x1+x2)/2
    o=f'<path d="M{x1},{y} Q{xm},{y+2*sag} {x2},{y} Q{xm},{y+2*sag-30} {x1},{y} Z" fill="url(#x1)" stroke="{INK}" stroke-width="2.4"/>'
    o+=f'<path d="M{x1},{y} Q{xm},{y+2*sag} {x2},{y}" fill="none" stroke="{INK}" stroke-width="3"/>'
    return o
def fish(x,y,s=1,flip=False):
    sx=-s if flip else s
    return f'<g transform="translate({x},{y}) scale({sx},{s})" {ST}><path d="M-16,0 q16,-12,30,0 q-14,12,-30,0 Z" fill="url(#h2)"/><path d="M-16,0 l-10,-8 v16 Z" fill="{PAPER}"/><circle cx="8" cy="-2" r="1.8" fill="{INK}"/></g>'
def water(y):
    return f'<path d="M0,{y} H330 V355 H0 Z" fill="url(#h6)" stroke="{INK}" stroke-width="2.4"/>'+''.join(f'<path d="M{x},{y+18} q8,-6,16,0 q8,6,16,0" fill="none" stroke="{INK}" stroke-width="1.6"/>' for x in (20,120,220,280))
# P1: the gift
p1=sky+ground(300)+grass(260,300,3)+alien(70,300,.9,True,"flat")+alien(200,302,.72,False,"happy",arms="up")+netbundle(200,176,.9)
p1+=bubble(6,34,250,70,["GIFT: THE FISHING NET.","A HUNDRED FISH AT ONCE."],(110,102,130,102),(92,196))
# P2: Grog with the net, ?
p2=sky+sun(290,64,16)+ground(300)+grass(40,300,3)+grass(280,300,2)+caveman(170,300,.85,look="up",mood="confused")+netbundle(120,282,.8)
p2+='<text x="168" y="160" text-anchor="middle" class="big" style="font-size:44px">?</text>'
# P3: hammock
p3=sky+sun(165,60,14)+ground(312)+tree(40,312,.8)+tree(290,312,.8)
p3+=hammock(44,286,214,26)
p3+=caveman(165,232,.62,look="side",mood="happy",rot=-82)
p3+='<text x="214" y="160" class="big" style="font-size:18px">z</text><text x="226" y="146" class="big" style="font-size:22px">z</text>'
p3+=bubble(70,32,210,62,["AHHH. GROG","CATCH NAP."],(146,92,164,92),(142,214))
# P4: aliens watch
p4=sky+water(306)+fish(60,336,.9)+fish(150,328,.9,True)+fish(250,338,.8)
p4+=alien(60,306,.62,True,"flat")+alien(140,306,.5,False,"worried")
p4+=bubble(150,96,170,58,["FISH CAUGHT:","ZERO."],(176,148,192,150),(146,258))
p4+=bubble(10,34,250,64,["BUT HE DID INVENT","THE WEEKEND."],(54,94,72,96),(62,212))
open("today.svg","w").write(strip([panel(0,p1,"EARTH, 8,000 B.C."),panel(1,p2,"THE NEXT MORNING"),panel(2,p3,"FRIDAY"),panel(3,p4,"BY THE RIVER")]))
