import os
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.join(HERE, '..', '..')
import re
from final import *
ART = open(os.path.join(REPO, 'src', 'art.ts')).read()
def arrays(block_name):
    start = ART.index(f'export const {block_name}')
    end = ART.index('\n};', start) if block_name != 'TATREEZ_BAND' else ART.index('];', start)
    return ART[start:end]
def parse_record(name):
    out = []
    for m in re.finditer(r"(?:\n\s*//\s*([^\n]*))?\n\s*(\w+):\s*\[(.*?)\]", arrays(name), re.S):
        rows = re.findall(r"'([^']*)'", m.group(3))
        if rows: out.append((m.group(2), m.group(1) or '', rows))
    return out
def parse_avatars():
    blk = arrays('AVATARS')
    return [(a, re.findall(r"'([^']*)'", rows)) for a, rows in re.findall(r"ar:\s*'([^']*)',\s*art:\s*\[(.*?)\]", blk, re.S)]
TH = {'r': '#b5121b', 'g': '#4f6b2c', 'y': '#c9962a', 'k': '#2a1f1a', 'b': '#3b3f7a'}
def stitch_art(rows, cell=12):
    w, h = max(len(r) for r in rows) * cell, len(rows) * cell
    out = ''.join(xstitch(c * cell + cell/2, r * cell + cell/2, cell * .8, TH[v], cell * .28) for r, row in enumerate(rows) for c, v in enumerate(row) if v in TH)
    return svg(w, h, out)
cats = parse_record('CATEGORY_ART')
modes = parse_record('MODE_ART')
avs = parse_avatars()
band = re.findall(r"'([^']*)'", arrays('TATREEZ_BAND'))

def band_svg(n=14, cell=10):
    rows = [row * n for row in band]
    return stitch_art(rows, cell)

SH = re.search(r"--shemagh: (url\(\"data:image/svg\+xml,.*?\"\));", open(os.path.join(REPO, 'src', 'styles.css')).read()).group(1)

light = [('Cream fabric','--bg','#f4ecdd','Page background','60%'),('Surface','--surface','#fbf6ec','Cards, sheets',''),('Line','--line','#dccbae','Borders, dividers',''),
         ('Stitch','--stitch','#c7b08a','Running-stitch borders',''),('Ink','--text','#2a1f1a','Text, wordmark','25%'),('Muted','--muted','#7a6650','Secondary text',''),
         ('Shemagh red','--red','#b5121b','Brand, primary action, game card','10%'),('Olive','--olive','#4f6b2c','Correct, team 2','5% threads'),('Gold','--gold','#b9861f','Decoration, team 4',''),('Indigo','--indigo','#3b3f7a','Team 3, info','')]
dark = [('Night majlis','--bg','#17110e'),('Surface','--surface','#231a15'),('Line','--line','#3f3128'),('Stitch','--stitch','#6a5442'),('Cream text','--text','#f4ecdd'),('Muted','--muted','#b5a28a'),
        ('Red','--red','#d42630'),('Olive','--olive','#8aa75a'),('Gold','--gold','#ddae4a'),('Indigo','--indigo','#8d92d6')]
def chip(n, t, h, use='', pct=''):
    return f'<div class="sw"><span style="background:{h}"></span><b>{n}</b><code>{t} {h}</code>{f"<small>{use}</small>" if use else ""}</div>'

contrast = [('Ink on cream','13.7','AAA','Any text'),('Muted on cream','4.7','AA','Body text OK'),('Red on cream','5.8','AA','Text and buttons'),('Cream on red','6.5','AA','Button and card text'),
            ('Olive on cream','5.2','AA','Text OK'),('Gold on cream','2.8','Fail','Decoration only, never text'),('Indigo on cream','8.2','AAA','Text OK'),
            ('Cream on night','15.9','AAA','Any text'),('Red on night','3.7','Large only','Fills and 24px+ headings; small red text uses #e0444c'),('Cream on dark red','4.8','AA','Button text'),
            ('White on dark green','4.0','Large only','Buttons must stay bold 18px+')]
def row(c): 
    cls = 'bad' if c[2] == 'Fail' else ('warn' if 'Large' in c[2] else 'good')
    return f'<tr><td>{c[0]}</td><td class="num">{c[1]}:1</td><td><span class="pill {cls}">{c[2]}</span></td><td>{c[3]}</td></tr>'

def sized(s, a): return s.replace('<svg ', f'<svg {a} ', 1)
cat_html = ''.join(f'<figure class="art">{sized(stitch_art(r), "role=img aria-label=\"" + (c or k) + "\"")}<figcaption>{c or k}</figcaption></figure>' for k, c, r in cats)
av_html = ''.join(f'<figure class="art">{sized(stitch_art(r), "role=img aria-label=\"" + a + "\"")}<figcaption>{a}</figcaption></figure>' for a, r in avs)
mode_html = ''.join(f'<figure class="art">{sized(stitch_art(r), "role=img aria-label=\"" + (c or k) + "\"")}<figcaption>{c or k}</figcaption></figure>' for k, c, r in modes)

page = f'''<title>Wala Kelmeh Sahra System</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Almarai:wght@400;700;800&family=Cairo:wght@400;600;800&display=swap">
<style>
/* Layout: the Sahra system documented in its own fabric; stacked sections, swatches and specimens wrap. */
:root {{ --bg:#f4ecdd; --surface:#fbf6ec; --line:#dccbae; --stitch:#c7b08a; --text:#2a1f1a; --muted:#7a6650; --red:#b5121b; --on-red:#fff8ee; --olive:#4f6b2c; --gold:#b9861f;
  --display:'Almarai','Cairo',system-ui,sans-serif; --font:'Cairo',system-ui,-apple-system,'Segoe UI',sans-serif; --weave:rgba(90,60,30,.035); }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#17110e; --surface:#231a15; --line:#3f3128; --stitch:#6a5442; --text:#f4ecdd; --muted:#b5a28a; --red:#e0444c; --olive:#8aa75a; --gold:#ddae4a; --weave:rgba(255,240,220,.025); color-scheme:dark; }} }}
:root[data-theme="dark"] {{ --bg:#17110e; --surface:#231a15; --line:#3f3128; --stitch:#6a5442; --text:#f4ecdd; --muted:#b5a28a; --red:#e0444c; --olive:#8aa75a; --gold:#ddae4a; --weave:rgba(255,240,220,.025); color-scheme:dark; }}
* {{ box-sizing:border-box; }}
body {{ background:var(--bg); color:var(--text); font:16px/1.6 var(--font);
  background-image:repeating-linear-gradient(0deg,var(--weave) 0 1px,transparent 1px 6px),repeating-linear-gradient(90deg,var(--weave) 0 1px,transparent 1px 6px); }}
.wrap {{ max-width:1120px; margin:0 auto; padding-block:40px 72px; padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); display:grid; gap:52px; }}
h1,h2,h3 {{ font-family:var(--display); margin:0; line-height:1.2; text-wrap:balance; }}
h1 {{ font-size:clamp(30px,5vw,44px); }} h2 {{ font-size:26px; }} h3 {{ font-size:18px; }}
p {{ margin:0; max-width:65ch; }}
.eyebrow {{ font-size:13px; letter-spacing:.12em; text-transform:uppercase; color:var(--red); font-weight:800; }}
header {{ display:grid; gap:12px; }}
section {{ display:grid; gap:18px; }}
.sec-head {{ display:grid; gap:6px; border-top:2px dashed var(--stitch); padding-top:22px; }}
.sec-head p {{ color:var(--muted); }}
.panel {{ background:var(--surface); border:1px solid var(--line); border-radius:18px; padding:20px; display:grid; gap:14px; min-width:0; }}
.swatches {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(150px,1fr)); gap:12px; }}
.sw {{ display:grid; gap:2px; font-size:13px; }}
.sw span {{ height:60px; border-radius:12px; border:1px solid var(--line); }}
.sw code {{ color:var(--muted); font-size:12px; }} .sw small {{ color:var(--muted); }}
.night {{ background:#17110e; color:#f4ecdd; border-color:#3f3128; }} .night .sw code, .night .sw small, .night p {{ color:#b5a28a; }} .night .sw span {{ border-color:#3f3128; }}
.ratio {{ display:flex; height:46px; border-radius:12px; overflow:hidden; border:1px solid var(--line); }}
.ratio div {{ display:grid; place-items:center; font-size:12px; font-weight:700; }}
.tablewrap {{ overflow-x:auto; }}
table {{ border-collapse:collapse; width:100%; font-size:14px; }}
th,td {{ text-align:start; padding:9px 10px; border-bottom:1px solid var(--line); vertical-align:top; }}
th {{ font-family:var(--display); color:var(--muted); font-size:13px; }}
.num {{ font-variant-numeric:tabular-nums; white-space:nowrap; }}
.pill {{ font-size:12px; font-weight:700; padding:2px 10px; border-radius:999px; white-space:nowrap; }}
.pill.good {{ background:color-mix(in srgb, var(--olive) 18%, transparent); color:var(--olive); }}
.pill.warn {{ background:color-mix(in srgb, var(--gold) 22%, transparent); color:var(--text); }}
.pill.bad {{ background:color-mix(in srgb, var(--red) 15%, transparent); color:var(--red); }}
.type-row {{ display:grid; grid-template-columns:150px minmax(0,1fr); gap:14px; align-items:baseline; padding-block:10px; border-bottom:1px dashed var(--line); }}
.type-row:last-child {{ border-bottom:0; }}
.type-row .meta {{ font-size:12px; color:var(--muted); }}
.ar {{ direction:rtl; text-align:right; }}
.patterns {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(240px,1fr)); gap:14px; }}
.pat {{ margin:0; display:grid; gap:8px; }}
.pat .tile {{ height:120px; border-radius:14px; border:1px solid var(--line); overflow:hidden; display:grid; place-items:center; background:var(--surface); }}
.pat .shemagh {{ background:{SH} repeat; background-size:18px; }}
.pat figcaption {{ font-size:13px; color:var(--muted); }}
.pat .band svg {{ width:100%; height:auto; }}
.runner {{ width:80%; height:70px; border:2px dashed var(--stitch); border-radius:14px; }}
.xrow {{ display:flex; gap:10px; color:var(--red); font-weight:800; font-size:20px; }}
.arts {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(110px,1fr)); gap:12px; }}
.art {{ margin:0; background:#f7f0e3; border:1px solid #dccbae; border-radius:14px; padding:14px; display:grid; gap:8px; justify-items:center; }}
.art svg {{ width:72px; height:auto; }}
.art figcaption {{ font-size:12px; color:#6f5c47; text-align:center; line-height:1.3; }}
ul.rules {{ margin:0; padding-inline-start:20px; display:grid; gap:6px; max-width:72ch; }}
@media (max-width:600px) {{ .type-row {{ grid-template-columns:1fr; gap:4px; }} }}
</style>
<div class="wrap">
<header>
  <span class="eyebrow">Brand kit · Step 4 · Direction A</span>
  <h1>Sahra: colour, type, pattern</h1>
  <p>Cream fabric by day, night majlis after dark. Shemagh red leads, and olive, gold and indigo work as tatreez threads. These are the same tokens the app runs on, so the brand and the product never drift apart.</p>
</header>

<section>
  <div class="sec-head"><h2>Colour</h2><p>Light mode is cream fabric. Dark mode is night majlis. The bar below shows roughly how much of each colour a typical screen or post uses.</p></div>
  <div class="panel"><div class="swatches">{''.join(chip(*c[:4]) for c in light)}</div>
    <div class="ratio"><div style="flex:60;background:#f4ecdd;color:#2a1f1a">Cream 60%</div><div style="flex:25;background:#2a1f1a;color:#f4ecdd">Ink 25%</div><div style="flex:10;background:#b5121b;color:#fff8ee">Red 10%</div><div style="flex:5;background:linear-gradient(90deg,#4f6b2c,#b9861f,#3b3f7a)"></div></div>
  </div>
  <div class="panel night"><h3>Night majlis (dark)</h3><div class="swatches">{''.join(chip(*c) for c in dark)}</div>
    <p style="font-size:14px">Threads get lighter in the dark so they stay readable. Logo colours don’t change between themes.</p></div>
  <div class="panel"><h3>Contrast checks (WCAG)</h3><div class="tablewrap"><table>
    <thead><tr><th>Pair</th><th>Ratio</th><th>Level</th><th>Rule</th></tr></thead><tbody>{''.join(row(c) for c in contrast)}</tbody></table></div></div>
</section>

<section>
  <div class="sec-head"><h2>Type</h2><p>Almarai for headlines, Cairo for everything else, in both Arabic and Latin. The stitched lettering is for the logo only and is never used to set text.</p></div>
  <div class="panel">
    <div class="type-row"><span class="meta">Display · Almarai 800 · 40/48</span><span class="ar" style="font:800 40px/1.2 var(--display);color:var(--red)">مثّلها… بس ولا كلمة!</span></div>
    <div class="type-row"><span class="meta">H1 · Almarai 800 · 32/40</span><span class="ar" style="font:800 32px/1.25 var(--display)">مين أسرع؟</span></div>
    <div class="type-row"><span class="meta">H2 · Almarai 700 · 24/32</span><span class="ar" style="font:700 24px/1.35 var(--display)">أكل وشرب · ٤٠ بطاقة</span></div>
    <div class="type-row"><span class="meta">H3 · Cairo 800 · 20/28</span><span class="ar" style="font:800 20px/1.4 var(--font)">فريق الصقر</span></div>
    <div class="type-row"><span class="meta">Body · Cairo 400 · 16/28</span><span class="ar" style="font:400 16px/1.75 var(--font)">اسحب البطاقة يمين إذا فريقك عرفها، ويسار إذا بدك تتخطّاها. عندكم دقيقة وحدة… يلا!</span></div>
    <div class="type-row"><span class="meta">Small · Cairo 600 · 14/22</span><span class="ar" style="font:600 14px/1.6 var(--font);color:var(--muted)">٣ جولات · ٦٠ ثانية</span></div>
    <div class="type-row"><span class="meta">Latin · Cairo 600 · 16/26</span><span style="font:600 16px/1.6 var(--font)">Act it out. Not a word. Card in Arabizi: <i>mansaf</i></span></div>
  </div>
  <ul class="rules">
    <li>Arabic copy uses Eastern Arabic numerals «٣», and Latin copy uses 3.</li>
    <li>Arabic body text gets generous line height (1.7 to 1.8). Diacritics and shadda need the room.</li>
    <li>Never letter-space Arabic. Latin uppercase labels get +0.12em.</li>
    <li>Headlines in red or ink. Body text in ink or muted, never gold.</li>
  </ul>
</section>

<section>
  <div class="sec-head"><h2>Pattern</h2><p>Four textile devices, all drawn from shemagh and tatreez. Use one or two per layout, never all four at once.</p></div>
  <div class="patterns">
    <figure class="pat"><div class="tile shemagh"></div><figcaption><b>Shemagh weave:</b> the red diamond check. For bands, card backs and a full-bleed background behind the logo.</figcaption></figure>
    <figure class="pat"><div class="tile band">{sized(band_svg(), 'role="img" aria-label="Tatreez band"')}</div><figcaption><b>Tatreez band:</b> a repeating cross-stitch border. For section edges, headers and the bottom of posters.</figcaption></figure>
    <figure class="pat"><div class="tile"><div class="runner"></div></div><figcaption><b>Running stitch:</b> a dashed border in the stitch colour. It outlines cards, avatars and inputs, like a patch sewn on.</figcaption></figure>
    <figure class="pat"><div class="tile"><div class="xrow" aria-hidden="true">✕ ✕ ✕ ✕ ✕ ✕</div></div><figcaption><b>Cross-stitch row:</b> the X stitch from the logo frame. It works as a divider, a bullet, or the partner lockup separator.</figcaption></figure>
  </div>
</section>

<section>
  <div class="sec-head"><h2>Illustration</h2><p>Everything is drawn as cross-stitch: one X per square on a grid, using only the five thread colours. These are the illustrations already in the app.</p></div>
  <div class="panel"><h3>Categories</h3><div class="arts">{cat_html}</div></div>
  <div class="panel"><h3>Team emblems</h3><div class="arts">{av_html}</div></div>
  <div class="panel"><h3>Game modes</h3><div class="arts">{mode_html}</div></div>
  <ul class="rules">
    <li>Use the five threads only: red, olive, gold, ink and indigo. No gradients, outlines or shading.</li>
    <li>Keep grids small, about 8 to 12 squares across, so they read as embroidery, not pixel art.</li>
    <li>Always show the stitches on fabric (cream), even in dark mode, where they sit on a cream patch.</li>
    <li>شمّوغ, the mascot, is the one exception: a drawn character, with stitch details on its shemagh.</li>
  </ul>
</section>
</div>'''
open(os.path.join(HERE, 'out-sahra.html'),'w').write(page)
print('ok', len(cats), len(avs), len(modes))
