"""Final logo system assets for ولا كلمة / Wala Kelmeh."""
import os
from logos import *
from lockups2 import *
from stitchword import ROWS as AR_ROWS
from stitchlatin import LATIN_ROWS

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logo')
BR = RED_HI
_n = [0]
def gid(p='f'): _n[0] += 1; return f'{p}{_n[0]}'

def patch(gid_):
    return icon_C('red', gid_)

def symbol_mono(color):
    """One-colour symbol: the tile in one ink with the frame and star knocked out (for stamps, embroidery, laser)."""
    n, inset = 9, 62
    step = (512 - 2 * inset) / (n - 1)
    pts = set()
    for i in range(n):
        p = inset + i * step
        pts |= {(p, inset), (p, 512 - inset), (inset, p), (512 - inset, p)}
    holes = ''.join(xstitch(x, y, 28, '#000', 10) for x, y in sorted(pts))
    holes += f'<polygon points="{star7(256,262,136)}" fill="#000"/>'
    m = gid('m')
    return svg(512, 512, f'<defs><mask id="{m}"><rect width="512" height="512" fill="#fff"/>{holes}</mask></defs>'
                         f'<rect width="512" height="512" rx="112" fill="{color}" mask="url(#{m})"/>')

def star_only_mono(color):
    m = gid('m')
    return svg(512, 512, f'<defs><mask id="{m}"><rect width="512" height="512" fill="#fff"/><polygon points="{star7(256,262,170)}" fill="#000"/></mask></defs>'
                         f'<rect width="512" height="512" rx="112" fill="{color}" mask="url(#{m})"/>')

def wordmark(rows, fg, star=RED, solid=False, cell=14, pad=None):
    b, w, h = grid_svg(rows, fg, star, cell, solid)
    pad = cell * 1.5 if pad is None else pad
    return svg(w + 2 * pad, h + 2 * pad, f'<g transform="translate({pad} {pad})">{b}</g>')

def files():
    F = {}
    # symbols
    F['symbol/symbol-primary.svg'] = patch('s1')
    F['symbol/symbol-light.svg'] = icon_C('cream')
    F['symbol/symbol-small.svg'] = icon_star_only('s2')
    F['symbol/symbol-mono-ink.svg'] = symbol_mono(INK)
    F['symbol/symbol-mono-white.svg'] = symbol_mono('#ffffff')
    F['symbol/symbol-small-mono-ink.svg'] = star_only_mono(INK)
    # wordmarks
    for lang, rows in (('arabic', AR_ROWS), ('english', LATIN_ROWS)):
        F[f'wordmark/wordmark-{lang}-on-light.svg'] = wordmark(rows, INK, RED)
        F[f'wordmark/wordmark-{lang}-on-dark.svg'] = wordmark(rows, CREAM, BR)
        F[f'wordmark/wordmark-{lang}-on-red.svg'] = wordmark(rows, CREAM, GOLD)
        F[f'wordmark/wordmark-{lang}-small-on-light.svg'] = wordmark(rows, INK, RED, solid=True)
        F[f'wordmark/wordmark-{lang}-small-on-dark.svg'] = wordmark(rows, CREAM, BR, solid=True)
        F[f'wordmark/wordmark-{lang}-mono-ink.svg'] = wordmark(rows, INK, INK)
        F[f'wordmark/wordmark-{lang}-mono-white.svg'] = wordmark(rows, '#ffffff', '#ffffff')
    # lockups
    F['lockup/lockup-arabic-horizontal-on-light.svg'] = horiz_ar(patch('l1'))
    F['lockup/lockup-arabic-horizontal-on-dark.svg'] = horiz_ar(patch('l2'), CREAM, BR)
    F['lockup/lockup-english-horizontal-on-light.svg'] = horiz_en(patch('l3'))
    F['lockup/lockup-english-horizontal-on-dark.svg'] = horiz_en(patch('l4'), CREAM)
    F['lockup/lockup-arabic-stacked-on-light.svg'] = stacked_single(patch('l5'), 'ar')
    F['lockup/lockup-arabic-stacked-on-dark.svg'] = stacked_single(patch('l6'), 'ar', CREAM, BR, '#b5a28a')
    F['lockup/lockup-english-stacked-on-light.svg'] = stacked_single(patch('l7'), 'en')
    F['lockup/lockup-english-stacked-on-dark.svg'] = stacked_single(patch('l8'), 'en', CREAM, BR, '#b5a28a')
    F['lockup/lockup-arabic-horizontal-mono-ink.svg'] = horiz_ar(symbol_mono(INK), INK, INK)
    F['lockup/lockup-english-horizontal-mono-ink.svg'] = horiz_en(symbol_mono(INK), INK)
    # partner & sponsor
    F['partner/partner-lockup-arabic.svg'] = partner_lockup('ar')
    F['partner/partner-lockup-english.svg'] = partner_lockup('en')
    F['partner/partner-badge-arabic.svg'] = partner_badge('ar')
    F['partner/partner-badge-english.svg'] = partner_badge('en')
    F['partner/sponsored-pack-badge-arabic-light.svg'] = sponsor_pill('ar', 'light')
    F['partner/sponsored-pack-badge-arabic-dark.svg'] = sponsor_pill('ar', 'dark')
    F['partner/sponsored-pack-badge-english-light.svg'] = sponsor_pill('en', 'light')
    F['partner/sponsored-pack-badge-english-dark.svg'] = sponsor_pill('en', 'dark')
    return F

def _stitch_divider(x, y0, y1, color):
    n = int((y1 - y0) / 22)
    return ''.join(xstitch(x, y0 + 11 + i * 22, 12, color, 4) for i in range(n))

def partner_lockup(lang):
    """Our horizontal lockup, a stitched divider, then the partner's logo area (placeholder)."""
    ours = horiz_ar(patch(gid())) if lang == 'ar' else horiz_en(patch(gid()))
    import re
    vb = re.search(r'viewBox="0 0 ([\d.]+) ([\d.]+)"', ours)
    ow, oh = float(vb.group(1)), float(vb.group(2))
    inner = ours.split('>', 1)[1].rsplit('</svg>', 1)[0]
    gap, pw = 40, 300
    label = 'شعار الشريك' if lang == 'ar' else 'PARTNER LOGO'
    font = 'Almarai-Bold.ttf' if lang == 'ar' else 'Cairo%5Bslnt%2Cwght%5D.ttf'
    W = ow + gap * 2 + pw + 24
    if lang == 'ar':   # reading right to left: ours on the right, partner on the left
        px, ox = 24, 24 + pw + gap * 2
        dx = 24 + pw + gap
    else:
        ox, px = 0, ow + gap * 2
        dx = ow + gap
    d, tw, a, de = text_path(label, font, 26, x=px + pw / 2, y=oh / 2 + 9, wght=None if lang == 'ar' else 700, anchor='middle')
    body = (f'<g transform="translate({ox} 0)">{inner}</g>'
            + _stitch_divider(dx, 30, oh - 30, RED)
            + f'<rect x="{px}" y="{oh/2-55}" width="{pw}" height="110" rx="14" fill="none" stroke="#b3a184" stroke-width="3" stroke-dasharray="10 8"/>'
            + f'<path d="{d}" fill="#8a755d"/>')
    return svg(W, oh, body)

def partner_badge(lang):
    """Round window/table badge for partner venues."""
    S, c = 420, 210
    ring = ''.join(xstitch(c + 176 * math.cos(math.radians(a)), c + 176 * math.sin(math.radians(a)), 16, CREAM, 5) for a in range(0, 360, 12))
    body = f'<circle cx="{c}" cy="{c}" r="{c}" fill="{RED}"/>{ring}'
    body += f'<polygon points="{star7(c, 150, 62)}" fill="{CREAM}"/>'
    if lang == 'ar':
        t1, w1, _, _ = text_path('شريك', 'Almarai-ExtraBold.ttf', 50, x=c, y=268, anchor='middle')
        t2, w2, _, _ = text_path('ولا كلمة', 'Almarai-ExtraBold.ttf', 50, x=c, y=330, anchor='middle')
    else:
        t1, w1, _, _ = text_path('WALA KELMEH', 'Cairo%5Bslnt%2Cwght%5D.ttf', 36, x=c, y=262, wght=900, letter=3, anchor='middle')
        t2, w2, _, _ = text_path('PARTNER', 'Cairo%5Bslnt%2Cwght%5D.ttf', 42, x=c, y=318, wght=900, letter=8, anchor='middle')
    body += f'<path d="{t1}" fill="{CREAM}"/><path d="{t2}" fill="{GOLD}"/>'
    return svg(S, S, body)

def sponsor_pill(lang, theme):
    """In-app label on a sponsored pack. {brand} is replaced by the sponsor's name."""
    bg, fg, line = (CREAM, INK, '#dccbae') if theme == 'light' else ('#2e231c', CREAM, '#4a3a2e')
    star_c = RED if theme == 'light' else BR
    if lang == 'ar':
        d, w, _, _ = text_path('مقدّم من الراعي · مجاني', 'Almarai-Bold.ttf', 26, x=0, y=0)
    else:
        d, w, _, _ = text_path('Presented by Sponsor · Free', 'Cairo%5Bslnt%2Cwght%5D.ttf', 24, x=0, y=0, wght=700)
    H, padx, sr = 52, 22, 13
    W = padx + w + 14 + sr * 2 + padx
    if lang == 'ar':
        sx, tx = W - padx - sr, padx
    else:
        sx, tx = padx + sr, padx + sr * 2 + 14
    body = (f'<rect x="1.5" y="1.5" width="{W-3:.1f}" height="{H-3}" rx="{(H-3)/2}" fill="{bg}" stroke="{line}" stroke-width="3"/>'
            f'<polygon points="{star7(sx, H/2, sr)}" fill="{star_c}"/>'
            f'<g transform="translate({tx:.1f} {H/2 + 9})"><path d="{d}" fill="{fg}"/></g>')
    return svg(W, H, body)

if __name__ == '__main__':
    F = files()
    for k, v in F.items():
        p = f'{ROOT}/{k}'; os.makedirs(os.path.dirname(p), exist_ok=True); open(p, 'w').write(v)
    print(len(F), 'files')
