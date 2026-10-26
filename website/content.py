"""All website copy, in Arabic and English. One entry per string: {'ar': ..., 'en': ...}."""

SITE = 'https://walakelmeh.com'
CONTACT = 'hello@walakelmeh.com'
# Official accounts: linked in the footer and in the Organization's sameAs. Add TikTok here once it exists.
SOCIAL = {'Instagram': 'https://www.instagram.com/walakelmeh/'}
# Analytics IDs live in the game's src/config.ts, so the site and the game always match:
# GoatCounter (cookie-free, always on), and Google Analytics + Microsoft Clarity (after consent).
def _config(name):
    import os, re
    src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'src', 'config.ts'), encoding='utf-8').read()
    m = re.search(r"export const %s = '([^']*)'" % name, src)
    return m.group(1) if m else ''
GOATCOUNTER, GA_ID, CLARITY_ID = _config('GOATCOUNTER_CODE'), _config('GA_ID'), _config('CLARITY_ID')
CONSENT = {
  'text': {'ar': 'بنستعمل Google Analytics و Microsoft Clarity لنفهم كيف بتنلعب ولا كلمة ونحسّن الموقع. بنشغّلهم بس إذا وافقت، وبتقدر تغيّر رأيك وقت ما بدك.',
           'en': 'We use Google Analytics and Microsoft Clarity to understand how Wala Kelmeh is played and improve the site. They only run if you agree, and you can change your mind any time.'},
  'yes': {'ar': 'تمام', 'en': 'OK'},
  'no': {'ar': 'لا، شكراً', 'en': 'No thanks'},
  'privacy': {'ar': 'الخصوصية', 'en': 'Privacy'},
  'settings': {'ar': 'إعدادات الإحصائيات', 'en': 'Analytics settings'},
  'label': {'ar': 'الإحصائيات', 'en': 'Analytics'},
}

CATEGORIES = [  # id, Arabic, English, cards
    ('screen', 'أفلام ومسلسلات', 'Movies & TV', 40),
    ('food', 'أكل وشرب', 'Food & Drink', 40),
    ('places', 'أماكن', 'Places', 38),
    ('life', 'مواقف أردنية', 'Jordanian Moments', 38),
    ('sayings', 'حكي أردني', 'Jordanian Sayings', 38),
    ('heritage', 'تراث وأغراض', 'Heritage', 38),
    ('fun', 'رياضة وفن', 'Sports & Arts', 38),
    ('animals', 'حيوانات', 'Animals', 25),
    ('jobs', 'مهن', 'Jobs', 25),
    ('office', 'جو الشغل', 'Office Life', 25),
    ('weddings', 'أعراس ومناسبات', 'Weddings & Occasions', 25),
    ('nineties', 'نوستالجيا التسعينات', '90s Nostalgia', 25),
    ('amman', 'عمّان وأحيائها', 'Amman', 25),
    ('ramadan', 'رمضان والعيد', 'Ramadan & Eid', 25),
    ('actions', 'أفعال وحركات', 'Actions', 25),
    ('shabab', 'باكيت الشباب', 'Shabab Pack', 40),
]
TOTAL_CARDS = sum(c[3] for c in CATEGORIES)

T = {
  'lang_switch': {'ar': 'English', 'en': 'عربي'},
  'nav': {
    'how': {'ar': 'كيف تلعب', 'en': 'How to play'},
    'categories': {'ar': 'الفئات', 'en': 'Categories'},
    'cafes': {'ar': 'للمقاهي', 'en': 'For cafés'},
    'stickers': {'ar': 'ستيكرات شمّوغ', 'en': 'Stickers'},
    'blog': {'ar': 'المدونة', 'en': 'Blog'},
  },
  'play': {'ar': 'يلا نلعب', 'en': 'Let’s play'},
  'install': {'ar': 'ثبّتها على جوالك', 'en': 'Install on your phone'},
  'meta_title': {'ar': 'ولا كلمة: لعبة التمثيل الأردنية للسهرات', 'en': 'Wala Kelmeh: The Jordanian Charades Party Game'},
  'meta_desc': {
    'ar': 'مثّلها… بس ولا كلمة! لعبة تمثيل وتخمين أردنية بأكثر من ٥٠٠ بطاقة و٣ طرق للعب. مجانية، بدون حساب، وبتشتغل بدون إنترنت.',
    'en': 'Act it out, not a word! A Jordanian charades and heads-up game with 500+ cards and three ways to play. Free, no account, works offline.'},
  'hero_eyebrow': {'ar': 'لعبة التمثيل الأردنية', 'en': 'The Jordanian charades game'},
  'hero_h1': {'ar': 'مثّلها… بس ولا كلمة!', 'en': 'Act it out. Not a word.'},
  'hero_sub': {
    'ar': 'طلّع البطاقة، مثّلها بالحركات بس، وخلّي فريقك يحزر قبل ما يخلص الوقت. أكثر من ٥٠٠ بطاقة أردنية لسهرات العيلة والصحاب.',
    'en': 'Draw a card, act it out with gestures only, and get your team to guess before time runs out. Over 500 Jordanian cards for family nights and friends’ sahras.'},
  'hero_facts': {'ar': ['مجانية دايماً', 'بدون إنترنت', 'بدون حساب'], 'en': ['Free forever', 'Works offline', 'No account']},
  'stores_soon': {'ar': 'قريباً على', 'en': 'Coming soon to'},
  'modes_h': {'ar': '٣ طرق للعب', 'en': 'Three ways to play'},
  'modes_p': {'ar': 'من سهرة هادية لحرب تخمين. اختاروا اللي بناسب الجَمعة.', 'en': 'From a calm night in to a full-on guessing war. Pick what suits the crowd.'},
  'modes': [
    ('classic', {'ar': 'تمثيل', 'en': 'Classic charades'},
     {'ar': 'واحد بمثّل وفريقه بحزر. اسحب البطاقة يمين إذا عرفوها، ويسار لتتخطّاها.', 'en': 'One player acts, the team guesses. Swipe right when they get it, left to skip.'},
     {'ar': '٢ لـ ٤ فرق', 'en': '2 to 4 teams'}),
    ('headsup', {'ar': 'عالجبين', 'en': 'Heads up'},
     {'ar': 'حط الجوال على جبينك بالعرض وفريقك يمثّل لك. نزّله إذا عرفتها، وارفعه لتتخطّى.', 'en': 'Hold the phone sideways on your forehead while your team acts it out. Tilt down for correct, up to skip.'},
     {'ar': '٢ لـ ٤ فرق', 'en': '2 to 4 teams'}),
    ('fastest', {'ar': 'مين أسرع؟', 'en': 'Who’s fastest?'},
     {'ar': 'بدون فرق. واحد بمثّل والكل بجاوب، وأول واحد بعرفها بياخذ النقطة.', 'en': 'No teams. One acts, everyone shouts, and the first right answer takes the point.'},
     {'ar': '٢ لـ ١٢ لاعب', 'en': '2 to 12 players'}),
  ],
  'cats_h': {'ar': f'{TOTAL_CARDS} بطاقة، ١٦ فئة', 'en': f'{TOTAL_CARDS} cards, 16 categories'},
  'cats_p': {'ar': 'من المنسف للجاهة لنتايج التوجيهي. كل بطاقة بالعربي ومع كتابة بالحروف الإنجليزية.', 'en': 'From mansaf to the jaha to tawjihi results. Every card in Arabic, with Arabizi underneath.'},
  'cards_word': {'ar': 'بطاقة', 'en': 'cards'},
  'how_h': {'ar': 'كيف تلعب؟', 'en': 'How to play'},
  'how': [
    ({'ar': 'اختاروا الطريقة', 'en': 'Pick a mode'}, {'ar': 'تمثيل، عالجبين، أو مين أسرع؟ وبعدين الفرق والوقت وعدد الجولات.', 'en': 'Classic, heads up or who’s fastest, then teams, timer and rounds.'}),
    ({'ar': 'مثّلها… بس ولا كلمة', 'en': 'Act it out, silently'}, {'ar': 'إشارات وحركات بس. ممنوع الحكي، ممنوع الأصوات، وممنوع تأشّر على إشي بالغرفة.', 'en': 'Gestures only. No talking, no sounds, no pointing at things in the room.'}),
    ({'ar': 'اجمعوا النقاط', 'en': 'Score and win'}, {'ar': 'كل بطاقة صح بنقطة. بعد آخر جولة، الفريق اللي معه أكثر بيفوز… وبتشاركوا صورة النتيجة.', 'en': 'Every correct card is a point. After the last round the top team wins, and you can share the result.'}),
  ],
  'promise_h': {'ar': 'وعدنا إلك', 'en': 'Our promise'},
  'promise': [
    ({'ar': 'مجانية دايماً', 'en': 'Free forever'}, {'ar': 'اللعبة الأساسية مجانية، وما في إعلانات بنص اللعب.', 'en': 'The core deck is free, and there’s never an ad mid-game.'}),
    ({'ar': 'بدون إنترنت', 'en': 'Works offline'}, {'ar': 'ثبّتها مرة وحدة، والعبها بالرحلة أو بالمزرعة.', 'en': 'Install once, then play on a road trip or at the farm.'}),
    ({'ar': 'بدون حساب', 'en': 'No account'}, {'ar': 'لا تسجيل ولا إيميل. افتح والعب.', 'en': 'No sign-up, no email. Open it and play.'}),
    ({'ar': 'بطاقات ما بتتكرر', 'en': 'No repeats'}, {'ar': 'اللعبة بتتذكر شو لعبتوا، فكل سهرة بطاقات جديدة.', 'en': 'The game remembers what you played, so every night brings new cards.'}),
  ],
  'cafes_eyebrow': {'ar': 'للمقاهي والأماكن', 'en': 'For cafés and venues'},
  'cafes_h': {'ar': 'ليلة ولا كلمة… عندك', 'en': 'Host a Wala Kelmeh night'},
  'cafes_p': {'ar': 'خلّي زبائنك يسهروا عندك أطول: تحدّيات بين الطاولات، كود خاص بمحلّك بيفتح فئة باسمك، وخصم للفريق الفائز.', 'en': 'Keep guests around longer: table-vs-table challenges, a code that unlocks a category named after your place, and a reward for the winning team.'},
  'cafes_cta': {'ar': 'احكي معنا', 'en': 'Talk to us'},
  'stickers_h': {'ar': 'ستيكرات شمّوغ', 'en': 'Shammogh stickers'},
  'stickers_p': {'ar': 'شمّوغ هو الشماغ اللي ما بقدر يسكت… بلعبة ممنوع فيها الحكي. ١٤ ستيكر لواتساب.', 'en': 'Shammogh is the shemagh who can’t stop talking, in a game where talking isn’t allowed. 14 stickers for WhatsApp.'},
  'stickers_cta': {'ar': 'شوف الستيكرات', 'en': 'See the stickers'},
  'faq_h': {'ar': 'أسئلة بتنسأل كثير', 'en': 'Questions people ask'},
  'faq': [
    ({'ar': 'هل اللعبة مجانية؟', 'en': 'Is it free?'}, {'ar': 'آه. اللعبة الأساسية بكل فئاتها مجانية دايماً، وما في إعلانات بنص اللعب. ممكن نضيف باكيتات خاصة بالمستقبل، وبتكون اختيارية.', 'en': 'Yes. The core game and all its categories are free forever, with no ads mid-game. Special packs may come later, always optional.'}),
    ({'ar': 'كيف بثبّتها على جوالي؟', 'en': 'How do I install it?'}, {'ar': 'افتح اللعبة واكبس «ثبّتها على جوالك». على أندرويد بتنثبّت بكبسة وحدة، وعلى آيفون بتورجيك الخطوتين: زر المشاركة، وبعدين «إضافة إلى الشاشة الرئيسية». إذا فاتحها من انستغرام أو تيك توك، افتحها بالمتصفح أوّل. وقريباً على المتاجر.', 'en': 'Open the game and tap “Install on your phone” («ثبّتها على جوالك»). On Android it installs in one tap; on iPhone it shows you the two steps: Share, then “Add to Home Screen”. If you opened it from Instagram or TikTok, open it in your browser first. Store versions are coming soon.'}),
    ({'ar': 'بتشتغل بدون إنترنت؟', 'en': 'Does it work offline?'}, {'ar': 'آه، بعد أول مرة بتفتحها كل البطاقات بتنحفظ على جوالك.', 'en': 'Yes. After the first visit, every card is saved on your phone.'}),
    ({'ar': 'إذا مش أردني، بقدر ألعبها؟', 'en': 'I’m not Jordanian. Can I play?'}, {'ar': 'أكيد! فئات مثل الأكل والأفلام والحيوانات والأفعال بيعرفها كل العرب، وكل بطاقة مكتوبة كمان بالحروف الإنجليزية.', 'en': 'Of course. Food, movies, animals and actions work for every Arab, and every card is also written in Arabizi.'}),
    ({'ar': 'لأي عمر؟', 'en': 'What ages is it for?'}, {'ar': 'للكل، من الصغار للجدّ. وفي باكيت للشباب إذا بدكم إشي أجرأ شوي.', 'en': 'Everyone, from kids to grandparents. There’s also a Shabab pack if you want something a bit cheekier.'}),
  ],
  'skip': {'ar': 'تخطّى للمحتوى', 'en': 'Skip to content'},
  'about_h': {'ar': 'شو هي «ولا كلمة»؟', 'en': 'What is Wala Kelmeh?'},
  'about_p': {
    'ar': '«ولا كلمة» لعبة تمثيل وتخمين أردنية مجانية، بتنلعب على الجوال من المتصفح أو كتطبيق. فيها ٥١٠ بطاقات بالعربي ومع كتابة بالحروف الإنجليزية (Arabizi)، موزّعة على ١٦ فئة، و٣ طرق للعب: تمثيل، عالجبين، ومين أسرع؟. انعملت بعمّان سنة ٢٠٢٦ لسهرات العيلة والصحاب، بالأردن وبكل مكان فيه عرب.',
    'en': 'Wala Kelmeh (Arabic for “not a word”) is a free Jordanian charades and heads-up game for phones, played in the browser or installed as an app. It has 510 cards in Arabic with Arabizi transliteration, across 16 categories, and three ways to play: classic charades, heads up and who’s fastest. It was made in Amman in 2026 for family nights and friends’ gatherings, in Jordan and wherever Arabs live.'},
  'facts': [
    ({'ar': 'السعر', 'en': 'Price'}, {'ar': 'مجانية', 'en': 'Free'}),
    ({'ar': 'اللاعبين', 'en': 'Players'}, {'ar': 'من ٢ لـ ١٢', 'en': '2 to 12'}),
    ({'ar': 'البطاقات', 'en': 'Cards'}, {'ar': '٥١٠ بطاقة، ١٦ فئة', 'en': '510 cards, 16 categories'}),
    ({'ar': 'اللغة', 'en': 'Language'}, {'ar': 'عربي، مع كتابة بالإنجليزي', 'en': 'Arabic, with Arabizi'}),
    ({'ar': 'الإنترنت', 'en': 'Internet'}, {'ar': 'مش ضروري بعد التثبيت', 'en': 'Not needed after install'}),
    ({'ar': 'من وين؟', 'en': 'Made in'}, {'ar': 'عمّان، الأردن', 'en': 'Amman, Jordan'}),
  ],
  'footer_cta': {'ar': 'جاهزين للسهرة؟', 'en': 'Ready for tonight?'},
  'col_play': {'ar': 'العب', 'en': 'Play'},
  'col_more': {'ar': 'ولا كلمة', 'en': 'Wala Kelmeh'},
  'og_alt': {'ar': 'ولا كلمة: لعبة التمثيل الأردنية، مع شمّوغ', 'en': 'Wala Kelmeh, the Jordanian charades game, with Shammogh the mascot'},
  'footer_tag': {'ar': 'لعبة التمثيل الأردنية للسهرات', 'en': 'The Jordanian charades party game'},
  'privacy': {'ar': 'الخصوصية', 'en': 'Privacy'},
  'contact': {'ar': 'تواصل معنا', 'en': 'Contact'},
  'rights': {'ar': '© ٢٠٢٦ ولا كلمة', 'en': '© 2026 Wala Kelmeh'},
  'preview_note': {'ar': 'نسخة تجريبية: الروابط للصفحات الثانية رح تشتغل لما نبنيها.', 'en': 'Preview: links to other pages will work once they’re built.'},
}

# ---------- suggestion forms ----------
# Submissions go to our own script on the hosting (static/api/send.php), which emails each one
# to CONTACT. Empty = forms fall back to opening the visitor's email app.
SUGGEST_ENDPOINT = '/api/send.php'
SUGGEST = {
  'by_email': {'ar': 'ابعتها بالإيميل', 'en': 'Send it by email'},
  'card_h': {'ar': 'عندك بطاقة لهالفئة؟', 'en': 'Got a card for this category?'},
  'card_p': {'ar': 'اقترح كلمة أو موقف، وإذا انضافت للعبة بنكتب اسمك بقائمة الشكر (إذا بدك).',
             'en': 'Suggest a word or a moment. If it makes it into the game, we’ll thank you by name (if you like).'},
  'cat_h': {'ar': 'بدك فئة جديدة؟', 'en': 'Want a new category?'},
  'cat_p': {'ar': 'قلنا شو الفئة اللي ناقصة، وأعطينا كم مثال عليها.', 'en': 'Tell us which category is missing, and give us a few examples.'},
  'word': {'ar': 'الكلمة أو الموقف', 'en': 'Word or moment'},
  'word_ph': {'ar': 'مثلاً: مسخّن', 'en': 'e.g. Musakhan'},
  'arabizi': {'ar': 'بالحروف الإنجليزية (اختياري)', 'en': 'In Arabizi (optional)'},
  'arabizi_ph': {'ar': 'Msakhan', 'en': 'Msakhan'},
  'level': {'ar': 'قديش صعبة؟', 'en': 'How hard is it?'},
  'cat_name': {'ar': 'اسم الفئة', 'en': 'Category name'},
  'cat_name_ph': {'ar': 'مثلاً: مسلسلات بدوية', 'en': 'e.g. Bedouin TV series'},
  'examples': {'ar': 'أمثلة (اختياري)', 'en': 'Examples (optional)'},
  'examples_ph': {'ar': 'كلمة بكل سطر', 'en': 'One per line'},
  'name': {'ar': 'اسمك (اختياري)', 'en': 'Your name (optional)'},
  'name_ph': {'ar': 'مثلاً: أبو أحمد من إربد', 'en': 'e.g. Ahmad from Irbid'},
  'send': {'ar': 'ابعت الاقتراح', 'en': 'Send suggestion'},
  'sending': {'ar': 'عم نبعت…', 'en': 'Sending…'},
  'thanks': {'ar': 'وصل! شكراً إلك 🙏 بنقرا كل اقتراح.', 'en': 'Got it, thank you! 🙏 We read every suggestion.'},
  'error': {'ar': 'ما زبطت. جرّب كمان مرة، أو ابعتلنا على الإيميل.', 'en': 'That didn’t work. Try again, or email us.'},
  'privacy': {'ar': 'ما بنطلب إيميل ولا رقم. بنستعمل الاقتراح بس لتطوير اللعبة.', 'en': 'We don’t ask for your email or number. Suggestions are only used to improve the game.'},
  'another': {'ar': 'اقترح كمان', 'en': 'Suggest another'},
  'home_h': {'ar': 'شارك بصناعة اللعبة', 'en': 'Help build the game'},
  'home_p': {'ar': 'عندك كلمة أو فئة ناقصة؟ اقتراحاتكم بتصير بطاقات.', 'en': 'Got a missing word or category? Your suggestions become cards.'},
  'home_cta': {'ar': 'اقترح بطاقة أو فئة', 'en': 'Suggest a card or category'},
}
