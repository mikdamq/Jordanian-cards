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
| Home | Built: logo fix, SEO pass, original footer |
| How to play | Built, in review |
| Categories, plus one page per category (16) | Built, in review |
| For cafés and partners | To do |
| شمّوغ stickers | To do |
| Privacy | Existing page, to restyle |
| Blog | Planned |

Search setup and what we still need: see [SEO.md](SEO.md). Static images (share cards, favicons) are rendered by `make_og.py` into `static/`.

## Suggestion forms

Every category page has a "suggest a card" form, and the Categories page has a "suggest a category" form. Set `SUGGEST_ENDPOINT` in `content.py` to the form service's URL to collect submissions there. While it's empty, the forms open the visitor's email app with the suggestion filled in. Fields sent: `kind`, `lang`, `category`, `word`, `arabizi`, `level`, `category_name`, `examples`, `name`, `page`. A hidden `website` field catches bots.

The privacy page must mention suggestions before launch.
