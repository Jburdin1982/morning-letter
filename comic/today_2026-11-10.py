from comiclib import *
sky='<rect width="330" height="355" fill="url(#h6)"/>'
def mapsheet(x,y,s=1,rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})" {ST}>'
            '<rect x="-34" y="-26" width="68" height="52" fill="#f7f0dd"/>'
            '<path d="M-24,12 q10,-24 22,-8 t24,-10" fill="none" stroke-dasharray="3 3"/>'
            '<path d="M14,-18 l10,10 M24,-18 l-10,10" fill="none"/></g>')
def roast(x,y,s=1):
    return f'<g transform="translate({x},{y}) scale({s})" {ST}><ellipse cx="0" cy="0" rx="20" ry="12" fill="url(#h3)"/><path d="M14,-4 l14,-10 M14,4 l14,10" fill="none"/></g>'
p1=sky+sun(270,70)+mountains(255)+hills(285)+grass(20,300,2)+mapsheet(165,300,1.1)+alien(60,285,.9,True,"flat",arms="point")+alien(115,288,.8,False,"happy")+caveman(268,320,.7,look="s")
p1+=bubble(8,30,255,56,["TODAY'S GIFT: A MAP.","IT SHOWS WHERE THINGS ARE."],(60,86,85,86),(68,190))
p2=sky+sun(270,60)+hills(290)+caveman(170,318,.95,look="up",mood="happy")+mapsheet(170,206,1.1,180)
p2+=f'<text x="262" y="214" class="s" style="font-size:30px">?</text>'
p2+=bubble(14,36,200,50,["THE PICTURE IS","UPSIDE DOWN!"],(130,86,150,86),(140,190))
p3=sky+hills(300)+grass(30,312,2)+mapsheet(165,326,1.6)+roast(165,312,1.1)+caveman(255,322,.9,look="s",mood="happy")
p3+=bubble(8,36,190,52,["BEST TABLECLOTH","IN THE VALLEY."],(150,88,175,88),(240,232))
p4=sky+hills(300)+grass(40,310,2)+mapsheet(250,330,1.3)+roast(250,318,.9)+caveman(262,316,.7,look="s",mood="happy")+alien(70,305,1.0,True,"flat")+alien(150,306,.8,False,"worried",arms="up")
p4+=bubble(8,34,160,52,["IT'S A PLACEMAT."],(50,86,75,86),(68,190))
p4+=bubble(170,98,150,52,["AT LEAST IT'S","NEAR FOOD."],(190,150,210,150),(162,210))
open("today.svg","w").write(strip([panel(0,p1,"EARTH — 15,000 B.C."),panel(1,p2),panel(2,p3),panel(3,p4)]))
