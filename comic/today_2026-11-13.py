from comiclib import *
sky='<rect width="330" height="355" fill="url(#h6)"/>'
def mirror(x,y,s=1,flash=False):
    g=f'<g transform="translate({x},{y}) scale({s})" {ST}><ellipse cx="0" cy="0" rx="22" ry="30" fill="url(#h2)"/><ellipse cx="0" cy="0" rx="15" ry="22" fill="{PAPER}"/><path d="M-7,-12 l10,-6 M-9,-4 l14,-8" fill="none" stroke-width="1.6"/><path d="M0,30 v22" fill="none" stroke-width="5"/></g>'
    if flash: g+=speedlines(x,y-40,5,18,90)
    return g
def qmark(x,y): return f'<text x="{x}" y="{y}" text-anchor="middle" class="s" style="font-size:38px">?</text>'
def hearts(x,y):
    return "".join(f'<path transform="translate({x+dx},{y+dy}) scale(.8)" d="M0,6 l-9,-9 a5,5 0 0 1 9,-5 a5,5 0 0 1 9,5 Z" fill="{INK}"/>' for dx,dy in ((0,0),(22,-16),(-18,-20)))
p1=sky+hills(292)+grass(30,310,3)+alien(70,300,.9,True,"flat",arms="point")+alien(170,302,.72,False,"happy")+mirror(210,250,.9)
p1+=bubble(8,30,312,74,["GIFT: THE MIRROR. FOR FLASHING","SIGNALS TO DISTANT TRIBES."],(70,100,94,100),(76,186))
p2=sky+hills(296)+grass(30,316,3)+rock(250,322,1.1)+mirror(250,268,.9)+caveman(120,326,.95,look="s",mood="confused")+qmark(122,190)
p3=sky+hills(300)+mirror(240,262,1.15)+caveman(120,330,.9,look="s",mood="happy")+hearts(185,170)
p3+=bubble(10,26,250,62,["HANDSOME MAN","LIVE IN SHINY ROCK!"],(120,86,144,86),(130,206))
p4=('<rect width="330" height="355" fill="'+INK+'" opacity=".12"/>'+stars(26,13,34,150)+moon(290,62)+hills(300)
    +mirror(250,268,1.0)+caveman(150,330,.85,look="s",mood="happy")+alien(48,316,.62,False,"happy"))
p4+=bubble(6,26,250,46,["NIGHT NIGHT, HANDSOME MAN."],(150,70,170,70),(160,212))
p4+=bubble(6,92,150,58,["HE DID FIND","SOMEONE."],(40,148,58,148),(50,232))
open("today.svg","w").write(strip([panel(0,p1,"EARTH — 20,000 B.C."),panel(1,p2),panel(2,p3,"NOON"),panel(3,p4,"MIDNIGHT")]))
