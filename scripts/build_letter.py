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
body.append('<div class="date">Monday, the Ninth of November, 2026</div><div class="orn">&#10086;</div>')
body.append(P('Good morning,'))
body.append(P("A cool, clear start to the week, with a warm afternoon on the way and the new moon overhead. The news is thick this morning: a White House shake-up, two Senate seats still undecided, a vote on impeaching the Defense Secretary expected in the House, and the Governor's first budget proposal in Little Rock. Here it is, as plainly as we can set it down."))
body.append('<h2>The Day Ahead</h2>')
body.append(hourly); body.append(grid)
body.append(P("Monday opens cold, about 40 degrees at dawn under a thin deck of cloud, then clears to a sunny, mild afternoon near 67 with a light breeze and no chance of rain. By evening it cools through the 50s toward a low near 39.||Tuesday is cloudier and warmer still, with a high near 71. Wednesday, Veterans Day, is the warmest day of the stretch, near 78 with a low of about 56 and a slim 16 percent chance of rain, before a cold front brings Thursday down to the low 60s and the weekend to the low 50s, with lows near freezing on Saturday morning."))
body.append('<h2>The Almanac</h2>')
body.append(f'''<table class="alm"><tr><td>First light</td><td>{alm['first_light']}</td><td>Sunrise</td><td>{alm['sunrise']}</td></tr>
<tr><td>Solar noon</td><td>{alm['noon']}</td><td>Sunset</td><td>{alm['sunset']}</td></tr>
<tr><td>Last light</td><td>{alm['last_light']}</td><td>Length of day</td><td>{alm['day_length']}</td></tr>
<tr><td>Change from yesterday</td><td>{alm['change'].replace('-','&minus;')}</td><td>Moon</td><td>{alm['moon']}, {alm['illum']}% lit</td></tr></table>''')
body.append(P("The moon is new today, which means no moonlight at all tonight and the best dark sky of the month for anyone who can get away from the streetlights. The Leonid meteors, bits of an old comet, peak around the 17th and 18th, and a slim crescent will be setting early by then.||In the garden this is garlic-planting time in Northeast Arkansas: push cloves a couple of inches deep, pointed end up, and mulch them with leaves. Spinach, kale and turnips are sweetest after a frost, and any tender potted plants should come inside before Saturday's near-freezing morning."))
body.append(P("Along the ridge and in the bottoms the sweetgums are at their deepest red and the pecans are dropping; squirrels are busy and the persimmons, soft now, are for the possums and the patient. White-throated sparrows have arrived to scratch under the feeders, and the first big flocks of wintering ducks are working the rice stubble at dusk. An old country saying holds that a heavy crop of acorns promises a hard winter. It is lore, not a forecast, and the squirrels do not seem to have heard it."))
body.append('<h2>Of Local Interest</h2>')
body.append('<h3>Governor names three Jonesboro residents to state boards</h3>')
body.append(P("Gov. Sarah Huckabee Sanders announced a long list of appointments to state boards and commissions on Friday, and three of those named are from Jonesboro, according to Jonesboro Right Now. Gina Gomez joins the new 2030 Arkansas Complete Count Committee, a panel set up to encourage everyone in the state to take part in the 2030 U.S. Census, since the population count affects federal funding and representation. Landon Wilson was named to the Arkansas Pollution Control and Ecology Commission, the board that makes the state's environmental rules, for a term ending March 29, 2030.||Dr. Todd Higginbotham was appointed to the Arkansas State Board of Dental Examiners, which licenses and disciplines dentists, replacing Cara Jones, for a term ending September 1, 2029. The committee's chair is Andrea Allen; the report does not say where she lives."))
body.append('<h3>Three men sentenced in A-State golf cart theft</h3>')
body.append(P("Three men accused of stealing a golf cart from Arkansas State University pleaded guilty to misdemeanor theft of property under $1,000 and first-degree criminal mischief and received suspended sentences, KAIT reported Sunday. Caleb Deshaun Quinn, Taris Durell Randolph and Robert Selvy, 23, each received 12 months of suspended imposition of sentence on each count, meaning the sentence is not served if they follow the court's terms. Each must also pay court costs, fines and fees in $75 monthly installments, plus $1,954.28 in restitution.||The cart had been leased to the A-State Alumni Association for the football season. It was reported stolen September 14 and was recovered the next morning. According to the arrest affidavit, campus cameras showed three people taking it near Red Wolf Boulevard before it left campus, and traffic cameras tracked it to a gas station on East Johnson Avenue. They had first been charged with felony theft of a vehicle. (KAIT's dates for the sentencing were inconsistent, so none is given here.)"))
body.append('<h3>Osceola father speaks after autistic son removed from courtroom</h3>')
body.append(P("The father of an autistic man says his son was mistreated when officers removed him from an Osceola district courtroom after a guilty verdict, KAIT reported Sunday. Daniel Thomas Sr. said his son, Daniel Thomas Jr., was found guilty of misdemeanor harassment and faced 30 days. The verdict, the station said, came at a July 22 hearing before District Judge Catherine Dean. After it, the son began loudly begging and moved toward the judge; police called it a safety breach and officers took him out. Video, KAIT said, captured him saying, &ldquo;I can't breathe.&rdquo;||The father says police told him the judge felt threatened. Judge Dean has said her social media post about the incident did not name anyone. A therapist who works with autistic people told KAIT, speaking generally, that stress behaviors can be misread as threats. Osceola police declined to comment on camera, saying an investigation is ongoing; the report does not say what happened to the harassment case afterward."))
body.append('<h3>Free chronic wasting disease testing for hunters</h3>')
body.append(P("The Arkansas Game and Fish Commission offers free testing for chronic wasting disease (CWD), a fatal, contagious brain illness of deer and elk, throughout hunting season, KAIT reported. Hunters can drop samples at sites or participating taxidermists listed at agfc.com or bring them to AGFC regional offices (call ahead). Anyone who sees a sick deer is asked to report it with photos or video. The CDC and the Arkansas Department of Health advise against eating any animal that tests positive or appears sick."))
body.append('<h3>Around town</h3>')
body.append(P("Jonesboro native and World War II veteran Pearly Lasley turned 100 on Saturday, with family, friends and neighbors gathered to celebrate. He served in the Army in 1945 and 1946, and his advice for a long life, he told KAIT, was to &ldquo;stay away from bad company&rdquo; and to go to church on Sundays.||<b>Little Shop of Horrors</b>, the musical, opens Friday at A-State's Fowler Center Drama Theatre and runs through November 22 (7:30 p.m. Fridays and Saturdays, 2:30 p.m. Sundays; $15 to $20)."))
body.append('<h2>From the State</h2>')
body.append('<h3>Sanders proposes a $6.97 billion budget</h3>')
body.append(P("Gov. Sarah Huckabee Sanders delivered her proposed state budget to lawmakers on Friday: $6.969 billion for the coming year, an increase of $311.6 million, or 3.94 percent. She says she is holding spending growth down to leave room for another round of income-tax cuts once the budget passes. The state ended its last fiscal year with a $655 million surplus, and revenue in the first four months of this year ran more than $150 million above forecast.||The plan includes $150 million in ongoing Medicaid money, including services for people on a waiting list for a disability-support waiver, plus $200 million in one-time surplus funds for what the Governor calls Medicaid sustainability. It sets aside $70 million for Education Freedom Accounts, the school-voucher program created by her LEARNS Act, and $25 million to cover SNAP (food stamp) administrative costs, with $50 million more in one-time money in case the state must share the cost of SNAP benefits. Other items include $20 million for early childhood education and $50 million for the State Water Plan. The budget goes next to the legislature, which meets in January."))
body.append('<h3>What the election changed in Little Rock</h3>')
body.append(P("Democrats flipped 11 legislative seats on Tuesday, 10 in the House and one in the Senate, but Republicans still hold a 70-30 majority in the House, according to the Arkansas Times. That matters because appropriations bills, which authorize agency spending, need a three-fourths vote in both chambers, so the minority party now has more weight. House Minority Leader Andrew Collins said more leverage does not mean Democrats will block spending bills, though he promised to be vocal against policies they oppose."))
body.append('<h2>From the Nation</h2>')
body.append('<h3>Stephen Miller becomes chief of staff</h3>')
body.append(P("President Trump named Stephen Miller, his longtime adviser and the architect of his immigration crackdown, White House chief of staff on Friday, replacing Susie Wiles, who is moving to the President's political operation. Miller takes over today. The change follows Tuesday's midterms, in which Republicans lost the House and the Senate. Democrats are expected to investigate Miller when they take control in January; Rep. Robert Garcia has already said he will. Trump also said he had offered the press secretary job to Dana White, the president of the UFC."))
body.append('<h3>Two Senate races still undecided</h3>')
body.append(P("Democrats hold 54 Senate seats and Republicans 44, according to the Associated Press as of Saturday, with Alaska and Mississippi still uncalled. In Mississippi, Democrat Scott Colom led Republican Sen. Cindy Hyde-Smith by about 2,500 votes with 97 percent counted; absentee ballots that arrive by Tuesday still count, counties must certify by Friday, and Mississippi has no statewide recount provision. In Alaska, Democrat Mary Peltola led Sen. Dan Sullivan by only 637 votes with 74 percent counted on Thursday, with more ballots due today and tomorrow; if nobody passes 50 percent, ranked-choice counting begins November 18. In the House, Democrats held 254 seats to 162 as of Sunday, with 19 races uncalled (Yahoo News snapshot, Monday)."))
body.append('<h3>Impeachment vote on Hegseth expected this week</h3>')
body.append(P("Rep. Thomas Massie, a Kentucky Republican, says he will force a House vote this week on impeaching Defense Secretary Pete Hegseth, and Democratic leader Hakeem Jeffries says he will vote yes. Massie's eight articles of impeachment include allegations that Hegseth violated the War Powers Resolution during the Iran war. Hegseth has called them sham articles. The speaker has up to two legislative days to schedule a vote, and the House could instead vote to table the resolution. A simple majority of those voting is enough to impeach; conviction would require two-thirds of the Senate, which is far less likely. Reports differ on the odds: Massie says better than even, while others call it unclear."))
body.append('<h2>From Abroad</h2>')
body.append('<h3>Israel: Netanyahu rival asked to form a government</h3>')
body.append(P("Israel's President Isaac Herzog has asked Gadi Eisenkot, a former army chief of staff and war-cabinet member who leads the Yashar party, to try to form the next government, passing over Prime Minister Benjamin Netanyahu after October's inconclusive election. No bloc won a majority in the 120-seat Knesset, Israel's parliament. Eisenkot has 28 days to build a coalition, with a possible 14-day extension, and says he wants a &ldquo;national emergency government.&rdquo; Reports differ on his backing: one says lawmakers representing 67 seats recommended him, another credits his four-party alliance with 48 seats. If he fails, a new election must be called within 90 days, and Netanyahu would stay on as caretaker prime minister."))
body.append('<h3>Ukraine: peace talks in Abu Dhabi</h3>')
body.append(P("Ukraine, Russia and the United States are due to hold talks in Abu Dhabi, in the United Arab Emirates, on November 10 and 11, with a focus on security arrangements after the war, according to U.S. envoy Steve Witkoff. France's foreign minister says European countries will be represented, although NPR reported the Kremlin objected. Kyiv says Moscow's demands, including control of all of the Donbas region, show it is not serious about a deal, while President Trump has floated a security arrangement that &ldquo;might involve all of Europe,&rdquo; with few details so far."))
body.append('<h3>South Africa: ruling ANC suffers record local defeat</h3>')
body.append(P("The African National Congress, the party of Nelson Mandela and South Africa's governing party since apartheid ended, won about 31 percent of the vote in last week's local elections, its worst municipal result ever, against nearly 46 percent in 2021. The main opposition Democratic Alliance had about 25 percent. The ANC lost its majority in six of the eight big cities, including Johannesburg, so coalition talks will decide who runs them. The party's secretary-general called the result &ldquo;catastrophic.&rdquo;"))
body.append('<h3>Japan: strong earthquake injures at least 22</h3>')
body.append(P("A magnitude 5.7 earthquake (5.5 by the U.S. Geological Survey) struck western Shizuoka Prefecture in central Japan early Sunday, injuring at least 22 people and shattering store windows. No tsunami warning was issued, and the Japan Meteorological Agency said the chance that it is linked to a feared great Nankai Trough earthquake is low."))
body.append('<h2>Markets &amp; the Farm</h2>')
body.append('<p class="note">Figures are as of Friday&rsquo;s close, November 6 (markets reopen today).</p>')
body.append('''<table class="mk"><tr><th>Index</th><th>Close</th><th>Change</th><th>Week</th></tr>
<tr><td>S&amp;P 500</td><td class="n">7,376.86</td><td class="n">+0.31%</td><td class="n">&minus;2.68%</td></tr>
<tr><td>Dow Jones Industrials</td><td class="n">51,285.73</td><td class="n">&minus;0.46%</td><td class="n">&minus;0.94%</td></tr>
<tr><td>Nasdaq Composite</td><td class="n">24,579.42</td><td class="n">+1.09%</td><td class="n">&minus;3.37%</td></tr></table>''')
body.append(P("Stocks rebounded modestly on Friday after Thursday's steep technology sell-off, but the week was the S&amp;P 500's worst since the April 2025 tariff drop. Investors cited worries about the artificial-intelligence boom and possible tighter regulation of it after the election, and a strong October jobs report pushed interest-rate expectations and the dollar higher. Reports differ slightly on the Dow's exact change, so the figures are approximate.||This week the October inflation report (CPI) arrives on Tuesday, markets are open on Veterans Day, and investors will watch for Federal Reserve comments."))
body.append(P("<i>No analyst-call roundup is printed today: the lists for Friday and Monday could not be confirmed from more than one source. This is information, not advice.</i>"))
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
body.append(P("Oil fell about 13 to 16 percent last week depending on the contract, to $98.32 for Brent and $90.83 for WTI, as traders bet that the Democratic election sweep opens the way to a U.S.-Iran deal; no agreement has been signed and attacks near the Strait of Hormuz continue. Arkansas gasoline averaged $3.71 a gallon on AAA's Thursday report, down 9 cents in a week, and Jonesboro $3.63, down 10 cents. Gasoline changes are for the week; other lines are Friday's change. The grain and livestock lines come from a single source (Brownfield Ag News) for Friday."))
body.append('<h2>On the Field</h2>')
body.append(P("<b>Arkansas State football</b> (lost 19-17 to Louisiana-Monroe in the Rice Bowl Saturday) visits Coastal Carolina next Saturday, November 14; check astateredwolves.com for the kickoff time. <b>Arkansas</b> (3-6) hosts South Carolina on Saturday at 6:45 p.m. Central on the SEC Network.||<b>A-State women's basketball</b> fell to 0-2 with a 59-89 loss at Florida Gulf Coast on Saturday in Fort Myers; Crislyn Rose led the Red Wolves with 14 points, and Amina Gray and Monica Marsh scored 13 each. The team plays Wednesday at 7 p.m. at Loyola Chicago."))
body.append('<h2>Afield &amp; Afloat</h2>')
body.append('<p class="note">Ratings are rule-of-thumb estimates from the forecast, the rut calendar and the sun, not measurements of animal or fish behavior.</p>')
body.append('<h3>Deer outlook: Good</h3>')
body.append(P("The rut is in its peak window, dawn is a cool 40 degrees and the wind is nearly calm, but a warm afternoon near 67 will keep deer bedded in the shade as the day heats. Be in the stand by first light at 6:05 a.m. and hunt about two hours after sunrise (6:33), then take the evening from about 3:00 p.m. to sunset at 4:59. In the peak rut, 10 a.m. to 2 p.m. is realistic too, as bucks cruise for does.||<b>Today's tip:</b> with the breeze so light, scent will hang low and drift unpredictably; set up with a funnel or creek bottom behind you and be extra patient when you climb down."))
body.append(P("<b>Tomorrow, Tuesday (estimate: Good):</b> dawn near 42, a mild afternoon near 71 under heavy cloud and light wind. Watch 6:04 to about 8:30 a.m. and 2:58 to 4:58 p.m. <b>Tomorrow's tip:</b> overcast skies often keep deer moving later into the morning, so stay put until ten."))
body.append('<h3>Fishing outlook: Good</h3>')
body.append(P("At the Crowley's Ridge lakes (Craighead Forest Lake, Lake Frierson) steady pressure and a warm afternoon near 67 make a good day. Fish late morning through mid-afternoon as the shallows warm, then again in the last hour before sunset at 4:59.||<b>Today's tip:</b> with the water cooling, crappie are moving toward brush piles and docks in 8 to 12 feet; small minnows or 1/16-ounce jigs under a float work well, and bass will take slow-rolled spinnerbaits near wood."))
body.append(P("<b>Tomorrow, Tuesday (estimate: Good):</b> steady pressure, an overcast sky and a warm afternoon near 71; best late morning to mid-afternoon, with another window before sunset at 4:58. <b>Tomorrow's tip:</b> clouds let bass roam farther from cover, so try a crankbait along the points."))
body.append('<h3>In season now, and what is next (zones 3, 4, 6 and 8)</h3>')
body.append('''<table class="mk"><tr><th>Zone</th><th>Archery</th><th>Youth gun</th><th>Modern gun</th><th>Muzzleloader</th></tr>
<tr><td>3</td><td>open to Feb. 28</td><td>Nov. 7&ndash;8; Jan. 2&ndash;3</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr>
<tr><td>4</td><td>open to Feb. 28</td><td>Nov. 7&ndash;8; Jan. 2&ndash;3</td><td>Nov. 14&ndash;22; Dec. 26&ndash;28</td><td>closed</td></tr>
<tr><td>6</td><td>open to Feb. 28</td><td>Nov. 7&ndash;8; Jan. 2&ndash;3</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr>
<tr><td>8</td><td>open to Feb. 28</td><td>Nov. 7&ndash;8; Jan. 2&ndash;3</td><td>Nov. 14&ndash;Dec. 6; Dec. 26&ndash;28</td><td>Dec. 12&ndash;14</td></tr></table>''')
body.append(P("<b>Open now:</b> archery season, open in all four zones since September 26 through February 28.||<b>Saturday, November 14,</b> modern gun season opens in all four zones. Zone 4, which includes Craighead County, runs only to November 22, while Zones 3, 6 and 8 run to December 6. Muzzleloader season runs December 12&ndash;14 in Zones 3, 6 and 8 (closed in Zone 4); the second youth hunt is January 2&ndash;3."))
body.append(P("<b>Waterfowl:</b> duck, coot and merganser season runs November 21&ndash;29, December 10&ndash;23 and December 26 to January 31. Check agfc.com for small-game dates."))
body.append('<h2>Postscript</h2>')
body.append('<p class="ps">The Last Pecan.</p>')
body.append('<p class="ps">Every fall Aunt Delphine counted the pecans in her yard, and every fall the squirrels counted them too, more efficiently. By Thanksgiving she had a tally of nine, which she kept in a coffee can on the porch, guarded like crown jewels.</p>')
body.append('<p class="ps">&ldquo;They are a gift,&rdquo; she told the squirrel on the fence post. &ldquo;I am not going to argue with you.&rdquo; She argued with him for an hour.</p>')
body.append('<p class="ps">On Christmas Eve the can held ten. She never learned who had added the tenth, and the squirrel, who sat on the post looking innocent, was not talking.</p>')
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
