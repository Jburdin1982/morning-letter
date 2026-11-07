from comiclib import *
sky=f'<rect width="330" height="355" fill="url(#h6)"/>'
p1=sky+stars(14,3)+moon(280,70)+mountains(255)+hills(285)+grass(20,300,2)+rock(300,320)+alien(70,285,.9,True,"flat")+alien(150,288,.9,False,"happy")+caveman(262,318,.7,look="s")
p1+=bubble(10,36,230,56,["TODAY'S GIFT: THE LEVER.","A SIMPLE MACHINE."],(78,92,98,92),(88,128))
p2=mountains(250)+hills(285)+grass(300,300,2)+f'<path d="M70,300 L260,300" stroke="{INK}" stroke-width="3"/>'+f'<g {ST}><path d="M150,300 L170,268 L190,300 Z" fill="url(#h2)"/><path d="M62,266 L270,300 L272,290 L66,254 Z" fill="url(#h3)" transform="rotate(-1 160 280)"/></g>'+alien(60,255,.8,False,"happy",arms="point")+caveman(240,300,.75,look="s",mood="confused")+tree(305,330,.6)
p2+=bubble(12,36,214,52,["PLEASE USE RESPONSIBLY."],(60,88,80,88),(70,124))
p2+=f'<text x="262" y="178" class="s" style="font-size:30px">?</text>'
p3=sky.replace("url(#h6)","#fbf5e3")+f'<path d="M0,250 q80,20,330,0" stroke="none"/>'+mountains(260)+hills(290)+f'<g {ST}><path d="M130,300 L150,268 L170,300 Z" fill="url(#h2)"/><path d="M40,262 L222,262" fill="none"/></g>'
p3+=f'<g {ST}><path d="M40,236 L222,300 L226,290 L44,226 Z" fill="url(#h3)"/></g>'+rock(226,226,1.7)+speedlines(226,246,4,18,90)
p3+=caveman(200,170,.8,look="up",mood="shocked",rot=-35)+speedlines(205,215,5,26,90)+f'<text x="92" y="150" class="big" text-anchor="middle" transform="rotate(-10 92 150)">AIEEEE!</text>'
p4=sky+stars(10,9)+hills(300)+tree(268,335,1.0)+f'<g transform="translate(268,160) rotate(180)">{caveman(0,0,.6,look="s",mood="shocked")}</g>'+alien(78,300,1.0,True,"tired")+alien(160,302,.9,False,"worried",arms="up")+timedial(300,318,.55)
p4+=bubble(10,34,176,50,["HE HAS INVENTED","FLIGHT."],(66,82,90,82),(78,160))
p4+=bubble(92,100,196,40,["THE LANDING NEEDS WORK."],(150,138,170,138),(160,200)).replace('class="s"','class="s" style="font-size:11px"')
open("sample2.svg","w").write(strip([panel(0,p1,"EARTH — 40,000 B.C."),panel(1,p2),panel(2,p3),panel(3,p4)]))
