import re, os
HERE = os.path.dirname(os.path.abspath(__file__))
from final import *
from logos import horizontal_lockup

def sized(s, attr): return s.replace('<svg ', f'<svg {attr} ', 1)
def fig(s, cls, cap, label, attr=''):
    return f'<figure class="tile {cls}">{sized(s, f"role=img aria-label=\"{label}\" {attr}")}<figcaption>{cap}</figcaption></figure>'
P = lambda: patch(gid('g'))

# clear-space diagram around the Arabic horizontal lockup
def clearspace():
    lk = horiz_ar(P())
    vw, vh = map(float, re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', lk).groups())
    inner = lk.split('>', 1)[1].rsplit('</svg>', 1)[0]
    x = SYM / 4
    W, H = vw + 2 * x, vh + 2 * x
    sym_x = x + vw - PAD - SYM
    d = (f'<rect x="1" y="1" width="{W-2}" height="{H-2}" fill="none" stroke="#b5121b" stroke-width="2" stroke-dasharray="8 6"/>'
         f'<rect x="{x}" y="{x}" width="{vw}" height="{vh}" fill="none" stroke="#b3a184" stroke-width="1.5"/>'
         f'<g transform="translate({x} {x})">{inner}</g>'
         f'<rect x="{sym_x+x-x:.1f}" y="0" width="{x:.1f}" height="{x:.1f}" fill="#b5121b" opacity=".18"/>'
         f'<rect x="{W-x:.1f}" y="{H/2-x/2:.1f}" width="{x:.1f}" height="{x:.1f}" fill="#b5121b" opacity=".18"/>'
         f'<rect x="0" y="{H/2-x/2:.1f}" width="{x:.1f}" height="{x:.1f}" fill="#b5121b" opacity=".18"/>'
         f'<rect x="{W/2-x/2:.1f}" y="{H-x:.1f}" width="{x:.1f}" height="{x:.1f}" fill="#b5121b" opacity=".18"/>')
    for (tx, ty) in ((sym_x + x / 2, x / 2 + 6), (W - x / 2, H / 2 + 6), (x / 2, H / 2 + 6), (W / 2, H - x / 2 + 6)):
        t, *_ = text_path('x', 'Cairo%5Bslnt%2Cwght%5D.ttf', 22, x=tx, y=ty, wght=800, anchor='middle')
        d += f'<path d="{t}" fill="#b5121b"/>'
    return svg(W, H, d)

# misuse examples
def dont_stretch():
    s = horiz_ar(P()); return s.replace('<svg ', '<svg preserveAspectRatio="none" ', 1).replace('viewBox="0 0 ', 'data-x="').replace('" >', '" >')
def dont_mixed(): return horizontal_lockup(P(), 'stitched', INK, RED)
def dont_gold(): return wordmark(AR_ROWS, INK, GOLD)
def dont_effects():
    s = horiz_en(P())
    f = gid('fx')
    return s.replace('<svg ', '<svg style="overflow:visible" ', 1).replace('>', f'><defs><filter id="{f}"><feDropShadow dx="6" dy="6" stdDeviation="3" flood-color="#000" flood-opacity=".6"/></filter></defs><g filter="url(#{f})" transform="skewX(-12) translate(60 0)">', 1).replace('</svg>', '</g></svg>')
def dont_rotate():
    s = P(); return s.replace('<polygon', '<polygon transform="rotate(25 256 262)"')
def dont_red_on_red():
    return svg(600, 220, f'<rect width="600" height="220" fill="{RED}"/>' + f'<g transform="translate(20 10)">' + horiz_ar(P()).split('>', 1)[1].rsplit('</svg>', 1)[0] + '</g>')

style = re.search(r'<style>.*?</style>', open(os.path.join(HERE, 'page-style.css')).read(), re.S).group(0)
style = style.replace('</style>', '''
.grid2 { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 16px; }
.grid3 { display: grid; grid-template-columns: repeat(auto-fit, minmax(220px, 1fr)); gap: 16px; }
.tile { margin: 0; border-radius: 16px; padding: 22px; display: grid; gap: 12px; align-content: space-between; justify-items: center; min-width: 0; }
.tile svg { width: 100%; height: auto; max-height: 240px; }
.tile figcaption { font-size: 13px; justify-self: start; }
.tile.cream { background: #f6efe3; border: 1px solid var(--line); } .tile.cream figcaption { color: #6f5c47; }
.tile.night { background: #17110e; } .tile.night figcaption { color: #b5a28a; }
.tile.red { background: #b5121b; } .tile.red figcaption { color: #f6dcd0; }
.tile.sym svg { max-width: 160px; }
.dont { position: relative; }
.dont::after { content: "✕"; position: absolute; top: 10px; inset-inline-end: 14px; color: #b5121b; font-weight: 900; font-size: 20px; }
.dont svg { opacity: .9; }
table { border-collapse: collapse; width: 100%; font-size: 14px; }
th, td { text-align: start; padding: 10px 12px; border-bottom: 1px solid var(--line); vertical-align: top; }
th { font-family: var(--display); font-size: 13px; color: var(--muted); }
.tablewrap { overflow-x: auto; background: var(--surface); border: 1px solid var(--line); border-radius: 16px; }
code { font-size: 13px; background: var(--surface); padding: 1px 6px; border-radius: 6px; border: 1px solid var(--line); }
.files { columns: 2 260px; font-size: 14px; margin: 0; padding-inline-start: 18px; }
.ladder-row { display: flex; gap: 22px; align-items: end; flex-wrap: wrap; }
.ladder-row figure { margin: 0; display: grid; justify-items: center; gap: 4px; }
</style>''')

ladder = ''.join(f'<figure>{sized(P() if px >= 48 else icon_star_only(gid("so")), f"width={px} height={px}")}<figcaption>{px}px</figcaption></figure>' for px in (128, 64, 48, 32, 24, 16))

page = f'''<title>Wala Kelmeh Logo Guide</title>
<meta name="claude:viewport-fit-sides" content="cover">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Almarai:wght@700;800&family=Cairo:wght@400;600;800;900&display=swap">
{style}
<div class="wrap">
<header>
  <span class="eyebrow">Brand kit · Step 3 · Final</span>
  <h1>ولا كلمة logo guide</h1>
  <p>The approved logo: a shemagh-red patch with a cream flag star in a cross-stitched frame, and the name hand-stitched on a tatreez grid. Two flag stars stand in for the dots of ة. Arabic and English always appear in separate lockups.</p>
</header>

<section>
  <div class="sec-head"><h2>Primary lockups</h2><p>Use the horizontal lockup by default. Use the stacked one for square spaces such as avatars, posters and the splash screen.</p></div>
  <div class="grid2">
    {fig(horiz_ar(P()), 'cream', 'Arabic, horizontal', 'Arabic horizontal lockup')}
    {fig(horiz_en(P()), 'cream', 'English, horizontal', 'English horizontal lockup')}
    {fig(horiz_ar(P(), CREAM, BR), 'night', 'Arabic, horizontal, on dark', 'Arabic horizontal lockup on dark')}
    {fig(horiz_en(P(), CREAM), 'night', 'English, horizontal, on dark', 'English horizontal lockup on dark')}
    {fig(stacked_single(P(), 'ar'), 'cream', 'Arabic, stacked, with «مثّلها… بس ولا كلمة!»', 'Arabic stacked lockup')}
    {fig(stacked_single(P(), 'en'), 'cream', 'English, stacked, with “Act it out. Not a word.”', 'English stacked lockup')}
  </div>
</section>

<section>
  <div class="sec-head"><h2>Symbol</h2><p>The red patch is the app icon and the brand’s signature. Point the star straight up.</p></div>
  <div class="grid3">
    {fig(P(), 'cream sym', 'Primary: red patch', 'Primary symbol')}
    {fig(icon_C('cream'), 'night sym', 'Light alternative: cream patch, for light-mode surfaces and print on red', 'Cream patch symbol')}
    {fig(icon_star_only(gid('so')), 'cream sym', 'Small: star only, below 48px', 'Small symbol')}
    {fig(symbol_mono(INK), 'cream sym', 'One colour, ink: stamps, embroidery, laser', 'Mono ink symbol')}
    {fig(symbol_mono('#ffffff'), 'night sym', 'One colour, white', 'Mono white symbol')}
  </div>
  <div class="card"><div class="ladder-row">{ladder}</div><p style="font-size:14px;color:var(--muted)">From 48px up, use the patch with its stitched frame. Below 48px, the star stands alone on the red tile.</p></div>
</section>

<section>
  <div class="sec-head"><h2>Wordmarks</h2><p>Hand-stitched, two stitches thick. Never retype the name in a font.</p></div>
  <div class="grid2">
    {fig(wordmark(AR_ROWS, INK, RED), 'cream', 'On light: ink stitches, red stars', 'Arabic wordmark on light')}
    {fig(wordmark(LATIN_ROWS, INK), 'cream', 'On light: ink stitches', 'English wordmark on light')}
    {fig(wordmark(AR_ROWS, CREAM, BR), 'night', 'On dark: cream stitches, bright red stars', 'Arabic wordmark on dark')}
    {fig(wordmark(LATIN_ROWS, CREAM), 'night', 'On dark: cream stitches', 'English wordmark on dark')}
    {fig(wordmark(AR_ROWS, CREAM, GOLD), 'red', 'On red: cream stitches, gold stars', 'Arabic wordmark on red')}
    {fig(wordmark(LATIN_ROWS, CREAM), 'red', 'On red: cream stitches', 'English wordmark on red')}
    {fig(wordmark(AR_ROWS, INK, RED, solid=True), 'cream', 'Small version: filled squares, for anything under 40px tall', 'Small Arabic wordmark')}
    {fig(wordmark(LATIN_ROWS, INK, solid=True), 'cream', 'Small version, English', 'Small English wordmark')}
  </div>
</section>

<section>
  <div class="sec-head"><h2>Clear space and minimum sizes</h2><p><b>x</b> is a quarter of the symbol’s height. Keep at least x of empty space on every side of any lockup.</p></div>
  <figure class="tile cream">{sized(clearspace(), 'role="img" aria-label="Clear space diagram"')}<figcaption>Clear space: x on every side, where x = symbol height ÷ 4</figcaption></figure>
  <div class="tablewrap"><table>
    <thead><tr><th>Element</th><th>Screen minimum</th><th>Print minimum</th><th>Below that</th></tr></thead>
    <tbody>
      <tr><td>Symbol with frame</td><td>48px</td><td>12mm</td><td>Use the star-only symbol</td></tr>
      <tr><td>Star-only symbol</td><td>16px</td><td>5mm</td><td>Don’t go smaller</td></tr>
      <tr><td>Stitched wordmark (letter height)</td><td>40px</td><td>12mm</td><td>Use the filled-square version</td></tr>
      <tr><td>Filled-square wordmark</td><td>16px</td><td>5mm</td><td>Use the symbol alone</td></tr>
      <tr><td>Horizontal lockup (width)</td><td>200px</td><td>45mm</td><td>Use the symbol alone</td></tr>
    </tbody>
  </table></div>
</section>

<section>
  <div class="sec-head"><h2>Don’t</h2><p>Each of these breaks the logo. Use the supplied files as they are.</p></div>
  <div class="grid3">
    {fig(dont_mixed(), 'cream dont', 'Don’t mix Arabic and English in one lockup', 'Misuse: mixed scripts')}
    {fig(dont_gold(), 'cream dont', 'Don’t recolour the stars (gold only on red)', 'Misuse: gold stars on cream')}
    {fig(horiz_ar(P()).replace('<svg ', '<svg preserveAspectRatio="none" style="width:100%;height:56px" ', 1), 'cream dont', 'Don’t stretch or squash', 'Misuse: stretched')}
    {fig(dont_rotate(), 'cream dont sym', 'Don’t rotate the star: one point always faces up', 'Misuse: rotated star')}
    {fig(dont_effects(), 'cream dont', 'Don’t add shadows, skews or effects', 'Misuse: effects')}
    {fig(dont_red_on_red(), 'cream dont', 'Don’t put the red patch on red, use the cream patch there', 'Misuse: red on red')}
  </div>
</section>

<section>
  <div class="sec-head"><h2>Partners and sponsors</h2><p>Partner venues and sponsored packs get their own marks, so the brand stays recognisable next to someone else’s.</p></div>
  <div class="grid2">
    {fig(partner_lockup('ar'), 'cream', 'Partner lockup, Arabic: our mark on the right, a stitched divider, the partner’s logo on the left', 'Arabic partner lockup')}
    {fig(partner_lockup('en'), 'cream', 'Partner lockup, English: our mark on the left', 'English partner lockup')}
  </div>
  <div class="grid3">
    {fig(partner_badge('ar'), 'cream sym', 'Partner badge, Arabic: café windows, table tents, menus', 'Arabic partner badge')}
    {fig(partner_badge('en'), 'cream sym', 'Partner badge, English', 'English partner badge')}
  </div>
  <div class="grid2">
    {fig(sponsor_pill('ar', 'light'), 'cream', 'Sponsored-pack label, Arabic, light. <bdi>«الراعي»</bdi> is replaced with the sponsor’s name.', 'Arabic sponsored pack label')}
    {fig(sponsor_pill('en', 'dark'), 'night', 'Sponsored-pack label, English, dark', 'English sponsored pack label')}
  </div>
  <p style="color:var(--muted);font-size:14px">Rules: partner logos are never bigger than ours. A sponsored pack is always labelled and always opt-in, and sponsors never appear mid-turn.</p>
</section>

<section>
  <div class="sec-head"><h2>Files</h2><p>Everything is in the repo under <code>brand/logo/</code>. Use SVGs wherever possible. PNGs are for tools that can’t take SVG.</p></div>
  <ul class="files">
    <li><code>symbol/</code> primary, light, small, mono ink and white</li>
    <li><code>wordmark/</code> Arabic and English: on light, dark, red, small, mono</li>
    <li><code>lockup/</code> horizontal and stacked, each language, light and dark, mono</li>
    <li><code>partner/</code> partner lockups, badges, sponsored-pack labels</li>
    <li><code>png/</code> app icon 1024, 512, 192, 180, favicon 48, 32, 16, and lockups at 1600px</li>
  </ul>
</section>
</div>'''
open(os.path.join(HERE, 'out-logo-guide.html'), 'w').write(page)
print('ok')
