from comiclib import *
sky='<rect width="330" height="355" fill="url(#h6)"/>'
def ladder(x,y,h,ang=0,s=1):
    rungs="".join(f'<line x1="-14" y1="{-i}" x2="14" y2="{-i}"/>' for i in range(18,int(h),22))
    return f'<g transform="translate({x},{y}) rotate({ang}) scale({s})" {ST} fill="none"><line x1="-14" y1="0" x2="-14" y2="{-h}"/><line x1="14" y1="0" x2="14" y2="{-h}"/>{rungs}</g>'
def qmark(x,y): return f'<text x="{x}" y="{y}" text-anchor="middle" class="s" style="font-size:38px">?</text>'
p1=sky+hills(292)+grass(250,312,3)+alien(70,300,.9,True,"flat",arms="point")+alien(170,302,.72,False,"happy",arms="up")+ladder(250,300,150,8,1)
p1+=bubble(8,30,312,74,["GIFT: THE LADDER.","REACH HIGHER. SEE FARTHER."],(70,100,94,100),(76,186))
p2=sky+hills(296)+ladder(220,330,170,-6,1)+caveman(120,326,.95,look="s",mood="confused")+qmark(122,186)
p3=sky+hills(310)+tree(200,340,1.55)+ladder(120,340,190,-24,1)+caveman(205,200,.6,look="s",mood="happy")+speedlines(50,170,3,16,180)
p3+=bubble(8,30,250,62,["GROG KING","OF TREE!"],(130,88,150,88),(196,128))
night='<rect width="330" height="355" fill="url(#h4)" opacity=".55"/>'+stars(14,7,30,110)+moon(290,62,16)
p4=night+hills(310)+tree(250,340,1.55)+caveman(255,200,.6,look="s",mood="confused")+ladder(130,340,190,90,.85)
p4+=alien(42,330,.7,True,"flat")+alien(108,332,.58,False,"worried")
p4+=bubble(70,150,150,44,["SHOULD WE...?"],(130,192,146,192),(112,262))
p4+=bubble(4,78,124,44,["NO CONTACT."],(40,120,56,120),(44,228))
p4+=bubble(176,36,140,62,["KING...","FOREVER."],(236,96,252,96),(256,120))
open("today.svg","w").write(strip([panel(0,p1,"EARTH — 12,000 B.C."),panel(1,p2),panel(2,p3),panel(3,p4,"THAT NIGHT")]))
