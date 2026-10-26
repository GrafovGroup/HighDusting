"""New service/guide routes and the city-to-enquiry journey."""
import json
import re
import unittest
from html import unescape
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import parse_qs, urlsplit
from local_growth import CITY_HANDOVERS, POST_PATH, FR_POST_PATH, COST_PATH, FR_COST_PATH, TRANSLATIONS

ROOT = Path(__file__).parent
SITE = 'https://highdusting.ca'


class Links(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.links = []
        self.alternates = {}
        self.inputs = {}
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'a':
            self.links.append(attrs.get('href', ''))
        if tag == 'link' and attrs.get('rel') == 'alternate':
            self.alternates[attrs['hreflang']] = attrs['href']
        if tag == 'input':
            self.inputs[attrs.get('name')] = attrs


def read(path):
    return (ROOT / path.lstrip('/') / 'index.html').read_text()


class GrowthTests(unittest.TestCase):
    def test_niche_services_and_local_enquiry_links(self):
        from niche_services import NICHE_SERVICES, FOCUS_SERVICES, FR_NICHE
        for slug, title, *_ in NICHE_SERVICES:
            route = '/services/' + slug + '/'
            html = read(route)
            self.assertIn(route, Links(read('/services/')).links)
            self.assertEqual(Links(html).inputs['selected_service']['value'], slug)
            image = '/assets/services/' + slug + '.webp'
            placements = sum(p.read_text().count('src="' + image + '"') for p in ROOT.rglob('*.html') if not {'.data', 'dist'}.intersection(p.parts))
            self.assertEqual(placements, 1, slug)
            self.assertIn('Scope boundaries', html)
        cities = json.loads((ROOT / 'data/cities.json').read_text())
        provinces = {p['code']: p['slug'] for p in json.loads((ROOT / 'data/provinces.json').read_text())}
        for city in cities:
            route = f'/locations/{provinces[city["province"]]}/{city["slug"]}/'
            html = read(route)
            for slug in FOCUS_SERVICES.get(city['focus'], []):
                self.assertIn('id="specialist-surfaces"', html)
                if city['province'] == 'QC':
                    self.assertIn('data-service-choice="' + slug + '"', html)
                    self.assertIn(FR_NICHE[slug], html)
                else:
                    target = '/services/' + slug + '/'
                    queries = [parse_qs(urlsplit(link).query) for link in Links(html).links if urlsplit(link).path == target]
                    self.assertIn({'city': [city['name'] + ', ' + city['province']], 'source': [route]}, queries)

    def test_all_city_briefs_and_contextual_links(self):
        cities = json.loads((ROOT / 'data/cities.json').read_text())
        provinces = {p['code']: p['slug'] for p in json.loads((ROOT / 'data/provinces.json').read_text())}
        self.assertEqual(set(CITY_HANDOVERS), {c['slug'] for c in cities})
        self.assertEqual(len(set(CITY_HANDOVERS.values())), len(cities))
        for city in cities:
            route = f'/locations/{provinces[city["province"]]}/{city["slug"]}/'
            html = read(route)
            self.assertIn(CITY_HANDOVERS[city['slug']], unescape(html))
            self.assertIn('id="post-construction"', html)
            self.assertIn('id="cost"', html)
            expected = (FR_POST_PATH, FR_COST_PATH) if city['province'] == 'QC' else (POST_PATH, COST_PATH)
            links = Links(html).links
            for target in expected:
                matches = [parse_qs(urlsplit(link).query) for link in links if urlsplit(link).path == target]
                self.assertTrue(matches, route + ' -> ' + target)
                self.assertIn({'city': [city['name'] + ', ' + city['province']], 'source': [route]}, matches)

    def test_translation_pairs_are_reciprocal_and_reachable(self):
        for english, french in TRANSLATIONS.items():
            expected = {'en-CA': SITE + english, 'fr-CA': SITE + french, 'x-default': SITE + english}
            for route, other, language in ((english, french, 'en-CA'), (french, english, 'fr-CA')):
                html = read(route)
                doc = Links(html)
                self.assertEqual(doc.alternates, expected)
                self.assertIn(other, doc.links)
                self.assertEqual(doc.inputs['language']['value'], language)
                self.assertIn(f'lang="{language}"', html)

    def test_guides_and_services_describe_different_entities(self):
        for path, expected_type in ((POST_PATH, 'Service'), (FR_POST_PATH, 'Service'), (COST_PATH, 'Article'), (FR_COST_PATH, 'Article')):
            html = read(path)
            graph = json.loads(re.search(r'<script type="application/ld\+json">(.*?)</script>', html).group(1))['@graph']
            nodes = {item['@id']: item for item in graph}
            main = nodes[SITE + path + '#webpage']['mainEntity']['@id']
            self.assertEqual(nodes[main]['@type'], expected_type)
            if expected_type == 'Article':
                self.assertIn('<table class="cost-table">', html)
            else:
                self.assertEqual(Links(html).inputs['selected_service']['value'], 'post-construction-high-dusting')

    def test_new_pages_have_incoming_navigation(self):
        self.assertIn(POST_PATH, Links(read('/')).links)
        self.assertIn(COST_PATH, Links(read('/')).links)
        for route in ('/services/', POST_PATH):
            self.assertIn(COST_PATH, Links(read(route)).links)


if __name__ == '__main__':
    unittest.main()
