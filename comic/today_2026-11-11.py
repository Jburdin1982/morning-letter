from comiclib import *
import random
sky='<rect width="330" height="355" fill="url(#h6)"/>'
def tablet(x,y,s=1,rot=0,label=""):
    cells="".join(f'<rect x="{-30+c*15}" y="{-14+r*12}" width="15" height="12" fill="none" stroke-width="1.4"/>' for r in range(3) for c in range(4))
    lab=f'<text x="0" y="-19" text-anchor="middle" class="s" style="font-size:11px">{label}</text>' if label else ''
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})" {ST}>'
            f'<rect x="-36" y="-32" width="72" height="62" rx="6" fill="#f7f0dd"/>{cells}</g>'
            + (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})">{lab}</g>' if label else ''))
def gtab(x,y,s=1):
    cells="".join(f'<rect x="{-30+c*15}" y="{-24+r*16}" width="15" height="16" fill="none" stroke-width="1.4"/>' for r in range(3) for c in range(4))
    txt="".join(f'<text x="{-22.5+c*15}" y="{-12+r*16}" text-anchor="middle" style="font:700 4.4px serif;fill:{INK}">GROG</text>' for r in range(3) for c in range(4))
    return f'<g transform="translate({x},{y}) scale({s})" {ST}><rect x="-36" y="-30" width="72" height="62" rx="6" fill="#f7f0dd"/>{cells}</g><g transform="translate({x},{y}) scale({s})">{txt}</g>' 
def snow(seed,n=40):
    r=random.Random(seed)
    return "".join(f'<circle cx="{r.randint(6,324)}" cy="{r.randint(30,330)}" r="{r.choice([2,2.5,3])}" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>' for _ in range(n))
p1=sky+sun(290,150)+hills(290)+grass(20,305,2)+tablet(200,300,.8)+alien(60,290,.9,True,"flat",arms="point")+alien(122,292,.75,False,"happy")+caveman(275,322,.7,look="s",mood="happy")
p1+=bubble(6,32,280,74,["TODAY'S GIFT: A CALENDAR.","SO HE KNOWS WHEN","WINTER IS COMING."],(55,102,80,102),(66,184))
p2=sky+sun(40,70)+hills(292)+grass(240,312,3)+caveman(120,322,.95,look="s",mood="happy")+gtab(235,232,1.35)
p2+=bubble(60,34,210,56,["EVERY DAY","GROG DAY!"],(130,88,152,88),(128,200))
p3=sky+hills(296)+rock(260,300,1.4)+alien(85,300,1.0,True,"tired")+alien(185,302,.85,False,"happy",arms="down")+timedial(222,262,0.9)
p3+=bubble(6,36,140,50,["REWIND."],(70,86,92,86),(86,150))
p3+=bubble(186,60,130,46,["ON IT!"],(220,104,240,104),(200,148))
p4='<rect width="330" height="355" fill="url(#h6)"/>'+'<path d="M0,290 q80,-24,165,-6 t165,-4 V360 H0 Z" fill="'+PAPER+'" '+ST+'/>'+snow(11)+caveman(210,326,.95,look="s",mood="shocked")+tablet(206,192,0.95,-8)+alien(62,312,.85,True,"worried")
p4+=bubble(6,34,170,52,["THAT WAS","FORWARD."],(60,84,82,84),(66,180))
p4+=bubble(176,72,148,50,["GROG DAY","CHILLY!"],(250,120,268,120),(240,150))
open("today.svg","w").write(strip([panel(0,p1,"EARTH — 9,000 B.C."),panel(1,p2),panel(2,p3),panel(3,p4,"A LITTLE LATER")]))
