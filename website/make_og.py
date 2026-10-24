"""Renders the static images: social share cards (1200x630), favicon, Apple touch icon, logo PNG. Needs Playwright."""
import json, os, subprocess, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import build as B
from logos import icon_C
OUT = os.path.join(HERE, 'static', 'assets')
TMP = os.path.join(HERE, 'out', '_og')
os.makedirs(OUT, exist_ok=True); os.makedirs(TMP, exist_ok=True)

FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Almarai:wght@800&family=Cairo:wght@600;800&display=swap">'
def og(lang):
    tag = B.T['hero_h1'][lang]
    sub = {'ar': 'لعبة التمثيل الأردنية · ٥١٠ بطاقة · مجانية', 'en': 'The Jordanian charades game · 510 cards · Free'}[lang]
    m = B.msvg(B.MOODS['wink'][2]('og'), B.MASCOT_VB)
    return f'''<!doctype html><html lang="{lang}" dir="{'rtl' if lang == 'ar' else 'ltr'}"><head><meta charset="utf-8">{FONTS}<style>
body{{margin:0;width:1200px;height:630px;overflow:hidden;background:#f4ecdd;font-family:Cairo,sans-serif;
 background-image:repeating-linear-gradient(0deg,rgba(90,60,30,.04) 0 1px,transparent 1px 6px),repeating-linear-gradient(90deg,rgba(90,60,30,.04) 0 1px,transparent 1px 6px)}}
.wrap{{position:absolute;inset:0 0 28px;display:grid;grid-template-columns:1.35fr 1fr;align-items:center;padding:0 70px;gap:20px}}
.l{{display:grid;gap:26px}} .l svg{{width:560px;height:auto}} h1{{margin:0;font:800 64px/1.15 Almarai,sans-serif;color:#b5121b}}
p{{margin:0;font:600 28px/1.4 Cairo,sans-serif;color:#7a6650}} .m svg{{width:430px;height:auto}}
.band{{position:absolute;inset:auto 0 0;height:28px;background:repeating-linear-gradient(45deg,#b5121b 0 14px,#f6efe3 14px 28px)}}
</style></head><body><div class="wrap"><div class="l">{B.lockup(lang, 'light')}<h1>{tag}</h1><p>{sub}</p></div><div class="m">{m}</div></div><div class="band"></div></body></html>'''

def icon_page(svg, size, pad=0):
    return f'<!doctype html><html><body style="margin:0;width:{size}px;height:{size}px;background:transparent">{svg.replace("<svg ", f"<svg width={size} height={size} ", 1)}</body></html>'

jobs = []
for lang in ('ar', 'en'):
    p = os.path.join(TMP, f'og-{lang}.html'); open(p, 'w', encoding='utf-8').write(og(lang))
    jobs.append({'src': p, 'out': os.path.join(OUT, f'og-{lang}.png'), 'w': 1200, 'h': 630, 'transparent': False})
small = open(os.path.join(B.REPO, 'brand', 'logo', 'symbol', 'symbol-small.svg')).read()
square = icon_C('red', 'sq').replace('rx="112"', 'rx="0"')
for name, svg, size, tr in (('favicon-32.png', small, 32, True), ('apple-touch-icon.png', square, 180, False), ('logo-512.png', icon_C('red', 'lg'), 512, True)):
    p = os.path.join(TMP, name + '.html'); open(p, 'w').write(icon_page(svg, size))
    jobs.append({'src': p, 'out': os.path.join(OUT, name), 'w': size, 'h': size, 'transparent': tr})
js = os.path.join(TMP, 'render.cjs')
open(js, 'w').write('''let pw; try { pw = require('playwright'); } catch (e) { pw = require('/opt/node22/lib/node_modules/playwright'); } const { chromium } = pw;
const jobs = require(process.argv[2]);
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  for (const j of jobs) { await p.setViewportSize({ width: j.w, height: j.h }); await p.goto('file://' + j.src); await p.waitForTimeout(700);
    await p.screenshot({ path: j.out, omitBackground: j.transparent }); }
  await b.close(); })();''')
jf = os.path.join(TMP, 'jobs.json'); json.dump(jobs, open(jf, 'w'))
subprocess.run(['node', js, jf], check=True, timeout=180)
print('static images:', sorted(os.listdir(OUT)))
