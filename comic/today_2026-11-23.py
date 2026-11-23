from comiclib import *
sky='<rect width="330" height="355" fill="url(#h6)"/>'
night='<rect width="330" height="355" fill="url(#h4)" opacity=".55"/>'
ground=lambda y: f'<path d="M0,{y} H330 V355 H0 Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
def needle(x,y,s=1):
    return (f'<g transform="translate({x},{y}) scale({s})" {ST}><path d="M0,0 L46,-46" stroke-width="3.2" fill="none"/>'
            f'<ellipse cx="42" cy="-42" rx="3" ry="6" fill="{PAPER}" stroke-width="1.6" transform="rotate(45 42 -42)"/>'
            f'<path d="M44,-44 q24,-10,18,14 q-6,22,22,18" fill="none" stroke-width="1.6" stroke-dasharray="4 2"/></g>')
_cid=[0]
def sackman(x,y,s=1,mood="happy",rot=0):
    """Grog sewn into a fur sack: only his head shows. Feet-level at (x,y)."""
    _cid[0]+=1; cid=f"sk{_cid[0]}"
    head=f'<clipPath id="{cid}"><rect x="-34" y="-130" width="68" height="64"/></clipPath><g clip-path="url(#{cid})">{caveman(0,0,1,look="s",mood=mood)}</g>'
    sack=(f'<path d="M-30,-66 q-14,30,-8,66 q38,10,76,0 q6,-36,-8,-66 q-30,8,-60,0 Z" fill="url(#h3)" {ST}/>'
          f'<path d="M-30,-66 q30,8,60,0" fill="none" {ST}/>'
          + ''.join(f'<path d="M{-26+i*8},-70 l4,8" stroke="{INK}" stroke-width="1.8"/>' for i in range(7))
          + f'<path d="M-32,-30 l6,4 l-6,4 M34,-40 l-6,4 l6,4" fill="none" stroke="{INK}" stroke-width="1.6"/>')
    return f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">{head}{sack}</g>'
# P1: the gift
p1=sky+ground(300)+grass(250,300,3)+alien(62,300,.9,True,"flat")+alien(170,302,.72,False,"happy",arms="up")+needle(226,286,1.0)
p1+=bubble(6,30,300,72,["GIFT: NEEDLE AND THREAD.","SEW WARM CLOTHES FOR WINTER."],(104,100,124,100),(94,196))
# P2: that night Grog sews himself into his sleeping fur
p2=night+stars(12,5,40,130)+moon(288,64)+ground(300)+rock(40,302,1.1)+sackman(170,300,1.0)
p2+=bubble(40,34,230,64,["GROG SEW FUR SHUT.","GROG SNUG!"],(176,96,194,96),(178,190))
# P3: morning, hopping
p3=sky+sun(292,140,16)+ground(300)+grass(40,300,2)+sackman(200,270,.95,mood="shocked",rot=-8)+speedlines(150,296,4,22,180)
p3+=f'<path d="M150,300 q14,-30,28,-6 M118,300 q14,-26,24,-4" fill="none" stroke="{INK}" stroke-width="1.6" stroke-dasharray="3 4"/>'
p3+=f'<text x="70" y="250" class="big" text-anchor="middle" transform="rotate(-8 70 250)">HOP!</text><text x="96" y="200" class="big" text-anchor="middle" style="font-size:16px">HOP!</text>'
p3+=bubble(14,32,250,58,["MORNING. GROG STUCK.","GROG MUST... HOP."],(186,88,204,86),(204,156))
# P4: punchline
p4=sky+ground(300)+alien(56,300,.85,True,"flat")+alien(130,302,.66,False,"happy")+sackman(250,300,.8,mood="happy")
p4+=f'<g {ST}><path d="M200,300 v-46 M300,300 v-46" fill="none"/><path d="M200,258 h100" stroke-dasharray="6 4" fill="none" stroke-width="2"/></g>'
p4+=bubble(4,30,150,52,["HE SEWED","HIMSELF IN."],(52,80,68,80),(60,160))
p4+=bubble(160,30,166,58,["GROG INVENT","SACK RACE!"],(244,86,260,84),(252,196))
p4+=bubble(70,110,140,40,["WELL... HE'S WARM."],(118,148,132,148),(132,222)).replace('class="s"','class="s" style="font-size:11px"')
open("today.svg","w").write(strip([panel(0,p1,"EARTH, 30,000 B.C., FIRST FROST"),panel(1,p2,"THAT NIGHT"),panel(2,p3,"NEXT MORNING"),panel(3,p4,"BY NOON")]))
