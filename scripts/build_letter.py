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
body.append('<div class="date">Monday, the Sixteenth of November, 2026</div><div class="orn">&#10086;</div>')
body.append(P('Good morning,'))
body.append(P("A third frosty dawn, about 34 degrees, gives way to a cloudless afternoon near 58, and the whole week leans warmer, toward 70 by Thursday. The City Council takes a first look tomorrow at a 20-year plan for a Jonesboro of 100,000 people, a record field of runners raised money for the Church Health Center, and the gun deer season enters its first full week. Farther off, a rocket carrying 40 Amazon internet satellites failed after launch from Florida, and Estonia says it will close its border crossings with Russia after a foiled sabotage plot."))
body.append('<h2>The Day Ahead</h2>')
body.append(hourly); body.append(grid)
body.append(P("Frost on the rooftops again this morning: it is about 34 degrees at 6 o'clock under a perfectly clear sky, with only a light breeze of 6 or 7 miles an hour. The sun does the rest, bringing 44 by 9 o'clock, 56 at noon and a high near 58 by mid-afternoon, with no cloud and no chance of rain anywhere in the day. It cools quickly after the 4:54 sunset, to about 47 by suppertime and 40 by 9 p.m.||Tuesday is a near copy, a frosty 34 at dawn and a sunny 62 in the afternoon with almost no wind. From there the week warms steadily: 67 on Wednesday, about 70 on Thursday and 69 on Friday, with lows climbing into the 40s and 50s. Clouds thicken over the weekend, and the first small rain chances of the week, near 10 to 20 percent, arrive Saturday and Sunday."))
body.append('<h2>The Almanac</h2>')
body.append(f'''<table class="alm"><tr><td>First light</td><td>{alm['first_light']}</td><td>Sunrise</td><td>{alm['sunrise']}</td></tr>
<tr><td>Solar noon</td><td>{alm['noon']}</td><td>Sunset</td><td>{alm['sunset']}</td></tr>
<tr><td>Last light</td><td>{alm['last_light']}</td><td>Length of day</td><td>{alm['day_length']}</td></tr>
<tr><td>Change from yesterday</td><td>{alm['change'].replace('-','&minus;')}</td><td>Moon</td><td>{alm['moon']}, {alm['illum']}% lit</td></tr></table>''')
body.append(P("The young moon, a little more than a third lit, hangs in the south-southwest at dusk and reaches first quarter around Tuesday; it will be full around the 24th, two days before Thanksgiving. The day is down to 10 hours and 14 minutes, losing a minute and 37 seconds since yesterday. The Leonid meteor shower, which by long custom peaks around Nov. 17, is best seen in the dark hours after the moon sets and before dawn; it is usually a modest show of a dozen or so an hour, but these clear, cold nights give it a fair chance.||In the yard, the pecans are dropping, and a calm sunny afternoon is the time to gather them before the crows and squirrels do. There is still time to set out garlic and spring bulbs such as daffodils and tulips while the ground is workable. Watch the brush piles and the edges of the lawn for the first juncos, the small slate-gray sparrows country people call snowbirds, which come down from the north about this time and stay until spring."))
body.append(P('<i>Weather lore, not a forecast:</i> &ldquo;If there&rsquo;s ice in November that will bear a duck, there&rsquo;ll be nothing after but sludge and muck.&rdquo; So far the frost has not managed more than the windshield.'))
body.append('<h2>Of Local Interest</h2>')
body.append(P("It was a quiet weekend in town, with most of the news looking ahead to Tuesday's council meeting and the busy week before Thanksgiving."))
body.append('<h3>Council to see a draft 20-year growth plan and weigh a North Church Street rezoning appeal</h3>')
body.append(P("The Jonesboro City Council meets at 5:30 p.m. Tuesday at the Municipal Center, 300 S. Church St. The biggest item is a first look at \"Plan Jonesboro,\" the city's proposed 20-year comprehensive plan for growth, along with a new Master Street Plan, the map that guides how the city and the Metropolitan Area Planning Commission, the city-county planning board, rule on new development and road projects. The draft says Jonesboro has about 82,000 residents, up 48 percent since 2000, and expects to pass 100,000 in less than 15 years; it also notes that sales tax supplies 67 percent of the city's operating money. Tuesday's session is a presentation only; under the draft, the street plan goes to a planning commission public hearing before any council vote.||The council will also be asked to set a public hearing on an appeal by KPT LLC, a private owner, after the planning commission refused to rezone about 1.45 acres on North Church Street from single-family homes to general commercial use. The land sits next to an elementary magnet school, and at the commission's Oct. 13 meeting neighbors objected that the commercial use was not clearly defined and raised worries about traffic and children's safety. The applicant's engineer said the owners had mentioned a possible unmanned ATM or a butcher shop and promised to keep the school's driveway open.||Also on the agenda: a resolution to go ahead with condemning two run-down buildings on North Church Street that a city inspection calls a hazard; a hearing date on a request to give up a 10-foot alley off West Washington; the first reading of a private club permit, which allows alcohol sales, for Delta Catfish, Grill &amp; Seafood on South Caraway Road; and a proclamation honoring Valley View's state champion girls tennis team. Before the meeting, the council's Public Safety Committee meets at 5 p.m. on the city's application for a federal Justice Department grant that helps pay for police bulletproof vests."))
body.append('<h3>Hytrol 5K/10K draws a record field and $7,000 for the Church Health Center</h3>')
body.append(P("The 30th annual Hytrol 5K/10K in Jonesboro drew a record 255 runners on Saturday, up about 40 percent from 175 last year, and the registration fees raised about $7,000, also a record, for the Jonesboro Church Health Center, which provides care for uninsured and underinsured families. Race coordinator Hannah Freeland had set a goal of more than 200 runners and said she hopes to keep the race growing and make it more family-friendly, with walkers welcome. Justin Depew, second in the men's 10K, credited the area's run clubs with drawing more people to local races."))
body.append("<h3>Children's museum color run meets its goal as backers eye a groundbreaking in about a year</h3>")
body.append(P("The Northeast Arkansas Children's Museum, a nonprofit planning a hands-on museum for children, held a half-mile color run with inflatables and face painting this weekend on its future site at 215 W. Monroe Ave. downtown. Board President Jordan Carlow said late registrations carried the event to its goal of 200 participants, with the money going straight to the museum ahead of a larger fundraising campaign. The city and the museum signed a land-use agreement in September, and Carlow said the plan is to break ground in about a year."))
body.append('<h3>Around town</h3>')
body.append(P("<b>Today:</b> Red Cross blood drives, 10 a.m. to 3 p.m. at Arkansas State University&ndash;Newport's Jonesboro campus, 5504 Krueger Drive, and 9 a.m. to 2 p.m. at Riverside High School in Lake City; November donors get a free A1C blood-sugar test. A Friendsgiving dinner runs 4 to 8 p.m. at Native Brew Works, 515 S. Gee St., $45 a plate, drinks extra, 21 and older to dine in.||<b>Tuesday:</b> another Red Cross blood drive, 10 a.m. to 3 p.m., NYIT Wilson Hall, 2405 Aggie Road. A free community Thanksgiving dinner, dine in or carry out, 6 to 8 p.m. at 3915 E. Nettleton Ave.||<b>Friday:</b> the Food Bank of Northeast Arkansas holds its 19th annual Fill the Food Bank drive, 6 a.m. to 6 p.m., aiming for 400,000 meals; drop-off spots include Harps in Brookland, both Jonesboro Walmart Supercenters, the Walmart Neighborhood Markets on Creek Drive and Harrisburg Road, and Sam's Club. Bring unexpired food in non-glass containers, or text NEAFOOD to 43414 to give.||<b>Friday through Sunday:</b> the 40th Lit'l Bita Christmas arts and crafts show at First National Bank Arena, noon to 7 p.m. Friday, 9 to 6 Saturday and 10 to 4 Sunday; $6 a day or $15 for all three, free parking and Santa daily, with proceeds for A-State athletes' scholarships. <b>Nov. 20&ndash;23:</b> &ldquo;The Nutcracker,&rdquo; presented by the Foundation of Arts at the Forum Theatre, 115 E. Monroe, 7 p.m. Friday, Saturday and Monday with a 2 p.m. Sunday matinee; $22 to $26, 870-935-2726.||<b>Saturday:</b> The Warrior Center's third annual Thanksgiving turkey giveaway, 11 a.m. until they run out, Parker Park, 1506 N. Church St.; one turkey per family, bring a current utility bill."))
body.append('<h2>From the Police Reports</h2>')
body.append('<p class="note">Jonesboro Police incident reports. Charges are allegations. No names are printed.</p>')
body.append(P("The department had posted no new daily incident reports by press time; its shared folder still ends with the reports filed Friday, Nov. 13, which appeared in Saturday's letter. The weekend's reports will appear here once they are released."))
body.append('<div><p class="note" style="break-after:avoid">At the county jails</p>'+P("The Craighead County jail roster listed 315 people held on Monday morning, 15 of them booked in the previous 48 hours; among those listed first, the most common charges were domestic assault or battery, drunk or suspended-license driving, burglary and drug possession. The Randolph County jail at Pocahontas listed 62 inmates, with no new bookings and no releases in the past 48 hours; its most recent booking, early Saturday, was for a second-offense DWI. Charges are allegations, and being on a roster does not mean anyone has been convicted.")+'</div>')
body.append('<h2>From the State</h2>')
body.append("<h3>High schools reshape career classes to match the state's list of well-paying, in-demand jobs</h3>")
body.append(P("Arkansas public high schools are reworking their career-education programs to meet the LEARNS Act, the sweeping 2023 education law signed by Gov. Sarah Huckabee Sanders, which requires every high school to offer a diploma through at least one \"career-ready pathway\" tied to well-paying jobs employers need. For this school year the state Department of Education lists 29 qualifying pathways, among them accounting, agriculture, early childhood education, nursing, welding and military service. Schools may keep other programs, but the state's A-through-F school grades give extra credit only for the listed ones, and middle schools must now offer \"career awareness\" activities such as field trips and guest speakers.||The change followed a state-commissioned review by the University of Arkansas Office for Education Policy, which found that the top 10 high school career programs had little to do with the state's top 10 occupations and industries. Some school leaders are keeping unlisted programs anyway because local employers need the workers; Waldron High School in western Arkansas, for one, is keeping its certified nursing assistant course for nearby nursing homes and a hospital, even if it costs points on the school's grade. Sanders and Education Secretary Jacob Oliva sum up the aim as \"the three E's\": every graduate enrolled in more schooling, enlisted in the military, or employed."))
body.append('<h3>Parole board turns down a hit man but recommends mercy for a man imprisoned 54 years</h3>')
body.append(P("The Arkansas Post-Prison Transfer Board, the state panel that advises the governor on parole and clemency, on Thursday rejected a request to shorten the life sentence of Vonzell Johnson Jr., who pleaded guilty in 1988 to the murder-for-hire shooting of Little Rock used-car dealer Jimmy L. Spears the year before. The board gave no reasons; Johnson, held at the East Arkansas Regional Unit, also faces a separate life sentence in Louisiana.||In another case, the board recommended clemency, a reduced sentence, for Ira Ballard, 77, who has served 54 years of a life sentence for the 1972 shooting deaths of two men at a liquor store on the Arkansas side of Texarkana. Gov. Sanders has the final word and may commute the sentence, shorten it or decline. A similar recommendation the board made in June for another long-serving inmate is still on her desk."))
body.append('<h3>Little Rock School Board to weigh starting its own police force</h3>')
body.append(P("The Little Rock School District, the state's largest urban school system, will decide at Thursday's board meeting whether to replace the 22 city police officers now assigned to its schools with a district-run police department. Safety director William El-Amin says an in-house force would give the district more say over officer policy, as school districts in Fort Smith and Cabot have done. The push follows two incidents, in August 2025 and this September, in which officers used pepper spray inside Central High School to break up a fight and then a crowd, which drew objections from some board members.||El-Amin's plan calls for 12 certified officers at the high schools, armed security guards without arrest powers at the younger grades, and a social worker. The board will also consider two alternatives: keeping the city police contract or partnering with the Pulaski County Sheriff's Office."))
body.append('<h2>From the Nation</h2>')
body.append('<h3>Rocket failure destroys 40 Amazon internet satellites</h3>')
body.append(P("A Vulcan rocket built by United Launch Alliance, the joint venture of Boeing and Lockheed Martin that launches many military and NASA missions, failed about 10 minutes after liftoff from Cape Canaveral, Florida, on Sunday afternoon, and all 40 satellites aboard were lost. The satellites belonged to Amazon Leo, Amazon's planned network of internet satellites meant to compete with SpaceX's Starlink. It was the company's first complete mission failure since it was formed in 2006.||The company said only that the rocket \"suffered an anomaly\" and did not reach orbit; early flight data pointed to trouble around the time the upper stage separated and fired its engine, but the cause is not known. The launch was the first of 38 Vulcan flights Amazon has bought. The rocket is likely to be grounded during the investigation, slowing Amazon's plan for more than 3,300 satellites and possibly delaying military launches that depend on the Vulcan."))
body.append('<h3>Investigators say a tanker\'s rudder stuck before it capsized a New Orleans riverboat</h3>')
body.append(P("The tanker that rammed and rolled over a docked passenger riverboat in New Orleans on Friday had a steering failure moments before the crash, according to the National Transportation Safety Board, the federal agency that investigates major transportation accidents. The ship's voyage data recorder shows its rudder stayed turned to the right, sending the tanker Atlantic Asphalt toward the Mississippi River's east bank. The riverboat American Heritage, with 140 passengers and 50 crew, capsized in about 22 minutes; everyone was accounted for, more than 30 were hurt, and as of Saturday eight were still in the hospital, two seriously.||Investigators have not said why the rudder stuck and expect a preliminary report in about 30 days. The Port of New Orleans has sued the tanker's owner in federal court for at least $1 million, and a federal judge has temporarily placed the ship under federal control."))
body.append('<h3>Days after resigning, former Nvidia chief is reported to be weighing a comeback</h3>')
body.append(P("Jensen Huang, who resigned last week as chief executive of Nvidia, the chipmaker whose processors power much of the artificial-intelligence industry, has discussed returning to the job with close confidants, according to a single report in a British financial newspaper citing unnamed people; neither Huang nor the company has confirmed it. Huang stepped down after reports of extramarital affairs, including one with a woman suspected of ties to Chinese intelligence. Elon Musk and two major shareholders have urged the board to consider all options, including bringing him back, while Treasury Secretary Scott Bessent said Sunday that Nvidia should look outside the company.||The board says it is conducting an independent investigation and has begun a search for a new chief. Interim CEO Colette Kress, the longtime finance chief, will face investors when Nvidia reports quarterly earnings on Tuesday."))
body.append("<h3>Democrat wins Alaska's governorship for the first time since 1998</h3>")
body.append(P("Jonathan Kreiss-Tomkins, 37, a Democrat and former state lawmaker, won the race for governor of Alaska outright, according to a race call by The Associated Press early Saturday; he took a majority of first-choice votes, so the state's ranked-choice counting was not needed. He defeated three Republicans, including Anchorage businesswoman Bernadette Wilson, whom President Trump backed, and had the endorsement of Republican U.S. Sen. Lisa Murkowski. He will succeed term-limited Republican Gov. Mike Dunleavy as the youngest governor in the state's history, after a campaign for more school money, lower energy costs, expanded Medicaid and a pause on new data centers until lawmakers write rules for them. Democrats are set to hold 30 governorships next year."))
body.append('<h3>Richard Sterban, the bass voice of the Oak Ridge Boys, dies at 83</h3>')
body.append(P("Richard Sterban, whose deep \"oom-papa-mow-mow\" made the Oak Ridge Boys' 1981 hit \"Elvira\" a country classic, died Saturday at his home in Hendersonville, Tennessee, at 83, of complications from bronchitis and pneumonia after a long fight with cancer, his family and the group said. He joined the country and gospel quartet in 1972 after singing backup for Elvis Presley, and the group went on to 17 No. 1 country singles and the Country Music Hall of Fame in 2015. Funeral plans have not been announced."))
body.append('<h2>From Abroad</h2>')
body.append('<h3>Estonia will close its border crossings with Russia after a foiled sabotage plot</h3>')
body.append(P("Estonia, a small NATO country on Russia's western border, said Sunday it will close its road crossings with Russia starting Dec. 1, after a failed arson attack early Saturday on Threod Systems, an Estonian maker of military drones. Foreign Minister Margus Tsahkna said there is \"clear evidence\" the attack was ordered by the GRU, Russia's military intelligence agency; eight people were detained, and the company's own security stopped the fire before it did serious damage.||Prime Minister Kristen Michal called it part of Russia's \"hybrid war\" on Europe, meaning sabotage and other attacks short of open warfare, and said, \"We will not be intimidated.\" Russia did not answer the accusation directly; a Kremlin spokesman said \"Estonia is building walls,\" and the Foreign Ministry called the move \"Russophobia.\" No date has been set for reopening."))
body.append('<h3>Trump is reported to be weighing a pause on new strikes against Iran</h3>')
body.append(P("President Trump has privately told senior advisers he may hold off on new attacks on Iran as long as neither Iran nor the Iran-backed Houthi militia in Yemen provokes the United States again, according to a single news-agency report citing three unnamed people, who said he has made no commitment either way. The U.S.-Iran war, which Trump launched with Israel in February, has driven up fuel prices around the world. Saudi Crown Prince Mohammed bin Salman and Turkish President Recep Tayyip Erdogan have both reportedly urged restraint. A White House official said only Trump knows \"what he will do, and when,\" and a third U.S. aircraft carrier group is moving into the region. Iran, for its part, told the U.N. nuclear watchdog it will not discuss resuming inspections while under U.S. threat."))
body.append('<h3>Saudi Arabia says it shot down Houthi missiles aimed at Riyadh</h3>')
body.append(P("The Saudi-led military coalition fighting in Yemen said Sunday it intercepted two ballistic missiles fired at Riyadh, the Saudi capital, by the Houthis, the Iran-backed rebels who control much of northern Yemen, and three drones headed for the kingdom's oil-producing Eastern Province. The account comes only from the coalition; the Houthis did not claim the launches, and no casualties were reported. Saudi officials say at least 26 people have been killed in suspected Houthi attacks inside the kingdom since Sept. 23, and the U.S. Embassy in Riyadh has issued a nationwide security alert."))
body.append('<h3>Israel kills a Hamas commander in southern Gaza as the truce frays</h3>')
body.append(P("Israel's military said a drone strike on Saturday killed Samir Abu Younis, commander of Hamas' Rafah Brigade, one of the militant group's main fighting units, and Hamas confirmed his death. The strike hit a tent for displaced people in al-Mawasi, a crowded coastal area near Khan Younis, wounding two others. A ceasefire that took effect in October 2025 is nominally in place, but Gaza's Hamas-run Health Ministry says at least 1,643 Palestinians have been killed since then; Israel says its strikes target militants who break the truce. The European Union has called for open aid access after winter storms flooded tent camps."))
body.append('<h3>Zelensky says satellite limits are hurting the defense of Ukraine\'s power grid</h3>')
body.append(P("Ukrainian President Volodymyr Zelensky said Sunday that speed limits on Starshield terminals, the military version of SpaceX's Starlink satellite internet, keep Ukraine's interceptor drones from catching Russian attack drones before they hit power stations, since the terminals lose connection above about 100 mph while the Russian drones fly 185 to 250. He said Russia launched more than 2,300 attack drones at Ukraine in the past week. Responsibility is disputed: Elon Musk has said the U.S. government controls the settings, the Pentagon said in October it ordered no limits, and SpaceX called claims of renewed limits \"false.\""))
body.append('<h3>Southeast Asian leaders keep Myanmar\'s generals at arm\'s length as their summit opens</h3>')
body.append(P("Leaders of the Association of Southeast Asian Nations, a 10-country regional bloc, opened their annual summit in Manila, the Philippine capital, this weekend and agreed for now to keep barring the leaders of Myanmar's military government, which seized power in a 2021 coup and has been fighting a civil war since, from top-level meetings. They are also discussing a long-sought code of conduct with China for the disputed South China Sea, though finishing it this week looks unlikely, and ways to cope with fuel prices pushed up by the Iran war. President Trump is expected to attend before going on to China."))
body.append('<div style="break-inside:avoid;page-break-inside:avoid"><h2>Markets &amp; the Farm</h2><p class="note">Figures are as of Friday&rsquo;s close, November 13. Week changes are from Friday, November 6.</p><table class="mk"><tr><th>Index</th><th>Close</th><th>Day</th><th>Week</th></tr><tr><td>S&amp;P 500</td><td class="n">7,561.67</td><td class="n">&minus;0.40%</td><td class="n">+2.51%</td></tr><tr><td>Dow Jones Industrials</td><td class="n">52,347.55</td><td class="n">+0.10%</td><td class="n">+2.07%</td></tr><tr><td>Nasdaq Composite</td><td class="n">25,136.27</td><td class="n">&minus;0.91%</td><td class="n">+2.27%</td></tr></table></div>')
body.append(P("Chip stocks kept sliding Friday after Jensen Huang's resignation from Nvidia, but all three indexes still finished their best week since August. Stock futures pointed lower early Monday, led by technology shares, as chipmakers sold off in Asia. The week's big tests are Nvidia's earnings on Tuesday, the minutes of the Federal Reserve's October meeting on Wednesday, and reports from Walmart, Target, Home Depot and Lowe's, which will show how shoppers are holding up heading into the holidays."))
body.append('<h3>What analysts are saying</h3>')
body.append('<ul class="picks"><li><b>Analysts leaned toward buying: NUE</b> (Nucor, the largest U.S. steelmaker). UBS upgraded it to buy on Monday morning, expecting steel prices to stay higher for longer, with order backlogs running into mid-2027 and strong cash flow ahead. Risk: UBS itself expects steel prices to ease over time, and imports could pick up. <i>(Single source: Investing.com.)</i></li><li><b>Analysts leaned toward buying: COLD</b> (Americold Realty, which owns and runs refrigerated warehouses for food). Piper Sandler upgraded it on Friday, citing a turnaround under new management that began in April and shares still cheap next to other warehouse owners. Risk: the turnaround is young, and fuel costs and food-storage demand can squeeze results.</li><li><b>Analysts leaned toward buying: DECK</b> (Deckers Outdoor, maker of Hoka running shoes and Ugg boots). StoneX began coverage Friday with a buy rating, pointing to growth at both brands and a solid balance sheet; the stock rose about 4 percent. Risk: most analysts still rate it only a hold, and footwear sales depend on how freely shoppers spend.</li><li><b>Analysts turned cautious: TSCO</b> (Tractor Supply, the farm-and-ranch retail chain familiar to every country road in Arkansas). Evercore ISI cut it to the equivalent of a hold on Friday after its survey found only 37 percent of households plan a home project in the next year, down from 49, and said future earnings growth would lean mostly on share buybacks. Risk to this view: steady rural demand and buybacks could still lift results.</li><li><b>Analysts turned cautious: YETI</b> (Yeti, maker of coolers and drinkware). Goldman Sachs cut it to neutral on Monday, citing a more meaningful slowdown in its U.S. direct-to-customer sales. Risk to this view: a strong holiday season could prove the call too gloomy. <i>(Single source: CNBC.)</i></li></ul>')
body.append('<p class="note">This is information about what analysts said, not advice to buy or sell.</p>')
body.append('<h3>Commodities</h3>')
body.append('<table class="mk split"><tr><th>Commodity</th><th>Close</th><th>Change</th></tr><tr><td>WTI crude (Dec.)</td><td class="n">$88.56</td><td class="n">&minus;$0.18</td></tr><tr><td>Brent crude (Jan.)</td><td class="n">$95.84</td><td class="n">+$0.02</td></tr><tr><td>Arkansas avg. regular gas (AAA, Nov. 12)</td><td class="n">$3.55</td><td class="n">&minus;16&cent; on week</td></tr><tr><td>Jonesboro metro avg. gas (AAA, Nov. 12)</td><td class="n">$3.48</td><td class="n">&minus;15&cent; on week</td></tr><tr><td>Live cattle (Dec.), per cwt</td><td class="n">$220.65</td><td class="n">+$1.75</td></tr><tr><td>Feeder cattle (Jan.), per cwt</td><td class="n">$335.35</td><td class="n">+$3.67</td></tr><tr><td>Lean hogs (Dec.), per cwt</td><td class="n">$55.45</td><td class="n">+$0.30</td></tr><tr><td>Corn (Dec.), per bu.</td><td class="n">$4.43&frac12;</td><td class="n">+3&cent;</td></tr><tr><td>Soybeans (Jan.), per bu.</td><td class="n">$12.31&frac12;</td><td class="n">+12&frac12;&cent;</td></tr><tr><td>Wheat, Chicago (Dec.), per bu.</td><td class="n">$5.93&frac14;</td><td class="n">+9&cent;</td></tr><tr><td>Rough rice (Jan.), per cwt</td><td class="n">$18.39</td><td class="n">&minus;26&frac12;&cent;</td></tr><tr><td>Cotton (Dec.), per lb.</td><td class="n">78.78&cent;</td><td class="n">+0.11&cent;</td></tr></table>')
body.append('<p class="note">Commodities as of Friday&rsquo;s close. Oil fell about 2.5% on the week and was a little lower again in overnight trading. Livestock: single source (Brownfield); soybeans, wheat and rice confirmed by government settlement reports; one such report put December corn about 2&cent; higher. Gasoline: AAA Arkansas, Nov. 12, single outlet (KAIT).</p>')
body.append('<h2>On the Field</h2>')
body.append(P('<b>Arkansas State</b> football (4&ndash;6, 2&ndash;4 Sun Belt) goes to Louisiana Tech on Saturday, 6 p.m. at Joe Aillet Stadium in Ruston, Louisiana, streamed on ESPN+. With Troy coming to Jonesboro to close the season the week after, the Red Wolves must win both games to reach six wins and a fourth straight bowl trip.'))
body.append(P('<b>A-State men&rsquo;s basketball</b> (2&ndash;2) finishes a three-game home stand Wednesday at 7 p.m. against Arkansas&ndash;Pine Bluff at First National Bank Arena, on ESPN+ and the Red Wolves radio network, then heads to Miami next week for three games in a Thanksgiving tournament, Nov. 23&ndash;25, against Southern Utah, Long Beach State and host FIU.'))
body.append(P('<b>Arkansas</b> (4&ndash;6, 2&ndash;5 SEC), fresh off the 34&ndash;6 rout of South Carolina, plays at Texas (8&ndash;2) on Saturday at 2:30 p.m., on ABC or ESPN, with the network to be named. The Razorbacks must beat both Texas and LSU the following week to become bowl-eligible.'))
body.append(P('<b>Tennessee</b> (8&ndash;2, 5&ndash;2 SEC) plays its final home game Saturday against LSU at Neyland Stadium, 2:30 p.m. Central on ABC, and closes the regular season at Vanderbilt on Nov. 28. The new College Football Playoff rankings, in which the Vols stood eighth last week, come out Tuesday night.'))
body.append('<h2>Afield &amp; Afloat</h2>')
body.append('<p class="note">Ratings are rule-of-thumb estimates from the forecast, the rut calendar and the sun, not measurements of animal or fish behavior.</p>')
body.append('<h3>Deer outlook: Good</h3>')
body.append(P("The rut is still near its peak in north Arkansas, dawn is a frosty 34 degrees, and the barometer is high and steady after the weekend's front, all of which favor movement. Windows: about 6:10 to 8:40 a.m.; 10 a.m. to 2 p.m. is realistic with bucks cruising for does; and 2:54 p.m. to sunset at 4:54. <b>Today's tip:</b> after an opening weekend of orange in the woods, mature deer slip into the thickest cover they can find. On this first weekday of the season, with fewer hunters out, sit the edge of a thicket, a cutover or a briar-choked drain where pressured deer go to ground, and stay put through midday; with a light breeze of 6 to 9 mph, check its direction before you walk in and set up downwind of where the deer will be."))
body.append(P("<b>Tomorrow, Tuesday (estimate: Good).</b> Another frosty dawn near 34 under clear skies, almost no wind (4 to 6 mph) and a barometer easing slowly through the day. Windows: about 6:11 to 8:41 a.m., 10 a.m. to 2 p.m., and 2:53 p.m. to sunset at 4:53. <b>Tomorrow's tip:</b> on a still morning, cold air drains downhill and carries your scent with it, so hunt above the deer early, on a ridge or the high side of a bottom, and come back down the slope for the evening sit when the warming air rises. Zone 4 hunters have just through Sunday left in the modern gun season, so make the calm days count."))
body.append('<h3>Fishing outlook: Good</h3>')
body.append(P("A sunny afternoon near 58, steady pressure and a light chop on the water should get fish moving on Craighead Forest Lake and Lake Frierson. Best times: late morning through mid-afternoon as the water warms, and again in the last hour before the 4:54 sunset. <b>Today's tip:</b> as the lakes cool, crappie bunch up on brush piles and standing timber in roughly 8 to 15 feet of water; fish a small jig or a minnow slowly straight down into the cover, and when you catch one, stay on that spot, because there are usually more."))
body.append(P("<b>Tomorrow, Tuesday (estimate: Excellent).</b> The best day of the two: a warmer afternoon near 62, steady pressure with a slow fall ahead of the next weather, and a light breeze. Best times: late morning to mid-afternoon and the last hour before the 4:53 sunset. <b>Tomorrow's tip:</b> bass will slide up onto the banks that have soaked up the sun since morning, often the north bank, which faces south; work a spinnerbait or a shallow crankbait slowly along wood and rock there in the afternoon. For a family outing, the state's community fishing program stocks trout from November through February in its ponds, including the Youth and Senior Pond at Craighead Forest."))
body.append('<h3>In season now, and what is next (zones 3, 4, 6 and 8)</h3>')
body.append('<table class="mk"><tr><th>Zone</th><th>Archery</th><th>Youth gun</th><th>Modern gun</th><th>Muzzleloader</th></tr>\n<tr><td>3</td><td>open to Feb. 28</td><td>Jan. 2&ndash;3</td><td>open to Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr>\n<tr><td>4</td><td>open to Feb. 28</td><td>Jan. 2&ndash;3</td><td>open to Nov. 22; Dec. 26&ndash;28</td><td>no season</td></tr>\n<tr><td>6</td><td>open to Feb. 28</td><td>Jan. 2&ndash;3</td><td>open to Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr>\n<tr><td>8</td><td>open to Feb. 28</td><td>Jan. 2&ndash;3</td><td>open to Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr></table>')
body.append(P("<b>Modern gun season is open</b> in all four zones. In Zone 4, which takes in Craighead County, it closes this Sunday, Nov. 22, with only one antlerless deer allowed by modern gun; Zones 3, 6 and 8 run to Dec. 6, and all four reopen for the holiday hunt Dec. 26&ndash;28. The season limit in all four zones is four deer, no more than two of them bucks. Archery stays open to the end of February. Every deer must be checked in by the Game and Fish app, at agfc.com or by phone.||<b>Duck season opens Saturday, Nov. 21,</b> with the first segment running through Nov. 29 (not Dec. 1, as some published guides misprinted), then Dec. 10&ndash;23 and Dec. 26 to Jan. 31; Canada geese and white-fronted, snow, blue and Ross's geese follow the same three segments. Quail is open on private land through Feb. 7 with a daily limit of six, and squirrel and rabbit remain open well into winter; check agfc.com for the rules on any wildlife management area you plan to hunt."))
body.append('<h2>Postscript</h2>')
body.append('<p class="ps">No warmth, no cheerfulness, no healthful ease,<br>&nbsp;&nbsp;No comfortable feel in any member&mdash;<br>No shade, no shine, no butterflies, no bees,<br>&nbsp;&nbsp;No fruits, no flowers, no leaves, no birds,&mdash;<br>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;November!</p>')
body.append('<p class="ps">&mdash; Thomas Hood, the closing lines of &ldquo;No!&rdquo; (1840s). Hood&rsquo;s catalog of November gloom is a fine thing to read with a week of sunshine and 70 degrees ahead; Northeast Arkansas may claim an exception.</p>')
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
