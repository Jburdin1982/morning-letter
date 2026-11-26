import json, sys
from datetime import date, datetime
wx = json.load(open('wx.json')); past = json.load(open('past.json')); alm = json.load(open('alm.json'))
DASH = "&mdash;"
def sky(c):
    if c is None: return '<span class="dash">&mdash;</span>'
    if isinstance(c,str):
        l=c.lower(); c = 10 if ("sunny" in l or "clear" in l or "frost" in l) and "partly" not in l and "mostly" not in l else 50 if ("partly" in l or "mostly sunny" in l or "mostly clear" in l) else 100
    if c < 20: return '<svg class="ic" viewBox="0 0 24 24"><circle cx="12" cy="12" r="5" fill="none" stroke="#5a4526" stroke-width="1.6"/>'+''.join(f'<line x1="12" y1="1.5" x2="12" y2="4.5" stroke="#5a4526" stroke-width="1.6" transform="rotate({a} 12 12)"/>' for a in range(0,360,45))+'</svg>'
    if c < 75: return '<svg class="ic" viewBox="0 0 24 24"><circle cx="8" cy="9" r="4" fill="none" stroke="#5a4526" stroke-width="1.5"/><path d="M8 20h10a4 4 0 0 0 0-8 5 5 0 0 0-9.5-1A4.5 4.5 0 0 0 8 20z" fill="#f7f0dd" stroke="#5a4526" stroke-width="1.5"/></svg>'
    return '<svg class="ic" viewBox="0 0 24 24"><path d="M6 19h12a4.5 4.5 0 0 0 0-9 6 6 0 0 0-11.5 1.5A3.8 3.8 0 0 0 6 19z" fill="#e9dfc2" stroke="#5a4526" stroke-width="1.5"/></svg>'
def pct(v): return DASH if v is None else f"{round(v)}%"
def deg(v): return DASH if v is None else f"{round(v)}&deg;"
def clock(h): return f"{h%12 or 12} {'AM' if h<12 else 'PM'}"
hrs = ''.join(f"<th>{clock(h['hour'])}</th>" for h in wx['hours'])
hrow = lambda f: ''.join(f"<td>{f(h)}</td>" for h in wx['hours'])
hourly = f'''<table class="wx hr"><tr><th>Today</th>{hrs}</tr>
<tr><td class="l">Temperature</td>{hrow(lambda h: deg(h['temp']))}</tr>
<tr><td class="l">Sky</td>{hrow(lambda h: sky(h['cloud']))}</tr>
<tr><td class="l">Rain</td>{hrow(lambda h: pct(h['rain']))}</tr></table>'''
days = wx['days']
def dname(s): return datetime.fromisoformat(s).strftime('%a %-d')
def per(day,p,key): return wx['periods'].get(day['date'],{}).get(p,{}).get(key)
grid = '<table class="wx wk"><tr><th></th>'+''.join(f"<th>{dname(d['date'])}</th>" for d in days)+'</tr>'
grid += '<tr><td class="l">High / Low</td>'+''.join(f"<td><b>{deg(d['high'])}</b> / {deg(d['low'])}</td>" for d in days)+'</tr>'
for lab,p in (("Morning","morning"),("Midday","midday"),("Afternoon","afternoon")):
    grid += f'<tr><td class="l">{lab}</td>'+''.join(f"<td>{sky(per(d,p,'cloud'))}<br><small>{deg(per(d,p,'temp'))} &middot; {pct(per(d,p,'rain'))}</small></td>" for d in days)+'</tr>'
grid += '<tr><td class="l">Rain, day</td>'+''.join(f"<td>{pct(d['rain'])}</td>" for d in days)+'</tr></table>'

css = '''
@page { size: 8.5in 11in; margin: 0.7in 0.8in; }
html { background: transparent; }
body { font-family: "Latin Modern Roman","LM Roman 10",serif; font-size: 10.9pt; line-height: 1.32; color:#2b2118; margin:0; text-align: justify; hyphens: auto; }
.frame { position: fixed; top:-0.38in; left:-0.45in; right:-0.45in; bottom:-0.38in; border: 1.6pt solid #8a6a35; outline: 0.6pt solid #8a6a35; outline-offset: -5pt; z-index:-1; }
h1 { font-variant: small-caps; text-align:center; font-size: 32pt; font-weight: normal; letter-spacing: 0.04em; margin: 0; color:#4a3618; }
.sub { text-align:center; font-style: italic; font-size: 10.6pt; margin: 2pt 0; color:#5a4526; }
.date { text-align:center; font-variant: small-caps; letter-spacing:0.12em; font-size: 12pt; margin: 4pt 0 2pt; }
.orn { text-align:center; color:#8a6a35; font-size: 13pt; margin: 2pt 0 8pt; }
h2 { font-variant: small-caps; font-weight: normal; font-size: 16pt; text-align:center; letter-spacing: 0.06em; margin: 16pt 0 6pt; color:#4a3618; break-after: avoid; page-break-after: avoid; }
h2::before, h2::after { content:"\\2766"; color:#8a6a35; font-size: 11pt; margin: 0 0.6em; }
h3 { font-size: 11.4pt; margin: 8pt 0 2pt; font-weight: bold; text-align:left; break-after: avoid; page-break-after: avoid; }
p { margin: 0 0 6pt; orphans: 3; widows: 3; }
.sal { margin-top: 6pt; }
table { border-collapse: collapse; width:100%; margin: 4pt 0 8pt; break-inside: avoid; page-break-inside: avoid; }
.wx th, .wx td { border: 0.6pt solid #b99d62; padding: 2.5pt 2pt; text-align:center; font-size: 9.4pt; }
.wx th { background:#efe3c3; font-weight: normal; font-variant: small-caps; letter-spacing:0.04em; }
.wx td.l { text-align:left; font-variant: small-caps; background:#f3e9cd; white-space:nowrap; }
.wx small { font-size: 8pt; color:#5a4526; }
.ic { width: 15pt; height: 15pt; vertical-align: middle; }
.dash { color:#8a6a35; }
.alm { width:100%; } .alm td { border:none; border-bottom: 0.5pt dotted #b99d62; padding: 2pt 4pt; font-size: 10.4pt; text-align:left; } .alm td:nth-child(even){ text-align:right; font-weight:bold; }
.mk td, .mk th { border: 0.6pt solid #b99d62; padding: 2.5pt 5pt; font-size: 10pt; text-align:left; } .mk th { background:#efe3c3; font-weight: normal; font-variant: small-caps; } .mk td.n { text-align:right; }
.picks { margin:2pt 0 6pt 1.2em; padding:0; text-align:left; } .picks li { margin-bottom:3pt; }
.mk.zt td,.mk.zt th{font-size:8.8pt;padding:1.5pt 4pt;line-height:1.15}
.mk.split{break-inside:auto;page-break-inside:auto} .mk.split tr{break-inside:avoid}
.note { font-size: 9.6pt; font-style: italic; color:#5a4526; }
.ps { font-style: italic; }
.sign { margin-top: 6pt; margin-bottom:0; text-align:left; }
.foot { text-align:center; font-size: 8.8pt; color:#6b5a3c; margin-top: 4pt; margin-bottom:0; font-style: italic; }
.page { break-before: page; page-break-before: always; }
.pastimes h2 { margin-top: 0; }
.flip { transform: rotate(180deg); font-size: 8pt; line-height:1.25; margin-top: 4pt; text-align:left; }
.flip.box { border-top: 0.6pt solid #b99d62; padding-top:4pt; }
ol.clues.fl { font-size:8.8pt; line-height:1.22; margin:3pt 0 3pt 1.1em; } ol.clues.fl .bl{ letter-spacing:.06em; font-family:monospace; font-size:8.5pt; }
ol.clues { margin: 2pt 0 6pt 1.2em; padding:0; text-align:left; } ol.clues li { margin-bottom: 2pt; }
.two { display:flex; gap: 20pt; align-items:flex-start; } .two > div { flex:1; }
.board { text-align:center; } .board svg { width: 100%; max-width: 3.1in; height:auto; }
'''
def P(t): return "".join(f"<p>{x.strip()}</p>" for x in t.split("||"))
body = []

import os as _os
SD='sections/'
def SEC(txt, lead=False):
    out=[]; first=True
    for ln in txt.strip().split('\n'):
        ln=ln.strip()
        if not ln or ln.startswith('LOG:'): continue
        if ln.startswith('### '): out.append(f'<h3>{ln[4:].strip()}</h3>')
        else: out.append(P(ln))
    return out
def part(fn, tag=None):
    t=open(SD+fn).read()
    t=t.split('\nLOG:')[0]
    if tag is None: return t
    import re
    m=re.split(r'^## (\w[\w ]*)$', t, flags=re.M)
    d={m[i].strip():m[i+1] for i in range(1,len(m),2)}
    return d.get(tag,'')
def raw(fn): return open(SD+fn).read() if _os.path.exists(SD+fn) else ''

INTRO=P(open(SD+'intro.txt').read().strip())
ZONE=part('sports.txt','ZONE TABLE').strip().replace('class="mk"','class="mk zt"',1)
body.append('<h1>The Morning Letter</h1><div class="sub">With the compliments of the Editor, to Jonesboro, Brookland &amp; neighbors</div>')
body.append('<div class="date">Thursday, the Twenty-Sixth of November, 2026 &middot; Thanksgiving Day</div><div class="orn">&#10086;</div>')
body.append('<p>Good morning,</p>')
body.append(INTRO)
body.append('<h2>The Day Ahead</h2>'); body.append(hourly); body.append(grid)
body.append(P('Thanksgiving Day opens cold and gray, about 33 degrees at six o’clock under a solid lid of cloud, with a breeze near 10 miles an hour. The wet weather gathers through the morning: the rain chance is about 21 percent at dawn, 54 percent by nine and 69 percent by noon, and it peaks near 90 percent around three o’clock. With the thermometer stuck between 34 and 38 all day, some of what falls may come as wet snow or sleet mixed with the rain, though ground this warm should keep most roads simply wet. The high is only about 39. The wind picks up as the day goes on, to 17 or 18 miles an hour by afternoon and near 19 at suppertime, so it will feel colder than the numbers say; anyone driving to the family table will want headlights on and a little extra following distance.||The rain chance falls back to about 13 percent by nine tonight, and the low settles near 33. Friday stays cloudy but dry, about 36 at nine and 47 for the high, with the wind easing to a breath by evening. Then the weekend turns mild: about 62 on Saturday and 63 on Sunday, with a 50 percent chance of showers Sunday morning and midday as a front passes, the temperature already falling to about 50 by midafternoon behind it. Monday brings sunshine and about 52, and the mild air returns Tuesday and Wednesday, near 58 and 64.'))
body.append('<h2>The Almanac</h2>')
body.append(f'''<table class="alm"><tr><td>First light</td><td>{alm['first_light']}</td><td>Sunrise</td><td>{alm['sunrise']}</td></tr>
<tr><td>Solar noon</td><td>{alm['noon']}</td><td>Sunset</td><td>{alm['sunset']}</td></tr>
<tr><td>Last light</td><td>{alm['last_light']}</td><td>Length of day</td><td>{alm['day_length']}</td></tr>
<tr><td>Change from yesterday</td><td>{alm['change'].replace('-','&minus;')}</td><td>Moon</td><td>{alm['moon']}, {alm['illum']}% lit</td></tr></table>''')
body.append(P('The sun rises at 6:50 and sets at 4:49, and today, for the first time this season, the day falls short of ten hours, at 9 hours and 59 minutes, about a minute and 16 seconds less than yesterday’s. The moon, two days past full and still 98 percent lit, will be hidden behind the rain clouds tonight; it wanes toward its last quarter around the first of December, rising later each evening.'))
body.append(P('<i>In field and woods:</i> the wild turkeys of Crowley’s Ridge have long since gathered into their winter flocks, hens and young birds together, and on a raw day like this one they keep to the hardwood draws, scratching through the leaves for acorns; a flock of twenty crossing a gravel road near Bono or Lake City is a fine sight for the drive home. Pecans are falling in the old yard trees around Jonesboro, and the morning after a windy rain is the best time to gather them before the squirrels and crows do. At the feeder, the slate-gray juncos, the little birds our grandparents called snowbirds, have arrived from the north for the winter, and they feed on the ground beneath it; scatter a little millet there for them. In the kitchen, save the turkey carcass: simmered tomorrow with an onion, a carrot and a bay leaf, it makes the stock for the best soup of the year.'))
body.append('<p><i>Weather lore, not a forecast:</i> the old fisherman’s rhyme runs, “When the wind is in the north, the skillful fisher goes not forth; when the wind is in the east, ’tis neither fit for man nor beast; when the wind is in the south, it blows the bait in the fish’s mouth; when the wind is in the west, then ’tis at the very best.” Today’s cold, wet wind would have kept the old-timers by the fire, which, on Thanksgiving, is where most of us mean to be anyway.</p>')

body.append('<h2>Of Local Interest</h2>')
_loc=open(SD+'local.txt').read().split('\nLOG:')[0].strip().split('\n',1)
body.append(P(_loc[0].strip()))
body.extend(SEC(_loc[1]))
if _os.path.exists(SD+'police.html'): body.append(raw('police.html').split('<!-- MAX')[0])
body.append('<h2>From the State</h2>'); body.extend(SEC(part('state.txt')))
body.append('<h2>From the Nation</h2>'); body.extend(SEC(part('world.txt','NATION')))
body.append('<h2>From Abroad</h2>'); body.extend(SEC(part('world.txt','ABROAD')))
body.append(raw('markets.html').split('<!-- LOG')[0])
body.append('<h2>On the Field</h2>'); body.extend(SEC(part('sports.txt','ON THE FIELD')))
body.append('<h2>Afield &amp; Afloat</h2><p class="note" style="break-after:avoid;page-break-after:avoid">Ratings are rule-of-thumb estimates from the forecast, the rut calendar and the sun, not measurements of animal or fish behavior.</p><h3>Deer outlook: Fair</h3>'+P('Three things help today: the rut, now in its late, post-peak phase when older bucks still check for the last does; a cold dawn near 33; and a barometer that has been falling since yesterday, which often keeps deer feeding ahead of weather. Against them stands the rain, likely by midday and heaviest around three o’clock. Best windows: from 6:20 a.m. to about two hours after sunrise, the driest part of the day, and from 2:49 p.m. until sunset at 4:49 for anyone willing to sit in the wet.||<i>Today’s tip:</i> make it a short dawn hunt before the turkey goes in the oven. The rain chance is only about one in five at daylight but better than one in two by nine, so be in the stand early and plan to be home by midmorning. Hunt the edges of thick bedding cover, where deer will slip back as the weather arrives, and wear a quiet rain shell over wool. In Zone 4, around Jonesboro, it is bows only; in Zones 3, 6 and 8 the rifles are still out.'))
body.append(P('<b>Tomorrow, Friday (estimate: Fair).</b> A cold, gray dawn near 34, the barometer holding steady, a breeze near 10 miles an hour that fades through the day, and no rain to speak of. Deer that sat out Thursday’s weather should be on their feet. Windows: 6:21 a.m. to about two hours after sunrise, and 2:49 p.m. to sunset at 4:49.||<i>Tomorrow’s tip:</i> after a soaking rain the leaves are soft and quiet underfoot, the best still-hunting conditions of the fall. Ease along slowly, a few steps and a long look, through the oak flats and along field edges, where hungry deer will be making up for a day of lying low. Fresh scrapes freshened after the rain are worth an evening sit.'))
body.append('<h3>Fishing outlook: Fair</h3>')
body.append(P('The barometer has fallen fast since yesterday and keeps sliding slowly through today, which can set off a short feed, but the solid overcast, the rising wind and an afternoon no warmer than about 38 will slow Craighead Forest Lake and Lake Frierson. Best times: late morning, before the heavier rain around midafternoon, and the last hour before sunset at 4:49 if the weather breaks.||<i>Today’s tip:</i> if you can slip away between the parade and the meal, keep it short and slow. Crappie should be suspended near brush piles and the old creek channels in deeper water; a small minnow under a slip float, set just above the cover, needs no casting skill and little patience in the cold.'))
body.append(P('<b>Tomorrow, Friday (estimate: Good).</b> A steady barometer, a light chop in the morning from a 10-mile-an-hour breeze, and an afternoon near 47 under cloud make Friday the better day on the water. Best times: late morning through midafternoon, as the water warms a little, and the last hour before sunset at 4:49.||<i>Tomorrow’s tip:</i> Thursday’s rain will muddy the inflows, and that runoff carries food; bass and catfish often stack up just where stained water meets clearer water. Work a slow-rolled spinnerbait or a jig along that line, or along the rocks of the dam, which hold the day’s warmth longest. A morning on the lake is a pleasant alternative to the Black Friday crowds.'))
body.append('<h3>In season now, and what is next (zones 3, 4, 6 and 8)</h3>')
body.append(ZONE)
body.extend(SEC(part('sports.txt','SEASONS')))
body.append('<div style="break-inside:avoid;page-break-inside:avoid"><h2>Postscript</h2>')
body.append('<p class="ps" style="margin-left:2em;margin-right:2em">Over the river, and through the wood,<br>&emsp;To grandfather’s house we go;<br>&emsp;&emsp;The horse knows the way,<br>&emsp;&emsp;To carry the sleigh,<br>&emsp;Through the white and drifted snow.<br><br>Over the river, and through the wood,<br>&emsp;Oh, how the wind does blow!<br>&emsp;&emsp;It stings the toes,<br>&emsp;&emsp;And bites the nose,<br>&emsp;As over the ground we go.</p>')
body.append('<p class="ps">&mdash; Lydia Maria Child, from “The New-England Boy’s Song about Thanksgiving Day,” first printed in her <i>Flowers for Children</i> in the 1840s. Few of us travel by sleigh, and our snow today is mostly rain, but the wind will sting the toes and bite the nose on the way to the table all the same. A happy Thanksgiving to every household.</p>')
body.append('<p class="sign">Until tomorrow, with good wishes &mdash;<br><b>The Editor</b></p>')
body.append('<div class="foot">Compiled from many reports.</div></div>')


# Pastimes
import os, json as _json
fleet = _json.load(open('fleet.json')) if os.path.exists('fleet.json') else None
def fleet_svg(d):
    n=d['size']; cs=30; lab=18; W=lab+n*cs; H=lab+n*cs
    o=[f'<svg viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg" style="width:100%;height:auto;display:block;font-family:inherit">']
    for c in range(n): o.append(f'<text x="{lab+c*cs+cs/2}" y="12" text-anchor="middle" font-size="10" fill="#8a6a35">{chr(65+c)}</text>')
    for r in range(n):
        o.append(f'<text x="{lab/2}" y="{lab+r*cs+cs/2+4}" text-anchor="middle" font-size="10" fill="#4a3618">{r+1}</text>')
        for c in range(n):
            x=lab+c*cs;y=lab+r*cs
            o.append(f'<rect x="{x}" y="{y}" width="{cs}" height="{cs}" fill="none" stroke="#8a6a35" stroke-width="1"/><text x="{x+cs/2}" y="{y+cs/2+6}" text-anchor="middle" font-size="17" font-weight="bold" fill="#2b2118">{d["grid"][r][c]}</text>')
    o.append('</svg>'); return ''.join(o)
body.append('<div class="page pastimes"><h2>The Pastimes</h2>')
left='<div><h3>I. Mate in Two</h3>'+f'<div class="board">{past["chess_svg"]}</div>'+f'<p>{past["chess_prompt"]} White is shown with the lighter, outlined pieces; the board is oriented with White at the bottom.</p></div>'
if fleet:
    tot=sum(len(x['word']) for x in fleet['ships'])
    clues=''.join(f'<li><span class="bl">{" ".join("_" for _ in x["word"])}</span> ({len(x["word"])}) {x["hint"]}</li>' for x in fleet['ships'])
    right=('<div><h3>II. Word Fleet</h3>'+'<div style="width:84%">'+fleet_svg(fleet)+'</div>'+
      f'<ol class="clues fl">{clues}</ol>'
      f'<p class="note">Each clue is a definition. Find its word in the grid, across or down. Fire by putting a pencil dot on a letter: one dot is one shot. Check the answers below, then circle each right letter and cross out each wrong one. Your score is your number of dots. <b>Best possible score: {tot} shots.</b> My shots: ________</p></div>')
    sol_ii='II. '+', '.join(f"{x['word']} {chr(65+x['c'])}{x['r']+1} {'across' if x['dir']=='A' else 'down'}" for x in fleet['ships'])
else:
    right='<div><h3>II. The Four Houses</h3>'+f'<p>{past["logic_intro"]}</p><ol class="clues">'+''.join(f'<li>{c}</li>' for c in past['logic_clues'])+f'</ol><p>{past["logic_question"]}</p></div>'
    sol_ii='II. '+past['logic_answer']
body.append('<div class="two">'+left+right+'</div>')
if os.path.exists('comic/today.svg'):
    body.append('<h3 style="margin-top:2pt;margin-bottom:0">III. Sorry, Earth</h3><div class="comic" style="margin:1pt 0 0 0"><img src="comic/today.png" style="width:92%;display:block;margin:0 auto"></div>')
body.append('<div class="flip box"><b>Solutions printed upside down.</b><br>I. '+past['chess_solution']+'<br>'+sol_ii+'</div></div>')

html = f'<!doctype html><html><head><meta charset="utf-8"><title>The Morning Letter</title><style>{css}</style></head><body>'+'\n'.join(body)+'</body></html>'
open('letter.html','w').write(html)
print(len(html))

# ---- Phone reading view (reader.html): same content, reflowing, large type ----
import re, base64, os
rcss = '''
*{box-sizing:border-box} html{-webkit-text-size-adjust:100%}
body{margin:0;background:#f7f0dd;color:#2b2118;font-family:"Latin Modern Roman","CMU Serif",Georgia,serif;font-size:19px;line-height:1.55;text-align:left}
.wrap{padding:14px 16px 30px;max-width:720px;margin:0 auto}
h1{font-variant:small-caps;font-weight:normal;text-align:center;font-size:2rem;line-height:1.15;margin:6px 0;color:#4a3618}
.sub{text-align:center;font-style:italic;font-size:.9rem;color:#5a4526}
.date{text-align:center;font-variant:small-caps;letter-spacing:.08em;font-size:1.05rem;margin:8px 0 0}
.orn{text-align:center;color:#8a6a35;margin:2px 0 10px}
h2{font-variant:small-caps;font-weight:normal;text-align:center;font-size:1.45rem;letter-spacing:.05em;margin:34px 0 10px;padding-top:14px;border-top:1px solid #b99d62;color:#4a3618}
h2::before,h2::after{content:"\\2766";color:#8a6a35;font-size:.9rem;margin:0 .5em}
h3{font-size:1.1rem;margin:20px 0 4px}
p{margin:0 0 12px}
.tw{overflow-x:auto;margin:8px -4px 14px;padding:0 4px;-webkit-overflow-scrolling:touch}
table{border-collapse:collapse;width:100%}
.wx{min-width:520px} .wx th,.wx td{border:1px solid #b99d62;padding:5px 3px;text-align:center;font-size:.8rem}
.wx th{background:#efe3c3;font-weight:normal;font-variant:small-caps}
.wx td.l{text-align:left;font-variant:small-caps;background:#f3e9cd;white-space:nowrap}
.wx small{font-size:.7rem;color:#5a4526}
.ic{width:20px;height:20px;vertical-align:middle}
.alm td{border:none;border-bottom:1px dotted #b99d62;padding:5px 4px;font-size:.95rem;text-align:left}
.alm td:nth-child(even){text-align:right}
.mk{min-width:420px} .mk td,.mk th{border:1px solid #b99d62;padding:6px 8px;font-size:.9rem;text-align:left}
.mk th{background:#efe3c3;font-weight:normal;font-variant:small-caps}
.picks{margin:4px 0 12px 1.2em;padding:0} .picks li{margin-bottom:8px}
.note{font-size:.85rem;font-style:italic;color:#5a4526}
.ps{font-style:italic}.sign{margin-top:16px}
.foot{text-align:center;font-size:.8rem;color:#6b5a3c;font-style:italic;margin-top:18px}
.two{display:block} .two>div{margin-bottom:12px}
.board{text-align:center}.board svg{width:100%;max-width:340px;height:auto}
ol.clues{margin:4px 0 12px 1.3em;padding:0} ol.clues li{margin-bottom:6px} .bl{letter-spacing:.1em;font-family:monospace}
.comic img{width:100%;height:auto;border:1px solid #8a6a35}
.flip{transform:rotate(180deg);font-size:.8rem;border-top:1px solid #b99d62;padding-top:6px;margin-top:20px}
'''
def _reader(parts):
    h = '\n'.join(parts)
    h = re.sub(r'<table', '<div class="tw"><table', h); h = h.replace('</table>', '</table></div>')
    h = h.replace('<div class="page pastimes">', '<div class="pastimes">')
    if os.path.exists('comic/today.png'):
        b64 = base64.b64encode(open('comic/today.png','rb').read()).decode()
        h = h.replace('src="comic/today.png"', 'src="data:image/png;base64,'+b64+'"')
    return h
open('reader.html','w').write('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>The Morning Letter</title><style>'+rcss+'</style></head><body><div class="wrap">'+_reader(body)+'</div></body></html>')

