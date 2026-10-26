"""French national entry point and explicit, crawlable language navigation."""
import json
import re
import xml.etree.ElementTree as ET
from html import escape
from local_growth import TRANSLATIONS, FR_POST_PATH, FR_COST_PATH
from expansion import FR_SERVICE, translate

NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
PAIRS = {'/': '/fr/', '/privacy/': '/fr/confidentialite/', **TRANSLATIONS}


def build(base):
    root = base['ROOT']
    sample = (root / FR_POST_PATH.strip('/') / 'index.html').read_text()
    header = re.search(r'<body>(.*?)<main', sample).group(1)
    footer = re.search(r'</main>(.*?)</body>', sample).group(1)
    quote = translate(base['quote']).replace('href="/privacy/"', 'href="/fr/confidentialite/"')
    quote = quote.replace('id="quote-form"', 'id="quote-form" data-language="fr"')
    quote = quote.replace('name="language" value="en-CA"', 'name="language" value="fr-CA"')
    hero = '''<section class="hero home-hero"><img class="hero-image" src="/assets/hero.webp" alt="Technicien nettoyant les poutres d’un entrepôt à l’aide d’une plateforme élévatrice" width="1536" height="1024" fetchpriority="high"><div class="container hero-content"><div class="eyebrow">Dépoussiérage commercial et industriel · Canada</div><h1>LES SURFACES<br>EN HAUTEUR.<br><em>NOTRE SPÉCIALITÉ.</em></h1><p>Plafonds, poutres, charpentes et conduits extérieurs : nous nettoyons les endroits que votre entretien quotidien n’atteint pas.</p><div class="hero-buttons"><a class="btn" href="#quote">Demander une soumission ↗</a><a class="btn outline" href="#services">Découvrir nos services ↓</a></div><div class="hero-footnote"><span>Établissements commerciaux et industriels</span><span>Travaux planifiés selon vos activités</span></div></div></section>'''
    featured = [('warehouse-high-dusting', 'Pour les entrepôts et centres de distribution : poutres, charpentes et surfaces au-dessus des zones de stockage.'), ('ceiling-cleaning', 'Définissez les plafonds, structures et surfaces accessibles à inclure dans votre projet.'), ('hepa-high-dusting', 'Aspiration avec filtration à haute efficacité (HEPA), lorsque les poussières et les surfaces s’y prêtent.')]
    cards = ''.join(f'<a class="service-card" href="#quote" data-service-choice="{slug}"><div class="service-image"><img loading="lazy" src="/assets/services/{slug}.webp" alt="{escape(FR_SERVICE[slug])}" width="1536" height="1024"></div><div class="service-copy"><h3>{FR_SERVICE[slug]}</h3><p>{desc}</p><span class="text-link">Discuter de ce service ↗</span></div></a>' for slug, desc in featured)
    services = '<section class="section" id="services"><div class="container"><div class="section-heading"><div><div class="eyebrow">Chaque surface compte</div><h2>De grands espaces.<br>Une attention aux détails.</h2></div><p>Une portée de travaux adaptée à vos surfaces, à la poussière présente et aux accès disponibles.</p></div><div class="service-grid">'+cards+'</div><h3 class="fr-subheading">Tous nos services</h3><div class="industry-chips">'+''.join(f'<a href="#quote" data-service-choice="{slug}">{escape(title)} ↗</a>' for slug,title in FR_SERVICE.items())+f'</div><p class="region-more"><a class="text-link" href="{FR_POST_PATH}">Dépoussiérage après construction : préparer la remise des lieux ↗</a></p></div></section>'
    approach = '''<section class="feature" id="approach"><div class="feature-image"><img src="/assets/overhead.webp" alt="Charpente métallique et conduits en hauteur dans un bâtiment industriel" loading="lazy" width="1536" height="1024"></div><div class="feature-copy"><div class="eyebrow">Un travail bien préparé</div><h2>Nettoyer en hauteur.<br>Respecter vos activités.</h2><p>Nous planifions les travaux selon les accès, les équipements sensibles et les personnes présentes sous les zones à nettoyer.</p><ul class="feature-list"><li><div><strong>Préciser la portée</strong><span>Les surfaces, les dépôts et la hauteur guident le choix des méthodes.</span></div></li><li><div><strong>Convenir du moment</strong><span>Les travaux hors des heures d’ouverture, la fin de semaine ou pendant un arrêt sont évalués selon votre projet.</span></div></li><li><div><strong>Coordonner les accès</strong><span>Équipements d’accès, protection des zones et exigences du site sont discutés avant les travaux.</span></div></li></ul><a class="text-link" href="#quote">Parlons de votre établissement ↗</a></div></section>'''
    sectors = [('warehouses','Entrepôts et distribution','Des allées de stockage aux zones de chargement.'),('manufacturing','Fabrication et industrie','Une planification adaptée à la production.'),('retail','Commerces et bâtiments commerciaux','Un entretien qui tient compte des occupants et de la clientèle.')]
    industries = '<section class="section industries" id="industries"><div class="container"><div class="section-heading"><div><div class="eyebrow">Votre établissement, vos besoins</div><h2>Des secteurs différents.<br>La même attention en hauteur.</h2></div></div><div class="industry-grid">'+''.join(f'<a class="industry-card" href="#quote"><img src="/assets/industries/{slug}.webp" alt="{title}" loading="lazy"><div><h3>{title}</h3><p>{desc}</p><b>↗</b></div></a>' for slug,title,desc in sectors)+'</div><div class="industry-chips"><a href="#quote">Transformation alimentaire ↗</a><a href="#quote">Arénas et centres sportifs ↗</a><a href="#quote">Écoles et universités ↗</a><a href="#quote">Installations de transport ↗</a><a href="#quote">Plusieurs établissements ↗</a></div></div></section>'
    process = '''<section class="section process"><div class="container"><div class="section-heading"><div><div class="eyebrow">Du premier échange aux travaux</div><h2>Un projet clair.<br>Une planification pratique.</h2></div></div><div class="process-grid"><div><div class="step-number">01 /</div><h3>Décrivez votre espace</h3><p>Indiquez votre ville et les surfaces à nettoyer. Vous pouvez transmettre des photos par courriel après votre demande.</p></div><div><div class="step-number">02 /</div><h3>Définissons les travaux</h3><p>Nous examinons les dépôts, les accès et les contraintes d’horaire. Une visite peut être nécessaire pour confirmer la portée.</p></div><div><div class="step-number">03 /</div><h3>Planifions l’intervention</h3><p>Après l’acceptation de la soumission, nous convenons du moment et des exigences du site avec l’équipe chargée des travaux.</p></div></div></div></section>'''
    provinces = ['Alberta','Colombie-Britannique','Île-du-Prince-Édouard','Manitoba','Nouveau-Brunswick','Nouvelle-Écosse','Nunavut','Ontario','Québec','Saskatchewan','Terre-Neuve-et-Labrador','Territoires du Nord-Ouest','Yukon']
    coverage = '<section class="section home-locations" id="coverage"><div class="container"><div class="eyebrow">Un point de contact au Canada</div><h2>Votre ville.<br>Votre projet en hauteur.</h2><p class="listing-intro">Pour un établissement ou plusieurs adresses, commencez par une demande en français. Indiquez votre ville et votre province ou territoire pour que nous puissions évaluer votre projet.</p><div class="industry-chips">'+''.join(f'<a href="#quote">{p} ↗</a>' for p in provinces)+'</div><p class="coverage-note">La disponibilité locale, les déplacements et les équipements sont confirmés pour chaque projet. Les travaux peuvent être réalisés avec des prestataires locaux.</p><p class="region-more"><a class="text-link" href="/locations/quebec/">Consulter les villes du Québec ↗</a></p></div></section>'
    questions = [('Quelles surfaces sont comprises?', 'La soumission précise les surfaces et les zones retenues : poutres, charpentes, plafonds, rebords, conduits extérieurs ou boîtiers de luminaires accessibles. Le nettoyage intérieur des conduits exige une portée distincte.'), ('Faut-il fournir une plateforme élévatrice?', 'Pas nécessairement. Indiquez les équipements disponibles sur place. La hauteur, les dégagements et l’état des sols déterminent les moyens d’accès appropriés.'), ('Pouvez-vous traiter les poussières dangereuses ou combustibles?', 'Ces poussières nécessitent une évaluation distincte avant de proposer une méthode. Signalez les matières connues dans votre demande. Une aspiration HEPA ne rend pas automatiquement le travail adapté à ces risques.'), ('Comment le prix est-il établi?', 'Les surfaces, la hauteur, les accès, la protection des biens et les horaires influencent la portée et le prix. Décrivez votre projet pour obtenir une soumission adaptée.'), ('Offrez-vous un entretien récurrent?', 'Vous pouvez demander une intervention ponctuelle, un entretien planifié ou des travaux à plusieurs adresses. La fréquence et la disponibilité sont évaluées pour chaque établissement.')]
    faq = '<section class="section faq" id="faq"><div class="container faq-layout"><div><div class="eyebrow">Pour préparer votre demande</div><h2>Vos questions.<br>Des réponses claires.</h2></div><div>'+''.join(f'<details><summary>{q}</summary><p>{a}</p></details>' for q,a in questions)+'</div></div></section>'
    resources = f'<section class="section planning-resources"><div class="container"><h2>Préparez votre prochain nettoyage.</h2><p><a class="text-link" href="{FR_COST_PATH}">Consulter le guide des prix ↗</a></p><p><a class="text-link" href="{FR_POST_PATH}">Planifier le nettoyage après construction ↗</a></p></div></section>'
    html = base['page']('Dépoussiérage en hauteur au Canada | HighDusting.ca', 'Dépoussiérage commercial et industriel partout au Canada. Plafonds, poutres, charpentes et conduits extérieurs. Demandez une soumission en français.', hero+services+approach+industries+process+coverage+faq+resources+quote, '/fr/')
    html = html.replace(base['header'](),header).replace(base['footer'](),footer).replace('lang="en-CA"','lang="fr-CA"')
    html = html.replace('</head>', '<script id="service-labels" type="application/json">'+json.dumps(FR_SERVICE,ensure_ascii=False)+'</script></head>')
    base['write']('fr/index.html',html)
    sitemap = ET.parse(root/'sitemap.xml')
    entry = ET.SubElement(sitemap.getroot(),f'{{{NS}}}url')
    ET.SubElement(entry,f'{{{NS}}}loc').text='https://highdusting.ca/fr/'
    sitemap.write(root/'sitemap.xml',encoding='utf-8',xml_declaration=True)
    report=json.loads((root/'data/build-report.json').read_text());report['indexable_pages']+=1;report['french_homepage']=True
    (root/'data/build-report.json').write_text(json.dumps(report,indent=2))
    # Apply one consistent switch to every page, including the missing-page screen.
    reverse={v:k for k,v in PAIRS.items()}
    files=[root/'404.html']
    files += [root/node.text.removeprefix('https://highdusting.ca/').strip('/')/'index.html' for node in sitemap.findall(f'.//{{{NS}}}loc')]
    for file in files:
        text=file.read_text();path='/' + file.parent.relative_to(root).as_posix()+'/' if file.parent!=root else '/'
        fr=bool(re.search(r'<html[^>]* lang="fr-CA"',text))
        target=reverse.get(path,'/') if fr else PAIRS.get(path,'/fr/')
        exact=path in (reverse if fr else PAIRS)
        label=('English' if exact else 'English home') if fr else ('Français' if exact else 'Accueil français')
        text=re.sub(r'<div class="container language-switch">.*?</div>','',text)
        if fr:
            text=text.replace('href="/locations/quebec/" aria-label="HighDusting.ca Québec"','href="/fr/" aria-label="HighDusting.ca — accueil"')
            text=text.replace('href="/locations/quebec/#services"','href="/fr/#services"').replace('href="/locations/quebec/#industries"','href="/fr/#industries"')
            text=text.replace('<a href="/locations/" lang="en">Canada · EN</a>','<a href="/fr/#coverage">Partout au Canada</a>')
            text=text.replace('<a href="/locations/" lang="en">Canada · English</a>','<a href="/fr/#coverage">Partout au Canada</a>')
            text=text.replace('href="/locations/quebec/#quote"','href="/fr/#quote"')
            if path=='/fr/':text=text.replace('href="/locations/quebec/">Villes du Québec</a>','href="/fr/#approach">Notre approche</a>',1)
        switch=f'<a class="site-language-switch" href="{target}" lang="{"en" if fr else "fr"}" hreflang="{"en-CA" if fr else "fr-CA"}" aria-label="{label}">{"EN" if fr else "FR"}</a>'
        # Insert after the phone link so existing responsive phone rules still work.
        text=re.sub(r'(<div class="nav-actions"><a href="tel:[^"]+">.*?</a>)',lambda m:m.group(1)+switch,text,count=1)
        file.write_text(text)
