"""National location directory and image-led B2B pages. Called by build.py."""
import csv,json,re,unicodedata
from service_answers import render as service_answers
from niche_services import (NICHE_SERVICES, NICHE_SLUGS, NICHE_IMAGES, FR_NICHE, RELATED, details as niche_details, links as niche_links, local_links as niche_local_links)
from local_growth import (POST_SLUG, POST_PATH, FR_POST_PATH, COST_PATH, FR_COST_PATH, POST_IMAGE, FR_POST_IMAGE, COST_IMAGES, POST_SERVICE, city_sections, resource_links, post_details, cost_article)
from html import escape as e
from pathlib import Path
from urllib.parse import urlencode
ROOT=Path(__file__).parent
CITIES=json.loads((ROOT/'data/cities.json').read_text())
PROVINCES=json.loads((ROOT/'data/provinces.json').read_text())
MUNICIPALITIES=json.loads((ROOT/'data/municipalities.json').read_text())
BY_CODE={p['code']:p for p in PROVINCES}
BY_SLUG={c['slug']:c for c in CITIES}
EXTRA=[
('high-level-cobweb-removal','High-level cobweb removal','Clear the corners routine cleaning cannot reach.','', 'Target cobwebs around roof structures, elevated corners, fixtures and loading-area ceilings. The scope is defined around access and protection of the spaces below; pest treatment is a separate service.', ['Ceiling corners, truss connections and high ledges','Elevated entrance and loading-area surfaces where accessible','A focused add-on to a broader overhead cleaning scope']),
('elevated-fixture-cleaning','Elevated fixture cleaning','More attention to the details in plain sight.','', 'Plan surface cleaning for elevated lighting housings, signs and suspended fixtures. Identify delicate finishes and equipment requiring isolation by your facility team before work is considered.', ['Accessible exterior surfaces of high-bay lighting','Elevated signage and suspended non-electrical surfaces','Finish compatibility and access review before cleaning']),
('ceiling-fan-cleaning','Ceiling fan cleaning','Address the dust above the moving air.','', 'Dust on high ceiling fans needs a suitable access plan and equipment isolation. Include fan height, diameter, manufacturer information and the activity below each fan in your request.', ['High-volume, low-speed fans and accessible housings','Blade and exterior surface cleaning where compatible','Site-controlled isolation and manufacturer care requirements']),
('equipment-exterior-cleaning','Equipment exterior cleaning','Include the hard-to-reach equipment surfaces.','', 'Add elevated equipment exteriors to an overhead cleaning scope where access, materials and site procedures allow. This work addresses external surfaces and requires coordination with the equipment owner.', ['Accessible tops and exteriors of industrial equipment','Protection of openings, sensors and sensitive components','Equipment-specific boundaries and site isolation requirements']),
('shutdown-cleaning','Shutdown cleaning','Make the maintenance window count.','', 'Coordinate overhead cleaning within a planned production shutdown. Define access release, other trades, equipment protection and handover requirements before agreeing a work sequence.', ['Overhead cleaning aligned with a planned outage','Work-zone sequencing with the facility maintenance team','Clear scope boundaries and an agreed return-to-service handover']),
('recurring-overhead-maintenance','Recurring overhead maintenance','A repeatable plan for the areas above.','', 'Establish a recurring high-dusting scope based on your facility, observed buildup and access windows. Set review points so frequency can be adjusted as operations or conditions change.', ['Repeat scopes for defined overhead areas','Single-site and multi-location planning','Frequency based on conditions rather than a universal schedule'])]
INDUSTRIES={
'warehouses':('Warehouses & distribution','Storage keeps moving. Plan the clean around it.','Tell us how stock, people and equipment move through your building. Racking layout, aisle release and receiving hours help define a realistic overhead scope.',['Separate rack height from ceiling height','Identify stock that needs covering or relocation','Show access through the narrowest working aisle'],['warehouse-high-dusting','rafter-beam-cleaning','high-level-cobweb-removal']),
'manufacturing':('Manufacturing & industrial','Fit the clean into the production plan.','Every production area has its own access and material constraints. Describe the process, the dust and any equipment that must be protected or isolated.',['Identify process dust before selecting methods','Mark crane, conveyor and machine obstructions','Agree work release and handover with maintenance'],['manufacturing-high-dusting','equipment-exterior-cleaning','shutdown-cleaning']),
'food-processing':('Food processing & packaging','Start with the sanitation boundaries.','Overhead work in a food facility is coordinated with your own sanitation and quality teams. Product exposure, dust characteristics and production timing guide assessment.',['Separate open-product, packaging and storage zones','Identify potentially combustible organic dust','Coordinate cleaning with the sanitation sequence'],['food-facility-high-dusting','pipe-conduit-cleaning','shutdown-cleaning']),
'retail':('Retail & commercial spaces','A better view for customers and staff.','Expose the right details in your quote request: fixtures, signage, decorative ceilings and the finished surfaces below. Tell us when public access can be controlled.',['Include customer hours and delivery access','Identify fragile displays and finishes','Define exterior fixture cleaning separately from servicing'],['commercial-high-dusting','elevated-fixture-cleaning','ceiling-fan-cleaning']),
'arenas':('Arenas & recreation centres','Work around the next booking.','Sports and recreation spaces combine broad overhead spans with sensitive playing surfaces. Include bookings, seasonal changes and floor protection when planning high-level work.',['List event and maintenance windows','Identify court, turf or ice-surface restrictions','Show suspended scoreboards, lights and roof trusses'],['ceiling-cleaning','rafter-beam-cleaning','elevated-fixture-cleaning']),
'education':('Schools & universities','Plan above the timetable.','Campus and school buildings can have very different overhead conditions. Scope gyms, atria, workshops and support spaces individually, with access coordinated through the site team.',['Use building-specific access and occupancy windows','Protect teaching, research and sports equipment','Flag decorative ceilings and fragile finishes'],['commercial-high-dusting','ceiling-cleaning','recurring-overhead-maintenance'])}
FR_INDUSTRIES={'warehouses':'Entrepôts et distribution','manufacturing':'Fabrication et industrie','food-processing':'Transformation et emballage alimentaires','retail':'Commerces et bâtiments commerciaux','arenas':'Arénas et centres sportifs','education':'Écoles et universités'}
FR_SERVICE={'commercial-high-dusting':'Dépoussiérage commercial','industrial-high-dusting':'Dépoussiérage industriel','warehouse-high-dusting':'Dépoussiérage d’entrepôts','ceiling-cleaning':'Nettoyage des plafonds','rafter-beam-cleaning':'Nettoyage des poutres et charpentes','pipe-conduit-cleaning':'Nettoyage des tuyaux et conduits','duct-exterior-cleaning':'Nettoyage extérieur des gaines','hepa-high-dusting':'Aspiration avec filtration HEPA','food-facility-high-dusting':'Dépoussiérage en milieu alimentaire','manufacturing-high-dusting':'Dépoussiérage des installations de fabrication','high-level-cobweb-removal':'Retrait des toiles d’araignée en hauteur','elevated-fixture-cleaning':'Nettoyage des luminaires et enseignes','ceiling-fan-cleaning':'Nettoyage des ventilateurs de plafond','equipment-exterior-cleaning':'Nettoyage extérieur des équipements','shutdown-cleaning':'Nettoyage pendant un arrêt de production','recurring-overhead-maintenance':'Entretien récurrent en hauteur'}
FR_SERVICE[POST_SLUG] = 'Dépoussiérage après construction'
FR_SERVICE.update(FR_NICHE)
# Human-authored translations for the single-step French quote form.
FR={
'Have photos or videos? Send your quote request here, then email files to ':'Vous avez des photos ou vidéos? Envoyez votre demande ici, puis transmettez vos fichiers à ',
'. Include your name and city so we can match them to your request.':'. Indiquez votre nom et votre ville pour associer les fichiers à votre demande.',
'Let’s talk':'Parlons de votre projet',
'Tell us what’s<br>up there.':'Décrivez-nous<br>vos espaces en hauteur.',
'Tell us where you are and what needs cleaning. We’ll follow up to discuss the details.':'Indiquez votre ville et les surfaces à nettoyer. Nous communiquerons avec vous pour discuter des détails.',
'Prefer to talk through the details?':'Vous préférez en discuter?',
'Request a quote':'Demander une soumission',
'Full name *':'Nom complet *',
'Email *':'Courriel *',
'Phone (optional)':'Téléphone (facultatif)',
'City & province *':'Ville et province *',
'e.g. Toronto, ON':'Ex. Montréal, QC',
'What needs cleaning? *':'Que faut-il nettoyer? *',
'A short description of your space and what you need cleaned.':'Décrivez brièvement vos espaces et les surfaces à nettoyer.',
'Add photos or videos (optional)':'Ajouter des photos ou vidéos (facultatif)',
'Photos or videos (optional)':'Photos ou vidéos (facultatif)',
'Up to 5 files, 10 MB each. JPG, PNG, WebP, MP4 or MOV.':'Jusqu’à 5 fichiers de 10 Mo. JPG, PNG, WebP, MP4 ou MOV.',
'privacy notice':'politique de confidentialité',
'Send request':'Envoyer la demande',
'* Required fields':'* Champs obligatoires'}

def normalized(value):return ''.join(c for c in unicodedata.normalize('NFKD',value.casefold()) if not unicodedata.combining(c)).replace('’',"'")
def city_url(c):return f"/locations/{BY_CODE[c['province']]['slug']}/{c['slug']}/"
def quote_url(city='',service='',source=''):
 return '/?'+urlencode({k:v for k,v in [('city',city),('service',service),('source',source)] if v})+'#quote'
def translate(text):
 for a,b in sorted(FR.items(),key=lambda kv:-len(kv[0])):text=text.replace(a,b)
 return text

def build(base):
 write=base['write'];original_page=base['page'];services=base['SERVICES']+EXTRA+[POST_SERVICE]+NICHE_SERVICES;service_by={s[0]:s for s in services}
 def form(city='',service='',fr=False):
  q=base['quote'].replace('id="quote-form"',f'id="quote-form" data-city="{e(city)}" data-service="{e(service)}" data-language="{"fr" if fr else "en"}"')
  if fr:q=translate(q).replace('href="/privacy/"','href="/fr/confidentialite/"')
  q=q.replace('name="city" value=""',f'name="city" value="{e(city)}"')
  q=q.replace('name="selected_city" value=""',f'name="selected_city" value="{e(city)}"')
  q=q.replace('name="selected_service" value=""',f'name="selected_service" value="{e(service)}"')
  if fr:q=q.replace('name="language" value="en-CA"','name="language" value="fr-CA"')
  return q
 def render(title,desc,content,path,image,fr=False):
  html=original_page(title,desc,content,path)
  html=html.replace('</head>',f'<meta property="og:locale" content="{"fr_CA" if fr else "en_CA"}"></head>')
  html=html.replace('https://highdusting.ca/assets/hero.webp','https://highdusting.ca'+image).replace('href="/assets/hero.webp" as="image"',f'href="{image}" as="image"')
  html=html.replace('href="/#quote"','href="#quote"') if 'id="quote-form"' in content else html
  html=html.replace('href="/#coverage"','href="/locations/"').replace('href="/#industries"','href="/industries/"')
  if fr:
   html=html.replace('lang="en-CA"','lang="fr-CA"').replace('Commercial facility','Établissement commercial').replace('<small>Quebec</small>','<small>Québec</small>')
   html=html.replace(base['header'](),french_header()).replace(base['footer'](),french_footer())
   # Navigation substitutions above mean match through the same replacements.
   old=base['header']().replace('href="/#coverage"','href="/locations/"').replace('href="/#industries"','href="/industries/"')
   html=html.replace(old,french_header()).replace(old.replace('href="/#quote"','href="#quote"'),french_header())
   old=base['footer']().replace('href="/#coverage"','href="/locations/"').replace('href="/#industries"','href="/industries/"')
   html=html.replace(old,french_footer()).replace(old.replace('href="/#quote"','href="#quote"'),french_footer())
  if fr and 'id="quote-form"' not in content:html=html.replace('href="#quote"','href="/locations/quebec/#quote"')
  labels={s[0]:(FR_SERVICE[s[0]] if fr else s[1]) for s in services}
  html=html.replace('</head>','<script id="service-labels" type="application/json">'+json.dumps(labels,ensure_ascii=False)+'</script></head>')
  return html
 def french_header():
  return '''<a class="skip" href="#main">Aller au contenu</a><div class="topbar"><div class="container"><span>DÉPOUSSIÉRAGE COMMERCIAL ET INDUSTRIEL AU CANADA</span><span>Les surfaces en hauteur. Notre spécialité.</span></div></div><header class="header"><div class="container nav"><a class="brand" href="/locations/quebec/" aria-label="HighDusting.ca Québec"><span class="brand-art"><img class="brand-logo" src="/assets/logo-industrial-seal.png" width="2048" height="686" alt="HighDusting.ca"></span></a><nav class="navlinks" id="navigation" aria-label="Navigation principale"><a href="/locations/quebec/#services">Services</a><a href="/locations/quebec/#industries">Secteurs</a><a href="/locations/quebec/">Villes du Québec</a><a href="/locations/" lang="en">Canada · EN</a></nav><div class="nav-actions"><a href="tel:+18884513878">(888) 451 - DUST (3878)</a><a class="btn" href="#quote">Soumission <span class="arrow">↗</span></a><button class="menu-button" aria-label="Ouvrir le menu" aria-expanded="false" aria-controls="navigation">☰</button></div></div></header>'''
 def french_footer():
  return '''<footer class="footer"><div class="container"><div class="footer-grid"><div><a class="brand" href="/locations/quebec/" aria-label="HighDusting.ca Québec"><span class="brand-art"><img class="brand-logo" src="/assets/logo-industrial-seal-white.png" width="2048" height="686" alt="HighDusting.ca"></span></a><p>Dépoussiérage commercial et industriel. Les surfaces en hauteur, au cœur de notre travail.</p></div><div><h4>Votre projet</h4><a href="#quote">Demander une soumission</a><a href="tel:+18884513878">(888) 451 - DUST (3878)</a><a href="mailto:info@highdusting.ca">info@highdusting.ca</a></div><div><h4>Nos secteurs</h4><a href="/locations/quebec/#industries">Entrepôts et fabrication</a><a href="/locations/quebec/#industries">Commerces et établissements</a></div><div><h4>Nos régions</h4><a href="/locations/quebec/">Villes du Québec</a><a href="/locations/" lang="en">Canada · English</a></div></div><div class="footer-bottom"><span>© 2026 HighDusting.ca.</span><span>Disponibilité et méthodes confirmées après évaluation du site.</span><a href="/fr/confidentialite/">Confidentialité</a></div></div></footer><a class="mobile-cta" href="#quote">Demander une soumission <span>↗</span></a>'''
 def hero(title,desc,image,eyebrow='Commercial & industrial · Canada',breadcrumb='',fr=False):
  return f'''<section class="hero detail-hero location-hero{' framed-hero' if image in (POST_IMAGE,FR_POST_IMAGE,*COST_IMAGES.values(),*NICHE_IMAGES) else ''}"><img class="hero-image" src="{image}" alt="{e(title.capitalize())}" fetchpriority="high" width="1536" height="1024"><div class="container hero-content"><div class="breadcrumb">{breadcrumb}</div><div class="eyebrow">{eyebrow}</div><h1>{title}</h1><p>{desc}</p><div class="hero-buttons"><a class="btn" href="#quote">{'Demander une soumission' if fr else 'Scope your project'} <span>↗</span></a></div></div></section>'''
 def service_cards(slugs,fr=False,city='',origin=''):
  cards=[]
  for slug in slugs:
   s=service_by[slug];title=FR_SERVICE[slug] if fr else s[1]
   target='#quote' if fr else '/services/'+slug+'/'
   if city and not fr:target+='?'+urlencode({'city':city,'source':origin})
   target=e(target)
   if slug in NICHE_SLUGS:
    cards.append(f'<a class="service-card service-card-text" href="{target}"'+(f' data-service-choice="{e(slug)}"' if fr else '')+f'><div class="service-copy"><div class="eyebrow">{"Surfaces spécialisées" if fr else "Specialist surfaces"}</div><h3>{e(title)}</h3><p>{"Une portée de travaux adaptée à votre établissement." if fr else e(s[2])}</p><span class="text-link">{"Discuter de ce service" if fr else "Explore service"} ↗</span></div></a>')
    continue
   cards.append(f'<a class="service-card" href="{target}"'+(f' data-service-choice="{e(slug)}"' if fr else '')+f'><div class="service-image"><img loading="lazy" src="/assets/services/{slug}.webp" alt="{e(title)}" width="1536" height="1024"></div><div class="service-copy"><h3>{title}</h3><p>{"Une portée de travaux adaptée à votre établissement." if fr else s[2]}</p><span class="text-link">{"Discuter de ce service" if fr else "Explore service"} ↗</span></div></a>')
  return '<div class="service-grid">'+''.join(cards)+'</div>'
 def city_cards(cities):
  return '<div class="city-grid">'+''.join(f'<a class="city-card" href="{city_url(c)}"><img loading="lazy" width="1536" height="1024" src="/assets/cities/{c["slug"]}.webp" alt="Commercial facility"><div><small>{BY_CODE[c["province"]]["name"]}</small><h3>{c["name"]} <span>↗</span></h3></div></a>' for c in cities)+'</div>'
 def city_planning_links(fr=False):
  slugs=['montreal','quebec-city','laval','gatineau','longueuil','sherbrooke','trois-rivieres'] if fr else ['toronto','mississauga','ottawa','vancouver','surrey','calgary','edmonton','winnipeg','saskatoon','regina','halifax','st-johns']
  heading='Préparer votre projet au Québec' if fr else 'Plan for your city'
  text='Consultez les notes de remise des lieux et les facteurs de prix pour votre ville.' if fr else 'Explore handover planning and cost considerations for your local facility.'
  links=''.join(f'<a href="{city_url(BY_SLUG[slug])}#post-construction">{e(BY_SLUG[slug]["name"])} ↗</a>' for slug in slugs)
  return f'<section class="section"><div class="container"><h2>{heading}</h2><p class="planning-note">{text}</p><div class="industry-chips">{links}</div><p class="planning-note"><a class="text-link" href="/locations/">'+('Toutes les villes canadiennes' if fr else 'Explore all Canadian cities')+' ↗</a></p></div></section>'
 all_paths=['/','/services/','/privacy/']
 # Location search references published city pages and gives every other census community a scoped enquiry link.
 matching={(normalized(c['name']),c['province']):c for c in CITIES}
 matching[('quebec','QC')]=BY_SLUG['quebec-city'];matching[("st. john's",'NL')]=BY_SLUG['st-johns']
 directory=[]
 canonical_ids={}
 for m in sorted(MUNICIPALITIES,key=lambda x:x['population'] or 0,reverse=True):canonical_ids.setdefault((normalized(m['name']),m['province']),m['id'])
 for m in MUNICIPALITIES:
  key=(normalized(m['name']),m['province'])
  c=matching.get(key) if canonical_ids[key]==m['id'] else None
  directory.append(dict(id=m['id'],name=m['name'],province=m['province'],division=m.get('division',''),url=city_url(c) if c else quote_url(m['name']+', '+m['province'],source='/locations/'),featured=bool(c)))
 for c in CITIES:
  if not any(x['url']==city_url(c) for x in directory):directory.append(dict(id='local-'+c['slug'],name=c['name'],province=c['province'],url=city_url(c),featured=True))
 write('assets/locations.json',json.dumps(directory,ensure_ascii=False,separators=(',',':')))
 intro='''<section class="directory-heading"><div class="container"><div class="eyebrow">Commercial & industrial · Coast to coast</div><h1>FIND YOUR CITY.<br>PLAN YOUR CLEAN.</h1><p>Explore local high dusting pages or tell us where your facility is. Every enquiry starts with your site, your scope and local availability.</p><form class="location-search" id="location-search" action="/locations/" method="get"><label>City or community<input type="search" name="q" id="location-query" placeholder="Search Toronto, Trois-Rivières, Whitehorse…" autocomplete="off"></label><label>Province or territory<select name="province" id="location-province"><option value="">All of Canada</option>'''+''.join(f'<option value="{p["code"]}">{p["name"]}</option>' for p in PROVINCES)+'''</select></label><button class="btn dark" type="submit">Find location ↗</button></form><p id="location-status" aria-live="polite" class="directory-status">Browse the featured locations below, or search the national directory.</p><div id="location-results" class="location-results" hidden></div><button id="location-more" class="btn dark" type="button" hidden>Show more locations</button><noscript><p>Choose a province below, or <a href="/#quote"><u>enter your city in the quote form</u></a>.</p></noscript></div></section>'''
 province_tiles='<section class="section province-section"><div class="container"><div class="section-heading"><div><div class="eyebrow">Explore by region</div><h2>Across Canada.<br>Specific to your site.</h2></div></div><div class="province-grid">'+''.join(f'<a class="province-tile" href="/locations/{p["slug"]}/"><img src="/assets/provinces/{p["slug"]}.webp" alt="Commercial facility with overhead structures" loading="lazy"><span>{p["name"]} ↗</span></a>' for p in PROVINCES)+'</div></div></section>'
 location_content=intro+province_tiles+'<section class="section"><div class="container"><div class="section-heading"><div><div class="eyebrow">Local project planning</div><h2>Explore your market.</h2></div></div>'+city_cards(CITIES)+'</div></section><section class="directory-source container"><p>Directory geography: Statistics Canada, 2021 Census subdivisions (5,161 entries), plus named service communities. Boundaries and names may have changed. A listing is a location reference; service availability is assessed for each request. Can’t find your location? Enter it directly in the quote form.</p><a href="https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=9810000201" target="_blank" rel="noopener">Statistics Canada · Table 98-10-0002-01</a></section>'+form()
 write('locations/index.html',render('High Dusting Across Canada | Find Your City','Find commercial and industrial high dusting by city or province. Search Canadian communities and request a location-specific assessment.',location_content,'/locations/','/assets/canada-directory.webp'));all_paths.append('/locations/')
 # All city pages have their own original image, contextual form, local notes and relevant service scope.
 for c in CITIES:
  fr=c['province']=='QC';p=BY_CODE[c['province']];path=city_url(c);name=c['name'];focus=INDUSTRIES[c['focus']];slugs=focus[4];image='/assets/cities/'+c['slug']+'.webp'
  title=f'Dépoussiérage en hauteur à {name}, QC' if fr else f'High dusting in {name}, {c["province"]}'
  desc=f'Dépoussiérage en hauteur à {name}, QC : entretien commercial et industriel, nettoyage après construction et guide des prix. Demandez une soumission.' if fr else f'Commercial and industrial high dusting in {name}, {c["province"]}. Explore post-construction overhead cleaning, cost factors and request a facility quote.'
  crumbs=f'<a href="/locations/">Canada</a> / <a href="/locations/{p["slug"]}/">{p["name"] if not fr else "Québec"}</a> / {name}'
  content=hero(title.upper(),desc,image,f'{"Projet commercial" if fr else "Facility-first planning"} · {name}, {c["province"]}',crumbs,fr)
  content+=f'<section class="section"><div class="container local-layout"><article><div class="eyebrow">{"Préparer votre demande" if fr else "Your local project brief"}</div><h2>{"Un plan adapté<br>à votre établissement." if fr else "A better scope.<br>A more useful quote."}</h2><p>{c["brief"]}</p><div class="scope-note"><h3>{"À inclure dans votre demande" if fr else "Include in your request"}</h3><ul>'
  bullets=['Adresse du site et hauteur des surfaces à nettoyer','Photos des obstacles et des zones à protéger','Nature des dépôts et horaire souhaité'] if fr else focus[3]
  content+=''.join('<li>'+b+'</li>' for b in bullets)+'</ul></div></article>'
  content+=f'<aside class="local-sidebar"><span class="eyebrow">{"Votre secteur" if fr else "A relevant starting point"}</span><h3>{FR_INDUSTRIES[c["focus"]] if fr else focus[0]}</h3><p>{"Les travaux sont évalués selon les matériaux, les accès et les exigences de votre site." if fr else "Use this as a starting point, then identify the specific surfaces and conditions at your facility."}</p><a class="btn dark" href="#quote">{"Parlons de votre site" if fr else "Discuss your facility"} ↗</a><p class="coverage-note">{"Disponibilité, déplacement et équipements confirmés avant réservation. Les travaux peuvent être réalisés par des prestataires locaux." if fr else "Local availability, mobilisation and equipment are confirmed before booking. Projects may be delivered through local service providers."}</p></aside></div></section>'
  content+=f'<section class="section local-services" id="services"><div class="container"><div class="section-heading"><div><div class="eyebrow">{"Services à évaluer" if fr else "Overhead expertise"}</div><h2>{"De la poussière aux détails." if fr else "Bring the whole overhead<br>into the conversation."}</h2></div></div>'+service_cards(slugs,fr,name+', '+c['province'],path)+'</div></section>'
  content+=niche_links(c['focus'],name+', '+c['province'],path,fr)
  content+=city_sections(c,path)
  content+=f'<section class="section local-nearby"><div class="container"><div class="eyebrow">{"Votre projet s’étend plus loin?" if fr else "Planning beyond one address?"}</div><h2>{"Communautés à proximité" if fr else "Nearby communities"}</h2><div class="industry-chips">'
  for near in c['nearby'].split(', '):
   target=next((city_url(n) for n in CITIES if normalized(n['name'])==normalized(near)),('/locations/quebec/?'+urlencode({'city':near+', QC','source':path})+'#quote') if fr else quote_url(near,source=path))
   content+=f'<a href="{e(target)}">{near} ↗</a>'
  content+=f'</div><p>{"Précisez les adresses de chaque établissement. La disponibilité est évaluée séparément pour chaque site." if fr else "Include each facility address when requesting multi-site work. Availability is assessed separately for every location."}</p></div></section>'+form(name+', '+c['province'],'',fr)
  write(path.strip('/')+'/index.html',render(title+' | HighDusting.ca',desc,content,path,image,fr));all_paths.append(path)
 # Province hubs link to every published city in their region and carry distinct images.
 for p in PROVINCES:
  fr=p['code']=='QC';name='Québec' if fr else p['name'];path=f'/locations/{p["slug"]}/';region=[c for c in CITIES if c['province']==p['code']];image=f'/assets/provinces/{p["slug"]}.webp'
  title=f'Dépoussiérage en hauteur au {name}' if fr else f'High dusting in {name}'
  desc='Dépoussiérage en hauteur au Québec pour entrepôts et bâtiments commerciaux. Précisez votre ville, les surfaces et les contraintes d’accès.' if fr else f'High dusting in {name} for commercial and industrial facilities. Explore local cities and request a scope based on your surfaces, access and timing.'
  content=hero(title.upper(),desc,image,'Commercial et industriel' if fr else 'Commercial & industrial',f'<a href="/locations/">Canada</a> / {name}',fr)
  content+=f'<section class="section"><div class="container"><div class="eyebrow">{"Villes et communautés" if fr else "Choose your city"}</div><h2>{"Un point de départ local." if fr else "Your facility. Your location."}</h2><div style="margin-top:35px">'+city_cards(region)+'</div>'
  content+=f'<p class="region-more">{"Une autre ville? Inscrivez son nom dans la demande ci-dessous." if fr else "Looking for another community?"} '+('' if fr else f'<a href="/locations/?province={p["code"]}"><u>Search all {e(name)} locations</u></a>.')+'</p></div></section>'
  if fr:
   content+='<section class="section" id="industries"><div class="container"><div class="eyebrow">Nos secteurs</div><h2>Des espaces et des besoins variés.</h2><div class="industry-chips">'+''.join('<a href="#quote">'+v+'</a>' for v in FR_INDUSTRIES.values())+'</div><p>Chaque projet est évalué selon la poussière, les matériaux, l’accès et les horaires. Les prestataires et les équipements sont confirmés selon la ville.</p></div></section>'
  content+=f'<section class="section" id="services"><div class="container"><div class="section-heading"><h2>{"Les surfaces en hauteur.<br>Notre spécialité." if fr else "Specialist services.<br>Defined around your scope."}</h2></div>'+service_cards(['warehouse-high-dusting','industrial-high-dusting','recurring-overhead-maintenance'],fr)+'</div></section>'+form('', '',fr)
  write(path.strip('/')+'/index.html',render(title+' | HighDusting.ca',desc,content,path,image,fr));all_paths.append(path)
 # Rich service pages, each with an original service-specific hero and a relevant supporting image.
 for s in services:
  slug,title,sub,_,desc,items=s;path='/services/'+slug+'/';image='/assets/services/'+slug+'.webp'
  related=RELATED.get(slug,[k for k in ['rafter-beam-cleaning','elevated-fixture-cleaning','recurring-overhead-maintenance'] if k!=slug][:2])
  content=hero(title.upper(),sub,image,breadcrumb=f'<a href="/">Home</a> / <a href="/services/">Services</a> / {title}')
  content+=f'<section class="section"><div class="container local-layout"><article><div class="eyebrow">Scope the right work</div><h2>{sub}</h2><p>{desc}</p><div class="scope-note"><h3>What to include</h3><ul>'+''.join('<li>'+x+'</li>' for x in items)+'</ul></div><p>Share photos, ceiling height, approximate area and operating windows. Surface compatibility, dust characteristics and access conditions determine the proposed method.</p></article><aside class="local-sidebar"><h3>Find your location</h3><p>Explore local planning information or include your city directly in the quote below.</p><a href="/locations/" class="btn dark">Search Canadian locations ↗</a><p>Availability and equipment are assessed for each site.</p></aside></div></section>'
  if slug in NICHE_SLUGS:content+=niche_details(slug)+niche_local_links(slug,CITIES,city_url)
  if slug==POST_SLUG:content+='<div class="container language-switch"><a href="'+FR_POST_PATH+'" lang="fr" hreflang="fr-CA">Français</a></div>'+post_details()+city_planning_links()
  content+='<section class="section local-services"><div class="container"><div class="section-heading"><h2>Consider the adjacent surfaces.</h2><p>Add related overhead areas to the same request so the full scope can be reviewed together.</p></div>'+service_cards(related)+'</div></section>'+service_answers(slug)+form(service=slug)
  write(path.strip('/')+'/index.html',render(title+' | HighDusting.ca',desc,content,path,image));all_paths.append(path)
 listing='<section class="section"><div class="container"><div class="eyebrow">Our expertise</div><h1>HIGH DUSTING SERVICES.<br>EVERY OVERHEAD DETAIL.</h1><p class="listing-intro">Explore 20 specialist services for overhead structures, fixtures and equipment. Build a scope that fits your facility.</p>'+service_cards([s[0] for s in services])+resource_links()+'</div></section>'+form()
 write('services/index.html',render('Commercial & Industrial High Dusting Services | HighDusting.ca','Explore overhead cleaning, high dusting, fixtures, fans, shutdown cleaning and recurring maintenance.',listing,'/services/','/assets/services/ceiling-cleaning.webp'))
 # Complete French counterpart for the new service.
 title='Dépoussiérage après construction'
 desc='Nettoyage en hauteur après construction, rénovation ou réaménagement commercial : poutres, conduits extérieurs, rebords et luminaires. Demandez une soumission.'
 content=hero(title.upper(),'Préparez les surfaces en hauteur pour la remise des lieux.',FR_POST_IMAGE,'Après construction · Commercial et industriel','',True)
 content+='<div class="container language-switch"><a href="'+POST_PATH+'" lang="en" hreflang="en-CA">English</a></div>'
 content+='<section class="section"><div class="container guide-content"><h2>Après les travaux.<br>Avant la remise des lieux.</h2><p>Le dépoussiérage après construction vise les dépôts sur les poutres, les charpentes, les conduits extérieurs, les rebords et les boîtiers de luminaires accessibles. Après une construction, une rénovation ou un réaménagement commercial, nous définissons ces surfaces avec votre entrepreneur ou l’équipe du site.</p><p>Le calendrier tient compte des autres corps de métier, des revêtements à protéger et de la disponibilité des zones. Toute visite après des retouches se prévoit séparément.</p></div></section>'
 content+=post_details(True)+city_planning_links(True)
 content+='<section class="section faq"><div class="container guide-content"><h2>Vos questions avant la remise</h2><details open><summary>Quand prévoir le nettoyage en hauteur?</summary><p>Après la fin des travaux poussiéreux, lorsque les accès sont libérés. Si d’autres corps de métier doivent revenir, convenez des zones et des visites supplémentaires avant de fixer la remise.</p></details><details open><summary>Le nettoyage complet du chantier est-il inclus?</summary><p>La portée proposée concerne les surfaces en hauteur convenues. Les sols, les vitres, le gros débris et les traitements spécialisés doivent être définis séparément.</p></details></div></section>'+form(service=POST_SLUG,fr=True)
 write(FR_POST_PATH.strip('/')+'/index.html',render(title+' | HighDusting.ca',desc,content,FR_POST_PATH,FR_POST_IMAGE,True));all_paths.append(FR_POST_PATH)
 # Cost guides explain how quotes are scoped without inventing price ranges.
 for fr in (False,True):
  path=FR_COST_PATH if fr else COST_PATH
  title='Prix du dépoussiérage en hauteur au Canada' if fr else 'High Dusting Cost in Canada'
  desc='Comprendre le prix du dépoussiérage en hauteur : surfaces, accès, équipements, horaires et mobilisation. Comparez les soumissions et décrivez votre projet.' if fr else 'Understand high dusting costs in Canada: surfaces, access, equipment, working windows and mobilisation. Compare quote scopes and request pricing for your facility.'
  content=hero(title.upper(),'Les bonnes questions pour préparer votre budget.' if fr else 'Know what shapes your quote. Plan with a clearer scope.',COST_IMAGES[fr],'Guide des prix' if fr else 'Facility pricing guide','',fr)
  content+='<div class="container language-switch"><a href="'+(COST_PATH if fr else FR_COST_PATH)+'" lang="'+('en' if fr else 'fr')+'" hreflang="'+('en-CA' if fr else 'fr-CA')+'">'+('English' if fr else 'Français')+'</a></div>'
  content+=cost_article(fr)+city_planning_links(fr)+form(fr=fr)
  write(path.strip('/')+'/index.html',render(title+' | HighDusting.ca',desc,content,path,COST_IMAGES[fr],fr));all_paths.append(path)
 for slug,(title,sub,desc,checks,slugs) in INDUSTRIES.items():
  path='/industries/'+slug+'/';image='/assets/industries/'+slug+'.webp'
  content=hero(title.upper(),sub,image,breadcrumb=f'<a href="/">Home</a> / <a href="/industries/">Industries</a> / {title}')
  content+='<section class="section"><div class="container local-layout"><article><div class="eyebrow">For facility and operations teams</div><h2>'+sub+'</h2><p>'+desc+'</p><div class="scope-note"><h3>Plan the details up front</h3><ul>'+''.join('<li>'+x+'</li>' for x in checks)+'</ul></div></article><aside class="local-sidebar"><h3>A scope for your operation</h3><p>Include facility-specific requirements and photos of both the overhead surfaces and the work area below.</p><a href="/locations/" class="btn dark">Find your location ↗</a></aside></div></section><section class="section"><div class="container">'+service_cards(slugs)+'</div></section>'+form(service=slugs[0])
  content=content.replace(form(service=slugs[0]),niche_links(slug)+form(service=slugs[0]))
  write(path.strip('/')+'/index.html',render(title+' High Dusting | HighDusting.ca',desc,content,path,image));all_paths.append(path)
 industry_content='<section class="section"><div class="container"><div class="eyebrow">Built for B2B facilities</div><h1>HIGH DUSTING.<br>FOR YOUR INDUSTRY.</h1><p class="listing-intro">Explore the overhead planning considerations for your industry.</p><div class="city-grid">'+''.join(f'<a class="city-card" href="/industries/{slug}/"><img loading="lazy" src="/assets/industries/{slug}.webp" alt="{v[0].lower()} facility"><div><h3>{v[0]} ↗</h3></div></a>' for slug,v in INDUSTRIES.items())+'</div></div></section>'+form()
 write('industries/index.html',render('Industries We Serve | HighDusting.ca','High dusting for warehouses, manufacturing, food processing, retail, arenas and education facilities.',industry_content,'/industries/','/assets/industries/warehouses.webp'));all_paths.append('/industries/')
 # Enrich homepage without replacing its established identity.
 home=(ROOT/'index.html').read_text()
 home=home.replace(base['quote'],form()).replace('href="/#coverage"','href="/locations/"').replace('href="/#industries"','href="/industries/"')
 # Replace only the repeated service-card images, preserving main hero.
 for slug in ['warehouse-high-dusting','ceiling-cleaning','hepa-high-dusting']:
  pattern=r'(<a class="service-card" href="/services/'+slug+r'/"><div class="service-image"><img loading="lazy" src=")[^"]+'
  home=re.sub(pattern,r'\g<1>/assets/services/'+slug+'.webp',home)
 for old,new in [('/services/warehouse-high-dusting/','/industries/warehouses/'),('/services/manufacturing-high-dusting/','/industries/manufacturing/'),('/services/commercial-high-dusting/','/industries/retail/')]:
  home=home.replace('<a class="industry-card" href="'+old+'"','<a class="industry-card" href="'+new+'"')
 for slug in ['warehouses','manufacturing','retail']:
  home=re.sub(r'(<a class="industry-card" href="/industries/'+slug+r'/"><img src=")[^"]+',r'\g<1>/assets/industries/'+slug+'.webp',home)
 gallery='<section class="section visual-gallery"><div class="container"><div class="section-heading"><div><div class="eyebrow">Look closer. Look higher.</div><h2>From the big picture<br>to the overhead details.</h2></div><a href="/services/" class="text-link">Explore all 20 services ↗</a></div><div class="detail-gallery">'
 for slug in ['rafter-beam-cleaning','pipe-conduit-cleaning','elevated-fixture-cleaning','ceiling-fan-cleaning']:
  gallery+=f'<a href="/services/{slug}/"><img src="/assets/services/{slug}.webp" loading="lazy" alt="{service_by[slug][1].lower()}"><span>{service_by[slug][1]} ↗</span></a>'
 gallery+='</div></div></section>'
 home=home.replace('<section class="section industries"',gallery+'<section class="section industries"',1)
 coverage='<section class="section home-locations" id="coverage"><div class="container"><div class="section-heading"><div><div class="eyebrow">One point of contact · Canadian locations</div><h2>Your city.<br>Your overhead project.</h2></div><a href="/locations/" class="text-link">Search the national directory ↗</a></div>'+city_cards([BY_SLUG[s] for s in ['toronto','montreal','vancouver','calgary','halifax','winnipeg']])+'<p class="coverage-note">Explore location-specific planning. Local availability and mobilisation are confirmed for each project.</p></div></section>'
 home=home.replace(base['coverage'],coverage)
 home=home.replace('<section class="section quote-section"', '<section class="section planning-resources"><div class="container"><div class="eyebrow">Plan your next clean</div><h2>After construction.<br>Before your next step.</h2><p>Explore overhead cleaning after a build or renovation, and understand what affects your high dusting quote.</p>'+resource_links()+'</div></section><section class="section quote-section"',1)
 home=home.replace('</head>','<script id="service-labels" type="application/json">'+json.dumps({s[0]:s[1] for s in services})+'</script></head>')
 write('index.html',home)
 # French privacy page for complete Quebec enquiries.
 privacy='''<section class="section"><div class="container privacy"><div class="eyebrow">Vos renseignements</div><h1>CONFIDENTIALITÉ</h1><p>Mise à jour : 10 septembre 2026.</p><h2>Renseignements recueillis</h2><p>Une demande de soumission peut comprendre vos coordonnées professionnelles, les détails de votre établissement, la ville, le service demandé et des photos ou vidéos facultatives.</p><h2>Envoi des demandes</h2><p>Les détails de votre demande sont transmis par Formspree, notre fournisseur de traitement des formulaires. Les photos ou vidéos facultatives peuvent être envoyées séparément à info@highdusting.ca.</p><h2>Utilisation</h2><p>Ces renseignements servent à évaluer votre projet, à communiquer avec vous et à coordonner les travaux éventuels. Les détails pertinents peuvent être communiqués aux prestataires concernés par l’évaluation ou la réalisation. La page d’origine de la demande est conservée pour comprendre le besoin.</p><h2>Vos choix</h2><p>Pour demander une correction ou une suppression, ou poser une question sur vos renseignements, appelez le <a href="tel:+18884513878"><u>(888) 451 - DUST (3878)</u></a>. Certaines données peuvent être conservées pour administrer un projet en cours ou respecter les obligations applicables.</p><h2>Technologie du site</h2><p>Le site n’utilise pas de témoins publicitaires. Les polices sont fournies par Google Fonts, qui reçoit les renseignements techniques nécessaires à la connexion, dont l’adresse IP. Le service d’hébergement peut traiter des journaux techniques.</p><a class="btn dark" href="/locations/quebec/#quote">Retour à la demande ↗</a></div></section>'''
 write('fr/confidentialite/index.html',render('Confidentialité | HighDusting.ca','Utilisation des renseignements transmis dans une demande de soumission.',privacy,'/fr/confidentialite/','/assets/provinces/quebec.webp',True));all_paths.append('/fr/confidentialite/')
 paths=sorted(set(all_paths))
 write('sitemap.xml','<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+''.join(f'<url><loc>https://highdusting.ca{path}</loc></url>' for path in paths)+'</urlset>')
 report={'city_pages':len(CITIES),'province_pages':len(PROVINCES),'service_pages':len(services),'industry_pages':len(INDUSTRIES),'directory_entries':len(directory),'indexable_pages':len(paths),'guide_pages':2,'translated_service_pages':1,'geography_reference_year':2021}
 write('data/build-report.json',json.dumps(report,indent=2));print(json.dumps(report))
