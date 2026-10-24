# Store screenshots

Regenerates `brand/store/` from the real game.

```bash
npm run build && python3 -m http.server 4173 --directory dist   # serve the game
cd brand/tools/store
node capture.cjs        # raw screens into brand/store/raw/ (a full game; takes ~2 minutes)
node capture_hu.cjs     # heads up, landscape (dismisses the tilt tip)
node capture_cat.cjs    # categories with "select all"
node capture_fix.cjs    # winner screen after the confetti settles
python3 compose.py      # framed screenshots + feature graphics into brand/store/{ar,en}/
```

Captions, mascots and backgrounds per screenshot are in `SHOTS` at the top of `compose.py`.
