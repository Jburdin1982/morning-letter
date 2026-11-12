from comiclib import *
sky='<rect width="330" height="355" fill="url(#h6)"/>'
def fire(x,y,s=1,lit=True):
    logs=f'<path d="M-26,0 L22,-10 M-22,-10 L26,0" fill="none" stroke-width="6"/><path d="M-26,0 L22,-10 M-22,-10 L26,0" fill="none" stroke="{PAPER}" stroke-width="2"/>'
    fl=(f'<path d="M-16,-8 q-6,-22,6,-34 q-2,12,8,16 q2,-18,12,-26 q4,20,4,28 q4,-6,4,-12 q10,14,-2,28 Z" fill="url(#h2)"/>'
        f'<path d="M-6,-8 q-2,-12,6,-18 q6,8,4,18 Z" fill="{PAPER}"/>') if lit else '<path d="M-14,-6 q14,-10,28,0 Z" fill="url(#h4)"/>'
    return f'<g transform="translate({x},{y}) scale({s})" {ST}>{fl}{logs}</g>'
def qmark(x,y): return f'<text x="{x}" y="{y}" text-anchor="middle" class="s" style="font-size:38px">?</text>'
def smoke_word(x,y,word,s=1):
    puffs="".join(f'<circle cx="{x+i*58*s}" cy="{y}" r="{30*s}" fill="{PAPER}" {ST}/>' for i in range(len(word)))
    txt="".join(f'<text x="{x+i*58*s}" y="{y+12*s}" text-anchor="middle" class="s" style="font-size:{34*s}px">{c}</text>' for i,c in enumerate(word))
    return puffs+txt
def wisp(x,y0,y1):
    return f'<path d="M{x},{y0} q-12,-20,0,-40 q12,-20,0,-40 q-10,-18,0,-{(y0-y1)-80}" fill="none" stroke="{INK}" stroke-width="2.2" stroke-dasharray="6 5"/>'
def shiver(x,y): return "".join(f'<path d="M{x+dx},{y} q-4,-6,0,-12 q4,-6,0,-12" fill="none" stroke="{INK}" stroke-width="1.8"/>' for dx in (-46,-38,38,46))
p1=sky+hills(292)+grass(30,310,3)+alien(70,300,.9,True,"flat",arms="point")+alien(140,302,.72,False,"happy")+fire(260,318,.9)
p1+=bubble(8,34,300,74,["FROST TONIGHT. TODAY'S GIFT:","FIRE. FOR KEEPING","WARM."],(70,104,94,104),(76,186))
p2=sky+hills(296)+grass(250,312,3)+caveman(130,326,.95,look="s",mood="confused")+fire(230,318,1.2)+qmark(132,196)
p3=sky+hills(300)+smoke_word(50,92,"GROG",1.0)+wisp(232,292,112)+fire(230,316,1.0)+caveman(110,330,.85,look="up",mood="happy")
p3+=bubble(8,150,170,48,["GROG NAME","IN SKY!"],(92,196,112,196),(108,226))
p4=('<rect width="330" height="355" fill="'+INK+'" opacity=".12"/>'+stars(26,12,34,170)+moon(282,70)+hills(300)
    +fire(285,322,.8,lit=False)+caveman(185,330,.85,look="s",mood="shocked")+shiver(185,240)+alien(60,316,.85,True,"tired"))
p4+=bubble(6,38,210,62,["AT LEAST EVERYONE","KNOWS WHO'S COLD."],(70,98,94,98),(68,172))
open("today.svg","w").write(strip([panel(0,p1,"EARTH — 30,000 B.C."),panel(1,p2),panel(2,p3),panel(3,p4,"THAT NIGHT")]))
