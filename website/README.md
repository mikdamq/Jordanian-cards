# ولا كلمة website

Static, SEO-first site. Arabic at `/`, English at `/en/`, linked with `hreflang`. The game will move to `/play/` when the site goes live on walakelmeh.com.

```bash
pip install uharfbuzz          # for the brand tools
python3 website/build.py            # production build into website/out/
python3 website/build.py --preview  # links to the live game + out/preview.html (both languages in one file)
```

- `content.py`: every string, in Arabic and English
- `site.css`: Sahra tokens, logical properties for RTL and LTR
- `build.py`: assembles pages using the logo, mascot and stitch art from `brand/`

## Sitemap

| Page | Status |
| --- | --- |
| Home | Built, in review |
| How to play | To do |
| Categories, plus one page per category (16) | To do |
| For cafés and partners | To do |
| شمّوغ stickers | To do |
| Privacy | Existing page, to restyle |
| Blog | Planned |
