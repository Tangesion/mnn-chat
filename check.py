#!/usr/bin/env python3
"""Check project-path links and anchors in the generated GitHub Pages site."""
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import json

ROOT = Path(__file__).resolve().parent
DOCS = ROOT / 'docs'
PREFIX = '/mnn-chat'
links = 0

class Checker(HTMLParser):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def handle_starttag(self, tag, attrs):
        global links
        attrs = dict(attrs)
        assert tag not in ['script', 'form', 'iframe'], (self.page, tag)
        for key in ['href', 'src']:
            url = attrs.get(key, '')
            parsed = urlsplit(url)
            if url.startswith('/'):
                assert parsed.path.startswith(PREFIX + '/'), (self.page, url)
                target = DOCS / parsed.path.removeprefix(PREFIX + '/')
                if target.is_dir():
                    target = target / 'index.html'
            elif url.startswith('#'):
                target = self.page
            else:
                continue
            assert target.is_file(), (self.page, url)
            if parsed.fragment:
                assert f'id="{parsed.fragment}"' in target.read_text(), (self.page, url)
            links += 1

pages = list(DOCS.rglob('*.html'))
assert len(pages) == 13, len(pages)
for page in pages:
    text = page.read_text()
    assert 'chatgpt.site' not in text and '更新于' not in text, page
    Checker(page).feed(text)
    if page.name != '404.html':
        assert 'https://tangesion.github.io/mnn-chat/' in text, page
        assert 'tangesion@163.com' in text, page
assert (DOCS / '.nojekyll').is_file()
for language in ['en', 'zh-Hans']:
    data = json.loads((ROOT / f'content/LegalDocuments-{language}.json').read_text())
    assert set(data) == {'privacy', 'terms', 'disclaimer', 'services'}
print(f'PASS: {len(pages)} HTML files, {links} internal links and anchors, bilingual content and project paths')
