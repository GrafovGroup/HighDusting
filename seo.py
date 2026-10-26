"""Content-derived search metadata and image discovery for the static build.

The sitemap is the published route registry. Never infer business locations,
reviews, prices, credentials, or completed jobs from location names or artwork.
"""
import json
import re
from html import escape
from html.parser import HTMLParser
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET
from local_growth import FR_POST_PATH, COST_PATH, FR_COST_PATH
from french_home import PAIRS as TRANSLATIONS

SITE = 'https://highdusting.ca'
SITEMAP_NS = 'http://www.sitemaps.org/schemas/sitemap/0.9'
IMAGE_NS = 'http://www.google.com/schemas/sitemap-image/1.1'


class Metadata(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.title = ''
        self.description = ''
        self.language = 'en-CA'
        self.images = []
        self.in_title = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'title':
            self.in_title = True
        elif tag == 'html':
            self.language = attrs.get('lang', 'en-CA')
        elif tag == 'meta' and attrs.get('name') == 'description':
            self.description = attrs['content']
        elif tag == 'img' and attrs.get('src', '').startswith('/assets/') and attrs.get('class') != 'brand-logo':
            if not any(image['src'] == attrs['src'] for image in self.images):
                self.images.append(attrs)

    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title += data


def breadcrumbs(path, pages, cities, provinces, language):
    fr = language == 'fr-CA'
    parts = path.strip('/').split('/')
    trail = [('/fr/' if fr else '/', 'Accueil' if fr else 'Home')]
    for length in range(1, len(parts) + 1):
        route = '/' + '/'.join(parts[:length]) + '/'
        if route not in pages or route == trail[0][0]:
            continue
        label = pages[route].title.split(' | ')[0]
        if route == '/locations/':
            label = 'Canada'
        elif route == '/services/':
            label = 'Services'
        elif route == '/industries/':
            label = 'Industries'
        elif route in cities:
            label = cities[route]['name']
        elif route in provinces:
            label = 'Québec' if fr else provinces[route]['name']
        trail.append((route, label))
    return trail


def build(root):
    source = ET.parse(root / 'sitemap.xml')
    paths = [urlsplit(node.text).path for node in source.findall(f'.//{{{SITEMAP_NS}}}loc')]
    files = {path: root / path.lstrip('/') / 'index.html' for path in paths}
    documents = {path: file.read_text() for path, file in files.items()}
    pages = {path: Metadata(html) for path, html in documents.items()}
    province_data = json.loads((root / 'data/provinces.json').read_text())
    province_by_code = {p['code']: p for p in province_data}
    provinces = {f'/locations/{p["slug"]}/': p for p in province_data}
    cities = {
        f'/locations/{province_by_code[c["province"]]["slug"]}/{c["slug"]}/': c
        for c in json.loads((root / 'data/cities.json').read_text())
    }
    organization = {
        '@type': 'Organization', '@id': SITE + '/#organization',
        'name': 'HighDusting.ca', 'url': SITE + '/',
        'telephone': '+18884513878', 'email': 'info@highdusting.ca',
    }
    website = {
        '@type': 'WebSite', '@id': SITE + '/#website',
        'url': SITE + '/', 'name': 'HighDusting.ca',
        'publisher': {'@id': organization['@id']},
        'inLanguage': ['en-CA', 'fr-CA'],
    }
    ET.register_namespace('', SITEMAP_NS)
    ET.register_namespace('image', IMAGE_NS)
    sitemap = ET.Element(f'{{{SITEMAP_NS}}}urlset')
    service_count = 0
    for path, doc in pages.items():
        url = SITE + path
        html = documents[path]
        collection = path in provinces or path in ('/locations/', '/services/', '/industries/')
        webpage = {
            '@type': 'CollectionPage' if collection else 'WebPage',
            '@id': url + '#webpage', 'url': url, 'name': doc.title,
            'description': doc.description, 'inLanguage': doc.language,
            'isPartOf': {'@id': website['@id']},
            'publisher': {'@id': organization['@id']},
        }
        graph = [organization, website, webpage]
        if doc.images:
            primary = next((img for img in doc.images if 'hero-image' in img.get('class', '')), doc.images[0])
            image = {'@type': 'ImageObject', '@id': url + '#primaryimage',
                     'contentUrl': SITE + primary['src'], 'caption': primary.get('alt', '')}
            graph.append(image)
            webpage['primaryImageOfPage'] = {'@id': image['@id']}
        if path != '/':
            trail = breadcrumbs(path, pages, cities, provinces, doc.language)
            breadcrumb_id = url + '#breadcrumb'
            graph.append({'@type': 'BreadcrumbList', '@id': breadcrumb_id,
                          'itemListElement': [
                              {'@type': 'ListItem', 'position': i, 'name': label, 'item': SITE + route}
                              for i, (route, label) in enumerate(trail, 1)]})
            webpage['breadcrumb'] = {'@id': breadcrumb_id}
            links = [f'<a href="{route}">{escape(label)}</a>' for route, label in trail[:-1]]
            links.append(f'<span aria-current="page">{escape(trail[-1][1])}</span>')
            label = 'Fil d’Ariane' if doc.language == 'fr-CA' else 'Breadcrumb'
            inner = ' / '.join(links)
            if '<div class="breadcrumb">' in html:
                html = re.sub(r'<div class="breadcrumb">.*?</div>',
                              lambda _: f'<nav class="breadcrumb" aria-label="{label}">{inner}</nav>', html, count=1)
            else:
                html = html.replace('<main id="main">', f'<main id="main"><nav class="container breadcrumb page-breadcrumb" aria-label="{label}">{inner}</nav>', 1)
        is_service = (path.startswith('/services/') and path != '/services/') or path == FR_POST_PATH
        if is_service or path in cities:
            service_count += 1
            service = {
                '@type': 'Service', '@id': url + '#service',
                'name': doc.title.split(' | ')[0], 'url': url,
                'description': doc.description,
                'provider': {'@id': organization['@id']},
                'mainEntityOfPage': {'@id': webpage['@id']},
            }
            # Area served describes the enquiry scope; it is not a branch address.
            if path in cities:
                city = cities[path]
                service['areaServed'] = {
                    '@type': 'City', 'name': city['name'],
                    'containedInPlace': {'@type': 'AdministrativeArea', 'name': province_by_code[city['province']]['name'],
                                         'containedInPlace': {'@type': 'Country', 'name': 'Canada'}}}
            else:
                service['areaServed'] = {'@type': 'Country', 'name': 'Canada'}
            webpage['mainEntity'] = {'@id': service['@id']}
            graph.append(service)
        if path in (COST_PATH, FR_COST_PATH):
            article = {
                '@type': 'Article', '@id': url + '#article',
                'headline': doc.title.split(' | ')[0],
                'description': doc.description, 'inLanguage': doc.language,
                'author': {'@id': organization['@id']},
                'publisher': {'@id': organization['@id']},
                'mainEntityOfPage': {'@id': webpage['@id']},
            }
            if doc.images:
                article['image'] = {'@id': url + '#primaryimage'}
            graph.append(article)
            webpage['mainEntity'] = {'@id': article['@id']}
        html = re.sub(r'<script type="application/ld\+json">.*?</script>', '', html, flags=re.S)
        structured = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False).replace('<', '\\u003c')
        head = f'<script type="application/ld+json">{structured}</script>'
        for english, french in TRANSLATIONS.items():
            if path in (english, french):
                head += f'<link rel="alternate" hreflang="en-CA" href="{SITE + english}">'
                head += f'<link rel="alternate" hreflang="fr-CA" href="{SITE + french}">'
                head += f'<link rel="alternate" hreflang="x-default" href="{SITE + english}">'
        if path == '/':
            head += '<meta name="google-site-verification" content="KRGBQ-QRrORP7V4Wo4DoazzzY2em3M3B1S0jcEyLmCc">'
            head += '<meta name="msvalidate.01" content="8540AF3FE8C8197267E84BBE602115F7">'
        head += '<meta name="robots" content="index,follow,max-image-preview:large">'
        head += f'<meta property="og:url" content="{url}"><meta property="og:site_name" content="HighDusting.ca">'
        if 'property="og:locale"' not in html:
            head += f'<meta property="og:locale" content="{doc.language.replace("-", "_")}">'
        head += '<meta name="twitter:card" content="summary_large_image">'
        if doc.images:
            # Use the same primary image for sharing and page identity.
            html = re.sub(r'<meta property="og:image" content="[^"]*">',
                          lambda _: f'<meta property="og:image" content="{SITE + primary["src"]}">', html)
            head += f'<meta property="og:image:alt" content="{escape(primary.get("alt", ""), quote=True)}">'
        html = html.replace('</head>', head + '</head>', 1)
        files[path].write_text(html)
        entry = ET.SubElement(sitemap, f'{{{SITEMAP_NS}}}url')
        ET.SubElement(entry, f'{{{SITEMAP_NS}}}loc').text = url
        for img in doc.images:
            node = ET.SubElement(entry, f'{{{IMAGE_NS}}}image')
            ET.SubElement(node, f'{{{IMAGE_NS}}}loc').text = SITE + img['src']
    ET.ElementTree(sitemap).write(root / 'sitemap.xml', encoding='utf-8', xml_declaration=True)
    # A missing page must not identify itself as the canonical homepage.
    missing = (root / '404.html').read_text()
    missing = re.sub(r'<link rel="canonical"[^>]*>', '', missing)
    missing = re.sub(r'<script type="application/ld\+json">.*?</script>', '', missing, flags=re.S)
    missing = missing.replace('</head>', '<meta name="robots" content="noindex,follow"></head>')
    (root / '404.html').write_text(missing)
    print(f'SEO: {len(pages)} linked page graphs; {service_count} service entities; image sitemap generated.')
