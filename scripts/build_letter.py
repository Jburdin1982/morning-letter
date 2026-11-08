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
body.append('<div class="date">Saturday, the Seventh of November, 2026</div><div class="orn">&#10086;</div>')
body.append(P('Good morning,'))
body.append(P("A grey, mild Saturday is on offer, with Arkansas State at home this afternoon and the whole country still sorting out the week's election. Here is the news, set down as plainly as we can manage it."))

# Weather
body.append('<h2>The Day Ahead</h2>')
body.append(hourly); body.append(grid)
body.append(P("Today stays under a blanket of cloud, with a high near 56 and no rain in the forecast; the evening clears a little before clouding over again, and the low settles near 41.||Sunday begins cold, near 36 degrees, with the chance of morning fog, then brightens into a sunny afternoon around 61. The warm spell builds after that: the upper 60s Monday and the low 70s Tuesday and Wednesday. A chance of showers, about one in five, comes Wednesday afternoon and lingers into Thursday, and Friday turns crisp, with a high near 49 and a low in the 30s."))

# Almanac
body.append('<h2>The Almanac</h2>')
body.append(f'''<table class="alm"><tr><td>First light</td><td>{alm['first_light']}</td><td>Sunrise</td><td>{alm['sunrise']}</td></tr>
<tr><td>Solar noon</td><td>{alm['noon']}</td><td>Sunset</td><td>{alm['sunset']}</td></tr>
<tr><td>Last light</td><td>{alm['last_light']}</td><td>Length of day</td><td>{alm['day_length']}</td></tr>
<tr><td>Change from yesterday</td><td>{alm['change'].replace('-','&minus;')}</td><td>Moon</td><td>{alm['moon']}, {alm['illum']}% lit</td></tr></table>''')
body.append(P("The days continue to shorten, now by nearly two minutes each morning, and with the clocks turned back last weekend the sun is gone by a few minutes past five. The old moon is a thin sliver before dawn this week; the new moon comes around Monday or Tuesday, which makes the coming nights fine ones for looking at stars if the clouds break."))
body.append(P("In the country this week, the cotton pickers and rice combines have mostly gone quiet and the soybean fields are about done; drilling winter wheat and spreading lime are the jobs that remain.||In the garden it is the season for planting garlic and spring bulbs, raking and composting leaves, and mulching beds before the first hard freeze, which Sunday's near-freezing morning may preview in the low spots. Along the woods and sloughs the ducks are moving down the flyway; if you are heading out, check the current seasons and licence rules with the Arkansas Game and Fish Commission before you go."))

# Local
body.append('<h2>Of Local Interest</h2>')
body.append('<h3>Jonesboro bans camping in city parks and parking lots</h3>')
body.append(P("The Jonesboro City Council voted 10 to 0 on Thursday to adopt Ordinance 26-038, which bars camping in city parks and city parking lots except in areas the city designates for it. The ordinance defines camping as setting up a tent or other shelter, or laying out a sleeping bag or bedding, for overnight use. A first violation carries a fine of at least $100, police and code-enforcement officers may remove violators and their belongings, and the city can issue a special permit for camping during a special event.||City Attorney Carol Duncan said the rule also covers RV camping and described it as a starting point for keeping people in designated camping areas as the city expands its parks.||The council passed it without discussion; two members, John Street and Dr. Anthony Coleman, were absent, and the meeting had been moved from Tuesday to Thursday because of the general election. Reports did not say when the ordinance takes effect or where the designated camping areas will be."))
body.append('<h3>Century-old bank building burns at Trumann</h3>')
body.append(P("Fire destroyed the old Bank of Trumann building in Trumann, a city of about 7,400 in Poinsett County, on Monday night. Crews were sent out at about 8:07 p.m. and fought the blaze from outside for roughly three hours, using an estimated 150,000 to 200,000 gallons of water to protect neighboring buildings. The building dated from the early 1920s and had been vacant and deteriorating for decades.||Investigators from the Trumann Fire and Police Departments believe human activity started the fire on the second floor but have not said whether it was deliberate or accidental. No deaths were reported, but a cracked exterior wall fell during the fight and bricks struck several firefighters; Fire Chief Revis Kemper called it a close call, saying the wall missed by a foot or two.||Mayor Jay Paul Woods said the owner lives in New York and ignored the city's letters demanding cleanup and security. The building contains asbestos, and Woods put cleanup at about $40,000 on a lot he values near $1,000. City crews have pushed down the unstable walls, and anyone with information is asked to call the Trumann Police Department."))
body.append('<h3>Fatal shooting on Preakness Drive</h3>')
body.append(P("Jonesboro police are investigating a shooting at a home in the 3400 block of Preakness Drive in south Jonesboro, which happened at about 3:45 p.m. Wednesday. Police identified Kayunte Sanders, 31, as the person who died and also as a suspect; Jasmine Anderson, 27, was shot in the hand and wrist, and Devandre James, 28, is listed as a victim in the report. According to the incident report, a man came to the home with a gun and began beating a victim, and shots followed. Police spokesperson Sally Smith said a person of interest was taken into custody, but no charges have been filed. The investigation is continuing."))
body.append('<h3>Couple sues the city over a steakhouse permit</h3>')
body.append(P("Michael Shannon Kee and Elaine Kee of Jonesboro have sued the city in Craighead County Circuit Court after the City Council refused them a private-club permit, which allows a restaurant to serve alcohol. The couple planned 141 Prime, an upscale steakhouse at 2740 N. Church St., and applied on August 24; the council denied the application on October 20, and according to the lawsuit members cited the restaurant&rsquo;s nearness to a school. The suit, filed November 3, calls the denial &ldquo;arbitrary and capricious,&rdquo; says the application met every requirement, and says other establishments near schools have been approved. It asks the court to reverse the decision. The city&rsquo;s response was not included in the reports."))
body.append('<h3>Votes counted, results unofficial</h3>')
body.append(P("Voters in Black Rock, in Lawrence County, rejected a half-cent city sales tax on Tuesday, with 62 percent against, according to KAIT. Police Chief Bryan Archer said the money would have helped lower water rates and let the town match grants for a tornado siren, a walking trail and a playground. He said the city budget is tight after losing businesses, including its only grocery store, and paying for storm repairs, and that without the new revenue matching grants may be harder to pursue. These totals are unofficial until county election commissions certify them."))
body.append('<h3>Courts and public safety</h3>')
body.append(P("Anthony Keaton Graves, 35, of Jonesboro, received a 60-year prison term under a plea agreement, Jonesboro Right Now and KAIT reported Friday. Circuit Judge Randy Philhours imposed six consecutive 120-month terms for six counts of possessing or distributing child sexual abuse material, with further counts carrying suspended sentences, and Graves must register as a sex offender.||Police said the case began with an FBI tip to the Jonesboro Police Department&rsquo;s Internet Crimes Against Children unit, which led to a SWAT search of his home.||Separately, the owner of an Exxon station at 3109 Dr. Martin Luther King Jr. Drive, Mirzali Lakhani, is charged with one felony count of possessing a controlled substance after state regulatory police said they found 62 kratom pills (31 two-pill packages) for sale on November 5. Arkansas lists two kratom compounds as Schedule I controlled substances. Mr. Lakhani cooperated with the search, was released on his own recognizance and is due in Craighead County Circuit Court on January 25. Charges are allegations, and he is presumed innocent."))
body.append('<h3>Pantry short on turkeys; food drive set for Nov. 20</h3>')
body.append(P("Helping Neighbor Food Pantry in Jonesboro has fewer turkeys than clients this Thanksgiving, so staff hold a drawing each Tuesday and Thursday shift for the few it has. Coordinator Elizabeth Ivener said it has been a difficult year for pantries and the families they serve, with donations trailing demand, less food arriving since cuts to federal commodity programs, and inflation straining households.||The 19th annual Fill the Food Bank drive runs 6 a.m. to 6 p.m. on November 20 at the Walmart on Highland Drive in Jonesboro, and organizers are asking for nonperishable food. Other drop-off sites include Harps at 8107 U.S. 49 N. in Brookland, plus Walmarts in Paragould, Walnut Ridge, Newport, Blytheville and Osceola. Families seeking help can find a nearby pantry on the &ldquo;find food&rdquo; map at foodbankofnea.org."))
body.append('<h3>Around town</h3>')
body.append(P("A-State&rsquo;s third annual Catalyst event drew about 500 to 600 people to the Embassy Suites in Jonesboro on Thursday for a panel of professors, industry leaders and students on what employers want and what careers look like after graduation; Chancellor Calvin White Jr. said he hopes next year&rsquo;s gathering is bigger.||Two seasonal events fall today: Artsy&rsquo;s Magical Christmas Craft Show, 10 a.m. to 4 p.m. at the Hilton Garden Inn on South Caraway Road ($1 admission), and Christmas on the Farm at Jackson Farm, Highway 117, Black Rock, today and tomorrow. Next Friday, A-State Theatre opens <i>Little Shop of Horrors</i> at the Fowler Center, running November 13 to 22, with tickets at $15 to $20 and free for A-State students. The Jonesboro Public Schools Foundation awarded $75,000 in classroom grants to 44 teachers, and South Wind Heights assisted living is offering free meals to veterans through November. Drivers should expect overnight road closures for the Caraway Road expansion project, and residents may comment through December 11 on a federal study of a proposed national heritage area in eastern Arkansas."))

# State
body.append('<h2>From the State</h2>')
body.append('<h3>Governor Sanders presents a $6.97 billion budget</h3>')
body.append(P("Gov. Sarah Huckabee Sanders, a Republican elected to a second term on Tuesday with about 54 percent of the vote, presented her proposed 2027-28 state budget to lawmakers on Friday. The plan totals $6,969,073,258, an increase of about $311.6 million, or 3.94 percent, over the current year. It adds $70 million for Education Freedom Accounts, the state's school-choice program, which the governor said more than 50,000 students use, and $20 million for early childhood education.||From one-time surplus money (last year's surplus was $655 million), she proposes $50 million for the State Water Plan and $50 million toward a possible state share of SNAP, the federal food-assistance program, and she directs $75 million a year in interest earnings to Medicaid. Sanders said the plan leaves room for another income-tax cut.||The legislature, where Democrats broke the Republican supermajority in the state House on Tuesday, must still pass the budget when it convenes."))
body.append('<h3>Former bar-exam official charged with altering scores</h3>')
body.append(P("Nancie Givens, the former executive director of the Arkansas Supreme Court&rsquo;s Office of Professional Programs, which keeps bar-exam records, was arrested Thursday on 65 counts of tampering with a public record, each a Class C felony, Sixth Judicial District Prosecuting Attorney Will Jones announced. Investigators allege she moved points from some test-takers&rsquo; scores to others&rsquo; on the same exam, lifting some to or above the passing score of 270, and that records were altered or destroyed; a court review found discrepancies in at least eight testing rounds between July 2020 and July 2025.||Ms. Givens resigned in February. Her successor, Robert Brech, found about 11,400 files had been deleted or made inaccessible in January, many of them records required to be kept for 25 years. The Arkansas State Police and FBI have investigated since April.||She pleaded not guilty Wednesday in Little Rock District Court, and on Thursday a panel of the court&rsquo;s professional-conduct committee suspended her from practicing law. The state&rsquo;s justices said most people told they passed did pass, and that affected test-takers will be notified once results are confirmed. The charges are allegations."))
body.append('<h3>Issue 3 fails; Northeast Arkansas mostly voted yes</h3>')
body.append(P("Issue 3, which would have created new economic-development zones, each with its own governing board, failed in uncertified statewide returns. Supporters pitched it as a tool for small, rural counties, and experts told KAIT many voters were unsure what it would do. Forty-one of the state&rsquo;s 75 counties voted for it, mostly in the Delta and the South, while larger counties such as Pulaski, Washington and Faulkner voted no. Most of Northeast Arkansas supported it; Randolph County was the exception, voting no with 51 percent. County election commissions must still certify the results."))
body.append('<h3>$8.4 million from the Monsanto settlement for 21 water projects</h3>')
body.append(P("Attorney General Tim Griffin announced Friday that $8.4 million from the state&rsquo;s settlement with Monsanto will pay for 21 waterway projects. The October 2 settlement resolved claims that PCBs, industrial chemicals made by Monsanto, contaminated the environment, and it restricts the money to water-quality work such as erosion control and habitat restoration. The Arkansas Game and Fish Commission will administer $6.7 million for 17 projects, including $1 million each for the Eleven Point River in Randolph County and Crooked Creek in Baxter County; four other projects share $1.7 million, led by $1 million for Bayou Bartholomew. No timeline was given."))
body.append('<h3>Governor names appointees, including Jonesboro residents</h3>')
body.append(P("Governor Sanders announced dozens of board appointments Friday. Among them, Andrea Allen of Jonesboro will chair the 2030 Arkansas Complete Count Committee, a panel to encourage participation in the 2030 census, joined by Gina Gomez of Jonesboro; Landon Wilson of Jonesboro joins the Pollution Control and Ecology Commission; and Dr. Todd Higginbotham of Jonesboro joins the State Board of Dental Examiners.||Matt Jones of Blytheville was named to the Board of Dispensing Opticians and Seth Holifield of Blytheville to the Blytheville-Gosnell Regional Airport Authority."))

# Nation
body.append('<h2>From the Nation</h2>')
body.append('<h3>Democrats win both chambers of Congress</h3>')
body.append(P("Democrats won control of both the U.S. House and Senate in Tuesday's midterm elections, ending the Republican Party's control of all three of the White House, the Senate and the House. By Associated Press counts reported midweek, Democrats led 225 to 137 in the House with 73 races still uncalled, and held 54 Senate seats to the Republicans' 44 with two undecided; one of those, in Mississippi, was razor-close between Democrat Scott Colom and Republican Sen. Cindy Hyde-Smith. National Public Radio reports that Rep. Hakeem Jeffries of New York, the House Democratic leader, is poised to become the first Black Speaker.||Democrats also say they will widen investigations into the fatal shootings of Renee Good and Alex Pretti by immigration agents during a federal enforcement surge in Minneapolis last winter. President Trump said on <i>60 Minutes</i> that he plans Cabinet changes after the losses."))
body.append('<h3>Stephen Miller named White House chief of staff</h3>')
body.append(P("Mr. Trump has named Stephen Miller, until now his deputy chief of staff for policy and homeland security adviser, as White House chief of staff, replacing Susie Wiles. Ms. Wiles, who managed Mr. Trump's 2024 campaign, was the first woman to hold the post. Mr. Miller has been a driving force behind the administration's immigration policy, including expanded deportations. Before the election Mr. Trump had publicly expressed full confidence in Ms. Wiles; the change was announced after the vote."))
body.append('<h3>Measles cases pass 5,000</h3>')
body.append(P("The Centers for Disease Control and Prevention reports more than 5,000 confirmed measles cases in the United States, ABC News reported Saturday. Measles is a highly contagious viral illness that vaccination prevents; health officials generally urge families to check that children's MMR shots are up to date."))

# Abroad
body.append('<h2>From Abroad</h2>')
body.append('<h3>Iran: strikes, a blockade and talks</h3>')
body.append(P("The United States and Iran remain in a standoff that began with a US-Israeli war on Iran this year; a ceasefire collapsed in June. President Trump says US forces carried out another round of what he called minor strikes on Iran, and Iranian media reported two missiles hitting Qeshm Island in the Strait of Hormuz, the narrow waterway through which much of the world's oil moves. The US Navy is blockading Iranian shipping, and US Central Command (the military command covering the Middle East) said it is creating a task force to restrict Iran's overland trade as well, and offered a $20 million reward for information on Iran's nuclear program.||At the same time, reports of progress in talks sent oil prices sharply lower this week; Iran says it will not fully reopen the Strait until the blockade is lifted, sanctions are eased and frozen assets are released. No agreement has been announced."))
body.append('<h3>Ukraine: new talks set for Tuesday</h3>')
body.append(P("Missiles struck Kyiv early Saturday and wounded at least five people, the Associated Press reported, days before negotiators from Russia, Ukraine and the United States are due to meet in Abu Dhabi, the capital of the United Arab Emirates, on Tuesday. Russian President Vladimir Putin confirmed the meeting. Separately, Beijing has confirmed that a summit among Chinese President Xi Jinping, Mr. Trump and Mr. Putin is under discussion, according to The Guardian's briefing; no date has been given."))
body.append('<h3>Bomb threats disrupt European air travel</h3>')
body.append(P("Bomb threats have targeted flights, airports and media outlets in at least five European countries, Anadolu Agency reported. Authorities have not publicly said who is behind them. Travelers in affected countries should expect delays and extra security checks."))
body.append('<h3>Paraguay\'s president impeached</h3>')
body.append(P("Paraguay's Congress impeached President Santiago Pe&ntilde;a, and The Guardian reports he was detained minutes later as protesters demanded answers over the suspension of the Ueno bank; another outlet describes his status as house arrest. Reporting so far is thin and the details may change."))

# Markets
body.append('<h2>Markets &amp; the Farm</h2>')
body.append('<p class="note">Figures are as of Friday&rsquo;s close, November 6.</p>')
body.append('''<table class="mk"><tr><th>Index</th><th>Close</th><th>Change</th><th>Week</th></tr>
<tr><td>S&amp;P 500</td><td class="n">7,376.86</td><td class="n">+0.31%</td><td class="n">&minus;2.68%</td></tr>
<tr><td>Dow Jones Industrials</td><td class="n">51,285.73</td><td class="n">&minus;0.46%</td><td class="n">&minus;0.94%</td></tr>
<tr><td>Nasdaq Composite</td><td class="n">24,579.42</td><td class="n">+1.09%</td><td class="n">&minus;3.37%</td></tr></table>''')
body.append(P("Stocks steadied on Friday after Thursday's rout, the worst day for the major averages since the April 2025 tariff sell-off, when the S&amp;P 500 fell 4.4 percent and the Nasdaq slid into a correction (a drop of more than 10 percent from its high). Investors blamed fears that Democratic election wins would bring tighter regulation of artificial intelligence, along with worry over stretched valuations in AI-related companies.||On Friday, technology and chip shares bounced and a stronger-than-expected October jobs report added to the mix; the S&amp;P 500 still finished the week down about 2.7 percent, its worst since the April 2025 tariff week. Investors are now watching Tuesday's consumer-price report and the coming earnings from Nvidia, the AI chip leader."))
body.append('<h3>What analysts are saying</h3>')
body.append(P("Brokerage analysts changed their views on several well-known companies on Friday. <b>Analysts leaned toward buying:</b>"))
body.append('<ul class="picks">'
'<li><b>Becton Dickinson (BDX)</b>, a maker of syringes, medical devices and diagnostic tests. Wells Fargo raised it to Overweight (buy-leaning) from Equal Weight, citing growth upside, and lifted its price target to $242 from $170. <i>Risk:</i> the target jumped far above the old one, so expectations are now higher to meet.</li>'
'<li><b>SiTime (SITM)</b>, which makes precision timing chips, the tiny &ldquo;clocks&rdquo; inside electronics. Seaport upgraded it to Buy with a $425 target, arguing the AI-driven chip cycle is not over and the recent sell-off was overdone. <i>Risk:</i> the call rests on AI demand holding up, the very worry that hit tech stocks this week.</li>'
'<li><b>Centrus Energy (LEU)</b>, which supplies enriched uranium fuel for nuclear power plants. Roth upgraded it to Buy from Neutral with a $115 target after the shares fell sharply, saying an acquisition of Westerman offsets a looming revenue decline. <i>Risk:</i> that revenue decline still has to be offset.</li></ul>')
body.append(P("<b>Analysts turned cautious:</b>"))
body.append('<ul class="picks">'
'<li><b>Molson Coors (TAP)</b>, the brewer behind Coors and Miller. Wells Fargo cut it to Underweight from Equal Weight, citing &ldquo;earnings risk,&rdquo; with a $36 target that implies about 15 percent downside. <i>Risk to the call:</i> if earnings hold up better than Wells expects, the cautious view could prove wrong.</li>'
'<li><b>TripAdvisor (TRIP)</b>, the travel-review and booking site. Bank of America downgraded it to Underperform from Buy, saying growth is slowing. <i>Risk to the call:</i> a sudden pickup in bookings would undercut it. <i>(Single source: CNBC.)</i></li></ul>')
body.append(P("Molson Coors, Becton Dickinson, SiTime and Centrus appeared in at least two or three of the daily analyst roundups checked (CNBC, Yahoo Finance/The Fly, 24/7 Wall St., Daily Trade Alert, Quantisnow). Analysts are often wrong, and the stocks may already have moved. This is information, not advice."))
body.append('''<table class="mk"><tr><th>Commodity</th><th>Latest</th><th>Change</th></tr>
<tr><td>Crude oil, WTI (Dec.)</td><td class="n">$90.83</td><td class="n">+$0.31</td></tr>
<tr><td>Crude oil, Brent (Jan.)</td><td class="n">$98.32</td><td class="n">+$0.03</td></tr>
<tr><td>Gasoline, Arkansas average (regular), week</td><td class="n">$3.71</td><td class="n">&minus;$0.09</td></tr>
<tr><td>Gasoline, Jonesboro metro average, week</td><td class="n">$3.63</td><td class="n">&minus;$0.10</td></tr>
<tr><td>Live cattle (Dec.)</td><td class="n">$214.05</td><td class="n">&minus;$0.35</td></tr>
<tr><td>Feeder cattle (Jan.)</td><td class="n">$318.37</td><td class="n">&minus;$1.95</td></tr>
<tr><td>Lean hogs (Dec.)</td><td class="n">$53.52</td><td class="n">&minus;$1.57</td></tr>
<tr><td>Corn (Dec.), per bushel</td><td class="n">$4.415</td><td class="n">+1.5&cent;</td></tr>
<tr><td>Soybeans (Jan.), per bushel</td><td class="n">$11.9375</td><td class="n">+5.5&cent;</td></tr>
<tr><td>Wheat, Chicago (Dec.), per bushel</td><td class="n">$5.9125</td><td class="n">&minus;8&cent;</td></tr>
<tr><td>Cotton (Dec.), cents per pound</td><td class="n">79.11</td><td class="n">+0.40</td></tr></table>''')
body.append(P("||By CNBC's counts, Brent fell roughly 16 percent this week and WTI about 13 percent, among the steepest weekly drops in years, on hopes of a US-Iran deal; prices steadied Friday as tanker attacks continued. Cattle futures ended the week lower. Gasoline figures are from AAA&rsquo;s Thursday release (November 5), when the national average was $4.10, down 12 cents on the week. Rice is omitted today because no source dated Friday could be found. <i>(Grain, livestock and cotton prices: single source, Brownfield Ag News.)</i>"))

# Sports
body.append('<h2>On the Field</h2>')
body.append(P("<b>Arkansas State football</b> hosts Louisiana-Monroe (ULM) at Centennial Bank Stadium this afternoon, with kickoff listed at 2 p.m. and the game on ESPN+. It is the Red Wolves' first game since a bye week; they won their homecoming game on October 24, beating Georgia State 38-32. Head coach Butch Jones has said he hopes the team picks up where it left off. Still ahead: at Coastal Carolina on November 14, at Louisiana Tech on November 19 or 21 (sources differ), and Troy at home on November 28."))
body.append(P("<b>Men's basketball</b> opened its season Monday night with a win over Toledo, decided by a late free throw from Tameron Ferguson with the score tied in the final seconds."))
body.append(P("<b>Arkansas football</b> is scheduled to visit Auburn today, though the kickoff time was not confirmed in the sources checked, and then returns to Fayetteville to host South Carolina on November 14."))

# Outdoors
body.append('<h2>Afield &amp; Afloat</h2>')
body.append('<p class="note">Ratings are rule-of-thumb estimates from the forecast, the rut calendar and the sun, not measurements of animal or fish behavior.</p>')
body.append('<h3>Deer outlook: Fair</h3>')
body.append(P("The rut is only beginning in Northeast Arkansas. The Game and Fish Commission puts the average statewide peak of breeding around mid-November, a little later in the Delta, so bucks are starting to cruise but are not yet chasing hard. Today brings a cool dawn near 46 degrees, a light wind of 4 to 5 mph, heavy cloud and high pressure that climbed about 0.12 inches over the past day, so expect ordinary, steady movement rather than a banner day.||Best windows are first light, around 6:01 a.m. until about 8:30, and the last two hours of the day, 3:01 to 5:01 p.m. (sunrise is 6:31 and sunset 5:01). Tomorrow looks a shade better, with a colder Sunday dawn near 38 degrees."))
body.append(P("<b>Today&rsquo;s tip:</b> this is the youth modern-gun weekend, so put young hunters on a stand overlooking a field edge or a trail between thick cover and food, and favor the evening sit, when it is warmest and easiest on small hands and feet. With so little wind, keep scent in mind and approach the stand slowly and quietly."))
body.append(P("<b>Tomorrow, Sunday (estimate: Good):</b> a sharp cool-down brings a dawn near 38 degrees, with light wind and the rut moving into its peak window, so movement should be better than today. Hunt first light at 6:02 a.m. for about two hours, the evening from 3:00 to 5:00 p.m., and do not leave the stand early: 10 a.m. to 2 p.m. is realistic for bucks cruising.||<b>Tomorrow&rsquo;s tip:</b> it is the last day of the youth hunt, so keep young hunters on the warmest sit, and set up downwind of a trail or a bedding-to-food travel route, since cold, still mornings carry scent a long way."))
body.append('<h3>Fishing outlook: Good</h3>')
body.append(P("For the Crowley&rsquo;s Ridge lakes such as Craighead Forest Lake and Lake Frierson, a mild afternoon near 55 degrees, overcast skies and a light ripple on the water add up to a good day. Fish the late morning through mid-afternoon as the shallows warm, and again in the last hour before sunset.||<b>Today&rsquo;s tip:</b> as the water cools, slow everything down. Work small minnows or tiny jigs around brush piles and docks for crappie, and crawl a spinnerbait or crankbait along wind-touched banks and points for bass. These are general fall pointers; no current lake report was available."))
body.append(P("<b>Tomorrow, Sunday (estimate: Good):</b> steady pressure and a warmer afternoon near 62 degrees should have the shallows waking up. Fish late morning through mid-afternoon, with a second window in the last hour before sunset at 5:00 p.m.||<b>Tomorrow&rsquo;s tip:</b> with the afternoon warming after a cold dawn, look for crappie to move shallow near brush and docks, and try a slow-rolled spinnerbait on the sunny, wind-blown bank for bass."))
body.append('<h3>In season now, and what is next (zones 3, 4, 6 and 8)</h3>')
body.append('''<table class="mk"><tr><th>Zone</th><th>Archery</th><th>Youth gun</th><th>Modern gun</th><th>Muzzleloader</th></tr>
<tr><td>3</td><td>open to Feb. 28</td><td>Nov. 7&ndash;8</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr>
<tr><td>4</td><td>open to Feb. 28</td><td>Nov. 7&ndash;8</td><td>Nov. 14&ndash;22; Dec. 26&ndash;28</td><td>closed</td></tr>
<tr><td>6</td><td>open to Feb. 28</td><td>Nov. 7&ndash;8</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr>
<tr><td>8</td><td>open to Feb. 28</td><td>Nov. 7&ndash;8</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr></table>''')
body.append(P("<b>This weekend:</b> the Youth Modern Gun Deer Hunt runs today and tomorrow in all four zones, with a second weekend January 2&ndash;3. Archery season has been open since September 26 in all four zones.||<b>Next week:</b> modern gun season opens Saturday, November 14. Note that Zone 4 closes much sooner than the others, on November 22, with one antlerless deer allowed by modern gun there, while Zones 3, 6 and 8 run through December 6. Zone 4&rsquo;s chronic wasting disease rules cover Craighead County, so check them before you hunt, and dogs may be used for deer in Zones 6 and 8 from November 14 to December 6. The Christmas hunt, December 26&ndash;28, applies in all four zones."))
body.append(P("<b>Other seasons:</b> snow, blue, Ross&rsquo;s and white-fronted geese are open through tomorrow, November 8, and duck season opens November 21, running November 21&ndash;29, December 10&ndash;23 and December 26 to January 31. Quail season is open (November 1 to February 7, six a day), as are rabbit (to February 28, eight a day) and squirrel (to February 28, twelve a day). Turkey hunters wait for spring, with a youth hunt April 10&ndash;11 and the general season April 19 to May 9."))

# Postscript
body.append('<h2>Postscript</h2>')
body.append('<p class="ps">There is a particular quiet that settles over a November Saturday. The leaves are down, the harvest is in, and the light goes early enough that supper feels earned by four o&rsquo;clock. It is a fine season for a pot of something slow on the stove, for a porch chair with a blanket, and for ringing up the friend you keep meaning to call. The year is nearly done with its work; there is no shame in letting it rest.</p>')
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
