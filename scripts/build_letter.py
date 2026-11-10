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
body.append('<div class="date">Tuesday, the Tenth of November, 2026</div><div class="orn">&#10086;</div>')
body.append(P('Good morning,'))
body.append(P("A cold start and a summery afternoon, with Veterans Day arriving tomorrow on a day that may touch 75 degrees. The Craighead County budget got its first public airing, the state has cleared Lake Poinsett for swimmers and boaters again, Congress is back in a lame-duck mood, and stocks sprang back sharply on Monday. Here it is, as plainly as we can set it down."))
body.append('<h2>The Day Ahead</h2>')
body.append(hourly); body.append(grid)
body.append(P("Tuesday opens cold, about 40 degrees at dawn under a lid of cloud, then climbs to 66 by noon and about 69 by mid-afternoon, with no rain in sight. The evening cools back into the 50s, with some clearing late.||Wednesday, Veterans Day, is the warmest day of the stretch, near 75 with a low of about 49 and a slim 7 percent chance of rain. A cold front then drops Thursday to the low 60s and Friday to the low 50s, and Saturday morning, opening day of modern gun deer season, will start near 33 degrees."))
body.append('<h2>The Almanac</h2>')
body.append(f'''<table class="alm"><tr><td>First light</td><td>{alm['first_light']}</td><td>Sunrise</td><td>{alm['sunrise']}</td></tr>
<tr><td>Solar noon</td><td>{alm['noon']}</td><td>Sunset</td><td>{alm['sunset']}</td></tr>
<tr><td>Last light</td><td>{alm['last_light']}</td><td>Length of day</td><td>{alm['day_length']}</td></tr>
<tr><td>Change from yesterday</td><td>{alm['change'].replace('-','&minus;')}</td><td>Moon</td><td>{alm['moon']}, {alm['illum']}% lit</td></tr></table>''')
body.append(P("The moon is a hairline crescent, barely a day old, and will slip below the western horizon soon after the sun, so tonight is still very dark. Tomorrow is Martinmas, St. Martin's Day, and the old folk belief in a mild spell around it, a &ldquo;Martinmas summer,&rdquo; looks well matched by Wednesday's forecast. It is lore, not a forecast. The United States Marine Corps, for its part, marks its birthday today; it was founded on November 10, 1775.||In the garden, rake the leaves onto the beds rather than the curb: oak and sweetgum leaves make good mulch for garlic and strawberries, and a thick layer keeps the soil from heaving in a hard freeze. Collards and mustard greens are at their sweetest now, and a warm spell like Wednesday's is a fine day to clean and oil the pruning tools."))
body.append(P("Out on the Delta the combines are mostly parked, and the winter wheat that went in after soybeans is just showing its green rows. Overhead, long skeins of geese and the first sandhill cranes are heading south; listen for the cranes' rattling call on a still evening. Hickory nuts and black walnuts are down in the woods, and the deer tracks in the soft ground of field edges are thickening, a sign of the rut."))
body.append('<h2>Of Local Interest</h2>')
body.append('<h3>Craighead County&rsquo;s 2027 budget gets a public airing</h3>')
body.append(P("The Craighead County Quorum Court, the county's legislative body, presented its proposed 2027 budget to the public on Monday at the courthouse annex. The plan calls for an overall increase of 1.4 percent, a 4 percent raise for county employees and a new public information officer. County Judge Marvin Day, the county's chief executive, said the new position would mainly handle Freedom of Information Act requests, the public-records requests that citizens and reporters file, and would also help with press releases and social media.||The budget may still be amended before the Quorum Court votes on it in December. Judge Day also introduced the newly elected justices of the peace, who take office in January, and said he has given each of them the current and proposed budgets so they can &ldquo;hit the ground running.&rdquo; (KAIT's report gives no dollar totals.)"))
body.append('<h3>Lake Poinsett cleared of its algae advisory</h3>')
body.append(P("The Arkansas Division of Environmental Quality, part of the state Department of Energy and Environment, has lifted the harmful algal advisory for Lake Poinsett in Poinsett County. The advisory was issued in September after the agency confirmed a bloom of cyanobacteria, sometimes called blue-green algae, which can produce toxins harmful to people and pets. After water samples taken over two weeks, the agency said the toxin levels had &ldquo;fully dissipated&rdquo; and are within safe recreational levels.||The agency still asks anyone who sees a suspected new bloom to stay out of the water and report it, at 501-682-0744 or ee.habs@arkansas.gov."))
body.append('<h3>Probation in the school bus threat case</h3>')
body.append(P("A 30-year-old Jonesboro man pleaded guilty Monday to first-degree terroristic threatening, a Class D felony, over an incident on September 15 at Brazos and Kingsbury streets, and Circuit Judge Scott Ellington sentenced him to 60 months of probation and 120 days in the Craighead County jail, with credit for 55 days already served. A misdemeanor trespassing charge was dropped. According to the arrest affidavit, he went to a school bus looking for someone who had cursed at his children and, when the driver kept him from boarding, threatened the driver; bus video recorded him saying he would come back with a gun. He told police he was angry and trying to protect his children.||He must stay away from the victim, complete anger-management and parenting classes and pay $640 in fines and fees. Jonesboro Public Schools has since updated its bus rules: parents who need to speak with a driver must now do so through the driver's window, not at the bus door."))
body.append('<h3>Former DHS caseworker&rsquo;s trial pushed to March</h3>')
body.append(P("The jury trial of a former Craighead County caseworker for the Arkansas Department of Human Services, who is accused of possessing child sexual abuse material, has been moved from December to March 1&ndash;12, 2027, according to Jonesboro Right Now. He was arrested in September after two tips from the National Center for Missing and Exploited Children flagged a Google account that allegedly uploaded 44 videos. He remains in the Craighead County jail on a $250,000 bond. These are allegations; he has not been convicted.||The state department says its review of every case he handled found no connection between his official duties and the material, and that it interviewed every child still in foster care in those cases. A DHS spokesman said the agency hopes to finish its internal review soon."))
body.append('<h3>Child battering arrest on Melrose Street</h3>')
body.append(P("A 20-year-old Jonesboro man faces two counts of second-degree domestic battering, both Class B felonies, after police went to an apartment on Melrose Street on Sunday, November 8. A caller had reported hearing a child being struck repeatedly for about 20 minutes. According to the probable cause affidavit, officers saw injuries on the side and stomach of a 9-year-old and a loop-shaped welt on a 4-year-old; the older child said he was hit with an extension cord, and the man at first blamed a dog.||At his first appearance Monday, District Judge Tommy Fowler set a secured bond (the amount was not reported), ordered no contact and appointed a public defender. He is due in Craighead County Circuit Court at 8:30 a.m. on December 16. The charges are allegations."))
body.append('<h3>Public asked to weigh in on a Delta &ldquo;heritage area&rdquo;</h3>')
body.append(P("Public comment is open until December 11 on a study to create the Arkansas Delta National Heritage Area, a congressionally designated region whose historic, natural and cultural resources are managed by local partners. The proposal covers 17 eastern Arkansas counties, Craighead among them. If Congress approves, the area would receive federal funds for 15 years; backers describe it as an economic development and tourism tool, with ideas such as music tourism and a competitive grant program for preservation and the arts.||The effort is led by Arkansas State University's Heritage Sites under Dr. Adam Long, and Sen. Tom Cotton and Rep. Bruce Westerman plan to introduce legislation. The full study is on the A-State website; comments and letters of support go by email to Dr. Long at adamlong@AState.edu."))
body.append('<h3>Around town</h3>')
body.append(P("<b>Christmas at the Park</b> returns to Joe Mack Campbell Park, 600 Harry Drive, from Thanksgiving night, November 26, through December 24 (new this year, Christmas Eve is included). More than 400,000 lights line a route of over half a mile, including a 300-foot lighted tunnel. Drive-through-only nights are $10 a vehicle; nights with Santa's Village open are $20 or $25 a vehicle, and online or card purchases carry a booking fee. Hours through December 17 are 5:30&ndash;8:30 p.m. Sunday to Thursday and 5:30&ndash;9:30 p.m. Friday and Saturday, then 5:30&ndash;9:30 nightly through Christmas Eve. The Santa Shuffle fun run is December 8.||<b>Foundation of Arts</b> in downtown Jonesboro marked the opening of a new mural and its renovated tap room with a ribbon-cutting. A-State's annual lecture-concert series welcomes Dr. Adam Feltz, speaking on ethical interactions."))
body.append('<h2 style="break-before:page;page-break-before:always">From the Police Reports</h2>')
body.append('<p class="note">Jonesboro Police incident reports. Charges are allegations. No names are printed.</p>')
body.append(P("<b>Friday through early Monday:</b> 75 reports were filed between Friday afternoon, November 6, and 8:19 a.m. Monday, with about 40 arrests, roughly half of them on warrants. No shootings, fires or serious-injury crashes appeared in this batch.||<b>Overnight Monday, a string of car break-ins</b> hit the Rains Street area, an apartment complex on East Cherry Avenue and Richmond Avenue between about 2 and 7 a.m. Windows were smashed, and at least one wallet was taken and its debit card used online. A white SUV was also reported stolen from a home on Mitzi Lane around the same hours, and a burglary on Mitzi Lane, discovered Sunday, involved four guns, cash and jewelry. No arrests yet. <i>Tip: lock the car, take guns and wallets indoors, and leave nothing visible.</i>||<b>Drunk driving:</b> three DWI arrests came out of crashes over the weekend. In the early hours of Saturday a driver was arrested after a wreck at East Oak Avenue and South Main Street that destroyed a retaining wall (felony criminal mischief and DWI). Late Saturday, a woman was arrested after a crash at a church property on Rains Street on charges including DWI, felony second-degree battery of a police officer and resisting arrest; she was charged again at the hospital with felony battery of medical personnel. Early Sunday, a driver in a vehicle taken without permission crashed on Marketplace Drive and was arrested on charges including DWI, felony criminal mischief, unauthorized use of a vehicle and a suspended license. Six hit-and-run reports, all misdemeanors, were filed, including at East Highland and South Caraway, near Highway 18 and Martin Luther King Jr. Drive and on South Caraway, with no arrests."))
body.append(P("<b>Drugs and warrants:</b> four people were arrested at a home near Chancery Lane and East Johnson Avenue on Sunday evening on drug-possession, paraphernalia and warrant charges, including a parole violation. Others were arrested at a motel lot on Phillips Drive (a felony Schedule II possession charge) and on a Friday night traffic stop near Race Street and Red Wolf Boulevard, where an officer says a man swallowed methamphetamine (tampering with evidence, a felony). About 14 people were arrested on warrants for unpaid fines or failures to appear, and two more were cited.||<b>Domestic cases:</b> about a dozen family-violence reports were filed. Felony second-degree domestic battering arrests were made in the 72405 area on Sunday morning and in the 72401 area on Sunday, the latter on a warrant, and a Monday-morning call in the 72405 area ended with two arrests on battery and child-endangerment charges. Several no-contact or protection-order violations were also reported.||<b>Fraud:</b> a man in the 72404 area reported wiring $5,000 to a stranger as a &ldquo;tractor deposit&rdquo; and losing it (felony theft); never wire money to someone you have not met. Two video game consoles were taken from a store on East Highland Drive using a fake payment app. A weekend of juvenile-related reports, including a fight in the 72401 area, and two sexual-offense reports are on file with detectives; no further details are printed."))
body.append('<p class="note">At the county jails</p>')
body.append(P("In Craighead County, the sheriff's roster shows 300 people held, 31 of them booked in the last 48 hours; among those listed first, failures to appear and a firearms-possession charge were common. In Randolph County (Pocahontas), 60 people are held, one booking in the last two days and six releases, with drug and warrant charges leading among the newest bookings. Being on a roster does not mean a person was convicted."))
body.append('<h2>From the State</h2>')
body.append('<h3>What the 2026 campaigns cost</h3>')
body.append(P("Arkansas's two statewide races together drew more than $25 million in reported spending, according to a Jonesboro Right Now analysis of campaign-finance data. Gov. Sarah Huckabee Sanders, who won a second term with about 54 percent, spent roughly $5.7 million by one tracker's count, about $12 for each vote she received; another tally, drawn from state ethics filings, puts her at about $9.9 million. Her Democratic opponent, state Sen. Fred Love, reported about $206,000 to $296,000, depending on the source.||In the U.S. Senate race, Republican Sen. Tom Cotton, also at about 54 percent, reported $15.8 million through October 14 against $3.3 million for Democrat Hallie Shoffner. The article cautions that the figures are preliminary and leave out outside groups' spending, which in the Senate race ran to millions of dollars."))
body.append('<h3>Democrats say a smaller majority means more leverage on the budget</h3>')
body.append(P("With Republicans holding a 70-30 House majority after Tuesday's election, down from a supermajority, most appropriations bills, which need three-fourths of both chambers, will now require some Democratic votes, House Minority Leader Andrew Collins told the Arkansas Times. He said Democrats will not automatically block spending bills but will fight policies they oppose. Governor Sanders's office said she will keep her focus on education, public safety and tax cuts and work with both parties where priorities align. The Governor's $6.97 billion budget plan now goes to the legislature, which meets in January."))
body.append('<h2>From the Nation</h2>')
body.append('<h3>Congress returns; the Hegseth impeachment vote looms</h3>')
body.append(P("Congress came back Monday for a lame-duck session, the stretch between the November election and the swearing-in of the new members in January. Democrats won both chambers and will take control next year. At the top of the to-do list is a government funding bill to head off a shutdown in December; the debt limit is also on the agenda, according to CNBC.||Kentucky Republican Rep. Thomas Massie reintroduced articles of impeachment against Defense Secretary Pete Hegseth on Monday, which under House rules requires leaders to act within two legislative days, so a vote is expected by week's end. Massie's earlier resolution lapsed in September when the House left for a recess. Republicans hold a narrow 218-214 majority, and Democratic leader Hakeem Jeffries has called himself a &ldquo;hard yes.&rdquo; Impeachment needs only a simple House majority; conviction would take two-thirds of the Senate. Hegseth has dismissed the effort."))
body.append('<h3>Trump: Iran standoff stays at the &ldquo;status quo&rdquo;</h3>')
body.append(P("President Trump told reporters at an impromptu White House briefing that the United States will hold the war with Iran, which began with American and Israeli strikes in February, at the &ldquo;status quo&rdquo; while talks continue, though he warned that American forces are &ldquo;locked and loaded.&rdquo; Secretary of State Marco Rubio said Sunday that talks are not on the verge of a breakthrough because Iran's demands are unacceptable. Iran says it is still talking through mediators in Qatar and Pakistan, and Qatar's prime minister was due at the White House to discuss a possible deal on the Strait of Hormuz, the shipping lane through which a large share of the world's oil passes. Oil prices fell sharply on the news (see Markets)."))
body.append('<h2>From Abroad</h2>')
body.append('<h3>G7 ministers press Rubio on Iran and Ukraine</h3>')
body.append(P("Foreign ministers of the Group of Seven, the club of leading industrial democracies, opened a two-day meeting in Paris on Monday. It is Rubio's first major trip overseas since the U.S. elections. European ministers want assurances that any settlement of Russia's war in Ukraine is fair to Kyiv, and Ukraine's foreign minister, Andriy Sybiha, joined the Ukraine session today. Germany's foreign minister, Johann Wadephul, said the talks would also look at ways to avoid military escalation with Iran.||Separately, U.S.-mediated talks involving Ukraine and Russia are scheduled in Abu Dhabi, in the United Arab Emirates, for Tuesday and Wednesday. The United States takes over the G7 presidency from France in 2027."))
body.append('<h2>Markets &amp; the Farm</h2>')
body.append('<p class="note">Figures are for Monday&rsquo;s close, November 9. Index levels agree across CNBC and other reports; small differences in oil quotes are noted below.</p>')
body.append('''<table class="mk"><tr><th>Index</th><th>Close</th><th>Day</th></tr>
<tr><td>S&amp;P 500</td><td class="n">7,549.94</td><td class="n">+2.35%</td></tr>
<tr><td>Dow Jones Industrials</td><td class="n">52,389.75</td><td class="n">+2.15%</td></tr>
<tr><td>Nasdaq Composite</td><td class="n">25,253.14</td><td class="n">+2.74%</td></tr></table>''')
body.append(P("Stocks bounced hard on Monday, the S&amp;P 500's best day since April 8, after last week's sell-off over worries that the artificial-intelligence build-out could slow. Oil fell sharply on hopes of a deal with Iran, and chip stocks led the way, with a semiconductor fund up more than 7 percent. Nvidia fell about 4 percent after its board opened an investigation into its chief executive's relationship with a woman U.S. intelligence agencies describe as a Chinese spy. The S&amp;P is still about 3.4 percent below its October record. Today brings the October consumer price index (inflation report) at 8:30 a.m. Eastern; Producer prices come Friday, and Nvidia reports November 17. The Dow is now above its Election Day close; the S&amp;P and Nasdaq are not yet."))
body.append('<h3>What analysts are saying</h3>')
body.append(P("Analysts leaned toward buying <b>Advanced Micro Devices (AMD)</b>, the chip maker: Oppenheimer upgraded it to Outperform with a $600 target, raising estimates after a strong earnings call (risk: chip stocks have swung violently this month). They also upgraded <b>Rollins (ROL)</b>, the pest-control company, with Citi moving to Buy and lifting its target to $49 from $32 on solid demand and steady acquisitions (risk: it relies on continued deal-making). JPMorgan upgraded <b>SAP</b>, the business-software firm, to Overweight, arguing that artificial intelligence is moving from pilot projects to real use (risk: AI spending could slow).||Analysts turned cautious on <b>Molson Coors (TAP)</b>, the brewer: JPMorgan cut it to Underweight, trimming its target to $37 from $41 after third-quarter results (risk: the stock may already reflect the bad news). Stifel downgraded <b>DraftKings (DKNG)</b>, the sports-betting company, to Hold with a target of $21, down from $32; the reports we saw did not give the reason (risk: unknown). Nvidia was split: Aletheia cut it to Hold while Bernstein stuck with Outperform. Calls drawn from CNBC and 24/7 Wall St. This is information, not advice."))
body.append('''<table class="mk split"><tr><th>Commodity</th><th>Close</th><th>Change</th></tr>
<tr><td>Crude oil, WTI</td><td class="n">$86.85</td><td class="n">&minus;$3.98</td></tr>
<tr><td>Crude oil, Brent</td><td class="n">$92.57</td><td class="n">&minus;5.85%</td></tr>
<tr><td>Gasoline, Arkansas average (regular), AAA Nov. 5</td><td class="n">$3.71</td><td class="n">&minus;$0.09, week</td></tr>
<tr><td>Live cattle (Dec.)</td><td class="n">$216.20</td><td class="n">+$2.15</td></tr>
<tr><td>Feeder cattle (Jan.)</td><td class="n">$324.17</td><td class="n">+$5.80</td></tr>
<tr><td>Lean hogs (Dec.)</td><td class="n">$55.87</td><td class="n">+$2.35</td></tr>
<tr><td>Corn (Dec.), per bushel</td><td class="n">$4.3925</td><td class="n">&minus;2&frac14;&cent;</td></tr>
<tr><td>Soybeans (Jan.), per bushel</td><td class="n">$11.8225</td><td class="n">&minus;6&frac34;&cent;</td></tr>
<tr><td>Wheat, Chicago (Dec.), per bushel</td><td class="n">$5.88</td><td class="n">&minus;3&frac14;&cent;</td></tr>
<tr><td>Cotton (Dec.), cents per pound</td><td class="n">78.78</td><td class="n">&minus;0.33</td></tr>
<tr><td>Rice (Jan.), per hundredweight</td><td class="n">$18.15</td><td class="n">&minus;10&frac12;&cent;</td></tr></table>''')
body.append(P("Crude oil's WTI price is from Brownfield and CNBC, which agree; Brent is CNBC's figure (another report had it a few cents higher). Arkansas gasoline is AAA's Thursday figure, with prices easing as crude has slipped. The Jonesboro metro average was not available for this week and is omitted. Grain and livestock lines come from a single source (Brownfield Ag News)."))
body.append('<h2>On the Field</h2>')
body.append(P("<b>Arkansas State football</b> (4-5, 2-3 in the Sun Belt Conference after Saturday's 19-17 home loss to Louisiana-Monroe) plays at Coastal Carolina this Saturday, November 14, at noon Central. <b>Arkansas</b> (3-6, 1-5 in the SEC, after a 26-23 loss at Auburn) hosts South Carolina Saturday at 6:45 p.m. on the SEC Network, then visits Texas on November 21. <b>Tennessee</b> (7-2) beat Kentucky 34-6 Saturday and visits Texas A&amp;M on Saturday at 3 p.m. Eastern on ESPN.||<b>A-State men&rsquo;s basketball</b> opened the season on November 2 against Toledo and played at Alabama on November 6, with home games coming against UT Martin, Dillard and Arkansas-Pine Bluff (check astateredwolves.com for dates and results)."))
body.append('<h2>Afield &amp; Afloat</h2>')
body.append('<p class="note">Ratings are rule-of-thumb estimates from the forecast, the rut calendar and the sun, not measurements of animal or fish behavior.</p>')
body.append('<h3>Deer outlook: Good</h3>')
body.append(P("The rut is at its peak, dawn is a crisp 40 degrees and the wind is nearly calm, with a slow fall in pressure ahead of Wednesday's warmth, all in the hunter's favor; the warm afternoon near 69 is the only drawback. Be settled by first light at 6:06 a.m. and hunt until about 8:30, then sit again from about 3:00 p.m. to sunset at 4:58. In the peak of the rut, 10 a.m. to 2 p.m. is realistic too, with bucks cruising.||<b>Today's tip:</b> bowhunters should get to the stand before the first light and stay quiet; with air this still, your scent will pool and drift unpredictably, so keep a cover scent bag or pick a stand with a creek or thicket behind you. Remember that only archery is open this week; modern gun opens Saturday."))
body.append(P("<b>Tomorrow, Wednesday (estimate: Good):</b> dawn near 49, a warm afternoon near 75 and a southerly wind rising to about 13 mph by evening. Watch about 6:05 to 8:35 a.m. and 2:57 to 4:57 p.m. <b>Tomorrow's tip:</b> the warm afternoon will push deer into shade, so favor the morning sit and the thick bedding cover on the downwind side of a field."))
body.append('<h3>Fishing outlook: Good</h3>')
body.append(P("At the Crowley's Ridge lakes (Craighead Forest Lake, Lake Frierson), steady pressure and a mild afternoon make a good day: fish late morning through mid-afternoon as the shallows warm, then again in the last hour before sunset at 4:58.||<b>Today's tip:</b> crappie are moving to deeper brush and docks as the water cools; try small minnows or 1/16-ounce jigs under a float at 8 to 12 feet, and slow-roll a spinnerbait along wood for bass."))
body.append(P("<b>Tomorrow, Wednesday (estimate: Fair):</b> pressure drops fast ahead of the cold front, which fish tend not to like. Late morning to mid-afternoon is best, with a second window before sunset at 4:57. <b>Tomorrow's tip:</b> fish slowly and a bit deeper, and expect wind to stir the surface by afternoon."))
body.append('<h3>In season now, and what is next (zones 3, 4, 6 and 8)</h3>')
body.append('''<table class="mk"><tr><th>Zone</th><th>Archery</th><th>Youth gun</th><th>Modern gun</th><th>Muzzleloader</th></tr>
<tr><td>3</td><td>open to Feb. 28</td><td>Jan. 2&ndash;3</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr>
<tr><td>4</td><td>open to Feb. 28</td><td>Jan. 2&ndash;3</td><td>Nov. 14&ndash;22; Dec. 26&ndash;28</td><td>closed</td></tr>
<tr><td>6</td><td>open to Feb. 28</td><td>Jan. 2&ndash;3</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr>
<tr><td>8</td><td>open to Feb. 28</td><td>Jan. 2&ndash;3</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr></table>''')
body.append(P("<b>Open now:</b> archery season, since September 26 through February 28 in all four zones. The first youth gun hunt was last weekend; the second is January 2&ndash;3.||<b>Saturday, November 14,</b> modern gun season opens in all four zones, four days away. Zone 4, which includes Craighead County, closes November 22, while Zones 3, 6 and 8 run to December 6. Bag limit in these zones is four deer, no more than two bucks. Dogs are allowed for deer in Zones 6 and 8 during modern gun season but not in Zones 3 and 4. Craighead is in the Chronic Wasting Disease regulation area; the free CWD testing AGFC offers is described at agfc.com.||<b>Waterfowl:</b> duck, coot and merganser season opens Saturday, November 21 and runs November 21&ndash;29, December 10&ndash;23 and December 26 to January 31; Canada geese follow the same segments. The youth and veterans waterfowl hunt is February 6&ndash;7. Check agfc.com for small-game dates."))
body.append('<h2>Postscript</h2>')
body.append('<p class="ps">They shall grow not old, as we that are left grow old:<br>Age shall not weary them, nor the years condemn.<br>At the going down of the sun and in the morning<br>We will remember them.</p>')
body.append('<p class="ps">&mdash; Laurence Binyon, &ldquo;For the Fallen&rdquo; (1914). Written in the first weeks of the Great War; spoken each year on Remembrance Day, the Armistice anniversary we know as Veterans Day, tomorrow.</p>')
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
