"""Social kit: profile pictures, launch posts (1080x1350), stories and reel covers (1080x1920), highlight covers."""
import json, os, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
REPO = '/home/user/Jordanian-cards'
OUT = os.path.join(REPO, 'brand', 'social')
F = lambda *p: 'file://' + os.path.join(REPO, *p)
M = lambda k: F('brand', 'mascot', 'svg', f'shammogh-{k}.svg')
ART = lambda k: F('website', 'out', 'assets', 'art', k + '.svg')
RAW = lambda k: F('brand', 'store', 'raw', k + '.png')
HANDLE = '@walakelmeh'
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Almarai:wght@800&family=Cairo:wght@600;800&display=swap">'
THEME = {'cream': ('#f4ecdd', '#2a1f1a', '#b5121b', '#7a6650'), 'red': ('#b5121b', '#fff8ee', '#fff8ee', '#ffd9d3'), 'night': ('#17110e', '#f4ecdd', '#ec5f66', '#b5a28a')}
LOCK = {'cream': F('brand', 'logo', 'lockup', 'lockup-arabic-horizontal-on-light.svg'), 'night': F('brand', 'logo', 'lockup', 'lockup-arabic-horizontal-on-dark.svg'),
        'red': F('brand', 'logo', 'wordmark', 'wordmark-arabic-on-red.svg')}

def doc(w, h, theme, body, css=''):
    bg, ink, accent, muted = THEME[theme]
    return f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">{FONTS}<style>
*{{box-sizing:border-box}} body{{margin:0;width:{w}px;height:{h}px;overflow:hidden;position:relative;background:{bg};color:{ink};font-family:Cairo,sans-serif}}
.weave{{position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,rgba(90,60,30,.05) 0 2px,transparent 2px 12px),repeating-linear-gradient(90deg,rgba(90,60,30,.05) 0 2px,transparent 2px 12px)}}
.band{{position:absolute;left:0;right:0;height:30px;background:repeating-linear-gradient(45deg,#b5121b 0 15px,#f6efe3 15px 30px)}}
.band.dark{{background:repeating-linear-gradient(45deg,#2a1f1a 0 15px,#f6efe3 15px 30px)}}
h1{{margin:0;font:800 96px/1.15 Almarai,sans-serif;color:{accent}}} h2{{margin:0;font:800 64px/1.2 Almarai,sans-serif;color:{ink}}}
p{{margin:0;font:600 40px/1.5 Cairo,sans-serif;color:{muted}}}
.handle{{position:absolute;bottom:58px;left:64px;font:800 30px Cairo,sans-serif;color:{muted};direction:ltr}}
.logo{{position:absolute;bottom:44px;right:64px;height:64px}}
.masc{{position:absolute;filter:drop-shadow(0 18px 24px rgba(23,17,14,.3))}}
.card{{background:#b5121b;color:#fff8ee;border-radius:40px;text-align:center;box-shadow:0 14px 0 #8e0e16;outline:4px dashed rgba(255,248,238,.5);outline-offset:-22px;display:grid;place-content:center;gap:8px}}
.card b{{font:800 120px/1.2 Almarai,sans-serif}} .card span{{font:600 40px Cairo,sans-serif;color:#ffd9d3;direction:ltr}}
.chip{{display:inline-block;background:{accent};color:{bg};font:800 34px Cairo,sans-serif;padding:10px 30px;border-radius:999px}}
{css}</style></head><body><div class="weave"></div>{body}</body></html>'''

def foot(theme, logo=True):
    return f'<span class="handle">{HANDLE}</span>' + (f'<img class="logo" src="{LOCK[theme]}">' if logo else '')

# ---------- launch posts (1080x1350) ----------
P = []
def post(name, theme, body, css=''):
    P.append((f'post-{len(P)+1:02d}-{name}', 1080, 1350, doc(1080, 1350, theme, body, css)))

post('arrived', 'red', f'''<div class="band dark" style="top:0"></div>
<img src="{F('brand','logo','symbol','symbol-light.svg')}" style="position:absolute;top:150px;left:50%;transform:translateX(-50%);width:300px">
<img src="{LOCK['red']}" style="position:absolute;top:500px;left:50%;transform:translateX(-50%);width:760px">
<div style="position:absolute;top:880px;left:0;right:0;text-align:center;display:grid;gap:18px"><h1 style="font-size:84px">وصلت!</h1><p>لعبة التمثيل الأردنية للسهرات</p></div>
{foot('red', False)}''')
post('meet-shammogh', 'cream', f'''<div class="band" style="top:0"></div>
<div style="position:absolute;top:120px;right:80px;left:80px;display:grid;gap:22px"><span class="chip" style="justify-self:start">تعرّفوا على</span><h1>شمّوغ</h1>
<p style="max-width:560px">الشماغ اللي ما بقدر يسكت… بلعبة ممنوع فيها الحكي.</p></div>
<img class="masc" src="{M('wave')}" style="width:620px;bottom:120px;left:40px">{foot('cream')}''')
post('how-it-works', 'night', f'''<div class="band" style="top:0"></div>
<div style="position:absolute;top:130px;right:80px;left:80px;display:grid;gap:44px"><h1>مثّلها… بس ولا كلمة!</h1>
<ol style="margin:0;padding:0;list-style:none;display:grid;gap:34px">{''.join(f'<li style="display:flex;gap:28px;align-items:center"><span style="flex:none;width:96px;height:96px;border-radius:50%;background:#b5121b;color:#fff8ee;display:grid;place-items:center;font:800 50px Almarai">{n}</span><h2 style="font-size:54px">{t}</h2></li>' for n, t in (('١', 'طلّع البطاقة'), ('٢', 'مثّلها بالحركات بس'), ('٣', 'فريقك بحزر قبل ما يخلص الوقت')))}</ol></div>
{foot('night')}''')
post('card-mansaf', 'cream', f'''<div class="band" style="top:0"></div>
<div style="position:absolute;top:110px;left:0;right:0;text-align:center;display:grid;gap:14px"><span class="chip" style="justify-self:center">🍽️ أكل وشرب</span><h2>مين بيقدر يمثّلها؟</h2></div>
<div class="card" style="position:absolute;top:400px;left:200px;right:200px;height:560px"><b>منسف</b><span>Mansaf</span></div>
<img class="masc" src="{M('shh')}" style="width:300px;bottom:110px;left:40px">
<p style="position:absolute;bottom:150px;right:80px;width:520px;text-align:right">اكتبوا بالتعليقات كيف بتمثّلوها 👇</p>{foot('cream', False)}''')
post('three-modes', 'cream', f'''<div class="band" style="top:0"></div>
<div style="position:absolute;top:110px;left:0;right:0;text-align:center"><h1 style="font-size:88px">٣ طرق للعب</h1></div>
<div style="position:absolute;top:330px;left:70px;right:70px;display:grid;gap:26px">{''.join(f'<div style="display:flex;gap:30px;align-items:center;background:#fbf6ec;border:3px dashed #c7b08a;border-radius:34px;padding:26px 30px"><img src="{ART("mode-" + k)}" style="width:130px;height:130px;object-fit:contain;background:#f6efe3;border-radius:24px;padding:10px"><div><h2 style="font-size:52px">{n}</h2><p style="font-size:34px">{d}</p></div></div>' for k, n, d in (('classic', 'تمثيل', 'واحد بمثّل وفريقه بحزر'), ('headsup', 'عالجبين', 'الجوال على جبينك والكل بمثّلك'), ('fastest', 'مين أسرع؟', 'بدون فرق، أول واحد بياخذ النقطة')))}</div>
{foot('cream')}''')
cats = ['food', 'places', 'screen', 'life', 'sayings', 'heritage', 'animals', 'weddings', 'nineties']
post('categories', 'red', f'''<div class="band dark" style="top:0"></div>
<div style="position:absolute;top:110px;left:0;right:0;text-align:center;display:grid;gap:10px"><h1>٥١٠ بطاقة</h1><p style="color:#ffd9d3">١٦ فئة… من المنسف للجاهة</p></div>
<div style="position:absolute;top:420px;left:150px;right:150px;display:grid;grid-template-columns:repeat(3,1fr);gap:30px">{''.join(f'<div style="aspect-ratio:1;background:#f6efe3;border-radius:36px;display:grid;place-items:center;outline:4px dashed #e8c9b4;outline-offset:-14px"><img src="{ART("cat-" + c)}" style="width:62%"></div>' for c in cats)}</div>
{foot('red', False)}''')
post('saying', 'night', f'''<div class="band" style="top:0"></div>
<div style="position:absolute;top:130px;left:0;right:0;text-align:center;display:grid;gap:14px"><span class="chip" style="justify-self:center">🗣️ حكي أردني</span></div>
<div style="position:absolute;top:330px;left:0;right:0;text-align:center;display:grid;gap:20px"><h1 style="font-size:180px;color:#f4ecdd">يا زلمة!</h1><p>مثّلها… بدون ما تحكيها 😏</p></div>
<img class="masc" src="{M('compete')}" style="width:380px;bottom:110px;right:50%;transform:translateX(50%)">{foot('night', False)}''')
post('heads-up', 'cream', f'''<div class="band" style="top:0"></div>
<div style="position:absolute;top:110px;right:80px;left:80px;display:grid;gap:18px"><h1>عالجبين!</h1><p style="max-width:620px">الجوال على جبينك، والكل بمثّلك. نزّله إذا عرفتها، ارفعه لتتخطّى.</p></div>
<div style="position:absolute;top:560px;left:90px;width:620px;height:350px;border-radius:44px;background:#17110e;padding:14px;transform:rotate(-5deg);box-shadow:0 24px 48px rgba(23,17,14,.3)"><img src="{RAW('headsup')}" style="width:100%;height:100%;border-radius:32px;object-fit:cover"></div>
<img class="masc" src="{M('headsup')}" style="width:420px;bottom:110px;right:40px">{foot('cream', False)}''')
post('play-now', 'night', f'''<div class="band" style="top:0"></div>
<div style="position:absolute;top:120px;left:0;right:0;text-align:center;display:grid;gap:22px"><h1 style="font-size:110px">العبوها هسّا</h1><p>مجانية · بدون حساب · بتشتغل بدون إنترنت</p>
<span class="chip" style="justify-self:center;font-size:40px">الرابط بالبايو 🔗</span></div>
<img class="masc" src="{M('yay')}" style="width:600px;bottom:120px;left:50%;transform:translateX(-50%)">{foot('night', False)}''')

# ---------- stories (1080x1920; keep the top 250px and bottom 300px clear) ----------
S = []
def story(name, theme, body):
    S.append((f'story-{len(S)+1:02d}-{name}', 1080, 1920, doc(1080, 1920, theme, body)))
story('guess-the-word', 'red', f'''<div style="position:absolute;top:300px;left:0;right:0;text-align:center;display:grid;gap:20px"><h1 style="font-size:110px">احزر الكلمة!</h1><p style="color:#ffd9d3">شمّوغ بمثّل… شو بتكون؟</p></div>
<img class="masc" src="{M('think')}" style="width:560px;top:640px;left:50%;transform:translateX(-50%)">
<div style="position:absolute;top:1280px;left:120px;right:120px;height:260px;border:5px dashed #fff8ee;border-radius:40px;display:grid;place-items:center;font:800 40px Cairo;color:#ffd9d3">ضيفوا ستيكر «اختبار» هون</div>''')
story('game-night', 'night', f'''<div style="position:absolute;top:280px;left:0;right:0;text-align:center;display:grid;gap:24px"><span class="chip" style="justify-self:center">ليلة ولا كلمة</span><h1 style="font-size:120px">كل خميس</h1><p>الساعة ٨ · اسم المحل هون</p></div>
<img class="masc" src="{M('cool')}" style="width:560px;top:820px;left:50%;transform:translateX(-50%)">
<div style="position:absolute;bottom:330px;left:0;right:0;text-align:center"><p style="color:#f4ecdd">الفريق الفايز بياخذ: <b style="color:#ddae4a">الجائزة هون</b></p></div>''')
story('suggest-a-card', 'cream', f'''<div style="position:absolute;top:300px;right:90px;left:90px;display:grid;gap:22px"><h1 style="font-size:100px">عندك بطاقة؟</h1><p>اقترح كلمة أو موقف، وإذا انضاف للعبة بنكتب اسمك بقائمة الشكر.</p></div>
<img class="masc" src="{M('love')}" style="width:520px;top:820px;right:60px">
<div style="position:absolute;bottom:330px;left:90px;right:90px;height:200px;border:5px dashed #c7b08a;border-radius:40px;display:grid;place-items:center;font:800 38px Cairo;color:#7a6650">ستيكر «سؤال» أو رابط الموقع</div>''')
story('this-or-that', 'cream', f'''<div style="position:absolute;top:300px;left:0;right:0;text-align:center"><h1 style="font-size:96px">شو أصعب تمثّل؟</h1></div>
<div style="position:absolute;top:620px;left:90px;right:90px;display:grid;gap:60px">
<div class="card" style="height:380px"><b style="font-size:96px">الجاهة</b><span>Il-Jaha</span></div>
<div style="text-align:center;font:800 70px Almarai;color:#7a6650">ولّا</div>
<div class="card" style="height:380px;background:#4f6b2c;box-shadow:0 14px 0 #2f5f22"><b style="font-size:96px">نتايج التوجيهي</b><span>Nataij It-Tawjihi</span></div></div>''')
story('new-card-drop', 'night', f'''<div style="position:absolute;top:300px;left:0;right:0;text-align:center;display:grid;gap:18px"><span class="chip" style="justify-self:center">بطاقة جديدة 🎉</span><h2>انضافت للعبة</h2></div>
<div class="card" style="position:absolute;top:640px;left:140px;right:140px;height:620px"><b>مسخّن</b><span>Msakhan</span></div>
<p style="position:absolute;bottom:340px;left:0;right:0;text-align:center">اقتراح: الاسم هون 🙏</p>''')

# ---------- reel / TikTok covers (1080x1920; title in the middle third) ----------
R = []
def reel(name, theme, title, mood):
    R.append((f'reel-cover-{len(R)+1:02d}-{name}', 1080, 1920, doc(1080, 1920, theme, f'''
<img class="masc" src="{M(mood)}" style="width:640px;top:430px;left:50%;transform:translateX(-50%)">
<div style="position:absolute;top:1080px;left:70px;right:70px;text-align:center"><h1 style="font-size:104px;line-height:1.2">{title}</h1></div>
<div class="band" style="bottom:0"></div>''')))
reel('auntie-mansaf', 'cream', 'لما خالتك تمثّل «منسف» 😂', 'laugh')
reel('family-vs-friends', 'red', 'العيلة ضد الصحاب: مين بيفوز؟', 'compete')
reel('impossible-card', 'night', 'أصعب بطاقة باللعبة 😳', 'shock')

# ---------- profile + highlights ----------
X = []
X.append(('profile-patch', 1080, 1080, doc(1080, 1080, 'cream', f'<img src="{F("brand","logo","symbol","symbol-primary.svg")}" style="position:absolute;inset:150px;width:780px">')))
X.append(('profile-shammogh', 1080, 1080, doc(1080, 1080, 'red', f'<img src="{M("wink")}" style="position:absolute;width:820px;left:130px;top:150px">')))
HL = [('how', 'كيف تلعب', 'mode-classic'), ('cats', 'الفئات', 'cat-food'), ('shammogh', 'شمّوغ', None), ('nights', 'سهراتكم', 'mode-fastest'), ('cafes', 'للمقاهي', 'cat-heritage'), ('soon', 'قريباً', 'cat-nineties')]
for k, label, art in HL:
    icon = f'<img src="{ART(art)}" style="width:300px">' if art else f'<img src="{M("wave")}" style="width:380px">'
    X.append((f'highlight-{k}', 1080, 1920, doc(1080, 1920, 'cream', f'''<div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);width:620px;height:620px;border-radius:50%;background:#b5121b;display:grid;place-items:center;outline:8px dashed #f6efe3;outline-offset:-34px">
<div style="width:440px;height:440px;border-radius:50%;background:#f6efe3;display:grid;place-items:center">{icon}</div></div>
<p style="position:absolute;top:1360px;left:0;right:0;text-align:center;font:800 64px Almarai;color:#2a1f1a">{label}</p>''')))

def render(items, sub):
    d = os.path.join(OUT, sub); os.makedirs(d, exist_ok=True)
    jobs = []
    for name, w, h, html in items:
        f = os.path.join(HERE, 'html', name + '.html'); os.makedirs(os.path.dirname(f), exist_ok=True)
        open(f, 'w', encoding='utf-8').write(html)
        jobs.append({'src': f, 'out': os.path.join(d, name + '.png'), 'w': w, 'h': h})
    return jobs
jobs = render(P, 'posts') + render(S, 'stories') + render(R, 'reel-covers') + render(X, 'profile')
json.dump(jobs, open(os.path.join(HERE, 'jobs.json'), 'w'))
open(os.path.join(HERE, 'render.cjs'), 'w').write('''const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const jobs = require(process.argv[2]);
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  for (const j of jobs) { await p.setViewportSize({ width: j.w, height: j.h }); await p.goto('file://' + j.src); await p.waitForTimeout(700);
    await p.screenshot({ path: j.out }); }
  await b.close(); })();''')
subprocess.run(['node', os.path.join(HERE, 'render.cjs'), os.path.join(HERE, 'jobs.json')], check=True, timeout=400)
print('rendered', len(jobs))
