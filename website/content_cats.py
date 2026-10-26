"""Categories index + one page per category."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))

C = {
  'index_title': {'ar': 'فئات ولا كلمة: ٥١٠ بطاقة تمثيل أردنية بـ١٦ فئة', 'en': '510 Jordanian Charades Cards in 16 Categories | Wala Kelmeh'},
  'index_desc': {'ar': 'تصفّح فئات لعبة ولا كلمة: أكل أردني، أماكن، أفلام، أعراس، رمضان، نوستالجيا التسعينات وغيرها. شوف أمثلة من البطاقات واختار فئتك.',
                 'en': 'Browse the Wala Kelmeh categories: Jordanian food, places, movies, weddings, Ramadan, 90s nostalgia and more. See sample cards and pick your favourites.'},
  'index_crumb': {'ar': 'الفئات', 'en': 'Categories'},
  'index_h1': {'ar': 'فئات «ولا كلمة»', 'en': 'Wala Kelmeh categories'},
  'index_answer': {'ar': '«ولا كلمة» فيها ٥١٠ بطاقة تمثيل موزّعة على ١٦ فئة، من الأكل الأردني والأماكن لنوستالجيا التسعينات وباكيت الشباب. كل بطاقة بالعربي ومع كتابة بالحروف الإنجليزية، وبتقدروا تختاروا الفئات اللي بدكم إياها قبل كل لعبة.',
                   'en': 'Wala Kelmeh has 510 charades cards across 16 categories, from Jordanian food and places to 90s nostalgia and the Shabab pack. Every card is in Arabic with Arabizi, and you choose which categories to play before each game.'},
  'cards_word': {'ar': 'بطاقة', 'en': 'cards'},
  'see_cards': {'ar': 'شوف البطاقات', 'en': 'See the cards'},
  'samples_h': {'ar': 'أمثلة من البطاقات', 'en': 'Sample cards'},
  'samples_note': {'ar': 'هاي {n} من {total} بطاقة. الباقي مفاجأة بنص اللعبة 😉', 'en': 'These are {n} of {total} cards. The rest are a surprise in the game 😉'},
  'levels': {'ar': ['سهلة', 'متوسطة', 'صعبة'], 'en': ['Easy', 'Medium', 'Hard']},
  'level_h': {'ar': 'المستويات', 'en': 'Difficulty'},
  'best_h': {'ar': 'الأحسن لـ', 'en': 'Best for'},
  'related_h': {'ar': 'فئات ثانية ممكن تعجبكم', 'en': 'More categories you might like'},
  'play_cat': {'ar': 'يلا نلعب هالفئة', 'en': 'Let’s play this category'},
  'cat_title': {'ar': '{name}: {n} بطاقة تمثيل | ولا كلمة', 'en': '{name}: {n} Charades Cards | Wala Kelmeh'},
  'cat_h1': {'ar': 'فئة {name}', 'en': '{name}'},
  'cta_h': {'ar': 'جاهزين تمثّلوها؟', 'en': 'Ready to act them out?'},
}

# id: (Arabic intro, English intro, Arabic best-for, English best-for)
CAT = {
  'screen': ('من كابتن ماجد وسالي لتايتانيك وهاري بوتر: أفلام ومسلسلات وكرتون كبرنا عليه، بتعرفها الأجيال كلها.',
             'From Captain Majid and Sally to Titanic and Harry Potter: films, series and cartoons every generation knows.',
             'سهرات العيلة بكل الأعمار', 'Family nights with all ages'),
  'food': ('منسف ومقلوبة وكنافة وفلافل… أطيب فئة باللعبة. تمثيل الأكل الأردني بيضحّك وبيجوّع.',
           'Mansaf, maqloubeh, knafeh, falafel… the tastiest category. Acting out Jordanian food is funny, and it makes you hungry.',
           'العزايم وقعدات بعد الغدا', 'Dinner parties and after-lunch sittings'),
  'places': ('من البتراء ووادي رم للبحر الميت ووسط البلد: جولة بالأردن بدون ولا كلمة.',
             'From Petra and Wadi Rum to the Dead Sea and downtown Amman: a tour of Jordan without a single word.',
             'المغتربين اللي مشتاقين للبلد', 'Jordanians abroad missing home'),
  'life': ('تستنى السرفيس، تفاصل مع البياع، قطعت الكهربا… مواقف أردنية يومية كل واحد عاشها.',
           'Waiting for the service taxi, haggling with a shopkeeper, the power cut… everyday Jordanian moments everyone has lived.',
           'الضحك على حالنا', 'Laughing at ourselves'),
  'sayings': ('يا هلا، على راسي، يا زلمة، عنجد؟… الحكي الأردني اللي بنحكيه كل يوم، مثّله بدون ما تحكيه!',
              'Ya hala, 3ala rasi, ya zalameh, 3anjad?… the Jordanian phrases we say every day. Now act them out without saying them.',
              'التحدّي الأصعب للممثّلين', 'The ultimate challenge for actors'),
  'heritage': ('شماغ وعقال ودلّة وفنجان وصقر: أغراض وتراث أردني أصيل.',
               'Shemagh, agal, coffee pot, cup and falcon: authentic Jordanian heritage and objects.',
               'المناسبات الوطنية والجَمعات الكبيرة', 'National days and big gatherings'),
  'fun': ('النشامى، ضربة جزاء، طاولة زهر، دي جي بالعرس: رياضة وفن وهوايات.',
          'The Nashama, a penalty kick, backgammon, a wedding DJ: sports, arts and hobbies.',
          'سهرات الشباب ومباريات الكورة', 'Game nights and football evenings'),
  'animals': ('قرد، فيل، جمل، ديك… أسهل فئة للصغار وأضحك فئة للكبار.',
              'Monkey, elephant, camel, rooster… the easiest category for kids and the funniest for grown-ups.',
              'الصغار والعيلة', 'Kids and families'),
  'jobs': ('شرطي سير، حلّاق، سوّاق تكسي، دكتور أسنان: مهن بتعرفها من أول حركة.',
           'Traffic police, barber, taxi driver, dentist: jobs you recognise from the first gesture.',
           'البداية للاعبين الجداد', 'Warming up new players'),
  'office': ('اجتماع زووم، الواي فاي فصل، المدير جاي: جو الشغل بكل تفاصيله.',
             'A Zoom meeting, the Wi-Fi dropping, “the manager’s coming”: office life in all its glory.',
             'فعاليات الشركات وجَمعات الزملاء', 'Team events and colleague nights out'),
  'weddings': ('العريس والعروس، زغرودة، قص الكيك، الجاهة: أعراس ومناسبات بطابع أردني.',
               'The groom and bride, a zaghrouta, cutting the cake, the jaha: weddings and occasions, Jordanian style.',
               'سهرات الحنّة وقبل العرس', 'Henna nights and pre-wedding gatherings'),
  'nineties': ('شريط كاسيت، جيم بوي، نوكيا ٣٣١٠، كرتون الصبح: رجعة للتسعينات.',
               'Cassette tapes, Game Boy, the Nokia 3310, morning cartoons: straight back to the 90s.',
               'جيل التسعينات والثمانينات', 'The 80s and 90s generation'),
  'amman': ('مكة مول، جبل عمّان، الرينبو، الدوار السابع: عمّان وأحياؤها وأماكنها المعروفة.',
            'Mecca Mall, Jabal Amman, Rainbow Street, Seventh Circle: Amman’s neighbourhoods and landmarks.',
            'أهل عمّان واللي بيعرفوها منيح', 'Ammanis and anyone who knows the city'),
  'ramadan': ('سحور، إفطار، تمر وحليب، كعك العيد، مراجيح العيد: أجواء رمضان والعيد.',
              'Suhoor, iftar, dates and milk, Eid cookies, Eid swings: the spirit of Ramadan and Eid.',
              'سهرات رمضان والعيد', 'Ramadan nights and Eid visits'),
  'actions': ('بتسبح، بتطبخ، بتعطس، بتنفخ بالون: أفعال وحركات تمثيل صافي.',
              'Swimming, cooking, sneezing, blowing up a balloon: pure mime actions.',
              'الصغار ومين أسرع؟', 'Kids, and the who’s fastest mode'),
  'shabab': ('واسطة، مفلس آخر الشهر، فويس عشر دقايق، ستوري انستغرام: باكيت الشباب الأجرأ شوي.',
             'Wasta, broke at the end of the month, a ten-minute voice note, an Instagram story: the slightly cheekier Shabab pack.',
             'سهرات الصحاب والجامعة', 'Friends’ nights and university crowds'),
}

def load_cards():
    s = open(os.path.join(HERE, '..', 'src', 'data', 'cards.ts'), encoding='utf-8').read()
    raw = s[s.index('const RAW'):s.index('export const CARDS')]
    out = {}
    for m in re.finditer(r'\n  (\w+): \[(.*?)\n  \],', raw, re.S):
        out[m.group(1)] = [(a, b, int(c)) for a, b, c in re.findall(r"\['([^']*)',\s*'([^']*)',\s*(\d)\]", m.group(2))]
    return out

def samples(cards, n=12):
    """The first easy cards, topped up with medium ones if a category has fewer easy cards."""
    easy = [c for c in cards if c[2] == 1]
    med = [c for c in cards if c[2] == 2]
    return (easy + med)[:n]

# «كيف تمثّلوا هالفئة؟»: three acting tips per category, shown on its page (unique, useful text
# that also answers "how do you act out …?" questions).
TIPS_H = {'ar': 'كيف تمثّلوا هالفئة؟', 'en': 'How to act these cards'}
TIPS = {
  'screen': (['ابدأ بإشارة الفيلم (لفّ إيدك كأنك بتصوّر بكاميرا قديمة) أو المسلسل (ارسم شاشة بإيديك).', 'مثّل أشهر مشهد أو حركة للبطل، مش القصة كلها.', 'للكرتون، قلّد مشية الشخصية أو حركتها المشهورة.'],
             ['Start with the film signal (crank an old camera) or the TV signal (draw a screen with your hands).', 'Act the most famous scene or the hero’s signature move, not the whole plot.', 'For cartoons, copy the character’s walk or trademark gesture.']),
  'food': (['مثّل كيف بتنوكل: المنسف بالإيد، الكنافة بتمطّ، الفلافل بتنزل عالزيت.', 'إذا الأكلة صعبة، اطبخها قدّامهم خطوة خطوة.', 'وجّه فريقك على المكوّن الأشهر أوّل: رز، جبنة، حمص.'],
           ['Act how it’s eaten: mansaf by hand, stretchy knafeh, falafel dropping into the fryer.', 'If the dish is tricky, cook it in front of them step by step.', 'Point your team to the best-known ingredient first: rice, cheese, chickpeas.']),
  'places': (['ارسم شكل المكان بإيديك: القلعة، البحر، المدرّج.', 'مثّل شو الناس بتعمل هناك: تطفي عالبحر الميت، تطلع درج القلعة.', 'قسّم الاسم المركّب لكلمات، ومثّل كل كلمة لحال.'],
             ['Draw the place’s shape with your hands: a castle, the sea, the amphitheatre.', 'Act what people do there: floating in the Dead Sea, climbing the Citadel steps.', 'Split two-word names and act each word on its own.']),
  'life': (['هاي مواقف، فمثّلها كمشهد قصير: مين موجود وشو بيصير.', 'ركّز على اللحظة اللي الكل بيعرفها، مثل زمّور السيارة أو رنّة جوال الماما.', 'خلّي فريقك يحزر الموقف، مش الكلمات بالحرف.'],
           ['These are moments, so act them as a short scene: who’s there and what happens.', 'Focus on the bit everyone recognises, like the car horn or mum’s ringtone.', 'Let your team guess the situation, not the exact words.']),
  'sayings': (['عدّ كلمات المثل على أصابعك أوّل.', 'مثّل كل كلمة لحال، أو مثّل الموقف اللي بينقال فيه المثل.', 'لما فريقك يقرّب، أشّر بإيدك «كمّل».'],
              ['Count the words on your fingers first.', 'Act each word, or act the situation where people say it.', 'When your team gets close, wave “keep going”.']),
  'heritage': (['مثّل كيف الغرض بينستعمل: الدلة بتصب القهوة، المهباش بيدق، الشماغ بينلف.', 'إذا كان أداة، ارسم شكلها بالهوا.', 'الجدّات بيعرفوا أغراض التراث أسرع، فخلّوا وحدة بفريقكم.'],
               ['Act how the object is used: pouring from the dallah, pounding with the mihbash, wrapping the shemagh.', 'If it’s a tool, trace its shape in the air.', 'Grandparents spot heritage items fastest, so get one on your team.']),
  'fun': (['مثّل الحركة الأشهر بالرياضة: ضربة الجزاء، رمية السلة.', 'للغنا والفن، مثّل الآلة كأنك بتعزف عليها.', 'للاعبين والفنانين المشهورين، قلّد حركتهم المعروفة.'],
          ['Act the sport’s signature move: a penalty kick, a basketball shot.', 'For music and the arts, mime playing the instrument.', 'For famous players and artists, copy their trademark gesture.']),
  'animals': (['مشية الحيوان أحسن تلميح: الجمل بيتمختر، البطريق بيتهزهز.', 'استعمل إيديك للأذان أو الذيل أو المنقار.', 'وممنوع الأصوات! الحركة بس.'],
              ['The walk is your best clue: a camel’s sway, a penguin’s waddle.', 'Use your hands for ears, a tail or a beak.', 'And no animal noises: only movement is allowed.']),
  'jobs': (['مثّل أداة المهنة: سمّاعة الدكتور، مقص الحلاق، طبشورة الأستاذ.', 'مثّل ثانيتين من يوم شغلهم.', 'إذا علقت، مثّل المكان اللي بيشتغلوا فيه.'],
           ['Act the tool of the trade: a doctor’s stethoscope, the barber’s scissors, a teacher’s chalk.', 'Show two seconds of their working day.', 'Stuck? Act the place where they work.']),
  'office': (['مواقف شغل الكل عاشها: الاجتماع اللي ما بيخلص، إيميل «رد على الكل»، استراحة القهوة.', 'مثّل ردة فعلك أكثر من الموقف نفسه.', 'ممتازة لسهرات الشركات وفعاليات الفرق.'],
             ['Office moments everyone has lived: the endless meeting, the reply-all email, the coffee break.', 'Act your reaction more than the moment itself.', 'Great for company nights and team events.']),
  'weddings': (['مثّل الطقس الأشهر: الدبكة، الزفّة، تقطيع الكيك، الجاهة وهي بتطلب.', 'اعمل حالك لابس الثوب أو البدلة.', 'صفّق كأنك بالعرس، بس بدون صوت!'],
               ['Act the best-known ritual: the dabke, the zaffeh, cutting the cake, the jaha asking for the bride’s hand.', 'Pretend you’re wearing the thobe or the suit.', 'Clap along like you’re at the wedding, silently!']),
  'nineties': (['رجّع فريقك للتسعينات: الأتاري، لفّ شريط الكاسيت بقلم، الكاميرا أبو الفيلم.', 'مثّل كيف كنا نستعمل الغرض، لأنه الجيل الجديد يمكن ما شافه.', 'هاي البطاقات بتضحّك الأهل أكثر من الصغار.'],
               ['Take your team back to the 90s: the Atari, rewinding a cassette with a pencil, the film camera.', 'Act how we used it, since younger players may never have seen one.', 'These cards make parents laugh more than kids.']),
  'amman': (['مثّل شو بتعمل بالمنطقة: أكلة بوسط البلد، تسوّق، طلعة عالجبل.', 'ارسم الطلعات والنزلات بالهوا، عمّان كلها جبال.', 'قسّم الأسماء المركّبة (جبل، شارع، دوّار) ومثّل كل جزء.'],
            ['Act what you do there: a meal downtown, shopping, a drive up the hill.', 'Draw the slopes in the air: Amman is all hills.', 'Split compound names (Jabal, Street, Circle) and act each part.']),
  'ramadan': (['مثّل اللحظات: مدفع الإفطار، أوّل تمرة، المسحّراتي بطبلته، الفانوس.', 'للعيد، مثّل العيدية والمعمول والأواعي الجديدة.', 'فئة مثالية لسهرات رمضان مع العيلة.'],
              ['Act the moments: the iftar cannon, the first date, the mesaharati with his drum, the lantern.', 'For Eid, act the eidiyeh money, ma’amoul and new clothes.', 'Perfect for family Ramadan nights.']),
  'actions': (['هاي الفئة كلها حركات، فاعمل الفعل نفسه.', 'بلّش بطيء وواضح، وبعدين زيد.', 'مناسبة كتير للصغار، ولأوّل مرة بتلعبوا.'],
              ['This category is pure mime: just do the action.', 'Start slow and clear, then build up.', 'Ideal for kids and for your first game.']),
  'shabab': (['بطاقات أجرأ شوي عن حياة الشباب: الواسطة، آخر الشهر، الفويس نوت الطويل.', 'بالغ بالتمثيل، هون المبالغة هي النكتة.', 'الباكيت اختياري، فشغّلوه بس إذا السهرة بتناسب.'],
             ['Slightly cheekier cards about young life: wasta, broke at the end of the month, the endless voice note.', 'Exaggerate: here over-acting is the joke.', 'The pack is optional, so switch it on only when the crowd suits it.']),
}
