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

from content import T, CATEGORIES, SITE, CONTACT, SOCIAL, GOATCOUNTER, GA_ID, CLARITY_ID, CONSENT, TOTAL_CARDS, SUGGEST, SUGGEST_ENDPOINT
from logos import icon_C, xstitch, svg as raw_svg
from lockups2 import horiz_ar, horiz_en
from final import BR, CREAM, INK, RED, GOLD
from poses4 import P as MOODS, svg as msvg

PREVIEW = '--preview' in sys.argv
PLAY = 'https://walakelmeh.com/play/' if PREVIEW else '/play/'
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

MASCOT_FILES = tuple(MOODS)   # every mood: the stickers page shows them all
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
PAGES = {'home': '', 'how': 'how-to-play/', 'categories': 'categories/', 'cafes': 'cafes/', 'stickers': 'stickers/', 'privacy': 'privacy/', 'blog': 'blog/'}
PAGES.update({f'cat-{cid}': f'categories/{cid}/' for cid, *_ in CATEGORIES})
import content_blog as CB
PAGES.update({f'post-{p["slug"]}': f'blog/{p["slug"]}/' for p in CB.POSTS})

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
           'foundingLocation': {'@type': 'Place', 'name': 'Amman, Jordan'}, 'sameAs': list(SOCIAL.values())}
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
    items = (('how', 'how'), ('categories', 'categories'), ('cafes', 'cafes'), ('stickers', 'stickers'), ('blog', 'blog'))
    cur = 'categories' if c.key.startswith('cat-') else 'blog' if c.key.startswith('post-') else c.key
    nav = ''.join(f'<a href={c.href(k)}{" aria-current=page" if k == cur else ""}>{T["nav"][n][lang]}</a>' for n, k in items)
    home_label = 'الرئيسية' if lang == 'ar' else 'Home'
    mnav = f'<a href={c.href("home")}{" aria-current=page" if cur == "home" else ""}>{home_label}</a>' + nav
    panel_id = f'mnav-{c.key}-{lang}'
    return f'''<a class="skip" href="#main">{t('skip', lang)}</a>
<header class="top">
  <div class="in">
    <a class="brand" href={c.href('home')} aria-label="{'ولا كلمة، الصفحة الرئيسية' if lang == 'ar' else 'Wala Kelmeh home'}">{logo_pair(lang, c.pre)}</a>
    <nav class="menu" aria-label="{'القائمة الرئيسية' if lang == 'ar' else 'Main'}">{nav}</nav>
    <div class="actions">
      <a class="lang" href={c.href(c.key, other)} hreflang="{other}" lang="{other}">{t('lang_switch', lang)}</a>
      <a class="btn btn-red btn-sm" href="{PLAY}" data-goatcounter-click="site/play">{t('play', lang)}</a>
      <button class="menu-btn" type="button" aria-expanded="false" aria-controls="{panel_id}" data-open="{'افتح القائمة' if lang == 'ar' else 'Open menu'}" data-close="{'سكّر القائمة' if lang == 'ar' else 'Close menu'}" aria-label="{'افتح القائمة' if lang == 'ar' else 'Open menu'}"><span></span><span></span><span></span></button>
    </div>
  </div>
  <div class="mnav" id="{panel_id}" hidden>
    <nav aria-label="{'القائمة' if lang == 'ar' else 'Menu'}">{mnav}</nav>
    <div class="mnav-foot">
      <a class="lang" href={c.href(c.key, other)} hreflang="{other}" lang="{other}">{t('lang_switch', lang)}</a>
      <a class="btn btn-red" href="{PLAY}" data-goatcounter-click="site/play">{t('play', lang)}</a>
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
             (T['nav']['stickers'][lang], c.href('stickers')), (T['nav']['blog'][lang], c.href('blog')), (t('privacy', lang), c.href('privacy')), (t('contact', lang), f'"mailto:{CONTACT}"')]
    nav = ''.join(f'<a href={h}>{n}</a>' for n, h in links)
    nav += ''.join(f'<a href="{u}" rel="me noopener" target="_blank" lang="en" dir="ltr">{n}</a>' for n, u in SOCIAL.items())
    if CONSENT_ON:
        nav += f'<button type="button" class="foot-btn" data-consent-open>{CONSENT["settings"][lang]}</button>'
    return f'''</main>
<div class="band" aria-hidden="true"></div>
<footer class="foot"><div class="in">
  <div class="foot-brand">{logo_img(lang, 'dark', c.pre, 54)}<p>{t('footer_tag', lang)}</p></div>
  <nav class="foot-links" aria-label="{'روابط' if lang == 'ar' else 'Footer'}">{nav}</nav>
  <p class="rights">{t('rights', lang)}</p>
</div></footer>
{SITE_JS}
{ANALYTICS}
{consent_js(c)}
{SUGGEST_JS if c.key.startswith('cat') or c.key in ('categories', 'cafes') else ''}
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
  <h2>{heading}</h2><a class="btn btn-red" href="{PLAY}" data-goatcounter-click="site/play">{t('play', c.lang)}</a></div></section>'''

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
      <div class="ctas"><a class="btn btn-red" href="{PLAY}" data-goatcounter-click="site/play">{t('play', lang)}</a><a class="btn btn-ghost" href="{PLAY}?install=1" data-goatcounter-click="site/install">{t('install', lang)}</a></div>
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
  <ul class="cats">{tiles}</ul>
  <div class="invite"><div><b>{SUGGEST['home_h'][lang]}</b><span>{SUGGEST['home_p'][lang]}</span></div><a class="btn btn-ghost" href={c.href('categories')[:-1] + '#suggest"' if not PREVIEW else c.href('categories')}>{SUGGEST['home_cta'][lang]}</a></div></div></section>
<section class="sec how" id="how" aria-labelledby="how-h"><div class="in">
  <div class="sec-head"><h2 id="how-h">{t('how_h', lang)}</h2></div>
  <div class="how-grid"><div class="how-text"><ol class="steps">{steps}</ol><a class="btn btn-ghost" href={c.href('how')}>{'القواعد كاملة' if lang == 'ar' else 'Read the full rules'}</a></div><div class="how-mascot">{mascot_img('shh', lang, pre)}</div></div></div></section>
<section class="sec" id="promise" aria-labelledby="promise-h"><div class="in">
  <div class="sec-head"><h2 id="promise-h">{t('promise_h', lang)}</h2></div>
  <ul class="promise">{promise}</ul></div></section>
<section class="cafes" id="cafes" aria-labelledby="cafes-h"><div class="in">
  <div class="cafes-text"><span class="eyebrow gold">{t('cafes_eyebrow', lang)}</span><h2 id="cafes-h">{t('cafes_h', lang)}</h2><p>{t('cafes_p', lang)}</p>
    <div class="ctas"><a class="btn btn-red" href={c.href('cafes')}>{t('cafes_cta', lang)}</a><span class="mail" dir="ltr">{CONTACT}</span></div></div>
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

# ---------- suggestion forms ----------
def suggest_form(c, kind, cid=None, cat_name=None):
    """kind: card (inside a category page) or category (new category idea). Works without a backend: falls back to email."""
    lang, S = c.lang, (lambda k: SUGGEST[k][c.lang])
    fid = f'sg-{kind}-{cid or "new"}-{lang}'
    if kind == 'card':
        lv = ''.join(f'<label><input type="radio" name="level" value="{i}"{" checked" if i == 1 else ""}><span>{n}</span></label>'
                     for i, n in enumerate(CC.C['levels'][lang], 1))
        fields = f'''<input type="hidden" name="category" value="{cid}">
      <div class="f-row"><label for="{fid}-w">{S('word')}</label><input id="{fid}-w" name="word" required maxlength="60" placeholder="{S('word_ph')}" autocomplete="off"></div>
      <div class="f-row"><label for="{fid}-a">{S('arabizi')}</label><input id="{fid}-a" name="arabizi" maxlength="60" dir="ltr" placeholder="{S('arabizi_ph')}" autocomplete="off"></div>
      <fieldset class="f-row"><legend>{S('level')}</legend><div class="seg">{lv}</div></fieldset>'''
        head_h, head_p, mood = S('card_h'), S('card_p'), 'think'
    else:
        fields = f'''<div class="f-row"><label for="{fid}-c">{S('cat_name')}</label><input id="{fid}-c" name="category_name" required maxlength="60" placeholder="{S('cat_name_ph')}" autocomplete="off"></div>
      <div class="f-row"><label for="{fid}-e">{S('examples')}</label><textarea id="{fid}-e" name="examples" rows="3" maxlength="400" placeholder="{S('examples_ph')}"></textarea></div>'''
        head_h, head_p, mood = S('cat_h'), S('cat_p'), 'think'
    subject = ('اقتراح بطاقة' if kind == 'card' else 'اقتراح فئة') + (f': {cat_name}' if cat_name else '')
    return f'''<section class="suggest" id="suggest" aria-labelledby="{fid}-h"><div class="in">
  <div class="suggest-card">
    <div class="suggest-head"><div class="suggest-art">{mascot_img(mood, lang, c.pre, w=160)}</div><div><h2 id="{fid}-h">{head_h}</h2><p>{head_p}</p></div></div>
    <form class="sg-form" id="{fid}" data-kind="{kind}" data-subject="{html.escape(subject)}" data-endpoint="{SUGGEST_ENDPOINT}" data-mail="{CONTACT}" novalidate>
      <input type="hidden" name="subject" value="{html.escape('ولا كلمة · ' + subject)}">
      <input type="hidden" name="from_name" value="Wala Kelmeh website">
      <input type="hidden" name="kind" value="{kind}"><input type="hidden" name="lang" value="{lang}">
      {fields}
      <div class="f-row"><label for="{fid}-n">{S('name')}</label><input id="{fid}-n" name="name" maxlength="60" placeholder="{S('name_ph')}" autocomplete="nickname"></div>
      <div class="hp" aria-hidden="true"><label>Website<input type="checkbox" name="botcheck" tabindex="-1"></label></div>
      <div class="f-actions"><button class="btn btn-red" type="submit" data-label="{S('send')}" data-busy="{S('sending')}">{S('send')}</button>
        <p class="f-note">{S('privacy')}</p></div>
      <p class="f-status" role="status" aria-live="polite" data-ok="{S('thanks')}" data-err="{S('error')}" data-mail-label="{S('by_email')}"></p>
    </form>
  </div></div></section>'''

# Google Analytics and Clarity: a banner asks first, and the answer is shared with the game
# (same origin, same "wk.consent" key). Off when neither ID is set, and in the preview.
CONSENT_ON = bool(GA_ID or CLARITY_ID) and not PREVIEW

def consent_text(lang):
    tools = [n for n, on in (('Google Analytics', GA_ID), ('Microsoft Clarity', CLARITY_ID)) if on]
    many = len(tools) > 1
    return CONSENT['text'][lang].format(tools=(' و ' if lang == 'ar' else ' and ').join(tools),
                                        them='بنشغّلهم' if many else 'بنشغّله', they='They only run' if many else 'It only runs')

def consent_js(c):
    if not CONSENT_ON:
        return ''
    cfg = json.dumps({'ga': GA_ID, 'clarity': CLARITY_ID, 'privacyHref': c.href('privacy').strip('"'), 'privacyText': CONSENT['privacy'][c.lang],
                      'text': consent_text(c.lang), **{k: CONSENT[k][c.lang] for k in ('yes', 'no', 'label')}}, ensure_ascii=False)
    return f"""<script>
(function (cfg) {{
  var KEY = 'wk.consent';
  function get() {{ try {{ var v = JSON.parse(localStorage.getItem(KEY) || 'null'); return v && v.analytics; }} catch (e) {{ return null; }} }}
  function inject(src) {{ var s = document.createElement('script'); s.async = true; s.src = src; document.head.appendChild(s); }}
  function load() {{
    if (cfg.ga && !window.gtag) {{
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () {{ window.dataLayer.push(arguments); }};
      gtag('js', new Date()); gtag('config', cfg.ga); inject('https://www.googletagmanager.com/gtag/js?id=' + cfg.ga);
    }}
    if (cfg.clarity && !window.clarity) {{
      window.clarity = function () {{ (window.clarity.q = window.clarity.q || []).push(arguments); }};
      inject('https://www.clarity.ms/tag/' + cfg.clarity); window.clarity('consent');
    }}
  }}
  function revoke() {{
    if (!window.gtag && !window.clarity) return;
    try {{ window.clarity && window.clarity('consent', false); }} catch (e) {{}}
    document.cookie.split(';').forEach(function (c) {{
      var n = c.split('=')[0].trim();
      if (/^(_ga|_gid|_gat|_clck|_clsk|CLID|ANONCHK|MR|MUID|SM)/.test(n)) ['', '; domain=' + location.hostname, '; domain=.' + location.hostname.replace(/^www\\./, '')].forEach(function (d) {{
        document.cookie = n + '=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/' + d; }});
    }});
    location.reload();
  }}
  function answer(granted) {{
    try {{ localStorage.setItem(KEY, JSON.stringify({{ analytics: granted ? 'granted' : 'denied', at: Date.now() }})); }} catch (e) {{}}
    close(); if (granted) load(); else revoke();
  }}
  var box = null;
  function close() {{ if (box) {{ box.remove(); box = null; }} }}
  function open() {{
    if (box) return;
    box = document.createElement('div'); box.className = 'consent'; box.setAttribute('role', 'region'); box.setAttribute('aria-label', cfg.label);
    var p = document.createElement('p'); p.textContent = cfg.text + ' ';
    var link = document.createElement('a'); link.href = cfg.privacyHref; link.textContent = cfg.privacyText;
    p.appendChild(link);
    var row = document.createElement('div'); row.className = 'consent-btns';
    [[cfg.yes, true, 'btn btn-red'], [cfg.no, false, 'btn btn-ghost']].forEach(function (b) {{
      var el = document.createElement('button'); el.type = 'button'; el.className = b[2]; el.textContent = b[0];
      el.addEventListener('click', function () {{ answer(b[1]); }}); row.appendChild(el);
    }});
    box.appendChild(p); box.appendChild(row); document.body.appendChild(box);
  }}
  document.addEventListener('click', function (e) {{ if (e.target.closest('[data-consent-open]')) open(); }});
  var v = get();
  if (v === 'granted') load(); else if (v !== 'denied') open();
}})({cfg});
</script>"""

# GoatCounter: cookie-free, no personal data. data-goatcounter-click on links counts those clicks too.
ANALYTICS = '' if PREVIEW or not GOATCOUNTER else f'<script data-goatcounter="https://{GOATCOUNTER}.goatcounter.com/count" async src="https://gc.zgo.at/count.js"></script>'

SITE_JS = """<script>
(function () {
  var root = document.documentElement;
  root.classList.add('js');
  // Mobile menu: one handler for every header (the preview bundle has many).
  function setMenu(btn, open) {
    var panel = document.getElementById(btn.getAttribute('aria-controls'));
    if (!panel) return;
    btn.setAttribute('aria-expanded', open ? 'true' : 'false');
    btn.setAttribute('aria-label', open ? btn.dataset.close : btn.dataset.open);
    panel.hidden = !open;
    root.classList.toggle('menu-open', open);
    if (open) { var first = panel.querySelector('a'); if (first) first.focus(); }
  }
  function openBtn() { return document.querySelector('.menu-btn[aria-expanded="true"]'); }
  document.addEventListener('click', function (e) {
    var btn = e.target.closest('.menu-btn');
    if (btn) { setMenu(btn, btn.getAttribute('aria-expanded') !== 'true'); return; }
    var b = openBtn();
    if (b && (e.target.closest('.mnav a') || !e.target.closest('.top'))) setMenu(b, false);
  });
  document.addEventListener('keydown', function (e) {
    var b = openBtn();
    if (e.key === 'Escape' && b) { setMenu(b, false); b.focus(); }
  });
  window.addEventListener('resize', function () { var b = openBtn(); if (b && window.innerWidth > 860) setMenu(b, false); });
  // Header shadow once the page scrolls.
  var onScroll = function () { root.classList.toggle('scrolled', window.scrollY > 8); };
  window.addEventListener('scroll', onScroll, { passive: true }); onScroll();
  // Scroll reveals. Without JS, or with reduced motion, everything simply shows.
  if (!('IntersectionObserver' in window) || window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
  var groups = '.cats, .catlist, .modes, .scards, .stickers, .sgallery, .faq, .rule-steps, .post-list, .kit-list, .why-grid, .how-steps';
  var items = 'main section:not(.hero) > .in > *, main .rule-block, .cta-band .cta-art';
  var seen = new Set();
  document.querySelectorAll(groups).forEach(function (g) {
    Array.prototype.forEach.call(g.children, function (el, i) { el.style.setProperty('--i', Math.min(i, 8)); el.classList.add('rv', 'rv-item'); seen.add(el); });
  });
  document.querySelectorAll(items).forEach(function (el) {
    if (seen.has(el) || el.closest('.rv-item')) return;
    el.classList.add('rv');
    if (el.querySelector(':scope > img, :scope > .pv-img') && el.matches('[class*="art"], [class*="mascot"]')) el.classList.add('rv-pop');
  });
  var io = new IntersectionObserver(function (entries) {
    entries.forEach(function (en) { if (en.isIntersecting) { en.target.classList.add('in-view'); io.unobserve(en.target); } });
  }, { rootMargin: '0px 0px -8% 0px', threshold: 0.12 });
  document.querySelectorAll('.rv').forEach(function (el) { io.observe(el); });
})();
</script>"""

SUGGEST_JS = """<script>
(function () {
  document.querySelectorAll('form.sg-form').forEach(function (f) {
    f.addEventListener('submit', function (e) {
      e.preventDefault();
      var status = f.querySelector('.f-status'), btn = f.querySelector('button[type=submit]');
      var missing = null;
      f.querySelectorAll('[required]').forEach(function (r) {
        var bad = !r.value.trim();
        if (bad) { r.setAttribute('aria-invalid', 'true'); missing = missing || r; } else { r.removeAttribute('aria-invalid'); }
      });
      if (missing) { missing.focus(); return; }
      var data = new FormData(f);
      if (data.get('botcheck')) return;                      // honeypot: bots tick hidden fields
      data.append('page', location.pathname);
      var done = function (ok) {
        btn.disabled = false; btn.textContent = btn.dataset.label;
        status.textContent = ok ? status.dataset.ok : status.dataset.err;
        status.className = 'f-status ' + (ok ? 'ok' : 'err');
        if (ok) { f.reset(); }
      };
      btn.disabled = true; btn.textContent = btn.dataset.busy;
      var url = f.dataset.endpoint;
      var skip = { subject: 1, from_name: 1, botcheck: 1 };
      var lines = []; data.forEach(function (v, k) { if (v && !skip[k]) lines.push(k + ': ' + v); });
      var mailto = 'mailto:' + f.dataset.mail + '?subject=' + encodeURIComponent(f.dataset.subject) + '&body=' + encodeURIComponent(lines.join('\\n'));
      // If our server can't send it, the reason shows and the visitor can still send it by email.
      var failed = function (code) {
        done(false);
        status.textContent = status.dataset.err + ' (' + code + ') ';
        var a = document.createElement('a'); a.href = mailto; a.textContent = status.dataset.mailLabel; status.appendChild(a);
      };
      if (window.__PREVIEW__) { setTimeout(function () { done(true); }, 500); return; }
      if (url) {
        fetch(url, { method: 'POST', body: data, headers: { Accept: 'application/json' } })
          .then(function (r) { return r.text().then(function (t) {
            var j = null; try { j = JSON.parse(t); } catch (err) { j = null; }
            if (r.ok && j && j.success) done(true); else failed((j && j.error) || ('http ' + r.status));
          }); })
          .catch(function () { failed('network'); });
        return;
      }
      location.href = mailto;
      done(true);
    });
  });
})();
</script>"""

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
{suggest_form(c, 'category')}
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
      <div class="ctas"><a class="btn btn-red" href="{PLAY}" data-goatcounter-click="site/play">{L(CC.C['play_cat'])}</a></div></div>
    <div class="page-hero-art cat-hero-art">{art_img('cat', cid, CAT_ART[cid], (('رسمة تطريز لفئة ' + ar) if lang == 'ar' else ('Cross-stitch art for ' + en)), pre, 220)}</div>
  </div></div></section>
<div class="band" aria-hidden="true"></div>
<section class="sec" aria-labelledby="samples-h"><div class="in">
  <div class="sec-head"><h2 id="samples-h">{L(CC.C['samples_h'])}</h2><p>{note}</p></div>
  <ul class="scards">{''.join(card_tile(a, b, lv, lang) for a, b, lv in sample)}</ul></div></section>
{suggest_form(c, 'card', cid, name)}
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

# ---------- cafés and partners ----------
PARTNER_FILES = {}
def partner_badge_img(lang, pre, w=220):
    name = f'partner-badge-{lang}.svg'
    if name not in PARTNER_FILES:
        PARTNER_FILES[name] = open(os.path.join(REPO, 'brand', 'logo', 'partner', f'partner-badge-{"arabic" if lang == "ar" else "english"}.svg')).read()
    alt = 'شارة شريك ولا كلمة' if lang == 'ar' else 'Wala Kelmeh partner badge'
    return f'<img src="{pre}assets/{name}" width="{w}" height="{w}" alt="{alt}" loading="lazy" decoding="async">'

def table_tent(lang, pre):
    """A table tent mock-up: the symbol, a call to scan, and a stylised QR placeholder."""
    cells = ''.join(f'<i class="{"on" if (r * 7 + c * 3) % 5 < 2 or r in (0, 6) and c in (0, 1, 5, 6) or c in (0, 6) and r in (0, 1, 5, 6) else ""}"></i>' for r in range(7) for c in range(7))
    return f'''<div class="tent" aria-hidden="true">
  <div class="tent-top">{logo_img(lang, 'light', pre, 34)}</div>
  <div class="qr">{cells}</div>
  <b>{'امسح والعب!' if lang == 'ar' else 'Scan and play!'}</b>
  <span>{'ليلة ولا كلمة · كل خميس' if lang == 'ar' else 'Wala Kelmeh night · every Thursday'}</span>
</div>'''

def partner_form(c):
    from content_cafes import P
    lang, L = c.lang, (lambda k: P[k][c.lang])
    fid = f'pf-{lang}'
    types = ''.join(f'<option>{t_}</option>' for t_ in P['types'][lang])
    return f'''<section class="suggest" id="contact" aria-labelledby="{fid}-h"><div class="in">
  <div class="suggest-card">
    <div class="suggest-head"><div class="suggest-art">{mascot_img('wink', lang, c.pre, w=160)}</div><div><h2 id="{fid}-h">{L('form_h')}</h2><p>{L('form_p')}</p></div></div>
    <form class="sg-form" id="{fid}" data-kind="partner" data-subject="{html.escape('طلب شراكة')}" data-endpoint="{SUGGEST_ENDPOINT}" data-mail="{CONTACT}" novalidate>
      <input type="hidden" name="subject" value="{html.escape('ولا كلمة · طلب شراكة')}">
      <input type="hidden" name="from_name" value="Wala Kelmeh website">
      <input type="hidden" name="kind" value="partner"><input type="hidden" name="lang" value="{lang}">
      <div class="f-grid">
        <div class="f-row"><label for="{fid}-v">{L('venue')}</label><input id="{fid}-v" name="venue" required maxlength="80" placeholder="{L('venue_ph')}" autocomplete="organization"></div>
        <div class="f-row"><label for="{fid}-c">{L('city')}</label><input id="{fid}-c" name="city" maxlength="40" placeholder="{L('city_ph')}" autocomplete="address-level2"></div>
        <div class="f-row"><label for="{fid}-t">{L('type')}</label><select id="{fid}-t" name="type">{types}</select></div>
        <div class="f-row"><label for="{fid}-n">{L('who')}</label><input id="{fid}-n" name="name" maxlength="60" autocomplete="name"></div>
      </div>
      <div class="f-row"><label for="{fid}-p">{L('contact')}</label><input id="{fid}-p" name="contact" required maxlength="80" dir="ltr" placeholder="{L('contact_ph')}" autocomplete="tel" inputmode="tel"></div>
      <div class="f-row"><label for="{fid}-m">{L('msg')}</label><textarea id="{fid}-m" name="message" rows="3" maxlength="800" placeholder="{L('msg_ph')}"></textarea></div>
      <div class="hp" aria-hidden="true"><label>Website<input type="checkbox" name="botcheck" tabindex="-1"></label></div>
      <div class="f-actions"><button class="btn btn-red" type="submit" data-label="{L('send')}" data-busy="{SUGGEST['sending'][lang]}">{L('send')}</button>
        <p class="f-note">{L('privacy')}</p></div>
      <p class="f-status" role="status" aria-live="polite" data-ok="{SUGGEST['thanks'][lang]}" data-err="{SUGGEST['error'][lang]}" data-mail-label="{SUGGEST['by_email'][lang]}"></p>
    </form>
  </div></div></section>'''

def cafes_page(c):
    from content_cafes import P
    lang, pre, L = c.lang, c.pre, (lambda k: P[k][c.lang])
    home_name = 'الرئيسية' if lang == 'ar' else 'Home'
    why = ''.join(f'<li><h3>{h[lang]}</h3><p>{p[lang]}</p></li>' for h, p in P['why'])
    how = ''.join(f'<li><span class="step" aria-hidden="true">{num(i, lang)}</span><h3>{h[lang]}</h3><p>{p[lang]}</p></li>' for i, (h, p) in enumerate(P['how'], 1))
    soon_tag = f'<em>{L("soon")}</em>'
    kit = ''.join(f'<li{" class=soon" if soon else ""}><b>{h[lang]}</b><span>{p[lang]}</span>{soon_tag if soon else ""}</li>' for h, p, soon in P['kit'])
    others = ''.join(f'<li><h3>{h[lang]}</h3><p>{p[lang]}</p></li>' for h, p in P['others'])
    qs = ''.join(f'<details{" open" if i == 0 else ""}><summary><h3>{q[lang]}</h3></summary><p>{a[lang]}</p></details>' for i, (q, a) in enumerate(P['faq']))
    main = f'''<section class="page-hero cafes-hero"><div class="in">
  {crumbs_html(c, [(home_name, 'home'), (L('crumb'), 'cafes')])}
  <div class="page-hero-grid">
    <div class="page-hero-text"><span class="eyebrow gold">{L('eyebrow')}</span><h1>{L('h1')}</h1><p class="answer">{L('answer')}</p>
      <div class="ctas"><a class="btn btn-red" href="#contact">{L('cta')}</a></div></div>
    <div class="page-hero-art cafes-hero-art">{mascot_img('cool', lang, pre, eager=True, w=300)}</div>
  </div></div></section>
<div class="band" aria-hidden="true"></div>
<section class="sec" aria-labelledby="why-h"><div class="in">
  <div class="sec-head"><h2 id="why-h">{L('why_h')}</h2></div><ul class="promise">{why}</ul></div></section>
<section class="sec how" aria-labelledby="how-h"><div class="in">
  <div class="sec-head"><h2 id="how-h">{L('how_h')}</h2></div>
  <div class="how-grid"><ol class="steps">{how}</ol><div class="how-mascot">{table_tent(lang, pre)}</div></div></div></section>
<section class="sec" aria-labelledby="kit-h"><div class="in">
  <div class="kit-grid"><div class="kit-text"><div class="sec-head"><h2 id="kit-h">{L('kit_h')}</h2></div><ul class="kit">{kit}</ul></div>
  <div class="kit-badge">{partner_badge_img(lang, pre)}</div></div></div></section>
<section class="sec related" aria-labelledby="others-h"><div class="in">
  <div class="sec-head"><h2 id="others-h">{L('others_h')}</h2></div><ul class="promise">{others}</ul></div></section>
{partner_form(c)}
<section class="sec" aria-labelledby="pfaq-h"><div class="in narrow">
  <div class="sec-head"><h2 id="pfaq-h">{L('faq_h')}</h2></div><div class="faq">{qs}</div></div></section>'''
    title, desc = L('title'), L('desc')
    service = {'@type': 'Service', '@id': c.url + '#service', 'name': L('h1'), 'description': L('answer'), 'provider': {'@id': SITE + '/#org'},
               'areaServed': {'@type': 'Country', 'name': 'Jordan'}, 'serviceType': 'Game nights for venues and companies'}
    graph = base_graph(c) + [webpage(c, title, desc), breadcrumbs_ld(c, [(home_name, c.abs('home')), (L('crumb'), c.url)]), service, faq_ld(P['faq'], lang)]
    return head(c, title, desc, graph) + header(c) + '<main id="main">' + main + footer(c)

# ---------- stickers ----------
STICKER_SRC = os.path.join(REPO, 'brand', 'mascot', 'stickers')

def stickers_page(c):
    from content_stickers import S
    lang, pre, L = c.lang, c.pre, (lambda k: S[k][c.lang])
    home_name = 'الرئيسية' if lang == 'ar' else 'Home'
    tiles = ''.join(f'''<li class="stile"><figure>{mascot_img(k, lang, pre, w=200)}<figcaption><b lang="ar" dir="rtl">{ar_line}</b><span>{en}</span></figcaption></figure>
      <a class="dl" href="{pre}assets/stickers/shammogh-{k}.png" download>{L('download')}<span class="sr"> {en}</span></a></li>''' for k, (ar_line, en, _) in MOODS.items())
    add = ''.join(f'<div class="add-card"><h3>{dev[lang]}</h3><ol class="rule-steps">{"".join(f"<li>{st[lang]}</li>" for st in steps)}</ol></div>' for dev, steps in S['add'])
    rules = ''.join(f'<li class="{"ok" if i < 2 else "no"}">{r[lang]}</li>' for i, r in enumerate(S['rules']))
    qs = ''.join(f'<details{" open" if i == 0 else ""}><summary><h3>{q[lang]}</h3></summary><p>{a[lang]}</p></details>' for i, (q, a) in enumerate(S['faq']))
    main = f'''<section class="page-hero"><div class="in">
  {crumbs_html(c, [(home_name, 'home'), (L('crumb'), 'stickers')])}
  <div class="page-hero-grid">
    <div class="page-hero-text"><span class="eyebrow">{num(len(MOODS), lang)} {'ستيكر' if lang == 'ar' else 'stickers'}</span><h1>{L('h1')}</h1><p class="answer">{L('answer')}</p>
      <div class="ctas"><a class="btn btn-red" href="{pre}assets/stickers/shammogh-stickers.zip" download>{L('download_all')}</a><a class="btn btn-ghost" href="#add">{L('add_h')}</a></div></div>
    <div class="page-hero-art">{mascot_img('wave', lang, pre, eager=True, w=300)}</div>
  </div></div></section>
<div class="band" aria-hidden="true"></div>
<section class="sec" aria-labelledby="gal-h"><div class="in">
  <div class="sec-head"><h2 id="gal-h">{L('gallery_h')}</h2><p>{L('gallery_p')}</p></div>
  <ul class="sgallery">{tiles}</ul></div></section>
<section class="sec how" id="add" aria-labelledby="add-h"><div class="in">
  <div class="sec-head"><h2 id="add-h">{L('add_h')}</h2></div><div class="add-grid">{add}</div></div></section>
<section class="sec" aria-labelledby="who-h"><div class="in">
  <div class="kit-grid"><div class="sec-head"><h2 id="who-h">{L('who_h')}</h2><p>{L('who')}</p></div>
  <div class="kit-badge">{mascot_img('shh', lang, pre, w=240)}</div></div></div></section>
<section class="sec related" aria-labelledby="use-h"><div class="in narrow">
  <div class="sec-head"><h2 id="use-h">{L('rules_h')}</h2></div><ul class="use-rules">{rules}</ul></div></section>
<section class="sec" aria-labelledby="sfaq-h"><div class="in narrow">
  <div class="sec-head"><h2 id="sfaq-h">{L('faq_h')}</h2></div><div class="faq">{qs}</div></div></section>
{cta_band(c, L('cta_h'), 'card')}'''
    title, desc = L('title'), L('desc')
    gallery = {'@type': 'ImageGallery', 'name': L('h1'), 'description': L('answer'), 'associatedMedia': [
        {'@type': 'ImageObject', 'name': f'Shammogh: {en}', 'caption': ar_line, 'contentUrl': f'{SITE}/assets/stickers/shammogh-{k}.png',
         'width': 512, 'height': 512, 'creator': {'@id': SITE + '/#org'}, 'copyrightHolder': {'@id': SITE + '/#org'},
         'license': c.url + '#use', 'acquireLicensePage': c.abs('cafes')} for k, (ar_line, en, _) in MOODS.items()]}
    graph = base_graph(c) + [webpage(c, title, desc), breadcrumbs_ld(c, [(home_name, c.abs('home')), (L('crumb'), c.url)]), gallery, faq_ld(S['faq'], lang)]
    return head(c, title, desc, graph) + header(c) + '<main id="main">' + main + footer(c)

# ---------- privacy ----------
def privacy_page(c):
    from content_privacy import PR
    lang, L = c.lang, (lambda k: PR[k][c.lang])
    home_name = 'الرئيسية' if lang == 'ar' else 'Home'
    toc = ''.join(f'<li><a href="#{k}">{h[lang]}</a></li>' for k, h, _ in PR['sections'])
    # English names inside Arabic sentences get their own direction, or the letters scramble
    iso = (lambda x: re.sub(r'([A-Za-z][A-Za-z0-9]*(?: [A-Za-z][A-Za-z0-9]*)*)', r'<bdi>\1</bdi>', x)) if lang == 'ar' else (lambda x: x)
    body = ''.join(f'<section class="rule-block" id="{k}" aria-labelledby="{k}-h"><h2 id="{k}-h">{h[lang]}</h2><ul class="plain">{"".join(f"<li>{iso(p[lang])}</li>" for p in ps)}</ul></section>'
                   for k, h, ps in PR['sections'])
    main = f'''<section class="page-hero"><div class="in">
  {crumbs_html(c, [(home_name, 'home'), (L('crumb'), 'privacy')])}
  <div class="page-hero-text"><h1>{L('h1')}</h1><p class="updated">{L('updated')}</p><p class="answer">{L('short')}</p></div></div></section>
<div class="band" aria-hidden="true"></div>
<div class="in doc">
  <aside class="toc" aria-label="{'محتويات الصفحة' if lang == 'ar' else 'On this page'}"><h2>{'بهاي الصفحة' if lang == 'ar' else 'On this page'}</h2><ol>{toc}</ol></aside>
  <div class="doc-body">{body}
    <section class="rule-block" id="contact"><h2>{L('contact_h')}</h2><p>{L('contact_p')} <span class="sel" dir="ltr">{CONTACT}</span></p></section>
  </div>
</div>'''
    title, desc = L('title'), L('desc')
    page = webpage(c, title, desc)
    graph = base_graph(c) + [page, breadcrumbs_ld(c, [(home_name, c.abs('home')), (L('crumb'), c.url)])]
    return head(c, title, desc, graph) + header(c) + '<main id="main">' + main + footer(c)

# ---------- blog ----------
import math
MONTHS_AR = ['كانون الثاني', 'شباط', 'آذار', 'نيسان', 'أيار', 'حزيران', 'تموز', 'آب', 'أيلول', 'تشرين الأول', 'تشرين الثاني', 'كانون الأول']
MONTHS_EN = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
def nice_date(iso, lang):
    y, m, d = map(int, iso.split('-'))
    return f'{ar_digits(d)} {MONTHS_AR[m - 1]} {ar_digits(y)}' if lang == 'ar' else f'{d} {MONTHS_EN[m - 1]} {y}'

def post_words(p, lang):
    return sum(len((x[lang] if isinstance(x, dict) else ' '.join(i[lang] for i in x)).split()) for _, x in p['body'])

def read_time(p, lang):
    n = max(1, math.ceil(post_words(p, lang) / 180))
    if lang == 'ar' and n <= 2:
        return 'دقيقة قراءة' if n == 1 else 'دقيقتين قراءة'
    return CB.B['minutes'][lang].format(n=num(n, lang))

def post_card(c, p):
    lang = c.lang
    return f'''<li><a class="post-card" href={c.href('post-' + p['slug'])}>
      <span class="post-art">{mascot_img(p['mood'], lang, c.pre, w=160)}</span>
      <span class="post-meta"><time datetime="{p['date']}">{nice_date(p['date'], lang)}</time> · {read_time(p, lang)}</span>
      <b>{p['title'][lang]}</b><span class="post-ex">{p['excerpt'][lang]}</span><span class="more">{CB.B['read'][lang]}</span></a></li>'''

def blog_index(c):
    lang, L = c.lang, (lambda k: CB.B[k][c.lang])
    home_name = 'الرئيسية' if lang == 'ar' else 'Home'
    posts = sorted(CB.POSTS, key=lambda p: p['date'], reverse=True)
    main = f'''<section class="page-hero"><div class="in">
  {crumbs_html(c, [(home_name, 'home'), (L('crumb'), 'blog')])}
  <div class="page-hero-grid"><div class="page-hero-text"><h1>{L('h1')}</h1><p class="answer">{L('intro')}</p></div>
  <div class="page-hero-art">{mascot_img('think', lang, c.pre, eager=True, w=260)}</div></div></div></section>
<div class="band" aria-hidden="true"></div>
<section class="sec"><div class="in"><ul class="posts">{''.join(post_card(c, p) for p in posts)}</ul></div></section>'''
    title, desc = L('title'), L('desc')
    blog = {'@type': 'Blog', '@id': c.url + '#blog', 'name': L('h1'), 'description': desc, 'inLanguage': lang, 'publisher': {'@id': SITE + '/#org'},
            'blogPost': [{'@type': 'BlogPosting', 'headline': p['title'][lang], 'url': c.abs('post-' + p['slug']), 'datePublished': p['date']} for p in posts]}
    graph = base_graph(c) + [webpage(c, title, desc), breadcrumbs_ld(c, [(home_name, c.abs('home')), (L('crumb'), c.url)]), blog]
    return head(c, title, desc, graph) + header(c) + '<main id="main">' + main + footer(c)

def render_block(kind, x, lang, idx):
    if kind == 'p': return f'<p>{x[lang]}</p>'
    if kind == 'h2': return f'<h2 id="s{idx}">{x[lang]}</h2>'
    if kind == 'tip': return f'<aside class="tip"><p>{x[lang]}</p></aside>'
    tag = 'ol' if kind == 'ol' else 'ul'
    return f'<{tag}>' + ''.join(f'<li>{i[lang]}</li>' for i in x) + f'</{tag}>'

def post_page(p):
    def render(c):
        lang, L = c.lang, (lambda k: CB.B[k][c.lang])
        home_name = 'الرئيسية' if lang == 'ar' else 'Home'
        body = ''.join(render_block(k, x, lang, i) for i, (k, x) in enumerate(p['body']))
        toc = ''.join(f'<li><a href="#s{i}">{x[lang]}</a></li>' for i, (k, x) in enumerate(p['body']) if k == 'h2')
        others = [o for o in CB.POSTS if o['slug'] != p['slug']]
        main = f'''<article class="post">
<section class="page-hero"><div class="in">
  {crumbs_html(c, [(home_name, 'home'), (L('crumb'), 'blog'), (p['title'][lang], 'post-' + p['slug'])])}
  <div class="page-hero-grid"><div class="page-hero-text"><h1>{p['title'][lang]}</h1>
    <p class="post-byline"><span>{L('author')}</span> · <time datetime="{p['date']}">{nice_date(p['date'], lang)}</time> · {read_time(p, lang)}</p>
    <p class="answer">{p['desc'][lang]}</p></div>
  <div class="page-hero-art">{mascot_img(p['mood'], lang, c.pre, eager=True, w=260)}</div></div></div></section>
<div class="band" aria-hidden="true"></div>
<div class="in doc">
  <aside class="toc" aria-label="{L('contents')}"><h2>{L('contents')}</h2><ul class="toc-plain">{toc}</ul></aside>
  <div class="doc-body post-body">{body}</div>
</div>
</article>
<section class="sec related" aria-labelledby="more-h"><div class="in">
  <div class="sec-head"><h2 id="more-h">{L('more_h')}</h2></div><ul class="posts">{''.join(post_card(c, o) for o in others)}</ul></div></section>
{cta_band(c, L('cta_h'), 'card')}'''
        title = p['title'][lang] + (' | ولا كلمة' if lang == 'ar' else ' | Wala Kelmeh')
        if len(title) > 70: title = p['title'][lang]
        desc = p['desc'][lang]
        posting = {'@type': 'BlogPosting', '@id': c.url + '#post', 'headline': p['title'][lang], 'description': desc, 'inLanguage': lang,
                   'datePublished': p['date'], 'dateModified': p['date'], 'wordCount': post_words(p, lang),
                   'author': {'@type': 'Organization', 'name': L('author'), '@id': SITE + '/#org'}, 'publisher': {'@id': SITE + '/#org'},
                   'image': SITE + f'/assets/og-{lang}.png', 'mainEntityOfPage': c.url, 'isPartOf': {'@id': c.abs('blog') + '#blog'}}
        graph = base_graph(c) + [webpage(c, title, desc), breadcrumbs_ld(c, [(home_name, c.abs('home')), (L('crumb'), c.abs('blog')), (p['title'][lang], c.url)]), posting]
        h = head(c, title, desc, graph).replace('<meta property="og:type" content="website">', f'<meta property="og:type" content="article">\n<meta property="article:published_time" content="{p["date"]}">')
        return h + header(c) + '<main id="main">' + main + footer(c)
    return render

BUILT = {'home': home, 'how': how_page, 'categories': categories_page, 'cafes': cafes_page, 'stickers': stickers_page, 'privacy': privacy_page, 'blog': blog_index}
BUILT.update({f'post-{p["slug"]}': post_page(p) for p in CB.POSTS})
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
    blog = '\n'.join(f'- [{p["title"]["en"]}]({SITE}/en/blog/{p["slug"]}/): {p["desc"]["en"]}' for p in CB.POSTS)
    return f'''# ولا كلمة — Wala Kelmeh

> {T['about_p']['en']}

- Website: {SITE}/ (Arabic), {SITE}/en/ (English)
- How to play: {SITE}/en/how-to-play/
- Play: {SITE}/play/
- Price: free. No account. Works offline after install. No ads during play.
- Players: 2 to 12. Teams: 2 to 4, or none. Turns: 30, 60 or 90 seconds. Rounds: 1 to 10.
- Modes: classic charades (تمثيل), heads up (عالجبين), who's fastest (مين أسرع؟)
- Made in Amman, Jordan, 2026. Contact: {CONTACT}
- Instagram: {SOCIAL['Instagram']}

## How to play
{H['answer']['en']}

{rules}

## Categories ({TOTAL_CARDS} cards)
{cats}

## Blog
{blog}

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
    write(os.path.join(OUT, 'privacy.html'), f'<!doctype html><meta charset="utf-8"><title>Privacy</title><link rel="canonical" href="{SITE}/privacy/"><meta name="robots" content="noindex"><meta http-equiv="refresh" content="0; url=privacy/"><a href="privacy/">سياسة الخصوصية · Privacy policy</a>')
    write(os.path.join(OUT, 'robots.txt'), robots())
    write(os.path.join(OUT, 'sitemap.xml'), sitemap())
    write(os.path.join(OUT, 'llms.txt'), llms())
    for name, svg in ART_FILES.items():
        write(os.path.join(OUT, 'assets', 'art', name), svg)
    for name, svg in list(LOGO_FILES.items()) + list(PARTNER_FILES.items()):
        write(os.path.join(OUT, 'assets', name), svg)
    for k in MASCOT_FILES:
        write(os.path.join(OUT, 'assets', f'shammogh-{k}.svg'), msvg(MOODS[k][2](f'a{k}'), MASCOT_VB))
    shutil.copy(os.path.join(REPO, 'brand', 'logo', 'symbol', 'symbol-small.svg'), os.path.join(OUT, 'assets', 'icon.svg'))
    import zipfile
    sdir = os.path.join(OUT, 'assets', 'stickers'); os.makedirs(sdir, exist_ok=True)
    with zipfile.ZipFile(os.path.join(sdir, 'shammogh-stickers.zip'), 'w', zipfile.ZIP_DEFLATED) as z:
        for k in MOODS:
            shutil.copy(os.path.join(STICKER_SRC, f'{k}.png'), os.path.join(sdir, f'shammogh-{k}.png'))
            z.write(os.path.join(STICKER_SRC, f'{k}.png'), f'shammogh-{k}.png')
            z.write(os.path.join(STICKER_SRC, f'{k}.webp'), f'webp/shammogh-{k}.webp')
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
        s = re.sub(r'<img src="(?:\.\./)*assets/(partner-badge-\w+\.svg)"[^>]*?alt="([^"]*)"[^>]*>',
                   lambda m: PARTNER_FILES[m.group(1)].replace('<svg ', f'<svg role="img" aria-label="{m.group(2)}" class="pv-img" ', 1), s)
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
           '<script>window.__PREVIEW__ = true;</script>' + f'{note}{views}{script}')
    write(os.path.join(OUT, 'preview.html'), doc)
    print('preview bundle written')

if __name__ == '__main__':
    build()
    if PREVIEW:
        preview_bundle()
