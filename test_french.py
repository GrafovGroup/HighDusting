"""French entry point, locale metadata, navigation, and quote contracts."""
import json
import re
import unittest
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit
from french_home import PAIRS

ROOT=Path(__file__).parent
class Links(HTMLParser):
    def __init__(self, text):
        super().__init__();self.links=[];self.feed(text)
    def handle_starttag(self,tag,attrs):
        if tag=='a':self.links.append(dict(attrs))

class FrenchJourney(unittest.TestCase):
    def test_one_visible_language_switch_on_every_page(self):
        reverse={v:k for k,v in PAIRS.items()}
        for file in ROOT.rglob('*.html'):
            if 'dist' in file.parts:continue
            html=file.read_text();fr='<html lang="fr-CA"' in html
            path='/' if file.parent==ROOT else '/'+file.parent.relative_to(ROOT).as_posix()+'/'
            switches=[a for a in Links(html).links if a.get('class')=='site-language-switch']
            self.assertEqual(len(switches),1,str(file))
            target=(reverse.get(path,'/') if fr else PAIRS.get(path,'/fr/'))
            self.assertEqual(switches[0]['href'],target,str(file))
            self.assertTrue((ROOT/target.strip('/')/'index.html').exists())
            if path not in (reverse if fr else PAIRS):self.assertIn('home' if fr else 'Accueil',switches[0]['aria-label'])
    def test_reciprocal_home_and_privacy_metadata(self):
        for en,fr in PAIRS.items():
            for route in (en,fr):
                html=(ROOT/route.strip('/')/'index.html').read_text()
                for lang,target in [('en-CA',en),('fr-CA',fr)]:
                    self.assertIn(f'hreflang="{lang}" href="https://highdusting.ca{target}"',html)
    def test_french_home_has_complete_quote_journey(self):
        html=(ROOT/'fr/index.html').read_text()
        for section in ['services','industries','coverage','approach','faq','quote']:
            self.assertIn(f'id="{section}"',html)
        self.assertIn('data-language="fr"',html)
        self.assertIn('name="language" value="fr-CA"',html)
        self.assertIn('action="https://formspree.io/f/mqpkndrp"',html)
        self.assertNotIn('type="file"',html)
        self.assertIn('href="/fr/confidentialite/"',html)
        links=Links(html).links
        for a in links:
            target=a.get('href','')
            if not target.startswith('/') or a.get('class')=='site-language-switch':continue
            path=urlsplit(target).path
            dest=(ROOT/path.strip('/')/'index.html').read_text()
            self.assertIn('<html lang="fr-CA"',dest,target)
    def test_french_brand_returns_to_french_home(self):
        for file in ROOT.rglob('*.html'):
            if 'dist' in file.parts:continue
            html=file.read_text()
            if '<html lang="fr-CA"' not in html:continue
            brands=[a for a in Links(html).links if a.get('class')=='brand']
            self.assertTrue(brands)
            self.assertTrue(all(a['href']=='/fr/' for a in brands),str(file))

if __name__=='__main__':unittest.main()
