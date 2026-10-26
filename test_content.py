"""Build invariants: distinct required assets, crawlable links, locale, geography, forms."""
import hashlib,json,unittest
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit,unquote
ROOT=Path(__file__).parent
class Document(HTMLParser):
 def __init__(self,html):
  super().__init__();self.ids=set();self.urls=[];self.fragments=[];self.heroes=[];self.forms=0;self.quote_attrs=[];self.lang='';self.headings=0;self.feed(html)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if 'id' in a:self.ids.add(a['id'])
  for k in ['src','href']:
   if a.get(k,'').startswith('/'):self.urls.append(a[k])
   if a.get(k,'').startswith('#'):self.fragments.append(a[k][1:])
  if tag=='html':self.lang=a.get('lang')
  if tag=='img' and 'hero-image' in a.get('class',''):self.heroes.append(a['src'])
  if tag=='form' and a.get('id')=='quote-form':self.forms+=1;self.quote_attrs.append(a)
  if tag=='h1':self.headings+=1
class ContentTests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.pages={p:Document(p.read_text()) for p in ROOT.rglob('*.html') if not {'.data','dist'}.intersection(p.parts)}
 def test_all_local_assets_routes_and_fragments(self):
  for path,doc in self.pages.items():
   self.assertEqual(doc.headings,1,str(path))
   for fragment in doc.fragments:self.assertIn(fragment,doc.ids,f'{path}: #{fragment}')
   for value in doc.urls:
    url=urlsplit(value);target=ROOT/unquote(url.path).lstrip('/')
    if target.is_dir():target=target/'index.html'
    self.assertTrue(target.is_file(),f'{path}: {value}')
    if url.fragment and target.suffix=='.html':self.assertIn(url.fragment,self.pages[target].ids,f'{path}: {value}')
 def test_distinct_city_hero_images(self):
  cities=json.loads((ROOT/'data/cities.json').read_text());images=[]
  provinces={p['code']:p for p in json.loads((ROOT/'data/provinces.json').read_text())}
  for city in cities:
   path=ROOT/'locations'/provinces[city['province']]['slug']/city['slug']/'index.html';doc=self.pages[path];self.assertEqual(doc.forms,1);self.assertEqual(doc.lang,'fr-CA' if city['province']=='QC' else 'en-CA');self.assertEqual(len(doc.heroes),1)
   image=ROOT/doc.heroes[0].lstrip('/');images.append(hashlib.sha256(image.read_bytes()).hexdigest());self.assertIn(city['brief'],path.read_text())
  self.assertEqual(len(cities),52);self.assertEqual(len(images),len(set(images)))
 def test_nationwide_directory(self):
  source=json.loads((ROOT/'data/municipalities.json').read_text());self.assertEqual(len(source),5161);self.assertEqual(len({x['province'] for x in source}),13)
  published=json.loads((ROOT/'assets/locations.json').read_text());self.assertEqual(sum(x['featured'] for x in published),52);self.assertEqual(len({x['id'] for x in published}),len(published))
 def test_unique_service_province_industry_heroes(self):
  for directory,count in [('services',20),('industries',6)]:
   pages=list((ROOT/directory).glob('*/index.html'));self.assertEqual(len(pages),count);digests=[hashlib.sha256((ROOT/self.pages[p].heroes[0].lstrip('/')).read_bytes()).hexdigest() for p in pages];self.assertEqual(len(set(digests)),count)
  pages=list((ROOT/'locations').glob('*/index.html'));self.assertEqual(len(pages),13);self.assertEqual(len({self.pages[p].heroes[0] for p in pages}),13)
 def test_no_empty_published_images(self):
  for path,doc in self.pages.items():
   for url in doc.urls:
    if urlsplit(url).path.endswith('.webp'):self.assertGreater((ROOT/urlsplit(url).path.lstrip('/')).stat().st_size,1000)
 def test_main_photos_are_unique_across_pages(self):
  photos={}
  for path,doc in self.pages.items():
   for source in doc.heroes:
    digest=hashlib.sha256((ROOT/source.lstrip('/')).read_bytes()).hexdigest()
    self.assertNotIn(digest,photos,f'Main photo repeated on {path} and {photos.get(digest)}')
    photos[digest]=path
 def test_quote_forms_use_formspree(self):
  total=0
  for path,doc in self.pages.items():
   for attrs in doc.quote_attrs:
    total+=1
    self.assertEqual(attrs['action'],'https://formspree.io/f/mqpkndrp',str(path))
    self.assertEqual(attrs['method'].upper(),'POST')
    self.assertEqual(attrs['enctype'],'multipart/form-data')
    html=path.read_text()
    self.assertIn('name="_gotcha"',html)
    self.assertNotIn('type="file"',html)
    self.assertIn('mailto:info@highdusting.ca?subject=HighDusting.ca%20project%20photos',html)
    self.assertLess(html.index('src="/formspree.js"'),html.index('src="/app.js"'))
  self.assertEqual(total,98)
  app=(ROOT/'app.js').read_text()
  self.assertNotIn('/api/quotes',app)
  self.assertNotIn('result.reference',app)
if __name__=='__main__':unittest.main()
