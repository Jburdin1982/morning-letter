"""Reusable drawing kit for 'Sorry, Earth'. Import: from comiclib import *"""
import random, math
INK="#3a2a14"; PAPER="#fbf5e3"; SEP="#8a6a35"
DEFS=f'''<pattern id="h1" width="5" height="5" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="5" stroke="{INK}" stroke-width="1"/></pattern>
<pattern id="h2" width="4" height="4" patternUnits="userSpaceOnUse" patternTransform="rotate(-45)"><line x1="0" y1="0" x2="0" y2="4" stroke="{INK}" stroke-width="1"/></pattern>
<pattern id="h3" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="{INK}" stroke-width="1.1"/></pattern>
<pattern id="h4" width="3" height="3" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="3" stroke="{INK}" stroke-width="1"/></pattern>
<pattern id="h5" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(60)"><line x1="0" y1="0" x2="0" y2="7" stroke="{INK}" stroke-width="1"/></pattern>
<pattern id="h6" width="9" height="9" patternUnits="userSpaceOnUse"><line x1="0" y1="0" x2="9" y2="0" stroke="{INK}" stroke-width=".7"/></pattern>
<pattern id="x1" width="6" height="6" patternUnits="userSpaceOnUse"><path d="M0,0 L6,6 M6,0 L0,6" stroke="{INK}" stroke-width=".8"/></pattern>
<style>.s{{font:700 12.5px 'Latin Modern Roman','CMU Serif',Georgia,serif;fill:{INK}}}.c{{font:700 13px 'Latin Modern Roman','CMU Serif',Georgia,serif;fill:{PAPER};letter-spacing:2px}}.big{{font:700 22px 'Latin Modern Roman','CMU Serif',Georgia,serif;fill:{INK}}}</style>'''
ST=f'stroke="{INK}" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"'
def bubble(x,y,w,h,lines,tail,tip):
    """tail=(x1,y1,x2,y2) base points near the bubble's lower edge, tip=(x,y)."""
    t="".join(f'<text x="{x+w/2}" y="{y+h/2-(len(lines)-1)*8+5+i*16}" text-anchor="middle" class="s">{l}</text>' for i,l in enumerate(lines))
    return (f'<g><path d="M{tail[0]},{tail[1]} L{tip[0]},{tip[1]} L{tail[2]},{tail[3]} Z" fill="{PAPER}" stroke="{INK}" stroke-width="2.2"/>'
            f'<ellipse cx="{x+w/2}" cy="{y+h/2}" rx="{w/2}" ry="{h/2}" fill="{PAPER}" stroke="{INK}" stroke-width="2.2"/>'
            f'<path d="M{tail[0]+1},{tail[1]-2} L{tail[2]-1},{tail[3]-2}" stroke="{PAPER}" stroke-width="4"/>{t}</g>')
def stars(n,seed,y0=34,y1=150):
    r=random.Random(seed); return "".join(f'<circle cx="{r.randint(8,322)}" cy="{r.randint(y0,y1)}" r="{r.choice([1,1.2,1.8,2.2])}" fill="{INK}"/>' for _ in range(n))
def moon(x,y,r=18): return f'<g {ST}><circle cx="{x}" cy="{y}" r="{r}" fill="{PAPER}"/><circle cx="{x-5}" cy="{y-4}" r="{r*.22:.1f}" fill="url(#h1)"/><circle cx="{x+6}" cy="{y+6}" r="{r*.15:.1f}" fill="url(#h1)"/></g>'
def sun(x,y,r=20):
    rays="".join(f'<line x1="{x+math.cos(a)*(r+4):.1f}" y1="{y+math.sin(a)*(r+4):.1f}" x2="{x+math.cos(a)*(r+13):.1f}" y2="{y+math.sin(a)*(r+13):.1f}"/>' for a in [i*math.pi/6 for i in range(12)])
    return f'<g {ST}><circle cx="{x}" cy="{y}" r="{r}" fill="{PAPER}"/>{rays}</g>'
def cloud(x,y,s=1): return f'<g transform="translate({x},{y}) scale({s})" {ST}><path d="M0,0 q-4,-14,12,-14 q6,-14,24,-6 q18,-4,20,10 q12,2,8,10 Z" fill="{PAPER}"/><path d="M6,-2 h46" stroke="url(#h1)" stroke-width="4" fill="none"/></g>'
def mountains(y0,w=330):
    return (f'<path d="M0,{y0} L50,{y0-70} L85,{y0-34} L140,{y0-96} L190,{y0-40} L240,{y0-78} L290,{y0-30} L{w},{y0-52} V{y0+10} H0 Z" fill="url(#h4)" {ST} opacity=".9"/>'
            f'<path d="M140,{y0-96} l-14,22 l10,-6 l8,10 l8,-12 l8,8 z" fill="{PAPER}" {ST}/>')
def volcano(x,y0,s=1):
    return f'<g transform="translate({x},{y0}) scale({s})" {ST}><path d="M-70,0 L-18,-80 L18,-80 L70,0 Z" fill="url(#h3)"/><path d="M-18,-80 q18,-10,36,0" fill="{PAPER}"/><path d="M0,-86 q-14,-22,0,-36 q14,-14,-4,-34 M12,-90 q18,-18,6,-30" fill="none"/></g>'
def hills(y0,w=330,x0=0,pat="h5"):
    return f'<path d="M{x0},{y0} q60,-34,110,-6 t120,-4 t{w-230},10 V{y0+140} H{x0} Z" fill="url(#{pat})" {ST}/>'
def grass(x,y,n=3):
    return "".join(f'<path d="M{x+i*7},{y} q-3,-10,-6,-14 M{x+i*7},{y} q1,-12,2,-16 M{x+i*7},{y} q4,-8,8,-12" fill="none" stroke="{INK}" stroke-width="1.8" stroke-linecap="round"/>' for i in range(n))
def rock(x,y,s=1): return f'<g transform="translate({x},{y}) scale({s})" {ST}><path d="M-22,0 l4,-16 l14,-8 l16,6 l8,18 Z" fill="url(#h2)"/><path d="M-14,-12 l10,-2" fill="none" stroke-width="1.6"/></g>'
def tree(x,y,s=1): return f'<g transform="translate({x},{y}) scale({s})" {ST}><path d="M-9,0 q2,-50,-2,-80 h22 q-4,30,0,80 Z" fill="url(#h3)"/><circle cx="0" cy="-100" r="38" fill="{PAPER}"/><path d="M-30,-92 q10,18,30,16 q22,2,32,-18" fill="url(#h2)" stroke="none" opacity=".6"/><circle cx="-24" cy="-118" r="22" fill="{PAPER}"/><circle cx="26" cy="-116" r="20" fill="{PAPER}"/><path d="M-4,-4 l-14,10 M6,-4 l14,10" fill="none"/></g>'
def saucer(x,y,s=1,beam=False):
    b=f'<path d="M-24,12 L-52,120 L52,120 L24,12 Z" fill="url(#h6)" stroke="none" opacity=".8"/>' if beam else ''
    return f'<g transform="translate({x},{y}) scale({s})" {ST}>{b}<ellipse cx="0" cy="0" rx="56" ry="14" fill="{PAPER}"/><path d="M-56,0 q56,22,112,0 q-56,10,-112,0 Z" fill="url(#h1)"/><path d="M-26,-6 q0,-34,26,-34 q26,0,26,34 Z" fill="{PAPER}"/><path d="M-14,-12 q2,-18,14,-20" fill="none" stroke-width="1.6"/><circle cx="-36" cy="2" r="2.5" fill="{INK}"/><circle cx="0" cy="6" r="2.5" fill="{INK}"/><circle cx="36" cy="2" r="2.5" fill="{INK}"/></g>'
def alien(x,y,s=1,tall=True,mood="flat",arms="down",sash=None):
    """Feet at (x,y). Glim = tall=True (sash), Bonk = tall=False. mood: flat|happy|worried|shocked|tired. arms: down|up|point"""
    bh=76 if tall else 52
    g=f'<g transform="translate({x},{y}) scale({s})" {ST}>'
    g+=f'<path d="M-9,0 l-4,12 h12 M9,0 l4,12 h-12" fill="{PAPER}" stroke-width="2"/>'
    g+=f'<path d="M-15,-6 L-10,-{bh} Q0,-{bh+6},10,-{bh} L15,-6 Z" fill="url(#h1)"/><path d="M-10,-{bh-8} h20" stroke-width="1.6" fill="none"/>'
    if tall: g+=f'<path d="M-12,-{bh-10} L12,-6" stroke="{PAPER}" stroke-width="7"/><path d="M-12,-{bh-10} L12,-6" fill="none" stroke-width="2.4"/><circle cx="-2" cy="-{bh//2+8}" r="5" fill="{PAPER}"/><path d="M-2,-{bh//2+12} v8 M-5,-{bh//2+8} h6" stroke-width="1.4" fill="none"/>'
    else: g+=f'<path d="M-11,-{bh-12} h22" stroke-width="3" fill="none"/><circle cx="0" cy="-{bh-12}" r="3.5" fill="{PAPER}"/>'
    armtop=-bh+10
    if arms=="down": g+=f'<path d="M-12,{armtop} q-14,16,-14,34 M12,{armtop} q14,16,14,34" fill="none"/><path d="M-26,{armtop+34} l-3,5 M-26,{armtop+34} l0,6 M-26,{armtop+34} l3,4 M26,{armtop+34} l3,5 M26,{armtop+34} l0,6 M26,{armtop+34} l-3,4" fill="none" stroke-width="1.8"/>'
    elif arms=="up": g+=f'<path d="M-12,{armtop} q-22,-6,-22,-30 M12,{armtop} q22,-6,22,-30" fill="none"/><path d="M-34,{armtop-30} l-4,-5 M-34,{armtop-30} l0,-7 M-34,{armtop-30} l4,-5 M34,{armtop-30} l4,-5 M34,{armtop-30} l0,-7 M34,{armtop-30} l-4,-5" fill="none" stroke-width="1.8"/>'
    else: g+=f'<path d="M-12,{armtop} q-14,16,-14,34 M12,{armtop} q24,-4,38,-16" fill="none"/><path d="M50,{armtop-16} l5,-3 M50,{armtop-16} l6,1 M50,{armtop-16} l4,4" fill="none" stroke-width="1.8"/>'
    hy=-bh-28
    g+=f'<ellipse cx="0" cy="{hy}" rx="27" ry="30" fill="{PAPER}"/><path d="M-26,{hy+6} q4,24,26,26 q22,-2,26,-26 q-12,18,-26,18 q-14,0,-26,-18" fill="url(#h2)" stroke="none" opacity=".5"/>'
    g+=f'<path d="M-9,{hy-28} q-6,-18,-18,-20 M9,{hy-28} q6,-18,18,-20" fill="none"/><circle cx="-28" cy="{hy-49}" r="4.5" fill="{INK}"/><circle cx="28" cy="{hy-49}" r="4.5" fill="{INK}"/>'
    ew,eh=(8,11)
    if mood=="shocked": ew,eh=(10,13)
    g+=f'<ellipse cx="-12" cy="{hy+2}" rx="{ew}" ry="{eh}" fill="{INK}" transform="rotate(14 -12 {hy+2})"/><ellipse cx="12" cy="{hy+2}" rx="{ew}" ry="{eh}" fill="{INK}" transform="rotate(-14 12 {hy+2})"/>'
    g+=f'<circle cx="-14" cy="{hy-2}" r="2.6" fill="{PAPER}" stroke="none"/><circle cx="10" cy="{hy-2}" r="2.6" fill="{PAPER}" stroke="none"/>'
    if mood=="tired": g+=f'<path d="M-22,{hy-8} h20 M2,{hy-8} h20" stroke="{PAPER}" stroke-width="9"/><path d="M-22,{hy-8} h20 M2,{hy-8} h20" fill="none"/>'
    if mood=="happy": g+=f'<path d="M-8,{hy+19} q8,8,16,0" fill="none"/>'
    elif mood=="shocked": g+=f'<ellipse cx="0" cy="{hy+22}" rx="4" ry="5" fill="{INK}"/>'
    elif mood=="worried": g+=f'<path d="M-7,{hy+22} q7,-6,14,0" fill="none"/><path d="M-20,{hy-14} l10,3 M20,{hy-14} l-10,3" fill="none" stroke-width="1.8"/>'
    else: g+=f'<path d="M-6,{hy+20} h12" fill="none"/>'
    g+='</g>'; return g
def caveman(x,y,s=1,look="up",mood="happy",hat=None,rot=0,flip=False):
    sx=-s if flip else s
    g=f'<g transform="translate({x},{y}) rotate({rot}) scale({sx},{s})" {ST}>'
    g+=f'<path d="M-12,0 l-2,10 h14 M12,0 l2,10 h-14" fill="{PAPER}" stroke-width="2"/>'
    g+=f'<path d="M-24,-8 q-6,-50,24,-56 q30,6,24,56 Z" fill="url(#h3)"/><path d="M-24,-8 l3,-8 l6,6 l5,-8 l6,8 l5,-8 l6,8 l5,-6 l4,8" fill="{PAPER}" stroke-width="2"/>'
    g+=f'<path d="M-24,-60 q-16,16,-18,36" fill="none"/><path d="M24,-60 q14,10,16,28" fill="none"/>'
    g+=f'<path d="M38,-34 l8,-36 l10,2 l-6,36 z" fill="{PAPER}" transform="rotate(-6 40 -34)"/><circle cx="52" cy="-76" r="9" fill="url(#h2)"/>'
    g+=f'<circle cx="0" cy="-90" r="23" fill="{PAPER}"/><path d="M-23,-94 q0,-26,23,-24 q24,-2,23,24 q-6,-12,-23,-10 q-17,-2,-23,10" fill="{INK}"/><path d="M-22,-96 q-8,2,-6,14 q4,-6,6,-4" fill="{INK}" stroke-width="1.5"/>'
    g+=f'<path d="M-19,-84 q-3,26,19,30 q22,-4,19,-30 q-6,12,-19,12 q-13,0,-19,-12" fill="url(#h4)"/><path d="M-8,-70 q8,5,16,0" fill="{PAPER}" stroke-width="1.8"/>'
    dy={"up":-3,"s":0,"side":0}.get(look,0); dx={"side":3}.get(look,0)
    g+=f'<circle cx="{-8+dx}" cy="{-93+dy}" r="3.4" fill="{INK}" stroke="none"/><circle cx="{9+dx}" cy="{-93+dy}" r="3.4" fill="{INK}" stroke="none"/>'
    if mood=="happy": g+=f'<path d="M-13,-101 l8,2 M13,-101 l-8,2" fill="none" stroke-width="2"/><path d="M-9,-68 q9,10,18,0 z" fill="{INK}"/>'
    elif mood=="confused": g+=f'<path d="M-13,-98 l8,-3 M13,-102 l-8,3" fill="none" stroke-width="2"/>'
    elif mood=="shocked": g+=f'<path d="M-13,-103 l8,-2 M13,-103 l-8,-2" fill="none" stroke-width="2"/><ellipse cx="0" cy="-66" rx="5" ry="6" fill="{INK}"/>'
    if hat: g+=hat
    g+='</g>'; return g
def dino(x,y,s=1,flip=False,mood="calm"):
    sx=-s if flip else s
    g=f'<g transform="translate({x},{y}) scale({sx},{s})" {ST}>'
    g+=f'<path d="M-70,-10 q-34,4,-64,24 q30,-6,60,-4 Z" fill="url(#h3)"/>'  # tail
    g+=f'<ellipse cx="-14" cy="-42" rx="62" ry="38" fill="{PAPER}"/><path d="M-72,-34 q60,46,116,-4 q-10,34,-58,36 q-44,0,-58,-32" fill="url(#h1)" stroke="none" opacity=".7"/>'
    g+=f'<path d="M30,-62 q22,-6,28,-48 q4,-30,22,-30 q18,0,22,10 q6,10,-4,14 q-12,2,-14,-8 q-6,26,-10,44 q-8,32,-30,32 Z" fill="{PAPER}"/>'
    g+=f'<circle cx="86" cy="-132" r="2.8" fill="{INK}"/><path d="M88,-124 q6,2,10,0" fill="none" stroke-width="1.8"/>'
    if mood=="calm": g+=f'<path d="M80,-140 q6,-3,12,-1" fill="none" stroke-width="1.8"/>'
    g+=f'<path d="M-50,-8 v24 h20 v-26 M10,-6 v26 h20 v-28" fill="{PAPER}"/><path d="M-50,10 h20 M10,12 h20" stroke-width="1.6" fill="none"/>'
    g+='</g>'; return g
def wheel(cx,cy,r,rot=0):
    sp="".join(f'<line x1="0" y1="0" x2="{r*0.95:.1f}" y2="0" transform="rotate({a})"/>' for a in range(0,360,45))
    return f'<g transform="translate({cx},{cy}) rotate({rot})" {ST} fill="none"><circle r="{r}" fill="{PAPER}"/><circle r="{r-5}"/><circle r="5" fill="{INK}"/>{sp}</g>'
def timedial(x,y,s=1):
    return f'<g transform="translate({x},{y}) scale({s})" {ST}><rect x="-24" y="-14" width="48" height="28" rx="7" fill="{PAPER}"/><circle cx="0" cy="0" r="10" fill="url(#h1)"/><path d="M0,0 l6,-6 M-18,-6 h4 M-18,0 h4 M-18,6 h4" fill="none" stroke-width="1.8"/><path d="M14,-8 l6,0 l-3,-4 M14,8 l6,0 l-3,4" fill="none" stroke-width="1.4"/></g>'
def speedlines(x,y,n=5,l=26,ang=90):
    out=""
    for i in range(n):
        a=math.radians(ang+(i-n/2)*10); out+=f'<line x1="{x+math.cos(a)*14*i/2:.1f}" y1="{y+math.sin(a)*8:.1f}" x2="{x+math.cos(a)*14*i/2+math.cos(a)*l:.1f}" y2="{y+math.sin(a)*8+math.sin(a)*l:.1f}" stroke="{INK}" stroke-width="2" stroke-linecap="round"/>'
    return out
def panel(i,body,cap=""):
    x=20+i*345
    cp=f'<rect x="0" y="0" width="330" height="26" fill="{INK}"/><text x="165" y="18" text-anchor="middle" class="c">{cap}</text>' if cap else ''
    return f'<g transform="translate({x},20)"><clipPath id="c{i}"><rect width="330" height="355"/></clipPath><rect width="330" height="355" fill="{PAPER}"/><g clip-path="url(#c{i})">{body}</g>{cp}<rect width="330" height="355" fill="none" stroke="{INK}" stroke-width="4"/></g>'
def strip(panels,title_note="SORRY, EARTH"):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 440" width="1400" height="440"><defs>{DEFS}</defs>'
            f'<rect width="1400" height="440" fill="{PAPER}"/><rect x="6" y="6" width="1388" height="428" fill="none" stroke="{SEP}" stroke-width="2"/>'
            + "".join(panels) + f'<text x="1380" y="428" text-anchor="end" class="s" style="font-size:12px;font-style:italic">{title_note}</text></svg>')
