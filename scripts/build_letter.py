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
ZONE=part('sports.txt','ZONE TABLE').strip()
body.append('<h1>The Morning Letter</h1><div class="sub">With the compliments of the Editor, to Jonesboro, Brookland &amp; neighbors</div>')
body.append('<div class="date">Wednesday, the Twenty-Fifth of November, 2026</div><div class="orn">&#10086;</div>')
body.append('<p>Good morning,</p>')
body.append(INTRO)
body.append('<h2>The Day Ahead</h2>'); body.append(hourly); body.append(grid)
body.append(P('The day before Thanksgiving starts cold and gray, about 36 degrees at six o’clock under a full deck of cloud, with a north wind near 9 miles an hour. It stays dry through the morning, about 40 by nine, and the thermometer struggles to the low 40s at midday, near 43 to 44 for the high. Then the rain moves in: the chance is about 31 percent at noon, 79 percent by three o’clock and 88 percent by six, with the temperature already slipping back to about 40 by midafternoon and 36 by suppertime. Anyone driving to the grandparents’ house will want to leave early or go slowly after dark.||Tonight the rain may mix with or turn to a little wet snow as the air cools, with the low near 34 to 35; amounts look light, and ground this warm should keep most roads merely wet. Thanksgiving Day itself stays raw: about 34 in the morning and no warmer than the mid- to upper 30s by the hourly figures (the Weather Service’s own forecast is a bit milder, near 45), with rain and snow showers possible much of the day (the chance runs about 40 percent in the morning and near 76 percent by midafternoon) and a gusty northwest wind that will make it feel colder still. Then the weather turns kind for the long weekend: sunshine and about 54 on Friday, the low 60s Saturday and Sunday, with a chance of a shower Sunday, and the low 50s with sun next Monday and Tuesday.'))
body.append('<h2>The Almanac</h2>')
body.append(f'''<table class="alm"><tr><td>First light</td><td>{alm['first_light']}</td><td>Sunrise</td><td>{alm['sunrise']}</td></tr>
<tr><td>Solar noon</td><td>{alm['noon']}</td><td>Sunset</td><td>{alm['sunset']}</td></tr>
<tr><td>Last light</td><td>{alm['last_light']}</td><td>Length of day</td><td>{alm['day_length']}</td></tr>
<tr><td>Change from yesterday</td><td>{alm['change'].replace('-','&minus;')}</td><td>Moon</td><td>{alm['moon']}, {alm['illum']}% lit</td></tr></table>''')
body.append(P('The sun rises at 6:49 and sets at 4:50, giving ten hours and one minute of daylight, about a minute and 19 seconds less than yesterday’s. The moon, a day past full, still shows its whole face, though tonight’s rain clouds will keep it to themselves; it rises a little later each evening now and will wane toward its last quarter in early December.'))
body.append(P('<i>In field and garden:</i> a cold rain on the eve of a holiday is an old Delta tradition, and the farm ditches along the Cache River bottoms will be glad of it after this autumn’s long dry spell. Cotton stalks stand shredded in the fields and the rice levees are bare, so this is the week the snow geese and ducks look for any standing water, and a slow drive past a flooded field at dusk on Friday may show them by the hundreds. In the garden, pull the last of the kale and collards before the hard freeze, or throw an old sheet over them tonight; they are sweeter for a touch of frost but not for a hard freeze. In the kitchen, the pie crust likes this weather: cold butter, cold hands and a cold counter make it flaky, and a damp day keeps the dough from cracking.'))
body.append('<p><i>Weather lore, not a forecast:</i> the old saying runs, “If there’s ice in November that will bear a duck, there’ll be nothing after but sludge and muck,” meaning an early freeze promises a mild, muddy winter. Tonight may bring a few flakes, but no ice fit for a duck, so the saying will have to wait.</p>')

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
body.append('<h2>Afield &amp; Afloat</h2><p class="note" style="break-after:avoid;page-break-after:avoid">Ratings are rule-of-thumb estimates from the forecast, the rut calendar and the sun, not measurements of animal or fish behavior.</p><h3>Deer outlook: Fair</h3>'+P('The calendar still helps, since the rut has not quite left its peak window in north Arkansas, and the dawn is a cold 36, but the afternoon’s rain, likely by three o’clock, takes the shine off the day. The barometer has been easing down since yesterday ahead of the storm. Best windows: from 6:19 a.m. to about two hours after sunrise; from 10 a.m. to 2 p.m., while bucks are still cruising and before the rain arrives; and from 2:50 p.m. until sunset at 4:50 if the rain holds off.||<i>Today’s tip:</i> with a north wind near 10 to 12 miles an hour, sit on the south side of the cover you are hunting and approach from the south, and put the morning to work, since that is the dry part of the day. Deer often feed hard in the hours just ahead of a front, so a late-morning sit over an acorn flat or a food plot may be the best of it. In Zone 4, around Jonesboro, it is bow-only now; in Zones 3, 6 and 8 the rifles are still out.'))
body.append(P('<b>Tomorrow, Thanksgiving Day (estimate: Fair).</b> A raw dawn near 34 with a stiffer northwest wind, about 13 to 16 miles an hour, rain and snow showers possible through the day, and the barometer still falling, which tends to keep deer feeding; the rut is past its peak, though late chasing goes on. Windows: 6:20 a.m. to about two hours after sunrise, and 2:49 p.m. to sunset at 4:49.||<i>Tomorrow’s tip:</i> a short dawn sit before the turkey goes in the oven is the classic Thanksgiving hunt. Dress for wet cold, not dry cold, with wool or synthetic layers and a quiet shell, and choose a stand on the lee side of a ridge where the gusts will not carry your scent and the deer can bed out of the wind.'))
body.append('<h3>Fishing outlook: Poor</h3>')
body.append(P('A fast-falling barometer, a solid gray sky and an afternoon that barely reaches the low 40s add up to a slow day on Craighead Forest Lake and Lake Frierson, and the cold rain arriving after noon will chill the shallows further. If you go, go early in the afternoon before the rain, from late morning until about two o’clock, when the water is as warm as it will get.||<i>Today’s tip:</i> fish slow and deep. Crappie should be holding on brush piles and creek-channel edges in 12 to 18 feet of water; a small jig or a live minnow hung just above the cover, barely moving, will out-fish anything that has to be chased. Catfish are worth a try on cut bait in the deeper water.'))
body.append(P('<b>Tomorrow, Thanksgiving Day (estimate: Fair).</b> The barometer falls slowly through the day, which often starts a short feed ahead of the next change, but the afternoon stays in the mid-30s with a raw, gusty wind. Best times: late morning through midafternoon, and the last hour before sunset at 4:49, if you can get away from the table.||<i>Tomorrow’s tip:</i> fish the wind-sheltered banks, where you can keep a light line still; a blade bait or a jigging spoon worked off the bottom along the old creek channel is a good cold-water choice for bass. Then plan a longer trip for the sunny, mild weekend, when the water will begin to warm again.'))
body.append('<h3>In season now, and what is next (zones 3, 4, 6 and 8)</h3>')
body.append(ZONE)
body.extend(SEC(part('sports.txt','SEASONS')))
body.append('<div style="break-inside:avoid;page-break-inside:avoid"><h2>Postscript</h2>')
body.append('<p class="ps" style="margin-left:2em;margin-right:2em">“The year that is drawing towards its close, has been filled with the blessings of fruitful fields and healthful skies.”</p>')
body.append('<p class="ps">&mdash; Abraham Lincoln, Proclamation of Thanksgiving, October 3, 1863, the opening words of the proclamation that set apart “the last Thursday of November” as a national day of thanksgiving, written in the middle of the Civil War. On the eve of the holiday it began, the fields are in and the year is drawing toward its close.</p>')
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

