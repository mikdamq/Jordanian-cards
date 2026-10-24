"""شمّوغ v3: the living shemagh, cartoon-shaded, after Mikdam's reference. All vector."""
import math
INK, RED, RED2, RED3 = '#1f1612', '#c4141f', '#8e0e16', '#e8343e'
FACE, HAND, WHITE, GOLD, PINK = '#fbf1e1', '#fbf1e1', '#fffaf1', '#d9a33a', '#ef8f86'
OL = 7  # outline

def pat(pid, s=1.3):
    c = 26 * s
    return (f'<pattern id="{pid}" width="{c}" height="{c}" patternUnits="userSpaceOnUse" patternTransform="rotate(-6)">'
            f'<rect width="{c}" height="{c}" fill="{WHITE}"/>'
            f'<g transform="scale({s})" fill="{RED}"><path fill-rule="evenodd" d="M13 1.5L24.5 13L13 24.5L1.5 13Z M13 6.8L6.8 13L13 19.2L19.2 13Z"/>'
            f'<rect x="10.6" y="10.6" width="4.8" height="4.8"/><rect x="-2.4" y="-2.4" width="4.8" height="4.8"/><rect x="23.6" y="-2.4" width="4.8" height="4.8"/>'
            f'<rect x="-2.4" y="23.6" width="4.8" height="4.8"/><rect x="23.6" y="23.6" width="4.8" height="4.8"/></g></pattern>')

# ---------------- body ----------------
SIL = ('M58 362 C72 320 88 290 92 248 C82 124 138 52 206 50 C276 52 332 124 320 248 '
       'C324 290 340 320 354 362 L318 350 L280 374 L243 356 L206 380 L169 356 L132 374 L94 350 Z')
FACE_P = 'M112 134 Q206 106 302 130 Q316 200 302 264 Q206 290 110 266 Q96 200 112 134 Z'
BRIM = 'M98 166 Q206 114 316 158 L312 128 Q206 80 104 134 Z'
CHIN = 'M86 262 Q206 306 326 252 L332 314 Q206 346 80 314 Z'
TIPS = [(354, 362), (280, 374), (206, 380), (132, 374), (58, 362)]

def tassel(x, y):
    return (f'<path d="M{x-9} {y+6} L{x-12} {y+30} Q{x} {y+38} {x+12} {y+30} L{x+9} {y+6} Z" fill="{RED}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>'
            f'<path d="M{x+3} {y+10} L{x+5} {y+31}" stroke="{RED2}" stroke-width="4" stroke-linecap="round"/>'
            f'<rect x="{x-8}" y="{y-1}" width="16" height="9" rx="4" fill="{RED2}" stroke="{INK}" stroke-width="3.5"/>')

def body(pid, cid, agal=False):
    s = f'<defs>{pat(pid)}<clipPath id="{cid}"><path d="{SIL}"/></clipPath></defs>'
    s += '<ellipse cx="206" cy="400" rx="146" ry="13" fill="#000" opacity=".16"/>'
    s += ''.join(tassel(x, y - 4) for x, y in TIPS)
    s += f'<path d="{SIL}" fill="url(#{pid})"/>'
    s += f'<g clip-path="url(#{cid})"><path d="M250 40 C330 80 350 260 340 400 L400 400 L400 0Z" fill="{INK}" opacity=".16"/>'  # shade, right side
    s += f'<path d="M60 300 Q206 360 360 300 L360 420 L60 420Z" fill="{INK}" opacity=".08"/></g>'
    s += f'<path d="{SIL}" fill="none" stroke="{INK}" stroke-width="{OL}" stroke-linejoin="round"/>'
    s += f'<path d="M120 118 Q140 72 194 62" stroke="#fff" stroke-width="9" fill="none" stroke-linecap="round" opacity=".55"/>'
    s += f'<path d="{FACE_P}" fill="{FACE}" stroke="{INK}" stroke-width="5"/>'
    s += f'<path d="M108 172 Q206 126 310 164 L308 184 Q206 148 110 192 Z" fill="{INK}" opacity=".09"/>'   # shadow under brim
    s += f'<path d="M274 140 Q308 150 306 220 Q300 252 284 264 Q298 200 274 140Z" fill="{INK}" opacity=".06"/>'
    s += f'<path d="{BRIM}" fill="url(#{pid})" stroke="{INK}" stroke-width="{OL-1}" stroke-linejoin="round"/>'
    s += f'<path d="{CHIN}" fill="url(#{pid})" stroke="{INK}" stroke-width="{OL-1}" stroke-linejoin="round"/>'
    s += f'<g clip-path="url(#{cid})"><path d="M80 302 Q206 340 332 302 L332 332 Q206 364 80 332Z" fill="{INK}" opacity=".08"/></g>'
    if agal:
        s += (f'<g transform="rotate(-8 206 96)"><path d="M136 100 Q206 126 276 100" stroke="{INK}" stroke-width="13" fill="none" stroke-linecap="round"/>'
              f'<path d="M142 84 Q206 108 270 84" stroke="{INK}" stroke-width="12" fill="none" stroke-linecap="round"/>'
              f'<path d="M160 96 Q180 104 196 106" stroke="#6b5a50" stroke-width="3" fill="none" stroke-linecap="round"/></g>')
    return s

# ---------------- face ----------------
def brow(cx, cy, kind, side):
    """Thick tapered brow. side=-1 left, +1 right. kind: up, flat, angry, sad, high."""
    w = 26
    inner, outer = cx - side * w, cx + side * w
    lift = {'up': (-6, -2), 'flat': (0, 0), 'angry': (10, -8), 'sad': (-10, 4), 'high': (-14, -10)}[kind]
    yi, yo = cy + lift[0], cy + lift[1]
    arch = -12 if kind in ('up', 'high', 'flat') else -4
    return (f'<path d="M{inner} {yi} Q{cx} {min(yi, yo) + arch} {outer} {yo} Q{cx} {min(yi, yo) + arch + 12} {inner} {yi + 2} Z" '
            f'fill="{INK}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>')

def eye(cx, cy, kind, look=(0, 0)):
    o = f'stroke="{INK}" stroke-width="6"'
    if kind == 'happy':
        return f'<path d="M{cx-20} {cy+6} Q{cx} {cy-18} {cx+20} {cy+6}" stroke="{INK}" stroke-width="8" fill="none" stroke-linecap="round"/>'
    if kind == 'shut':
        return f'<path d="M{cx-20} {cy} Q{cx} {cy+12} {cx+20} {cy}" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>'
    rx, ry, pr = (26, 30, 13) if kind != 'wide' else (28, 34, 8)
    dx, dy = look
    s = f'<ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" fill="#fff" {o}/>'
    s += f'<circle cx="{cx+dx}" cy="{cy+dy}" r="{pr}" fill="{INK}"/><circle cx="{cx+dx+pr*.35}" cy="{cy+dy-pr*.4}" r="{max(3, pr*.33)}" fill="#fff"/>'
    if kind == 'angry':   # lid cuts the top of the eye at an angle
        s += f'<path d="M{cx-34} {cy-34} L{cx+34} {cy-34} L{cx+30} {cy-6} L{cx-30} {cy-20} Z" fill="{FACE}"/><path d="M{cx-28} {cy-19} L{cx+28} {cy-7}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    if kind == 'sad':
        s += f'<path d="M{cx-34} {cy-34} L{cx+34} {cy-34} L{cx+30} {cy-18} L{cx-30} {cy-6} Z" fill="{FACE}"/><path d="M{cx-28} {cy-7} L{cx+28} {cy-19}" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>'
    return s

def mouth(cx, cy, kind):
    if kind == 'grin':      # open smile with tongue
        return (f'<path d="M{cx-34} {cy-6} Q{cx} {cy+46} {cx+38} {cy-12} Q{cx+2} {cy+4} {cx-34} {cy-6} Z" fill="{INK}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                f'<path d="M{cx-14} {cy+22} Q{cx+4} {cy+8} {cx+22} {cy+16} Q{cx+6} {cy+32} {cx-14} {cy+22} Z" fill="{RED3}"/>')
    if kind == 'smirk':
        return (f'<path d="M{cx-30} {cy+2} Q{cx} {cy+22} {cx+30} {cy-10}" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>'
                f'<path d="M{cx+30} {cy-10} q6 -2 8 -8" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>')
    if kind == 'laugh':
        return (f'<path d="M{cx-40} {cy-8} Q{cx} {cy-2} {cx+40} {cy-8} Q{cx+34} {cy+46} {cx} {cy+48} Q{cx-34} {cy+46} {cx-40} {cy-8} Z" fill="{INK}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
                f'<path d="M{cx-32} {cy-4} Q{cx} {cy+2} {cx+32} {cy-4} L{cx+30} {cy+6} Q{cx} {cy+12} {cx-30} {cy+6} Z" fill="#fff"/>'
                f'<path d="M{cx-18} {cy+36} Q{cx} {cy+22} {cx+18} {cy+36} Q{cx} {cy+46} {cx-18} {cy+36} Z" fill="{RED3}"/>')
    if kind == 'o':
        return f'<ellipse cx="{cx}" cy="{cy+8}" rx="12" ry="15" fill="{INK}"/><ellipse cx="{cx}" cy="{cy+15}" rx="7" ry="5" fill="{RED3}"/>'
    if kind == 'frown':
        return f'<path d="M{cx-22} {cy+14} Q{cx} {cy-2} {cx+22} {cy+14}" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>'
    if kind == 'teeth':     # gritted, competitive
        return (f'<rect x="{cx-30}" y="{cy-4}" width="60" height="26" rx="10" fill="#fff" stroke="{INK}" stroke-width="6"/>'
                f'<path d="M{cx-26} {cy+9} H{cx+26} M{cx-10} {cy-2} V{cy+20} M{cx+10} {cy-2} V{cy+20}" stroke="{INK}" stroke-width="3.5"/>')
    if kind == 'pursed':
        return f'<ellipse cx="{cx}" cy="{cy+6}" rx="9" ry="7" fill="{INK}"/>'
    if kind == 'smile':
        return f'<path d="M{cx-26} {cy} Q{cx} {cy+24} {cx+26} {cy}" stroke="{INK}" stroke-width="7" fill="none" stroke-linecap="round"/>'
    return ''

def face(e, b, m, look=(0, 0), blush=False, tilt=0, extras=''):
    L, R, Y = 168, 244, 200
    el, er = e if isinstance(e, tuple) else (e, e)
    bl, br = b if isinstance(b, tuple) else (b, b)
    s = brow(L, Y - 46, bl, -1) + brow(R, Y - 46, br, 1)
    s += eye(L, Y, el, look) + eye(R, Y, er, look)
    if blush: s += f'<ellipse cx="{L-18}" cy="{Y+40}" rx="16" ry="9" fill="{PINK}" opacity=".6"/><ellipse cx="{R+18}" cy="{Y+40}" rx="16" ry="9" fill="{PINK}" opacity=".6"/>'
    s += mouth(206, Y + 44, m) + extras
    return f'<g transform="rotate({tilt} 206 210)">{s}</g>'

# ---------------- arms and hands ----------------
SH_L, SH_R = (100, 288), (312, 288)

def sleeve(x0, y0, x1, y1, bend=0):
    mx, my = (x0 + x1) / 2 + bend, (y0 + y1) / 2 - abs(bend) * .3
    d = f'M{x0} {y0} Q{mx} {my} {x1} {y1}'
    ang = math.degrees(math.atan2(y1 - my, x1 - mx))
    return (f'<path d="{d}" stroke="{INK}" stroke-width="36" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="{RED}" stroke-width="24" fill="none" stroke-linecap="round"/>'
            f'<path d="{d}" stroke="{RED2}" stroke-width="6" fill="none" stroke-linecap="round" opacity=".5" transform="translate(3 4)"/>'
            f'<g transform="translate({x1} {y1}) rotate({ang})"><ellipse cx="0" cy="0" rx="9" ry="19" fill="{RED2}" stroke="{INK}" stroke-width="5"/></g>'), ang

def cap(x, y, w, l, a):
    """A finger: rounded capsule from (x,y) going up by l, rotated a degrees."""
    return f'<rect x="{x - w/2}" y="{y - l}" width="{w}" height="{l + w/2}" rx="{w/2}" fill="{HAND}" stroke="{INK}" stroke-width="5" transform="rotate({a} {x} {y})"/>'

def hand(kind, x, y, a=0, s=1.18, flip=1):
    """Glove hand, wrist at (x,y), pointing 'up' before rotation a. flip=-1 mirrors (left hand)."""
    g = ''
    palm = f'<rect x="-21" y="-46" width="42" height="44" rx="17" fill="{HAND}" stroke="{INK}" stroke-width="5"/>'
    knuckles = ''.join(f'<rect x="{-20 + i*10.5}" y="-56" width="12" height="18" rx="6" fill="{HAND}" stroke="{INK}" stroke-width="4.5"/>' for i in range(4))
    if kind == 'open':
        g = ''.join(cap(-15 + i * 10, -38, 12, 30 + (6 if i in (1, 2) else 0), -16 + i * 10) for i in range(4))
        g += palm + cap(19, -18, 13, 24, 58)
    elif kind == 'point':      # index up
        g = cap(-11, -40, 13, 40, -2) + palm
        g += ''.join(f'<rect x="{-2 + i*8}" y="-52" width="11" height="16" rx="5.5" fill="{HAND}" stroke="{INK}" stroke-width="4.5"/>' for i in range(3))
        g += f'<rect x="-18" y="-28" width="34" height="13" rx="6.5" fill="{HAND}" stroke="{INK}" stroke-width="4.5"/>'
    elif kind == 'peace':
        g = cap(-12, -40, 12, 38, -12) + cap(1, -40, 12, 38, 8) + palm
        g += ''.join(f'<rect x="{6 + i*8}" y="-50" width="10" height="15" rx="5" fill="{HAND}" stroke="{INK}" stroke-width="4.5"/>' for i in range(2))
        g += f'<rect x="-18" y="-28" width="32" height="13" rx="6.5" fill="{HAND}" stroke="{INK}" stroke-width="4.5"/>'
    elif kind == 'thumb':      # thumbs up: fist turned sideways, thumb to the sky
        g = cap(-6, -54, 15, 30, -4)
        g += f'<rect x="-22" y="-56" width="44" height="40" rx="15" fill="{HAND}" stroke="{INK}" stroke-width="5"/>'
        g += ''.join(f'<rect x="8" y="{-54 + i*9.5}" width="20" height="12" rx="6" fill="{HAND}" stroke="{INK}" stroke-width="4.5"/>' for i in range(4))
    elif kind == 'fist':
        g = palm + knuckles + f'<rect x="-22" y="-30" width="30" height="13" rx="6.5" fill="{HAND}" stroke="{INK}" stroke-width="4.5"/>'
    elif kind == 'mitt':       # relaxed fist: one rounded shape and a thumb
        g = f'<rect x="-22" y="-44" width="44" height="42" rx="20" fill="{HAND}" stroke="{INK}" stroke-width="5"/>'
        g += f'<path d="M-8 -36 q10 6 20 0" stroke="{INK}" stroke-width="3.5" fill="none" stroke-linecap="round"/>'
        g += f'<rect x="12" y="-30" width="13" height="22" rx="6.5" fill="{HAND}" stroke="{INK}" stroke-width="4.5"/>'
    elif kind == 'grip':       # wrapped around something held across the palm
        g = palm + ''.join(f'<rect x="{-21 + i*10.5}" y="-42" width="12" height="22" rx="6" fill="{HAND}" stroke="{INK}" stroke-width="4.5"/>' for i in range(4))
    return f'<g transform="translate({x} {y}) rotate({a}) scale({s * flip} {s})">{g}</g>'

def arm(side, wx, wy, kind, bend=0, hand_rot=None, s=1.18):
    sx, sy = SH_L if side == 'L' else SH_R
    sl, ang = sleeve(sx, sy, wx, wy, bend)
    a = (ang + 90) if hand_rot is None else hand_rot
    return sl + hand(kind, wx, wy, a, s, -1 if side == 'L' else 1)

def rest(side):
    return arm(side, SH_L[0] - 18, SH_L[1] + 46, 'mitt', bend=-12, hand_rot=196) if side == 'L' else arm(side, SH_R[0] + 18, SH_R[1] + 46, 'mitt', bend=12, hand_rot=164)

def sparks(c1=GOLD, c2=RED):
    pts = ((52, 92, -24, -16, c1), (40, 136, -28, 0, c2), (360, 92, 24, -16, c1), (372, 136, 28, 0, c2))
    return ''.join(f'<path d="M{x} {y} l{dx} {dy}" stroke="{c}" stroke-width="8" stroke-linecap="round"/>' for x, y, dx, dy, c in pts)

def svg(inner, vb='0 0 412 420'):
    return f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{vb}">{inner}</svg>'
