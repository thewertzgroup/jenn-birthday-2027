#!/usr/bin/env python3
"""Builds index.html from the trip data below. Run: python3 build.py"""
import json, html
E = html.escape
CRED = json.load(open('credits.json'))

GF = {
 'b_eco':'https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDI3LTA1LTI5agcIARIDU0ZPcgcIARIDRFVCGh4SCjIwMjctMDYtMTNqBwgBEgNDREdyBwgBEgNTRk9AAUABSAFwAYIBCwj___________8BmAEB&curr=USD&hl=en',
 'b_prem':'https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDI3LTA1LTI5agcIARIDU0ZPcgcIARIDRFVCGh4SCjIwMjctMDYtMTNqBwgBEgNDREdyBwgBEgNTRk9AAUABSAJwAYIBCwj___________8BmAEB&curr=USD&hl=en',
 'b_biz':'https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDI3LTA1LTI5agcIARIDU0ZPcgcIARIDRFVCGh4SCjIwMjctMDYtMTNqBwgBEgNDREdyBwgBEgNTRk9AAUABSANwAYIBCwj___________8BmAEB&curr=USD&hl=en',
 'a_eco':'https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDI3LTA2LTAyagcIARIDU0ZPcgcIARIDRFVCGh4SCjIwMjctMDYtMTJqBwgBEgNDREdyBwgBEgNTRk9AAUABSAFwAYIBCwj___________8BmAEB&curr=USD&hl=en',
 'a_prem':'https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDI3LTA2LTAyagcIARIDU0ZPcgcIARIDRFVCGh4SCjIwMjctMDYtMTJqBwgBEgNDREdyBwgBEgNTRk9AAUABSAJwAYIBCwj___________8BmAEB&curr=USD&hl=en',
 'a_biz':'https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDI3LTA2LTAyagcIARIDU0ZPcgcIARIDRFVCGh4SCjIwMjctMDYtMTJqBwgBEgNDREdyBwgBEgNTRk9AAUABSANwAYIBCwj___________8BmAEB&curr=USD&hl=en',
 'noc':'https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDI3LTA2LTA5agcIARIDTk9DcgcIARIDTEhSQAFAAUgBcAGCAQsI____________AZgBAg&curr=USD&hl=en',
 'lgw':'https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDI3LTA2LTEwagcIARIDTEdXcgcIARIDTkNFQAFAAUgBcAGCAQsI____________AZgBAg&curr=USD&hl=en',
 'nce':'https://www.google.com/travel/flights/search?tfs=CBwQAhoeEgoyMDI3LTA2LTExagcIARIDTkNFcgcIARIDQ0RHQAFAAUgBcAGCAQsI____________AZgBAg&curr=USD&hl=en',
}
L = {
 'adare_book':'https://secure.adaremanor.com/convert/site/Adare%20Manor/en/results.php?currency=USD&partya=2&checkin=2027-06-06&nights=2',
 'adare_ege':'https://www.adaremanor.com/exclusive-golf-experience/',
 'adare':'https://www.adaremanor.com/',
 'lhw':'https://www.lhw.com/hotel/Adare-Manor-Adare-Ireland',
 'ashford_book':'https://secure.ashfordcastle.com/convert/site/Ashford%20Castle/en/results.php?currency=USD&partya=2&checkin=2027-06-08&nights=1',
 'ashford':'https://ashfordcastle.com/',
 'ic_dub':'https://www.ihg.com/intercontinental/hotels/us/en/dublin/dubha/hoteldetail',
 'pembroke':'https://www.pembrokekilkenny.com/',
 'kpark':'https://www.killarneyparkhotel.ie/',
 'aghadoe':'https://www.aghadoeheights.com/',
 'ic_pl':'https://www.ihg.com/intercontinental/hotels/us/en/london/lonha/hoteldetail',
 'anantara':'https://www.anantara.com/en/plaza-nice',
 'negresco':'https://www.lenegresco.com/',
 'mcbay':'https://www.montecarlosbm.com/en/hotel-monaco/monte-carlo-bay-hotel-resort',
 'fairmont':'https://www.fairmont.com/en/hotels/monte-carlo/fairmont-monte-carlo.html',
 'castille':'https://collezione.starhotels.com/en/our-hotels/castille-paris/',
 'f1':'https://www.formula1.com/en/racing/2027/monaco',
}

def a(href, text, cls='btn'):
    return f'<a class="{cls}" href="{E(href)}" target="_blank" rel="noopener">{text}</a>'

def pic(key, alt, cls='', eager=False, sizes='(min-width: 900px) 50vw, 100vw'):
    load = 'eager" fetchpriority="high' if eager else 'lazy'
    w, h = CRED[key]['w'], CRED[key]['h']
    return (f'<img class="{cls}" src="images/{key}-800.jpg" srcset="images/{key}-800.jpg 800w, images/{key}-1600.jpg 1600w" '
            f'sizes="{sizes}" width="{w}" height="{h}" alt="{E(alt)}" loading="{load}" decoding="async">')

# ---------- Version B day cards ----------
B = [
 dict(date='Sat May 29', place='Fly SFO → Dublin', img='plane', alt='Aer Lingus Airbus A321neo in flight',
      body='Aer Lingus nonstop, departs 5:35 pm, lands Dublin 11:40 am the next day. Open-jaw round trip: home from Paris (CDG) on Sun Jun 13.',
      price='$2,038 economy', sub='Premium economy (BA, 1 stop) $4,573 · Business: Aer Lingus nonstop $13,513, or Alaska/Aer Lingus 1-stop $12,569',
      links=[(GF['b_eco'],'Economy fares'),(GF['b_prem'],'Premium'),(GF['b_biz'],'Business')]),
 dict(date='Sun May 30 – Tue Jun 1', place='Dublin · 2 nights', img='dublin', alt="Ha'penny Bridge over the River Liffey, Dublin",
      body='InterContinental Dublin in leafy Ballsbridge. Land, nap, then a slow first evening in the city.',
      price='$574', sub='$287/night', links=[(L['ic_dub'],'InterContinental Dublin')], img2='ic-dublin', alt2='InterContinental Dublin, Ballsbridge'),
 dict(date='Tue Jun 1', place='Pick up the car · Kilkenny · 1 night', img='kilkenny', alt='Kilkenny Castle',
      body='Rental car from Dublin, about 1.5 h to medieval Kilkenny. Pembroke Hotel sits by the castle. One-way car hire: no live price yet.',
      price='$120', sub='1 night', links=[(L['pembroke'],'Pembroke Hotel')]),
 dict(date='Wed Jun 2 – Sun Jun 6', place='Killarney & Kerry · 4 nights', img='killarney', alt="Ladies View, Ring of Kerry, Killarney National Park",
      body='Base in Killarney for the Ring of Kerry, Gap of Dunloe, Muckross and the lakes. The Killarney Park in town.',
      price='$1,308', sub='$327/night · alt: Aghadoe Heights ~$204/night', links=[(L['kpark'],'The Killarney Park'),(L['aghadoe'],'Aghadoe Heights')]),
 dict(date='Sun Jun 6 – Tue Jun 8', place='Adare Manor · 2 nights · her birthday', img='adare', alt='Adare Manor, County Limerick', star=True,
      body=('Check in 4 pm Sunday, so Monday Jun 7 is a full birthday day at Adare. 2-bedroom Manor Lodge on the <b>Exclusive Golf Experience</b>: '
            'Carriage House dinner, breakfast, lunch, and golf with caddies (tee time 9–11 am on checkout morning). Drinks extra.'
            '<span class="warn">The Manor House and spa are closed Apr 30 – Sep 27, 2027 for Ryder Cup prep, so the lodge package is the only way to stay. Few lodges left.</span>'
            '<span class="warn">Deposit reportedly 50% within 30 days of booking and 50% 60 days before arrival, non-refundable (Limerick Leader, Sep 16, 2026). Confirm when booking.</span>'),
      price='$16,485', sub='$8,243/night incl. taxes (€15,000 total)',
      links=[(L['adare_book'],'Check Jun 6–8 live'),(L['adare_ege'],'Exclusive Golf Experience'),(L['lhw'],'Closure notice (LHW)')], img2='adare-village', alt2='Thatched cottages in Adare village'),
 dict(date='Tue Jun 8', place='Ashford Castle · 1 night', img='ashford', alt='Ashford Castle from Lough Corrib',
      body='About a 2–2.5 h drive north from Adare to Cong, on Lough Corrib. Check-in 3 pm. Deluxe Lake room, bed & breakfast.',
      price='$1,703', sub='Gourmet Getaway with five-course dinner: $2,017', links=[(L['ashford_book'],'Check Jun 8 live'),(L['ashford'],'Ashford Castle')]),
 dict(date='Wed Jun 9', place='Knock → London · 1 night', img='ic-parklane', alt='InterContinental London Park Lane',
      body='Drop the car at Ireland West Airport Knock (about 45 min from Ashford). Aer Lingus 1:05 pm to Heathrow. Evening in Mayfair.',
      price='$172 + ~$349', sub='Flight $172 · InterContinental Park Lane ~$349', links=[(GF['noc'],'Knock → LHR fares'),(L['ic_pl'],'InterContinental Park Lane')]),
 dict(date='Thu Jun 10', place='London → the Riviera · 1 night', img='nice', alt='Promenade des Anglais, Nice',
      body='easyJet Gatwick → Nice 6:15 pm (or 1:30 pm for $256 and an afternoon on the coast). Stay in Nice, or in Monaco at Monte-Carlo Bay.',
      price='$235 + ~$256', sub='Anantara Plaza Nice ~$256 · or Monte-Carlo Bay $299', links=[(GF['lgw'],'LGW → NCE fares'),(L['anantara'],'Anantara Plaza Nice'),(L['mcbay'],'Monte-Carlo Bay')], img2='mc-bay', alt2='Monte-Carlo Bay Hotel & Resort'),
 dict(date='Fri Jun 11 – Sun Jun 13', place='Paris · 2 nights', img='eiffel', alt='Sunset over the Seine and the Eiffel Tower',
      body='easyJet Nice → Paris CDG 8:10 am (12:45 pm option $169). Castille Paris on rue Cambon, around the corner from Place Vendôme.',
      price='$131 + $728', sub='Castille $364/night', links=[(GF['nce'],'NCE → CDG fares'),(L['castille'],'Castille Paris')], img2='paris', alt2='Place Vendôme, Paris'),
 dict(date='Sun Jun 13', place='Home: Paris → SFO', img=None,
      body='Return leg of the open-jaw ticket booked on May 29.', price='included', sub='in the round-trip fare above', links=[]),
]

def card(d):
    star = ' star' if d.get('star') else ''
    media = ''
    if d['img']:
        media = f'<figure class="media">{pic(d["img"], d["alt"])}'
        if d.get('img2'):
            media += f'<div class="inset">{pic(d["img2"], d["alt2"], sizes="200px")}</div>'
        media += '</figure>'
    links = ''.join(a(h, t) for h, t in d['links'])
    badge = '<span class="badge">🎂 Birthday · Mon Jun 7</span>' if d.get('star') else ''
    return f'''<article class="day{star}">{media}<div class="day-body">
<p class="date">{d["date"]}</p>{badge}<h3>{d["place"]}</h3><p>{d["body"]}</p>
<p class="price">{d["price"]}<small>{d["sub"]}</small></p><div class="links">{links}</div></div></article>'''

# Itemized totals (economy, Nice night)
items = [('Flights SFO⇄Europe (economy)',2038),('Dublin, 2 nights',574),('Kilkenny, 1 night',120),('Killarney, 4 nights',1308),
         ('Adare Manor, 2 nights',16485),('Ashford Castle, 1 night',1703),('Knock → Heathrow',172),('London, 1 night',349),
         ('Gatwick → Nice',235),('Nice, 1 night',256),('Nice → Paris',131),('Paris, 2 nights',728)]
total = sum(v for _, v in items)
rows = ''.join(f'<tr><td>{k}</td><td>${v:,}</td></tr>' for k, v in items)

cards = '\n'.join(card(d) for d in B)

credits = ''.join(
  f'<li><a href="{E(v["page"])}" target="_blank" rel="noopener">{E(v["title"][5:])}</a> by {E(v["artist"])} · '
  f'<a href="{E(v["licenseurl"])}" target="_blank" rel="noopener">{E(v["license"])}</a></li>' for v in CRED.values())

page = open('template.html').read()
for k, v in dict(CARDS=cards, ROWS=rows, TOTAL=f'${total:,}', CREDITS=credits).items():
    page = page.replace('{{'+k+'}}', v)
for k, v in GF.items(): page = page.replace('{{GF_'+k+'}}', E(v))
for k, v in L.items(): page = page.replace('{{L_'+k+'}}', E(v))
import re
def picrep(m):
    key, alt = m.group(1), m.group(2)
    return pic(key, alt, 'cover')
page = page.replace('{{BTN_ECO}}', a(GF['b_eco'],'Economy fares')).replace('{{BTN_PREM}}', a(GF['b_prem'],'Premium fares')).replace('{{BTN_BIZ}}', a(GF['b_biz'],'Business fares'))
page = page.replace('{{A_LINKS}}', a(GF['a_eco'],'Economy','chip')+a(GF['a_prem'],'Premium','chip')+a(GF['a_biz'],'Business','chip'))
page = re.sub(r'\{\{PIC:([\w-]+)\|([^}]*)\}\}', picrep, page)
page = page.replace('{{HERO}}', pic('adare', 'Adare Manor, County Limerick', 'hero-img', eager=True, sizes='100vw'))
assert '{{' not in page, re.findall(r'\{\{[^}]*\}\}', page)
open('index.html', 'w').write(page)
print('built, total', total)
