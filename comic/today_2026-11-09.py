from comiclib import *
sky='<rect width="330" height="355" fill="url(#h6)"/>'
def shovel(x,y,s=1,rot=0):
    return f'<g transform="translate({x},{y}) rotate({rot}) scale({s})" {ST}><path d="M0,-70 L0,0" fill="none"/><path d="M-6,-72 h12" fill="none"/><path d="M-12,0 q12,26,24,0 Z" fill="url(#h3)"/></g>'
def pit(x,y,w=120):
    return f'<g {ST}><ellipse cx="{x}" cy="{y}" rx="{w/2}" ry="16" fill="url(#h2)"/></g>'
p1=sky+sun(270,70)+mountains(255)+hills(285)+grass(20,300,2)+shovel(165,320,1.3)+alien(60,285,.9,True,"flat",arms="point")+alien(115,288,.8,False,"happy")+caveman(268,320,.7,look="s")
p1+=bubble(8,34,250,56,["TODAY'S GIFT: THE SHOVEL.","IT MOVES DIRT."],(70,90,92,90),(76,128))
p2=sky+sun(270,60)+hills(290)+pit(120,322,110)+caveman(230,316,.9,look="up",mood="happy")+shovel(180,322,1.2,20)
p2+=f'<text x="285" y="214" class="s" style="font-size:30px">?</text>'
p2+=bubble(20,40,190,50,["A STICK WITH A SPOON!"],(150,90,175,90),(218,222))
p3=sky+hills(300)+pit(165,322,200)+caveman(165,322,.9,look="s",mood="happy")+shovel(235,322,1.3,-10)
p3+=bubble(8,40,170,52,["BEST SEAT","IN THE VALLEY."],(120,92,150,92),(155,230))
p4=sky+hills(300)+grass(40,310,2)+pit(250,326,130)+caveman(250,324,.7,look="s",mood="happy")+alien(70,305,1.0,True,"flat")+alien(150,306,.8,False,"worried",arms="up")
p4+=bubble(8,34,150,52,["USE","RESPONSIBLY."],(110,86,135,86),(148,205))
p4+=bubble(170,98,150,40,["HE WON'T."],(180,138,200,138),(88,172))
open("today.svg","w").write(strip([panel(0,p1,"EARTH — 20,000 B.C."),panel(1,p2),panel(2,p3),panel(3,p4)]))
