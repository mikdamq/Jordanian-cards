# Social kit and launch plan

The dated launch campaign (5 November 2026) that schedules these posts is in [`docs/marketing/launch-plan.md`](../marketing/launch-plan.md).

Instagram first, TikTok alongside. Graphics are in [`brand/social/`](../../brand/social/); regenerate them with `brand/tools/social/social.py` (it needs `website/out/` built for the stitch art).

Handle: **@walakelmeh** on every platform (placeholder until the accounts exist; change `HANDLE` in the script if it differs).

## Profile

| Item | File / text |
| --- | --- |
| Profile picture | `profile/profile-patch.png` (recommended, matches the app icon) or `profile/profile-shammogh.png` |
| Name | ولا كلمة · Wala Kelmeh |
| Bio | 🎭 لعبة التمثيل الأردنية<br>🤫 مثّلها… بس ولا كلمة!<br>📱 مجانية · بدون حساب · بدون إنترنت<br>⬇️ يلا نلعب |
| Link | walakelmeh.com |
| Highlights | `profile/highlight-*.png`: كيف تلعب · الفئات · شمّوغ · سهراتكم · للمقاهي · قريباً |

## The 9 launch posts (1080×1350)

Post them in this order, so post 1 ends up bottom-right of the first 3×3 grid and post 9 top-left.

| # | File | Caption | When |
| --- | --- | --- | --- |
| 1 | `post-01-arrived` | «ولا كلمة» وصلت! 🇯🇴 لعبة التمثيل الأردنية للسهرات: مثّلها… بس ولا كلمة! 🤫 الرابط بالبايو. | Launch day |
| 2 | `post-02-meet-shammogh` | تعرّفوا على شمّوغ 👋 الشماغ اللي ما بقدر يسكت… بلعبة ممنوع فيها الحكي. شو أول كلمة لازم يمثّلها؟ | Day 2 |
| 3 | `post-03-how-it-works` | كيف تلعب؟ ٣ خطوات بس: طلّع البطاقة، مثّلها بالحركات، وفريقك بحزر قبل ما يخلص الوقت ⏱️ | Day 4 |
| 4 | `post-04-card-mansaf` | مين بيقدر يمثّل «منسف» بدون ولا كلمة؟ 🍽️ اكتبوا بالتعليقات كيف بتمثّلوها 👇 | Day 6 |
| 5 | `post-05-three-modes` | ٣ طرق للعب: تمثيل 🎭 عالجبين 📱 ومين أسرع؟ ⏱️ إنتو أي فريق؟ | Day 8 |
| 6 | `post-06-categories` | ٥١٠ بطاقة بـ١٦ فئة: أكل، أماكن، أعراس، نوستالجيا التسعينات… وفي كمان باكيت الشباب 😎 أي فئة بتبلّشوا فيها؟ | Day 10 |
| 7 | `post-07-saying` | «يا زلمة!» 🗣️ مثّلها… بدون ما تحكيها 😏 تاجوا صاحبكم اللي ما بقدر يسكت. | Day 12 |
| 8 | `post-08-heads-up` | عالجبين! 📱 الجوال على جبينك والكل بمثّلك. نزّله إذا عرفتها، ارفعه لتتخطّى. | Day 14 |
| 9 | `post-09-play-now` | العبوها الليلة 🔥 مجانية، بدون حساب، وبتشتغل بدون إنترنت. الرابط بالبايو 🔗 | Day 16 |

Add an English line under captions when the post is for the diaspora (e.g. post 1: *Wala Kelmeh is here: the Jordanian charades game. Act it out, not a word! Link in bio.*). One language leads each line, per the voice guide.

## Alt text

Alt text lets people using a screen reader hear what's in a picture, and helps Instagram and search understand the post. Add it to **every** post and story before publishing.

- **Instagram:** after choosing the picture, tap **Next**, scroll down to **Advanced settings → Accessibility → Write alt text**. For a carousel, add it to each picture. To fix an old post: **⋯ → Edit → Edit alt text**.
- **Facebook:** tap the picture while editing, then **Alternative text**.
- **TikTok photo posts:** add it from the post's options before posting.
- **Videos (reels and TikToks):** there's no alt text, so turn on **auto captions** and keep the hook as on-screen text. Our acting videos have little speech, so the text on screen carries the meaning.

**How to write it:** say what the picture shows and repeat any words in it. Don't start with "صورة" or "image of". Keep it to one or two sentences. Use the Arabic by default and the English for posts that lead in English. In stories with placeholders, swap `[اسم المحل]`, `[الجائزة]` and `[الاسم]` for the real details.

**Hashtags:** in English, capitalise each word (#WalaKelmeh, not #walakelmeh) so screen readers say them as words.

### Posts

| File | Arabic | English |
| --- | --- | --- |
| `post-01-arrived` | شعار ولا كلمة: نجمة بيضا على رقعة حمرا مطرّزة. النص: «وصلت! لعبة التمثيل الأردنية للسهرات». | The Wala Kelmeh logo, a white star on a red stitched patch. Text: “It’s here! The Jordanian charades game for nights in.” |
| `post-02-meet-shammogh` | شمّوغ، شماغ أحمر وأبيض كرتوني إله وجه، بيسلّم بفرح. النص: «تعرّفوا على شمّوغ، الشماغ اللي ما بقدر يسكت… بلعبة ممنوع فيها الحكي». | Shammogh, a cartoon red-and-white shemagh with a face, saying hello. Text: “Meet Shammogh, the shemagh who can’t stop talking… in a game where talking isn’t allowed.” |
| `post-03-how-it-works` | خطوات اللعب على خلفية غامقة: ١ طلّع البطاقة، ٢ مثّلها بالحركات بس، ٣ فريقك بحزر قبل ما يخلص الوقت. | How to play, in three numbered steps on a dark background: draw a card, act it out with gestures only, your team guesses before time runs out. |
| `post-04-card-mansaf` | بطاقة حمرا مكتوب عليها «منسف» من فئة أكل وشرب، وشمّوغ ساكت وتمّه مسكّر. النص: «مين بيقدر يمثّلها؟ اكتبوا بالتعليقات كيف بتمثّلوها». | A red game card reading “Mansaf” from the Food & Drink category, with Shammogh keeping his mouth shut. Text: “Who can act this one? Tell us how in the comments.” |
| `post-05-three-modes` | ٣ طرق للعب، كل وحدة برسمة تطريز: تمثيل، عالجبين (الجوال على جبينك والكل بمثّلك)، ومين أسرع؟ (أول واحد بجاوب بياخذ النقطة). | Three ways to play, each with a cross-stitch icon: Charades, Heads Up (phone on your forehead while everyone acts) and Who’s Fastest? (first to guess scores). |
| `post-06-categories` | على خلفية حمرا: «٥١٠ بطاقة، ١٦ فئة… من المنسف للجاهة»، وتحتها ٩ رسومات تطريز للفئات مثل الأكل والأماكن والأعراس. | On red: “510 cards, 16 categories… from mansaf to the jaha”, above nine cross-stitch category icons such as food, places and weddings. |
| `post-07-saying` | بخط كبير من فئة حكي أردني: «يا زلمة!»، وتحتها «مثّلها… بدون ما تحكيها»، وشمّوغ جاهز للتحدّي. | From the Jordanian Sayings category, in big letters: “Ya zalameh!”, then “Act it out… without saying it”, with Shammogh ready for the challenge. |
| `post-08-heads-up` | جوال بالعرض عليه شاشة وضع عالجبين، وشمّوغ جنبه. النص: «عالجبين! الجوال على جبينك والكل بمثّلك. نزّله إذا عرفتها، ارفعه لتتخطّى». | A phone held sideways showing the Heads Up screen, next to Shammogh. Text: “Heads up! Phone on your forehead, everyone acts. Tilt down if you got it, up to skip.” |
| `post-09-play-now` | شمّوغ فرحان على خلفية غامقة. النص: «يلا نلعبها: مجانية، بدون حساب، وبتشتغل بدون إنترنت. الرابط بالبايو». | A delighted Shammogh on a dark background. Text: “Let’s play: free, no account, works offline. Link in bio.” |

### Stories

| File | Arabic | English |
| --- | --- | --- |
| `story-01-guess-the-word` | «احزر الكلمة! شمّوغ بمثّل… شو بتكون؟» وشمّوغ بفكّر. | “Guess the word! Shammogh is acting… what is it?” with Shammogh thinking. |
| `story-02-game-night` | إعلان «ليلة ولا كلمة كل خميس الساعة ٨» في [اسم المحل]، والجائزة [الجائزة]، وشمّوغ لابس نظارة شمسية. | “Wala Kelmeh night, every Thursday at 8” at [venue], prize: [prize], with Shammogh in sunglasses. |
| `story-03-suggest-a-card` | «عندك بطاقة؟ اقترح كلمة أو موقف، وإذا انضاف للعبة بنكتب اسمك بقائمة الشكر»، وشمّوغ متحمّس. | “Got a card? Suggest a word or moment, and if it’s added we’ll thank you by name”, with an excited Shammogh. |
| `story-04-this-or-that` | «شو أصعب تمثّل؟» بطاقتين: «الجاهة» ولّا «نتايج التوجيهي». | “Which is harder to act?” Two cards: “Il-Jaha” or “Tawjihi results”. |
| `story-05-new-card-drop` | «بطاقة جديدة انضافت للعبة»: بطاقة حمرا مكتوب عليها «مسخّن»، باقتراح من [الاسم]. | “New card added to the game”: a red card reading “Msakhan”, suggested by [name]. |

### Reel and TikTok covers

| File | Arabic | English |
| --- | --- | --- |
| `reel-cover-01-auntie-mansaf` | شمّوغ بيضحك، والعنوان: «لما خالتك تمثّل منسف 😂». | Shammogh laughing, with the title “When your auntie acts out mansaf 😂”. |
| `reel-cover-02-family-vs-friends` | شمّوغ جاهز للتحدّي على خلفية حمرا، والعنوان: «العيلة ضد الصحاب: مين بيفوز؟». | Shammogh ready to compete on red, with the title “Family vs friends: who wins?”. |
| `reel-cover-03-impossible-card` | شمّوغ مصدوم على خلفية غامقة، والعنوان: «أصعب بطاقة باللعبة 😳». | A shocked Shammogh on a dark background, with the title “The hardest card in the game 😳”. |

## Hashtags

Use 5 to 8 per post, mixed:
- **Brand:** #ولا_كلمة #WalaKelmeh #شموغ
- **Topic:** #لعبة_تمثيل #سهرات #ألعاب_جماعية #charades #partygames
- **Place:** #الأردن #عمان #Jordan #Amman
- **Seasonal:** #رأس_السنة #الشتوية #رمضان (in season only)

## Stories (1080×1920)

Keep the top 250 px and bottom 300 px clear for Instagram's own buttons.

| File | Use | Interactive sticker |
| --- | --- | --- |
| `story-01-guess-the-word` | Weekly guessing game: post a short clip of someone acting | Quiz |
| `story-02-game-night` | Partner cafés announce their «ليلة ولا كلمة» (edit day, venue, prize) | Countdown |
| `story-03-suggest-a-card` | Ask for card ideas, link to the website form | Question or link |
| `story-04-this-or-that` | Which is harder to act? | Poll |
| `story-05-new-card-drop` | Announce a suggested card that made it in, thanking the contributor | — |

## Reel and TikTok covers (1080×1920)

`reel-cover-01-auntie-mansaf`, `reel-cover-02-family-vs-friends`, `reel-cover-03-impossible-card`. The title sits in the middle third so it survives the grid crop.

## TikTok and Reels ideas

1. «لما خالتك تمثّل منسف» 😂: real family members acting one card each
2. **Family vs friends:** the same 5 cards, two groups, who wins?
3. **Hardest card challenge:** «حكي أردني» only, 30 seconds
4. **Heads-up fails:** compilation of the funniest wrong guesses
5. **POV: جدّك بمثّل "التوجيهي"**
6. **Guess with us:** act a card to camera, the answer appears at the end, viewers comment first
7. **شمّوغ reacts:** use the stickers as reactions over clips
8. **Café night recap:** a partner venue's game night in 15 seconds
9. **New Year's Eve countdown game** (late December), following the blog article's plan
10. **«بطاقتكم انضافت»:** thank a fan whose suggested card is now in the game

## Rhythm

- 3 feed posts a week, stories most days, 2 reels or TikToks a week.
- Reply to every comment in the first hour; the «اكتبوا بالتعليقات» posts are built for that.
- Reuse the best comments as cards: suggestions become content.
