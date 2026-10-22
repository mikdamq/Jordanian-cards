# 4. Colour, type, pattern and illustration

Direction **A: Sahra**, chosen by Mikdam on 2026-10-22 from four options (Sahra, Majlis Night, Souk Pop, Wadi Rum).

Sahra formalises what the app already runs on: cream fabric by day, night majlis after dark, shemagh red leading, and olive, gold and indigo as tatreez threads.

Tokens: [`brand/tokens/sahra.css`](../../brand/tokens/sahra.css) and [`brand/tokens/sahra.json`](../../brand/tokens/sahra.json). They mirror `src/styles.css`, so change both together.

## Colour

### Light: cream fabric

| Token | Hex | Use |
| --- | --- | --- |
| `--bg` | `#f4ecdd` | Page background |
| `--surface` | `#fbf6ec` | Cards, sheets |
| `--surface-2` | `#efe4cf` | Inset areas |
| `--line` | `#dccbae` | Borders, dividers |
| `--stitch` | `#c7b08a` | Running-stitch borders |
| `--text` | `#2a1f1a` | Ink: text, wordmark |
| `--muted` | `#7a6650` | Secondary text |
| `--red` | `#b5121b` | Shemagh red: brand, primary action, game card |
| `--red-2` | `#8e0e16` | Pressed red |
| `--olive` | `#4f6b2c` | Correct, team 2 |
| `--gold` | `#b9861f` | Decoration, team 4 (never text on cream) |
| `--indigo` | `#3b3f7a` | Team 3, info |

### Dark: night majlis

| Token | Hex |
| --- | --- |
| `--bg` | `#17110e` |
| `--surface` | `#231a15` |
| `--line` | `#3f3128` |
| `--stitch` | `#6a5442` |
| `--text` | `#f4ecdd` |
| `--muted` | `#b5a28a` |
| `--red` | `#d42630` (fills and large text) |
| `--red-text` | `#e0444c` (small red text) |
| `--olive` | `#8aa75a` |
| `--gold` | `#ddae4a` |
| `--indigo` | `#8d92d6` |

The threads get lighter in the dark so they stay readable. Logo colours never change between themes.

### Proportion

On a typical screen or post: about **60% cream, 25% ink, 10% red, 5% threads**. Red is the hero, so keep it scarce.

### Contrast (WCAG)

| Pair | Ratio | Rule |
| --- | --- | --- |
| Ink on cream | 13.7 | Any text |
| Muted on cream | 4.7 | Body text OK |
| Red on cream | 5.8 | Text and buttons |
| Cream on red | 6.5 | Button and card text |
| Olive on cream | 5.2 | Text OK |
| **Gold on cream** | **2.8** | **Decoration only, never text** |
| Indigo on cream | 8.2 | Text OK |
| Cream on night | 15.9 | Any text |
| Red `#d42630` on night | 3.7 | Fills and 24px+ headings only; small red text uses `#e0444c` |
| Cream on dark red | 4.8 | Button text |
| White on dark green `#4d8f39` | 4.0 | Buttons must stay bold 18px+ |

## Type

| Role | Font | Size / line height |
| --- | --- | --- |
| Display | Almarai 800 | 40 / 48 |
| H1 | Almarai 800 | 32 / 40 |
| H2 | Almarai 700 | 24 / 32 |
| H3 | Cairo 800 | 20 / 28 |
| Body | Cairo 400 | 16 / 28 |
| Small | Cairo 600 | 14 / 22 |
| Caption | Cairo 600 | 12 / 18 |

- Cairo covers Latin too, so English uses the same fonts.
- The stitched lettering belongs to the logo only. Never set text with it.
- Arabic copy uses Eastern Arabic numerals «٣», and Latin copy uses 3.
- Arabic body text gets a line height of 1.7 to 1.8.
- Never letter-space Arabic. Latin uppercase labels get +0.12em.
- Headlines are red or ink. Body text is ink or muted, never gold.

## Pattern

Four textile devices. Use one or two per layout, never all four.

| Device | What | Where |
| --- | --- | --- |
| **Shemagh weave** | The red diamond check (`--shemagh` in `src/styles.css`) | Bands, card backs, full-bleed behind the logo |
| **Tatreez band** | A repeating cross-stitch border (`TATREEZ_BAND` in `src/art.ts`) | Section edges, headers, poster bottoms |
| **Running stitch** | A 2px dashed border in `--stitch` | Cards, avatars and inputs, like sewn-on patches |
| **Cross-stitch row** | A row of X stitches from the logo frame | Dividers, bullets, the partner lockup separator |

## Illustration

Everything is cross-stitch: one X per square on a grid. The 16 category illustrations, 6 team emblems and 3 game-mode illustrations in `src/art.ts` are the reference set.

- Use the five threads only: red `#b5121b`, olive `#4f6b2c`, gold `#c9962a`, ink `#2a1f1a`, indigo `#3b3f7a`.
- No gradients, outlines or shading.
- Keep grids about 8 to 12 squares across, so they read as embroidery, not pixel art.
- Always place stitches on cream fabric, even in dark mode, where they sit on a cream patch.
- شمّوغ, the mascot, is the exception: a drawn character with stitch details on its shemagh.

## Not chosen, kept for reference

- **B, Majlis Night:** indigo night with saffron, teal and rose
- **C, Souk Pop:** brighter red with sun, mint and sky; Marhey + Readex Pro
- **D, Wadi Rum:** sand, terracotta, Petra rose and Rum sky; Reem Kufi + Tajawal

Souk Pop could still return for شمّوغ and kids' content if we want a louder sub-palette.
