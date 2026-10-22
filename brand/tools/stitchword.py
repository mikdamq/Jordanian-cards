"""Hand-built cross-stitch wordmark for ولا كلمة (columns run left to right)."""
W,H=50,16
g=[['.']*W for _ in range(H)]
def rect(c0,c1,r0,r1,v='x'):
    for r in range(r0,r1+1):
        for c in range(c0,c1+1): g[r][c]=v
def loop(c0,c1,r0,r1):
    rect(c0,c1,r0,r1); rect(c0+2,c1-2,r0+2,r1-2,'.')
# ة : tall loop + two dots (dots marked 'd' so they can be swapped)
loop(0,5,4,11)
rect(0,1,0,1,'d'); rect(3,4,0,1,'d')
rect(6,7,10,11)                 # joint
loop(8,13,6,11)                 # م
rect(14,15,10,11)
rect(16,17,0,11)                # ل
rect(18,26,10,11)               # baseline into ك
for r,c in enumerate([25,24,23,22,21,22,23,24,25,25]): rect(c,c+1,r,r)   # ك  "<"
# word space 27-31
rect(32,33,0,11); rect(37,38,0,11); rect(32,38,10,11)  # لا
loop(42,47,5,10)                # و head
rect(46,47,11,11)
for r,(a,b) in zip(range(12,16),[(45,46),(43,45),(41,43),(39,41)]): rect(a,b,r,r)
ROWS=[''.join(r) for r in g]
if __name__=='__main__':
    print('\n'.join(ROWS))
