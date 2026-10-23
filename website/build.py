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

# ---------- structured data ----------
def jsonld(lang):
    url = SITE + ('/' if lang == 'ar' else '/en/')
    org = {'@type': 'Organization', '@id': SITE + '/#org', 'name': 'ولا كلمة', 'alternateName': ['Wala Kelmeh', 'Wala Kilmeh', 'Not a Word'],
           'url': SITE + '/', 'logo': SITE + '/assets/logo-512.png', 'email': CONTACT,
           'foundingLocation': {'@type': 'Place', 'name': 'Amman, Jordan'}}
    site = {'@type': 'WebSite', '@id': SITE + '/#site', 'url': SITE + '/', 'name': 'ولا كلمة — Wala Kelmeh',
            'inLanguage': ['ar', 'en'], 'publisher': {'@id': SITE + '/#org'}}
    app = {'@type': ['SoftwareApplication', 'VideoGame'], '@id': SITE + '/#game', 'name': 'ولا كلمة — Wala Kelmeh',
           'alternateName': 'Wala Kelmeh', 'description': t('about_p', lang), 'url': url,
           'applicationCategory': 'GameApplication', 'genre': ['Party game', 'Charades', 'Word game'],
           'operatingSystem': 'Web, Android', 'inLanguage': 'ar', 'playMode': 'MultiPlayer',
           'numberOfPlayers': {'@type': 'QuantitativeValue', 'minValue': 2, 'maxValue': 12},
           'gamePlatform': ['Web browser', 'Android'], 'countryOfOrigin': 'JO', 'datePublished': '2026-10',
           'image': SITE + f'/assets/og-{lang}.png', 'publisher': {'@id': SITE + '/#org'},
           'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'JOD', 'availability': 'https://schema.org/InStock'}}
    cats = {'@type': 'ItemList', 'name': t('cats_h', lang), 'numberOfItems': len(CATEGORIES), 'itemListElement': [
        {'@type': 'ListItem', 'position': i, 'name': ar if lang == 'ar' else en, 'url': f'{url}categories/{cid}/'}
        for i, (cid, ar, en, n) in enumerate(CATEGORIES, 1)]}
    howto = {'@type': 'HowTo', 'name': t('how_h', lang), 'step': [
        {'@type': 'HowToStep', 'position': i, 'name': h[lang], 'text': p[lang]} for i, (h, p) in enumerate(T['how'], 1)]}
    faq = {'@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q[lang], 'acceptedAnswer': {'@type': 'Answer', 'text': a[lang]}} for q, a in T['faq']]}
    page = {'@type': 'WebPage', '@id': url + '#page', 'url': url, 'name': t('meta_title', lang), 'description': t('meta_desc', lang),
            'inLanguage': lang, 'isPartOf': {'@id': SITE + '/#site'}, 'about': {'@id': SITE + '/#game'}, 'dateModified': UPDATED,
            'primaryImageOfPage': SITE + f'/assets/og-{lang}.png'}
    return json.dumps({'@context': 'https://schema.org', '@graph': [org, site, page, app, cats, howto, faq]}, ensure_ascii=False)

# ---------- page parts ----------
def head(lang):
    url = SITE + ('/' if lang == 'ar' else '/en/')
    pre = '' if lang == 'ar' else '../'
    desc = html.escape(t('meta_desc', lang))
    return f'''<!doctype html>
<html lang="{lang}" dir="{'rtl' if lang == 'ar' else 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t('meta_title', lang)}</title>
<meta name="description" content="{desc}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="ar" href="{SITE}/">
<link rel="alternate" hreflang="en" href="{SITE}/en/">
<link rel="alternate" hreflang="x-default" href="{SITE}/">
<meta property="og:site_name" content="ولا كلمة — Wala Kelmeh">
<meta property="og:type" content="website">
<meta property="og:title" content="{t('meta_title', lang)}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-{lang}.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{html.escape(t('og_alt', lang))}">
<meta property="og:locale" content="{'ar_JO' if lang == 'ar' else 'en_US'}">
<meta property="og:locale:alternate" content="{'en_US' if lang == 'ar' else 'ar_JO'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{t('meta_title', lang)}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{SITE}/assets/og-{lang}.png">
<meta name="theme-color" content="#b5121b">
<link rel="icon" href="{pre}assets/icon.svg" type="image/svg+xml">
<link rel="icon" href="{pre}assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="{pre}assets/apple-touch-icon.png">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Almarai:wght@700;800&family=Cairo:wght@400;600;800&display=swap">
<script type="application/ld+json">{jsonld(lang)}</script>
<style>{CSS}</style>
</head>
<body>'''

def header(lang):
    other = 'en' if lang == 'ar' else 'ar'
    nav = ''.join(f'<a href="{h}">{T["nav"][k][lang]}</a>' for k, h in (('how', '#how'), ('categories', '#categories'), ('cafes', '#cafes'), ('stickers', '#stickers')))
    return f'''<a class="skip" href="#main">{t('skip', lang)}</a>
<header class="top">
  <div class="in">
    <a class="brand" href="./" aria-label="{'ولا كلمة، الصفحة الرئيسية' if lang == 'ar' else 'Wala Kelmeh home'}">{logo_pair(lang, '' if lang == 'ar' else '../')}</a>
    <nav class="menu" aria-label="{'القائمة الرئيسية' if lang == 'ar' else 'Main'}">{nav}</nav>
    <div class="actions">
      <a class="lang" href="{'en/' if lang == 'ar' else '../'}" hreflang="{other}" lang="{other}">{t('lang_switch', lang)}</a>
      <a class="btn btn-red btn-sm" href="{PLAY}">{t('play', lang)}</a>
    </div>
  </div>
</header>'''

def phone():
    return '''<div class="phone" aria-hidden="true" dir="rtl">
  <div class="ph-bar"><span class="chip">🍽️ أكل وشرب</span><span class="timer">0:42</span></div>
  <div class="ph-card"><b>منسف</b><span dir="ltr">mansaf</span></div>
  <div class="ph-btns"><span class="ph-ok">صح ✓</span><span class="ph-skip">عدّيها</span></div>
  <div class="ph-score"><span>فريق الصقر</span><b>٧</b></div>
</div>'''

def hero(lang, pre):
    facts = ''.join(f'<li>{f}</li>' for f in t('hero_facts', lang))
    stores = ''.join(f'<span class="store"><small>{t("stores_soon", lang)}</small><b dir="ltr">{n}</b></span>' for n in ('Google Play', 'AppGallery', 'Galaxy Store'))
    return f'''<section class="hero" aria-labelledby="hero-h">
  <div class="in">
    <div class="hero-text">
      <span class="eyebrow">{t('hero_eyebrow', lang)}</span>
      <h1 id="hero-h">{t('hero_h1', lang)}</h1>
      <p class="lead">{t('hero_sub', lang)}</p>
      <div class="ctas"><a class="btn btn-red" href="{PLAY}">{t('play', lang)}</a><a class="btn btn-ghost" href="#faq-install">{t('install', lang)}</a></div>
      <ul class="facts">{facts}</ul>
      <div class="stores">{stores}</div>
    </div>
    <div class="hero-art">{phone()}<div class="hero-mascot">{mascot_img('card', lang, pre, eager=True)}</div></div>
  </div>
</section>
<div class="band" aria-hidden="true"></div>'''

def about(lang):
    dl = ''.join(f'<div><dt>{k[lang]}</dt><dd>{v[lang]}</dd></div>' for k, v in T['facts'])
    return f'''<section class="sec about" id="about" aria-labelledby="about-h"><div class="in">
  <div class="about-grid"><div class="sec-head"><h2 id="about-h">{t('about_h', lang)}</h2><p>{t('about_p', lang)}</p></div>
  <dl class="facts-dl">{dl}</dl></div></div></section>'''

def modes(lang, pre):
    cards = ''.join(f'''<article class="mode">
      <div class="mode-art">{art_img('mode', k, MODE_ART[k], (('رسمة تطريز: ' if lang == 'ar' else 'Cross-stitch: ') + name[lang]), pre, 70)}</div>
      <h3>{name[lang]}</h3><p>{desc[lang]}</p><span class="tag">{who[lang]}</span></article>''' for k, name, desc, who in T['modes'])
    return f'''<section class="sec" id="modes" aria-labelledby="modes-h"><div class="in">
  <div class="sec-head"><h2 id="modes-h">{t('modes_h', lang)}</h2><p>{t('modes_p', lang)}</p></div>
  <div class="modes">{cards}</div></div></section>'''

def categories(lang, pre):
    tiles = ''.join(f'''<li><a class="cat" href="categories/{cid}/">
      <span class="cat-art">{art_img('cat', cid, CAT_ART[cid], (('رسمة تطريز لفئة ' + ar) if lang == 'ar' else ('Cross-stitch art for ' + en)), pre, 62)}</span>
      <b>{ar if lang == 'ar' else en}</b><small>{num(n, lang)} {t('cards_word', lang)}</small></a></li>''' for cid, ar, en, n in CATEGORIES)
    h = t('cats_h', lang)
    return f'''<section class="sec" id="categories" aria-labelledby="cats-h"><div class="in">
  <div class="sec-head"><h2 id="cats-h">{ar_digits(h) if lang == 'ar' else h}</h2><p>{t('cats_p', lang)}</p></div>
  <ul class="cats">{tiles}</ul></div></section>'''

def how(lang, pre):
    steps = ''.join(f'<li><span class="step" aria-hidden="true">{num(i, lang)}</span><h3>{h[lang]}</h3><p>{p[lang]}</p></li>' for i, (h, p) in enumerate(T['how'], 1))
    return f'''<section class="sec how" id="how" aria-labelledby="how-h"><div class="in">
  <div class="sec-head"><h2 id="how-h">{t('how_h', lang)}</h2></div>
  <div class="how-grid"><ol class="steps">{steps}</ol><div class="how-mascot">{mascot_img('shh', lang, pre)}</div></div></div></section>'''

def promise(lang):
    items = ''.join(f'<li><h3>{h[lang]}</h3><p>{p[lang]}</p></li>' for h, p in T['promise'])
    return f'''<section class="sec" id="promise" aria-labelledby="promise-h"><div class="in">
  <div class="sec-head"><h2 id="promise-h">{t('promise_h', lang)}</h2></div>
  <ul class="promise">{items}</ul></div></section>'''

def cafes(lang, pre):
    return f'''<section class="cafes" id="cafes" aria-labelledby="cafes-h"><div class="in">
  <div class="cafes-text"><span class="eyebrow gold">{t('cafes_eyebrow', lang)}</span><h2 id="cafes-h">{t('cafes_h', lang)}</h2><p>{t('cafes_p', lang)}</p>
    <div class="ctas"><a class="btn btn-red" href="mailto:{CONTACT}?subject=Wala%20Kelmeh%20night">{t('cafes_cta', lang)}</a><span class="mail" dir="ltr">{CONTACT}</span></div></div>
  <div class="cafes-art">{mascot_img('cool', lang, pre)}</div></div></section>'''

def stickers(lang, pre):
    row = ''.join(f'<li class="stk">{mascot_img(k, lang, pre, w=200)}</li>' for k in ('wave', 'laugh', 'yay', 'love', 'shock', 'proud'))
    return f'''<section class="sec" id="stickers" aria-labelledby="stk-h"><div class="in">
  <div class="sec-head"><h2 id="stk-h">{t('stickers_h', lang)}</h2><p>{t('stickers_p', lang)}</p></div>
  <ul class="stickers">{row}</ul>
  <a class="btn btn-ghost" href="stickers/">{t('stickers_cta', lang)}</a></div></section>'''

def faq(lang):
    qs = ''.join(f'<details{" id=faq-install" if i == 1 else ""}{" open" if i == 0 else ""}><summary><h3>{q[lang]}</h3></summary><p>{a[lang]}</p></details>' for i, (q, a) in enumerate(T['faq']))
    return f'''<section class="sec" id="faq" aria-labelledby="faq-h"><div class="in narrow">
  <div class="sec-head"><h2 id="faq-h">{t('faq_h', lang)}</h2></div>
  <div class="faq">{qs}</div></div></section>'''

def footer(lang, pre):
    links = [(T['nav']['how'][lang], 'how-to-play/'), (T['nav']['categories'][lang], 'categories/'), (T['nav']['cafes'][lang], 'cafes/'),
             (T['nav']['stickers'][lang], 'stickers/'), (t('privacy', lang), f'{pre}privacy.html'), (t('contact', lang), f'mailto:{CONTACT}')]
    nav = ''.join(f'<a href="{h}">{n}</a>' for n, h in links)
    return f'''</main>
<div class="band" aria-hidden="true"></div>
<footer class="foot"><div class="in">
  <div class="foot-brand">{logo_img(lang, 'dark', pre, 54)}<p>{t('footer_tag', lang)}</p></div>
  <nav class="foot-links" aria-label="{'روابط' if lang == 'ar' else 'Footer'}">{nav}</nav>
  <p class="rights">{t('rights', lang)}</p>
</div></footer>
</body>
</html>'''

def page(lang):
    pre = '' if lang == 'ar' else '../'
    return (head(lang) + header(lang) + '<main id="main">' + hero(lang, pre) + about(lang) + modes(lang, pre) + categories(lang, pre)
            + how(lang, pre) + promise(lang) + cafes(lang, pre) + stickers(lang, pre) + faq(lang) + footer(lang, pre))

# ---------- site files ----------
def robots():
    return f'User-agent: *\nAllow: /\n\nSitemap: {SITE}/sitemap.xml\n'

def sitemap():
    pairs = [('/', '/en/')]
    urls = ''
    for ar, en in pairs:
        for loc in (ar, en):
            urls += (f'  <url>\n    <loc>{SITE}{loc}</loc>\n    <lastmod>{UPDATED}</lastmod>\n'
                     f'    <xhtml:link rel="alternate" hreflang="ar" href="{SITE}{ar}"/>\n'
                     f'    <xhtml:link rel="alternate" hreflang="en" href="{SITE}{en}"/>\n'
                     f'    <xhtml:link rel="alternate" hreflang="x-default" href="{SITE}{ar}"/>\n  </url>\n')
    return ('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
            'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + urls + '</urlset>\n')

def llms():
    """Plain-language summary for AI answer engines (llms.txt convention)."""
    cats = '\n'.join(f'- {ar} ({en}): {n} cards' for cid, ar, en, n in CATEGORIES)
    faq = '\n'.join(f'**{q["en"]}** {a["en"]}' for q, a in T['faq'])
    return f'''# ولا كلمة — Wala Kelmeh

> {T['about_p']['en']}

- Website: {SITE}/ (Arabic), {SITE}/en/ (English)
- Play: {SITE}/play/
- Price: free. No account. Works offline after install. No ads during play.
- Players: 2 to 12. Modes: classic charades (تمثيل), heads up (عالجبين), who's fastest (مين أسرع؟)
- Made in Amman, Jordan, 2026. Contact: {CONTACT}

## Categories ({TOTAL_CARDS} cards)
{cats}

## FAQ
{faq}
'''

def build():
    os.makedirs(os.path.join(OUT, 'en'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page('ar'))
    open(os.path.join(OUT, 'en', 'index.html'), 'w', encoding='utf-8').write(page('en'))
    open(os.path.join(OUT, 'robots.txt'), 'w').write(robots())
    open(os.path.join(OUT, 'sitemap.xml'), 'w').write(sitemap())
    open(os.path.join(OUT, 'llms.txt'), 'w', encoding='utf-8').write(llms())
    os.makedirs(os.path.join(OUT, 'assets', 'art'), exist_ok=True)
    for name, svg in ART_FILES.items():
        open(os.path.join(OUT, 'assets', 'art', name), 'w').write(svg)
    for name, svg in LOGO_FILES.items():
        open(os.path.join(OUT, 'assets', name), 'w').write(svg)
    for k in MASCOT_FILES:
        open(os.path.join(OUT, 'assets', f'shammogh-{k}.svg'), 'w').write(msvg(MOODS[k][2](f'a{k}'), MASCOT_VB))
    shutil.copy(os.path.join(REPO, 'brand', 'logo', 'symbol', 'symbol-small.svg'), os.path.join(OUT, 'assets', 'icon.svg'))
    if os.path.isdir(STATIC):
        shutil.copytree(STATIC, OUT, dirs_exist_ok=True)
    print('built', OUT, '(preview)' if PREVIEW else '')

def preview_bundle():
    """One-file review link: both languages, images inlined, the language switch toggles."""
    def body(lang):
        s = page(lang)
        s = s[s.index('<body>') + 6:s.index('</body>')]
        def inline(m):
            key = m.group(1)
            svg = msvg(MOODS[key][2](uid('p')), MASCOT_VB)
            return svg.replace('<svg ', f'<svg role="img" aria-label="{html.escape(m.group(2))}" class="pv-img" ', 1)
        s = re.sub(r'<img src="(?:\.\./)?assets/shammogh-(\w+)\.svg"[^>]*?alt="([^"]*)"[^>]*>', inline, s)
        def inline_art(m):
            return ART_FILES[m.group(1)].replace('<svg ', f'<svg role="img" aria-label="{m.group(2)}" class="pv-img" ', 1)
        s = re.sub(r'<img src="(?:\.\./)?assets/art/([\w-]+\.svg)"[^>]*?alt="([^"]*)"[^>]*>', inline_art, s)
        return re.sub(r'<img src="(?:\.\./)?assets/(logo-[\w-]+\.svg)"[^>]*?alt="([^"]*)"[^>]*>', lambda m: LOGO_FILES[m.group(1)].replace('<svg ', '<svg class="pv-logo" ', 1), s)
    script = '''<script>
document.addEventListener('click', function (e) {
  var a = e.target.closest('a.lang');
  if (!a) return;
  e.preventDefault();
  var ar = document.getElementById('v-ar'), en = document.getElementById('v-en'), toEn = !ar.hidden;
  ar.hidden = toEn; en.hidden = !toEn; window.scrollTo(0, 0);
});
</script>'''
    note = ('<p class="pv-note">Preview · نسخة تجريبية · links to other pages work once they’re built</p>')
    doc = (f'<title>Wala Kelmeh Website</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
           '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
           '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Almarai:wght@700;800&family=Cairo:wght@400;600;800&display=swap">\n'
           f'<style>{CSS}\n.pv-img{{width:100%;height:auto;display:block}}.mode-art .pv-img{{width:70px}}.cat-art .pv-img{{width:62px}}.pv-note{{margin:0;padding:8px 16px;background:#2a1f1a;color:#f4ecdd;font:600 13px Cairo,sans-serif;text-align:center}}</style>\n'
           f'{note}<div id="v-ar" lang="ar" dir="rtl">{body("ar")}</div><div id="v-en" lang="en" dir="ltr" hidden>{body("en")}</div>{script}')
    open(os.path.join(OUT, 'preview.html'), 'w', encoding='utf-8').write(doc)
    print('preview bundle written')

if __name__ == '__main__':
    build()
    if PREVIEW:
        preview_bundle()
