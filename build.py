#!/usr/bin/env python3
"""Build the public help pages from the app's approved legal copy."""
from pathlib import Path
import html
import json
import re
import shutil

ROOT = Path(__file__).resolve().parent
OUT = ROOT / 'docs'
ORIGIN = 'https://tangesion.github.io'
BASE_PATH = '/mnn-chat'
EMAIL = 'tangesion@163.com'
LABELS = json.loads((ROOT / 'content/labels.json').read_text())
ROUTES = {'privacy': 'privacy', 'terms': 'terms', 'disclaimer': 'ai', 'services': 'services'}

def rich(text):
    escaped = html.escape(text)
    escaped = re.sub(r'\[([^\]]+)\]\((https://[^\s)]+)\)', r'<a href="\2" rel="noreferrer">\1</a>', escaped)
    return re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', escaped)

def build_language(lang):
    zh = lang == 'zh-Hans'
    prefix = '' if zh else '/en'
    label = lambda key: LABELS[key][lang]
    doc = json.loads((ROOT / f'content/LegalDocuments-{lang}.json').read_text())
    def href(route=''):
        return BASE_PATH + prefix + '/' + (route + '/' if route else '')
    def page(route, title, body, description):
        alternate = BASE_PATH + ('/en' if zh else '') + '/' + (route + '/' if route else '')
        nav = [('support', '帮助与反馈' if zh else 'Support'), ('privacy', label('legal.privacy.title'))]
        nav_html = ''.join(f'<a href="{href(r)}" aria-label="{t}"'+(' aria-current="page"' if route == r else '')+f'>{t}</a>' for r,t in nav)
        footer_links = ''.join(f'<a href="{href(r)}">{label("legal."+k+".title")}</a>' for k,r in ROUTES.items())
        content = f'''<!doctype html>
<html lang="{lang}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{html.escape(title)} · MNN Chat</title><meta name="description" content="{html.escape(description, quote=True)}">
<meta name="theme-color" content="#f6f8fc"><meta name="referrer" content="no-referrer">
<link rel="canonical" href="{ORIGIN}{href(route)}"><link rel="stylesheet" href="{BASE_PATH}/style.css"><link rel="icon" href="{BASE_PATH}/favicon.svg" type="image/svg+xml"></head>
<body><a class="skip" href="#main">{'跳到正文' if zh else 'Skip to content'}</a>
<header><div class="bar"><a class="brand" href="{href()}"><span class="mark" aria-hidden="true">M</span>MNN Chat</a>
<nav aria-label="{'主导航' if zh else 'Main navigation'}">{nav_html}<a class="language" href="{alternate}" lang="{'en' if zh else 'zh-Hans'}">{'English' if zh else '中文'}</a></nav></div></header>
<main id="main">{body}</main>
<footer><div class="footer-inner"><div><a class="brand" href="{href()}">MNN Chat</a><p>{'本地对话，自在使用。' if zh else 'Conversations on your device.'}</p></div><div class="footer-links">{footer_links}<a href="mailto:{EMAIL}">{EMAIL}</a></div></div></footer>
</body></html>'''
        dest = OUT / prefix.lstrip('/') / route
        dest.mkdir(parents=True, exist_ok=True)
        (dest / 'index.html').write_text(content)

    intro = '在您的设备上，与 AI 对话。' if zh else 'Talk with AI on your device.'
    detail = ('模型、使用方法，以及您想了解的隐私说明，都可以在这里找到。' if zh else 'Find help with models and conversations, and learn how MNN Chat handles your information.')
    cards = ''.join(f'<a class="card" href="{href(r)}"><span class="card-number">0{i}</span><h2>{t}</h2><p>{d}</p><span class="arrow" aria-hidden="true">↗</span></a>' for i,r,t,d in [
        (1,'support','使用帮助' if zh else 'Get help','从模型下载到本地数据管理，了解常用功能。' if zh else 'From model downloads to managing local data.'),
        (2,'privacy',label('legal.privacy.title'),'了解本地保存、联网功能，以及您的选择。' if zh else 'Local storage, online features, and your choices.')])
    body = f'<section class="hero"><p class="eyebrow">MNN CHAT / {"帮助中心" if zh else "HELP CENTER"}</p><h1>{intro}</h1><p class="lede">{detail}</p><span class="tag"><span aria-hidden="true">●</span> {label("support.fees")}</span></section><div class="cards">{cards}</div>'
    body += f'<section class="contact-strip"><div><h2>{"还有其他问题？" if zh else "Need a hand?"}</h2><p>{"欢迎反馈使用问题、建议或隐私请求。" if zh else "Send us questions, suggestions, or privacy requests."}</p></div><a class="email" href="mailto:{EMAIL}">{EMAIL} <span aria-hidden="true">↗</span></a></section>'
    page('', '帮助中心' if zh else 'Help center', body, detail)

    faq = ''.join(f'<details {"open" if i == 0 else ""}><summary>{label("support."+key+".question")}</summary><p>{rich(label("support."+key+".answer"))}</p></details>' for i,key in enumerate(['download','offline','cloud','slow','delete']))
    support_intro = '使用中遇到问题，可以先看看下面的说明。' if zh else 'Start with these answers to common questions.'
    contact_detail = rich(label('support.contact.detail'))
    report_hint = ('反馈时，您可以注明设备型号、iOS 版本、App 版本、所用模型和重现步骤。请只提供排查问题需要的信息。' if zh else 'For troubleshooting, you can include your device, iOS and app versions, model name, and steps to reproduce. Only share what is needed to investigate.')
    body = f'<section class="page-title"><p class="eyebrow">MNN CHAT / SUPPORT</p><h1>{"帮助与反馈" if zh else "Help & support"}</h1><p class="lede">{support_intro}</p></section><div class="support-grid"><section class="faq"><h2>{label("support.faq")}</h2>{faq}</section><aside class="contact-card"><span class="small-label">{label("support.contact.title")}</span><h2>{"我们会核实并回复" if zh else "We’re here to help"}</h2><a class="email" href="mailto:{EMAIL}?subject=MNN%20Chat">{EMAIL} ↗</a><p>{contact_detail}</p><hr><p>{report_hint}</p><p class="muted">{label("support.fees")}</p></aside></div>'
    page('support', '帮助与反馈' if zh else 'Support', body, support_intro)

    for kind, route in ROUTES.items():
        title = label(f'legal.{kind}.title')
        sections = doc[kind]['sections']
        toc = ''.join(f'<a href="#section-{i}"><span>{i:02}</span>{html.escape(s["title"])}</a>' for i,s in enumerate(sections,1))
        article = ''.join(f'<section id="section-{i}"><h2>{html.escape(s["title"])}</h2>'+''.join('<p>'+rich(p)+'</p>' for p in s['paragraphs'])+'</section>' for i,s in enumerate(sections,1))
        related = ''.join(f'<a href="{href(r)}">{label("legal."+k+".title")} →</a>' for k,r in ROUTES.items() if k != kind)
        body = f'<section class="page-title legal-title"><p class="eyebrow">MNN CHAT / {route.upper()}</p><h1>{title}</h1><a class="email" href="mailto:{EMAIL}">{EMAIL}</a></section><div class="legal-grid"><aside class="toc"><p class="small-label">{"本页内容" if zh else "ON THIS PAGE"}</p><nav aria-label="{"文章目录" if zh else "Table of contents"}">{toc}</nav></aside><article>{article}<div class="related">{related}</div></article></div>'
        if kind == 'privacy':
            hosting_title = '本网站的访问' if zh else 'Visits to this website'
            hosting_text = ('本网站由 GitHub Pages 托管。GitHub 会出于安全目的记录并保存访问者的 IP 地址，无论您是否登录 GitHub。本网站没有自行添加统计脚本或反馈提交表单。详情请参阅 ' if zh else 'This website is hosted on GitHub Pages. GitHub logs and stores visitors’ IP addresses for security purposes, whether or not they are signed in. This website adds no analytics scripts or feedback submission forms. See the ')
            hosting_link = 'GitHub 隐私声明' if zh else 'GitHub Privacy Statement'
            stop = '。' if zh else '.'
            note = f'<section id="website-privacy"><h2>{hosting_title}</h2><p>{hosting_text}<a href="https://docs.github.com/en/site-policy/privacy-policies/github-general-privacy-statement" rel="noreferrer">{hosting_link}</a>{stop}</p></section>'
            body = body.replace('<div class="related">', note + '<div class="related">')
        page(route, title, body, sections[0]['paragraphs'][0])

OUT.mkdir(exist_ok=True)
for lang in ['zh-Hans','en']:
    build_language(lang)
shutil.copy2(ROOT/'assets/style.css', OUT/'style.css')
shutil.copy2(ROOT/'assets/favicon.svg', OUT/'favicon.svg')
(OUT/'404.html').write_text(f'<!doctype html><html lang="zh-Hans"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>页面未找到 · MNN Chat</title><link rel="stylesheet" href="{BASE_PATH}/style.css"><main class="hero"><h1>页面未找到</h1><p>这个地址可能已变更。</p><a href="{BASE_PATH}/support/">前往帮助与反馈 →</a></main></html>')
(OUT / '.nojekyll').touch()
print('Built 12 pages in docs/ for ' + ORIGIN + BASE_PATH)
