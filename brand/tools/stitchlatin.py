"""Cross-stitch Latin capitals for WALA KELMEH, 12 rows tall, 2-stitch strokes (matches the Arabic grid)."""
H = 12
def blank(w): return [['.'] * w for _ in range(H)]
def fill(g, c0, c1, r0, r1):
    for r in range(r0, r1 + 1):
        for c in range(c0, c1 + 1):
            if 0 <= c < len(g[0]): g[r][c] = 'x'
def L():
    g = blank(7); fill(g,0,1,0,11); fill(g,0,6,10,11); return g
def E():
    g = blank(7); fill(g,0,1,0,11); fill(g,0,6,0,1); fill(g,0,5,5,6); fill(g,0,6,10,11); return g
def Hh():
    g = blank(8); fill(g,0,1,0,11); fill(g,6,7,0,11); fill(g,0,7,5,6); return g
def A():
    g = blank(8); fill(g,2,5,0,0); fill(g,1,6,1,1); fill(g,0,1,2,11); fill(g,6,7,2,11); fill(g,0,7,6,7); return g
def K():
    g = blank(8); fill(g,0,1,0,11)
    for r, c in enumerate([7,6,5,4,3,2,2,3,4,5,6,7]): fill(g,c,c+1,r,r)
    return g
def M():
    g = blank(10); fill(g,0,1,0,11); fill(g,8,9,0,11)
    for r,(a,b) in enumerate([(2,2),(2,3),(3,4),(4,5),(4,5)]): fill(g,a,b,r,r); fill(g,9-b,9-a,r,r)
    return g
def W():
    g = M(); return g[::-1]
GLYPHS = {'W': W, 'A': A, 'L': L, 'K': K, 'E': E, 'M': M, 'H': Hh}
def word(text, gap=2, space=5):
    rows = [''] * H
    for i, ch in enumerate(text):
        if ch == ' ':
            rows = [r + '.' * (space - gap) for r in rows]; continue
        g = GLYPHS[ch]()
        rows = [rows[r] + ''.join(g[r]) + ('.' * gap if i < len(text) - 1 else '') for r in range(H)]
    return rows
LATIN_ROWS = word('WALA KELMEH')
if __name__ == '__main__': print('\n'.join(LATIN_ROWS))
