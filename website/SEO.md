# Search, answer-engine and AI-search setup

This covers SEO (Google, Bing), AEO (answer boxes, voice assistants) and GEO (AI answers such as ChatGPT, Gemini, Perplexity and Google AI Overviews). Every new page follows this checklist.

## Built into every page

| Area | What we do |
| --- | --- |
| Languages | Separate URLs: Arabic at `/`, English at `/en/`. `hreflang` pairs plus `x-default`. `lang` and `dir` on `<html>`. |
| Titles and descriptions | Unique per page and language. Title 40 to 60 characters, description 110 to 160. |
| Canonical | Every page points to itself. |
| Social cards | Open Graph and Twitter tags with a real 1200×630 image per language (`static/assets/og-*.png`), with alt text. |
| Structured data | JSON-LD graph: Organization, WebSite, WebPage, SoftwareApplication + VideoGame (free offer, 2 to 12 players), ItemList of categories, HowTo, FAQPage. Subpages add BreadcrumbList. |
| Headings | One `h1` per page, then `h2` per section and `h3` inside. FAQ questions are headings. |
| Answer-ready copy | A plain "What is Wala Kelmeh?" definition near the top, a facts list (price, players, cards, language, made in), and short, direct FAQ answers. These are the passages AI engines quote. |
| Images | Real image files with `alt` text in the page's language, `width` and `height` set, lazy loading below the fold, high priority for the hero image. |
| Accessibility | Landmarks (header, nav, main, footer), skip link, visible focus, contrast checked, reduced-motion respected. Accessibility helps rankings too. |
| Speed | About 40 KB of HTML per page. Images and logos are cached files. Font preconnect with `display=swap`. |
| Internal links | Header, category tiles and footer link every page. The language switch links to the twin page. |

## Site-wide files

| File | Purpose |
| --- | --- |
| `robots.txt` | Allows everything, points to the sitemap |
| `sitemap.xml` | Every page with its `hreflang` alternates and last-modified date |
| `llms.txt` | A plain-language summary for AI crawlers: what the game is, facts, categories, FAQ |
| Favicons | SVG, 32px PNG, Apple touch icon |

## What we need from Mikdam (when ready)

1. ~~**Domain**~~ Done: walakelmeh.com on Namecheap hosting (see `docs/go-live.md`). All canonical, sitemap and social URLs already use it.
2. **Google Search Console and Bing Webmaster Tools**: verify the domain and submit `sitemap.xml`. This takes about 10 minutes once the domain is live. I'll walk you through it.
3. **Social accounts**: Instagram @walakelmeh is in the footer and the Organization `sameAs`. Add TikTok to `SOCIAL` in `content.py` once it exists.
4. ~~**Public creator name**~~ Decided: the site names the brand and «فريق ولا كلمة» (The Wala Kelmeh Team) only, never one person.
5. ~~**Analytics**~~ Done: GoatCounter (`walakelmeh.goatcounter.com`), cookie-free, always on, on the website and in the game. Site buttons count as `site/play` and `site/install`; game events: `game-start`, `category-pick`, `card-skip`, `turn-end`, `game-end`, `game-quit`, `share`, `install`. Google Analytics 4 and Microsoft Clarity load only after consent (one banner, one answer shared by site and game); set `GA_ID` and `CLARITY_ID` in `src/config.ts` to switch them on.
6. ~~**A brand email** on the new domain~~ Done: hello@walakelmeh.com is used everywhere.
7. **Later**: real player quotes and a short gameplay video. Reviews and video both improve rich results and AI citations.

## Before each release

- Run `python3 website/build.py` and check: one h1, every image has alt text, the JSON-LD parses.
- Test a page in Google's Rich Results Test and the PageSpeed Insights tool once the domain is live.
- Add each new page to the sitemap pairs in `build.py`.
