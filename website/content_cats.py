"""Categories index + one page per category."""
import os, re
HERE = os.path.dirname(os.path.abspath(__file__))

C = {
  'index_title': {'ar': 'فئات ولا كلمة: ٥١٠ بطاقة تمثيل أردنية بـ١٦ فئة', 'en': 'Wala Kelmeh Categories: 510 Jordanian Charades Cards in 16 Categories'},
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
  'play_cat': {'ar': 'العب هالفئة هسّا', 'en': 'Play this category now'},
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

def samples(cards, n=8):
    """The first easy cards, topped up with medium ones if a category has fewer easy cards."""
    easy = [c for c in cards if c[2] == 1]
    med = [c for c in cards if c[2] == 2]
    return (easy + med)[:n]
