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
body.append('<div class="date">Wednesday, the Eleventh of November, 2026</div><div class="orn">&#10086;</div>')
body.append(P('Good morning,'))
body.append(P("Veterans Day dawns mild and clear, and the afternoon should reach the upper 70s before a cold front knocks Thursday back to the 50s. Close to home, prosecutors have dropped a child-rape case because the young victim was not made available for trial, and a Brookland restaurant manager is charged with draining a teenage employee&rsquo;s pay card. Farther off, the President has picked an Arkansas Supreme Court justice for the federal appeals court, the House shelved the impeachment of the Defense Secretary, and October&rsquo;s prices rose faster than expected."))
body.append('<h2>The Day Ahead</h2>')
body.append(hourly); body.append(grid)
body.append(P("Wednesday opens near 52 degrees at 6 a.m. under a clear sky, climbs to about 62 by 9 o&rsquo;clock and 75 by noon, and tops out near 78 in mid-afternoon. There is no rain in the forecast. The breeze is light in the morning but builds to about 15 miles an hour by late afternoon, and the evening cools to the mid-60s by 6 and about 61 by 9.||Thursday turns: a cloudy morning near 52, then clearing, with a high of only 59 and a low of 42. Friday is sunny and crisp, 53 and 37, and Saturday, opening day of modern gun deer season, starts near 34 and only reaches about 52. Sunday brings clouds and a slight 12 percent chance of rain, and early next week runs in the upper 50s."))
body.append('<h2>The Almanac</h2>')
body.append(f'''<table class="alm"><tr><td>First light</td><td>{alm['first_light']}</td><td>Sunrise</td><td>{alm['sunrise']}</td></tr>
<tr><td>Solar noon</td><td>{alm['noon']}</td><td>Sunset</td><td>{alm['sunset']}</td></tr>
<tr><td>Last light</td><td>{alm['last_light']}</td><td>Length of day</td><td>{alm['day_length']}</td></tr>
<tr><td>Change from yesterday</td><td>{alm['change'].replace('-','&minus;')}</td><td>Moon</td><td>{alm['moon']}, {alm['illum']}% lit</td></tr></table>''')
body.append(P("At the eleventh hour of the eleventh day of the eleventh month of 1918, the guns of the Great War fell silent under the Armistice signed in a railway carriage in France. The day was kept here as Armistice Day until 1954, when Congress renamed it Veterans Day to honor all who have served. A minute of quiet at 11 o&rsquo;clock this morning is an old custom worth keeping.||The moon is a slim two-day crescent; look low in the southwest in the half hour after sunset, before it follows the sun down. It reaches first quarter around November 17 and is full around November 24."))
body.append(P("Enjoy today&rsquo;s warmth, because Saturday&rsquo;s dawn near 34 is close to frost in the low spots. Bring in potted herbs and geraniums, drain and coil the garden hoses, and pick the last green tomatoes to ripen on a windowsill. Turnips and collards will only sweeten with the cold.||In the woods, wild persimmons are softening on the bare twigs; they are best after a frost has wrinkled them, and the deer and possums know it. Old-timers split a persimmon seed to read the winter: a spoon shape means snow to shovel, a knife means cutting cold, a fork means mild. It is lore, not a forecast. At the feeders, watch for the dark-eyed juncos, the slate-gray &ldquo;snowbirds&rdquo; that arrive from the north about now and stay until spring."))
body.append('<h2>Of Local Interest</h2>')
body.append('<h3>Veterans Day: what is closed, and Saturday&rsquo;s parade</h3>')
body.append(P("Jonesboro city offices are closed today and reopen Thursday, and Brookland city offices are closed as well. In Jonesboro there is no trash or recycling pickup today: Thursday&rsquo;s trucks will run the Wednesday and Thursday trash routes, and Friday will cover the rest of Thursday&rsquo;s routes plus Friday&rsquo;s. For recycling, Thursday picks up the second Wednesday route and the Thursday routes, and Friday the second Friday route. In Brookland, Dedman&rsquo;s Sanitation is running its normal routes this week.||The Jonesboro University Heights Lions Club has put American flags out in front of businesses across town today, part of a program that raises flags at least ten times a year for $50 annually. The county&rsquo;s main observance is Saturday: the Craighead County Veterans Day Parade steps off at 10 a.m. downtown, with the theme of America&rsquo;s 250th, followed by a ceremony in front of the Craighead County Courthouse on South Main Street. Expect downtown streets to close for the morning."))
body.append('<h3>Prosecutors drop child-rape case for lack of a witness</h3>')
body.append(P("Prosecutors have dismissed the charges against a Jonesboro man arrested in March 2025 and accused of raping a 10-year-old girl. Circuit Judge Scott Ellington signed an order of nolle prosequi, the formal notice that the state will not go forward with the case, on Monday, November 9. The dismissed charges were rape, possession of firearms by certain persons and aggravated assault.||In the filing, Deputy Prosecuting Attorney Alexia Perkins wrote that the victim was &ldquo;either unavailable or uncooperative.&rdquo; The judge added a handwritten note that the child was not available to testify and that her parent would not make her available for trial. The man, who had been held on a $250,000 bond, has been ordered released. The reports did not say whether the charges could be filed again; he was never convicted."))
body.append('<h3>Brookland restaurant manager charged with draining a teen&rsquo;s pay card</h3>')
body.append(P("A manager of the McDonald&rsquo;s in Brookland faces two felonies and a misdemeanor after Brookland police say she cloned a teenage employee&rsquo;s payroll debit card. A Craighead County district judge found probable cause on Monday for financial identity fraud, a Class C felony; theft of property involving credit or debit cards, a Class D felony; and fraudulent use of a credit card or account number, a misdemeanor. Bond was set at $35,000 and her next court date is December 16.||According to police, managers have access to a safe of spare employee pay cards and can link a card to an employee&rsquo;s account. Investigators allege she linked an unissued card to the girl&rsquo;s account; on August 12, while the employee was in Memphis, her paycheck was drained in about half an hour through two ATM withdrawals totaling $760 at a Paragould bank. Police say bank surveillance photographs identified the manager. These are allegations; she has not been convicted."))
body.append('<h3>Prison term for spitting on hospital staff</h3>')
body.append(P("A 29-year-old man from Alicia, in Lawrence County, was sentenced Monday to 18 months in prison, with four more years suspended, after pleading guilty to felony assault charges for attacks on medical workers in two Jonesboro emergency rooms. In the early hours of August 2 at St. Bernards Medical Center he spat on a doctor, two nurses and a county jailer, tried to bite staff and threatened to &ldquo;shoot up the whole hospital&rdquo;; in July he had spat in a doctor&rsquo;s face at NEA Baptist.||Arkansas law makes aggravated assault on a health-care worker a felony. Circuit Judge Scott Ellington ran the sentences together, credited 101 days already served, ordered no contact with the victims and set monthly fines after release. A terroristic-threatening charge and a disorderly-conduct charge were dropped in the plea."))
body.append('<h3>Brookland Junior High takes second in the state</h3>')
body.append(P("Brookland Junior High placed second overall at the Arkansas Game and Fish Commission&rsquo;s second Generation Conservation Summit, a statewide contest of outdoor skills and conservation knowledge for students. Serenity Rainwater and McKenzie Davison won STEM in Conservation, and Aiden Looney won the Junior Cadet Challenge. The quiz bowl team of Stone McMillon, Cole Hayes, Noah Campbell, Hensley Hathcoat and Harper Frans took second.||Third-place finishes went to Elliot Metheny in photography, Drake Rainwater and Kayson Matthews in game calling, Siler Snell in air rifle and Owen Burdin in archery. Congratulations to all of them."))
body.append('<h3>A Beebe gift for the Bradbury</h3>')
body.append(P("Former Gov. Mike Beebe, a Searcy native who led Arkansas from 2007 to 2015, has given a painting called &ldquo;Beau&rdquo; to the permanent collection of the Bradbury Art Museum at Arkansas State University. It is from V. L. Cox&rsquo;s series &ldquo;Images of the American South,&rdquo; which uses old objects such as vintage screen doors to explore Southern history; Cox grew up in Arkansas and studied at Henderson State. &ldquo;I want to share it with as many people as possible,&rdquo; Beebe said. The museum has not announced when the piece will go on view."))
body.append('<h3>Around town</h3>')
body.append(P("<b>Free soup on Wednesdays:</b> a retired Jonesboro woman, Debbie Johnson, begins her third winter of free soup, served 5 to 6:30 p.m. each Wednesday through April at Bill&rsquo;s Fresh Market, Main Street and East Johnson Avenue. Chicken noodle, vegetable and potato rotate week to week.||<b>Veterans dinner:</b> Jonesboro Elks Lodge 498, 2113 W. Washington Ave., Friday, 6 to 7:30 p.m.; free for veterans and their spouses, $10 for others. <b>Judd Hill Farmers Market</b> opens its winter season Saturday, 9 a.m. to 2 p.m., on Aggie Road, with an ornament station and a holiday &ldquo;passport&rdquo; drawing; the later markets are November 21 and December 19.||<b>&ldquo;Little Shop of Horrors&rdquo;</b> from A-State Theatre, Fowler Center, November 13&ndash;22 (7:30 p.m. on the 13th, 14th, 20th and 21st; 2:30 p.m. on the 15th and 22nd); tickets $15&ndash;$20, A-State students free. The A-State Center for Leadership Excellence, which turned 10 on Monday, is looking for mentors for monthly one-hour online sessions with students (cle@astate.edu). The <b>Brookland Christmas Parade</b>, its 25th, is Sunday, December 6, at 2 p.m."))
body.append('<h2>From the Police Reports</h2>')
body.append('<p class="note">Jonesboro Police incident reports. Charges are allegations. No names are printed.</p>')
body.append(P("<b>Monday morning to Tuesday morning:</b> 39 reports were filed between 8 a.m. Monday and 8 a.m. Tuesday, with 14 people arrested or cited in 12 of them. There were no shootings, house burglaries or fires in this batch.||<b>Hit-and-run:</b> a man riding an electric bicycle was hurt early Monday, between about 6:30 and 7:30 a.m., near Lacy Drive and Mahon Drive, by a driver who did not stop. Police are looking for a small white or light-colored pickup, possibly a Chevrolet Colorado. Separately, a man with serious head and facial injuries was found near Promise Lane and Race Street around noon Monday and taken to St. Bernards; how he was hurt is not known."))
body.append(P("<b>Cars and guns:</b> seven vehicle break-ins or smashed windows were reported, on James Street, Richmond Avenue, South Church Street, West Huntington Avenue, Stallings Lane and Sanderson Lane; police have tied the Richmond Avenue case to a series of five. A handgun valued at $4,000 was taken from an unlocked pickup on James Street, and debit cards taken on Stallings Lane were used for purchases the same day. A 2005 car with a handgun inside was stolen on Jeanne McQueen Place, and an ATV was taken from outside a home on Charles Street. <b>The tip:</b> lock the car every time, and never leave a gun, wallet or cards inside.||<b>Other reports:</b> $6,588 in jewelry was stolen from a vendor&rsquo;s booth in a store on Woodsprings Road; a city license-plate camera and its solar panel were damaged, about $3,500, near Arrowhead Farm Road and North Culberhouse; someone reported $1,200 taken from a bank account by debit card; and a platinum and diamond wedding ring valued at $150,000 was reported lost in a parking lot on South Church Street. A woman was bitten by a dog on French Street, and loose, aggressive dogs were reported on Una Street."))
body.append(P("<b>Arrests:</b> two people were arrested for shoplifting at Walmart on East Highland Drive. A traffic stop for expired tags ended with an adult arrested on a felony charge of possession of a firearm by a felon and a juvenile charged with handgun possession, 72401 area. A driver stopped at East Parker and Harrisburg roads was arrested on a suspended license and an out-of-town warrant. Five others were arrested on warrants for failure to appear, unpaid fines or probation, most after traffic stops.||<b>Also reported:</b> a shoplifting and threatening case, juvenile suspect, 72401 area; an assault report, juvenile victim; a terroristic-threatening report, juvenile victim, 72404 area; and one sexual-offense report, under investigation."))
body.append('<div style="break-inside:avoid;page-break-inside:avoid"><p class="note">At the county jails</p>'+P("In Craighead County, the sheriff&rsquo;s roster shows 295 people held, 27 of them booked in the last 48 hours; among those listed first, second-degree battery, failures to appear, DWI and parole violations were common. In Randolph County (Pocahontas), 64 people are held, with five bookings in the last two days, two of them for second-offense DWI, and three releases. Being on a roster does not mean a person was convicted.")+'</div>')
body.append('<h2>From the State</h2>')
body.append('<h3>Justice Hiland replaces Judge Rudofsky as appeals-court nominee</h3>')
body.append(P("The White House on Tuesday withdrew its nomination of U.S. District Judge Lee Rudofsky, a federal trial judge in Little Rock and former Arkansas solicitor general, to the 8th U.S. Circuit Court of Appeals, and President Trump named Arkansas Supreme Court Justice Cody Hiland instead. The 8th Circuit is the federal appeals court just below the U.S. Supreme Court for Arkansas, Missouri, Iowa, Minnesota, Nebraska and the Dakotas; the seat opens because Judge Bobby Shepherd of Arkansas is taking senior status, a form of semi-retirement.||Hiland was U.S. attorney for the Eastern District of Arkansas from 2017 to 2020, and his state court term ends December 31. Arkansas&rsquo;s Republican senators, John Boozman and Tom Cotton, had never publicly backed Rudofsky, and outlets report Hiland is their choice. Rudofsky said that without his home-state senators, &ldquo;confirmation is simply not a practical possibility,&rdquo; and called Hiland &ldquo;a solid jurist and a good friend.&rdquo;||Time is short: the Senate must confirm him by January 3, when the new Democratic majority takes over, or the nomination lapses. Judiciary Chairman Chuck Grassley says he will push judges through in the lame-duck session."))
body.append('<h3>Medicaid expansion overhaul will take longer than Washington allowed</h3>')
body.append(P("ARHOME, the Arkansas Medicaid expansion program that uses federal money to buy private insurance for about 208,800 low-income working-age adults, has a federal extension only through June 30, 2027; the state had asked for two years. On Tuesday, Elizabeth Pitman, who directs the Division of Medical Services at the state Department of Human Services, told legislators that moving those enrollees to traditional fee-for-service Medicaid would take 12 to 18 months, and a move to managed care at least two years. She said federal officials signaled more extensions &ldquo;as needed.&rdquo; &ldquo;Nothing is off the table except for not continuing coverage,&rdquo; she said.||Meanwhile, about 70,000 enrollees in Centene plans must choose a Blue Cross plan by November 15 or be assigned one, because Centene is leaving the program, and the full Medicaid work requirement of 80 hours a month of work, school or volunteering takes effect January 1. Lawmakers say a new expansion model will be a top priority when the session opens in January."))
body.append('<h3>A new idea for the stalled prison plan</h3>')
body.append(P("At a joint meeting of the legislature&rsquo;s Judiciary committees on Tuesday, state Rep. Steve Unger, a Springdale Republican, proposed building two 500-bed state prisons beside the Washington County jail in Fayetteville, using money set aside for Gov. Sanders&rsquo;s planned 3,000-bed prison in Franklin County. That project&rsquo;s estimated cost had grown from $470 million to $825 million amid local opposition and water-supply problems, and corrections officials shelved it in April. No action was taken. Sen. Clarke Tucker, a Little Rock Democrat, noted the prison population is about 19,000, below the 21,000 once projected, and is pushing proposals to reduce the number of beds needed."))
body.append('<h2>From the Nation</h2>')
body.append('<h3>House shelves the Hegseth impeachment, 211&ndash;204</h3>')
body.append(P("The House voted 211 to 204 on Tuesday to send Rep. Thomas Massie&rsquo;s articles of impeachment against Defense Secretary Pete Hegseth to the Judiciary Committee, which effectively ends them. Massie, a Kentucky Republican who leaves Congress in January after losing his primary, was the only Republican to vote with all Democrats against the move. His articles accused Hegseth of starting the war with Iran without approval from Congress, of strikes on boats in the Caribbean that critics call unlawful killings, of directing the seizure of Venezuela&rsquo;s president, Nicol&aacute;s Maduro, and of retaliating against Sen. Mark Kelly.||Hegseth called the effort a &ldquo;farce,&rdquo; and President Trump said it &ldquo;miserably FAILED!&rdquo; House Democratic leader Hakeem Jeffries said, &ldquo;This is not the end of it.&rdquo; Massie says he will not file again but will force a vote on a war-powers resolution on Iran; Democrats could take up impeachment once they control both chambers in January."))
body.append('<h3>Republicans pick their leaders for the minority</h3>')
body.append(P("After losing both chambers in last week&rsquo;s election, House Republicans on Tuesday chose Rep. Jim Jordan of Ohio, chairman of the Judiciary Committee and a close Trump ally, as their leader in the next Congress, by 106 to 73 over Majority Leader Steve Scalise of Louisiana. Speaker Mike Johnson had already said he would not seek the post. Rep. Tom Emmer of Minnesota stays as whip and Rep. Lisa McClain of Michigan becomes conference chair.||Senate Republicans re-elected John Thune of South Dakota as their leader without opposition. Arkansas&rsquo;s Sen. Tom Cotton keeps the No. 3 job, chairman of the Senate Republican Conference. Dozens of Republican National Committee members had asked for a 30-day delay to study the losses; the votes went ahead. ABC counts Democrats ahead in the House, 254 to 166, with 15 races still undecided."))
body.append('<h3>Prices rose faster than expected in October</h3>')
body.append(P("The Bureau of Labor Statistics, the Labor Department agency that tracks prices, said consumer prices rose 0.4 percent in October, after 0.6 percent in September. Core prices, which leave out food and energy, rose 0.3 percent, more than economists expected. Energy rose 0.7 percent, food 0.5 percent and beef 0.9 percent; housing costs made up nearly a third of the increase, while used cars fell. The bureau could not publish a yearly rate because the 2025 government shutdown kept it from collecting prices in October 2025.||Traders now expect the Federal Reserve, the nation&rsquo;s central bank, to raise interest rates by a quarter point at its December 8&ndash;9 meeting; the benchmark rate is now 3.75 to 4 percent. Fed officials cite tariffs, the Iran war and spending on artificial-intelligence data centers among the pressures on prices."))
body.append('<h3>Senate Democrats divided over Schumer</h3>')
body.append(P("Sen. Chuck Schumer of New York, the Democratic leader, said Tuesday he is &ldquo;confident I will be elected majority leader&rdquo; when Democrats take control in January, but opposition is growing. Sen. Bernie Sanders of Vermont said, &ldquo;I will not be supporting Chuck,&rdquo; and Sen. Elissa Slotkin of Michigan said she is a &ldquo;no&rdquo; until someone offers a concrete plan for change; Fox News reports five newly elected Democratic senators also oppose him. No challenger has declared. The secret-ballot vote, which includes the senators-elect, is expected in early December."))
body.append('<h2>From Abroad</h2>')
body.append('<h3>Iran: Rubio says the blockade is working; Tehran says its uranium stays</h3>')
body.append(P("Secretary of State Marco Rubio said in Paris on Tuesday, after the meetings of the G7 industrial democracies, that President Trump &ldquo;has concluded that for the time being there is no need for major combat operations&rdquo; against Iran, because sanctions and the U.S. naval blockade are &ldquo;achieving the same objective by economic means.&rdquo; He called Tehran&rsquo;s conditions for talks &ldquo;absurd,&rdquo; though he offered no figures for his claim that Iran cannot sell its oil.||On Wednesday, Mohsen Rezaei, secretary of Iran&rsquo;s Supreme National Security Council, its top security body, told Lebanese television that Iran&rsquo;s enriched uranium will never leave the country and that no talks are under way; he warned of strikes on U.S. bases if Iran is attacked again. Attacks on shipping in the Strait of Hormuz have not eased, Reuters reports, and Iran&rsquo;s Revolutionary Guards said two tankers caught fire after hitting mines. Brent crude rose about 1.4 percent early Wednesday."))
body.append('<h3>Ukraine talks in Abu Dhabi end without a breakthrough</h3>')
body.append(P("The second day of American-brokered talks between Russian and Ukrainian officials in Abu Dhabi, capital of the United Arab Emirates, ended Wednesday after less than two hours, with no word of progress on the main disputes: territory, security guarantees and the terms of a ceasefire. It was the first face-to-face meeting of the two sides since February. Russian state media said both sides agreed to another large prisoner exchange; Kyiv had not confirmed it.||The fighting went on. Russia struck six Ukrainian power facilities in four regions, leaving parts of the city of Kryvyi Rih without power or heat, and Ukrainian drones set a fire at Russia&rsquo;s Ust-Luga port on the Baltic, injuring three workers."))
body.append('<h3>U.S. Army officer arrested in England on suspicion of spying for Russia</h3>')
body.append(P("British counterterrorism police, working with the FBI and the U.S. military, arrested a 41-year-old American soldier near Gloucester, England, on Tuesday. A U.S. official described him as a field-grade officer, a major to a colonel; he was assigned to NATO&rsquo;s Allied Rapid Reaction Corps headquarters in Gloucestershire. He has not been named or charged and is held under Britain&rsquo;s National Security Act. FBI Director Kash Patel called the allegations &ldquo;of the utmost concern&rdquo;; the Kremlin said Moscow had &ldquo;absolutely nothing to do with&rdquo; it."))
body.append('<h3>Europe quarrels over tying its budget to Ukraine aid</h3>')
body.append(P("German Chancellor Friedrich Merz has told European Union leaders that new aid for Ukraine is an &ldquo;essential prerequisite&rdquo; for approving the EU&rsquo;s next long-term budget, and the leaders of Slovakia, the Czech Republic, Hungary and Bulgaria pushed back; Slovakia&rsquo;s Robert Fico called it &ldquo;blackmail&rdquo; and threatened a veto. Both decisions need every member&rsquo;s consent. Ukraine faces a gap of about &euro;70 billion next year. <i>(single source: Euronews)</i>"))
body.append('<div style="break-inside:avoid;page-break-inside:avoid"><h2>Markets &amp; the Farm</h2>'+'<p class="note">Figures are for Tuesday&rsquo;s close, November 10. Week changes are from Friday, November 6. Index levels agree across AP and other reports.</p>')
body.append('''<table class="mk"><tr><th>Index</th><th>Close</th><th>Day</th><th>Week</th></tr>
<tr><td>S&amp;P 500</td><td class="n">7,520.93</td><td class="n">&minus;0.38%</td><td class="n">+1.95%</td></tr>
<tr><td>Dow Jones Industrials</td><td class="n">52,231.89</td><td class="n">&minus;0.30%</td><td class="n">+1.84%</td></tr>
<tr><td>Nasdaq Composite</td><td class="n">25,065.87</td><td class="n">&minus;0.74%</td><td class="n">+1.98%</td></tr></table></div>''')
body.append(P("Stocks gave back part of Monday&rsquo;s big rally after the hotter-than-expected inflation report raised the odds of a December rate increase; the 10-year Treasury yield climbed back near 5 percent. Nvidia, the chip maker, fell about 5.5 percent after its board hired outside lawyers to investigate a report about its chief executive&rsquo;s ties to an alleged Chinese intelligence asset, and Microsoft passed it in market value. The bond market is closed today for Veterans Day, though stocks trade normally. Producer prices come Friday, and Nvidia reports earnings November 17."))
body.append('<h3>What analysts are saying</h3>')
body.append(P("Analysts leaned toward buying <b>Riot Platforms (RIOT)</b>, a bitcoin miner turning to data centers: Jefferies upgraded it to Buy and more than doubled its target to $28, citing a favorable lease at its Corsicana, Texas, site (risk: the shares rise and fall with bitcoin). DZ Bank upgraded <b>Cloudflare (NET)</b>, the internet security and network company, to Buy with a $300 target after third-quarter revenue grew 39 percent (risk: the shares already trade above that target). Rothschild &amp; Co Redburn upgraded <b>American Airlines (AAL)</b> to Buy with a $17.50 target, expecting higher fares to hold through 2027 <i>(single source: CNBC)</i> (risk: jet fuel costs tied to the Iran war).||Analysts turned cautious on <b>Wix.com (WIX)</b>, the website-building company: Bank of America cut it two notches to Underperform, with a $68 target, arguing that AI coding tools threaten its core business (risk to the call: its latest quarter beat estimates). UBS downgraded <b>Carlyle Group (CG)</b>, the private-equity firm, to Neutral with a $47 target, doubting it can reach its 2028 growth goals (risk to the call: the shares already trade below that target). This is information, not advice."))
body.append('''<table class="mk split"><tr><th>Commodity</th><th>Close</th><th>Change</th></tr>
<tr><td>Crude oil, WTI (Dec.)</td><td class="n">$86.04</td><td class="n">&minus;$0.81</td></tr>
<tr><td>Crude oil, Brent (Jan.)</td><td class="n">$91.49</td><td class="n">&minus;$1.08</td></tr>
<tr><td>Gasoline, Arkansas average (regular), AAA Nov. 5</td><td class="n">$3.71</td><td class="n">&minus;9&cent;, week</td></tr>
<tr><td>Gasoline, Jonesboro average (regular), AAA Nov. 5</td><td class="n">$3.63</td><td class="n">&minus;10&cent;, week</td></tr>
<tr><td>Live cattle (Dec.)</td><td class="n">$219.20</td><td class="n">+$3.00</td></tr>
<tr><td>Feeder cattle (Jan.)</td><td class="n">$326.68</td><td class="n">+$2.50</td></tr>
<tr><td>Lean hogs (Dec.)</td><td class="n">$55.88</td><td class="n">&minus;$0.08</td></tr>
<tr><td>Corn (Dec.), per bushel</td><td class="n">$4.49</td><td class="n">+9&frac34;&cent;</td></tr>
<tr><td>Soybeans (Jan.), per bushel</td><td class="n">$12.28</td><td class="n">+39&frac34;&cent;</td></tr>
<tr><td>Wheat, Chicago (Dec.), per bushel</td><td class="n">$5.9275</td><td class="n">+4&frac34;&cent;</td></tr>
<tr><td>Cotton (Dec.), cents per pound</td><td class="n">78.69</td><td class="n">&minus;0.09</td></tr>
<tr><td>Rough rice (Jan.), per hundredweight</td><td class="n">$18.275</td><td class="n">+12&frac12;&cent;</td></tr></table>''')
body.append(P("Oil settled at its lowest since late August on hopes of U.S.&ndash;Iran talks, then firmed early Wednesday after Tehran denied any talks. Gasoline keeps sliding: AAA&rsquo;s daily average this morning is about $3.58 in Arkansas and $3.50 in Jonesboro, and the national average has dipped below $4 for the first time since July. Grains jumped after the Agriculture Department&rsquo;s monthly crop report cut its estimate of the U.S. corn crop by 141 million bushels and trimmed soybean stocks on stronger exports. Cattle extended their rebound. Oil and grains agree across several sources; rice is a single source (Brownfield Ag News)."))
body.append('<h2>On the Field</h2>')
body.append(P("<b>Arkansas State football</b> (4-5, 2-3 in the Sun Belt Conference) plays at Coastal Carolina (3-6) on Saturday at noon Central on ESPN+, coming off the 19-17 loss to Louisiana-Monroe; Coastal is a slight favorite. The Red Wolves visit Louisiana Tech on November 21.||<b>A-State men&rsquo;s basketball</b> (1-2) lost at home to UT Martin 82-65 on Tuesday night; the visitors led 54-34 at halftime, and A-State shot 31 percent. Layne Taylor led the Red Wolves with 18 points. They host Dillard on Saturday at 7 p.m. and Arkansas-Pine Bluff next Wednesday, November 18, at 7 p.m., both at First National Bank Arena."))
body.append(P("<b>Arkansas</b> (3-6, 1-5 in the SEC) hosts South Carolina (6-3) Saturday at 6:45 p.m. on the SEC Network; the Gamecocks are favored by about a touchdown. After two missed long field goals in the 26-23 loss at Auburn, coach Ryan Silverfield says he will take a &ldquo;long look&rdquo; at handing long attempts to Braeden McAlister. <b>Tennessee</b> (7-2) rose to No. 8 in Tuesday&rsquo;s College Football Playoff rankings, but lost its top pass rusher, defensive end Tyree Weathersby, for the season; the Volunteers play at Texas A&amp;M on Saturday at 2 p.m. Central on ESPN."))
body.append('<h2>Afield &amp; Afloat</h2>')
body.append('<p class="note">Ratings are rule-of-thumb estimates from the forecast, the rut calendar and the sun, not measurements of animal or fish behavior.</p>')
body.append('<h3>Deer outlook: Good</h3>')
body.append(P("The rut is at its peak in north Arkansas, and the barometer is falling ahead of Thursday&rsquo;s cold front, which tends to get deer on their feet. The drawbacks are a warm afternoon near 77 and a breeze building to about 15 miles an hour by evening. Be settled by 6:05 a.m. and hunt until about 8:35, then sit again from about 3:00 p.m. to sunset at 4:57; at the peak of the rut, 10 a.m. to 2 p.m. is realistic too, with bucks cruising.||<b>Today&rsquo;s tip:</b> only archery is open until Saturday. In this heat, bucks will cruise the shady, thick cover between bedding areas rather than open fields, so hang near a creek crossing or a funnel through timber. The afternoon wind will carry scent farther than this morning&rsquo;s calm air, so set up with it in your face."))
body.append(P("<b>Tomorrow, Thursday (estimate: Fair):</b> dawn near 47 under a cloudy sky that clears by afternoon, a high near 58 and a breeze of 10 to 15 miles an hour; the pressure settles after the front. Watch about 6:06 to 8:36 a.m. and 2:57 to 4:57 p.m., with midday still worth a sit in the rut. <b>Tomorrow&rsquo;s tip:</b> the first cool morning after a warm spell often gets deer moving, but it is also the last chance to check your rifle&rsquo;s zero and hang stands quietly before Saturday&rsquo;s opener; do your work at midday and stay out of the bedding cover."))
body.append('<h3>Fishing outlook: Fair</h3>')
body.append(P("At the Crowley&rsquo;s Ridge lakes (Craighead Forest Lake, Lake Frierson), the barometer is falling fast ahead of the front, which usually makes fish fickle, but the warm afternoon helps. Fish late morning through mid-afternoon as the shallows warm, then the last hour before sunset at 4:57.||<b>Today&rsquo;s tip:</b> the hours just before a front can bring a short feeding burst. Run a spinnerbait or shallow crankbait along the wind-blown bank for bass this afternoon, and keep a minnow under a float near brush for crappie."))
body.append(P("<b>Tomorrow, Thursday (estimate: Good):</b> steady pressure and an afternoon near 58, with a moderate breeze. Best from late morning to mid-afternoon, and again before sunset at 4:57. <b>Tomorrow&rsquo;s tip:</b> after the front, slow down: crappie will hold tight to brush piles in 10 to 15 feet, so drop small minnows or 1/16-ounce jigs straight down, and work a jig slowly along deeper wood for bass."))
body.append('<h3>In season now, and what is next (zones 3, 4, 6 and 8)</h3>')
body.append('''<table class="mk"><tr><th>Zone</th><th>Archery</th><th>Youth gun</th><th>Modern gun</th><th>Muzzleloader</th></tr>
<tr><td>3</td><td>open to Feb. 28</td><td>Jan. 2&ndash;3</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr>
<tr><td>4</td><td>open to Feb. 28</td><td>Jan. 2&ndash;3</td><td>Nov. 14&ndash;22; Dec. 26&ndash;28</td><td>no season</td></tr>
<tr><td>6</td><td>open to Feb. 28</td><td>Jan. 2&ndash;3</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr>
<tr><td>8</td><td>open to Feb. 28</td><td>Jan. 2&ndash;3</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr></table>''')
body.append(P("<b>Saturday, November 14,</b> modern gun season opens in all four zones. Zone 4, which includes Craighead County, closes November 22, while Zones 3, 6 and 8 run to December 6. New this year, centerfire rifles are allowed during modern gun season in Zone 4. The limit is four deer, no more than two bucks. <i>A correction:</i> Zone 4 has no muzzleloader season at all this year, as the table now shows.||<b>Ducks</b> open Saturday, November 21; the first segment runs through November 29 (the Game and Fish Commission says a magazine calendar and a duck-stamp mailer wrongly printed December 1), then December 10&ndash;23 and December 26 to January 31. Applications for permit-only waterfowl hunts open tomorrow, November 12, at 3 p.m., and now include a 715-acre section of St. Francis Sunken Lands WMA in Poinsett County; apply at agfc.com. <b>Quail</b> is open through February 7, and <b>rabbit</b> and <b>squirrel</b> through February 28."))
body.append('<h2>Postscript</h2>')
body.append('<p class="ps">&ldquo;It is rather for us to be here dedicated to the great task remaining before us&mdash;that from these honored dead we take increased devotion to that cause for which they gave the last full measure of devotion&mdash;that we here highly resolve that these dead shall not have died in vain, that this nation under God shall have a new birth of freedom, and that government of the people, by the people, for the people shall not perish from the earth.&rdquo;</p>')
body.append('<p class="ps">&mdash; Abraham Lincoln, the Gettysburg Address, November 19, 1863, at the dedication of a soldiers&rsquo; cemetery.</p>')
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
