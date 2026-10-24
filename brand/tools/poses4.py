"""شمّوغ, final direction: no hands. Gestures come from the face, body and props."""
import math
from sham import *
from poses import phone, heart, flag, shades, tear, card, think_dots, lines_up
from handsx import stitched_mouth

def star7(cx, cy, R, r=None):
    r = r or R * .45
    return ' '.join(f'{cx + (R if i % 2 == 0 else r) * math.cos(math.radians(-90 + i * 360 / 14)):.1f},{cy + (R if i % 2 == 0 else r) * math.sin(math.radians(-90 + i * 360 / 14)):.1f}' for i in range(14))
def twinkle(x, y, R, c=GOLD): return f'<polygon points="{star7(x, y, R)}" fill="{c}" stroke="{INK}" stroke-width="3" stroke-linejoin="round"/>'
def motion(side=1):
    x = 206 + side * 150
    return f'<path d="M{x} 150 q{14*side} 10 {12*side} 28 M{x+16*side} 132 q{18*side} 14 {16*side} 40" stroke="{GOLD}" stroke-width="6" fill="none" stroke-linecap="round"/>'
def shake():
    return ''.join(f'<path d="M{x} {y} q{dx} 8 0 16" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round" opacity=".5"/>' for x, y, dx in ((44, 200, -10), (34, 230, -10), (368, 200, 10), (378, 230, 10)))
def steam():
    return ''.join(f'<path d="M{x} {y} q-10 -12 0 -24 q10 -12 0 -24" stroke="#9a8a7c" stroke-width="7" fill="none" stroke-linecap="round"/>' for x, y in ((90, 92), (322, 92)))
def jump_lines(): return ''.join(f'<path d="M{x} 410 h26" stroke="{INK}" stroke-width="5" stroke-linecap="round" opacity=".35"/>' for x, y in ((122, 0), (264, 0)))
def lift(inner, dy=-14, sy=1.0):
    return f'<g transform="translate(206 400) scale(1 {sy}) translate(-206 -400) translate(0 {dy})">{inner}</g>'
def drops(): return ''.join(f'<path d="M{x} {y} q-6 10 0 14 q6 -4 0 -14Z" fill="#c7b08a" stroke="{INK}" stroke-width="2.5"/>' for x, y in ((150, 44), (190, 30), (232, 40), (268, 26)))
def cloud(): return f'<path d="M140 24 q-30 0 -30 -22 q0 -22 30 -20 q8 -22 36 -18 q24 -20 52 0 q30 -4 32 22 q22 4 18 24 q-2 16 -24 14 Z" transform="translate(0 6)" fill="#efe4cf" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'

P = {}
def pose(key, ar, en):
    def deco(fn): P[key] = (ar, en, fn); return fn
    return deco

@pose('wave', '«أهلين!»', 'Hello')
def _(pid): return f'<g transform="rotate(-5 206 400)">{body(pid, pid+"c")}{face(("open", "happy"), ("up", "up"), "grin", look=(2, 0))}</g>' + motion(1)
@pose('wink', '«تمام!»', 'All good')
def _(pid): return body(pid, pid+'c') + face(('open', 'happy'), ('up', 'high'), 'smirk', look=(3, 1)) + twinkle(342, 118, 24) + twinkle(372, 166, 12, RED)
@pose('shh', '«ششش… ولا كلمة!»', 'Shh')
def _(pid): return body(pid, pid+'c') + face('open', ('high', 'flat'), '', look=(10, 4)) + stitched_mouth()
@pose('laugh', '«هههههه»', 'Laughing')
def _(pid): return f'<g transform="rotate(4 206 400)">{body(pid, pid+"c")}{face("happy", "up", "laugh", blush=True)}</g>' + shake()
@pose('yay', '«يااا صح!»', 'Got it!')
def _(pid): return lift(body(pid, pid+'c') + face('wide', 'high', 'grin'), -18) + sparks() + jump_lines()
@pose('think', '«همم…»', 'Thinking')
def _(pid): return body(pid, pid+'c') + face('open', ('flat', 'high'), 'smirk', look=(8, -10), tilt=-4) + think_dots()
@pose('shock', '«شو؟!»', 'Shocked')
def _(pid): return lift(body(pid, pid+'c') + face('wide', 'high', 'o'), -6, 1.03) + lines_up()
@pose('headsup', '«عالجبين!»', 'Heads up')
def _(pid): return body(pid, pid+'c') + face('open', 'up', 'grin', look=(0, -12)) + phone(206, 98) + f'<path d="M120 70 l-12 -10 M292 70 l12 -10" stroke="{GOLD}" stroke-width="5" stroke-linecap="round"/>'
@pose('cool', '«ولا يهمك»', 'Cool')
def _(pid): return body(pid, pid+'c') + face('open', ('flat', 'up'), 'smirk', extras=shades()) + twinkle(296, 190, 9, '#fff') + sparks()
@pose('sad', '«خسرنا…»', 'Lost the round')
def _(pid): return lift(body(pid, pid+'c') + face('sad', 'sad', 'frown', look=(0, 6), extras=tear(258, 230)), 6, .97) + cloud() + drops()
@pose('love', '«بحبكم!»', 'Love')
def _(pid): return body(pid, pid+'c') + face('happy', 'up', 'smile', blush=True) + heart(338, 116, .9) + heart(372, 170, .55) + heart(72, 150, .6)
@pose('proud', '«نشامى!»', 'Proud, with the flag')
def _(pid): return flag(352, 380) + body(pid, pid+'c', agal=True) + face(('open', 'happy'), 'up', 'grin', look=(4, 0))
@pose('compete', '«جد؟!»', 'Game on')
def _(pid): return body(pid, pid+'c') + face('angry', 'angry', 'teeth') + steam()
@pose('card', '«مثّلها!»', 'Your turn')
def _(pid): return body(pid, pid+'c') + face(('open', 'happy'), ('up', 'high'), 'grin', look=(8, 2)) + card(358, 200, 14) + f'<path d="M392 140 l10 -10 M398 162 h14" stroke="{GOLD}" stroke-width="5" stroke-linecap="round"/>'
