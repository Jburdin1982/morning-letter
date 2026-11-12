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
body.append('<div class="date">Thursday, the Twelfth of November, 2026</div><div class="orn">&#10086;</div>')
body.append(P('Good morning,'))
body.append(P("Thursday brings one last mild, sunny afternoon in the low 60s before a cold front drops tonight toward the mid 30s; Friday and Saturday stay in the low 50s with frost likely by Saturday dawn. At home, the city&rsquo;s new ban on camping in parks has put a spotlight on Jonesboro&rsquo;s single 16-bed shelter just as the Salvation Army&rsquo;s red kettles come out Friday, and Cooksey&rsquo;s Flower Shop is closing after 74 years. Farther off, Indonesia&rsquo;s vice president has resigned, Congo&rsquo;s Ebola outbreak has passed 11,000 cases, and modern gun deer season opens Saturday."))

body.append('<h2>The Day Ahead</h2>')
body.append(hourly); body.append(grid)
body.append(P("Thursday opens near 48 degrees at 6 a.m. and climbs quickly under a sunny sky, to about 56 by 9 o&rsquo;clock and 62 from noon through mid-afternoon, with no rain in the forecast. The breeze is light this morning and picks up to around 13 miles an hour toward evening as the front arrives. After sunset the temperature slides to about 47 by 9 p.m. and toward 35 by morning.||Friday dawns near 33, and although the sun shines all day, the high reaches only about 52. Friday night is the coldest of the week, near 30, so expect a white frost on the grass and windshields Saturday morning. The weekend stays dry and bright with highs in the low to mid 50s, and the week ahead warms gently toward 60 by Wednesday with hardly a cloud of rain in sight."))

body.append('<h2>The Almanac</h2>')
body.append(f'''<table class="alm"><tr><td>First light</td><td>{alm['first_light']}</td><td>Sunrise</td><td>{alm['sunrise']}</td></tr>
<tr><td>Solar noon</td><td>{alm['noon']}</td><td>Sunset</td><td>{alm['sunset']}</td></tr>
<tr><td>Last light</td><td>{alm['last_light']}</td><td>Length of day</td><td>{alm['day_length']}</td></tr>
<tr><td>Change from yesterday</td><td>{alm['change'].replace('-','&minus;')}</td><td>Moon</td><td>{alm['moon']}, {alm['illum']}% lit</td></tr></table>''')
body.append(P("A thin young moon, only three days past new, sets early this evening in the southwest, so the nights are dark and the stars sharp after the front clears the air; first quarter comes around next Tuesday. The day is now ten hours and twenty minutes long, and we lose nearly two minutes of it every day."))
body.append(P("This is the week the fields along the St. Francis and the Cache turn to stubble and water. Rice ground is being flooded for the ducks that will be welcome on the 21st, and the cotton pickers are working the last of the late fields. On Crowley&rsquo;s Ridge the oaks have gone to rust and the sweetgums to wine, and a good wind will bring most of them down by Thanksgiving. Pecans are dropping in the yards; gather them before the squirrels do, and dry them a week or two in a shallow box before cracking.||In the garden, the front is the signal to finish: cut back the asparagus ferns, pull the frost-blackened peppers, and spread a few inches of chopped leaves over the bare beds. Collards, kale and turnip greens will shrug off a frost and taste the sweeter for it. Indoors, it is a fine week to check the furnace filter and the smoke-alarm batteries before the heater runs in earnest."))
body.append(P("<i>Weather lore, not a forecast:</i> the old fishermen held that &ldquo;when the wind is in the north, the skillful fisher goes not forth.&rdquo; Behind tonight&rsquo;s front, the lakes may well prove them right on Friday."))

body.append('<h2>Of Local Interest</h2>')
body.append('<h3>Park camping ban leaves the homeless few places to turn</h3>')
body.append(P("Jonesboro&rsquo;s new rule against camping in city parks is drawing attention to how few places the city&rsquo;s homeless residents have to sleep as cold weather settles in. On Nov. 5 the City Council voted 10 to 0 for Ordinance 26-038, which forbids putting up tents or shelters, or bedding down overnight, in any city park or city-owned parking lot outside a designated camping area; Craighead Forest Park holds the designated campground. Police or code-enforcement officers may remove a camper&rsquo;s belongings, and a first offense carries a fine of at least $100.||Dr. Charles Coleman, who has represented Ward 2 on the council for nearly 15 years, said the matter was raised months ago over safety concerns, including trouble around parked cars and people camping without permission. Maj. Jon-Phil Winter, who commands the Salvation Army on Cate Avenue, said he understands those concerns but called homelessness a complicated problem tied to addiction, health and money, and urged the community to help people out of it. The Salvation Army runs Jonesboro&rsquo;s only emergency shelter: 16 beds, for men only, open nightly from 5 p.m. to 8 a.m. It cannot take women and children because it lacks the staff and money to do so safely.||Neighbors are stepping in. Karleigh Johns, who owns Hunter&rsquo;s Loaded Lemonade, a food truck named for a late brother, is collecting jackets, gloves, blankets and rain ponchos through Dec. 5, to be handed out that day at the second annual Hunter&rsquo;s Holiday Market at Gamble&rsquo;s Shop Local Park, where more than 70 vendors and 10 food trucks have signed up."))
body.append('<h3>Red kettles return Friday</h3>')
body.append(P("The Salvation Army of Jonesboro begins its yearly Red Kettle Campaign on Friday, Nov. 13, with bell-ringers out through Christmas Eve and a goal of $100,000. The money pays for the charity&rsquo;s year-round work, including that overnight shelter, community meals and a food pantry; Maj. Winter calls it the group&rsquo;s biggest fundraiser of the year. Volunteers are needed at about 15 spots across Northeast Arkansas, among them Walmart, Kroger, Hobby Lobby and Belk, in four-hour shifts from 10 a.m. to 2 p.m. or 2 to 6 p.m.; children must ring with an adult. Cash, checks and digital payments are all accepted, and the Angel Tree Christmas program for children opened Thursday."))
body.append('<h3>Cooksey&rsquo;s Flower Shop closing after 74 years</h3>')
body.append(P("Cooksey&rsquo;s Flower Shop, which has made Jonesboro&rsquo;s corsages, wedding bouquets and holiday arrangements since the early 1950s, is closing for good. The family says the decision came after Henry Cooksey&rsquo;s wife was diagnosed with cancer, and Mr. Cooksey says he needs to be at her side. The shop was founded by the parents of the present generation and later run by Henry and Janelle Cooksey; it has already been closed for a while. A final sale is planned, with details still being worked out. In thanking the town, the family said its customers had been &ldquo;as much friends as you have customers.&rdquo;"))
body.append('<h3>Two seriously hurt in head-on crash on Nestle Road</h3>')
body.append(P("Two people were seriously injured about 6:30 Wednesday morning in a head-on collision between a GMC Acadia and a Ford F-250 pickup on Nestle Road near the Camfil plant, according to Jonesboro Police spokeswoman Sally Smith. The pickup&rsquo;s driver was flown to Regional One Health, the trauma hospital in Memphis, and the SUV&rsquo;s driver was taken to a Jonesboro hospital. Nestle Road was closed for a time between C.W. Post Road and Interstate 555. Police have not released the drivers&rsquo; names or said what caused the crash."))
body.append('<h3>A new playground built for every child</h3>')
body.append(P("City officials cut the ribbon Tuesday on a rebuilt playground at University Heights Lions Club Park on North Bridge Street, designed so children with disabilities can play alongside everyone else. It has a paved walkway, artificial turf that wheelchairs can roll across, and a rope-climbing feature that lets children who cannot walk still reach the slides. Parks and Recreation Director Jim Stearns said the park had fallen into disrepair before work began in October 2025: &ldquo;We want to make it inclusive where everybody has access regardless of their ability or disability.&rdquo; Mayor Harold Copenhaver spoke as well; another inclusive park is planned on Disciple Drive."))
body.append('<h3>Schoolchildren and seniors honor veterans</h3>')
body.append(P("About 55 veterans came to the fifth annual Veterans Day ceremony at Jonesboro&rsquo;s International Studies Magnet School on Wednesday. The speaker was Tim Doyle, a retired sergeant first class in the Army National Guard who served in Iraq in 2006 and 2007 and is the husband of Superintendent Misty Doyle; he told the students that &ldquo;small things make a difference.&rdquo; Fifth graders sang &ldquo;Our Heroes,&rdquo; senior Ava Fitzgerald sang the national anthem, and students pinned America 250 pins on veterans in their own families.||At South Wind Heights, an independent-living community, more than 80 residents and veterans shared a hamburger lunch and live music, and eight residents put on boxing gloves for friendly rounds with a coach; no one was hurt. &ldquo;I don&rsquo;t let anybody hold me back if I want to do something,&rdquo; said resident Connie Latham. South Wind Heights is serving one free meal a day to veterans and their spouses through the end of November."))
body.append('<h3>A-State leadership center turns 10 and asks for mentors</h3>')
body.append(P("Arkansas State University&rsquo;s Center for Leadership Excellence, founded on Nov. 10, 2016, by Kathy White Loyd and 28 other women to prepare students for careers and leadership, marked its tenth birthday this week. Its interns have received more than 145 scholarships, and about 100 students signed up for mentoring this semester, more than the center can easily match. Its &ldquo;Step Up, Reach Back&rdquo; program asks a volunteer for one hour a month in an online session with a small group of students; those interested may write to cle@astate.edu. Separately, five A-State students, among them Logan Cathey of Jonesboro, were named to the 2027 Arkansas Collegiate Civic Leadership Academy, a year-long public-service program of the Winthrop Rockefeller Institute."))
body.append('<h3>Around town</h3>')
body.append(P("<b>Space heaters:</b> with cold nights ahead, Brookland Assistant Fire Chief John Burns asks families to keep anything that can burn at least three feet from a space heater, to plug heaters straight into the wall rather than an extension cord, and to have a wood fireplace swept before its first fire. <b>Friday, Nov. 13:</b> Elks Lodge 498, 2113 W. Washington Ave., serves a pasta Veterans Dinner at 6 p.m., free to veterans and spouses and $10 for others; reservations are required. <b>Saturday, Nov. 14:</b> the Judd Hill Farmers Market on Aggie Road opens the first of three winter holiday markets, 9 a.m. to 2 p.m. (the others are Nov. 21 and Dec. 19). <b>Sunday, Nov. 15:</b> Together We Foster takes donations for foster children from 2 to 4 p.m. at 1400 E. Washington Ave.: coats, suitcases and duffel bags, new socks and underwear, winter clothes in all sizes, and new toys.||<b>Monday, Nov. 16:</b> the Northeast Arkansas Chorale sings its Christmas concert, &ldquo;The Arrival,&rdquo; at 7 p.m. in Manley Chapel at Williams Baptist University in Walnut Ridge; $10, or $20 a family. <b>Friday, Nov. 20:</b> the Food Bank of Northeast Arkansas holds its 19th &ldquo;Fill the Food Bank&rdquo; drive from 6 a.m. to 6 p.m., with drop-offs at Harps in Brookland and at Jonesboro&rsquo;s four Walmarts and Sam&rsquo;s Club. <b>Sunday, Dec. 6:</b> Brookland&rsquo;s 25th Christmas Parade steps off at 2 p.m., lining up at Brookland High School; no registration is needed."))
body.append('<h3>Our neighbors farther afield</h3>')
body.append(P("<b>Paragould:</b> a Paragould man, Steven Van Sickle, 55, charged with first-degree murder in the September shooting death of his roommate on East Court Street, will go to trial the week of Dec. 14. He pleaded not guilty on Oct. 29, and the charge is an accusation not yet proven in court. Greene County Circuit Judge Pam Honeycutt has set a plea and motions hearing for Dec. 2."))
body.append(P("<b>Manila:</b> the Manila Food Pantry, which serves more than 200 families in Mississippi County, must leave its building by the end of the year after the building was sold. Founder Angie Masters and board member Aimee McLaughlin say need is growing. A donated house is already full of clothing and may not bear the weight of refrigerators, so the pantry is asking for temporary space, volunteers and donations while it plans a new building on the lot next door."))
body.append(P("<b>West Memphis:</b> Dr. Derek Moore, most recently president of New Mexico Junior College and earlier an associate vice chancellor at ASU Mid-South, has been named chancellor of that two-year college of the Arkansas State University System. He was one of four finalists from 60 applicants."))

body.append('<h2>From the Police Reports</h2>')
body.append('<p class="note">Jonesboro Police incident reports. Charges are allegations. No names are printed.</p>')
body.append(P("No new incident reports have been posted since the batch summarized in yesterday&rsquo;s letter, so there is no blotter this morning. For a serious crash on Wednesday morning, see the Nestle Road item above."))
body.append('<div style="break-inside:avoid;page-break-inside:avoid"><p class="note">At the county jails</p>'+P("In Craighead County, the sheriff&rsquo;s roster shows 293 people held, 13 of them booked in the last 48 hours; among those listed first, the most common charges are failure to appear, drug possession, driving on a suspended license and battery or assault, along with parole violations and a firearm-possession charge. In Randolph County, 64 people are held; four were booked Tuesday and none since, and no releases are listed for the last 48 hours. The newest bookings involve a warrant, a second-offense drunken-driving arrest and criminal trespass. Being on a roster is not a conviction.")+'</div>')

body.append('<h2>From the State</h2>')
body.append('<h3>Former prison chief tells lawmakers the tools are already in hand</h3>')
body.append(P("Joe Profiri, who formerly ran the Arkansas Department of Corrections and now advises Gov. Sarah Huckabee Sanders, told a joint meeting of the House and Senate Judiciary Committees on Tuesday that the state already has the laws it needs to ease prison crowding. &ldquo;At this point it&rsquo;s largely about executing,&rdquo; he said, urging a shift &ldquo;from punitive to rehabilitative.&rdquo; It was his first appearance before legislators since 2025; he lost the corrections job after a public fight with the state Board of Corrections over adding prison beds without adding guards, and lawmakers had talked in September of subpoenaing him.||Profiri said the state has added about 1,500 beds, yet nearly 3,000 people sentenced to prison are again waiting in county jails for a bed. Marshall Clement of the Council of State Governments Justice Center, a nonprofit that advises states, told the committees that Arkansas sends a larger share of people to prison for breaking probation or parole rules than almost any other state, and suggested using the six community correction centers, lower-security residential sites, for the last months of some sentences. Lawmakers heard that the prison population could grow by about 5,000 over the next decade at a cost of roughly $2 billion. The governor&rsquo;s proposed 3,000-bed prison in Franklin County remains on hold; more hearings are expected before the session opens in January."))
body.append('<h3>University report grades Arkansas schools</h3>')
body.append(P("Researchers at the University of Arkansas Department of Education Reform, led by department head Harry Anthony Patrinos, have released a book-length report, &ldquo;The State of Education in Arkansas,&rdquo; weighing the LEARNS Act, the governor&rsquo;s 2023 overhaul of state school law, and the 2025 ACCESS Act. They found the state still trails the nation in educational attainment, and that fourth-grade reading and eighth-grade math slipped against other states on the national exam called the Nation&rsquo;s Report Card. On the state&rsquo;s own test, the share of students scoring proficient rose from 36.9 percent in 2025 to 42.2 percent this year.||The report urges five priorities: affordable, high-quality early childhood education; better pay and mentoring for teachers; public dashboards linking school and workforce data; more advanced math and career pathways; and more help with attendance and mental health. It praises the fast growth of Education Freedom Accounts, the state program that pays private-school and homeschool costs for 51,573 students this year, but calls for careful study of its effects on learning, public schools and the budget. State Rep. Jessie McGruder, a Marion Democrat and West Memphis teacher, said he worries about the program&rsquo;s long-term cost."))
body.append('<h3>Sultana museum reopens Saturday in Marion</h3>')
body.append(P("The Sultana Disaster Museum in Marion, about an hour southeast of Jonesboro, reopens Saturday in the restored 1938 Marion High School gymnasium on Military Road, after a preview Friday for descendants of those aboard. The museum remembers the worst maritime disaster in American history: early on April 27, 1865, the overloaded steamboat Sultana, built for 376 people but carrying nearly 2,000 Union soldiers just freed from Confederate prison camps, exploded on the Mississippi above Memphis. The museum honors almost 1,200 dead; some counts run higher. The wreck lies under a soybean field on the Arkansas side.||The renovation began in March 2025 and cost about $11 million, said John Fogleman, president of the Sultana Historical Preservation Society; FedEx and Hartford Steam Boiler each gave $1 million. The museum opened in 2015 in an 800-square-foot room. &ldquo;It is going to blow people away,&rdquo; Mr. Fogleman said."))

body.append('<h2>From the Nation</h2>')
body.append('<h3>White House warns Democrats their investigations could be &ldquo;criminality&rdquo;</h3>')
body.append(P("White House counsel Will Scharf, the president&rsquo;s chief in-house lawyer, sent a letter Monday to Rep. Robert Garcia of California, the senior Democrat on the House Oversight Committee and its expected chairman when Democrats take control of Congress in January. The letter warns that threatening executive-branch officials, or using legal demands &ldquo;designed merely to abuse or instill fear,&rdquo; could amount to &ldquo;blatant criminality.&rdquo; Oversight of the executive branch is one of Congress&rsquo;s ordinary powers.||Mr. Garcia replied that the letter suggests the president &ldquo;has something to hide&rdquo; and that Congress needs no &ldquo;permission of the White House&rdquo; to investigate. Democrats have said they plan to examine the growth of the Trump family&rsquo;s wealth, the handling of the Jeffrey Epstein investigation, immigration enforcement, the White House ballroom project, and the president&rsquo;s cryptocurrency and mineral dealings; the White House denies wrongdoing. Attorney General Todd Blanche first told CNN there &ldquo;could be&rdquo; a crime if Democratic rhetoric turned threatening, then said the Justice Department would work with Congress through ordinary subpoenas and letters."))
body.append('<h3>At Arlington, Trump defends his war policy and his planned arch</h3>')
body.append(P("President Trump laid a wreath at the Tomb of the Unknown Soldier at Arlington National Cemetery on Veterans Day with Vice President JD Vance, then spent much of his speech defending his use of force abroad, including the conflict with Iran and operations involving Venezuela, and praising Defense Secretary Pete Hegseth, who drew applause. He also honored individual veterans, among them a 103-year-old veteran of the Second World War.||Mr. Trump said he would dedicate to veterans his planned 250-foot &ldquo;triumphal arch,&rdquo; topped by a gold statue of Liberty, on Memorial Circle between the Lincoln Memorial and the cemetery. A federal planning commission approved the design Nov. 5, but U.S. District Judge Tanya Chutkan has temporarily blocked construction while lawsuits proceed, brought by Vietnam veterans, the District of Columbia, Virginia and, this week, nine members of the Kennedy family, whose relatives are buried at Arlington. Critics say the arch would overshadow the memorial and the cemetery."))
body.append('<h3>Immigration arrests go on at full pace</h3>')
body.append(P("Federal immigration arrests have not slowed since last week&rsquo;s election, even though President Trump said in a &ldquo;60 Minutes&rdquo; interview recorded Friday that his approach may have been &ldquo;too tough&rdquo; and that he would &ldquo;love to do something on immigration&rdquo; with Democrats. Homeland Security Secretary Markwayne Mullin, the former Oklahoma senator, says his orders have not changed and deportations will continue through the holidays. Advocates report arrests in California, Michigan, Massachusetts, Florida and elsewhere; Immigration and Customs Enforcement has released no numbers. Cases drawing attention include the detention of 19-year-old twin soccer players at Wallace State Community College in Alabama, whose relatives say they have pending asylum cases and work permits, and of an 8-year-old Haitian boy in San Diego. Hard-line Republicans have warned the White House against softening."))
body.append('<h3>Proposed food-stamp rule would drop millions by 2029</h3>')
body.append(P("The Agriculture Department has proposed a rule that its own analysis says would remove about 6.3 million people from SNAP, the federal food-assistance program once called food stamps, by 2029, and end automatic free school meals for about 1.8 million children. The rule targets &ldquo;broad-based categorical eligibility,&rdquo; used by more than 40 states, which lets families with incomes a little over the normal limit qualify if they receive certain non-cash help such as child-care aid or job training; only families receiving cash welfare would still qualify that way. The administration says the change stops benefits to households with too much income and too many assets; Rep. Angie Craig of Minnesota, top Democrat on the House Agriculture Committee, called it &ldquo;heartless and cruel.&rdquo; A similar rule was proposed in 2019 and withdrawn under President Biden. The proposal is open for public comment."))

body.append('<h2>From Abroad</h2>')
body.append('<h3>Indonesia&rsquo;s vice president resigns over his schooling</h3>')
body.append(P("Gibran Rakabuming Raka, 39, vice president of Indonesia, the world&rsquo;s fourth most populous country, resigned Thursday. He is the eldest son of former President Joko Widodo and was elected in 2024 as President Prabowo Subianto&rsquo;s running mate. Last month Indonesia&rsquo;s Constitutional Court and Supreme Court ruled that the education papers he filed before the election did not meet the legal requirement of a high-school diploma, and more than 120 lawmakers from eight parties began a process that could have led to impeachment; he stepped down hours before the House was to take it up.||President Prabowo said he accepted the resignation with a &ldquo;heavy heart.&rdquo; There will be no new election: the national legislature, the People&rsquo;s Consultative Assembly, will choose a new vice president within 60 days from two candidates the president names. Analysts say the episode may end the alliance between Prabowo and Widodo, at a time of street protests over the economy, corruption and months of wildfires."))
body.append('<h3>Congo&rsquo;s Ebola outbreak passes 11,000 cases</h3>')
body.append(P("The Ebola outbreak in the Democratic Republic of Congo has topped 11,000 cases, with 11,042 infections and 5,387 deaths, the Congolese government said Wednesday, making it the worst in that country&rsquo;s history; only the 2014&ndash;2016 West African epidemic was larger. Declared in mid-May, it is caused by the Bundibugyo strain, which has no approved vaccine or treatment, though trials are under way. It has reached eight of Congo&rsquo;s 26 provinces and spread to Uganda, Kenya and Nigeria. Health Minister Roger Kamba said most new infections are now in North Kivu, in the east, where fighting, bad roads and distrust of health workers slow the response. World Health Organization chief Tedros Adhanom Ghebreyesus condemned attacks that killed four health workers and said more than 1,000 people exposed to the virus are going untracked."))
body.append('<h3>Drones send Baltic residents to shelters</h3>')
body.append(P("Overnight Tuesday into Wednesday, Lithuania, Latvia and Estonia, the three small NATO countries on the Baltic Sea that border Russia, told residents to take shelter after unidentified drones crossed into their airspace, and NATO fighter jets were scrambled; the alerts lifted hours later, and no one was hurt. Lithuania&rsquo;s prime minister said four drones were detected across the region. The alerts said the drones came from Russia or Belarus, during a night of Ukrainian drone attacks on Russia that set fire to the port at Ust-Luga. Russia accuses Ukraine of using NATO airspace as cover; Ukraine says Russian jamming sometimes knocks its drones off course, and the Baltic governments deny letting their airspace be used. One attempt was made to shoot down a drone over northern Lithuania; whether it was hit is unclear. A NATO commander said the alliance could turn its Baltic air patrol into a full air-defense mission."))
body.append('<h3>World leaders meet for climate talks in Turkey, with many absent</h3>')
body.append(P("More than 100 heads of state and government gathered Wednesday and Thursday in Antalya, on Turkey&rsquo;s Mediterranean coast, for the leaders&rsquo; portion of COP31, the annual United Nations climate conference, which runs through Nov. 20. U.N. Secretary-General Ant&oacute;nio Guterres noted that global emissions hit a record in 2025: &ldquo;The brutal truth is that the climate crisis is outrunning us.&rdquo; Turkey&rsquo;s President Recep Tayyip Erdo&#287;an said wealthy nations must do more to cut emissions and pay for the change. Many major leaders stayed away, among them President Trump, China&rsquo;s Xi Jinping, India&rsquo;s Narendra Modi, France&rsquo;s Emmanuel Macron and Germany&rsquo;s Friedrich Merz, and the European Union&rsquo;s climate chief said &ldquo;expectations are not necessarily high&rdquo; for the final agreement."))
body.append('<h3>Iran lists Argentina&rsquo;s navy and air force as terrorists</h3>')
body.append(P("Iran&rsquo;s Foreign Ministry on Wednesday declared Argentina&rsquo;s navy and air force &ldquo;terrorist organizations,&rdquo; in retaliation for Argentina&rsquo;s decision in April to put Iran&rsquo;s Islamic Revolutionary Guard Corps, its most powerful military force, on Argentina&rsquo;s own terrorist list. Argentina blames the Guard and its Lebanese ally Hezbollah for the 1994 bombing of the AMIA Jewish community center in Buenos Aires, which killed 85 people. Argentina&rsquo;s foreign ministry said it &ldquo;categorically rejects&rdquo; Iran&rsquo;s move. Earlier this month Iran took a similar step against Britain&rsquo;s Royal Navy and Royal Air Force."))

body.append('<div style="break-inside:avoid;page-break-inside:avoid"><h2>Markets &amp; the Farm</h2>'+'<p class="note">Figures are for Wednesday&rsquo;s close, November 11; stocks traded on Veterans Day while the bond market was closed. Week changes are from Friday, November 6.</p>')
body.append('''<table class="mk"><tr><th>Index</th><th>Close</th><th>Day</th><th>Week</th></tr>
<tr><td>S&amp;P 500</td><td class="n">7,619.38</td><td class="n">+1.31%</td><td class="n">+3.29%</td></tr>
<tr><td>Dow Jones Industrials</td><td class="n">52,486.49</td><td class="n">+0.49%</td><td class="n">+2.34%</td></tr>
<tr><td>Nasdaq Composite</td><td class="n">25,466.19</td><td class="n">+1.60%</td><td class="n">+3.61%</td></tr></table></div>''')
body.append(P("Stocks won back Tuesday&rsquo;s losses as investors returned to the artificial-intelligence trade: CoreWeave, which rents out AI computing power, jumped about 24 percent after beating revenue estimates and raising its outlook, and chip makers led the way. The S&amp;P 500 now sits within about 2.6 percent of last month&rsquo;s record. After the close, Nvidia shares slipped on news reports concerning chief executive Jensen Huang and his future at the company. Traders now put the odds of a quarter-point Federal Reserve rate increase in December at about 90 percent; Thursday brings weekly jobless claims and existing-home sales."))
body.append('<h3>What analysts are saying</h3>')
body.append(P("Analysts leaned toward buying <b>Apple (AAPL)</b>, maker of the iPhone and Mac: China Renaissance upgraded it to Buy with a $425 target, citing its brand, steady services income and a huge base of devices that could carry new AI features (risk: weak upgrade demand and fierce competition in China); the stock hit a record Wednesday. They also favored <b>Republic Services (RSG)</b>, the trash-hauling, recycling and landfill company, which JPMorgan upgraded to Overweight with a $295 target as a steady, defensive business (risk: labor costs and a rich valuation), and <b>Corning (GLW)</b>, maker of specialty glass and the optical fiber that wires data centers, which Jefferies began covering at Buy with a $134 target on AI data-center demand (risk: a cyclical business with heavy spending)."))
body.append(P("Analysts turned cautious on <b>Nvidia (NVDA)</b>, the leading maker of AI chips: Baird cut it to Neutral and its target to $200 from $500, citing uncertainty around the chief executive (counterpoint: Morgan Stanley still rates it Overweight). Evercore ISI cut <b>Akamai (AKAM)</b>, which runs content-delivery and cybersecurity networks, to In Line with a $90 target, on slower growth against the big cloud providers (counterpoint: the shares already trade near that target). <i>This is information, not advice.</i>"))
body.append('''<table class="mk split"><tr><th>Commodity</th><th>Close</th><th>Change</th></tr>
<tr><td>Crude oil, WTI (Dec.)</td><td class="n">$86.53</td><td class="n">+$0.49</td></tr>
<tr><td>Crude oil, Brent (front month)</td><td class="n">$92.76</td><td class="n">+$1.27</td></tr>
<tr><td>Gasoline, Arkansas average (regular), AAA Nov. 12</td><td class="n">$3.56</td><td class="n">&minus;15&cent;, week</td></tr>
<tr><td>Gasoline, Jonesboro average (regular), AAA Nov. 12</td><td class="n">$3.49</td><td class="n">&mdash;</td></tr>
<tr><td>Live cattle (Dec.)</td><td class="n">$218.975</td><td class="n">&minus;22&frac12;&cent;</td></tr>
<tr><td>Feeder cattle (Jan.)</td><td class="n">$327.80</td><td class="n">+$1.125</td></tr>
<tr><td>Lean hogs (Dec.)</td><td class="n">$56.025</td><td class="n">+22&frac12;&cent;</td></tr>
<tr><td>Corn (Dec.), per bushel</td><td class="n">$4.48</td><td class="n">&minus;1&cent;</td></tr>
<tr><td>Soybeans (Jan.), per bushel</td><td class="n">$12.3075</td><td class="n">+2&frac34;&cent;</td></tr>
<tr><td>Wheat, Chicago (Dec.), per bushel</td><td class="n">$5.995</td><td class="n">+6&frac34;&cent;</td></tr>
<tr><td>Cotton (Dec.), cents per pound</td><td class="n">78.52</td><td class="n">&minus;0.17</td></tr>
<tr><td>Rough rice (Jan.), per hundredweight</td><td class="n">$18.325</td><td class="n">+5&cent;</td></tr></table>''')
body.append('<p class="note">Gasoline figures are AAA&rsquo;s daily averages this morning; AAA&rsquo;s weekly Arkansas report for this week was not yet out, and no week-ago Jonesboro figure was available. Rough rice: single source, Brownfield.</p>')
body.append(P("Oil firmed after Iran&rsquo;s top security official denied any talks with Washington, though prices remain near their lowest since August, and Arkansas pump prices keep sliding. Corn slipped despite a smaller government yield estimate because the dollar rallied to an 18-month high, which makes American grain dearer abroad; soybeans and wheat gained on bargain buying. Live cattle eased on profit-taking while feeders and hogs edged up, and cotton dipped with the stronger dollar."))

body.append('<h2>On the Field</h2>')
body.append(P("<b>Arkansas State football</b> (4-5) heads to Conway, S.C., to face Coastal Carolina (3-6) on Saturday at noon Central on ESPN+, as coach Butch Jones&rsquo;s Red Wolves try to recover from the loss to Louisiana-Monroe. <b>A-State men&rsquo;s basketball</b> (1-2) hosts Dillard on Saturday at 7 p.m. on ESPN+, the start of a three-game homestand, after Tuesday&rsquo;s 82-65 loss to UT Martin in which the Red Wolves shot just 31 percent; Layne Taylor led them with 18 points, six rebounds and five assists."))
body.append(P("<b>Arkansas</b> (3-6, 1-5 SEC), under first-year coach Ryan Silverfield, hosts No. 17 South Carolina (6-3), winners of four straight, Saturday at 6:45 p.m. on the SEC Network. Wednesday&rsquo;s league availability report lists Razorback defensive lineman Quincy Rhodes Jr. as questionable; Gamecock quarterback LaNorris Sellers hurt an ankle last week but is expected to play. <b>Tennessee</b> (7-2, 4-2), No. 8 in the playoff rankings, plays at Texas A&amp;M (4-5) Saturday at 2 p.m. Central on ESPN, without edge rusher Tyree Weathersby, lost for the season to a knee injury. The Vols have never won at Kyle Field and host LSU on Nov. 21."))

body.append('<h2>Afield &amp; Afloat</h2>')
body.append('<p class="note">Ratings are rule-of-thumb estimates from the forecast, the rut calendar and the sun, not measurements of animal or fish behavior.</p>')
body.append('<h3>Deer outlook: Fair</h3>')
body.append(P("The rut is at its peak in north Arkansas, which is reason enough to be in the woods, but this morning is mild, near 48 to 50 at dawn, the barometer is steady, and the afternoon will be warm for November. Be settled by 6:06 a.m. and hunt until about 8:35, then sit again from about 3:00 p.m. to sunset at 4:57; in the peak of the rut, 10 a.m. to 2 p.m. is realistic too, with bucks cruising for does. <b>Today&rsquo;s tip:</b> on a warm, light-wind day, does bed in shade and cover close to water, and bucks check them there; hang near a creek crossing or a thick bottom with the light breeze in your face, and save your best stand for tomorrow."))
body.append(P("<b>Tomorrow, Friday (estimate: Excellent):</b> the front brings a dawn near 33, about 15 degrees colder than today, a rising barometer and a moderate breeze of 10 to 12 miles an hour. That combination in the middle of the rut is about as good as the calendar offers. Watch from about 6:07 to 8:37 a.m. and 2:56 to sunset at 4:56, and stay through midday if you can. <b>Tomorrow&rsquo;s tip:</b> deer will be on their feet early after a cold, clear night; be in the stand well before first light, hunt the downwind side of a doe bedding area or a fresh scrape line, and keep scent down, since sound and smell carry far in cold, still air. It is also the last day to hunt archery-only before modern gun opens Saturday."))
body.append('<h3>Fishing outlook: Good</h3>')
body.append(P("At the Crowley&rsquo;s Ridge lakes (Craighead Forest Lake, Lake Frierson), steady pressure and an afternoon in the low 60s make this the best fishing day of the week. Fish late morning through mid-afternoon as the shallows warm, then the last hour before sunset at 4:57. <b>Today&rsquo;s tip:</b> fall bass are feeding up on shad; throw a shad-colored crankbait or a spinnerbait along the wind-blown banks and the mouths of coves, and look for crappie suspended around brush piles in 8 to 12 feet."))
body.append(P("<b>Tomorrow, Friday (estimate: Poor):</b> the cold front drops the dawn temperature by about 15 degrees, and the afternoon reaches only the upper 40s, which usually puts fish off their feed for a day or two. If you go, the best chance is early to mid-afternoon, plus the last hour before sunset at 4:56. <b>Tomorrow&rsquo;s tip:</b> slow everything down: a small jig or a live minnow fished vertically over deeper brush, and a jig-and-pig crawled along the bottom for bass, will catch more than anything moving fast."))
body.append('<h3>In season now, and what is next (zones 3, 4, 6 and 8)</h3>')
body.append('''<table class="mk"><tr><th>Zone</th><th>Archery</th><th>Youth gun</th><th>Modern gun</th><th>Muzzleloader</th></tr>
<tr><td>3</td><td>open to Feb. 28</td><td>Jan. 2&ndash;3</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr>
<tr><td>4</td><td>open to Feb. 28</td><td>Jan. 2&ndash;3</td><td>Nov. 14&ndash;22; Dec. 26&ndash;28</td><td>no season</td></tr>
<tr><td>6</td><td>open to Feb. 28</td><td>Jan. 2&ndash;3</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr>
<tr><td>8</td><td>open to Feb. 28</td><td>Jan. 2&ndash;3</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr></table>''')
body.append(P("<b>Saturday, Nov. 14,</b> modern gun season opens in all four zones. Zone 4, which includes Craighead County, closes Nov. 22, while Zones 3, 6 and 8 run to Dec. 6. Dogs may not be used for deer in Zones 3 and 4; in Zones 6 and 8 they are allowed Nov. 14 through Dec. 6. Chronic wasting disease rules apply in Craighead, Jackson, Mississippi and Randolph counties. Wear your hunter orange, and remember the limit of four deer, no more than two bucks.||<b>Ducks</b> open Saturday, Nov. 21, and run through Nov. 29, then Dec. 10&ndash;23 and Dec. 26 to Jan. 31; the AGFC warns that its magazine calendar and duck-stamp mailer wrongly listed the first segment as closing Dec. 1. The daily limit is six, with no more than four mallards (two hens). Geese follow the same segments. The AGFC has expanded its permit-only waterfowl hunts, including 715 acres of the St. Francis Sunken Lands in Poinsett County; applications open each week from 3 p.m. Thursday, beginning today, to midnight Sunday, at agfc.com. <b>Quail</b> (through Feb. 7), <b>rabbit</b> and <b>squirrel</b> (both through Feb. 28) are open."))

body.append('<h2>Postscript</h2>')
body.append('<p class="ps">Yet one smile more, departing, distant sun!<br>&nbsp;&nbsp;&nbsp;One mellow smile through the soft vapoury air,<br>Ere, o&rsquo;er the frozen earth, the loud winds run,<br>&nbsp;&nbsp;&nbsp;Or snows are sifted o&rsquo;er the meadows bare.</p>')
body.append('<p class="ps">&mdash; William Cullen Bryant, &ldquo;November,&rdquo; a sonnet (1824). A fitting word for the last warm afternoon before the frost.</p>')
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
