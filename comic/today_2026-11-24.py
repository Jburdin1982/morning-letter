from comiclib import *
sky='<rect width="330" height="355" fill="url(#h6)"/>'
night='<rect width="330" height="355" fill="url(#h4)" opacity=".55"/>'
ground=lambda y: f'<path d="M0,{y} H330 V355 H0 Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
def scope(x,y,rot=-30,s=1):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})" {ST}>'
            f'<path d="M0,-6 h34 v12 h-34 Z" fill="url(#h1)"/><path d="M34,-8 h30 v16 h-30 Z" fill="{PAPER}"/>'
            f'<path d="M64,-10 h22 v20 h-22 Z" fill="url(#h2)"/><path d="M44,-8 v16 M74,-10 v20" fill="none" stroke-width="1.4"/></g>')
def pie(cx,cy,r):
    crimp=''.join(f'<circle cx="{cx+r*math.cos(a*math.pi/12):.1f}" cy="{cy+r*math.sin(a*math.pi/12):.1f}" r="{r*.13:.1f}" fill="{PAPER}"/>' for a in range(24))
    return (f'<g {ST}><circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#h2)"/>{crimp}<circle cx="{cx}" cy="{cy}" r="{r*.82:.1f}" fill="{PAPER}"/>'
            f'<path d="M{cx},{cy} L{cx},{cy-r*.8:.1f} M{cx},{cy} L{cx+r*.7:.1f},{cy+r*.4:.1f} M{cx},{cy} L{cx-r*.7:.1f},{cy+r*.4:.1f}" fill="none" stroke-width="1.6"/>'
            f'<path d="M{cx-r*.3:.1f},{cy-r*.35:.1f} q6,-6,12,0 M{cx+r*.2:.1f},{cy+r*.15:.1f} q6,-6,12,0" fill="none" stroke-width="1.4"/></g>')
# P1: the gift
p1=sky+ground(300)+grass(250,300,3)+alien(62,300,.9,True,"flat")+alien(170,302,.72,False,"happy",arms="up")+scope(206,280,-20,1.0)
p1+=bubble(6,30,300,72,["GIFT: THE TELESCOPE.","STUDY THE HEAVENS!"],(104,100,124,100),(94,196))
# P2: Grog finds it
p2=sky+ground(300)+rock(270,302,1.2)+caveman(150,300,1.0,look="s",mood="confused")+scope(70,292,-8,.9)
p2+=f'<text x="150" y="168" class="big" text-anchor="middle" style="font-size:40px">?</text>'
# P3: night, full moon through the telescope
p3=night+stars(14,7,40,120)+ground(300)+caveman(70,300,.9,look="up",mood="shocked")+scope(80,224,-38,.9)
p3+=f'<path d="M150,166 L192,132" stroke="{INK}" stroke-width="1.6" stroke-dasharray="4 4"/>'+pie(250,110,62)
p3+=bubble(136,214,186,58,["MOON...","IS PIE!"],(142,236,146,254),(100,246))
# P4: punchline
p4=night+moon(276,70,26)+ground(300)+alien(46,300,.8,True,"flat")+caveman(232,300,.9,look="up",mood="happy")
p4+=f'<g {ST}><path d="M270,226 l22,-60" fill="none" stroke-width="3"/><path d="M286,170 l-2,-14 M290,172 l2,-14 M294,174 l6,-12" fill="none" stroke-width="2"/></g>'
p4+=bubble(4,40,170,58,["HE THINKS THE MOON","IS A PIE."],(48,96,66,96),(52,196))
p4+=bubble(120,118,150,52,["GROG SAVE","ROOM."],(200,168,218,168),(222,200))
open("today.svg","w").write(strip([panel(0,p1,"EARTH, 4,000 B.C."),panel(1,p2,"NEXT DAY"),panel(2,p3,"FULL MOON"),panel(3,p4,"STILL WAITING")]))
