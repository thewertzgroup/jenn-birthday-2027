#!/usr/bin/env python3
"""Builds index.html from template.html + the trip data below. Run: python3 build.py"""
import json, html, re
E = html.escape
CRED = json.load(open('credits.json'))
CHECKED = 'Nov 21, 2026'
GF = 'https://www.google.com/travel/flights/search?tfs={}&curr=USD&hl=en'
L = {
 'noc': GF.format('CBwQAhoeEgoyMDI3LTA2LTA4agcIARIDTk9DcgcIARIDTEhSQAFAAUgBcAGCAQsI____________AZgBAg'),
 'f222': 'https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDI3LTA2LTAzagcIARIDU0ZPcgcIARIDRFVCGh4SCjIwMjctMDYtMTRqBwgBEgNOQ0VyBwgBEgNTRk9AAUABSAFwAYIBCwj___________8BmAEB&curr=USD&hl=en',
 'f333': 'https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDI3LTA2LTAyagcIARIDU0ZPcgcIARIDRFVCGh4SCjIwMjctMDYtMTZqBwgBEgNOQ0VyBwgBEgNTRk9AAUABSAFwAYIBCwj___________8BmAEB&curr=USD&hl=en',
 'es10': 'https://www.eurostar.com/search/uk-en?adult=2&origin=7015400&destination=8727100&outbound=2027-06-10',
 'es11': 'https://www.eurostar.com/search/uk-en?adult=2&origin=7015400&destination=8727100&outbound=2027-06-11',
 'sncf': 'https://www.sncf-connect.com/en-en/train/route/reims/nice',
 'chanzy': 'https://www.marriott.com/en-us/hotels/rheak-la-caserne-chanzy-hotel-and-spa-autograph-collection/overview/',
 'royalch': 'https://royalchampagne.com/',
 'shel': 'https://www.marriott.com/en-us/hotels/dubdt-the-shelbourne-autograph-collection/overview/',
 'cgreen': 'https://www.marriott.com/en-us/hotels/dubcg-the-college-green-hotel-dublin-autograph-collection/overview/',
 'icdub': 'https://www.ihg.com/intercontinental/hotels/us/en/dublin/dblic/hoteldetail',
 'ashford': 'https://ashfordcastle.com/',
 'ashspa': 'https://ashfordcastle.com/wellness-and-spa',
 'grosv': 'https://www.marriott.com/en-us/hotels/longh-jw-marriott-grosvenor-house-london/overview/',
 'icpl': 'https://www.ihg.com/intercontinental/hotels/us/en/london/lonhb/hoteldetail',
 'lmnice': 'https://www.marriott.com/en-us/hotels/ncemd-le-meridien-nice/overview/',
 'lmbp': 'https://www.marriott.com/en-us/hotels/mcmmd-le-meridien-beach-plaza/overview/',
 'negresco': 'https://www.lenegresco.com/',
 'f1': 'https://www.formula1.com/en/racing/2027/monaco',
 'lhw': 'https://www.lhw.com/hotel/Adare-Manor-Adare-Ireland',
}
def a(href, text, cls='btn'):
    return f'<a class="{cls}" href="{E(href)}" target="_blank" rel="noopener">{text}</a>'
def pic(key, alt, cls='', eager=False, sizes='(min-width: 900px) 50vw, 100vw'):
    load = 'eager" fetchpriority="high' if eager else 'lazy'
    w, h = CRED[key]['w'], CRED[key]['h']
    return (f'<img class="{cls}" src="images/{key}-800.jpg" srcset="images/{key}-800.jpg 800w, images/{key}-1600.jpg 1600w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{E(alt)}" loading="{load}" decoding="async">')

# ---------- itinerary ----------
DAYS = [
 dict(date='Wed Jun 2', place='Fly SFO → Dublin', img='plane', alt='Airliner on approach', booked=True, bday=False,
      body=('United UA 2391 SFO 1:10 pm → Washington Dulles 9:27 pm, then UA 228 at 11:05 pm → Dublin 11:10 am Thursday. '
            'Home Wed Jun 16 on SWISS: LX 565 Nice 10:50 am → Zurich 12:05 pm, LX 38 Zurich 1:15 pm → SFO 4:15 pm.'
            '<span class="okline">Booked with United miles · confirmation PBWTSM · seats not selected yet.</span>'),
      price='168,000 miles + $234', sub='For both of you, both directions, economy, taxes and fees included',
      links=[]),
 dict(date='Thu Jun 3 – Sun Jun 6', place='Dublin · 3 nights', img='shelbourne', alt="The Shelbourne, St Stephen's Green, Dublin", img2='dublin', alt2="Ha'penny Bridge, Dublin", booked=True, bday=False,
      body=("<b>The Shelbourne, Autograph Collection</b>, on St Stephen's Green, a short walk to Grafton Street and Trinity College. Guest room, 1 King. Platinum perks can apply (see below)."
            '<span class="okline">Booked on Bonvoy points · confirmation 73079619 · free cancellation until 11:59 pm Dublin time, Jun 2, 2027.</span>'),
      price='332,000 Bonvoy points', sub='$0 cash · 3 nights',
      brand='Autograph Collection',
      links=[(L['shel'],'The Shelbourne')]),
 dict(date='Sun Jun 6', place='Drive to Ashford', img=None,
      body='Pick up a one-way rental car in Dublin and drive about 3 h to Cong. Check-in is from 3 pm. The car is only for the two transfers: Dublin → Ashford, then Ashford → Knock airport on Jun 8.',
      price='≈ $350', sub='Estimate: one-way rental with drop fee, plus fuel. Not priced live.', links=[]),
 dict(date='Sun Jun 6 – Tue Jun 8', place='Ashford Castle · 2 nights · her birthday', img='ashford2', alt='Ashford Castle, Cong, County Mayo', img2='ashford', alt2='Ashford Castle from Lough Corrib', booked=True,
      body=('Junior Stateroom on the <b>A Taste of Ireland</b> package: a five-course dinner in the George V Dining Room, an Irish dinner in The Dungeon, afternoon tea, and breakfast both mornings. '
            'Birthday <b>Mon Jun 7</b> at the castle. The Spa is open daily 8 am–7 pm (treatments 9:30 am–6 pm).'
            '<span class="okline">Booked · deposit paid · free cancellation until May 23, 2027.</span>'),
      price='€7,120 (~$7,825)', sub='Total for two nights, taxes included', links=[(L['ashford'],'Ashford Castle'),(L['ashspa'],'The Spa')]),
 dict(date='Tue Jun 8 – Fri Jun 11', place='Knock → London · 3 nights', img='grosvenor', alt='Grosvenor House on Park Lane, London', img2='ic-parklane', alt2='InterContinental London Park Lane',
      body='Drive 50 min to Ireland West Airport Knock and drop the car. Aer Lingus 1:05 pm → Heathrow 2:30 pm. <b>JW Marriott Grosvenor House</b> on Park Lane, facing Hyde Park. The hotel says its Executive Lounge is free for Platinum members.<span class="okline">Hotel booked · confirmation 73083147 · free cancellation until 11:59 pm London time, Jun 7, 2027 (£632 fee after).</span>',
      price='$172 + £1,919 (~$2,518)', sub='Flight $172 for two, not booked yet (Ryanair Knock → Stansted $108) · hotel £1,919.40 for 3 nights, Superior 1 King, Member Flexible rate, may be charged at the hotel · non-Marriott alternate: InterContinental Park Lane (IHG)', hotelbooked=True,
      brand='JW Marriott',
      links=[(L['noc'],'Knock → LHR'),(L['grosv'],'Grosvenor House'),(L['icpl'],'InterContinental (alt)')]),
 dict(date='Fri Jun 11 – Sun Jun 13', place='Eurostar → Champagne · 2 nights in Reims', img='reims', alt='Reims Cathedral', img2='chanzy', alt2='La Caserne Chanzy, Reims',
      body=('<b>Eurostar 12:31 pm</b> St Pancras → Paris Nord 3:59 pm, then a 5-minute walk to Paris Est and the TGV to Reims (about 45 min). '
            '<b>La Caserne Chanzy Hotel &amp; Spa, Autograph Collection</b>, a converted fire station facing the cathedral, with a spa. '
            'Sat Jun 12 is for the champagne houses: cellars in Reims, or the train to Épernay (about 25 min) for the Avenue de Champagne.'
            '<span class="okline">Hotel booked · confirmation 73084366 · free cancellation until 11:59 pm, Jun 10, 2027 (€319.60 fee after).</span>'),
      price='$273 + ≈$100 + €639 (~$702)', sub='Eurostar Plus £208 for two, live on eurostar.com, not booked yet (Standard £156) · Paris → Reims TGV 1st class ≈ $100, estimate · hotel €639.20 for 2 nights, Chanzy Guest Room 1 King, courtyard, Member Flexible rate', hotelbooked=True,
      brand='Autograph Collection',
      links=[(L['es11'],'Eurostar Jun 11'),(L['chanzy'],'La Caserne Chanzy'),(L['royalch'],'Royal Champagne (alt)')]),
 dict(date='Sun Jun 13 – Wed Jun 16', place='TGV → Nice · 3 nights on the Riviera', img='nice', alt='Promenade des Anglais, Nice', img2='tgv', alt2='TGV at Nice-Ville',
      body=('Train all the way: Reims → Paris Est (45 min), metro to Gare de Lyon, then a direct <b>TGV INOUI to Nice</b> (about 5 h 40 min). Door to door is about 7–8 hours. '
            'There is no direct train from Champagne-Ardenne TGV or Marne-la-Vallée to Nice; those routes change once or twice too. '
            '<b>First class is recommended</b> for this long leg: it\'s about $140 more for two (estimate). '
            '<b>Le Méridien Nice</b> on the Promenade des Anglais, 15 min from the airport. Monaco is 25 min by local train.'
            '<span class="okline">Hotel booked · confirmation 73085131 · free cancellation until 11:59 pm, Jun 10, 2027 (€574 fee after).</span>'),
      price='≈$400 + €1,723 (~$1,892)', sub='TGV 1st class for two ≈ $400, estimate (2nd ≈ $260); June 2027 French fares aren\'t on sale yet · hotel €1,722.88 for 3 nights, Classic 1 King, courtyard, Member Flexible rate', hotelbooked=True,
      brand='Le Méridien',
      links=[(L['sncf'],'SNCF Connect'),(L['lmnice'],'Le Méridien Nice'),(L['lmbp'],'Beach Plaza Monaco'),(L['negresco'],'Le Negresco (alt)')]),
 dict(date='Wed Jun 16', place='Fly Nice → SFO', img=None, body='SWISS LX 565 Nice 10:50 am → Zurich 12:05 pm, LX 38 Zurich 1:15 pm → SFO 4:15 pm. Booked, PBWTSM.', price='booked', sub='in the United miles booking above', links=[], nob=True),
]
def card(d):
    cls = ' star' if d.get('booked') and d.get('bday') is not False else ''
    media = ''
    if d['img']:
        media = f'<figure class="media">{pic(d["img"], d["alt"])}'
        if d.get('img2'):
            media += f'<div class="inset">{pic(d["img2"], d["alt2"], sizes="200px")}</div>'
        media += '</figure>'
    badge = ('<span class="badge booked">✓ Booked</span>' + ('' if d.get('bday') is False else ' <span class="badge">🎂 Birthday · Mon Jun 7</span>')) if d.get('booked') else ('' if d.get('nob') or d.get('hotelbooked') else '<span class="badge todo">Not booked yet</span>')
    if d.get('hotelbooked'): badge += '<span class="badge booked">✓ Hotel booked</span> <span class="badge todo">Travel not booked yet</span>'
    if d.get('brand'): badge += f'<span class="badge mar">Marriott Bonvoy · {d["brand"]}</span>'
    links = ''.join(a(h, t) for h, t in d['links'])
    return (f'<article class="day{cls}">{media}<div class="day-body"><p class="date">{d["date"]}</p>{badge}<h3>{d["place"]}</h3>'
            f'<p>{d["body"]}</p><p class="price">{d["price"]}<small>{d["sub"]}</small></p><div class="links">{links}</div></div></article>')

ITEMS = [('Flights SFO → Dublin / Nice → SFO · booked, PBWTSM (168,000 United miles + taxes)', 234, 'booked'), ('Dublin, 3 nights · The Shelbourne · booked, 73079619 (332,000 Bonvoy points)', 0, 'booked'),
         ('Car Dublin → Ashford → Knock (estimate)', 350, 'est'), ('Ashford Castle, 2 nights · booked (dinners included)', 7825, 'booked'),
         ('Knock → Heathrow', 172, ''), ('United seats, all flights · booked', 123, 'booked'), ('London, 3 nights · Grosvenor House · booked, 73083147 (£1,919.40)', 2518, 'booked'),
         ('Eurostar Plus London → Paris', 273, ''), ('TGV Paris → Reims, 1st class (estimate)', 100, 'est'), ('Reims, 2 nights · La Caserne Chanzy · booked, 73084366 (€639.20)', 702, 'booked'),
         ('TGV Reims → Paris → Nice, 1st class (estimate)', 400, 'est'), ('Nice, 3 nights · Le Méridien Nice · booked, 73085131 (€1,722.88)', 1892, 'booked'),
         ('Checked bags, 1 each, on the flights (estimate)', 320, 'est')]
TOT = sum(v for _, v, _ in ITEMS)
rows = ''.join(f'<tr class="{c}"><td>{k}</td><td>${v:,}</td></tr>' for k, v, c in ITEMS)
eco_lo, eco_hi = TOT + 2750, TOT + 4400

# ---------- other orders (economy, flights + hotels, 2 adults) ----------
OCOLS = ['3-2-3-2-3 <span class="badge booked">final plan</span>', '2 / 2 / 2', 'Previous plan: Kerry, London, Nice']
OROWS = [
 ('Dates', ['Wed Jun 2 – Wed Jun 16', 'Thu Jun 3 – Mon Jun 14', 'Sat May 29 – Sun Jun 13']),
 ('Nights in Europe', ['13', '10', '14']),
 ('Stops', ['Dublin 3 · Ashford 2 · London 3 · Reims 2 · Nice 3', 'Dublin 2 · Ashford 2 · London 2 · Reims 2 · Nice 2', 'Dublin 4 · Kerry 3 · Ashford 2 · London 2 · Nice 3']),
 ('Flights', ['$529: United miles booking $234 + seats $123 (booked) + Knock–Heathrow $172', '$1,974: Porter via Toronto $1,802 + Knock–Heathrow $172', '$2,458: Aer Lingus nonstop $2,037 + two short flights $421']),
 ('Trains', ['$773: Eurostar Plus $273 (live) + TGV 1st ≈ $500 (estimate)', '$878: Eurostar Plus $378 (live) + TGV 1st ≈ $500 (estimate)', '–']),
 ('Hotels', ['$12,937 cash + 332,000 Bonvoy points (all booked)', '$12,481', '$14,570']),
 ('Bags + car (estimates)', ['$670', '$670', '$410 + car (not priced)']),
 ('Food (estimate)', ['$2,750–4,400 (11 days)', '$2,000–3,200 (8 days)', '$3,250–5,200']),
 ('All in', ['<b>$17,659–19,309</b> + 168,000 miles + 332,000 points', '<b>$18,003–19,203</b>', '<b>$20,688–22,638</b> + car']),
 ('vs $20k', ['Under, by $700–2,300 (cash)', 'Under, by $800–2,000', 'Over, plus the car']),
]
orders = '<tr><th></th>' + ''.join(f'<th>{c}</th>' for c in OCOLS) + '</tr>' + ''.join(
  f'<tr><th>{k}</th>' + ''.join(f'<td>{v}</td>' for v in vals) + '</tr>' for k, vals in OROWS)

credits = ''.join(
  f'<li><a href="{E(v["page"])}" target="_blank" rel="noopener">{E(v["title"][5:])}</a> by {E(v["artist"])} · '
  f'<a href="{E(v["licenseurl"])}" target="_blank" rel="noopener">{E(v["license"])}</a></li>' for v in CRED.values())

page = open('template.html').read()
rep = dict(CARDS='\n'.join(card(d) for d in DAYS), ROWS=rows, TOTAL=f'${TOT:,}', CREDITS=credits, CHECKED=CHECKED,
           ECO_LO=f'${eco_lo:,}', ECO_HI=f'${eco_hi:,}', ORDERS=orders)
for k, v in rep.items(): page = page.replace('{{'+k+'}}', v)
for k, v in L.items(): page = page.replace('{{L_'+k+'}}', E(v))
page = re.sub(r'\{\{PIC:([\w-]+)\|([^}]*)\}\}', lambda m: pic(m.group(1), m.group(2), 'cover'), page)
page = page.replace('{{HERO}}', pic('ashford2', 'Ashford Castle, County Mayo', 'hero-img', eager=True, sizes='100vw'))
assert '{{' not in page, re.findall(r'\{\{[^}]*\}\}', page)
# keep credits to images actually used
used = set(re.findall(r'images/([\w-]+)-800\.jpg', page))
open('index.html', 'w').write(page)
print('built', TOT, 'eco', eco_lo, eco_hi, 'unused credits', sorted(set(CRED) - used))
