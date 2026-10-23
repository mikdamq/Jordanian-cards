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
| Go live | Domain on Cloudflare, Cloudflare Pages hosting, game at `/play/`, own suggestion backend, Search Console |

Search setup and what we still need: see [SEO.md](SEO.md). Static images (share cards, favicons) are rendered by `make_og.py` into `static/`.

## Suggestion forms

Every category page has a "suggest a card" form, and the Categories page has a "suggest a category" form. They post to [Web3Forms](https://web3forms.com), which emails each suggestion to the inbox tied to the access key.

- Put the key in `WEB3FORMS_KEY` in `content.py` and rebuild. While it's empty, the forms open the visitor's email app with the suggestion filled in instead.
- Fields sent: `kind`, `lang`, `category`, `word`, `arabizi`, `level`, `category_name`, `examples`, `name`, `page`. The email subject says what was suggested and where.
- `botcheck` is a hidden honeypot that Web3Forms uses to drop spam.

The privacy page must mention suggestions before launch.

**Decision (2026-10-23):** Web3Forms now, our own backend later. At go-live, host the site and game on Cloudflare Pages and replace Web3Forms with our own `/api/suggest` (Pages Function), a D1 database, Turnstile anti-spam, and a private `/admin` page to approve suggestions. The form markup stays the same; only `SUGGEST_ENDPOINT` and the fields change.
