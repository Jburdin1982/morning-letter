from comiclib import *
sky='<rect width="330" height="355" fill="url(#h6)"/>'
night='<rect width="330" height="355" fill="url(#h4)" opacity=".55"/>'
def pot(x,y,s=1):
    return (f'<g transform="translate({x},{y}) scale({s})" {ST}><path d="M-12,-34 h24 q-2,6,4,10 q16,10,14,28 q-2,22,-28,24 q-26,-2,-28,-24 q-2,-18,14,-28 q6,-4,0,-10 Z" fill="{PAPER}"/>'
            f'<path d="M-20,-4 q20,8,40,0" fill="none" stroke-width="1.4"/><path d="M-22,6 q22,8,44,0" fill="none" stroke-width="1.4"/><path d="M-20,12 q20,10,40,0 l-2,8 q-18,6,-36,0 Z" fill="url(#h2)" stroke-width="1"/></g>')
def note(x,y,s=1): return f'<g transform="translate({x},{y}) scale({s})" {ST}><ellipse cx="0" cy="0" rx="6" ry="4.5" fill="{INK}" transform="rotate(-20)"/><path d="M5,-2 v-24 q8,4,10,12" fill="none" stroke-width="2"/></g>'
def qmark(x,y): return f'<text x="{x}" y="{y}" text-anchor="middle" class="s" style="font-size:38px">?</text>'
def boom(x,y,t="BOOM!",sz=24): return f'<text x="{x}" y="{y}" text-anchor="middle" class="big" style="font-size:{sz}px">{t}</text>'
def snow(n,seed,y0=40,y1=330):
    import random as R; r=R.Random(seed)
    return "".join(f'<circle cx="{r.randint(6,324)}" cy="{r.randint(y0,y1)}" r="{r.choice([1.6,2,2.6])}" fill="{PAPER}" stroke="{INK}" stroke-width="1"/>' for _ in range(n))
# P1: gift
p1=sky+hills(292)+grass(270,312,3)+alien(70,300,.9,True,"flat",arms="down")+alien(185,302,.72,False,"happy",arms="up")+pot(258,272,.95)
p1+=bubble(10,30,310,76,["GIFT: THE CLAY POT.","STORE GRAIN FOR WINTER."],(160,104,182,104),(186,206))
# P2: Grog thumps it
p2=sky+hills(296)+caveman(170,326,.95,look="s",mood="confused")+pot(102,290,1.1)+qmark(178,182)+boom(92,236,"BOOM!",22)
p2+=bubble(14,30,300,62,["POT GO BOOM!"],(150,90,172,90),(170,150))
# P3: night drumming
p3=night+moon(282,70,16)+stars(10,4,40,120)+hills(300)+caveman(220,330,.8,look="s",mood="happy")+pot(170,318,.9)
p3+=note(262,200)+note(292,150,.8)+note(240,240,.8)
p3+=alien(46,332,.62,True,"flat")+alien(104,334,.5,False,"happy")
p3+=bubble(4,34,170,56,["IT'S FOR","GRAIN."],(36,86,56,86),(46,226))
p3+=bubble(96,104,160,58,["BUT LISTEN TO","THAT BEAT!"],(140,158,160,158),(108,264))
# P4: winter
cold='<rect width="330" height="355" fill="url(#h4)" opacity=".3"/>'
p4=cold+hills(316)+snow(40,7)+caveman(220,330,.85,look="s",mood="tired")+pot(160,320,.9)+note(268,200,.8)
p4+=alien(50,332,.62,True,"flat")+alien(108,334,.5,False,"worried")
p4+=bubble(4,34,170,56,["GRAIN STORED:","ZERO."],(60,88,80,88),(50,226))
p4+=bubble(150,96,176,74,["GROG NOT EAT.","GROG DANCE TO","STAY WARM!"],(220,168,240,168),(226,206))
open("today.svg","w").write(strip([panel(0,p1,"EARTH — 7,000 B.C."),panel(1,p2),panel(2,p3,"THAT NIGHT"),panel(3,p4,"WINTER")]))
