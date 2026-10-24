"""Shape text with HarfBuzz and return outlined SVG path data."""
import uharfbuzz as hb
import os
FONTS = os.environ.get('FONT_DIR', os.path.join(os.path.dirname(__file__), 'fonts')) + '/'

class Pen:
    def __init__(s, ox, oy, k): s.d = []; s.ox, s.oy, s.k = ox, oy, k
    def p(s, x, y): return f"{s.ox + x*s.k:.2f} {s.oy - y*s.k:.2f}"
    def moveTo(s, a): s.d.append('M' + s.p(*a))
    def lineTo(s, a): s.d.append('L' + s.p(*a))
    def qCurveTo(s, *pts):
        # hb gives one control + end
        s.d.append('Q' + ' '.join(s.p(*q) for q in pts))
    def curveTo(s, *pts): s.d.append('C' + ' '.join(s.p(*q) for q in pts))
    def closePath(s): s.d.append('Z')
    def endPath(s): pass

def text_path(text, font_file, size, x=0, y=0, wght=None, letter=0, anchor='start', features=None):
    """Returns (path_d, width, ascent_px, descent_px). y is the baseline."""
    blob = hb.Blob.from_file_path(FONTS + font_file)
    face = hb.Face(blob)
    font = hb.Font(face)
    if wght: font.set_variations({'wght': wght})
    upem = face.upem
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font, buf, features or {})
    k = size / upem
    total = sum(p.x_advance for p in buf.glyph_positions) * k + letter * (len(buf.glyph_infos) - 1)
    if anchor == 'middle': x -= total / 2
    elif anchor == 'end': x -= total
    d = []; cx = 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        pen = Pen(x + (cx + pos.x_offset) * k, y - pos.y_offset * k, k)
        font.draw_glyph_with_pen(info.codepoint, pen)
        d += pen.d
        cx += pos.x_advance + letter / k
    ext = font.get_font_extents('ltr')
    return ''.join(d), total, ext.ascender * k, -ext.descender * k

def glyph_list(text, font_file, size, wght=None):
    """Per-glyph paths at origin, with cluster index and advance, for detail edits."""
    blob = hb.Blob.from_file_path(FONTS + font_file)
    face = hb.Face(blob); font = hb.Font(face)
    if wght: font.set_variations({'wght': wght})
    buf = hb.Buffer(); buf.add_str(text); buf.guess_segment_properties()
    hb.shape(font, buf, {})
    k = size / face.upem
    out = []; cx = 0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        pen = Pen((cx + pos.x_offset) * k, -pos.y_offset * k, k)
        font.draw_glyph_with_pen(info.codepoint, pen)
        out.append(dict(d=''.join(pen.d), cluster=info.cluster, name=font.glyph_to_string(info.codepoint), adv=pos.x_advance*k, x=cx*k))
        cx += pos.x_advance
    return out, cx * k
