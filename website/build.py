"""Builds the Wala Kelmeh website: Arabic at /, English at /en/.

    python3 build.py            # production build into out/ (game linked at /play/)
    python3 build.py --preview  # links point at the live game, plus out/preview.html (both languages in one file)

Search setup in every page: unique title and description, canonical, hreflang pairs, Open Graph and
Twitter cards with a real image, JSON-LD (Organization, WebSite, SoftwareApplication, ItemList, HowTo,
FAQPage), one h1, landmarks, alt text on every image. Site-wide: robots.txt, sitemap.xml with hreflang,
llms.txt for AI answer engines, favicons.
"""
import html, json, os, re, shutil, sys
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(REPO, 'brand', 'tools'))

from content import T, CATEGORIES, SITE, CONTACT, TOTAL_CARDS
from logos import icon_C, xstitch, svg as raw_svg
from lockups2 import horiz_ar, horiz_en
from final import BR, CREAM, INK, RED, GOLD
from poses4 import P as MOODS, svg as msvg

PREVIEW = '--preview' in sys.argv
PLAY = 'https://mikdamq.github.io/Jordanian-cards/' if PREVIEW else '/play/'
OUT = os.path.join(HERE, 'out')
STATIC = os.path.join(HERE, 'static')
MASCOT_VB = '-24 -34 470 454'
UPDATED = '2026-10-23'

_n = [0]
def uid(p):
    _n[0] += 1
    return f'{p}{_n[0]}'

def t(key, lang):
    v = T[key]
    return v[lang] if isinstance(v, dict) else v

def ar_digits(s): return str(s).translate(str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩'))
def num(n, lang): return ar_digits(n) if lang == 'ar' else str(n)

def titled(svg, label):
    """Accessible inline SVG: role, label and a <title> that search engines and screen readers read."""
    return svg.replace('<svg ', '<svg role="img" aria-label="' + html.escape(label) + '" ', 1).replace('>', f'><title>{html.escape(label)}</title>', 1)

# ---------- brand assets ----------
def lockup(lang, theme):
    """theme: light (ink on fabric), dark (cream on night), red (cream on shemagh red)."""
    name = 'ولا كلمة' if lang == 'ar' else 'Wala Kelmeh'
    if theme == 'red':
        sym = icon_C('cream')
        s = horiz_ar(sym, CREAM, GOLD) if lang == 'ar' else horiz_en(sym, CREAM)
    else:
        sym = icon_C('red', uid('g'))
        fg, star = (INK, RED) if theme == 'light' else (CREAM, BR)
        s = horiz_ar(sym, fg, star) if lang == 'ar' else horiz_en(sym, fg)
    return titled(s, name)

LOGO_FILES = {}
def logo_img(lang, theme, pre, h=46, eager=False):
    """Lockup as a cached image file."""
    name = f'logo-{lang}-{theme}.svg'
    if name not in LOGO_FILES:
        LOGO_FILES[name] = lockup(lang, theme)
    vw, vh = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', LOGO_FILES[name]).groups())
    alt = 'ولا كلمة' if lang == 'ar' else 'Wala Kelmeh'
    load = '' if eager else ' loading="lazy" decoding="async"'
    return f'<img src="{pre}assets/{name}" width="{round(h * vw / vh)}" height="{h}" alt="{alt}"{load}>'

def logo_pair(lang, pre=''):
    """Both versions; CSS shows the one that matches the viewer's theme."""
    return f'<span class="logo-light">{logo_img(lang, "light", pre, eager=True)}</span><span class="logo-dark">{logo_img(lang, "dark", pre, eager=True)}</span>'

MASCOT_FILES = ('card', 'shh', 'cool', 'wave', 'laugh', 'yay', 'love', 'shock', 'proud', 'wink')
def mascot_img(key, lang, prefix, eager=False, w=440):
    ar_line, en = MOODS[key][0], MOODS[key][1]
    alt = f'شمّوغ، شماغ لعبة ولا كلمة: {ar_line}' if lang == 'ar' else f'Shammogh, the Wala Kelmeh shemagh mascot: {en}'
    h = round(w * 454 / 470)
    load = 'fetchpriority="high"' if eager else 'loading="lazy" decoding="async"'
    return f'<img src="{prefix}assets/shammogh-{key}.svg" width="{w}" height="{h}" alt="{html.escape(alt)}" {load}>'

ART_SRC = open(os.path.join(REPO, 'src', 'art.ts'), encoding='utf-8').read()
def parse_art(name):
    start = ART_SRC.index(f'export const {name}')
    block = ART_SRC[start:ART_SRC.index('\n};', start)]
    return {m.group(1): re.findall(r"'([^']*)'", m.group(2)) for m in re.finditer(r"\n\s*(\w+):\s*\[(.*?)\]", block, re.S)}
CAT_ART, MODE_ART = parse_art('CATEGORY_ART'), parse_art('MODE_ART')
TH = {'r': '#b5121b', 'g': '#4f6b2c', 'y': '#c9962a', 'k': '#2a1f1a', 'b': '#3b3f7a'}
def stitch(rows, label, cell=12):
    w, h = max(len(r) for r in rows) * cell, len(rows) * cell
    body = ''.join(xstitch(c * cell + cell / 2, r * cell + cell / 2, cell * .8, TH[v], cell * .28)
                   for r, row in enumerate(rows) for c, v in enumerate(row) if v in TH)
    return titled(raw_svg(w, h, body), label)

ART_FILES = {}
def art_img(kind, key, rows, label, pre, size=72):
    """Stitch art as a cached image file with alt text (smaller pages, indexable images)."""
    name = f'{kind}-{key}.svg'
    if name not in ART_FILES:
        w, h = max(len(r) for r in rows) * 12, len(rows) * 12
        body = ''.join(xstitch(c * 12 + 6, r * 12 + 6, 9.6, TH[v], 3.36) for r, row in enumerate(rows) for c, v in enumerate(row) if v in TH)
        ART_FILES[name] = raw_svg(w, h, body)
    hgt = round(size * len(rows) / max(len(r) for r in rows))
    return f'<img src="{pre}assets/art/{name}" width="{size}" height="{hgt}" alt="{html.escape(label)}" loading="lazy" decoding="async">'

CSS = open(os.path.join(HERE, 'site.css'), encoding='utf-8').read()

# ---------- routing ----------
PAGES = {'home': '', 'how': 'how-to-play/', 'categories': 'categories/', 'cafes': 'cafes/', 'stickers': 'stickers/'}
PAGES.update({f'cat-{cid}': f'categories/{cid}/' for cid, *_ in CATEGORIES})

class Ctx:
    """Where a page sits: language, its own route, and prefixes back to the site and language roots."""
    def __init__(self, lang, key):
        self.lang, self.key = lang, key
        depth = PAGES[key].count('/') + (1 if lang == 'en' else 0)
        self.pre = '../' * depth                       # to site root: assets, privacy
        self.url = SITE + '/' + ('en/' if lang == 'en' else '') + PAGES[key]
    def href(self, key, lang=None):
        lang = lang or self.lang
        path = ('en/' if lang == 'en' else '') + PAGES[key]
        h = self.pre + path
        go = f' data-go="{key}-{lang}"' if PREVIEW else ''
        return f'"{h or "./"}"{go}'
    def abs(self, key, lang=None):
        lang = lang or self.lang
        return SITE + '/' + ('en/' if lang == 'en' else '') + PAGES[key]

# ---------- structured data ----------
def base_graph(c):
    lang = c.lang
    org = {'@type': 'Organization', '@id': SITE + '/#org', 'name': 'ولا كلمة', 'alternateName': ['Wala Kelmeh', 'Wala Kilmeh', 'Not a Word'],
           'url': SITE + '/', 'logo': SITE + '/assets/logo-512.png', 'email': CONTACT,
           'foundingLocation': {'@type': 'Place', 'name': 'Amman, Jordan'}}
    site = {'@type': 'WebSite', '@id': SITE + '/#site', 'url': SITE + '/', 'name': 'ولا كلمة — Wala Kelmeh',
            'inLanguage': ['ar', 'en'], 'publisher': {'@id': SITE + '/#org'}}
    app = {'@type': ['SoftwareApplication', 'VideoGame'], '@id': SITE + '/#game', 'name': 'ولا كلمة — Wala Kelmeh',
           'alternateName': 'Wala Kelmeh', 'description': t('about_p', lang), 'url': c.abs('home'),
           'applicationCategory': 'GameApplication', 'genre': ['Party game', 'Charades', 'Word game'],
           'operatingSystem': 'Web, Android', 'inLanguage': 'ar', 'playMode': 'MultiPlayer',
           'numberOfPlayers': {'@type': 'QuantitativeValue', 'minValue': 2, 'maxValue': 12},
           'gamePlatform': ['Web browser', 'Android'], 'countryOfOrigin': 'JO', 'datePublished': '2026-10',
           'image': SITE + f'/assets/og-{lang}.png', 'publisher': {'@id': SITE + '/#org'},
           'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'JOD', 'availability': 'https://schema.org/InStock'}}
    return [org, site, app]

def webpage(c, title, desc):
    return {'@type': 'WebPage', '@id': c.url + '#page', 'url': c.url, 'name': title, 'description': desc, 'inLanguage': c.lang,
            'isPartOf': {'@id': SITE + '/#site'}, 'about': {'@id': SITE + '/#game'}, 'dateModified': UPDATED,
            'primaryImageOfPage': SITE + f'/assets/og-{c.lang}.png'}

def breadcrumbs_ld(c, crumbs):
    return {'@type': 'BreadcrumbList', 'itemListElement': [
        {'@type': 'ListItem', 'position': i, 'name': n, 'item': u} for i, (n, u) in enumerate(crumbs, 1)]}

def faq_ld(items, lang):
    return {'@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q[lang], 'acceptedAnswer': {'@type': 'Answer', 'text': a[lang]}} for q, a in items]}

# ---------- shared page parts ----------
def head(c, title, desc, graph):
    tw = 'en' if c.lang == 'ar' else 'ar'
    ld = json.dumps({'@context': 'https://schema.org', '@graph': graph}, ensure_ascii=False)
    d = html.escape(desc)
    return f'''<!doctype html>
<html lang="{c.lang}" dir="{'rtl' if c.lang == 'ar' else 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{d}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{c.url}">
<link rel="alternate" hreflang="ar" href="{c.abs(c.key, 'ar')}">
<link rel="alternate" hreflang="en" href="{c.abs(c.key, 'en')}">
<link rel="alternate" hreflang="x-default" href="{c.abs(c.key, 'ar')}">
<meta property="og:site_name" content="ولا كلمة — Wala Kelmeh">
<meta property="og:type" content="website">
<meta property="og:title" content="{title}">
<meta property="og:description" content="{d}">
<meta property="og:url" content="{c.url}">
<meta property="og:image" content="{SITE}/assets/og-{c.lang}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html.escape(t('og_alt', c.lang))}">
<meta property="og:locale" content="{'ar_JO' if c.lang == 'ar' else 'en_US'}">
<meta property="og:locale:alternate" content="{'en_US' if c.lang == 'ar' else 'ar_JO'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{title}">
<meta name="twitter:description" content="{d}">
<meta name="twitter:image" content="{SITE}/assets/og-{c.lang}.png">
<meta name="theme-color" content="#b5121b">
<link rel="icon" href="{c.pre}assets/icon.svg" type="image/svg+xml">
<link rel="icon" href="{c.pre}assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{c.pre}assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Almarai:wght@700;800&family=Cairo:wght@400;600;800&display=swap">
<script type="application/ld+json">{ld}</script>
<style>{CSS}</style>
</head>
<body>'''

def header(c):
    lang, other = c.lang, ('en' if c.lang == 'ar' else 'ar')
    items = (('how', 'how'), ('categories', 'categories'), ('cafes', 'cafes'), ('stickers', 'stickers'))
    cur = 'categories' if c.key.startswith('cat-') else c.key
    nav = ''.join(f'<a href={c.href(k)}{" aria-current=page" if k == cur else ""}>{T["nav"][n][lang]}</a>' for n, k in items)
    return f'''<a class="skip" href="#main">{t('skip', lang)}</a>
<header class="top">
  <div class="in">
    <a class="brand" href={c.href('home')} aria-label="{'ولا كلمة، الصفحة الرئيسية' if lang == 'ar' else 'Wala Kelmeh home'}">{logo_pair(lang, c.pre)}</a>
    <nav class="menu" aria-label="{'القائمة الرئيسية' if lang == 'ar' else 'Main'}">{nav}</nav>
    <div class="actions">
      <a class="lang" href={c.href(c.key, other)} hreflang="{other}" lang="{other}">{t('lang_switch', lang)}</a>
      <a class="btn btn-red btn-sm" href="{PLAY}">{t('play', lang)}</a>
    </div>
  </div>
</header>'''

def crumbs_html(c, crumbs):
    items = []
    for i, (name, key) in enumerate(crumbs):
        last = i == len(crumbs) - 1
        items.append(f'<li aria-current="page">{name}</li>' if last else f'<li><a href={c.href(key)}>{name}</a></li>')
    return f'<nav class="crumbs" aria-label="{"مسار الصفحة" if c.lang == "ar" else "Breadcrumb"}"><ol>{"".join(items)}</ol></nav>'

def footer(c):
    lang = c.lang
    links = [(T['nav']['how'][lang], c.href('how')), (T['nav']['categories'][lang], c.href('categories')), (T['nav']['cafes'][lang], c.href('cafes')),
             (T['nav']['stickers'][lang], c.href('stickers')), (t('privacy', lang), f'"{c.pre}privacy.html"'), (t('contact', lang), f'"mailto:{CONTACT}"')]
    nav = ''.join(f'<a href={h}>{n}</a>' for n, h in links)
    return f'''</main>
<div class="band" aria-hidden="true"></div>
<footer class="foot"><div class="in">
  <div class="foot-brand">{logo_img(lang, 'dark', c.pre, 54)}<p>{t('footer_tag', lang)}</p></div>
  <nav class="foot-links" aria-label="{'روابط' if lang == 'ar' else 'Footer'}">{nav}</nav>
  <p class="rights">{t('rights', lang)}</p>
</div></footer>
</body>
</html>'''

def phone():
    return '''<div class="phone" aria-hidden="true" dir="rtl">
  <div class="ph-bar"><span class="chip">🍽️ أكل وشرب</span><span class="timer">0:42</span></div>
  <div class="ph-card"><b>منسف</b><span dir="ltr">mansaf</span></div>
  <div class="ph-btns"><span class="ph-ok">صح ✓</span><span class="ph-skip">عدّيها</span></div>
  <div class="ph-score"><span>فريق الصقر</span><b>٧</b></div>
</div>'''

def cta_band(c, heading, mood='yay'):
    return f'''<section class="cta-band"><div class="in">
  <div class="cta-art">{mascot_img(mood, c.lang, c.pre, w=200)}</div>
  <h2>{heading}</h2><a class="btn btn-red" href="{PLAY}">{t('play', c.lang)}</a></div></section>'''

# ---------- home ----------
def home(c):
    lang, pre = c.lang, c.pre
    facts = ''.join(f'<li>{f}</li>' for f in t('hero_facts', lang))
    stores = ''.join(f'<span class="store"><small>{t("stores_soon", lang)}</small><b dir="ltr">{n}</b></span>' for n in ('Google Play', 'AppGallery', 'Galaxy Store'))
    dl = ''.join(f'<div><dt>{k[lang]}</dt><dd>{v[lang]}</dd></div>' for k, v in T['facts'])
    modes = ''.join(f'''<article class="mode">
      <div class="mode-art">{art_img('mode', k, MODE_ART[k], (('رسمة تطريز: ' if lang == 'ar' else 'Cross-stitch: ') + name[lang]), pre, 70)}</div>
      <h3>{name[lang]}</h3><p>{desc[lang]}</p><span class="tag">{who[lang]}</span></article>''' for k, name, desc, who in T['modes'])
    tiles = ''.join(f'''<li><a class="cat" href={c.href('cat-' + cid)}>
      <span class="cat-art">{art_img('cat', cid, CAT_ART[cid], (('رسمة تطريز لفئة ' + ar) if lang == 'ar' else ('Cross-stitch art for ' + en)), pre, 62)}</span>
      <b>{ar if lang == 'ar' else en}</b><small>{num(n, lang)} {t('cards_word', lang)}</small></a></li>''' for cid, ar, en, n in CATEGORIES)
    steps = ''.join(f'<li><span class="step" aria-hidden="true">{num(i, lang)}</span><h3>{h[lang]}</h3><p>{p[lang]}</p></li>' for i, (h, p) in enumerate(T['how'], 1))
    promise = ''.join(f'<li><h3>{h[lang]}</h3><p>{p[lang]}</p></li>' for h, p in T['promise'])
    stk = ''.join(f'<li class="stk">{mascot_img(k, lang, pre, w=200)}</li>' for k in ('wave', 'laugh', 'yay', 'love', 'shock', 'proud'))
    qs = ''.join(f'<details{" id=faq-install" if i == 1 else ""}{" open" if i == 0 else ""}><summary><h3>{q[lang]}</h3></summary><p>{a[lang]}</p></details>' for i, (q, a) in enumerate(T['faq']))
    cats_h = ar_digits(t('cats_h', lang)) if lang == 'ar' else t('cats_h', lang)
    main = f'''<section class="hero" aria-labelledby="hero-h"><div class="in">
    <div class="hero-text">
      <span class="eyebrow">{t('hero_eyebrow', lang)}</span>
      <h1 id="hero-h">{t('hero_h1', lang)}</h1>
      <p class="lead">{t('hero_sub', lang)}</p>
      <div class="ctas"><a class="btn btn-red" href="{PLAY}">{t('play', lang)}</a><a class="btn btn-ghost" href="#faq-install">{t('install', lang)}</a></div>
      <ul class="facts">{facts}</ul>
      <div class="stores">{stores}</div>
    </div>
    <div class="hero-art">{phone()}<div class="hero-mascot">{mascot_img('card', lang, pre, eager=True)}</div></div>
  </div></section>
<div class="band" aria-hidden="true"></div>
<section class="sec about" id="about" aria-labelledby="about-h"><div class="in">
  <div class="about-grid"><div class="sec-head"><h2 id="about-h">{t('about_h', lang)}</h2><p>{t('about_p', lang)}</p></div>
  <dl class="facts-dl">{dl}</dl></div></div></section>
<section class="sec" id="modes" aria-labelledby="modes-h"><div class="in">
  <div class="sec-head"><h2 id="modes-h">{t('modes_h', lang)}</h2><p>{t('modes_p', lang)}</p></div>
  <div class="modes">{modes}</div></div></section>
<section class="sec" id="categories" aria-labelledby="cats-h"><div class="in">
  <div class="sec-head"><h2 id="cats-h">{cats_h}</h2><p>{t('cats_p', lang)}</p></div>
  <ul class="cats">{tiles}</ul></div></section>
<section class="sec how" id="how" aria-labelledby="how-h"><div class="in">
  <div class="sec-head"><h2 id="how-h">{t('how_h', lang)}</h2></div>
  <div class="how-grid"><div class="how-text"><ol class="steps">{steps}</ol><a class="btn btn-ghost" href={c.href('how')}>{'القواعد كاملة' if lang == 'ar' else 'Read the full rules'}</a></div><div class="how-mascot">{mascot_img('shh', lang, pre)}</div></div></div></section>
<section class="sec" id="promise" aria-labelledby="promise-h"><div class="in">
  <div class="sec-head"><h2 id="promise-h">{t('promise_h', lang)}</h2></div>
  <ul class="promise">{promise}</ul></div></section>
<section class="cafes" id="cafes" aria-labelledby="cafes-h"><div class="in">
  <div class="cafes-text"><span class="eyebrow gold">{t('cafes_eyebrow', lang)}</span><h2 id="cafes-h">{t('cafes_h', lang)}</h2><p>{t('cafes_p', lang)}</p>
    <div class="ctas"><a class="btn btn-red" href="mailto:{CONTACT}?subject=Wala%20Kelmeh%20night">{t('cafes_cta', lang)}</a><span class="mail" dir="ltr">{CONTACT}</span></div></div>
  <div class="cafes-art">{mascot_img('cool', lang, pre)}</div></div></section>
<section class="sec" id="stickers" aria-labelledby="stk-h"><div class="in">
  <div class="sec-head"><h2 id="stk-h">{t('stickers_h', lang)}</h2><p>{t('stickers_p', lang)}</p></div>
  <ul class="stickers">{stk}</ul>
  <a class="btn btn-ghost" href={c.href('stickers')}>{t('stickers_cta', lang)}</a></div></section>
<section class="sec" id="faq" aria-labelledby="faq-h"><div class="in narrow">
  <div class="sec-head"><h2 id="faq-h">{t('faq_h', lang)}</h2></div>
  <div class="faq">{qs}</div></div></section>'''
    title, desc = t('meta_title', lang), t('meta_desc', lang)
    cats_ld = {'@type': 'ItemList', 'name': t('cats_h', lang), 'numberOfItems': len(CATEGORIES), 'itemListElement': [
        {'@type': 'ListItem', 'position': i, 'name': ar if lang == 'ar' else en, 'url': c.abs('categories') + f'{cid}/'}
        for i, (cid, ar, en, n) in enumerate(CATEGORIES, 1)]}
    graph = base_graph(c) + [webpage(c, title, desc), cats_ld, faq_ld(T['faq'], lang)]   # HowTo lives on the how-to-play page
    return head(c, title, desc, graph) + header(c) + '<main id="main">' + main + footer(c)

# ---------- how to play ----------
def how_page(c):
    from content_how import H
    lang, pre = c.lang, c.pre
    L = lambda d: d[lang]
    home_name = 'الرئيسية' if lang == 'ar' else 'Home'
    crumbs = [(home_name, 'home'), (L(H['crumb']), 'how')]
    quick = ''.join(f'<div><dt>{k[lang]}</dt><dd>{v[lang]}</dd></div>' for k, v in H['quick'])
    setup = ''.join(f'<li>{L(s)}</li>' for s in H['setup'])
    toc = [('setup', L(H['setup_h']))] + [(k, n[lang]) for k, n, _, _ in H['modes']] + [('scoring', L(H['score_h'])), ('rules', L(H['rules_h'])), ('signals', L(H['signals_h'])), ('tips', L(H['tips_h'])), ('faq', L(H['faq_h']))]
    toc_html = ''.join(f'<li><a href="#{a}">{n}</a></li>' for a, n in toc)
    modes = ''.join(f'''<section class="rule-block" id="{k}" aria-labelledby="{k}-h">
      <div class="rule-head"><span class="mode-art">{art_img('mode', k, MODE_ART[k], (('رسمة تطريز: ' if lang == 'ar' else 'Cross-stitch: ') + n[lang]), pre, 70)}</span><h2 id="{k}-h">{n[lang]}</h2></div>
      <ol class="rule-steps">{''.join(f'<li>{L(s)}</li>' for s in steps)}</ol><p class="best">{L(best)}</p></section>''' for k, n, steps, best in H['modes'])
    yes = ''.join(f'<li>{L(x)}</li>' for x in H['yes'])
    no = ''.join(f'<li>{L(x)}</li>' for x in H['no'])
    signals = ''.join(f'<tr><th scope="row">{a[lang]}</th><td>{b[lang]}</td></tr>' for a, b in H['signals'])
    tips_a = ''.join(f'<li>{L(x)}</li>' for x in H['tips_a'])
    tips_g = ''.join(f'<li>{L(x)}</li>' for x in H['tips_g'])
    house = ''.join(f'<li>{L(x)}</li>' for x in H['house'])
    qs = ''.join(f'<details{" open" if i == 0 else ""}><summary><h3>{q[lang]}</h3></summary><p>{a[lang]}</p></details>' for i, (q, a) in enumerate(H['faq']))
    main = f'''<section class="page-hero"><div class="in">
  {crumbs_html(c, crumbs)}
  <div class="page-hero-grid">
    <div class="page-hero-text"><h1>{L(H['h1'])}</h1><p class="answer">{L(H['answer'])}</p><dl class="facts-dl quick">{quick}</dl></div>
    <div class="page-hero-art">{mascot_img('card', lang, pre, eager=True, w=300)}</div>
  </div></div></section>
<div class="band" aria-hidden="true"></div>
<div class="in doc">
  <aside class="toc" aria-label="{'محتويات الصفحة' if lang == 'ar' else 'On this page'}"><h2>{'بهاي الصفحة' if lang == 'ar' else 'On this page'}</h2><ol>{toc_html}</ol></aside>
  <div class="doc-body">
    <section class="rule-block" id="setup" aria-labelledby="setup-h"><h2 id="setup-h">{L(H['setup_h'])}</h2><ol class="rule-steps">{setup}</ol></section>
    <h2 class="group-h">{L(H['modes_h'])}</h2>
    {modes}
    <section class="rule-block" id="scoring" aria-labelledby="scoring-h"><h2 id="scoring-h">{L(H['score_h'])}</h2><p>{L(H['score_p'])}</p></section>
    <section class="rule-block" id="rules" aria-labelledby="rules-h"><h2 id="rules-h">{L(H['rules_h'])}</h2>
      <div class="yesno"><div class="yes"><h3>{L(H['allowed'])}</h3><ul>{yes}</ul></div><div class="no"><h3>{L(H['forbidden'])}</h3><ul>{no}</ul></div></div></section>
    <section class="rule-block" id="signals" aria-labelledby="signals-h"><h2 id="signals-h">{L(H['signals_h'])}</h2><p>{L(H['signals_p'])}</p>
      <div class="tablewrap"><table class="signals"><thead><tr><th scope="col">{'المعنى' if lang == 'ar' else 'Meaning'}</th><th scope="col">{'الإشارة' if lang == 'ar' else 'Signal'}</th></tr></thead><tbody>{signals}</tbody></table></div></section>
    <section class="rule-block" id="tips" aria-labelledby="tips-h"><h2 id="tips-h">{L(H['tips_h'])}</h2>
      <div class="two"><div><h3>{L(H['tips_actor'])}</h3><ul>{tips_a}</ul></div><div><h3>{L(H['tips_guess'])}</h3><ul>{tips_g}</ul></div></div>
      <h3>{L(H['house_h'])}</h3><ul>{house}</ul></section>
    <section class="rule-block" id="faq" aria-labelledby="faq-h"><h2 id="faq-h">{L(H['faq_h'])}</h2><div class="faq">{qs}</div></section>
  </div>
</div>
{cta_band(c, L(H['cta_h']))}'''
    title, desc = L(H['title']), L(H['desc'])
    howto = {'@type': 'HowTo', '@id': c.url + '#howto', 'name': L(H['h1']), 'description': L(H['answer']),
             'totalTime': 'PT5M', 'supply': [{'@type': 'HowToSupply', 'name': 'A phone' if lang == 'en' else 'جوال'}],
             'step': [{'@type': 'HowToStep', 'position': i, 'text': L(s), 'url': c.url + '#setup'} for i, s in enumerate(H['setup'], 1)]}
    graph = base_graph(c) + [webpage(c, title, desc), breadcrumbs_ld(c, [(home_name, c.abs('home')), (L(H['crumb']), c.url)]), howto, faq_ld(H['faq'], lang)]
    return head(c, title, desc, graph) + header(c) + '<main id="main">' + main + footer(c)

# ---------- categories ----------
import content_cats as CC
CARDS = CC.load_cards()

def card_tile(ar, arabizi, level, lang):
    dots = ''.join(f'<i class="{"on" if i < level else ""}"></i>' for i in range(3))
    lvl = CC.C['levels'][lang][level - 1]
    return (f'<li class="scard"><b lang="ar" dir="rtl">{ar}</b><span lang="en" dir="ltr">{html.escape(arabizi)}</span>'
            f'<span class="lvl" title="{lvl}" aria-label="{lvl}">{dots}</span></li>')

def categories_page(c):
    lang, pre, L = c.lang, c.pre, (lambda d: d[c.lang])
    home_name = 'الرئيسية' if lang == 'ar' else 'Home'
    tiles = ''.join(f'''<li><a class="catrow" href={c.href('cat-' + cid)}>
      <span class="cat-art">{art_img('cat', cid, CAT_ART[cid], (('رسمة تطريز لفئة ' + ar) if lang == 'ar' else ('Cross-stitch art for ' + en)), pre, 62)}</span>
      <span class="catrow-text"><b>{ar if lang == 'ar' else en}</b><small>{num(n, lang)} {L(CC.C['cards_word'])}</small>
      <span>{CC.CAT[cid][0 if lang == 'ar' else 1]}</span></span></a></li>''' for cid, ar, en, n in CATEGORIES)
    main = f'''<section class="page-hero"><div class="in">
  {crumbs_html(c, [(home_name, 'home'), (L(CC.C['index_crumb']), 'categories')])}
  <div class="page-hero-grid"><div class="page-hero-text"><h1>{L(CC.C['index_h1'])}</h1><p class="answer">{L(CC.C['index_answer'])}</p></div>
  <div class="page-hero-art">{mascot_img('laugh', lang, pre, eager=True, w=300)}</div></div></div></section>
<div class="band" aria-hidden="true"></div>
<section class="sec"><div class="in"><ul class="catlist">{tiles}</ul></div></section>
{cta_band(c, L(CC.C['cta_h']))}'''
    title, desc = L(CC.C['index_title']), L(CC.C['index_desc'])
    items = {'@type': 'ItemList', 'numberOfItems': len(CATEGORIES), 'itemListElement': [
        {'@type': 'ListItem', 'position': i, 'name': ar if lang == 'ar' else en, 'url': c.abs('cat-' + cid)} for i, (cid, ar, en, n) in enumerate(CATEGORIES, 1)]}
    page = webpage(c, title, desc); page['@type'] = 'CollectionPage'
    graph = base_graph(c) + [page, breadcrumbs_ld(c, [(home_name, c.abs('home')), (L(CC.C['index_crumb']), c.url)]), items]
    return head(c, title, desc, graph) + header(c) + '<main id="main">' + main + footer(c)

def category_page(cid):
    def render(c):
        lang, pre, L = c.lang, c.pre, (lambda d: d[c.lang])
        _, ar, en, n = next(x for x in CATEGORIES if x[0] == cid)
        name = ar if lang == 'ar' else en
        intro_ar, intro_en, best_ar, best_en = CC.CAT[cid]
        cards = CARDS[cid]
        sample = CC.samples(cards)
        counts = [sum(1 for x in cards if x[2] == k) for k in (1, 2, 3)]
        home_name = 'الرئيسية' if lang == 'ar' else 'Home'
        crumbs = [(home_name, 'home'), (L(CC.C['index_crumb']), 'categories'), (name, 'cat-' + cid)]
        levels = ''.join(f'<div><dt>{lv}</dt><dd>{num(k, lang)}</dd></div>' for lv, k in zip(CC.C['levels'][lang], counts) if k)
        idx = [x[0] for x in CATEGORIES].index(cid)
        related = [CATEGORIES[(idx + d) % len(CATEGORIES)] for d in (1, 2, 3)]
        rel = ''.join(f'''<li><a class="cat" href={c.href('cat-' + r[0])}><span class="cat-art">{art_img('cat', r[0], CAT_ART[r[0]], (('رسمة تطريز لفئة ' + r[1]) if lang == 'ar' else ('Cross-stitch art for ' + r[2])), pre, 62)}</span>
          <b>{r[1] if lang == 'ar' else r[2]}</b><small>{num(r[3], lang)} {L(CC.C['cards_word'])}</small></a></li>''' for r in related)
        note = L(CC.C['samples_note']).format(n=num(len(sample), lang), total=num(n, lang))
        h1 = L(CC.C['cat_h1']).format(name=name)
        main = f'''<section class="page-hero"><div class="in">
  {crumbs_html(c, crumbs)}
  <div class="page-hero-grid">
    <div class="page-hero-text"><span class="eyebrow">{num(n, lang)} {L(CC.C['cards_word'])}</span><h1>{h1}</h1>
      <p class="answer">{intro_ar if lang == 'ar' else intro_en}</p>
      <dl class="facts-dl quick"><div><dt>{L(CC.C['best_h'])}</dt><dd>{best_ar if lang == 'ar' else best_en}</dd></div>{levels}</dl>
      <div class="ctas"><a class="btn btn-red" href="{PLAY}">{L(CC.C['play_cat'])}</a></div></div>
    <div class="page-hero-art cat-hero-art">{art_img('cat', cid, CAT_ART[cid], (('رسمة تطريز لفئة ' + ar) if lang == 'ar' else ('Cross-stitch art for ' + en)), pre, 220)}</div>
  </div></div></section>
<div class="band" aria-hidden="true"></div>
<section class="sec" aria-labelledby="samples-h"><div class="in">
  <div class="sec-head"><h2 id="samples-h">{L(CC.C['samples_h'])}</h2><p>{note}</p></div>
  <ul class="scards">{''.join(card_tile(a, b, lv, lang) for a, b, lv in sample)}</ul></div></section>
<section class="sec related" aria-labelledby="rel-h"><div class="in">
  <div class="sec-head"><h2 id="rel-h">{L(CC.C['related_h'])}</h2></div>
  <ul class="cats">{rel}</ul></div></section>
{cta_band(c, L(CC.C['cta_h']), 'card')}'''
        title = L(CC.C['cat_title']).format(name=name, n=num(n, lang))
        desc = (intro_ar if lang == 'ar' else intro_en) + (f' {num(n, lang)} بطاقة بلعبة ولا كلمة.' if lang == 'ar' else f' {n} cards in Wala Kelmeh.')
        terms = {'@type': 'DefinedTermSet', 'name': name, 'inLanguage': 'ar', 'hasDefinedTerm': [
            {'@type': 'DefinedTerm', 'name': a, 'alternateName': b} for a, b, _ in sample]}
        page = webpage(c, title, desc); page['@type'] = 'CollectionPage'
        graph = base_graph(c) + [page, breadcrumbs_ld(c, [(home_name, c.abs('home')), (L(CC.C['index_crumb']), c.abs('categories')), (name, c.url)]), terms]
        return head(c, title, desc, graph) + header(c) + '<main id="main">' + main + footer(c)
    return render

BUILT = {'home': home, 'how': how_page, 'categories': categories_page}
BUILT.update({f'cat-{cid}': category_page(cid) for cid, *_ in CATEGORIES})

# ---------- site files ----------
def robots():
    return f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n'

def sitemap():
    urls = ''
    for key in BUILT:
        ar, en = SITE + '/' + PAGES[key], SITE + '/en/' + PAGES[key]
        for loc in (ar, en):
            urls += (f'  <url>\n    <loc>{loc}</loc>\n    <lastmod>{UPDATED}</lastmod>\n'
                     f'    <xhtml:link rel="alternate" hreflang="ar" href="{ar}"/>\n'
                     f'    <xhtml:link rel="alternate" hreflang="en" href="{en}"/>\n'
                     f'    <xhtml:link rel="alternate" hreflang="x-default" href="{ar}"/>\n  </url>\n')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + '</urlset>\n')

def llms():
    """Plain-language summary for AI answer engines (llms.txt convention)."""
    from content_how import H
    cats = '\n'.join(f'- {ar} ({en}): {n} cards' for cid, ar, en, n in CATEGORIES)
    faq = '\n'.join(f'**{q["en"]}** {a["en"]}' for q, a in T['faq'] + H['faq'])
    rules = '\n'.join(f'{i}. {s["en"]}' for i, s in enumerate(H['setup'], 1))
    return f'''# ولا كلمة — Wala Kelmeh

> {T['about_p']['en']}

- Website: {SITE}/ (Arabic), {SITE}/en/ (English)
- How to play: {SITE}/en/how-to-play/
- Play: {SITE}/play/
- Price: free. No account. Works offline after install. No ads during play.
- Players: 2 to 12. Teams: 2 to 4, or none. Turns: 30, 60 or 90 seconds. Rounds: 1 to 10.
- Modes: classic charades (تمثيل), heads up (عالجبين), who's fastest (مين أسرع؟)
- Made in Amman, Jordan, 2026. Contact: {CONTACT}

## How to play
{H['answer']['en']}

{rules}

## Categories ({TOTAL_CARDS} cards)
{cats}

## FAQ
{faq}
'''

def write(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    open(path, 'w', encoding='utf-8').write(text)

def build():
    for key, fn in BUILT.items():
        for lang in ('ar', 'en'):
            write(os.path.join(OUT, 'en' if lang == 'en' else '', PAGES[key], 'index.html'), fn(Ctx(lang, key)))
    write(os.path.join(OUT, 'robots.txt'), robots())
    write(os.path.join(OUT, 'sitemap.xml'), sitemap())
    write(os.path.join(OUT, 'llms.txt'), llms())
    for name, svg in ART_FILES.items():
        write(os.path.join(OUT, 'assets', 'art', name), svg)
    for name, svg in LOGO_FILES.items():
        write(os.path.join(OUT, 'assets', name), svg)
    for k in MASCOT_FILES:
        write(os.path.join(OUT, 'assets', f'shammogh-{k}.svg'), msvg(MOODS[k][2](f'a{k}'), MASCOT_VB))
    shutil.copy(os.path.join(REPO, 'brand', 'logo', 'symbol', 'symbol-small.svg'), os.path.join(OUT, 'assets', 'icon.svg'))
    if os.path.isdir(STATIC):
        shutil.copytree(STATIC, OUT, dirs_exist_ok=True)
    print('built', OUT, '(preview)' if PREVIEW else '', '·', ', '.join(BUILT))

def preview_bundle():
    """One-file review link: every built page in both languages; internal links switch views."""
    def body(key, lang):
        s = BUILT[key](Ctx(lang, key))
        s = s[s.index('<body>') + 6:s.index('</body>')]
        s = re.sub(r'<img src="(?:\.\./)*assets/shammogh-(\w+)\.svg"[^>]*?alt="([^"]*)"[^>]*>',
                   lambda m: msvg(MOODS[m.group(1)][2](uid('p')), MASCOT_VB).replace('<svg ', f'<svg role="img" aria-label="{m.group(2)}" class="pv-img" ', 1), s)
        s = re.sub(r'<img src="(?:\.\./)*assets/art/([\w-]+\.svg)"[^>]*?alt="([^"]*)"[^>]*>',
                   lambda m: ART_FILES[m.group(1)].replace('<svg ', f'<svg role="img" aria-label="{m.group(2)}" class="pv-img" ', 1), s)
        s = re.sub(r'<img src="(?:\.\./)*assets/(logo-[\w-]+\.svg)"[^>]*?alt="([^"]*)"[^>]*>',
                   lambda m: LOGO_FILES[m.group(1)].replace('<svg ', '<svg class="pv-logo" ', 1), s)
        return s
    views = ''.join(f'<div class="pv-view" id="v-{k}-{l}" lang="{l}" dir="{"rtl" if l == "ar" else "ltr"}"{"" if (k, l) == ("home", "ar") else " hidden"}>{body(k, l)}</div>'
                    for k in BUILT for l in ('ar', 'en'))
    script = '''<script>
document.addEventListener('click', function (e) {
  var a = e.target.closest('a[data-go]');
  if (!a) return;
  var v = document.getElementById('v-' + a.dataset.go);
  if (!v) { e.preventDefault(); return; }
  e.preventDefault();
  document.querySelectorAll('.pv-view').forEach(function (x) { x.hidden = x !== v; });
  window.scrollTo(0, 0);
});
</script>'''
    note = '<p class="pv-note">Preview · نسخة تجريبية · ' + ' · '.join(BUILT) + ' built; other links switch once their pages exist</p>'
    doc = (f'<title>Wala Kelmeh Website</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
           '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
           '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Almarai:wght@700;800&family=Cairo:wght@400;600;800&display=swap">\n'
           f'<style>{CSS}\n.pv-img{{width:100%;height:auto;display:block}}.mode-art .pv-img{{width:70px}}.cat-art .pv-img{{width:62px}}'
           '.pv-note{margin:0;padding:8px 16px;background:#2a1f1a;color:#f4ecdd;font:600 13px Cairo,sans-serif;text-align:center}</style>\n'
           f'{note}{views}{script}')
    write(os.path.join(OUT, 'preview.html'), doc)
    print('preview bundle written')

if __name__ == '__main__':
    build()
    if PREVIEW:
        preview_bundle()
