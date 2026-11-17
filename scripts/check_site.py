"""Smoke test the actual Nginx deployment, not a Python preview server.

Usage: python3 scripts/check_site.py [base_url]
Only Python's standard library is required.
"""
from html.parser import HTMLParser
import json
import sys
import time
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import build_opener, HTTPRedirectHandler, Request
import xml.etree.ElementTree as ET

BASE = (sys.argv[1] if len(sys.argv) > 1 else 'https://metronomeo.com').rstrip('/')
CANONICAL = 'https://metronomeo.com'

class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, *args):
        return None

client = build_opener(NoRedirect)

def get(path, expected=200, headers=None):
    try:
        response = client.open(Request(BASE + path, headers=headers or {}), timeout=15)
    except HTTPError as error:
        response = error
    assert response.code == expected, f'{path}: expected {expected}, got {response.code}; Location={response.headers.get("Location")}'
    return response.headers, response.read()

class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.canonical = None
        self.h1s = 0
        self.media = set()
        self.jsonld = []
        self.buffer = None
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'h1': self.h1s += 1
        if tag == 'link' and attrs.get('rel') == 'canonical': self.canonical = attrs['href']
        if tag in ('img', 'source') and attrs.get('src'): self.media.add(attrs['src'])
        if tag == 'script' and attrs.get('type') == 'application/ld+json': self.buffer = ''
    def handle_data(self, text):
        if self.buffer is not None: self.buffer += text
    def handle_endtag(self, tag):
        if tag == 'script' and self.buffer is not None:
            self.jsonld.append(json.loads(self.buffer))
            self.buffer = None

for attempt in range(30):
    try:
        get('/health')
        break
    except (URLError, OSError):
        if attempt == 29: raise
        time.sleep(.5)

_, sitemap = get('/sitemap.xml')
paths = [urlparse(element.text).path for element in ET.fromstring(sitemap).iter() if element.tag.endswith('loc')]
assert len(paths) == 11, f'Unexpected sitemap size: {len(paths)}'
media = set()
for path in paths:
    _, body = get(path)
    page = Page()
    page.feed(body.decode())
    assert page.h1s == 1, path
    assert page.canonical == CANONICAL + path, (path, page.canonical)
    for src in page.media:
        media.add(urlparse(urljoin(BASE + path, src)).path)
for path in sorted(media):
    get(path)
for path, destination in [('/guides', '/guides/'), ('/guides?test=1', '/guides/?test=1')]:
    headers, _ = get(path, 301)
    assert headers['Location'] == destination, (path, headers['Location'])
for path, destination in [('/index.html', '/'), ('/guides/index.html', '/guides/')]:
    _, body = get(path)
    page = Page(); page.feed(body.decode())
    assert page.canonical == CANONICAL + destination
get('/not-a-real-page-smoke-check', 404)
get('/assets/not-a-real-image-smoke-check.webp', 404)
_, body = get('/assets/audio/ratio-3-2.mp3', 206, {'Range': 'bytes=0-2047'})
assert len(body) == 2048
print(f'PASS: {len(paths)} pages, {len(media)} media files, canonical links, redirects, 404s and audio range requests.')
