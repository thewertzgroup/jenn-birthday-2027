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
 dict(date='Wed Jun 2', place='Fly SFO → Dublin', img='plane', alt='Airliner on approach',
      body='United via Washington Dulles, 1:10 pm, lands Dublin 10:40 am Thursday. One open-jaw ticket: in to Dublin, home from Nice on Wed Jun 16. <b>Worth a look:</b> Aer Lingus nonstop, 5:35 pm → 11:40 am, is only $165 more.',
      price='$2,284 economy', sub='Round trip for two, Google Flights · Aer Lingus nonstop $2,449 · cheapest $1,721 (TAP via Lisbon, 9 h 45 min layover) · San Jose and Oakland cost more ($2,082+, 2 stops) · checked bags not included, estimate below',
      links=[(L['f333'],'Economy fares')]),
 dict(date='Thu Jun 3 – Sun Jun 6', place='Dublin · 3 nights', img='shelbourne', alt="The Shelbourne, St Stephen's Green, Dublin", img2='dublin', alt2="Ha'penny Bridge, Dublin",
      body="Marriott pick: <b>The Shelbourne, Autograph Collection</b>, on St Stephen's Green, a short walk to Grafton Street and Trinity College. Platinum perks can apply (see below).",
      price='$2,574', sub='$858/night · Google Hotels (a rate with free cancellation until Jun 1 was listed) · cheaper Marriott: The College Green Hotel · alt: InterContinental Dublin',
      links=[(L['shel'],'The Shelbourne'),(L['cgreen'],'College Green'),(L['icdub'],'InterContinental')]),
 dict(date='Sun Jun 6', place='Drive to Ashford', img=None,
      body='Pick up a one-way rental car in Dublin and drive about 3 h to Cong. Check-in is from 3 pm. The car is only for the two transfers: Dublin → Ashford, then Ashford → Knock airport on Jun 8.',
      price='≈ $350', sub='Estimate: one-way rental with drop fee, plus fuel. Not priced live.', links=[]),
 dict(date='Sun Jun 6 – Tue Jun 8', place='Ashford Castle · 2 nights · her birthday', img='ashford2', alt='Ashford Castle, Cong, County Mayo', img2='ashford', alt2='Ashford Castle from Lough Corrib', booked=True,
      body=('Junior Stateroom on the <b>A Taste of Ireland</b> package: a five-course dinner in the George V Dining Room, an Irish dinner in The Dungeon, afternoon tea, and breakfast both mornings. '
            'Birthday <b>Mon Jun 7</b> at the castle. The Spa is open daily 8 am–7 pm (treatments 9:30 am–6 pm).'
            '<span class="okline">Booked · deposit paid · free cancellation until May 23, 2027.</span>'),
      price='€7,120 (~$7,825)', sub='Total for two nights, taxes included', links=[(L['ashford'],'Ashford Castle'),(L['ashspa'],'The Spa')]),
 dict(date='Tue Jun 8 – Fri Jun 11', place='Knock → London · 3 nights', img='grosvenor', alt='Grosvenor House on Park Lane, London', img2='ic-parklane', alt2='InterContinental London Park Lane',
      body='Drive 50 min to Ireland West Airport Knock and drop the car. Aer Lingus 1:05 pm → Heathrow 2:30 pm. Marriott pick: <b>JW Marriott Grosvenor House</b> on Park Lane, facing Hyde Park. The hotel says its Executive Lounge is free for Platinum members.',
      price='$172 + $1,542', sub='Flight $172 for two (Ryanair Knock → Stansted $108) · hotel $514/night, Google Hotels (a rate with free cancellation until Jun 7 was listed) · alt: InterContinental Park Lane',
      links=[(L['noc'],'Knock → LHR'),(L['grosv'],'Grosvenor House'),(L['icpl'],'InterContinental')]),
 dict(date='Fri Jun 11 – Sun Jun 13', place='Eurostar → Champagne · 2 nights in Reims', img='reims', alt='Reims Cathedral', img2='chanzy', alt2='La Caserne Chanzy, Reims',
      body=('<b>Eurostar 12:31 pm</b> St Pancras → Paris Nord 3:59 pm, then a 5-minute walk to Paris Est and the TGV to Reims (about 45 min). '
            'Marriott pick: <b>La Caserne Chanzy Hotel &amp; Spa, Autograph Collection</b>, a converted fire station facing the cathedral, with a spa. '
            'Sat Jun 12 is for the champagne houses: cellars in Reims, or the train to Épernay (about 25 min) for the Avenue de Champagne.'),
      price='$273 + ≈$100 + $590', sub='Eurostar Plus £208 for two, live on eurostar.com (Standard £156, Premier £660) · Paris → Reims TGV 1st class ≈ $100, estimate · hotel $295/night, Google Hotels (free cancellation listed) · luxury alt: Royal Champagne Hotel &amp; Spa $1,242/night',
      links=[(L['es11'],'Eurostar Jun 11'),(L['chanzy'],'La Caserne Chanzy'),(L['royalch'],'Royal Champagne')]),
 dict(date='Sun Jun 13 – Wed Jun 16', place='TGV → Nice · 3 nights on the Riviera', img='nice', alt='Promenade des Anglais, Nice', img2='tgv', alt2='TGV at Nice-Ville',
      body=('Train all the way: Reims → Paris Est (45 min), metro to Gare de Lyon, then a direct <b>TGV INOUI to Nice</b> (about 5 h 40 min). Door to door is about 7–8 hours. '
            'There is no direct train from Champagne-Ardenne TGV or Marne-la-Vallée to Nice; those routes change once or twice too. '
            '<b>First class is recommended</b> for this long leg: it\'s about $140 more for two (estimate). '
            'Marriott pick: <b>Le Méridien Nice</b> on the Promenade des Anglais, 15 min from the airport. Monaco is 25 min by local train.'),
      price='≈$400 + $1,734', sub='TGV 1st class for two ≈ $400, estimate (2nd ≈ $260). June 2027 French domestic fares aren\'t on sale yet · hotel $578/night, Google Hotels (a rate with free cancellation until Jun 10 was listed) · alts: Le Méridien Beach Plaza Monaco, AC Hotel Nice, Le Negresco',
      links=[(L['sncf'],'SNCF Connect'),(L['lmnice'],'Le Méridien Nice'),(L['lmbp'],'Beach Plaza Monaco'),(L['negresco'],'Le Negresco')]),
 dict(date='Wed Jun 16', place='Fly Nice → SFO', img=None, body='Return leg of the open-jaw ticket.', price='included', sub='in the round-trip fare above', links=[], nob=True),
]
def card(d):
    cls = ' star' if d.get('booked') else ''
    media = ''
    if d['img']:
        media = f'<figure class="media">{pic(d["img"], d["alt"])}'
        if d.get('img2'):
            media += f'<div class="inset">{pic(d["img2"], d["alt2"], sizes="200px")}</div>'
        media += '</figure>'
    badge = '<span class="badge booked">✓ Booked</span> <span class="badge">🎂 Birthday · Mon Jun 7</span>' if d.get('booked') else ('' if d.get('nob') else '<span class="badge todo">Not booked yet</span>')
    links = ''.join(a(h, t) for h, t in d['links'])
    return (f'<article class="day{cls}">{media}<div class="day-body"><p class="date">{d["date"]}</p>{badge}<h3>{d["place"]}</h3>'
            f'<p>{d["body"]}</p><p class="price">{d["price"]}<small>{d["sub"]}</small></p><div class="links">{links}</div></div></article>')

ITEMS = [('Flights SFO → Dublin / Nice → SFO (economy)', 2284, ''), ('Dublin, 3 nights · The Shelbourne', 2574, ''),
         ('Car Dublin → Ashford → Knock (estimate)', 350, 'est'), ('Ashford Castle, 2 nights · booked (dinners included)', 7825, 'booked'),
         ('Knock → Heathrow', 172, ''), ('London, 3 nights · Grosvenor House', 1542, ''),
         ('Eurostar Plus London → Paris', 273, ''), ('TGV Paris → Reims, 1st class (estimate)', 100, 'est'), ('Reims, 2 nights · La Caserne Chanzy', 590, ''),
         ('TGV Reims → Paris → Nice, 1st class (estimate)', 400, 'est'), ('Nice, 3 nights · Le Méridien Nice', 1734, ''),
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
 ('Flights', ['$2,456: United via Washington $2,284 + Knock–Heathrow $172', '$1,974: Porter via Toronto $1,802 + Knock–Heathrow $172', '$2,458: Aer Lingus nonstop $2,037 + two short flights $421']),
 ('Trains', ['$773: Eurostar Plus $273 (live) + TGV 1st ≈ $500 (estimate)', '$878: Eurostar Plus $378 (live) + TGV 1st ≈ $500 (estimate)', '–']),
 ('Hotels', ['$14,265', '$12,481', '$14,570']),
 ('Bags + car (estimates)', ['$670', '$670', '$410 + car (not priced)']),
 ('Food (estimate)', ['$2,750–4,400 (11 days)', '$2,000–3,200 (8 days)', '$3,250–5,200']),
 ('All in', ['<b>$20,914–22,564</b>', '<b>$18,003–19,203</b>', '<b>$20,688–22,638</b> + car']),
 ('vs $20k', ['Over, by $900–2,600', 'Under, by $800–2,000', 'Over, plus the car']),
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
