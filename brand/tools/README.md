# Logo tools

Python scripts that generate every file in `brand/logo/`. All lettering is output as outlines, so the SVGs need no fonts installed.

```bash
pip install uharfbuzz
# Put these Google Fonts (OFL) in brand/tools/fonts/, or point FONT_DIR at them:
#   Almarai-Bold.ttf, Almarai-ExtraBold.ttf, Cairo[slnt,wght].ttf (saved as Cairo%5Bslnt%2Cwght%5D.ttf)
python3 final.py                  # writes brand/logo/{symbol,wordmark,lockup,partner}
node export_png.cjs jobs.json      # optional PNG exports (needs Playwright)
```

- `stitchword.py`: the Arabic stitch grid. `d` cells mark the two stars on ة.
- `stitchlatin.py`: the Latin stitch alphabet for WALA KELMEH
- `logos.py`: the symbol, the seven-point star, and shared helpers
- `lockups2.py`: horizontal and stacked lockups, one language each
- `final.py`: the full asset list, plus partner and sponsor marks

## Mascot and guidelines

- `sham.py`: شمّوغ's body, face and shading. `poses4.py`: the 14 no-hands moods.
- `build_book.py`: regenerates the brand book body (`brand/guidelines/book-body.html`). `brand/guidelines/index.html` is the standalone copy.
- `poses.py` and `handsx.py` hold the earlier hand experiments that `poses4.py` reuses props from.
