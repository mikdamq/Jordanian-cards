# Café partner kit («ليلة ولا كلمة»)

Printable files for partner cafés and lounges. They match the promises on the website's cafés page. Every PDF is at real paper size with **3 mm bleed** on every side, and backgrounds are included. PNG previews are in `brand/partner-kit/previews/`.

| File | Trim size | What it is |
| --- | --- | --- |
| `table-tent-a5-fold.pdf` | A5, 148 × 210 mm | QR table tent. Fold on the dashed line so it stands; both faces read the right way up. |
| `poster-a3.pdf` | A3, 297 × 420 mm | «ليلة ولا كلمة» door poster, with blank lines for day, time and prize (fill them in with a marker). |
| `window-sticker-150mm.pdf` | Ø 150 mm | Round «شريك ولا كلمة» window badge. The red runs 3 mm past the cut. |
| `window-sticker-150mm-dieline.pdf` | Ø 150 mm | The cut path only, in magenta. Send it to the printer next to the sticker; it is never printed. |
| `table-card-a6.pdf` | A6, 105 × 148 mm | How to play in 3 steps, plus the QR. |
| `partner-guide-a4.pdf` | A4, 210 × 297 mm | One-page guide for the venue: before, during and after the night, prize ideas, and how to tag us. |

## Printing notes

- Paper: 300 gsm matte for the tent and table card, 170 gsm for the poster, and outdoor vinyl for the sticker (applied on the inside of the glass, facing out).
- The files are RGB. Most print shops in Amman convert them on their side. If a shop asks for CMYK, send the PDFs and ask them to keep the red close to `#b5121b`.
- QR codes are at least 26 mm wide, so they scan easily from across a table.

## The QR code

For now the QR codes open `https://mikdamq.github.io/Jordanian-cards/?ref=cafe`. When walakelmeh.com is live, rebuild everything with the new address. You can also make a kit for one venue, so its scans can be counted:

```
python3 brand/tools/partner/partner_kit.py --url "https://walakelmeh.com/play/?ref=venue-name"
```

The script needs `qrcode` (`pip install qrcode`) and the Playwright install in the container. Fonts come from Google Fonts at render time.

## Still to decide

- A story template for venues (one already exists in the social kit, `brand/social/stories/`)
- A venue-specific category that a partner QR unlocks, which needs app work first
- The English versions, if a venue asks for them
