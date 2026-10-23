from sham import *

def phone(x, y, a=0):
    return (f'<g transform="translate({x} {y}) rotate({a})"><rect x="-74" y="-30" width="148" height="60" rx="12" fill="{INK}"/>'
            f'<rect x="-62" y="-22" width="124" height="44" rx="6" fill="{RED}"/>'
            f'<text x="0" y="7" font-family="Almarai, Cairo, sans-serif" font-weight="800" font-size="24" fill="#fff8ee" text-anchor="middle">منسف</text></g>')
def heart(x, y, s=1):
    return f'<path transform="translate({x} {y}) scale({s})" d="M0 18 C-30 -4 -26 -30 -8 -30 C-2 -30 0 -24 0 -22 C0 -24 2 -30 8 -30 C26 -30 30 -4 0 18Z" fill="{RED3}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
def flag(x, y):
    """Jordan flag on a pole held at (x,y)."""
    import math
    def star7(cx, cy, R, r):
        return ' '.join(f'{cx + (R if i % 2 == 0 else r) * math.cos(math.radians(-90 + i * 360 / 14)):.1f},{cy + (R if i % 2 == 0 else r) * math.sin(math.radians(-90 + i * 360 / 14)):.1f}' for i in range(14))
    fx, fy, W, H = x, y - 150, 112, 72
    return (f'<rect x="{x-5}" y="{y-156}" width="10" height="190" rx="5" fill="#8a5a3a" stroke="{INK}" stroke-width="4"/>'
            f'<g transform="translate({fx+5} {fy}) skewY(-4)"><rect width="{W}" height="{H/3}" fill="#111"/><rect y="{H/3}" width="{W}" height="{H/3}" fill="#fff"/>'
            f'<rect y="{2*H/3}" width="{W}" height="{H/3}" fill="#007a3d"/><path d="M0 0 L{W*.5} {H/2} L0 {H} Z" fill="#ce1126"/>'
            f'<polygon points="{star7(W*.17, H/2, 7, 3)}" fill="#fff"/><rect width="{W}" height="{H}" fill="none" stroke="{INK}" stroke-width="4"/></g>')
def shades():
    return (f'<path d="M118 182 H294 L288 196 Q280 232 248 232 Q218 232 212 202 H200 Q194 232 164 232 Q132 232 124 196 Z" fill="{INK}"/>'
            f'<path d="M150 192 Q162 186 176 190" stroke="#fff" stroke-width="5" fill="none" opacity=".5" stroke-linecap="round"/>'
            f'<path d="M228 192 Q240 186 254 190" stroke="#fff" stroke-width="5" fill="none" opacity=".5" stroke-linecap="round"/>')
def tear(x, y):
    return f'<path d="M{x} {y} Q{x-9} {y+16} {x} {y+20} Q{x+9} {y+16} {x} {y}Z" fill="#8fc6e8" stroke="{INK}" stroke-width="3"/>'
def card(x, y, a=0):
    return (f'<g transform="translate({x} {y}) rotate({a})"><rect x="-30" y="-42" width="60" height="84" rx="9" fill="{RED}" stroke="{INK}" stroke-width="5"/>'
            f'<rect x="-22" y="-34" width="44" height="68" rx="5" fill="none" stroke="#fff8ee" stroke-width="2.5" stroke-dasharray="5 4"/>'
            f'<text x="0" y="8" font-family="Almarai, sans-serif" font-weight="800" font-size="24" fill="#fff8ee" text-anchor="middle">؟</text></g>')
def think_dots():
    return ''.join(f'<circle cx="{x}" cy="{y}" r="{r}" fill="#fff" stroke="{INK}" stroke-width="4"/>' for x, y, r in ((330, 90, 9), (350, 64, 13), (376, 34, 18)))
def lines_up():
    return ''.join(f'<path d="M{x} {y} l0 -22" stroke="{GOLD}" stroke-width="7" stroke-linecap="round"/>' for x, y in ((110, 52), (206, 28), (302, 52)))

P = {}
def pose(key, ar, en):
    def deco(fn): P[key] = (ar, en, fn); return fn
    return deco

@pose('wave', '«أهلين!»', 'Hello')
def _(pid): return body(pid, pid + 'c') + face(('open', 'happy'), ('up', 'up'), 'grin', look=(2, 0), tilt=-3) + rest('L') + arm('R', 364, 196, 'open', bend=26) + f'<path d="M392 150 q12 8 10 22 M402 136 q14 12 12 32" stroke="{GOLD}" stroke-width="6" fill="none" stroke-linecap="round"/>'

@pose('thumbs', '«تمام!»', 'Thumbs up')
def _(pid): return body(pid, pid + 'c') + face(('open', 'happy'), ('up', 'high'), 'smirk', look=(3, 1)) + rest('L') + arm('R', 360, 240, 'thumb', bend=14, hand_rot=0) + sparks()

@pose('shh', '«ششش… ولا كلمة!»', 'Shh')
def _(pid): return body(pid, pid + 'c') + face('open', ('high', 'flat'), 'pursed', look=(10, 4)) + rest('L') + arm('R', 212, 318, 'point', bend=46, hand_rot=-4)

@pose('laugh', '«هههههه»', 'Laughing')
def _(pid): return body(pid, pid + 'c') + face('happy', 'up', 'laugh', blush=True, tilt=4) + arm('L', 164, 340, 'grip', bend=-26, hand_rot=70) + arm('R', 248, 340, 'grip', bend=26, hand_rot=-70)

@pose('yay', '«يااا صح!»', 'Got it!')
def _(pid): return arm('L', 50, 168, 'open', bend=-20) + arm('R', 362, 168, 'open', bend=20) + body(pid, pid + 'c') + face('wide', 'high', 'grin') + sparks()

@pose('think', '«همم…»', 'Thinking')
def _(pid): return body(pid, pid + 'c') + face('open', ('flat', 'high'), 'smirk', look=(8, -10), tilt=-4) + rest('L') + arm('R', 262, 318, 'point', bend=40, hand_rot=-50) + think_dots()

@pose('shock', '«شو؟!»', 'Shocked')
def _(pid): return body(pid, pid + 'c') + face('wide', 'high', 'o') + arm('L', 76, 236, 'open', bend=-30, hand_rot=-20) + arm('R', 336, 236, 'open', bend=30, hand_rot=20) + lines_up()

@pose('headsup', '«عالجبين!»', 'Heads up')
def _(pid): return body(pid, pid + 'c') + face('open', 'up', 'grin', look=(0, -12)) + arm('L', 100, 196, 'grip', bend=-30, hand_rot=24) + arm('R', 312, 196, 'grip', bend=30, hand_rot=-24) + phone(206, 92)

@pose('cool', '«ولا يهمك»', 'Cool')
def _(pid): return body(pid, pid + 'c') + face('open', ('flat', 'up'), 'smirk', extras=shades()) + rest('L') + arm('R', 360, 196, 'peace', bend=30, hand_rot=8) + sparks()

@pose('sad', '«خسرنا…»', 'Lost the round')
def _(pid): return body(pid, pid + 'c') + face('sad', 'sad', 'frown', look=(0, 6), extras=tear(258, 230)) + rest('L') + rest('R')

@pose('love', '«بحبكم!»', 'Love')
def _(pid): return body(pid, pid + 'c') + face('happy', 'up', 'smile', blush=True) + arm('L', 140, 344, 'grip', bend=-20, hand_rot=70) + arm('R', 272, 344, 'grip', bend=20, hand_rot=-70) + heart(206, 322, 1.9) + heart(350, 104, .6) + heart(374, 146, .4)

@pose('proud', '«نشامى!»', 'Proud, with the flag')
def _(pid): return body(pid, pid + 'c', agal=True) + face(('open', 'happy'), 'up', 'grin', look=(4, 0)) + rest('L') + flag(354, 300) + arm('R', 354, 300, 'grip', bend=10, hand_rot=0)

@pose('compete', '«جد؟!»', 'Game on')
def _(pid): return body(pid, pid + 'c') + face('angry', 'angry', 'teeth') + arm('L', 150, 334, 'fist', bend=-40, hand_rot=10) + arm('R', 262, 334, 'fist', bend=40, hand_rot=-10)

@pose('card', '«مثّلها!»', 'Your turn')
def _(pid): return body(pid, pid + 'c') + face(('open', 'happy'), ('up', 'high'), 'grin', look=(6, 2)) + rest('L') + card(362, 184, 12) + arm('R', 352, 232, 'grip', bend=20, hand_rot=10)
