"""Search metadata checks against the actual generated HTML and route registry."""
import json
import re
import unittest
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

from seo import Metadata, SITE, SITEMAP_NS, IMAGE_NS
from service_answers import ANSWERS

ROOT = Path(__file__).parent


class HeadAndBreadcrumb(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.meta = {}
        self.canonicals = []
        self.crumb_text = ''
        self.in_breadcrumb = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'meta':
            self.meta[attrs.get('name', attrs.get('property'))] = attrs.get('content')
        elif tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonicals.append(attrs['href'])
        elif tag == 'nav' and 'breadcrumb' in attrs.get('class', '').split():
            self.in_breadcrumb = True

    def handle_endtag(self, tag):
        if tag == 'nav':
            self.in_breadcrumb = False

    def handle_data(self, text):
        if self.in_breadcrumb:
            self.crumb_text += text


class SEOTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.entries = ET.parse(ROOT / 'sitemap.xml').findall(f'{{{SITEMAP_NS}}}url')
        cls.pages = {}
        for entry in cls.entries:
            url = entry.find(f'{{{SITEMAP_NS}}}loc').text
            file = ROOT / urlsplit(url).path.lstrip('/') / 'index.html'
            html = file.read_text()
            scripts = re.findall(r'<script type="application/ld\+json">(.*?)</script>', html, re.S)
            cls.pages[url] = (html, Metadata(html), HeadAndBreadcrumb(html), scripts)

    def test_unique_metadata_and_indexable_canonicals(self):
        self.assertEqual(len(self.pages), 100)
        titles = []
        descriptions = []
        for url, (_, doc, head, _) in self.pages.items():
            self.assertEqual(head.canonicals, [url])
            self.assertEqual(head.meta['og:url'], url)
            self.assertEqual(head.meta['og:locale'], doc.language.replace('-', '_'))
            self.assertIn('max-image-preview:large', head.meta['robots'])
            self.assertTrue(head.meta['robots'].startswith('index,follow'))
            titles.append(doc.title)
            descriptions.append(doc.description)
        self.assertEqual(len(set(titles)), len(titles))
        self.assertEqual(len(set(descriptions)), len(descriptions))

    def test_graph_links_language_and_visible_breadcrumbs(self):
        services = 0
        for url, (_, doc, head, scripts) in self.pages.items():
            self.assertEqual(len(scripts), 1, url)
            graph = json.loads(scripts[0])['@graph']
            nodes = {node['@id']: node for node in graph}
            self.assertEqual(len(nodes), len(graph), url)
            page = nodes[url + '#webpage']
            self.assertEqual(page['description'], doc.description)
            self.assertEqual(page['inLanguage'], doc.language)
            self.assertEqual(nodes[SITE + '/#organization']['email'], 'info@highdusting.ca')
            self.assertEqual(nodes[SITE + '/#organization']['telephone'], '+18884513878')

            def check_refs(value):
                if isinstance(value, dict):
                    if set(value) == {'@id'}:
                        self.assertIn(value['@id'], nodes, url)
                    for child in value.values():
                        check_refs(child)
                elif isinstance(value, list):
                    for child in value:
                        check_refs(child)
            check_refs(graph)
            if url != SITE + '/':
                crumbs = nodes[url + '#breadcrumb']['itemListElement']
                self.assertEqual([c['position'] for c in crumbs], list(range(1, len(crumbs) + 1)))
                self.assertEqual(head.crumb_text, ' / '.join(c['name'] for c in crumbs))
                self.assertEqual(crumbs[-1]['item'], url)
                for crumb in crumbs:
                    self.assertIn(crumb['item'], self.pages)
            for node in graph:
                self.assertNotIn(node['@type'], ('LocalBusiness', 'Review', 'AggregateRating', 'Offer'))
                if node['@type'] == 'Service':
                    services += 1
                    expected = 'City' if '/locations/' in url else 'Country'
                    self.assertEqual(node['areaServed']['@type'], expected)
        self.assertEqual(services, 73)

    def test_sitemap_images_match_page_images_and_existing_files(self):
        for entry in self.entries:
            url = entry.find(f'{{{SITEMAP_NS}}}loc').text
            _, doc, head, scripts = self.pages[url]
            images = [image.find(f'{{{IMAGE_NS}}}loc').text for image in entry.findall(f'{{{IMAGE_NS}}}image')]
            self.assertEqual(set(images), {SITE + image['src'] for image in doc.images})
            for image in images:
                self.assertTrue((ROOT / urlsplit(image).path.lstrip('/')).is_file())
            if images:
                graph = json.loads(scripts[0])['@graph']
                primary = next(n for n in graph if n['@type'] == 'ImageObject')
                self.assertIn(primary['contentUrl'], images)
                self.assertEqual(head.meta['og:image'], primary['contentUrl'])
                self.assertEqual(head.meta['og:image:alt'], primary['caption'])

    def test_service_answers_are_visible_and_complete(self):
        urls = {url for url in self.pages if url.startswith(SITE + '/services/') and url != SITE + '/services/'}
        self.assertEqual(urls, {SITE + '/services/' + slug + '/' for slug in ANSWERS})
        for slug, (question, answer) in ANSWERS.items():
            html = self.pages[SITE + '/services/' + slug + '/'][0]
            from html import unescape
            self.assertIn(question, unescape(html))
            self.assertIn(answer, unescape(html))
            self.assertIn('id="service-questions"', html)
            self.assertIn('What affects the cost of this service?', html)

    def test_missing_page_is_not_the_homepage(self):
        html = (ROOT / '404.html').read_text()
        head = HeadAndBreadcrumb(html)
        self.assertEqual(head.canonicals, [])
        self.assertEqual(head.meta['robots'], 'noindex,follow')
        self.assertNotIn('application/ld+json', html)


if __name__ == '__main__':
    unittest.main()
