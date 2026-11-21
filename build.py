#!/usr/bin/env python3
"""Builds index.html from template.html + the trip data below. Run: python3 build.py"""
import json, html, re
E = html.escape
CRED = json.load(open('credits.json'))
CHECKED = 'Nov 21, 2026'
GF = 'https://www.google.com/travel/flights/search?tfs={}&curr=USD&hl=en'
L = {
 'oj_eco': GF.format('CBwQAhoeEgoyMDI3LTA1LTI5agcIARIDU0ZPcgcIARIDRFVCGh4SCjIwMjctMDYtMTNqBwgBEgNOQ0VyBwgBEgNTRk9AAUABSAFwAYIBCwj___________8BmAEB'),
 'oj_prem': GF.format('CBwQAhoeEgoyMDI3LTA1LTI5agcIARIDU0ZPcgcIARIDRFVCGh4SCjIwMjctMDYtMTNqBwgBEgNOQ0VyBwgBEgNTRk9AAUABSAJwAYIBCwj___________8BmAEB'),
 'oj_biz': GF.format('CBwQAhoeEgoyMDI3LTA1LTI5agcIARIDU0ZPcgcIARIDRFVCGh4SCjIwMjctMDYtMTNqBwgBEgNOQ0VyBwgBEgNTRk9AAUABSANwAYIBCwj___________8BmAEB'),
 'noc': GF.format('CBwQAhoeEgoyMDI3LTA2LTA4agcIARIDTk9DcgcIARIDTEhSQAFAAUgBcAGCAQsI____________AZgBAg'),
 'lonnce': 'https://www.google.com/travel/flights?hl=en&curr=USD&q=one%20way%20flights%20from%20London%20to%20NCE%20on%202027-06-10%202%20adults',
 'shel': 'https://www.marriott.com/en-us/hotels/dubdt-the-shelbourne-autograph-collection/overview/',
 'cgreen': 'https://www.marriott.com/en-us/hotels/dubcg-the-college-green-hotel-dublin-autograph-collection/overview/',
 'icdub': 'https://www.ihg.com/intercontinental/hotels/us/en/dublin/dblic/hoteldetail',
 'aghadoe': 'https://www.aghadoeheights.com/',
 'kpark': 'https://www.killarneyparkhotel.ie/',
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
 dict(date='Sat May 29', place='Fly SFO → Dublin', img='plane', alt='Aer Lingus Airbus A321neo',
      body='Aer Lingus nonstop, 5:35 pm, lands Dublin 11:40 am Sunday. Open-jaw ticket: home from Nice on Sun Jun 13 (the Nice → SFO leg connects).',
      price='$2,038 economy', sub='Round trip for two, Google Flights · premium economy $4,573 (BA via Heathrow, mixed cabins) · business $14,057 (Aer Lingus nonstop out; cheapest business $13,066, American via Chicago)',
      links=[(L['oj_eco'],'Economy'),(L['oj_prem'],'Premium'),(L['oj_biz'],'Business')]),
 dict(date='Sun May 30 – Thu Jun 3', place='Dublin · 4 nights', img='shelbourne', alt='The Shelbourne, St Stephen\'s Green, Dublin', img2='dublin', alt2="Ha'penny Bridge, Dublin",
      body='Marriott pick: <b>The Shelbourne, Autograph Collection</b>, on St Stephen\'s Green, a short walk to Grafton Street and Trinity College. Platinum perks can apply (see below).',
      price='$2,716', sub='$679/night · Google Hotels · cheaper Marriott: The College Green Hotel, Autograph Collection, $550/night ($2,200) · alt: InterContinental Dublin $326/night ($1,304)',
      links=[(L['shel'],'The Shelbourne'),(L['cgreen'],'College Green'),(L['icdub'],'InterContinental')]),
 dict(date='Thu Jun 3 – Sun Jun 6', place='Killarney & Kerry · 3 nights', img='muckross', alt='Muckross Lake, Killarney National Park', img2='killarney', alt2='Ladies View, Ring of Kerry',
      body='Pick up the rental car in Dublin and drive about 3.5 h to Killarney (lunch stop at Kilkenny or the Rock of Cashel). Two full days for the Ring of Kerry, the Gap of Dunloe, Muckross House and the lakes. No Marriott hotels in Kerry. Pick: <b>Aghadoe Heights Hotel &amp; Spa</b>, lake views, breakfast included.',
      price='$1,191', sub='$397/night B&amp;B · Google Hotels (hotel\'s own rate) · alt: The Killarney Park $646/night ($1,938) · The Europe Hotel &amp; Resort $521/night',
      links=[(L['aghadoe'],'Aghadoe Heights'),(L['kpark'],'The Killarney Park')]),
 dict(date='Sun Jun 6', place='Drive up the Wild Atlantic Way', img='moher', alt='Cliffs of Moher, County Clare',
      body='Killarney → Tarbert car ferry → Cliffs of Moher and the Burren → Cong. About 3.5–4 h of driving plus stops. Ashford check-in is from 3 pm.',
      price='Car', sub='One-way rental Dublin → Knock (or Shannon) not priced yet', links=[]),
 dict(date='Sun Jun 6 – Tue Jun 8', place='Ashford Castle · 2 nights · her birthday', img='ashford2', alt='Ashford Castle, Cong, County Mayo', img2='ashford', alt2='Ashford Castle from Lough Corrib', booked=True,
      body=('Junior Stateroom on the <b>A Taste of Ireland</b> package: a five-course dinner in the George V Dining Room, an Irish dinner in The Dungeon, afternoon tea, and breakfast both mornings. '
            'Birthday <b>Mon Jun 7</b> at the castle. The Spa is open daily 8 am–7 pm (treatments 9:30 am–6 pm).'
            '<span class="okline">Booked · deposit paid · free cancellation until May 23, 2027.</span>'),
      price='€7,120 (~$7,825)', sub='Total for two nights, taxes included', links=[(L['ashford'],'Ashford Castle'),(L['ashspa'],'The Spa')]),
 dict(date='Tue Jun 8 – Thu Jun 10', place='Knock → London · 2 nights', img='grosvenor', alt='Grosvenor House on Park Lane, London', img2='ic-parklane', alt2='InterContinental London Park Lane',
      body='Drive 45 min to Ireland West Airport Knock and drop the car. Aer Lingus 1:05 pm → Heathrow, 2:30 pm. Marriott pick: <b>JW Marriott Grosvenor House</b> on Park Lane, facing Hyde Park; the hotel says its Executive Lounge is free for Platinum members.',
      price='$172 + $1,062', sub='Flight $172 for two (Shannon → Heathrow is $138–158 but about 2 h further) · hotel $531/night, Google Hotels · alts: St. Pancras London, Autograph Collection $490/night · The London EDITION $820/night · InterContinental Park Lane $702/night',
      links=[(L['noc'],'Knock → LHR'),(L['grosv'],'Grosvenor House'),(L['icpl'],'InterContinental')]),
 dict(date='Thu Jun 10 – Sun Jun 13', place='London → Nice · 3 nights on the Riviera', img='nice', alt='Promenade des Anglais, Nice', img2='monaco2', alt2='Monaco from La Turbie',
      body='BA from London City 1:40 pm → Nice 4:40 pm. Marriott pick: <b>Le Méridien Nice</b> on the Promenade des Anglais, 15 min from the airport for the flight home. Monaco is 25 min by train for a day trip. The Grand Prix (Jun 4–6) is over by then.',
      price='$249 + $1,776', sub='Flight $249 for two (easyJet Gatwick $235–256, BA Heathrow 4:20 pm $290) · hotel $592/night, Google Hotels · alts: Le Méridien Beach Plaza, Monaco, $631/night · AC Hotel Nice $598/night · Le Negresco $969/night',
      links=[(L['lonnce'],'London → Nice'),(L['lmnice'],'Le Méridien Nice'),(L['lmbp'],'Beach Plaza Monaco'),(L['negresco'],'Le Negresco')]),
 dict(date='Sun Jun 13', place='Fly Nice → SFO', img=None, body='Return leg of the open-jaw ticket (one connection).', price='included', sub='in the round-trip fare above', links=[]),
]
def card(d):
    cls = ' star' if d.get('booked') else ''
    media = ''
    if d['img']:
        media = f'<figure class="media">{pic(d["img"], d["alt"])}'
        if d.get('img2'):
            media += f'<div class="inset">{pic(d["img2"], d["alt2"], sizes="200px")}</div>'
        media += '</figure>'
    badge = '<span class="badge booked">✓ Booked</span> <span class="badge">🎂 Birthday · Mon Jun 7</span>' if d.get('booked') else ''
    links = ''.join(a(h, t) for h, t in d['links'])
    return (f'<article class="day{cls}">{media}<div class="day-body"><p class="date">{d["date"]}</p>{badge}<h3>{d["place"]}</h3>'
            f'<p>{d["body"]}</p><p class="price">{d["price"]}<small>{d["sub"]}</small></p><div class="links">{links}</div></div></article>')

ITEMS = [('Flights SFO → Dublin / Nice → SFO (economy)', 2038, ''), ('Dublin, 4 nights · The Shelbourne', 2716, ''),
         ('Killarney, 3 nights · Aghadoe Heights (B&amp;B)', 1191, ''), ('Ashford Castle, 2 nights · booked (dinners included)', 7825, 'booked'),
         ('Knock → Heathrow', 172, ''), ('London, 2 nights · Grosvenor House', 1062, ''), ('London → Nice', 249, ''),
         ('Nice, 3 nights · Le Méridien Nice', 1776, '')]
TOT = sum(v for _, v, _ in ITEMS)
rows = ''.join(f'<tr class="{c}"><td>{k}</td><td>${v:,}</td></tr>' for k, v, c in ITEMS)
eco_lo, eco_hi = TOT + 3250, TOT + 5200
prem = TOT + (4573 - 2038); biz = TOT + (14057 - 2038)

credits = ''.join(
  f'<li><a href="{E(v["page"])}" target="_blank" rel="noopener">{E(v["title"][5:])}</a> by {E(v["artist"])} · '
  f'<a href="{E(v["licenseurl"])}" target="_blank" rel="noopener">{E(v["license"])}</a></li>' for v in CRED.values())

page = open('template.html').read()
rep = dict(CARDS='\n'.join(card(d) for d in DAYS), ROWS=rows, TOTAL=f'${TOT:,}', CREDITS=credits, CHECKED=CHECKED,
           ECO_LO=f'${eco_lo:,}', ECO_HI=f'${eco_hi:,}', PREM=f'${prem:,}', BIZ=f'${biz:,}',
           BIZ_LO=f'${biz+3250:,}', BIZ_HI=f'${biz+5200:,}', PREM_LO=f'${prem+3250:,}', PREM_HI=f'${prem+5200:,}')
for k, v in rep.items(): page = page.replace('{{'+k+'}}', v)
for k, v in L.items(): page = page.replace('{{L_'+k+'}}', E(v))
page = re.sub(r'\{\{PIC:([\w-]+)\|([^}]*)\}\}', lambda m: pic(m.group(1), m.group(2), 'cover'), page)
page = page.replace('{{HERO}}', pic('ashford2', 'Ashford Castle, County Mayo', 'hero-img', eager=True, sizes='100vw'))
assert '{{' not in page, re.findall(r'\{\{[^}]*\}\}', page)
# keep credits to images actually used
used = set(re.findall(r'images/([\w-]+)-800\.jpg', page))
open('index.html', 'w').write(page)
print('built', TOT, 'eco', eco_lo, eco_hi, 'prem', prem, 'biz', biz, 'unused credits', sorted(set(CRED) - used))
