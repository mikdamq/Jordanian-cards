"""Single-language lockups: Arabic only (symbol on the right) and English only (symbol on the left)."""
from logos import *
from stitchword import ROWS as AR_ROWS
from stitchlatin import LATIN_ROWS

def grid_svg(rows, color, dot_color=RED, cell=14, solid=False, star_r=1.45):
    out, squares = [], []
    for r, row in enumerate(rows):
        for c, v in enumerate(row):
            if v == '.': continue
            if v == 'd':
                if r > 0 and rows[r-1][c] == 'd' or c > 0 and row[c-1] == 'd': continue
                out.append(f'<polygon points="{star7((c + 1) * cell, (r + 1) * cell, cell * star_r)}" fill="{dot_color}"/>')
            elif solid:
                # one path for every square, so neighbouring cells merge without hairline seams
                squares.append(f'M{c*cell:.2f} {r*cell:.2f}h{cell}v{cell}h-{cell}Z')
            else:
                out.append(xstitch(c * cell + cell / 2, r * cell + cell / 2, cell * 0.86, color, cell * 0.34))
    if squares:
        out.insert(0, f'<path d="{"".join(squares)}" fill="{color}"/>')
    return ''.join(out), len(rows[0]) * cell, len(rows) * cell

def _inner(icon): return icon.split('>', 1)[1].rsplit('</svg>', 1)[0]
CELL = 12
CAP = 12 * CELL           # letter band height (rows 0-11 in both scripts)
SYM = CAP * 1.3           # symbol a little taller than the letters
GAP = 4 * CELL
PAD = 24

def horiz_ar(icon, fg=INK, star=RED, bg=None):
    word, w, h = grid_svg(AR_ROWS, fg, star, CELL)
    top = PAD + (SYM - CAP) / 2
    W = PAD + w + GAP + SYM + PAD
    H = max(PAD + SYM + PAD, top + h + PAD)
    body = (f'<g transform="translate({PAD} {top})">{word}</g>'
            f'<g transform="translate({PAD + w + GAP} {PAD}) scale({SYM/512})">{_inner(icon)}</g>')
    bgr = f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ''
    return svg(W, H, bgr + body)

def horiz_en(icon, fg=INK, style='stitched', bg=None):
    if style == 'stitched':
        word, w, h = grid_svg(LATIN_ROWS, fg, cell=CELL)
    else:
        size = CAP / 0.72
        d, w, a, de = text_path('WALA KELMEH', 'Cairo%5Bslnt%2Cwght%5D.ttf', size, x=0, y=CAP, wght=900, letter=size * 0.08)
        word, h = f'<path d="{d}" fill="{fg}"/>', CAP
    top = PAD + (SYM - CAP) / 2
    W = PAD + SYM + GAP + w + PAD
    H = PAD + SYM + PAD
    body = (f'<g transform="translate({PAD} {PAD}) scale({SYM/512})">{_inner(icon)}</g>'
            f'<g transform="translate({PAD + SYM + GAP} {top})">{word}</g>')
    bgr = f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ''
    return svg(W, H, bgr + body)

def stacked_single(icon, lang, fg=INK, star=RED, sub='#7a6650', bg=None):
    W = 900
    parts = [f'<g transform="translate({W/2-110} 30) scale({220/512})">{_inner(icon)}</g>']
    y = 300
    if lang == 'ar':
        word, w, h = grid_svg(AR_ROWS, fg, star, 13)
        parts.append(f'<g transform="translate({(W-w)/2:.1f} {y})">{word}</g>')
        d, tw, a, de = text_path('مثّلها… بس ولا كلمة!', 'Almarai-Bold.ttf', 38, x=W/2, y=y + h + 60, anchor='middle')
    else:
        word, w, h = grid_svg(LATIN_ROWS, fg, cell=7)
        parts.append(f'<g transform="translate({(W-w)/2:.1f} {y})">{word}</g>')
        d, tw, a, de = text_path('Act it out. Not a word.', 'Cairo%5Bslnt%2Cwght%5D.ttf', 36, x=W/2, y=y + h + 60, wght=600, anchor='middle')
    parts.append(f'<path d="{d}" fill="{sub}"/>')
    H = y + h + 100
    bgr = f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ''
    return svg(W, H, bgr + ''.join(parts))
