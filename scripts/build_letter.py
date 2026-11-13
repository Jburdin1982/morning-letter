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
body.append('<h1>The Morning Letter</h1><div class="sub">With the compliments of the Editor, to Jonesboro, Brookland &amp; neighbors</div>')
body.append('<div class="date">Friday, the Thirteenth of November, 2026</div><div class="orn">&#10086;</div>')
body.append(P('Good morning,'))
body.append(P("Friday the 13th dawns frosty and bright, near 34 degrees, with a sunny afternoon only just reaching 49, and a harder freeze near 29 waits for Saturday&rsquo;s opening of modern gun deer season. In town, the Golden Grotto is closing after 41 years, and the city&rsquo;s bike-and-walking path over the Marion Berry Parkway has come in $884,000 over budget. Farther out, Paragould is getting a $20 million plant expansion. Nationally, Nvidia&rsquo;s founder has resigned and a Brooklyn building collapse has killed eight, and abroad, President Putin has warned Europe against sending peacekeeping troops to Ukraine."))

body.append('<h2>The Day Ahead</h2>')
body.append(hourly); body.append(grid)
body.append(P("Frost on the windshields this morning: it is about 34 degrees at 6 a.m. under a perfectly clear sky, warming to 42 by 9 o&rsquo;clock and 48 at noon, and topping out near 49 in mid-afternoon with nothing but sun. A northwest breeze of 10 to 12 miles an hour through the middle of the day will keep it feeling cooler than that. The wind lies down at sunset, and the temperature falls fast, to about 41 by 6 p.m. and 37 by 9.||Saturday brings the hardest freeze yet, near 29 at dawn, then a gray, overcast day near 50. From there the week warms steadily and stays dry: mid 50s Sunday, near 60 by Tuesday, the upper 60s Wednesday and about 71 next Thursday, with rain chances in single digits every day."))

body.append('<h2>The Almanac</h2>')
body.append(f'''<table class="alm"><tr><td>First light</td><td>{alm['first_light']}</td><td>Sunrise</td><td>{alm['sunrise']}</td></tr>
<tr><td>Solar noon</td><td>{alm['noon']}</td><td>Sunset</td><td>{alm['sunset']}</td></tr>
<tr><td>Last light</td><td>{alm['last_light']}</td><td>Length of day</td><td>{alm['day_length']}</td></tr>
<tr><td>Change from yesterday</td><td>{alm['change'].replace('-','&minus;')}</td><td>Moon</td><td>{alm['moon']}, {alm['illum']}% lit</td></tr></table>''')
body.append(P("The crescent moon, a little fuller each evening, hangs low in the southwest after sunset and goes down by mid-evening, leaving the clear, cold sky to the stars; first quarter falls around Tuesday. The sun now sets before five, and the day is ten hours and nineteen minutes long."))
body.append(P("This is the weekend to finish the frost chores: drain and coil the garden hoses, bring in the last potted geraniums and ferns, and pick any green tomatoes still hanging; they will ripen slowly on a windowsill. The turnip greens, collards and mustard in the fall garden will only sweeten from a freeze, as old cooks have always said, and so will the persimmons along the fencerows, which are hardly worth eating before a frost and very much worth it after. Out in the woods, the squirrels are cutting hickory nuts in earnest, and the first flocks of robins and cedar waxwings are working the hollies and cedars along Crowley&rsquo;s Ridge."))
body.append(P("<i>Weather lore, not a forecast:</i> &ldquo;Clear moon, frost soon.&rdquo; Tonight the old saying and the forecast happen to agree."))

body.append('<h2>Of Local Interest</h2>')
body.append('<h3>Golden Grotto closing after 41 years</h3>')
body.append(P("The Golden Grotto, the costume and party shop on Red Wolf Boulevard that has dressed generations of Jonesboro children for Halloween, school plays and birthday parties, is closing after 41 years. It opened as a costume store in 1985 and later added balloons, decorations and party supplies. In a message to customers, the store said the &ldquo;difficult decision&rdquo; came from &ldquo;several circumstances,&rdquo; and thanked the town for the friendships and memories, calling it &ldquo;our joy and privilege to help make your dreams come true.&rdquo; A closing sale begins today, Friday, and the last day of business has not been announced. It is the second long-standing local shop to announce its closing this week, after Cooksey&rsquo;s Flower Shop."))
body.append('<h3>Parkway trail bid comes in $884,000 over the estimate</h3>')
body.append(P("The city&rsquo;s planned walking and biking path across the Marion Berry Parkway overpass drew a low bid of about $2.38 million from White River Material, roughly $884,000 more than the city expected; the other three bids, opened Oct. 21, ran from $2.81 million to $3.36 million. The project would build a protected shared path and better sidewalks from Washington Avenue to Aggie Road, with lane changes, drainage, bridge work and lighting.||The bid includes two options that would trim the cost: dropping color-changing decorative lights and some wiring would save about $338,000, and a different paving choice about $87,000, which together would bring it to about $1.96 million, still some $258,000 over the August estimate. Arkansas State University had asked for accent lighting, including for university logos, and for stairs. A $500,000 federal grant is lined up for the work, and the city is expected to decide on a contract around Dec. 20."))
body.append('<h3>Trials set for man accused in threatening-letter campaign</h3>')
body.append(P("Cody Dale Taylor, 26, of Forrest City, who faces nearly 140 felony and misdemeanor charges over forged letters threatening murder, rape and kidnapping, will go to trial early next year in two counties. Authorities say the letters went to government and school officials, private citizens and former classmates, and were forged to appear to come from other people; the Craighead County case began May 4, when a Bono resident reported receiving 19 of them. Police say Mr. Taylor admitted forging letters in retaliation for how he had been treated during and after school. The charges are allegations.||In Craighead County he is charged with stalking, forgery, terroristic threatening and harassing communications, and his jury trial is set for Feb. 1 through 12. In Greene County, where a judge found probable cause for 135 offenses and investigators say most letters bore a local educator&rsquo;s name, leading to more than a dozen false police reports against that educator, he has pleaded not guilty; trial there is set for the week of Jan. 4, and he is held on a $750,000 bond."))
body.append('<h3>Nettleton schools look over ten years of building plans</h3>')
body.append(P("Leaders of the Nettleton School District reviewed draft designs Thursday for the projects paid for by the 4.8-mill tax increase voters approved last year. Superintendent Karen Curtner met with principals and architects from the firm Brackett Krennerich over plans for new classrooms and storm safe rooms at the high school, junior high and STEAM campuses, a covered walkway joining the two STEAM schools, a performing arts hall students may help name, a new end-zone building and an indoor sports building to be called Raider Arena. STEAM Intermediate Principal Lisa Hogan said theater classes now held in portable buildings would finally have a stage. The district has just over 3,700 students and is &ldquo;at capacity right now,&rdquo; Ms. Curtner said; work begins at the junior high and high school and should pick up by summer 2027."))
body.append('<h3>Around town</h3>')
body.append(P("<b>Tonight, Friday, 6 p.m.:</b> Elks Lodge 498, 2113 W. Washington Ave., serves a pasta Veterans Dinner, free to veterans and spouses, $10 for others. <b>Saturday, 8 a.m. to noon:</b> city clean-up at 2650 Lacy Drive takes furniture, mattresses, TVs, computers, appliances with refrigerant removed, and up to eight tires without rims; no yard waste or hazardous materials. The last one this year is Dec. 5. <b>Saturday, 9 a.m. to 2 p.m.:</b> Judd Hill Farmers Market on Aggie Road opens the first of three winter markets, with an ornament-decorating station; the others are Nov. 21 and Dec. 19. <b>Saturday 7 p.m. and Sunday 2 p.m.:</b> Visual Performing Arts Magnet students present &ldquo;Charlie and the Chocolate Factory&rdquo; at the JHS Center for the Performing Arts, tickets online. <b>Sunday, 2 to 4 p.m.:</b> Together We Foster collects coats, new socks and underwear, suitcases and children&rsquo;s winter clothes for foster children at 1400 E. Washington Ave.||<b>Monday, 7 p.m.:</b> the Northeast Arkansas Chorale sings its Christmas concert at Williams Baptist University in Walnut Ridge, $10 or $20 a family. <b>Tuesday:</b> the City Council meets at 5:30 p.m. <b>Friday, Nov. 20, 6 a.m. to 6 p.m.:</b> the Fill the Food Bank drive collects canned goods, peanut butter, macaroni and rice at Harps in Brookland and the Jonesboro Walmarts and Sam&rsquo;s Club. <b>Sunday, Dec. 6, 2 p.m.:</b> the 25th Brookland Christmas Parade lines up at Brookland High School; no registration needed."))
body.append('<h3>Our neighbors farther afield</h3>')
body.append(P("<b>Paragould:</b> Georgia-Pacific will invest about $20 million at its Anchor Packaging plant, adding two production lines and 10 to 20 jobs to a work force of more than 600 that makes plastic food containers for restaurants and grocery stores. Work has begun, and the new lines should run by late 2027. Mayor Josh Agee called it exciting news for the whole community."))
body.append(P("<b>Greene County:</b> two Paragould residents, Pamela S. Bryant, 64, and Billy J. Adams, 47, were killed Monday evening when their car, turning left from U.S. 412 onto Highway 139, was struck by another car, State Police said; the other driver was hurt. <b>Wynne:</b> the City Council has barred new data centers in the city for one year, to give it time to plan for water, power and zoning; the pause ends unless the council extends it."))

body.append('<h2>From the Police Reports</h2>')
body.append('<p class="note">Jonesboro Police incident reports. Charges are allegations. No names are printed.</p>')
body.append(P(open('parts/police.txt').read()))
body.append('<div style="break-inside:avoid;page-break-inside:avoid"><p class="note">At the county jails</p>'+P(open('parts/jail.txt').read())+'</div>')

body.append('<h2>From the State</h2>')
body.append('<h3>Bar exam scandal could reach thousands of court cases</h3>')
body.append(P("At least 64 people who took the Arkansas bar exam, the test lawyers must pass to be licensed, had their scores changed between July 2020 and July 2025, according to a sworn police statement filed this week. Nancie Givens, 62, who ran the Arkansas Supreme Court&rsquo;s Office of Professional Programs, which gives the exam, was arrested Nov. 5 and charged with 65 felony counts of tampering with public records; she has pleaded not guilty, and the charges are allegations. The justices say points were taken from some test-takers and given to others, lifting some to the 270 needed to pass, while at least one person who passed may have been recorded as failing.||Gregg Parrish, who heads the state&rsquo;s public defender agency, the lawyers appointed for people who cannot afford one, estimates that thousands of cases could be touched if dozens of lawyers were wrongly licensed, and expects convicted defendants to ask that their convictions be thrown out; he says there is no legal precedent. Officials have not said how many of those affected went on to practice law. The Supreme Court says it will decide what to do when state and federal investigations finish, and Ms. Givens has a review hearing on Jan. 4."))
body.append('<h3>State board presses failing districts to drop four-day weeks</h3>')
body.append(P("&ldquo;We have lost our way,&rdquo; Education Secretary Jacob Oliva told the State Board of Education on Thursday as it heard improvement plans from the seven traditional school districts graded F this fall: Lafayette County, Pine Bluff, Watson Chapel, Blytheville, Strong-Huttig, Prescott and Blevins. Three of them, Prescott, Blevins and Strong-Huttig, hold classes only four days a week, and Mr. Oliva urged all three to return to five. Strong-Huttig&rsquo;s board already wants to, and Blevins will ask the state board for approval in December; any calendar change needs both boards&rsquo; consent.||For our corner of the state, the news is Blytheville, already under state control, whose acting superintendent told the board the district might rise to a D this year but could remain an F. Mr. Oliva warned that Lafayette County could be moved to the highest level of state intervention if it does not improve by spring."))
body.append('<h3>Rural health grants hold steady at $207.7 million</h3>')
body.append(P("Arkansas will receive $207.7 million in the second year of the Rural Health Transformation Program, a five-year, $50 billion federal effort to shore up health care in the countryside, the U.S. Department of Health and Human Services announced Monday; that is about half a percent less than the first year. Gov. Sarah Huckabee Sanders expects the five-year total to reach about $1 billion. First-year money in Northeast Arkansas included nearly $3 million for a family-medicine residency and $9.6 million largely to restore cancer infusion care at Great River Medical Center in Blytheville. The money cannot cover a struggling hospital&rsquo;s day-to-day costs. The state will open applications for second-year grants in early January, and earlier recipients must apply again."))
body.append('<h3>Governor takes her book tour to California</h3>')
body.append(P("Gov. Sanders, promoting her new memoir &ldquo;Unapologetic,&rdquo; told an audience at the Ronald Reagan Presidential Library in California on Thursday that she expects &ldquo;a lot of buyers&rsquo; remorse&rdquo; among voters after Democrats&rsquo; gains in last week&rsquo;s election, and that Republicans need to &ldquo;go on offense.&rdquo; The tour, which goes to Dallas on Sunday and ends in early December, has fed talk of a future national campaign; she said she is focused on her present job. Back home, Democrats flipped 10 state House seats, ending the Republican three-fourths majority there that is needed to pass spending bills, so the January session will require bargaining with the minority. Republicans keep their supermajority in the Senate."))

body.append('<h2>From the Nation</h2>')
body.append('<h3>Nvidia&rsquo;s founder resigns as chief executive</h3>')
body.append(P("Jensen Huang, who co-founded Nvidia and ran it for 33 years, resigned Thursday as chief executive and left its board. Nvidia makes the computer chips that power much of the world&rsquo;s artificial intelligence and is among the most valuable companies on earth. The company gave no reason; its chief financial officer, Colette Kress, becomes interim chief executive, and longtime director Harvey Jones becomes its first board chairman.||On Sunday Mr. Huang admitted being unfaithful to his wife and apologized, after news reports that he had a relationship with a businesswoman whom U.S. intelligence officials reportedly believe works for Chinese intelligence; the New York Times later reported a second relationship, with a senior Nvidia executive who reported to him. Mr. Huang denies compromising national security or company secrets, the board says it has no reason to believe security was harmed, and the spying claim is unproven.||President Trump called it a &ldquo;horrible thing.&rdquo; Rep. Brian Mast of Florida, who chairs the House Foreign Affairs Committee, says Mr. Huang agreed to testify before Thanksgiving, and Sen. Tim Scott has asked him to appear before the Senate Banking Committee on Dec. 3. Nvidia stock fell about 4 percent."))
body.append('<h3>Brooklyn building collapse kills eight</h3>')
body.append(P("A three-story building in the Flatbush neighborhood of Brooklyn, New York, partly collapsed into a construction site next door about 4 p.m. Wednesday, killing eight people, two of them children ages 9 and 10, and two of them construction workers. Mayor Zohran Mamdani said 18 people were hurt, four of them firefighters, and praised workers who, having barely escaped, &ldquo;turned back and dug victims out of the rubble.&rdquo; Rescue work ended Thursday afternoon. No cause has been announced, but a report filed with the city in March described the wall facing the site as in &ldquo;poor condition with noticeable cracks,&rdquo; and a demolition contractor there was cited in April for working after a stop-work order. All work at the site is halted, police are leading an investigation, and inspectors are checking about 100 related job sites."))
body.append('<h3>Democrat wins Mississippi Senate seat</h3>')
body.append(P("After more than a week of counting absentee and provisional ballots, the Associated Press declared Democrat Scott Colom, a district attorney in northeast Mississippi, the winner over Republican Sen. Cindy Hyde-Smith, 49.2 percent to 48.7 percent with about 99 percent counted; Sen. Hyde-Smith conceded. Mr. Colom will be the first Black senator elected from Mississippi since 1874 and the state&rsquo;s first Democratic senator since 1982; in 2023 Sen. Hyde-Smith had blocked his nomination to a federal judgeship. The result gives Democrats and the independents who vote with them at least 55 seats in the new Senate, still short of the 60 needed to overcome a filibuster. Results are unofficial until certified."))
body.append('<h3>Gunman kills building manager in Washington</h3>')
body.append(P("A resident of an apartment building in Washington&rsquo;s Logan Circle neighborhood shot and killed the building&rsquo;s manager, James Stuart, 46, in a ground-floor gym Thursday morning, then fired from his seventh-floor balcony and wounded four people nearby, one critically, police said. Police identified the gunman as Matt Lambert, 55, whom his lawyer described as an emergency-room doctor. He barricaded himself in his apartment and set a fire that sprinklers helped contain; officers later found him dead of a self-inflicted gunshot wound. Investigators believe the shooting grew out of his long dispute with the condominium association over mold and other complaints."))
body.append('<h3>Microsoft outage disrupts email and Teams</h3>')
body.append(P("A widespread failure knocked out Microsoft&rsquo;s Outlook email, its Teams messaging and meeting app, and other workplace services on Thursday, with problems reported from more than 70 countries. Microsoft said some of its servers had &ldquo;unexpectedly&rdquo; become unavailable and that it was not a cyberattack. By early Friday it reported only partial recovery and gave no time for a full fix, though most Teams access had returned; it said delayed email will keep being retried for up to 48 hours, so messages should not be lost."))

body.append('<h2>From Abroad</h2>')
body.append('<h3>Putin meets U.S. envoys and warns Europe off sending troops</h3>')
body.append(P("Steve Witkoff and Jared Kushner, President Trump&rsquo;s special envoys, met Russian President Vladimir Putin at the Kremlin for about two hours Thursday, then flew to Dublin to brief Ukrainian President Volodymyr Zelenskyy. In the televised part of the meeting, Mr. Putin said that if European countries sent troops to Ukraine to guarantee a peace deal, Russia would treat them as targets and &ldquo;the war will resume immediately,&rdquo; and he repeated his demand that Ukraine withdraw from four regions Russia claims but does not fully hold.||Mr. Witkoff said Russia had agreed to let European countries join the next round of talks; on Friday the Kremlin said it had not. Mr. Zelenskyy sounded doubtful. European leaders were meeting in Dublin this week, and Russian and Ukrainian negotiators are expected to meet again next week. Overnight, Russia said it shot down 1,198 Ukrainian drones, and its officials said four people were killed in an industrial area of Volgograd; Ukraine said a Russian attack killed at least two in Odesa and a drone set a Kyiv hospital afire. Neither side&rsquo;s figures can be checked independently."))
body.append('<h3>Israeli strike on Gaza hospital kills six</h3>')
body.append(P("An Israeli airstrike hit the surgery building at Nasser Hospital in Khan Younis, in southern Gaza, shortly after midnight Thursday, killing at least six people, among them surgeon Rizk Abu Shaira and a 13-year-old boy, according to Gaza&rsquo;s Health Ministry, which is run by Hamas. The Israeli military said it targeted a senior Hamas commander and that Hamas used the hospital as a command center, and said it was looking into reports of medical staff and patients killed; Hamas called the claim a lie, and doctors there said there was no warning. The strike came despite the U.S.-backed ceasefire in place since October 2025, during which the ministry counts more than 1,600 Palestinians killed and Israel reports four soldiers killed. The World Health Organization says only two of Gaza&rsquo;s 37 hospitals are fully working."))
body.append('<h3>Nuclear inspectors &ldquo;increasingly concerned&rdquo; about Iran</h3>')
body.append(P("The International Atomic Energy Agency, the United Nations body that inspects nuclear programs, said in a confidential report Friday that it is &ldquo;increasingly concerned&rdquo; about a uranium-enrichment plant at Isfahan that Iran declared in June 2025 but has never let inspectors see. The agency does not know the plant&rsquo;s exact location or whether it holds nuclear material, calling that &ldquo;a matter of serious proliferation concern&rdquo;; its chief has said Iran&rsquo;s most highly enriched uranium is believed to be stored in tunnels there. On Thursday Iran&rsquo;s Assembly of Experts, the clerical body that oversees the supreme leader, called for a review of Iran&rsquo;s membership in the Nuclear Non-Proliferation Treaty, the pact that bars members from building nuclear weapons. President Trump said he would &ldquo;not hesitate&rdquo; to strike Iran again if it threatens allies or shipping. Iran&rsquo;s claims Friday to have hit a U.S. radar site in Bahrain and downed a U.S. drone are unconfirmed."))
body.append('<h3>Ireland pressed over shipments of an aluminum ingredient to Russia</h3>')
body.append(P("Ireland faces calls to stop sending Russia alumina, the refined powder that is the main ingredient in aluminum, which goes into everything from cans to missiles and drones and is not covered by European Union sanctions. Europe&rsquo;s largest alumina refinery, at Aughinish in County Limerick, belongs to the Russian aluminum company Rusal. An activist group estimates about 491,000 metric tons went from Ireland to Russia between March and October, and a joint investigation by reporters found that some reaches a supplier to Russian defense contractors; the company denies any military link, and an Irish minister says there is &ldquo;absolutely no evidence&rdquo; of it. Another minister said Ireland would consider sanctions if the European Commission proposed them."))

body.append('<div style="break-inside:avoid;page-break-inside:avoid"><h2>Markets &amp; the Farm</h2>'+'<p class="note">Figures are for Thursday&rsquo;s close, November 12. Week changes are from Friday, November 6.</p>')
body.append('''<table class="mk"><tr><th>Index</th><th>Close</th><th>Day</th><th>Week</th></tr>
<tr><td>S&amp;P 500</td><td class="n">7,592.40</td><td class="n">&minus;0.35%</td><td class="n">+2.92%</td></tr>
<tr><td>Dow Jones Industrials</td><td class="n">52,297.09</td><td class="n">&minus;0.36%</td><td class="n">+1.97%</td></tr>
<tr><td>Nasdaq Composite</td><td class="n">25,366.09</td><td class="n">&minus;0.39%</td><td class="n">+3.20%</td></tr></table></div>''')
body.append(P("Stocks gave back a little Thursday after Nvidia&rsquo;s chief executive resigned (see From the Nation); its shares fell as much as 14 percent before closing down about 4 percent. Rising long-term interest rates also weighed, and traders now see a strong chance the Federal Reserve raises rates at its Dec. 9 meeting. Even so, all three indexes are up 2 to 3 percent for the week. The October producer price index, a measure of wholesale prices, comes out Friday morning, and Nvidia reports its earnings Tuesday, with Walmart and Home Depot also due next week."))
body.append('<h3>What analysts are saying</h3>')
body.append(P("Analysts leaned toward buying two steel names: Barclays upgraded <b>Reliance (RS)</b>, the country&rsquo;s largest metals service center and steel distributor, to Overweight with a $507 target, citing tighter steel supply, stronger volumes and higher prices while costs hold steady (risk: steel is cyclical, and a slowdown would squeeze margins). Barclays also lifted <b>Cleveland-Cliffs (CLF)</b>, the steelmaker and iron-ore producer, to Equal Weight from Underweight, seeing opportunity after a selloff, a lukewarm upgrade to neutral rather than to buy (risk: heavy debt and dependence on carmakers)."))
body.append(P("Analysts turned cautious on <b>General Mills (GIS)</b>, maker of Cheerios, Betty Crocker and Pillsbury: Piper Sandler cut it to Neutral and its target to $35 from $41, citing operating pressures and a dividend that now takes about 80 percent of earnings (counterpoint: the stock is already about 30 percent off its February high and yields about 7 percent). Bernstein cut <b>ConocoPhillips (COP)</b>, the large oil and gas producer, to Market Perform with a $122 target, judging that easing with Iran is more likely than escalation and oil prices should settle (counterpoint: oil jumped Thursday). <i>This is information, not advice.</i>"))
body.append('''<table class="mk split"><tr><th>Commodity</th><th>Close</th><th>Change</th></tr>
<tr><td>Crude oil, WTI (Dec.)</td><td class="n">$88.74</td><td class="n">+$2.21</td></tr>
<tr><td>Crude oil, Brent (Jan.)</td><td class="n">$95.82</td><td class="n">+3.3%</td></tr>
<tr><td>Gasoline, Arkansas average (regular), AAA Nov. 12</td><td class="n">$3.55</td><td class="n">&minus;16&cent;, week</td></tr>
<tr><td>Gasoline, Jonesboro average (regular), AAA Nov. 12</td><td class="n">$3.49</td><td class="n">&minus;15&cent;, week</td></tr>
<tr><td>Live cattle (Dec.)</td><td class="n">$218.90</td><td class="n">&minus;7&frac12;&cent;</td></tr>
<tr><td>Feeder cattle (Jan.)</td><td class="n">$331.675</td><td class="n">+$3.875</td></tr>
<tr><td>Lean hogs (Dec.)</td><td class="n">$55.15</td><td class="n">&minus;87&frac12;&cent;</td></tr>
<tr><td>Corn (Dec.), per bushel</td><td class="n">$4.42&frac12;</td><td class="n">&minus;5&frac12;&cent;</td></tr>
<tr><td>Soybeans (Jan.), per bushel</td><td class="n">$12.19</td><td class="n">&minus;11&frac34;&cent;</td></tr>
<tr><td>Wheat, Chicago (Dec.), per bushel</td><td class="n">$5.84&frac14;</td><td class="n">&minus;15&frac14;&cent;</td></tr>
<tr><td>Cotton (Dec.), cents per pound</td><td class="n">78.67</td><td class="n">+0.15</td></tr>
<tr><td>Rough rice (Jan.), per hundredweight</td><td class="n">$18.65&frac12;</td><td class="n">+33&cent;</td></tr></table>''')
body.append('<p class="note">Rough rice and the Jonesboro gasoline average: single source (Brownfield; AAA via KAIT).</p>')
body.append(P("Oil rose after President Trump wrote that &ldquo;we don&rsquo;t need a deal with Iran&rdquo; and Iran reported tanker explosions in the Strait of Hormuz, though crude is still down for November. Grains slid on selling after Tuesday&rsquo;s government crop report and a dollar at an 18-month high, which makes American grain dearer abroad; wheat hit an eight-month low, and a 136,000-ton soybean sale to China did not stem the slide. Feeder cattle rallied on short covering while live cattle and hogs eased. At the pump, AAA&rsquo;s weekly report has the Arkansas average down 16 cents in a week, and the national average under $4 for the first time since July."))

body.append('<h2>On the Field</h2>')
body.append(P("<b>Arkansas State football</b> (4-5) comes off its open date to play Coastal Carolina (3-6) Saturday at noon Central in Conway, S.C., on ESPN+; the oddsmakers call it nearly even, and it may decide whether the Red Wolves reach a bowl. Starting right tackle Sterling Wiggins is out for the season, but linebacker Nigel Nelson, out since a September leg injury, could return. <b>A-State men&rsquo;s basketball</b> (1-2), beaten 82-65 by UT Martin on Tuesday while shooting 31 percent, hosts Dillard Saturday at 7 p.m. at First National Bank Arena (ESPN+) and UAPB on Wednesday."))
body.append(P("<b>Arkansas</b> (3-6, 1-5 SEC) hosts No. 17 South Carolina (6-3), winners of four straight, Saturday at 6:45 p.m. in Fayetteville on the SEC Network; Gamecock quarterback LaNorris Sellers, their leading passer and rusher, is expected to play on a sore ankle. <b>Tennessee</b> (7-2), up to No. 8 in Tuesday&rsquo;s College Football Playoff rankings, visits Texas A&amp;M Saturday at 2 p.m. on ESPN. The next playoff rankings come out Tuesday."))

body.append('<h2>Afield &amp; Afloat</h2>')
body.append('<p class="note">Ratings are rule-of-thumb estimates from the forecast, the rut calendar and the sun, not measurements of animal or fish behavior.</p>')
body.append('<h3>Deer outlook: Excellent</h3>')
body.append(P("Everything lines up this morning: the rut at its peak in north Arkansas, a frosty dawn near 34 degrees about 14 colder than yesterday, and a barometer climbing behind the front. Be settled by 6:07 a.m. and hunt until about 8:40, sit again from 2:56 p.m. to sunset at 4:56, and if you can stay, 10 a.m. to 2 p.m. is realistic, with bucks cruising for does. <b>Today&rsquo;s tip:</b> the breeze behind a front usually comes out of the north or northwest and freshens to around 12 miles an hour by noon; hunt a stand on the south or east side of where you expect deer, and use this last bow-only day to watch a doe bedding area from downwind."))
body.append(P("<b>Tomorrow, Saturday (estimate: Good):</b> modern gun season opens in all four of our zones. Dawn will be near 29 under a gray sky with a light breeze and a still-rising barometer. Watch from about 6:08 to 8:40 a.m. and 2:55 to sunset at 4:55, and stay put through midday. <b>Tomorrow&rsquo;s tip:</b> opening-morning traffic moves deer; rather than leave at 9, sit tight while other hunters walk out and push deer past you, and wear the required blaze orange on the way in and out as well as on the stand."))
body.append('<h3>Fishing outlook: Fair</h3>')
body.append(P("At the Crowley&rsquo;s Ridge lakes (Craighead Forest Lake and Lake Frierson), the sudden cold puts fish off their feed, though a light chop and a sunny afternoon near 49 help some. Fish late morning through mid-afternoon as the sun warms the shallows, and again in the last hour before sunset at 4:56. <b>Today&rsquo;s tip:</b> look for crappie on the north banks, which catch the most sun, and around brush piles in 8 to 12 feet of water; a small minnow under a slip cork, barely moving, is the honest choice on a day like this."))
body.append(P("<b>Tomorrow, Saturday (estimate: Fair):</b> after a hard frost, an overcast day near 50 with light wind and a steady barometer. Best from late morning through mid-afternoon and in the last hour before sunset at 4:55. <b>Tomorrow&rsquo;s tip:</b> clouds keep bass from tucking deep into cover; slow-roll a spinnerbait or crawl a jig along the first drop-off off a point, and expect to work for each bite."))
body.append('<h3>In season now, and what is next (zones 3, 4, 6 and 8)</h3>')
body.append('''<table class="mk"><tr><th>Zone</th><th>Archery</th><th>Youth gun</th><th>Modern gun</th><th>Muzzleloader</th></tr>
<tr><td>3</td><td>open to Feb. 28</td><td>Jan. 2&ndash;3</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr>
<tr><td>4</td><td>open to Feb. 28</td><td>Jan. 2&ndash;3</td><td>Nov. 14&ndash;22; Dec. 26&ndash;28</td><td>no season</td></tr>
<tr><td>6</td><td>open to Feb. 28</td><td>Jan. 2&ndash;3</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr>
<tr><td>8</td><td>open to Feb. 28</td><td>Jan. 2&ndash;3</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr></table>''')
body.append(P("<b>Saturday, Nov. 14,</b> modern gun season opens. In Zone 4, which includes Craighead County, it runs only nine days, to Nov. 22, and allows one antlerless deer by modern gun; Zones 3, 6 and 8 run to Dec. 6. The bag in all four zones is four deer, no more than two of them antlered bucks. Dogs may not be used for deer in Zones 3 and 4, and chronic wasting disease rules apply in Craighead, Jackson, Mississippi and Randolph counties.||<b>Ducks</b> open a week from Saturday, Nov. 21, for a first segment that ends Nov. 29 (not Dec. 1, as two AGFC mailings misprinted); the later segments are Dec. 10&ndash;23 and Dec. 26 through Jan. 31. The daily limit is six, with no more than four mallards, two of them hens. The AGFC is drawing for new permit-only waterfowl hunts, including 715 acres of the St. Francis Sunken Lands WMA in Poinsett County; applications open at agfc.com each Thursday at 3 p.m. and close Sunday at midnight. Quail are open through Feb. 7, and rabbit and squirrel through Feb. 28."))

body.append('<h2>Postscript</h2>')
body.append('<p class="ps">The Frost performs its secret ministry,<br>Unhelped by any wind.</p>')
body.append('<p class="ps">&mdash; Samuel Taylor Coleridge, &ldquo;Frost at Midnight&rdquo; (1798). Tonight, with the air still and the sky clear, it will be at work on every roof and pasture in the county.</p>')
body.append('<p class="sign">Until tomorrow, with good wishes &mdash;<br><b>The Editor</b></p>')
body.append('<div class="foot">Compiled from many reports.</div>')

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
