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
| For cafés and partners | Built, in review |
| شمّوغ stickers | Built, in review |
| Privacy | Built: covers the game, website, forms and third parties. `/privacy.html` redirects here. |
| Blog | Built: index + 3 launch articles (party games, charades in Arabic, winter and New Year). Ramadan article to add in January. |
| Go live | Namecheap hosting with automatic deploys, game at `/play/`, own PHP form script, old address redirects. Steps: [docs/go-live.md](../docs/go-live.md) |

Search setup and what we still need: see [SEO.md](SEO.md). Static images (share cards, favicons) are rendered by `make_og.py` into `static/`.

## Forms

Every category page has a "suggest a card" form, the Categories page has a "suggest a category" form, and the Cafés page has a partner form. They all post to our own script, `static/api/send.php`, on the Namecheap hosting. It emails each submission to hello@walakelmeh.com. No third-party service is involved.

- Fields sent: `kind`, `lang`, `category`, `word`, `arabizi`, `level`, `category_name`, `examples`, `venue`, `city`, `type`, `contact`, `message`, `name`, `page`. The email subject says what was sent and from where.
- Spam protection: a hidden `botcheck` honeypot, a same-site check, field length limits, and a limit of 5 submissions per visitor every 10 minutes.
- If the endpoint is empty, or in the preview, the forms open the visitor's email app with the message filled in instead.

**Decision (2026-10-24):** our own PHP script on the Namecheap hosting, instead of Web3Forms. A database and a private /admin page to approve suggestions can come later on the same hosting.
