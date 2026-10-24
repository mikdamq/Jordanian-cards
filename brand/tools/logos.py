"""Logo concept generator for ولا كلمة / Wala Kelmeh. Outputs standalone SVG strings."""
import math, re
from textpath import glyph_list, text_path
from stitchword import ROWS

RED, RED2, RED_HI = '#b5121b', '#8e0e16', '#e0293b'
CREAM, INK, GOLD, OLIVE = '#f6efe3', '#2a1f1a', '#d9a33a', '#4f6b2c'
NIGHT = '#17110e'

def star7(cx, cy, R, ratio=0.442, rot=-90):
    pts = []
    for i in range(14):
        r = R if i % 2 == 0 else R * ratio
        a = math.radians(rot + i * 360 / 14)
        pts.append(f'{cx + r*math.cos(a):.1f},{cy + r*math.sin(a):.1f}')
    return ' '.join(pts)

def xstitch(cx, cy, s, color, w, cap='round'):
    h = s / 2
    return (f'<path d="M{cx-h:.1f} {cy-h:.1f}L{cx+h:.1f} {cy+h:.1f}M{cx+h:.1f} {cy-h:.1f}L{cx-h:.1f} {cy+h:.1f}" '
            f'stroke="{color}" stroke-width="{w}" stroke-linecap="{cap}" fill="none"/>')

def svg(vb_w, vb_h, body, extra=''):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vb_w:.0f} {vb_h:.0f}" {extra}>{body}</svg>'

GRAD = (f'<defs><linearGradient id="{{id}}" x1="0" y1="0" x2="0.4" y2="1">'
        f'<stop offset="0" stop-color="{RED_HI}"/><stop offset="1" stop-color="#8f0b1a"/></linearGradient></defs>')

def tile(gid):
    return GRAD.replace('{id}', gid) + f'<rect width="512" height="512" rx="112" fill="url(#{gid})"/>'

# ---------- Symbols (512 app-icon tiles) ----------
def icon_current():
    return svg(512, 512, tile('gc') + f'<polygon points="{star7(256,256,144)}" fill="{CREAM}"/>')

def icon_A(gid='ga'):
    """Stitched bubble: the typing dots are cross-stitches; the flag star sparks above."""
    bubble = (f'<path d="M168 128H344A80 80 0 0 1 424 208V268A80 80 0 0 1 344 348H236L156 410L170 348H168'
              f'A80 80 0 0 1 88 268V208A80 80 0 0 1 168 128Z" fill="{CREAM}"/>')
    stitches = ''.join(xstitch(x, 238, 46, RED, 19) for x in (176, 256, 336))
    star = f'<polygon points="{star7(404,132,62)}" fill="{GOLD}" stroke="#a40f1c" stroke-width="12" stroke-linejoin="round"/>'
    return svg(512, 512, tile(gid) + bubble + stitches + star)

def icon_B(gid='gb'):
    """The flag star with its mouth stitched shut."""
    body = f'<polygon points="{star7(256,266,172)}" fill="{CREAM}"/>'
    body += ''.join(xstitch(x, 272, 42, RED, 17) for x in (208, 256, 304))
    return svg(512, 512, tile(gid) + body)

def icon_C(variant='cream', gid='gcr'):
    """Embroidered patch: stitched frame around the flag star. cream = red on fabric, red = fabric on red."""
    if variant == 'cream':
        body, thread, star = f'<rect x="2" y="2" width="508" height="508" rx="110" fill="{CREAM}" stroke="#d8c6a6" stroke-width="4"/>', RED, RED
    else:
        body, thread, star = tile(gid), CREAM, CREAM
    n, inset = 9, 62
    step = (512 - 2 * inset) / (n - 1)
    pts = set()
    for i in range(n):
        p = inset + i * step
        pts |= {(p, inset), (p, 512 - inset), (inset, p), (512 - inset, p)}
    body += ''.join(xstitch(x, y, 28, thread, 10) for x, y in sorted(pts))
    body += f'<polygon points="{star7(256,262,136)}" fill="{star}"/>'
    return svg(512, 512, body)

# ---------- Wordmarks ----------
def ar_wordmark(font, size, color, mark_color, wght=None, mark='star'):
    """Outlined ولا كلمة; the dots of ة become one brand mark."""
    glyphs, width = glyph_list('ولا كلمة', font, size, wght)
    paths, mark_svg = [], ''
    for gl in glyphs:
        subs = ['M' + s for s in gl['d'].split('M') if s]
        if gl['name'] in ('uniFE94', 'uni0629.fina'):
            dots, keep = [], []
            for s in subs:
                n = [float(v) for v in re.findall(r'-?\d+\.?\d*', s)]
                ys = n[1::2]
                (dots if max(ys) < -0.47 * size else keep).append(s)
            if dots:
                cs = []
                for d in dots:
                    n = [float(v) for v in re.findall(r'-?\d+\.?\d*', d)]
                    xs, ys = n[0::2], n[1::2]
                    cs.append(((min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2))
                mx = sum(c[0] for c in cs) / len(cs)
                for cx, cy in cs:
                    sx = mx + (cx - mx) * 1.3
                    mark_svg += f'<polygon points="{star7(sx, cy - size*0.015, size*0.085)}" fill="{mark_color}"/>' if mark == 'star' else xstitch(sx, cy, size * 0.1, mark_color, size * 0.04)
            subs = keep
        paths.append(''.join(subs))
    asc, desc = size * 0.86, size * 0.42
    top = asc + size * 0.1
    body = f'<g transform="translate(0 {top:.1f})"><path d="{"".join(paths)}" fill="{color}"/>{mark_svg}</g>'
    return body, width, top + desc

def stitched_wordmark(color, dot_color, cell=14, solid=False, star_r=1.45):
    """Cross-stitch lettering. solid=True fills each cell, for small sizes where stitches blur."""
    out = []
    for r, row in enumerate(ROWS):
        for c, v in enumerate(row):
            if v == '.': continue
            if v == 'd':
                # each 2x2 dot block of ة becomes one flag star, drawn from its top-left cell
                if r > 0 and ROWS[r-1][c] == 'd' or c > 0 and row[c-1] == 'd': continue
                out.append(f'<polygon points="{star7((c + 1) * cell, (r + 1) * cell, cell * star_r)}" fill="{dot_color}"/>')
                continue
            if solid:
                out.append(f'<rect x="{c*cell:.1f}" y="{r*cell:.1f}" width="{cell+0.3:.1f}" height="{cell+0.3:.1f}" fill="{color}"/>')
            else:
                out.append(xstitch(c * cell + cell / 2, r * cell + cell / 2, cell * 0.86, color, cell * 0.34))
    return ''.join(out), len(ROWS[0]) * cell, len(ROWS) * cell

def latin(size, color, width=None, x=0, y=0, anchor='start'):
    d, w, a, de = text_path('WALA KELMEH', 'Cairo%5Bslnt%2Cwght%5D.ttf', size, x=x, y=y, wght=800, letter=size * 0.16, anchor=anchor)
    return f'<path d="{d}" fill="{color}"/>', w

def tagline(size, color, x, y):
    d, w, a, de = text_path('مثّلها… بس ولا كلمة!', 'Almarai-Bold.ttf', size, x=x, y=y, anchor='middle')
    return f'<path d="{d}" fill="{color}"/>', w

WORDMARKS = {
    'clean':    dict(font='Almarai-ExtraBold.ttf', wght=None, label='Clean · Almarai'),
    'playful':  dict(font='Marhey%5Bwght%5D.ttf', wght=700, label='Playful · Marhey'),
}

def wordmark_svg(kind, fg, mark, bg=None, solid=False):
    if kind == 'stitched':
        body, w, h = stitched_wordmark(fg, mark, solid=solid)
        pad = 20
    else:
        k = WORDMARKS[kind]
        body, w, h = ar_wordmark(k['font'], 200, fg, mark, k['wght'])
        pad = 10
    bgr = f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ''
    return svg(w + 2 * pad, h + 2 * pad, bgr + f'<g transform="translate({pad} {pad})">{body}</g>')

def stacked_lockup(icon_svg, kind, fg, mark, sub, bg=None, latin_color=None):
    """Symbol on top, Arabic wordmark, Latin name, tagline."""
    W = 900
    inner = icon_svg.split('>', 1)[1].rsplit('</svg>', 1)[0]
    parts = [f'<g transform="translate({W/2-110} 30) scale({220/512})">{inner}</g>']
    if kind == 'stitched':
        body, w, h = stitched_wordmark(fg, mark, cell=13)
    else:
        k = WORDMARKS[kind]
        body, w, h = ar_wordmark(k['font'], 170, fg, mark, k['wght'])
    y = 290
    parts.append(f'<g transform="translate({(W-w)/2:.1f} {y})">{body}</g>')
    y += h + 50
    lat, lw = latin(40, latin_color or fg, x=W / 2, y=y, anchor='middle')
    parts.append(lat)
    tg, tw = tagline(36, sub, W / 2, y + 66)
    parts.append(tg)
    H = y + 100
    bgr = f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ''
    return svg(W, H, bgr + ''.join(parts))

def horizontal_lockup(icon_svg, kind, fg, mark, bg=None, latin_color=None):
    """Arabic reads right to left, so the symbol leads on the right."""
    inner = icon_svg.split('>', 1)[1].rsplit('</svg>', 1)[0]
    if kind == 'stitched':
        body, w, h = stitched_wordmark(fg, mark, cell=10)
    else:
        k = WORDMARKS[kind]
        body, w, h = ar_wordmark(k['font'], 130, fg, mark, k['wght'])
    S = 190
    lat, lw = latin(30, fg)
    H = max(S, h + 50) + 40
    W = 30 + max(w, lw) + 40 + S + 30
    x0 = 30 + max(w, lw)
    parts = [f'<g transform="translate({x0+40} {(H-S)/2}) scale({S/512})">{inner}</g>']
    top = (H - (h + 46)) / 2
    parts.append(f'<g transform="translate({x0 - w:.1f} {top:.1f})">{body}</g>')
    lat, lw = latin(30, latin_color or fg, x=x0, y=top + h + 40, anchor='end')
    parts.append(lat)
    bgr = f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ''
    return svg(W, H, bgr + ''.join(parts))

def icon_star_only(gid='gso'):
    """Small-size symbol: the red tile and cream star without the stitched frame."""
    return svg(512, 512, tile(gid) + f'<polygon points="{star7(256,262,170)}" fill="{CREAM}"/>')
