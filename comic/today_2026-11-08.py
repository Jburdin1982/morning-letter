from comiclib import *
sky='<rect width="330" height="355" fill="url(#h6)"/>'
def dial(x,y,s=1):
    return f'<g transform="translate({x},{y}) scale({s})" {ST}><ellipse cx="0" cy="0" rx="46" ry="12" fill="url(#h2)"/><path d="M0,0 L22,-34 L30,-4 Z" fill="url(#h3)"/><path d="M-30,-2 h60" fill="none"/></g>'
p1=sky+sun(270,70)+mountains(255)+hills(285)+grass(20,300,2)+dial(165,318,1.3)+alien(60,285,.9,True,"flat",arms="point")+alien(115,288,.8,False,"happy")+caveman(268,320,.7,look="s")
p1+=bubble(8,34,250,56,["TODAY'S GIFT: THE SUNDIAL.","IT TELLS THE TIME."],(70,90,92,90),(76,128))
p2=sky+sun(270,60)+hills(290)+grass(300,300,2)+dial(150,316,1.4)+caveman(240,316,.9,look="up",mood="happy")
p2+=f'<g {ST}><path d="M130,292 q18,-10,36,0 q-6,10,-18,10 Z" fill="{PAPER}"/></g>'+f'<text x="282" y="214" class="s" style="font-size:30px">?</text>'
p2+=bubble(110,40,190,50,["LUNCH SHELF!"],(230,86,252,86),(252,196))
p3=f'<rect width="330" height="355" fill="#e9dfc2"/>'+cloud(80,80,2.2)+cloud(230,60,1.8)+hills(290)+dial(150,316,1.4)+caveman(240,316,.9,look="s",mood="shocked")
p3+=bubble(150,120,170,52,["WHERE DID","TIME GO?"],(250,172,268,172),(258,236))
p4=sky+hills(300)+grass(40,310,2)+dial(150,320,1.2)+alien(70,305,1.0,True,"flat")+alien(240,306,.9,False,"worried",arms="up")+timedial(150,250,.8)
p4+=bubble(8,34,170,52,["IT ONLY WORKS","WHEN IT'S SUNNY."],(60,86,80,86),(70,150))
p4+=bubble(172,98,150,40,["SO, HALF THE DAY?"],(240,136,256,136),(244,188))
p4+=f'<text x="150" y="222" text-anchor="middle" class="big" style="font-size:20px">REWIND.</text>'
open("today.svg","w").write(strip([panel(0,p1,"EARTH — 30,000 B.C."),panel(1,p2),panel(2,p3),panel(3,p4)]))
