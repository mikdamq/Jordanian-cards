# 4b. Mascot: شمّوغ (Shammogh)

Locked by Mikdam on 2026-10-23 after four rounds. The moods will be extended later.

## Who شمّوغ is

A **living shemagh**: the cloth itself, with a face. It's a cheeky troublemaker who can't stop talking, in a game where talking isn't allowed.

- **Personality:** cheeky, quick, warm. It teases and never mocks. It's on the players' side.
- **Voice:** short Jordanian lines in «quotes», following [02-voice-and-tone.md](02-voice-and-tone.md)
- **Name:** شمّوغ in Arabic, *Shammogh* in Latin

## Anatomy

| Part | Rule |
| --- | --- |
| Body | Draped shemagh, wide and chubby, red-and-white diamond pattern, a heavy ink outline (7 at 412px wide) |
| Face | A cream window under the hood's brim, with the cloth wrapped under the chin |
| Eyes | Big white ovals with an ink outline, black pupils with one white highlight |
| Brows | Thick tapered ink strokes, which carry most of the expression |
| Feet | Five red tassels with dark caps along the hem |
| Hands | **None.** Gestures come from the face, body and props. |
| Shading | Right side of the cloth darker, a shadow under the brim, a highlight on top of the hood, a soft ground shadow |
| Accessory | The agal, only for proud and national moments |

## Colours

Sahra colours only (see [04-colour-type-pattern.md](04-colour-type-pattern.md)): shemagh red `#c4141f`, dark red `#8e0e16`, cream face `#fbf1e1`, ink `#1f1612`, gold `#d9a33a` for sparkles. **No blue.**

## How it gestures without hands

| Want to show | Do this |
| --- | --- |
| Shh / not a word | Mouth stitched shut with three red cross-stitches |
| Excitement | Jump (body lifted, motion lines below) and red-gold sparks |
| Hello | Tilt with gold motion lines |
| Sadness | Slump (body squashed slightly) under a small cloud |
| Holding something | The prop floats beside it, tilted: card, phone, heart, flag |

## The 14 moods

| File | Line | Use |
| --- | --- | --- |
| `wave` | «أهلين!» | Onboarding, welcome |
| `wink` | «تمام!» | Confirmations, settings saved |
| `shh` | «ششش… ولا كلمة!» | Rules, the game's signature |
| `laugh` | «هههههه» | Funny moments, social |
| `yay` | «يااا صح!» | Correct answer |
| `think` | «همم…» | Loading, choosing a category |
| `shock` | «شو؟!» | Surprises, a close score |
| `headsup` | «عالجبين!» | Heads-up mode |
| `cool` | «ولا يهمك» | Winner screen |
| `sad` | «خسرنا…» | Time's up, losing team |
| `love` | «بحبكم!» | Thanks, reviews, community |
| `proud` | «نشامى!» | National days, big wins |
| `compete` | «جد؟!» | Rematch, competitive modes |
| `card` | «مثّلها!» | Your turn |

## Do

- Keep شمّوغ next to the logo, never inside it or replacing it
- Use one شمّوغ per screen or post
- Let it react to what's happening in the game

## Don't

- Add hands, arms or fingers
- Change the pattern, recolour it, or use blue
- Stretch it, or squash it beyond the built-in moods
- Give it other brands' products (consoles, logos)
- Use it for anything on the off-limits list in the voice guide

## Files

```
brand/mascot/
  svg/                      14 moods, vector
  stickers/*.png, *.webp    512×512, transparent, white die-cut outline (WebP under 100 KB, ready for WhatsApp)
  stickers/tray-icon.png    96×96 sticker-pack icon
  shammogh-hero-1024.png    hero image
  samples/                  earlier rounds, for reference
brand/tools/sham.py, poses4.py   the drawing source
```
