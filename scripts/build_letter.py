import json, sys
from datetime import date, datetime
wx = json.load(open('wx.json')); past = json.load(open('past.json')); alm = json.load(open('alm.json'))
DASH = "&mdash;"
def sky(c):
    if c is None: return '<span class="dash">&mdash;</span>'
    if isinstance(c,str):
        l=c.lower(); c = 10 if ("sunny" in l or "clear" in l) and "partly" not in l and "mostly" not in l else 50 if ("partly" in l or "mostly sunny" in l or "mostly clear" in l) else 100
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
body.append('<h1>The Morning Letter</h1><div class="sub">With the compliments of the Editor, to Jonesboro, Brookland &amp; neighbors</div>')
body.append('<div class="date">Sunday, the Eighth of November, 2026</div><div class="orn">&#10086;</div>')
body.append(P('Good morning,'))
body.append(P("A crisp, clear Sunday, with frost likely on the roofs and a warm afternoon to follow, and a great deal of news to get through: the fallout from Tuesday's elections at home and in Washington, a mass shooting in Poland, and a rare hard loss for the Red Wolves. Here is the week, set down as plainly as we can manage it."))

body.append('<h2>The Day Ahead</h2>')
body.append(hourly); body.append(grid)
body.append(P("Sunday starts cold, about 35 degrees at dawn, then turns sunny and mild, reaching a high near 64 under clear skies with a light breeze and no chance of rain. The evening stays clear and cools through the 50s toward a low near 35.||The week ahead is a warm one. Monday is sunny with a high near 69, Tuesday is mostly cloudy at about the same, and Wednesday, Veterans Day, climbs to the upper 70s with a shower chance of about one in three by afternoon. A cold front follows: Thursday tops out near 56, and Friday and Saturday turn properly chilly, with lows around 36 and 33."))

body.append('<h2>The Almanac</h2>')
body.append(f'''<table class="alm"><tr><td>First light</td><td>{alm['first_light']}</td><td>Sunrise</td><td>{alm['sunrise']}</td></tr>
<tr><td>Solar noon</td><td>{alm['noon']}</td><td>Sunset</td><td>{alm['sunset']}</td></tr>
<tr><td>Last light</td><td>{alm['last_light']}</td><td>Length of day</td><td>{alm['day_length']}</td></tr>
<tr><td>Change from yesterday</td><td>{alm['change'].replace('-','&minus;')}</td><td>Moon</td><td>{alm['moon']}, {alm['illum']}% lit</td></tr></table>''')
body.append(P("The moon is a hair-thin crescent in the pre-dawn east this morning, and the new moon arrives around Monday, which means the darkest nights of the month are just ahead. The Leonid meteors usually peak around November 17 and 18, and a dark moon will help; the best viewing comes after midnight. The full moon is due around the 24th."))
body.append(P("Out in the fields of Craighead and Poinsett counties the combines have mostly stopped, and the stubble is being disked or left for ducks; winter wheat that went in late is just showing a green haze. In the woods the oaks have dropped most of their acorns and the sweetgums and hickories have turned, so the last color of the year hangs on the ridges. Along the creeks, sparrows and juncos are arriving from the north to work the brush piles, and an early frost like this morning's finishes off whatever tender things are left in the garden.||<i>Weather lore, not a forecast:</i> &ldquo;When the woodpecker is busy in autumn, plenty of cold is coming.&rdquo; Country people read thick husks, busy squirrels and heavy hickory crops the same way."))

body.append('<h2>Of Local Interest</h2>')
body.append('<h3>Jonesboro voters reject the public safety tax</h3>')
body.append(P("Voters in Jonesboro turned down a proposed public safety tax on Tuesday, 59 percent against and 41 percent for, according to complete but unofficial results reported by Jonesboro Right Now. The tax, which the City Council had placed on the ballot in September, would have paid for the city's police and fire departments. The city now has to find another way to fund them, and no replacement has been announced. Results remain unofficial until the Craighead County Election Commission certifies them."))
body.append(P("In Ward 5 of the City Council, no candidate won a majority, so the top two, incumbent L.J. Bryant (38 percent) and challenger Patti Lack (29 percent), go to a runoff on December 1. Two other candidates, Vince Pearcy and James Carl Wilson Jr., were eliminated. In Lake City, a runoff on the same day will pit Daniel Haynes (38 percent) against Jackie Davis (36 percent); Mayor Cameron Tate finished third."))
body.append('<h3>Quorum Court and legislative seats change hands</h3>')
body.append(P("Democrats unseated four Republican incumbents on the Craighead County Quorum Court, the county's legislative body: Jolene Mullet won District 1, Blake Walker District 3, Roseann Askeland District 5 and Ross Kerley District 6. Republican Doug Formon won the open District 9 seat, and incumbents David Tennison (District 8) and Steve Cline (District 10) won re-election.||In the Arkansas House, Democrat Erika Askeland defeated six-term Republican Jack Ladyman by 109 votes to represent most of Jonesboro, while Republican Johnny Rye kept his seat over Democrat Shamal Carter. Curtis Hitt won the Second Judicial District circuit judge race, Division 4, with 63 percent. Voters also approved, by 63 percent, combining the county collector and treasurer offices, a change that takes effect in 2031."))
body.append('<h3>Brookland bonds will fund $27.6 million in projects</h3>')
body.append(P("Brookland voters approved restructuring and refinancing the city's bonds so it can pay for $27.555 million in projects without raising taxes. The list includes second phases of the sportsplex and the municipal building, sewer and storm-shelter work, and traffic changes at Highway 49 and School Street and at Highway 49 and Pine Log Road. Mayor Kenneth Jones said the bonds will be sold in January and construction could begin as early as March 2027."))
body.append('<h3>Acme Brick to end Jonesboro production on December 31</h3>')
body.append(P("Acme Brick will stop making brick at its Jonesboro plant on December 31, affecting 27 employees, the company's human resources director confirmed to NEA Report. An October 23 letter from company president Ed Watson listed Jonesboro among three plants being closed, with Montgomery, Alabama, and Tulsa, citing a need to align operations with market conditions; he wrote that business peaked in 2022 and profits have not recovered. The Jonesboro sales office, yard and distribution operation will stay open.||Eligible full-time workers will receive severance based on years of service, capped at 26 weeks, but must sign a release, and no severance is paid to anyone offered a comparable job elsewhere in the company. Watson said more details on benefits and job-placement help will follow."))
body.append('<h3>Grain and Gather festival honors rice farmers ahead of the Rice Bowl</h3>')
body.append(P("The Arkansas Rice Federation, led by executive director Kelly Robbins, held the first Grain and Gather festival in downtown Jonesboro on Friday night to thank rice farmers before the second annual Rice Bowl, the Arkansas State game against Louisiana-Monroe. The block party had a kids' zone, live music, rice-inspired dishes from downtown restaurants and a rice-brat eating contest, judged in part by Mayor Harold Copenhaver; the Lambda Chi Alpha fraternity won a $500 prize for the loudest cheering section. A tailgate followed on Saturday. Robbins said she hopes it becomes a Jonesboro tradition."))
body.append('<h3>Probation in a Jonesboro gunfire case</h3>')
body.append(P("A 21-year-old West Memphis woman pleaded guilty and was sentenced to 36 months of probation on two counts of aggravated assault and two counts of first-degree terroristic threatening, KAIT reported Sunday. Police said she fired a pistol on the 300 block of Reeves Street on May 27 while children were present, then drove off; officers later found her vehicle on East Washington Street, with a handgun, an AR-style pistol and suspected marijuana inside. As part of the sentence she must have no contact with the victim, pay court costs and complete a course toward a GED."))
body.append('<h3>Around town</h3>')
body.append(P("<b>Little Shop of Horrors</b>, the musical, runs at A-State's Fowler Center Drama Theatre November 13&ndash;22: 7:30 p.m. on Fridays and Saturdays (Nov. 13, 14, 20, 21) and 2:30 p.m. on Sundays (Nov. 15, 22). Tickets are $15 to $20, free for A-State students with ID, at the box office in First National Bank Arena or at 870-972-2781; the university suggests it for teens and older.||<b>Christmas at the Park</b> returns to Joe Mack Campbell Park, 600 Harry Drive, from Thursday, November 26 through Christmas Eve, with a drive-through of more than 400,000 lights ($10 a vehicle on drive-through nights; $20 or $25 for nights including Santa's Village), and check christmasattheparknea.com for hours."))

body.append('<h2>From the State</h2>')
body.append('<h3>Republicans lose their House supermajority</h3>')
body.append(P("Democrats flipped seats in Tuesday's election that cost Republicans their supermajority (a share large enough to pass certain bills alone) in the 100-member Arkansas House for the first time in a decade. Tallies in early reports differed, but by the most recent count Republicans hold about 70 seats and Democrats about 30, according to States Newsroom, and the figures are unofficial. Most appropriations bills need 75 votes, so Republicans will now need some Democratic support to fund state agencies.||House Minority Leader Andrew Collins said more leverage does not mean Democrats will hold up spending bills, while Republican Rep. David Ray warned Democrats not to overplay their hand. The first test comes in the 2027 session, when lawmakers take up the governor's roughly $7 billion budget proposal on Medicaid, SNAP and school vouchers."))
body.append('<h3>Statewide results</h3>')
body.append(P("Gov. Sarah Huckabee Sanders won a second term with 54 percent, U.S. Sen. Tom Cotton was re-elected with 55 percent over Democrat Hallie Shoffner, and Rep. Rick Crawford took the First Congressional District with 65 percent. Kim Hammer, a Republican, won secretary of state with nearly 56 percent. Statewide Issues 1, 2 and 4 passed and Issue 3 failed. All figures are unofficial until certified."))
body.append('<h3>Jury awards damages over a 2020 protest shooting</h3>')
body.append(P("A Little Rock jury awarded compensatory and punitive damages to a man who was hit in the face by a police beanbag round during the 2020 protests over police brutality, the Arkansas Democrat-Gazette reported this weekend. The case took six years to reach a verdict. We could not confirm the amounts, and the ruling may be appealed."))
body.append('<h3>Chase and group-home runaways</h3>')
body.append(P("Arkansas State Police arrested a teenager Saturday after a pursuit of about 100 mph that began in Forrest City after a shooting and ended in a crash on Interstate 40 in North Little Rock; a second suspect was still being sought. Separately, two of four teens who walked away from a Monticello group home Friday night were back in custody by Saturday evening, a state Department of Human Services official said."))

body.append('<h2>From the Nation</h2>')
body.append('<h3>Democrats win Congress; Trump shakes up his staff</h3>')
body.append(P("Democrats won control of both chambers of Congress in Tuesday's midterm elections. CBS News estimates they will hold at least 54 Senate seats and about 256 House seats when the new Congress convenes in January, up from 214 in the House now; more than 20 House races and two Senate races, in Alaska and Mississippi, were still uncalled. Among the notable results, Democrat James Talarico beat Republican Ken Paxton for a Texas Senate seat, and Democrats flipped more than 40 Republican-held House districts. Counting continues, and Alaska's ranked-choice tally is set for November 18.||President Trump said on Sunday that the nation had taken a &ldquo;giant step back in history,&rdquo; and said it was &ldquo;largely true&rdquo; that Republicans lost because of the Iran war, which he defended. In a 60 Minutes interview airing tonight he said he expects some firings. White House chief of staff Susie Wiles resigned and Stephen Miller, the president's longtime policy adviser, takes over on Monday, November 9. CBS reports that officials do not expect Miller's promotion to ease the immigration crackdown, and that several Justice Department officials have resigned."))
body.append(P("Democrats are already planning their agenda. Rep. Robert Garcia, the incoming House Oversight chair, plans investigations of the Trump family's businesses, immigration enforcement and the Epstein matter, and Sen. Elizabeth Warren plans to examine the financial sector as chair of the Senate Banking Committee. Both parties face leadership contests; Senate Democrats are debating whether to replace Chuck Schumer. Trump has called talk of impeachment &ldquo;extortion&rdquo; and asked the Justice Department to look into it. <i>(Reported by CBS News; other outlets should be consulted as results are finalized.)</i>"))
body.append('<h3>Employers added 165,000 jobs in October</h3>')
body.append(P("Employers added 165,000 jobs in October, far above the 59,000 economists expected, and the unemployment rate held at 4.1 percent, the Labor Department reported Friday. The strong report raised the odds that the Federal Reserve will keep interest rates high, which weighed on some stocks."))

body.append('<h2>From Abroad</h2>')
body.append('<h3>Six killed in a shooting in Krakow, Poland</h3>')
body.append(P("A 24-year-old Polish man opened fire in Krakow's Main Square, a crowded tourist area in the historic Old Town, on Saturday, killing six people and wounding 15. Police shot and wounded him, and he is in critical condition. Officers later found the bodies of his parents and sister at the family home about 93 miles away; he is also suspected in those deaths. His father legally owned more than 10 guns, and 11 weapons were recovered.||Poland's interior minister said the suspect held &ldquo;very radical&rdquo; far-right views, and prosecutors have classified the attack as terrorism. Poland declared two days of national mourning, and one of the two officers who stopped the gunman remains in a coma."))
body.append('<h3>The Iran war: blockade continues, talks paused</h3>')
body.append(P("The United States and Israel went to war with Iran on February 28. Heavy fighting has largely stopped, but Iran still restricts shipping through the Strait of Hormuz, the narrow waterway that carries much of the world's oil, and the U.S. keeps a blockade of Iranian ports. On Saturday U.S. forces disabled a cargo ship, the M/V Huda, in the Gulf of Oman after it allegedly tried to run the blockade, and U.S. Central Command announced a small new task force, Iron Gate, aimed at cutting Iran's overland trade routes. Iran's Revolutionary Guard called it &ldquo;wordplay.&rdquo;||Iran's foreign minister, Abbas Araghchi, said mediated talks have paused since the American elections and that Iran's proposal could reopen the strait within two days if U.S. conditions are met. President Trump told CNN that renewed all-out attacks are &ldquo;highly unlikely&rdquo; if talks progress. Secretary of State Marco Rubio is due at a G7 foreign ministers' meeting in Paris on Monday and Tuesday. Tanker explosions reported near the strait have not been independently confirmed."))
body.append('<h3>Ukraine: power outages ahead of winter</h3>')
body.append(P("Russian missile and drone strikes on Ukraine's energy system overnight left more than 600,000 people without power in the Dnipropetrovsk region and nearly 250,000 customers in the Kharkiv region, with 140 apartment buildings in Zhytomyr losing heat while temperatures hovered near freezing. President Volodymyr Zelenskyy said the death toll from a strike on an aid distribution center in Zaporizhzhia region on Monday had risen to 55. He accused Russia of stepping up attacks ahead of talks with Russia planned for next week."))
body.append('<h3>Train collision near Cairo</h3>')
body.append(P("One train crashed into the rear of another near Cairo, in the Giza area, killing at least seven people and injuring more than 100, according to CBS News. <i>(Single source; the toll may change.)</i>"))

body.append('<h2>Markets &amp; the Farm</h2>')
body.append('<p class="note">Figures are as of Friday&rsquo;s close, November 6.</p>')
body.append('''<table class="mk"><tr><th>Index</th><th>Close</th><th>Change</th><th>Week</th></tr>
<tr><td>S&amp;P 500</td><td class="n">7,376.86</td><td class="n">+0.31%</td><td class="n">&minus;2.68%</td></tr>
<tr><td>Dow Jones Industrials</td><td class="n">51,285.73</td><td class="n">&minus;0.46%</td><td class="n">&minus;0.94%</td></tr>
<tr><td>Nasdaq Composite</td><td class="n">24,579.42</td><td class="n">+1.09%</td><td class="n">&minus;3.37%</td></tr></table>''')
body.append(P("Stocks steadied on Friday after Thursday's sell-off, when technology shares fell hard, the S&amp;P 500 dropped 4.4 percent and the Nasdaq entered a correction (a fall of more than 10 percent from its high). Investors cited worries about the durability of the artificial-intelligence boom and about tighter regulation after the election. Friday's jobs report, stronger than expected, also lifted the dollar and interest-rate expectations. Chip stocks rebounded, while Oracle fell after Microsoft ended a cloud-capacity deal and DraftKings dropped after trimming its profit forecast.||Next week brings the October inflation (CPI) report on Tuesday, remarks from Federal Reserve officials, and earnings from Applied Materials, Cisco and CoreWeave."))
body.append('<h3>What analysts are saying</h3>')
body.append(P("Brokerage analysts changed their views on several well-known companies on Friday. <b>Analysts leaned toward buying:</b>"))
body.append('<ul class="picks">'
'<li><b>Becton Dickinson (BDX)</b>, a maker of syringes and medical devices. Wells Fargo raised it to Overweight (buy-leaning) from Equal Weight and lifted its price target to $242 from $170. <i>Risk:</i> a big jump in a target raises expectations the company must meet.</li>'
'<li><b>SiTime (SITM)</b>, which makes precision timing chips used in electronics. Seaport Research upgraded it to Buy from Neutral with a $425 target. <i>Risk:</i> chip stocks were extremely volatile this week.</li>'
'<li><b>Centrus Energy (LEU)</b>, which supplies enriched uranium fuel for nuclear plants. Roth Capital upgraded it to Buy from Neutral. <i>Risk:</i> shares in this niche can swing sharply on news. <i>(Single source: Daily Trade Alert.)</i></li></ul>')
body.append(P("<b>Analysts turned cautious:</b>"))
body.append('<ul class="picks">'
'<li><b>Molson Coors (TAP)</b>, the brewer of Coors and Miller. Wells Fargo cut it to Underweight from Equal Weight and trimmed its target to $36 from $38. <i>Risk to the call:</i> steadier earnings would prove it too gloomy.</li>'
'<li><b>BJ&rsquo;s Wholesale Club (BJ)</b>, the membership warehouse chain. Citigroup cut it to Neutral from Buy, with a target of $113, up from $111. <i>Risk to the call:</i> strong membership growth could prove it too cautious.</li></ul>')
body.append(P("The roundups checked (Yahoo Finance / The Fly, Daily Trade Alert, Benzinga) listed the ratings but not the analysts' full reasoning. Analysts are often wrong and prices may already have moved. This is information, not advice."))
body.append('''<table class="mk"><tr><th>Commodity</th><th>Latest</th><th>Change</th></tr>
<tr><td>Crude oil, WTI</td><td class="n">$90.83</td><td class="n">+$0.31</td></tr>
<tr><td>Crude oil, Brent</td><td class="n">$98.32</td><td class="n">+$0.03</td></tr>
<tr><td>Gasoline, Arkansas average (regular)</td><td class="n">$3.71</td><td class="n">&minus;$0.09, week</td></tr>
<tr><td>Gasoline, Jonesboro average (regular)</td><td class="n">$3.63</td><td class="n">&minus;$0.10, week</td></tr>
<tr><td>Live cattle (Dec.)</td><td class="n">$214.05</td><td class="n">&minus;$0.35</td></tr>
<tr><td>Feeder cattle (Jan.)</td><td class="n">$318.37</td><td class="n">&minus;$1.95</td></tr>
<tr><td>Lean hogs (Dec.)</td><td class="n">$53.52</td><td class="n">&minus;$1.57</td></tr>
<tr><td>Corn (Dec.), per bushel</td><td class="n">$4.415</td><td class="n">+1.5&cent;</td></tr>
<tr><td>Soybeans (Jan.), per bushel</td><td class="n">$11.9375</td><td class="n">+5.5&cent;</td></tr>
<tr><td>Wheat, Chicago (Dec.), per bushel</td><td class="n">$5.9125</td><td class="n">&minus;8&cent;</td></tr>
<tr><td>Cotton (Dec.), cents per pound</td><td class="n">79.11</td><td class="n">+0.40</td></tr>
<tr><td>Rice (Jan.), per hundredweight</td><td class="n">$18.255</td><td class="n">&minus;9&cent;</td></tr></table>''')
body.append(P("Oil prices ended Friday slightly higher but fell sharply for the week, with Brent down about 13 percent, its steepest weekly drop since the start of the pandemic, on hopes of a U.S.-Iran deal. Gasoline fell about a dime in a week in Arkansas, still nearly $1 above a year ago; the national average is near $4.10, per AAA as carried by local reports. Gasoline changes are for the week; other lines are Friday's change."))

body.append('<h2>On the Field</h2>')
body.append(P("<b>Arkansas State football</b> lost to Louisiana-Monroe 19-17 on Saturday at Centennial Bank Stadium in the Rice Bowl. The Red Wolves led 17-16 on Clune Van Andel's 41-yard field goal with about 5:42 left, but ULM answered with a 40-yard field goal, and an A-State interception with about a minute left ended the comeback. Quarterback Trey Owens threw for 193 yards and a touchdown and led the team with 67 rushing yards; AG McGhee had 14 tackles. A-State is 4-5, 2-3 in the Sun Belt, and plays at Coastal Carolina next Saturday, November 14, at noon Eastern on ESPN+. The final home game is November 28 against Troy."))
body.append(P("<b>Arkansas</b> lost at Auburn 26-23 on Saturday and fell to 3-6, 1-5 in the SEC; Cam Settles ran for 100 yards and kicker Max Gilbert hit three field goals. <b>Tennessee</b> beat Kentucky 34-6 at Neyland Stadium before 101,915 fans, scoring 24 straight points in the second half; DeSean Bishop ran for 109 yards and two touchdowns."))
body.append(P("<b>A-State volleyball</b> beat Louisiana Tech twice this weekend, in four sets and then in three, and A-State basketball lost on the road, 101-86 at No. 20 Alabama in an early-season test."))

body.append('<h2>Afield &amp; Afloat</h2>')
body.append('<p class="note">Ratings are rule-of-thumb estimates from the forecast, the rut calendar and the sun, not measurements of animal or fish behavior.</p>')
body.append('<h3>Deer outlook: Excellent</h3>')
body.append(P("Everything lines up for the last day of the youth weekend: the rut is in its peak window, dawn is a frosty 35 degrees after a sharp cool-down from yesterday, the wind is light and the barometer is slipping ahead of a change. Hunt first light at about 6:02 a.m. for roughly two hours, and the evening from 3:00 to 5:00 p.m. Ten to two is realistic for cruising bucks, so a sit through the middle of the day is worth it.||<b>Today's tip:</b> with almost no wind, scent will drift in odd swirls; get to the stand well before light, wear it quietly, and watch the downwind side of field corners and the trails between bedding and food, where bucks trail does. A grunt call and a few rattles from the stand can pull a cruising buck over."))
body.append(P("<b>Tomorrow, Monday (estimate: Good):</b> a milder dawn near 41 and a warm 69 in the afternoon, still peak rut, with light wind. Watch 6:03 to about 8 a.m. and 2:59 to 4:59 p.m. <b>Tomorrow's tip:</b> on warm afternoons deer hold in shade until late, so favor the last hour in the evening and the cooler morning hours."))
body.append('<h3>Fishing outlook: Good</h3>')
body.append(P("For the Crowley's Ridge lakes such as Craighead Forest Lake and Lake Frierson, steady pressure, a slow fall ahead of a change and a warm afternoon near 63 make a good day. Fish late morning through mid-afternoon as the shallows warm, and again in the last hour before sunset at 5:00 p.m.||<b>Today's tip:</b> after the cold snap, crappie will hold deeper around brush piles and docks in 8 to 12 feet; try small minnows or 1/16-ounce jigs under a float and fish slowly. Bass are likely to take a slow spinnerbait or jig along sunny, rocky banks as the afternoon warms."))
body.append(P("<b>Tomorrow, Monday (estimate: Good):</b> steady pressure and a warm afternoon near 69; best late morning through mid-afternoon, with another window in the last hour before sunset at 4:59 p.m. <b>Tomorrow's tip:</b> a sunny afternoon should push bream and crappie toward shallow water on the sun side of the lake; shorten your line and move slowly."))
body.append('<h3>In season now, and what is next (zones 3, 4, 6 and 8)</h3>')
body.append('''<table class="mk"><tr><th>Zone</th><th>Archery</th><th>Youth gun</th><th>Modern gun</th><th>Muzzleloader</th></tr>
<tr><td>3</td><td>open to Feb. 28</td><td>Nov. 7&ndash;8; Jan. 2&ndash;3</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr>
<tr><td>4</td><td>open to Feb. 28</td><td>Nov. 7&ndash;8; Jan. 2&ndash;3</td><td>Nov. 14&ndash;22; Dec. 26&ndash;28</td><td>closed</td></tr>
<tr><td>6</td><td>open to Feb. 28</td><td>Nov. 7&ndash;8; Jan. 2&ndash;3</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr>
<tr><td>8</td><td>open to Feb. 28</td><td>Nov. 7&ndash;8; Jan. 2&ndash;3</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr></table>''')
body.append(P("<b>This weekend:</b> today is the final day of the youth modern-gun hunt in all four zones; a second youth weekend follows January 2&ndash;3. Archery season has been open since September 26 in all four zones.||<b>Next Saturday, November 14,</b> modern gun season opens. Zone 4, which includes Craighead County, closes November 22 (reopening December 26&ndash;28), while Zones 3, 6 and 8 run through December 6. The bag limit is four deer, no more than two bucks. Outside the CWD (chronic wasting disease) management zone, legal bucks must be button bucks or have at least three points on one side. Craighead County falls under CWD regulations, and the Game and Fish Commission offers free CWD testing statewide through drop-off sites, taxidermists and regional offices; call ahead before visiting an office."))
body.append(P("<b>Waterfowl:</b> snow, blue, Ross's and white-fronted geese close today, November 8. Duck, coot and merganser season runs November 21&ndash;29, December 10&ndash;23 and December 26 to January 31. Check agfc.com for small-game dates."))

body.append('<h2>The Week in Review</h2>')
body.append(P("<b>Local:</b> The week's central story was Tuesday's election: Jonesboro rejected its public safety tax, Democrats took four Quorum Court seats and a Jonesboro House seat, Brookland approved bonds for $27.6 million in projects, and runoffs were set for December 1 in Jonesboro's Ward 5 and in Lake City. The City Council also limited camping in parks and parking lots, and Acme Brick announced it will end production in Jonesboro at year's end.||<b>State:</b> Governor Sanders won a second term and presented a roughly $7 billion budget, while Republicans lost their House supermajority. A former Arkansas Supreme Court bar-exam official was charged with 65 felonies, and the attorney general directed $8.4 million from the Monsanto settlement to 21 water projects.||<b>Nation and world:</b> Democrats won both houses of Congress and the White House chief of staff stepped down, while a mass shooting in Krakow and the stalled Iran talks dominated the world news. Oil fell sharply on hopes of a deal."))
body.append(P("<b>Sports and the week ahead:</b> A-State football lost 19-17 to ULM and visits Coastal Carolina Saturday; Arkansas lost at Auburn and hosts South Carolina on November 14; Tennessee routed Kentucky. Ahead: the CPI inflation report Tuesday, Veterans Day Wednesday, modern gun deer season Saturday, and Little Shop of Horrors opening Friday at A-State.||A closing thought: after a week this loud, a cold clear Sunday is a good gift. Whichever way you voted, the work now is the ordinary kind: check on a neighbor, pay attention to the budget, and be kind at the supermarket."))

body.append('<h2 class="page">Postscript</h2>')
body.append('<p class="ps">The Hawthorn Gate.</p>')
body.append('<p class="ps">Every November, old Mr. Pruitt walked the fence line of his hundred acres with a hammer and a coffee can of staples, and every November the neighbors said it was no use. The fence, they pointed out, had been falling down since 1974.</p>')
body.append('<p class="ps">&ldquo;It is not falling down,&rdquo; he told his granddaughter that morning, as the frost steamed off the pasture. &ldquo;It is leaning with dignity.&rdquo;</p>')
body.append('<p class="ps">She was nine, and she held the can. At the far corner they came to the gate, which was older than the fence, hung on a hinge made from a plow part, and which had not shut properly in anyone&rsquo;s memory. He lifted it, set it on its hook, and it hung open exactly as far as it always had.</p>')
body.append('<p class="ps">&ldquo;Why do you fix it if it never works?&rdquo; she asked.</p>')
body.append('<p class="ps">He considered this longer than a grown man should. &ldquo;The gate was never for keeping things out,&rdquo; he said. &ldquo;It is for letting the right things in. Your grandmother came through this gate. So did the Johnsons&rsquo; cow, once, and that was the only one of the two I did not enjoy.&rdquo;</p>')
body.append('<p class="ps">They stood a while. A flock of juncos, newly come down from the north, worked the hedgerow in a gray-and-white scurry.</p>')
body.append('<p class="ps">&ldquo;Well,&rdquo; said Mr. Pruitt, tapping the hinge with the hammer, &ldquo;that ought to hold until spring.&rdquo; The gate swung a quarter inch and settled. It had not held in fifty years, and it held that morning, perhaps out of politeness.</p>')
body.append('<p class="sign">Until tomorrow, with good wishes &mdash;<br><b>The Editor</b></p>')
body.append('<div class="foot">Compiled from many reports. Local election results are unofficial until certified.</div>')
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
    right=('<div><h3>II. Word Fleet</h3>'+'<div style="width:94%">'+fleet_svg(fleet)+'</div>'+
      f'<ol class="clues fl">{clues}</ol>'
      f'<p class="note">Each clue is a definition. Find its word in the grid, across or down. Fire by putting a pencil dot on a letter: one dot is one shot. Check the answers below, then circle each right letter and cross out each wrong one. Your score is your number of dots. <b>Best possible score: {tot} shots.</b> My shots: ________</p></div>')
    sol_ii='II. '+', '.join(f"{x['word']} {chr(65+x['c'])}{x['r']+1} {'across' if x['dir']=='A' else 'down'}" for x in fleet['ships'])
else:
    right='<div><h3>II. The Four Houses</h3>'+f'<p>{past["logic_intro"]}</p><ol class="clues">'+''.join(f'<li>{c}</li>' for c in past['logic_clues'])+f'</ol><p>{past["logic_question"]}</p></div>'
    sol_ii='II. '+past['logic_answer']
body.append('<div class="two">'+left+right+'</div>')
if os.path.exists('comic/today.svg'):
    body.append('<h3 style="margin-top:2pt;margin-bottom:0">III. Sorry, Earth</h3><div class="comic" style="margin:1pt 0 0 0"><img src="comic/today.png" style="width:96%;display:block;margin:0 auto"></div>')
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
