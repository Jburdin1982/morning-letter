from comiclib import *
sky='<rect width="330" height="355" fill="url(#h6)"/>'
ground=lambda y: f'<path d="M0,{y} H330 V355 H0 Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.4"/>'
def snow(seed,n=22,y1=290):
    r=random.Random(seed)
    return "".join(f'<g stroke="{INK}" stroke-width="1.3" stroke-linecap="round" transform="translate({r.randint(10,320)},{r.randint(34,y1)})"><path d="M-4,0 h8 M0,-4 v8 M-3,-3 l6,6 M3,-3 l-6,6"/></g>' for _ in range(n))
def mitten(x,y,s=1,rot=0):
    return (f'<g transform="translate({x},{y}) rotate({rot}) scale({s})" {ST}>'
            f'<path d="M-9,10 v-18 q0,-12,10,-12 q10,0,10,12 v18 Z" fill="url(#h2)"/>'
            f'<path d="M-9,-2 q-9,-2,-9,-10 q0,-5,5,-4 q3,2,4,6" fill="url(#h2)"/>'
            f'<path d="M-10,10 h22 v5 h-22 Z" fill="{PAPER}" stroke-width="2"/></g>')
def footmittens(x,y,s=1):
    # mittens worn over Grog's feet (feet at x-12 and x+12, ground y)
    def one(fx,d):
        return (f'<g transform="translate({fx},{y}) scale({d*s},{s})" {ST}>'
                f'<path d="M-6,-6 h14 q14,0,14,9 q0,9,-14,9 h-14 Z" fill="url(#h2)"/>'
                f'<path d="M4,-6 q2,-9,8,-8 q4,1,2,8" fill="url(#h2)" stroke-width="2"/>'
                f'<path d="M-10,-7 h6 v20 h-6 Z" fill="{PAPER}" stroke-width="2"/></g>')
    return one(x+6*s,1)+one(x-6*s,-1)
# P1: the gift
p1=sky+snow(3,16,200)+ground(300)+grass(250,300,3)+alien(70,300,.9,True,"flat")+alien(196,302,.72,False,"happy",arms="up")
p1+=mitten(158,204,1.0,-15)+mitten(236,204,1.0,15)
p1+=bubble(10,36,270,70,["GIFT: MITTENS.","WARM HANDS ALL WINTER."],(80,102,100,102),(76,182))
# P2: Grog finds them
p2=sky+snow(5,18,240)+ground(300)+rock(276,302,1.2)+caveman(150,300,1.0,look="s",mood="confused")+mitten(66,294,1.0,0)+mitten(92,294,1.0,10)
p2+=f'<text x="150" y="168" class="big" text-anchor="middle" style="font-size:40px">?</text>'
# P3: worn on the feet
p3=sky+snow(9,24,280)+ground(300)+caveman(120,296,1.05,look="s",mood="happy")+footmittens(120,296,1.05)
p3+=bubble(150,60,170,62,["GROG FEET","TOASTY!"],(196,118,214,118),(152,190))
# P4: punchline
p4=sky+snow(12,24,280)+ground(300)+alien(52,300,.85,True,"flat")+alien(150,302,.68,False,"worried")+caveman(262,300,.85,look="s",mood="shocked")+footmittens(262,300,.85)
p4+=f'<g stroke="{INK}" stroke-width="2" fill="none" stroke-linecap="round"><path d="M222,262 l-8,-4 M222,270 l-9,1 M306,250 l8,-4 M306,258 l9,1"/></g>'
p4+=bubble(4,34,186,56,["HIS HANDS","ARE FREEZING."],(46,88,64,88),(54,170))
p4+=bubble(108,104,196,50,["NEXT TIME...","FOUR MITTENS."],(150,152,170,152),(152,206))
open("today.svg","w").write(strip([panel(0,p1,"EARTH, 30,000 B.C."),panel(1,p2,"NEXT MORNING"),panel(2,p3,"AN HOUR LATER"),panel(3,p4,"THAT AFTERNOON")]))
