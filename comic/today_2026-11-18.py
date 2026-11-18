from comiclib import *
sky='<rect width="330" height="355" fill="url(#h6)"/>'
def plow(x,y,s=1,rot=0):
    # ground contact at (x,y); points right
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})" {ST}>'
            f'<path d="M-60,-62 L40,-14" fill="none" stroke-width="7"/><path d="M-60,-62 L40,-14" fill="none" stroke="{PAPER}" stroke-width="3"/>'
            f'<path d="M-62,-64 l-10,-26 M-46,-56 l-8,-28" fill="none" stroke-width="4"/>'
            f'<path d="M-10,-38 l-4,30 M14,-26 l-2,22" fill="none" stroke-width="4"/>'
            f'<path d="M-24,-6 Q10,-14 46,4 Q16,6 -24,2 Z" fill="url(#h4)"/>'
            f'<path d="M-30,0 h70" fill="none" stroke-width="1.6"/></g>')
def sprout(x,y,s=1):
    return f'<g transform="translate({x},{y}) scale({s})" {ST}><path d="M0,0 v-12" fill="none" stroke-width="1.8"/><path d="M0,-10 q-8,-6,-10,-2 q4,6,10,2 M0,-12 q8,-8,11,-3 q-4,6,-11,3" fill="{PAPER}" stroke-width="1.5"/></g>'
def zigfield(y0):
    out=f'<path d="M0,{y0} L330,{y0-30} L330,355 L0,355 Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
    pts=[(10,y0+14),(310,y0+4),(30,y0+34),(316,y0+26),(16,y0+56),(318,y0+50)]
    out+='<path d="M'+" L".join(f"{a},{b}" for a,b in pts)+f'" fill="none" stroke="{INK}" stroke-width="2.2" stroke-dasharray="7 4"/>'
    for (a,b),(c,d) in zip(pts,pts[1:]):
        for t in (0.2,0.45,0.7,0.9):
            out+=sprout(a+(c-a)*t,b+(d-b)*t,.9)
    return out
# P1: the gift
p1=sky+hills(292)+grass(240,312,3)+alien(62,300,.9,True,"flat",arms="point")+alien(170,302,.72,False,"happy",arms="down")+plow(268,304,1.0)
p1+=bubble(10,30,310,76,["GIFT: THE PLOW.","TILL THE SOIL. GROW FOOD."],(80,104,102,104),(70,172))
# P2: Grog sleds down the hill on it
slope=f'<path d="M0,170 L330,320 L330,355 L0,355 Z" fill="url(#h5)" stroke="{INK}" stroke-width="2.4"/>'
p2=sky+slope+caveman(168,236,.78,look="s",mood="happy",rot=24)+plow(214,292,1.05,24)+speedlines(96,196,5,30,200)
p2+=bubble(14,30,300,62,["WHEEEE! GROG SLED!"],(110,90,132,90),(140,128))
# P3: spring
p3=sky+sun(286,64,18)+zigfield(250)+alien(48,262,.62,True,"shocked")+alien(110,262,.5,False,"happy")
p3+=bubble(4,34,250,62,["HIS SLED TRACKS...","SPROUTED!"],(100,92,120,92),(110,168))
# P4: Grog claims credit
p4=sky+zigfield(276)+caveman(218,300,.85,look="s",mood="happy")+alien(52,290,.62,True,"flat")+alien(112,292,.5,False,"worried")
p4+=bubble(150,30,176,74,["GROG INVENT","FARMING!"],(222,102,242,102),(226,180))
p4+=bubble(2,96,150,62,["TECHNICALLY...","A SUCCESS."],(40,154,60,154),(52,178))
open("today.svg","w").write(strip([panel(0,p1,"EARTH, 6,000 B.C."),panel(1,p2,"THAT AFTERNOON"),panel(2,p3,"SPRING"),panel(3,p4)]))
