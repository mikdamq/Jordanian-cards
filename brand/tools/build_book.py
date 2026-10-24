import os
HERE = os.path.dirname(os.path.abspath(__file__))
import re
import build_guide as BG          # logo helpers (also rewrites logo-guide.html, harmless)
import build_sahra as BS          # palette, art, patterns
from final import *
from poses4 import P as MOODS, svg as msvg
VB = '-24 -34 470 454'
def sized(s, a): return s.replace('<svg ', f'<svg {a} ', 1)
n = [0]
def uid(p='b'): n[0] += 1; return f'{p}{n[0]}'
def Pt(): return patch(gid('bk'))
def mood(k, a=''): return sized(msvg(MOODS[k][2](uid('m')), VB), a)
def fig(svgs, cls, cap, label):
    return f'<figure class="tile {cls}">{sized(svgs, f"role=img aria-label=\"{label}\"")}<figcaption>{cap}</figcaption></figure>'

NAV = [('strategy', 'Strategy'), ('voice', 'Voice'), ('logo', 'Logo'), ('colour', 'Colour'), ('type', 'Type'), ('pattern', 'Pattern'), ('illustration', 'Illustration'), ('mascot', 'شمّوغ'), ('files', 'Files')]
nav = ''.join(f'<a href="#{k}">{v}</a>' for k, v in NAV)

hero = f'''<section class="cover">
  <div class="cover-in">
    <div class="cover-text">
      <span class="eyebrow gold">Brand guidelines · Version 1 · October 2026</span>
      <div class="cover-lock">{sized(horiz_ar(Pt(), CREAM, BR), 'role="img" aria-label="ولا كلمة logo"')}</div>
      <p class="tagline" lang="ar" dir="rtl">مثّلها… بس ولا كلمة!</p>
      <p class="sub">The Jordanian party game that turns any gathering into a sahra. Born in Amman, played by every Arab, wherever they live.</p>
    </div>
    <div class="cover-char">{mood('wink', 'role="img" aria-label="شمّوغ winking"')}</div>
  </div>
</section>'''

strategy = '''<section id="strategy" class="sec">
  <div class="sec-head"><span class="eyebrow">01</span><h2>Strategy</h2></div>
  <div class="cols">
    <div class="block"><h3>Positioning</h3><p class="big">The Jordanian party game that turns any gathering into a sahra.</p><p>Jordanian at heart, with the core deck proudly local. Open to the region and the world through pan-Arab categories, Arabizi on every card, and future dialect packs.</p></div>
    <div class="block"><h3>Promise</h3><p class="big" lang="ar" dir="rtl">اللعبة الأساسية مجانية دايماً، وما في إعلانات بنص اللعب.</p><p>Core deck free forever. Never an ad mid-game. No account needed, and it works offline. Sponsors appear only as labelled, opt-in packs.</p></div>
  </div>
  <div class="pillars">
    <div><b>🎭 Play</b><span>The app and its free core deck</span></div>
    <div><b>📦 Packs</b><span>Sponsored, paid, partner-unlocked and dialect packs</span></div>
    <div><b>☕ Places</b><span>Partner cafés and <bdi>«ليلة ولا كلمة»</bdi> game nights</span></div>
    <div><b>👥 People</b><span>Community, creators, challenges, user-made cards</span></div>
  </div>
  <div class="tablewrap"><table><thead><tr><th>Audience</th><th>What they want</th><th>Angle</th></tr></thead><tbody>
    <tr><td>Jordanians in Jordan</td><td>Family nights, friends’ sahras, Ramadan</td><td>Insider jokes, <bdi>«جمعة العيلة»</bdi></td></tr>
    <tr><td>Diaspora</td><td>A piece of home, a game for the kids</td><td>Nostalgia, Arabizi, <bdi>«ريحة البلد»</bdi></td></tr>
    <tr><td>Wider Arab world</td><td>A fun Arabic party game</td><td>Shared culture, dialect packs</td></tr>
    <tr><td>Youth and Gen Z</td><td>Chaos, laughs, content to post</td><td>TikTok challenges, the <bdi>شباب</bdi> pack</td></tr>
    <tr><td>Kids and families</td><td>Easy, safe, cute</td><td><bdi>شمّوغ</bdi>, a future <bdi>«صغار»</bdi> pack</td></tr>
  </tbody></table></div>
  <p class="note">Personality: <b>warm</b> like a majlis, <b>cheeky</b> like your favourite cousin, <b>proud</b> of where it comes from. Never formal, never cringe.</p>
</section>'''

voice = '''<section id="voice" class="sec">
  <div class="sec-head"><span class="eyebrow">02</span><h2>Voice</h2><p>The cousin who runs every family sahra: warm, quick, a little cheeky, and everyone feels included.</p></div>
  <div class="formula"><span lang="ar" dir="rtl">«<i>___</i>ها… بس ولا كلمة!»</span><p>The brand formula: a verb with <bdi>ها</bdi>, an ellipsis, then the name. Master tagline <bdi>«مثّلها… بس ولا كلمة!»</bdi>, campaign line <bdi>«ولّعها… بس بدون حكي!»</bdi>, and spin-offs like <bdi>«رمضنها»</bdi>, <bdi>«عيّدها»</bdi> and <bdi>«اشربها»</bdi>.</p></div>
  <div class="tablewrap"><table><thead><tr><th>Arabic</th><th>Arabizi</th><th>English</th></tr></thead><tbody>
    <tr><td lang="ar" dir="rtl">مثّلها… بس ولا كلمة!</td><td><i>Massilha… bas wala kelmeh!</i></td><td>Act it out. Not a word.</td></tr>
    <tr><td lang="ar" dir="rtl">ولّعها… بس بدون حكي!</td><td><i>Walla3ha… bas bdoon 7aki!</i></td><td>Light it up. No talking.</td></tr>
    <tr><td lang="ar" dir="rtl">السهرة بتبلّش هون</td><td><i>Il sahra btballish hon</i></td><td>The sahra starts here.</td></tr>
  </tbody></table></div>
  <div class="cols">
    <div class="block"><h3>Tone by channel</h3><ul>
      <li><b>TikTok, Reels:</b> loud. Full Jordanian, Arabizi, emoji.</li>
      <li><b>Instagram, WhatsApp:</b> lively. Jordanian, 1 to 3 emoji.</li>
      <li><b>In the app:</b> friendly and short: <bdi>«جاهزين؟»، «خلص الوقت!»</bdi></li>
      <li><b>Stores, partners:</b> clear, softer Levantine.</li>
      <li><b>Legal, support:</b> calm and plain, no jokes.</li></ul></div>
    <div class="block"><h3>Off-limits</h3><ul>
      <li>Politics and political figures</li><li>Religion or religious practice (Ramadan and Eid are celebrated, never mocked)</li>
      <li>Tribes, family names, origins</li><li>Other dialects or regions as a punchline</li><li>The royal family</li><li>Appearance, disability, gender or class</li></ul></div>
  </div>
  <p class="note">Name: <b lang="ar">ولا كلمة</b> · <b>Wala Kelmeh</b> · handles <code>walakelmeh</code>. Arabizi uses 3 = ع, 7 = ح, 2 = ء, kh, gh, sh. Full guide: <code>docs/brand/02-voice-and-tone.md</code></p>
</section>'''

logo = f'''<section id="logo" class="sec">
  <div class="sec-head"><span class="eyebrow">03</span><h2>Logo</h2><p>A shemagh-red patch with the cream flag star in a cross-stitched frame, and the name hand-stitched on a tatreez grid, with two flag stars for the dots of ة. Arabic and English never share a lockup.</p></div>
  <div class="grid2">
    {fig(horiz_ar(Pt()), 'cream', 'Arabic horizontal · symbol on the right', 'Arabic horizontal lockup')}
    {fig(horiz_en(Pt()), 'cream', 'English horizontal · symbol on the left', 'English horizontal lockup')}
    {fig(stacked_single(Pt(), 'ar'), 'cream', 'Arabic stacked', 'Arabic stacked lockup')}
    {fig(stacked_single(Pt(), 'en'), 'night', 'English stacked, on dark', 'English stacked lockup')}
  </div>
  <div class="grid4">
    {fig(Pt(), 'cream sym', 'Primary symbol', 'Primary symbol')}
    {fig(icon_C('cream'), 'night sym', 'Light alternative', 'Cream patch')}
    {fig(icon_star_only(gid('so')), 'cream sym', 'Below 48px', 'Small symbol')}
    {fig(symbol_mono(INK), 'cream sym', 'One colour', 'Mono symbol')}
  </div>
  <div class="grid3">
    {fig(wordmark(AR_ROWS, INK, RED), 'cream', 'On light: ink stitches, red stars', 'Wordmark on light')}
    {fig(wordmark(AR_ROWS, CREAM, BR), 'night', 'On dark: cream, bright red stars', 'Wordmark on dark')}
    {fig(wordmark(AR_ROWS, CREAM, GOLD), 'red', 'On red: cream, gold stars', 'Wordmark on red')}
  </div>
  <figure class="tile cream">{sized(BG.clearspace(), 'role="img" aria-label="Clear space"')}<figcaption>Clear space: x on every side, where x = symbol height ÷ 4</figcaption></figure>
  <div class="tablewrap"><table><thead><tr><th>Element</th><th>Screen min</th><th>Print min</th><th>Below that</th></tr></thead><tbody>
    <tr><td>Symbol with frame</td><td>48px</td><td>12mm</td><td>Star-only symbol</td></tr>
    <tr><td>Stitched wordmark (letter height)</td><td>40px</td><td>12mm</td><td>Filled-square version</td></tr>
    <tr><td>Horizontal lockup (width)</td><td>200px</td><td>45mm</td><td>Symbol alone</td></tr></tbody></table></div>
  <h3>Don’t</h3>
  <div class="grid3">
    {fig(BG.dont_mixed(), 'cream dont', 'Mix Arabic and English in one lockup', 'Misuse: mixed')}
    {fig(BG.dont_gold(), 'cream dont', 'Recolour the stars', 'Misuse: gold stars')}
    {fig(BG.dont_rotate(), 'cream dont sym', 'Rotate the star', 'Misuse: rotated')}
  </div>
  <h3>Partners and sponsors</h3>
  <div class="grid2">
    {fig(partner_lockup('ar'), 'cream', 'Partner lockup: our mark leads, a stitched divider, then the partner', 'Partner lockup')}
    {fig(partner_badge('ar'), 'cream sym', 'Partner badge for café windows', 'Partner badge')}
  </div>
  {fig(sponsor_pill('ar', 'light'), 'cream', 'Sponsored-pack label: always labelled, always opt-in', 'Sponsored pack label')}
</section>'''

swl = ''.join(BS.chip(*c[:4]) for c in BS.light)
swd = ''.join(BS.chip(*c) for c in BS.dark)
colour = f'''<section id="colour" class="sec">
  <div class="sec-head"><span class="eyebrow">04</span><h2>Colour · Sahra</h2><p>Cream fabric by day, night majlis after dark. Shemagh red leads, and olive, gold and indigo work as tatreez threads. These are the same tokens the app runs on.</p></div>
  <div class="panel"><div class="swatches">{swl}</div>
    <div class="ratio"><div style="flex:60;background:#f4ecdd;color:#2a1f1a">Cream 60%</div><div style="flex:25;background:#2a1f1a;color:#f4ecdd">Ink 25%</div><div style="flex:10;background:#b5121b;color:#fff8ee">Red 10%</div><div style="flex:5;background:linear-gradient(90deg,#4f6b2c,#b9861f,#3b3f7a)"></div></div></div>
  <div class="panel nightpanel"><h3>Night majlis</h3><div class="swatches">{swd}</div></div>
  <div class="tablewrap"><table><thead><tr><th>Pair</th><th>Ratio</th><th>Level</th><th>Rule</th></tr></thead><tbody>{''.join(BS.row(c) for c in BS.contrast)}</tbody></table></div>
  <p class="note">Small red or gold text uses <code>--red-text</code> and <code>--warn-text</code>, tuned for 4.5:1 in both themes. Tokens: <code>brand/tokens/sahra.css</code></p>
</section>'''

type_ = '''<section id="type" class="sec">
  <div class="sec-head"><span class="eyebrow">05</span><h2>Type</h2><p>Almarai for headlines, Cairo for everything else, in Arabic and Latin. The stitched lettering belongs to the logo only.</p></div>
  <div class="panel">
    <div class="type-row"><span class="meta">Display · Almarai 800 · 40/48</span><span class="ar" style="font:800 40px/1.2 var(--display);color:var(--red-text)">مثّلها… بس ولا كلمة!</span></div>
    <div class="type-row"><span class="meta">H1 · Almarai 800 · 32/40</span><span class="ar" style="font:800 32px/1.25 var(--display)">مين أسرع؟</span></div>
    <div class="type-row"><span class="meta">H2 · Almarai 700 · 24/32</span><span class="ar" style="font:700 24px/1.35 var(--display)">أكل وشرب · ٤٠ بطاقة</span></div>
    <div class="type-row"><span class="meta">Body · Cairo 400 · 16/28</span><span class="ar" style="font:400 16px/1.75 var(--font)">اسحب البطاقة يمين إذا فريقك عرفها، ويسار إذا بدك تتخطّاها. عندكم دقيقة وحدة… يلا!</span></div>
    <div class="type-row"><span class="meta">Latin · Cairo 600 · 16/26</span><span style="font:600 16px/1.6 var(--font)">Act it out. Not a word.</span></div>
  </div>
  <p class="note">Eastern Arabic numerals «٣» in Arabic copy, 3 in Latin. Never letter-space Arabic. Never set body text in gold.</p>
</section>'''

pattern = f'''<section id="pattern" class="sec">
  <div class="sec-head"><span class="eyebrow">06</span><h2>Pattern</h2><p>Four textile devices. Use one or two per layout, never all four.</p></div>
  <div class="patterns">
    <figure class="pat"><div class="ptile shemagh"></div><figcaption><b>Shemagh weave:</b> bands, card backs, behind the logo</figcaption></figure>
    <figure class="pat"><div class="ptile band">{sized(BS.band_svg(), 'role="img" aria-label="Tatreez band"')}</div><figcaption><b>Tatreez band:</b> section edges, headers, poster bottoms</figcaption></figure>
    <figure class="pat"><div class="ptile"><div class="runner"></div></div><figcaption><b>Running stitch:</b> dashed borders on cards and avatars</figcaption></figure>
    <figure class="pat"><div class="ptile"><div class="xrow" aria-hidden="true">✕ ✕ ✕ ✕ ✕ ✕</div></div><figcaption><b>Cross-stitch row:</b> dividers, bullets, the partner separator</figcaption></figure>
  </div>
</section>'''

def arts(items, label):
    return ''.join(f'<figure class="art">{sized(BS.stitch_art(r), f"role=img aria-label=\"{l}\"")}<figcaption>{l}</figcaption></figure>' for l, r in items)
illus = f'''<section id="illustration" class="sec">
  <div class="sec-head"><span class="eyebrow">07</span><h2>Illustration</h2><p>Cross-stitch on cream fabric: one X per square, five threads only (red, olive, gold, ink, indigo), grids of about 8 to 12 squares.</p></div>
  <div class="arts">{arts([(c or k, r) for k, c, r in BS.cats], 'cat')}</div>
  <div class="arts">{arts(BS.avs, 'av')}{arts([(c or k, r) for k, c, r in BS.modes], 'mode')}</div>
</section>'''

sheet = ''.join(f'<figure class="pose">{mood(k, f"role=img aria-label=\"{en}\"")}<figcaption><span class="say" lang="ar" dir="rtl">{ar}</span><span>{en}</span></figcaption></figure>' for k, (ar, en, f) in MOODS.items())
mascot = f'''<section id="mascot" class="sec">
  <div class="sec-head"><span class="eyebrow">08</span><h2><bdi lang="ar">شمّوغ</bdi> · Shammogh</h2><p>A living shemagh: the cloth itself, with a face. A cheeky troublemaker who can’t stop talking, in a game where talking isn’t allowed. No hands: it gestures with its face, its body and the props around it.</p></div>
  <div class="sheet">{sheet}</div>
  <div class="cols">
    <div class="block"><h3>Do</h3><ul><li>Keep it beside the logo, never inside it</li><li>One شمّوغ per screen or post</li><li>Let it react to the game</li><li>Shh is always the stitched-shut mouth</li></ul></div>
    <div class="block"><h3>Don’t</h3><ul><li>Add hands, arms or fingers</li><li>Recolour the pattern or use blue</li><li>Stretch it beyond the built-in moods</li><li>Give it other brands’ products</li></ul></div>
  </div>
</section>'''

files = '''<section id="files" class="sec">
  <div class="sec-head"><span class="eyebrow">09</span><h2>Files</h2><p>Everything lives in the repo on the brand branch. Use SVG wherever you can.</p></div>
  <div class="tablewrap"><table><thead><tr><th>Folder</th><th>What’s inside</th></tr></thead><tbody>
    <tr><td><code>brand/logo/symbol/</code></td><td>Primary, light, small, mono ink and white</td></tr>
    <tr><td><code>brand/logo/wordmark/</code></td><td>Arabic and English: on light, dark, red, small, mono</td></tr>
    <tr><td><code>brand/logo/lockup/</code></td><td>Horizontal and stacked, each language, light and dark</td></tr>
    <tr><td><code>brand/logo/partner/</code></td><td>Partner lockups, badges, sponsored-pack labels</td></tr>
    <tr><td><code>brand/logo/png/</code></td><td>App icon 1024 to 180, favicon 48 to 16, store icon, lockups at 1600px</td></tr>
    <tr><td><code>brand/tokens/</code></td><td>Sahra colours and type as CSS and JSON</td></tr>
    <tr><td><code>brand/mascot/svg/</code></td><td>شمّوغ, 14 moods</td></tr>
    <tr><td><code>brand/mascot/stickers/</code></td><td>WhatsApp-ready stickers (512px WebP under 100 KB) and tray icon</td></tr>
    <tr><td><code>brand/tools/</code></td><td>The scripts that draw all of the above</td></tr>
    <tr><td><code>docs/brand/</code></td><td>Written rules: strategy, voice, logo, colour and type, mascot</td></tr>
  </tbody></table></div>
  <p class="note">Questions about the brand: The Wala Kelmeh team · <span class="sel">hello@walakelmeh.com</span></p>
</section>'''

page = f'''<title>Wala Kelmeh Brand Guidelines</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Almarai:wght@400;700;800&family=Cairo:wght@400;600;800&display=swap">
<style>
/* Layout: a night-majlis cover, a sticky stitched contents bar, then numbered chapters on cream fabric. */
:root {{ --bg:#f4ecdd; --surface:#fbf6ec; --line:#dccbae; --stitch:#c7b08a; --text:#2a1f1a; --muted:#7a6650; --red:#b5121b; --red-text:#b5121b; --on-red:#fff8ee; --olive:#4f6b2c; --gold:#b9861f;
  --night:#17110e; --weave:rgba(90,60,30,.035);
  --display:'Almarai','Cairo',system-ui,sans-serif; --font:'Cairo',system-ui,-apple-system,'Segoe UI',sans-serif; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#17110e; --surface:#231a15; --line:#3f3128; --stitch:#6a5442; --text:#f4ecdd; --muted:#b5a28a; --red-text:#ec5f66; --olive:#8aa75a; --gold:#ddae4a; --weave:rgba(255,240,220,.025); color-scheme:dark; }} }}
:root[data-theme="dark"] {{ --bg:#17110e; --surface:#231a15; --line:#3f3128; --stitch:#6a5442; --text:#f4ecdd; --muted:#b5a28a; --red-text:#ec5f66; --olive:#8aa75a; --gold:#ddae4a; --weave:rgba(255,240,220,.025); color-scheme:dark; }}
* {{ box-sizing:border-box; }}
html {{ scroll-behavior:smooth; }}
@media (prefers-reduced-motion: reduce) {{ html {{ scroll-behavior:auto; }} }}
body {{ background:var(--bg); color:var(--text); font:16px/1.6 var(--font);
  background-image:repeating-linear-gradient(0deg,var(--weave) 0 1px,transparent 1px 6px),repeating-linear-gradient(90deg,var(--weave) 0 1px,transparent 1px 6px); }}
body::before {{ content:""; position:fixed; inset:0 0 auto; height:env(safe-area-inset-top, 0px); z-index:10; background:#17110e; }}
h1,h2,h3 {{ font-family:var(--display); margin:0; line-height:1.2; text-wrap:balance; }}
h2 {{ font-size:clamp(28px,4vw,38px); }} h3 {{ font-size:19px; }}
p {{ margin:0; max-width:68ch; }}
.eyebrow {{ font-size:13px; letter-spacing:.12em; text-transform:uppercase; color:var(--red-text); font-weight:800; }}
.eyebrow.gold {{ color:#ddae4a; }}
.cover {{ background:radial-gradient(110% 90% at 75% 30%, #2e231c 0%, #17110e 62%); color:#f4ecdd; padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); padding-block:44px 36px; border-bottom:14px solid transparent; border-image:repeating-linear-gradient(45deg,#b5121b 0 7px,#f6efe3 7px 14px) 14; }}
.cover-in {{ max-width:1120px; margin:0 auto; display:grid; grid-template-columns:minmax(0,1.3fr) minmax(0,1fr); gap:24px; align-items:center; }}
.cover-text {{ display:grid; gap:16px; }}
.cover-lock svg {{ width:min(100%, 520px); height:auto; }}
.tagline {{ font-family:var(--display); font-weight:800; font-size:clamp(26px,4vw,38px); color:#f6efe3; text-align:start; }}
.sub {{ color:#d9c9b2; font-size:17px; }}
.cover-char svg {{ width:100%; max-width:380px; height:auto; justify-self:center; display:block; margin-inline:auto; filter:drop-shadow(0 18px 30px rgba(0,0,0,.45)); }}
nav.toc {{ position:sticky; top:env(safe-area-inset-top, 0px); z-index:5; background:var(--surface); border-bottom:2px dashed var(--stitch); }}
nav.toc .in {{ max-width:1120px; margin:0 auto; display:flex; gap:4px; overflow-x:auto; padding-block:8px; padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); }}
nav.toc a {{ color:var(--text); text-decoration:none; font-weight:700; font-size:14px; padding:6px 12px; border-radius:999px; white-space:nowrap; }}
nav.toc a:hover, nav.toc a:focus-visible {{ background:var(--red); color:var(--on-red); outline:none; }}
main {{ max-width:1120px; margin:0 auto; padding-block:12px 80px; padding-left:max(16px, env(safe-area-inset-left, 0px)); padding-right:max(16px, env(safe-area-inset-right, 0px)); display:grid; gap:64px; }}
.sec {{ display:grid; gap:20px; scroll-margin-top:64px; }}
.sec-head {{ display:grid; gap:8px; padding-top:28px; border-top:2px dashed var(--stitch); }}
.sec-head p {{ color:var(--muted); }}
.cols {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(280px,1fr)); gap:16px; }}
.block, .panel {{ background:var(--surface); border:1px solid var(--line); border-radius:18px; padding:20px; display:grid; gap:10px; align-content:start; min-width:0; }}
.block ul {{ margin:0; padding-inline-start:18px; display:grid; gap:4px; }}
.big {{ font-family:var(--display); font-weight:800; font-size:22px; line-height:1.35; }}
.pillars {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(200px,1fr)); gap:12px; }}
.pillars div {{ background:var(--surface); border:2px dashed var(--stitch); border-radius:16px; padding:14px 16px; display:grid; gap:4px; }}
.pillars span {{ color:var(--muted); font-size:14px; }}
.formula {{ background:var(--red); color:var(--on-red); border-radius:20px; padding:22px; display:grid; gap:8px; }}
.formula span {{ font-family:var(--display); font-weight:800; font-size:clamp(28px,5vw,44px); }}
.formula i {{ font-style:normal; border-bottom:4px dashed #fff8ee; padding-inline:8px; }}
.formula p {{ color:#ffe7e3; }}
.note {{ color:var(--muted); font-size:14px; }}
code {{ font-size:13px; background:var(--surface); padding:1px 6px; border-radius:6px; border:1px solid var(--line); }}
.tablewrap {{ overflow-x:auto; background:var(--surface); border:1px solid var(--line); border-radius:16px; }}
table {{ border-collapse:collapse; width:100%; font-size:14px; }}
th,td {{ text-align:start; padding:10px 12px; border-bottom:1px solid var(--line); vertical-align:top; }}
th {{ font-family:var(--display); color:var(--muted); font-size:13px; }}
.num {{ font-variant-numeric:tabular-nums; white-space:nowrap; }}
.pill {{ font-size:12px; font-weight:700; padding:2px 10px; border-radius:999px; white-space:nowrap; }}
.pill.good {{ background:color-mix(in srgb, var(--olive) 18%, transparent); color:var(--olive); }}
.pill.warn {{ background:color-mix(in srgb, var(--gold) 22%, transparent); color:var(--text); }}
.pill.bad {{ background:color-mix(in srgb, var(--red) 15%, transparent); color:var(--red-text); }}
.grid2 {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(300px,1fr)); gap:14px; }}
.grid3 {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:14px; }}
.grid4 {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(160px,1fr)); gap:14px; }}
.tile {{ margin:0; border-radius:16px; padding:20px; display:grid; gap:12px; align-content:space-between; justify-items:center; min-width:0; }}
.tile svg {{ width:100%; height:auto; max-height:230px; }}
.tile figcaption {{ font-size:13px; justify-self:start; }}
.tile.cream {{ background:#f6efe3; border:1px solid var(--line); }} .tile.cream figcaption {{ color:#6f5c47; }}
.tile.night {{ background:#17110e; border:1px solid #3f3128; }} .tile.night figcaption {{ color:#b5a28a; }}
.tile.red {{ background:#b5121b; }} .tile.red figcaption {{ color:#f6dcd0; }}
.tile.sym svg {{ max-width:140px; }}
.dont {{ position:relative; }}
.dont::after {{ content:"✕"; position:absolute; top:10px; inset-inline-end:14px; color:#b5121b; font-weight:900; font-size:20px; }}
.swatches {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:12px; }}
.sw {{ display:grid; gap:2px; font-size:13px; }}
.sw span {{ height:56px; border-radius:12px; border:1px solid var(--line); }}
.sw code {{ background:none; border:0; padding:0; color:var(--muted); font-size:12px; }} .sw small {{ color:var(--muted); }}
.nightpanel {{ background:#17110e; color:#f4ecdd; border-color:#3f3128; }} .nightpanel .sw code, .nightpanel .sw small {{ color:#b5a28a; }} .nightpanel .sw span {{ border-color:#3f3128; }}
.ratio {{ display:flex; height:44px; border-radius:12px; overflow:hidden; border:1px solid var(--line); }}
.ratio div {{ display:grid; place-items:center; font-size:12px; font-weight:700; }}
.type-row {{ display:grid; grid-template-columns:170px minmax(0,1fr); gap:14px; align-items:baseline; padding-block:10px; border-bottom:1px dashed var(--line); }}
.type-row:last-child {{ border-bottom:0; }}
.type-row .meta {{ font-size:12px; color:var(--muted); }}
.ar {{ direction:rtl; text-align:right; }}
.patterns {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(220px,1fr)); gap:14px; }}
.pat {{ margin:0; display:grid; gap:8px; }}
.ptile {{ height:110px; border-radius:14px; border:1px solid var(--line); overflow:hidden; display:grid; place-items:center; background:var(--surface); }}
.ptile.shemagh {{ background:{BS.SH} repeat; background-size:18px; }}
.ptile.band svg {{ width:100%; height:auto; }}
.pat figcaption {{ font-size:13px; color:var(--muted); }}
.runner {{ width:80%; height:64px; border:2px dashed var(--stitch); border-radius:14px; }}
.xrow {{ display:flex; gap:10px; color:var(--red-text); font-weight:800; font-size:20px; }}
.arts {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(104px,1fr)); gap:10px; }}
.art {{ margin:0; background:#f7f0e3; border:1px solid #dccbae; border-radius:14px; padding:12px; display:grid; gap:6px; justify-items:center; }}
.art svg {{ width:64px; height:auto; }}
.art figcaption {{ font-size:11px; color:#6f5c47; text-align:center; line-height:1.3; }}
.sheet {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(138px,1fr)); gap:12px; }}
.pose {{ margin:0; background:#f6efe3; border:2px dashed #c7b08a; border-radius:18px; padding:10px; display:grid; gap:4px; justify-items:center; }}
.pose svg {{ width:100%; height:auto; }}
.pose figcaption {{ display:grid; justify-items:center; font-size:12px; color:#6f5c47; text-align:center; }}
.say {{ font-family:var(--display); font-weight:800; font-size:14px; color:#2a1f1a; }}
.sel {{ user-select:all; font-weight:700; color:var(--text); }}
@media (max-width:760px) {{ .cover-in {{ grid-template-columns:1fr; }} .cover-char svg {{ max-width:260px; }} .type-row {{ grid-template-columns:1fr; gap:4px; }} }}
</style>
{hero}
<nav class="toc" aria-label="Contents"><div class="in">{nav}</div></nav>
<main>
{strategy}{voice}{logo}{colour}{type_}{pattern}{illus}{mascot}{files}
</main>'''
open(os.path.join(HERE, '..', 'guidelines', 'book-body.html'), 'w').write(page)
print('ok', len(page) // 1024, 'KB')
