"""Stage only the website's public files for static Sites hosting."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import shutil
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parent.parent
OUTPUT = ROOT / 'dist'
NS = '{http://www.sitemaps.org/schemas/sitemap/0.9}'


class Assets(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.paths = set()
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        value = attrs.get('src') if tag in ('img', 'script') else attrs.get('href') if tag == 'link' else None
        if value and value.startswith('/') and not value.startswith('//'):
            self.paths.add(unquote(urlsplit(value).path).lstrip('/'))


paths = {'404.html', 'robots.txt', 'sitemap.xml', 'assets/locations.json', 'styles.css', 'app.js', 'formspree.js', 'favicon.svg'}
for node in ET.parse(ROOT / 'sitemap.xml').findall(f'.//{NS}loc'):
    route = urlsplit(node.text).path.lstrip('/')
    paths.add(route + 'index.html')
for name in list(paths):
    if name.endswith('.html'):
        paths.update(Assets((ROOT / name).read_text()).paths)
for name in paths:
    source = ROOT / name
    assert source.is_file() and not source.is_symlink(), name
    assert source.resolve().is_relative_to(ROOT), name
    assert not any(part.startswith('.') for part in Path(name).parts), name
    destination = OUTPUT / name
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, destination)
actual = {str(path.relative_to(OUTPUT)) for path in OUTPUT.rglob('*') if path.is_file()}
assert actual == paths, f'Unexpected files in publish directory: {actual - paths}'
print(f'Staged {len(paths)} public files ({sum((OUTPUT / name).stat().st_size for name in paths):,} bytes).')
