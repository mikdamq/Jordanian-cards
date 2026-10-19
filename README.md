# ولا كلمة — Wala Kilmeh

A Jordanian charades and heads-up party game, built as an installable web app (PWA).

- **🎭 Classic (تمثيل):** act out the card silently while your team guesses.
- **📱 Heads Up (عالجبين):** phone on your forehead. Tilt down for correct, tilt up to skip (tap buttons as a fallback).
- **230 cards** in Arabic + Arabizi across 7 categories: movies and TV, food, places, Jordanian moments, Jordanian sayings, heritage, and sports and arts. Plus an optional **شباب** youth pack.
- 2–4 teams, a 30/60/90s timer, 3/5/7 rounds, editable results after each turn, and no repeated cards across game nights.
- Works offline once installed and keeps the screen awake during play.

## Develop

```bash
npm install
npm run dev      # local dev server
npm test         # unit tests
npm run build    # typecheck + production build in dist/
```

Card content lives in `src/data/cards.ts`. Each row is `[arabic, arabizi, difficulty 1–3]`.

> Tilt controls need HTTPS (or localhost). On iPhone the game asks for motion permission when the team taps **جاهزين**.

## Analytics

Anonymous, cookie-free counts via [GoatCounter](https://www.goatcounter.com). Set `GOATCOUNTER_CODE` in `src/config.ts` to your site code to switch it on; it stays off while empty. Events: `game-start/<mode>/...`, `game-end/<mode>`, `share/<shared|downloaded|cancelled>`.

## Store listing

Draft Google Play listing text and checklists: `docs/google-play-listing.md`. Privacy policy: `public/privacy.html`.
