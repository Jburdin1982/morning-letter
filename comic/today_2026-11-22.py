from comiclib import *
sky='<rect width="330" height="355" fill="url(#h6)"/>'
ground=lambda y: f'<path d="M0,{y} H330 V355 H0 Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
def tablet(x,y,s=1,lines=None,blank=True,fs=9.5):
    o=f'<g transform="translate({x},{y}) scale({s})" {ST}><path d="M-30,0 v-62 q0,-14,30,-14 q30,0,30,14 v62 Z" fill="url(#h2)"/><path d="M-22,-4 v-54 q0,-9,22,-9 q22,0,22,9 v54 Z" fill="{PAPER}"/>'
    if lines:
        for i,l in enumerate(lines):
            o+=f'<text x="0" y="{-50+i*fs*1.3:.1f}" font-family="DejaVu Serif" font-size="{fs}" font-weight="bold" text-anchor="middle" fill="{INK}" stroke="none">{l}</text>'
    elif not blank:
        for i in range(4): o+=f'<path d="M-14,{-50+i*11} h28" fill="none" stroke-width="1.4" stroke-dasharray="3 3"/>'
    return o+'</g>'
def chisel(x,y): return f'<g {ST}><path d="M{x},{y} l18,-18" stroke-width="3" fill="none"/><rect x="{x+14}" y="{y-28}" width="10" height="10" fill="url(#h1)" transform="rotate(45 {x+19} {y-23})"/></g>'
# P1 the gift
p1=sky+ground(300)+grass(270,300,3)+alien(62,300,.9,True,"flat")+alien(180,302,.72,False,"happy",arms="up")+tablet(268,300,1.0,blank=False)
p1+=bubble(6,30,290,72,["GIFT: WRITING.","KNOWLEDGE FOR THE AGES!"],(112,100,132,100),(96,196))
# P2 Grog carving
p2=sky+ground(300)+rock(50,300,1.1)+tablet(140,300,1.2,blank=True)+chisel(162,262)+caveman(240,300,.85,look="side",mood="happy",flip=True)
p2+=bubble(60,30,250,64,["GROG WRITE","MOST IMPORTANT THING!"],(220,92,238,92),(240,186))
# P3 reveal
p3=sky+ground(300)+tablet(165,292,2.0,lines=["GROG FEAST:","MEAT","MEAT","PIE","MORE MEAT"],fs=4.7)+alien(46,300,.62,True,"flat")+alien(290,302,.52,False,"happy")
p3+=bubble(8,26,316,52,["THE FIRST WRITTEN WORDS...","...ARE A FEAST LIST."],(60,76,52,90),(48,200))
# P4 punchline
p4=sky+ground(300)+tree(285,300,.8)+alien(56,300,.85,True,"flat")+alien(140,302,.68,False,"happy")+caveman(228,300,.8,look="side",mood="happy",flip=True)
p4+=bubble(6,26,170,58,["WELL, KNOWLEDGE","WAS SAVED."],(110,82,128,80),(140,212))
p4+=bubble(150,100,176,62,["GROG NEVER","FORGET PIE!"],(232,160,248,158),(232,190))
open("today.svg","w").write(strip([panel(0,p1,"EARTH, 3,200 B.C."),panel(1,p2,"THAT AFTERNOON"),panel(2,p3,"AN HOUR LATER"),panel(3,p4,"THANKSGIVING WEEK, ROUGHLY")]))
