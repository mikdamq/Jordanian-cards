"""Builds the Wala Kelmeh website: Arabic at /, English at /en/.

    python3 build.py            # production links (game at /play/)
    python3 build.py --preview  # links point at the live game on GitHub Pages
"""
import json, os, re, sys, html
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, '..')
sys.path.insert(0, os.path.join(REPO, 'brand', 'tools'))

from content import T, CATEGORIES, SITE, CONTACT, TOTAL_CARDS
from logos import icon_C, xstitch, svg as raw_svg
from lockups2 import horiz_ar, horiz_en
from final import BR, CREAM, INK, RED
from poses4 import P as MOODS, svg as msvg

PREVIEW = '--preview' in sys.argv
PLAY = 'https://mikdamq.github.io/Jordanian-cards/' if PREVIEW else '/play/'
OUT = os.path.join(HERE, 'out')
MASCOT_VB = '-24 -34 470 454'

# ---------- assets ----------
_n = [0]
def uid(p):
    _n[0] += 1
    return f'{p}{_n[0]}'

def mascot(key, label):
    return msvg(MOODS[key][2](uid('m')), MASCOT_VB).replace('<svg ', f'<svg role="img" aria-label="{label}" ', 1)

def lockup(lang, dark=False):
    p = icon_C('red', uid('g'))
    s = (horiz_ar(p, CREAM, BR) if dark else horiz_ar(p)) if lang == 'ar' else (horiz_en(p, CREAM) if dark else horiz_en(p))
    return s.replace('<svg ', f'<svg role="img" aria-label="{"ولا كلمة" if lang == "ar" else "Wala Kelmeh"}" ', 1)

ART_SRC = open(os.path.join(REPO, 'src', 'art.ts'), encoding='utf-8').read()
def art_block(name):
    start = ART_SRC.index(f'export const {name}')
    return ART_SRC[start:ART_SRC.index('\n};', start)]
def parse_art(name):
    return {m.group(1): re.findall(r"'([^']*)'", m.group(2)) for m in re.finditer(r"\n\s*(\w+):\s*\[(.*?)\]", art_block(name), re.S)}
CAT_ART, MODE_ART = parse_art('CATEGORY_ART'), parse_art('MODE_ART')
TH = {'r': '#b5121b', 'g': '#4f6b2c', 'y': '#c9962a', 'k': '#2a1f1a', 'b': '#3b3f7a'}
def stitch(rows, label, cell=12):
    w, h = max(len(r) for r in rows) * cell, len(rows) * cell
    body = ''.join(xstitch(c * cell + cell / 2, r * cell + cell / 2, cell * .8, TH[v], cell * .28)
                   for r, row in enumerate(rows) for c, v in enumerate(row) if v in TH)
    return raw_svg(w, h, body).replace('<svg ', f'<svg role="img" aria-label="{html.escape(label)}" ', 1)

# ---------- page ----------
def t(key, lang):
    v = T[key]
    return v[lang] if isinstance(v, dict) else v

CSS = open(os.path.join(HERE, 'site.css'), encoding='utf-8').read()

def head(lang):
    other = 'en' if lang == 'ar' else 'ar'
    url = SITE + ('/' if lang == 'ar' else '/en/')
    ld_app = {
        '@context': 'https://schema.org', '@type': 'SoftwareApplication',
        'name': 'ولا كلمة — Wala Kelmeh', 'applicationCategory': 'GameApplication', 'operatingSystem': 'Android, iOS, Web',
        'inLanguage': ['ar', 'en'], 'description': t('meta_desc', lang), 'url': url,
        'offers': {'@type': 'Offer', 'price': '0', 'priceCurrency': 'USD'},
    }
    ld_faq = {'@context': 'https://schema.org', '@type': 'FAQPage', 'mainEntity': [
        {'@type': 'Question', 'name': q[lang], 'acceptedAnswer': {'@type': 'Answer', 'text': a[lang]}} for q, a in T['faq']]}
    return f'''<!doctype html>
<html lang="{lang}" dir="{'rtl' if lang == 'ar' else 'ltr'}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{t('meta_title', lang)}</title>
<meta name="description" content="{html.escape(t('meta_desc', lang))}">
<link rel="canonical" href="{url}">
<link rel="alternate" hreflang="ar" href="{SITE}/">
<link rel="alternate" hreflang="en" href="{SITE}/en/">
<link rel="alternate" hreflang="x-default" href="{SITE}/">
<meta property="og:type" content="website">
<meta property="og:title" content="{t('meta_title', lang)}">
<meta property="og:description" content="{html.escape(t('meta_desc', lang))}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{SITE}/assets/og-{lang}.png">
<meta property="og:locale" content="{'ar_JO' if lang == 'ar' else 'en_US'}">
<meta property="og:locale:alternate" content="{'en_US' if lang == 'ar' else 'ar_JO'}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#b5121b">
<link rel="icon" href="{'' if lang == 'ar' else '../'}assets/icon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Almarai:wght@700;800&family=Cairo:wght@400;600;800&display=swap">
<script type="application/ld+json">{json.dumps(ld_app, ensure_ascii=False)}</script>
<script type="application/ld+json">{json.dumps(ld_faq, ensure_ascii=False)}</script>
<style>{CSS}</style>
</head>
<body>'''

def header(lang):
    other_href = 'en/' if lang == 'ar' else '../'
    nav = ''.join(f'<a href="{h}">{T["nav"][k][lang]}</a>' for k, h in (('how', '#how'), ('categories', '#categories'), ('cafes', '#cafes'), ('stickers', '#stickers')))
    return f'''<header class="top">
  <div class="in">
    <a class="brand" href="./" aria-label="{'الصفحة الرئيسية' if lang == 'ar' else 'Home'}">{lockup(lang)}</a>
    <nav class="menu" aria-label="{'القائمة' if lang == 'ar' else 'Main'}">{nav}</nav>
    <div class="actions">
      <a class="lang" href="{other_href}" hreflang="{'en' if lang == 'ar' else 'ar'}" lang="{'en' if lang == 'ar' else 'ar'}">{t('lang_switch', lang)}</a>
      <a class="btn btn-red btn-sm" href="{PLAY}">{t('play', lang)}</a>
    </div>
  </div>
</header>'''

def phone(lang):
    word, sub = ('منسف', 'mansaf')
    return f'''<div class="phone" aria-hidden="true" dir="rtl">
  <div class="ph-bar"><span class="chip">🍽️ {'أكل وشرب'}</span><span class="timer">0:42</span></div>
  <div class="ph-card"><b>{word}</b><span dir="ltr">{sub}</span></div>
  <div class="ph-btns"><span class="ok">صح ✓</span><span class="skip">عدّيها</span></div>
  <div class="ph-score"><span>فريق الصقر</span><b>٧</b></div>
</div>'''

def stores(lang):
    names = ['Google Play', 'AppGallery', 'Galaxy Store']
    pills = ''.join(f'<span class="store"><small>{t("stores_soon", lang)}</small><b dir="ltr">{n}</b></span>' for n in names)
    return f'<div class="stores">{pills}</div>'

def hero(lang):
    facts = ''.join(f'<li>{f}</li>' for f in t('hero_facts', lang))
    return f'''<section class="hero">
  <div class="in">
    <div class="hero-text">
      <span class="eyebrow">{t('hero_eyebrow', lang)}</span>
      <h1>{t('hero_h1', lang)}</h1>
      <p class="lead">{t('hero_sub', lang)}</p>
      <div class="ctas"><a class="btn btn-red" href="{PLAY}">{t('play', lang)}</a><a class="btn btn-ghost" href="#faq-install">{t('install', lang)}</a></div>
      <ul class="facts">{facts}</ul>
      {stores(lang)}
    </div>
    <div class="hero-art">{phone(lang)}<div class="hero-mascot">{mascot('card', 'شمّوغ' if lang == 'ar' else 'Shammogh, the mascot')}</div></div>
  </div>
</section>
<div class="band" aria-hidden="true"></div>'''

def modes(lang):
    cards = ''.join(f'''<article class="mode">
      <div class="mode-art">{stitch(MODE_ART[k], name[lang], 13)}</div>
      <h3>{name[lang]}</h3><p>{desc[lang]}</p><span class="tag">{who[lang]}</span></article>''' for k, name, desc, who in T['modes'])
    return f'''<section class="sec" id="modes"><div class="in">
  <div class="sec-head"><h2>{t('modes_h', lang)}</h2><p>{t('modes_p', lang)}</p></div>
  <div class="modes">{cards}</div></div></section>'''

def categories(lang):
    tiles = ''.join(f'''<a class="cat" href="categories/{cid}/">
      <span class="cat-art">{stitch(CAT_ART[cid], en if lang == 'en' else ar)}</span>
      <b>{ar if lang == 'ar' else en}</b><small>{n if lang == 'en' else to_ar_digits(n)} {t('cards_word', lang)}</small></a>''' for cid, ar, en, n in CATEGORIES)
    return f'''<section class="sec" id="categories"><div class="in">
  <div class="sec-head"><h2>{t('cats_h', lang) if lang == 'en' else to_ar_digits_text(t('cats_h', lang))}</h2><p>{t('cats_p', lang)}</p></div>
  <div class="cats">{tiles}</div></div></section>'''

def to_ar_digits(n): return str(n).translate(str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩'))
def to_ar_digits_text(s): return s.translate(str.maketrans('0123456789', '٠١٢٣٤٥٦٧٨٩'))

def how(lang):
    steps = ''.join(f'<li><span class="step">{to_ar_digits(i) if lang == "ar" else i}</span><h3>{h[lang]}</h3><p>{p[lang]}</p></li>' for i, (h, p) in enumerate(T['how'], 1))
    return f'''<section class="sec how" id="how"><div class="in">
  <div class="sec-head"><h2>{t('how_h', lang)}</h2></div>
  <div class="how-grid"><ol class="steps">{steps}</ol><div class="how-mascot">{mascot('shh', 'شمّوغ: ششش… ولا كلمة!' if lang == 'ar' else 'Shammogh going shh')}</div></div></div></section>'''

def promise(lang):
    items = ''.join(f'<li><h3>{h[lang]}</h3><p>{p[lang]}</p></li>' for h, p in T['promise'])
    return f'''<section class="sec" id="promise"><div class="in">
  <div class="sec-head"><h2>{t('promise_h', lang)}</h2></div>
  <ul class="promise">{items}</ul></div></section>'''

def cafes(lang):
    return f'''<section class="cafes" id="cafes"><div class="in">
  <div class="cafes-text"><span class="eyebrow gold">{t('cafes_eyebrow', lang)}</span><h2>{t('cafes_h', lang)}</h2><p>{t('cafes_p', lang)}</p>
    <div class="ctas"><a class="btn btn-red" href="mailto:{CONTACT}?subject=Wala%20Kelmeh%20night">{t('cafes_cta', lang)}</a><span class="mail" dir="ltr">{CONTACT}</span></div></div>
  <div class="cafes-art">{mascot('cool', 'شمّوغ' if lang == 'ar' else 'Shammogh in sunglasses')}</div></div></section>'''

def stickers(lang):
    row = ''.join(f'<span class="stk">{mascot(k, MOODS[k][1])}</span>' for k in ('wave', 'laugh', 'yay', 'love', 'shock', 'proud'))
    return f'''<section class="sec" id="stickers"><div class="in">
  <div class="sec-head"><h2>{t('stickers_h', lang)}</h2><p>{t('stickers_p', lang)}</p></div>
  <div class="stickers">{row}</div>
  <a class="btn btn-ghost" href="stickers/">{t('stickers_cta', lang)}</a></div></section>'''

def faq(lang):
    qs = ''.join(f'<details{" id=faq-install" if i == 1 else ""}><summary>{q[lang]}</summary><p>{a[lang]}</p></details>' for i, (q, a) in enumerate(T['faq']))
    return f'''<section class="sec" id="faq"><div class="in narrow">
  <div class="sec-head"><h2>{t('faq_h', lang)}</h2></div>
  <div class="faq">{qs}</div></div></section>'''

def footer(lang):
    prefix = '' if lang == 'ar' else '../'
    return f'''<div class="band" aria-hidden="true"></div>
<footer class="foot"><div class="in">
  <div class="foot-brand">{lockup(lang, dark=True)}<p>{t('footer_tag', lang)}</p></div>
  <nav class="foot-links" aria-label="{'روابط' if lang == 'ar' else 'Footer'}">
    <a href="how-to-play/">{T['nav']['how'][lang]}</a><a href="categories/">{T['nav']['categories'][lang]}</a>
    <a href="cafes/">{T['nav']['cafes'][lang]}</a><a href="stickers/">{T['nav']['stickers'][lang]}</a>
    <a href="{prefix}privacy.html">{t('privacy', lang)}</a><a href="mailto:{CONTACT}">{t('contact', lang)}</a></nav>
  <p class="rights">{t('rights', lang)}</p>
</div></footer>
</body>
</html>'''

def page(lang):
    return (head(lang) + header(lang) + '<main>' + hero(lang) + modes(lang) + categories(lang) + how(lang)
            + promise(lang) + cafes(lang) + stickers(lang) + faq(lang) + '</main>' + footer(lang))

def build():
    os.makedirs(os.path.join(OUT, 'en'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'assets'), exist_ok=True)
    open(os.path.join(OUT, 'index.html'), 'w', encoding='utf-8').write(page('ar'))
    open(os.path.join(OUT, 'en', 'index.html'), 'w', encoding='utf-8').write(page('en'))
    import shutil
    shutil.copy(os.path.join(REPO, 'brand', 'logo', 'symbol', 'symbol-small.svg'), os.path.join(OUT, 'assets', 'icon.svg'))
    print('built', OUT, '(preview)' if PREVIEW else '')

if __name__ == '__main__':
    build()

def preview_bundle():
    """One-file preview for review links: both languages, the switch toggles between them."""
    def body(lang):
        s = page(lang)
        return s[s.index('<body>') + 6:s.index('</body>')]
    style = f'<style>{CSS}</style>'
    script = '''<script>
document.addEventListener('click', function (e) {
  var a = e.target.closest('a.lang');
  if (!a) return;
  e.preventDefault();
  var ar = document.getElementById('v-ar'), en = document.getElementById('v-en');
  var toEn = !ar.hidden;
  ar.hidden = toEn; en.hidden = !toEn;
  window.scrollTo(0, 0);
});
</script>'''
    note = '<p style="margin:0;padding:8px 16px;background:#2a1f1a;color:#f4ecdd;font:600 13px Cairo,sans-serif;text-align:center">' \
           'Preview · links to other pages work once they’re built · نسخة تجريبية</p>'
    doc = (f'<title>Wala Kelmeh Website</title>\n<meta name="claude:viewport-fit-sides" content="cover">\n'
           '<link rel="preconnect" href="https://fonts.googleapis.com">\n'
           '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Almarai:wght@700;800&family=Cairo:wght@400;600;800&display=swap">\n'
           f'{style}\n{note}<div id="v-ar" lang="ar" dir="rtl">{body("ar")}</div><div id="v-en" lang="en" dir="ltr" hidden>{body("en")}</div>{script}')
    open(os.path.join(OUT, 'preview.html'), 'w', encoding='utf-8').write(doc)

if __name__ == '__main__' and PREVIEW:
    preview_bundle()
    print('preview bundle written')
