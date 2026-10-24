"""Frames the raw game screens into store screenshots (1080x1920) and feature graphics (1024x500)."""
import json, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = '/home/user/Jordanian-cards'
OUT = os.path.join(REPO, 'brand', 'store')
RAW = os.path.join(REPO, 'brand', 'store', 'raw')
MASCOT = os.path.join(REPO, 'brand', 'mascot', 'svg')
LOGO = os.path.join(REPO, 'brand', 'logo')
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Almarai:wght@800&family=Cairo:wght@600;800&display=swap">'

SHOTS = [  # raw, Arabic caption, Arabic sub, English caption, English sub, mascot, theme
  ('home-light', 'لعبة التمثيل الأردنية', 'لسهرات العيلة والصحاب', 'The Jordanian charades game', 'For family and friends’ nights', 'wink', 'cream'),
  ('play', 'مثّلها… بس ولا كلمة!', 'واحد بمثّل وفريقه بحزر', 'Act it out. Not a word.', 'One acts, the team guesses', None, 'cream'),
  ('headsup', 'عالجبين', 'الجوال على جبينك وفريقك بمثّل', 'Heads up', 'Phone on your forehead, your team acts', 'yay', 'red'),
  ('fastest', 'مين أسرع؟', 'أول واحد بيعرفها بياخذ النقطة', 'Who’s fastest?', 'First right answer takes the point', None, 'cream'),
  ('categories', '٥١٠ بطاقة أردنية', '١٦ فئة، من المنسف للجاهة', '510 Jordanian cards', '16 categories, from mansaf to the jaha', None, 'cream'),
  ('setup', 'من ٢ لـ ٤ فرق', 'أو العبوها بدون فرق', '2 to 4 teams', 'Or play with no teams at all', None, 'cream'),
  ('final', 'مين النشامى؟', 'توّجوا الفايزين وشاركوا النتيجة', 'Crown the winners', 'And share the result on WhatsApp', None, 'red'),
  ('play-dark', 'فاتح وغامق', 'وبتشتغل بدون إنترنت', 'Light and dark', 'And it works offline', None, 'night'),
]
BG = {'cream': ('#f4ecdd', '#2a1f1a', '#b5121b', '#7a6650'), 'red': ('#b5121b', '#fff8ee', '#fff8ee', '#ffd9d3'), 'night': ('#17110e', '#f4ecdd', '#ec5f66', '#b5a28a')}

def page(body, w, h, lang, extra_css=''):
    return f'''<!doctype html><html lang="{lang}" dir="{'rtl' if lang == 'ar' else 'ltr'}"><head><meta charset="utf-8">{FONTS}<style>
*{{box-sizing:border-box}} body{{margin:0;width:{w}px;height:{h}px;overflow:hidden;position:relative;font-family:Cairo,sans-serif}}
.weave{{position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,rgba(90,60,30,.05) 0 2px,transparent 2px 12px),repeating-linear-gradient(90deg,rgba(90,60,30,.05) 0 2px,transparent 2px 12px)}}
.band{{position:absolute;left:0;right:0;height:28px;background:repeating-linear-gradient(45deg,#b5121b 0 14px,#f6efe3 14px 28px)}}
{extra_css}</style></head><body>{body}</body></html>'''

def shot_html(raw, cap, sub, mascot, theme, lang, landscape=False):
    bg, ink, accent, muted = BG[theme]
    img = f'file://{RAW}/{raw}.png'
    if landscape:
        phone = f'<div class="ph land"><img src="{img}"></div>'
    else:
        phone = f'<div class="ph"><img src="{img}"></div>'
    m = f'<img class="masc" src="file://{MASCOT}/shammogh-{mascot}.svg">' if mascot else ''
    css = f'''body{{background:{bg}}}
.cap{{position:absolute;top:96px;left:70px;right:70px;text-align:center;display:grid;gap:14px}}
.cap h1{{margin:0;font:800 {96 if lang == 'ar' else 88}px/1.15 Almarai,sans-serif;color:{accent}}}
.cap p{{margin:0;font:600 46px/1.35 Cairo,sans-serif;color:{muted}}}
.ph{{position:absolute;left:50%;transform:translateX(-50%);top:470px;width:800px;height:1422px;border-radius:84px;background:#17110e;padding:22px;box-shadow:0 40px 80px rgba(23,17,14,.35)}}
.ph img{{width:100%;height:100%;border-radius:64px;display:block;object-fit:cover;object-position:top}}
.ph.land{{top:700px;width:1000px;height:584px;border-radius:70px;padding:20px}}
.ph.land img{{border-radius:52px}}
.masc{{position:absolute;width:330px;bottom:{70 if landscape else 40}px;{'left' if lang == 'ar' else 'right'}:{30 if not landscape else 60}px;filter:drop-shadow(0 18px 24px rgba(23,17,14,.35))}}'''
    band = '<div class="band" style="top:0"></div>'
    return page(f'<div class="weave"></div>{band}<div class="cap"><h1>{cap}</h1><p>{sub}</p></div>{phone}{m}', 1080, 1920, lang, css)

def feature_html(lang):
    tag = 'مثّلها… بس ولا كلمة!' if lang == 'ar' else 'Act it out. Not a word.'
    sub = 'لعبة التمثيل الأردنية · ٥١٠ بطاقة · مجانية' if lang == 'ar' else 'The Jordanian charades game · 510 cards · Free'
    lock = f'file://{LOGO}/lockup/lockup-{"arabic" if lang == "ar" else "english"}-horizontal-on-light.svg'
    css = '''body{background:#f4ecdd}
.wrap{position:absolute;inset:0 0 22px;display:grid;grid-template-columns:1.25fr 1fr;align-items:center;padding:0 50px;gap:10px}
.l{display:grid;gap:16px} .l img{width:440px;height:auto} h1{margin:0;font:800 50px/1.15 Almarai,sans-serif;color:#b5121b;white-space:nowrap} :lang(en) h1{font-size:44px} p{margin:0;font:600 22px Cairo,sans-serif;color:#7a6650}
.r{position:relative;height:500px} .ph{position:absolute;top:56px;width:210px;height:373px;border-radius:30px;background:#17110e;padding:8px;transform:rotate(-6deg);box-shadow:0 20px 40px rgba(23,17,14,.3)}
.ph img{width:100%;height:100%;border-radius:23px;object-fit:cover;object-position:top}
.m{position:absolute;bottom:18px;width:210px;filter:drop-shadow(0 12px 16px rgba(23,17,14,.3))}
.band{bottom:0;height:22px}'''
    side = 'right' if lang == 'ar' else 'left'
    other = 'left' if lang == 'ar' else 'right'
    body = f'''<div class="weave"></div><div class="wrap"><div class="l"><img src="{lock}"><h1>{tag}</h1><p>{sub}</p></div>
<div class="r"><div class="ph" style="{side}:60px"><img src="file://{RAW}/play.png"></div><img class="m" src="file://{MASCOT}/shammogh-card.svg" style="{other}:0"></div></div><div class="band"></div>'''
    return page(body, 1024, 500, lang, css)

jobs = []
tmp = os.path.join(HERE, 'html'); os.makedirs(tmp, exist_ok=True)
for lang in ('ar', 'en'):
    d = os.path.join(OUT, lang); os.makedirs(d, exist_ok=True)
    for i, (raw, car, sar, cen, sen, masc, theme) in enumerate(SHOTS, 1):
        cap, sub = (car, sar) if lang == 'ar' else (cen, sen)
        f = os.path.join(tmp, f'{lang}-{i}.html')
        open(f, 'w', encoding='utf-8').write(shot_html(raw, cap, sub, masc, theme, lang, landscape=(raw == 'headsup')))
        jobs.append({'src': f, 'out': os.path.join(d, f'screenshot-{i:02d}-{raw}.png'), 'w': 1080, 'h': 1920})
    f = os.path.join(tmp, f'{lang}-feature.html'); open(f, 'w', encoding='utf-8').write(feature_html(lang))
    jobs.append({'src': f, 'out': os.path.join(d, 'feature-graphic-1024x500.png'), 'w': 1024, 'h': 500})
json.dump(jobs, open(os.path.join(HERE, 'jobs.json'), 'w'))
open(os.path.join(HERE, 'render.cjs'), 'w').write('''const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const jobs = require(process.argv[2]);
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  for (const j of jobs) { await p.setViewportSize({ width: j.w, height: j.h }); await p.goto('file://' + j.src); await p.waitForTimeout(900);
    await p.screenshot({ path: j.out, type: 'png' }); }
  await b.close(); })();''')
subprocess.run(['node', os.path.join(HERE, 'render.cjs'), os.path.join(HERE, 'jobs.json')], check=True, timeout=300)
print('rendered', len(jobs))
