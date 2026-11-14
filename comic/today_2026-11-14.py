from comiclib import *
sky='<rect width="330" height="355" fill="url(#h6)"/>'
def soap(x,y,s=1): return f'<g transform="translate({x},{y}) scale({s})" {ST}><rect x="-16" y="-10" width="32" height="20" rx="7" fill="{PAPER}"/><path d="M-8,-3 h16 M-6,3 h12" stroke-width="1.4" fill="none"/></g>'
def bubbles(pts): return "".join(f'<g {ST}><circle cx="{x}" cy="{y}" r="{r}" fill="none" stroke-width="2"/><path d="M{x-r*.45},{y-r*.2} a{r*.5},{r*.5} 0 0 1 {r*.35},{-r*.35}" fill="none" stroke-width="1.5"/></g>' for x,y,r in pts)
def puddle(x,y,w=70): return f'<g {ST}><ellipse cx="{x}" cy="{y}" rx="{w/2}" ry="9" fill="url(#h4)"/></g>'
def mud(x,y): return "".join(f'<circle cx="{x+dx}" cy="{y+dy}" r="3.2" fill="{INK}"/>' for dx,dy in ((0,0),(9,6),(-7,9),(4,-8),(-10,-3)))
def qmark(x,y): return f'<text x="{x}" y="{y}" text-anchor="middle" class="s" style="font-size:38px">?</text>'
p1=sky+hills(292)+grass(240,312,3)+alien(70,300,.9,True,"flat",arms="point")+alien(170,302,.72,False,"happy",arms="up")+soap(230,286,1.1)+speedlines(230,262,3,14,90)
p1+=bubble(8,30,312,74,["GIFT: SOAP. FOR WASHING.","THEY REALLY NEED IT."],(70,100,94,100),(76,186))
p2=sky+hills(296)+puddle(240,326,90)+caveman(130,326,.95,look="s",mood="confused")+mud(118,268)+soap(200,250,.9)+qmark(132,186)
p3=sky+hills(300)+puddle(240,330,90)+caveman(110,330,.9,look="up",mood="happy")+bubbles(((190,200,14),(230,160,20),(270,120,12),(215,95,9),(290,200,16)))
p3+=bubble(8,30,230,62,["GROG MAKE","TINY MOONS!"],(90,88,112,88),(110,206))
p4=(sky+hills(300)+bubbles(((290,120,10),(255,160,14),(305,60,8),(300,190,9)))
    +caveman(240,330,.8,look="up",mood="happy",rot=-8)+mud(232,282)+alien(50,316,.75,True,"tired")+alien(120,318,.6,False,"worried"))
p4+=bubble(70,128,160,46,["HE'S STILL MUDDY."],(118,172,134,172),(122,240))
p4+=bubble(4,30,200,68,["HYGIENE: ZERO.","JOY: OFF THE CHARTS."],(42,96,62,96),(50,220))
open("today.svg","w").write(strip([panel(0,p1,"EARTH — 30,000 B.C."),panel(1,p2),panel(2,p3),panel(3,p4,"ALL AFTERNOON")]))
