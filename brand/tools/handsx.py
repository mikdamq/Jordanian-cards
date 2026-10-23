"""Fingerless hand options for شمّوغ, compared in the same four poses."""
import math
from sham import *
from poses import card, sparks as _sp

def end(kind, x, y, ang):
    """Draw a fingerless hand at the wrist (x,y); ang is the arm direction in degrees."""
    a = ang + 90
    o = f'stroke="{INK}" stroke-width="5"'
    if kind == 'nub':        # a plain round ball
        dx, dy = math.cos(math.radians(ang)) * 18, math.sin(math.radians(ang)) * 18
        return f'<circle cx="{x+dx:.1f}" cy="{y+dy:.1f}" r="27" fill="{HAND}" {o}/>'
    if kind == 'half':       # half circle, flat at the cuff
        return f'<g transform="translate({x} {y}) rotate({a})"><path d="M-27 0 A27 30 0 0 1 27 0 Z" fill="{HAND}" {o} stroke-linejoin="round"/></g>'
    if kind == 'mitten':     # bean with a little thumb bump, no fingers
        return (f'<g transform="translate({x} {y}) rotate({a}) scale(1.25)"><path d="M-19 0 C-22 -30 -10 -44 2 -44 C16 -44 22 -30 19 0 Z" fill="{HAND}" {o} stroke-linejoin="round"/>'
                f'<path d="M17 -10 C30 -12 32 -26 22 -28" fill="{HAND}" {o} stroke-linecap="round"/></g>')
    if kind == 'tassel':     # the shemagh's own tassel is the hand
        return (f'<g transform="translate({x} {y}) rotate({a}) scale(1.25)"><rect x="-10" y="-10" width="20" height="12" rx="5" fill="{RED2}" {o}/>'
                f'<path d="M-12 -8 L-15 -40 Q0 -50 15 -40 L12 -8 Z" fill="{RED}" {o} stroke-linejoin="round"/>'
                f'<path d="M4 -12 L6 -38" stroke="{RED2}" stroke-width="4" stroke-linecap="round"/></g>')
    return ''

def limb(kind, side, wx, wy, bend=0):
    if kind == 'none': return ''
    sx, sy = SH_L if side == 'L' else SH_R
    sl, ang = sleeve(sx, sy, wx, wy, bend)
    if kind == 'tassel':   # no cuff: the sleeve runs straight into the tassel
        sl = re.sub(r'<g transform="translate[^>]*><ellipse[^>]*/></g>', '', sl)
    return sl + end(kind, wx, wy, ang)
import re

def rest(kind, side):
    return limb(kind, side, SH_L[0] - 16, SH_L[1] + 44, -12) if side == 'L' else limb(kind, side, SH_R[0] + 16, SH_R[1] + 44, 12)

def stitched_mouth():
    xs = ''.join(f'<path d="M{x-7} 236 l14 14 M{x+7} 236 l-14 14" stroke="{RED}" stroke-width="5" stroke-linecap="round"/>' for x in (184, 206, 228))
    return f'<path d="M172 243 H240" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>' + xs

def pose(kind, p, pid):
    b = body(pid, pid + 'c')
    if p == 'wave':
        if kind == 'none':
            return b + face(('open', 'happy'), ('up', 'up'), 'grin', look=(2, 0), tilt=-6) + f'<path d="M352 150 q14 10 12 28 M368 132 q18 14 16 40" stroke="{GOLD}" stroke-width="6" fill="none" stroke-linecap="round"/>'
        return b + face(('open', 'happy'), ('up', 'up'), 'grin', look=(2, 0), tilt=-3) + rest(kind, 'L') + limb(kind, 'R', 362, 200, 26) + f'<path d="M386 158 q12 8 10 22 M398 144 q14 12 12 32" stroke="{GOLD}" stroke-width="6" fill="none" stroke-linecap="round"/>'
    if p == 'shh':
        if kind == 'none':
            return b + face('open', ('high', 'flat'), '', look=(10, 4)) + stitched_mouth()
        return b + face('open', ('high', 'flat'), 'pursed', look=(10, 4)) + rest(kind, 'L') + limb(kind, 'R', 220, 268, 54)
    if p == 'yay':
        if kind == 'none':
            return f'<g transform="translate(0 -14)">{b}{face("wide", "high", "grin")}</g>' + sparks() + ''.join(f'<path d="M{x} 404 h24" stroke="{INK}" stroke-width="5" stroke-linecap="round" opacity=".35"/>' for x in (130, 260))
        return limb(kind, 'L', 52, 168, -20) + limb(kind, 'R', 360, 168, 20) + b + face('wide', 'high', 'grin') + sparks()
    if p == 'card':
        if kind == 'none':
            return b + face(('open', 'happy'), ('up', 'high'), 'grin', look=(8, 2)) + card(360, 200, 14) + f'<path d="M392 140 l10 -10 M398 160 h14" stroke="{GOLD}" stroke-width="5" stroke-linecap="round"/>'
        return b + face(('open', 'happy'), ('up', 'high'), 'grin', look=(6, 2)) + rest(kind, 'L') + card(362, 186, 12) + limb(kind, 'R', 350, 236, 20)

KINDS = [
  ('nub', 'Round ball', 'A plain round hand. The simplest option, emoji-like.'),
  ('half', 'Half circle', 'Your idea: a half circle sitting on the cuff. Graphic and tidy.'),
  ('mitten', 'Mitten', 'A soft bean with a small thumb bump. Still no fingers, but it can hold and wave.'),
  ('tassel', 'Tassel hands', 'The sleeve ends in a red shemagh tassel, the same as its feet. The most “living shemagh”.'),
  ('none', 'No hands', 'No arms at all. Gestures come from the face, a stitched-shut mouth for shh, tilts and props that float.'),
]
POSES = [('wave', 'Hello'), ('shh', 'Shh'), ('yay', 'Got it!'), ('card', 'Your turn')]
