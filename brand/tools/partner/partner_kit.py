"""Café partner kit: print-ready PDFs (with 3 mm bleed) and PNG previews.

    python3 partner_kit.py [--url https://walakelmeh.com/play/?ref=venue]
"""
import io, json, os, subprocess, sys, tempfile
import qrcode, qrcode.image.svg
HERE = tempfile.mkdtemp(prefix='partner-kit-')
REPO = '/home/user/Jordanian-cards'
OUT = os.path.join(REPO, 'brand', 'partner-kit')
URL = sys.argv[sys.argv.index('--url') + 1] if '--url' in sys.argv else 'https://walakelmeh.com/play/?ref=cafe'
F = lambda *p: 'file://' + os.path.join(REPO, *p)
M = lambda k: F('brand', 'mascot', 'svg', f'shammogh-{k}.svg')
ART = lambda k: F('website', 'out', 'assets', 'art', k + '.svg')
BLEED = 3
FONTS = '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Almarai:wght@800&family=Cairo:wght@600;800&display=swap">'

def qr_svg():
    q = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_M, border=0)
    q.add_data(URL); q.make(fit=True)
    img = q.make_image(image_factory=qrcode.image.svg.SvgPathImage)
    buf = io.BytesIO(); img.save(buf)
    return buf.getvalue().decode().replace('<?xml version=\'1.0\' encoding=\'UTF-8\'?>', '').replace('fill="#000000"', 'fill="#2a1f1a"')
QR = qr_svg()

def doc(w, h, body, css=''):
    """w, h are trim size in mm; the page adds bleed on every side."""
    W, H = w + 2 * BLEED, h + 2 * BLEED
    return f'''<!doctype html><html lang="ar" dir="rtl"><head><meta charset="utf-8">{FONTS}<style>
@page {{ size: {W}mm {H}mm; margin: 0 }}
*{{box-sizing:border-box}} html,body{{margin:0;width:{W}mm;height:{H}mm;overflow:hidden}}
body{{position:relative;background:#f4ecdd;color:#2a1f1a;font-family:Cairo,sans-serif;-webkit-print-color-adjust:exact;print-color-adjust:exact}}
.weave{{position:absolute;inset:0;background-image:repeating-linear-gradient(0deg,rgba(90,60,30,.05) 0 .5mm,transparent .5mm 3mm),repeating-linear-gradient(90deg,rgba(90,60,30,.05) 0 .5mm,transparent .5mm 3mm)}}
.band{{position:absolute;left:0;right:0;height:7mm;background:repeating-linear-gradient(45deg,#b5121b 0 3.5mm,#f6efe3 3.5mm 7mm)}}
.trim{{position:absolute;inset:{BLEED}mm}}
h1{{margin:0;font-family:Almarai,sans-serif;font-weight:800;color:#b5121b;line-height:1.15}}
h2{{margin:0;font-family:Almarai,sans-serif;font-weight:800;line-height:1.2}}
p{{margin:0;color:#7a6650}}
.qr svg{{width:100%;height:100%;display:block}}
.qrbox{{background:#fff;border-radius:4mm;padding:3mm;box-shadow:0 0 0 .6mm #dccbae}}
{css}</style></head><body><div class="weave"></div>{body}</body></html>'''

ITEMS = []
def item(name, w, h, html): ITEMS.append((name, w, h, html))

# 1. Table tent: A5 sheet (148 x 210 mm), folds in half into two A6 faces; the top face is upside down.
def tent_face(flip):
    return f'''<div style="position:absolute;left:0;right:0;{'top' if flip else 'bottom'}:0;height:105mm;{'transform:rotate(180deg);' if flip else ''}">
  <div style="position:absolute;inset:7mm 9mm 9mm;display:grid;grid-template-rows:auto 1fr auto;justify-items:center;text-align:center;gap:3mm">
    <img src="{F('brand','logo','lockup','lockup-arabic-horizontal-on-light.svg')}" style="height:13mm">
    <div style="display:flex;gap:6mm;align-items:center">
      <div class="qrbox qr" style="width:42mm;height:42mm">{QR}</div>
      <div style="display:grid;gap:1.5mm;text-align:right;width:58mm"><h1 style="font-size:9.5mm">امسح والعب!</h1><p style="font-size:3.6mm;line-height:1.5">لعبة تمثيل للطاولة كلها. جوال واحد بكفّي، ومجانية.</p></div>
    </div>
    <p style="font:800 3.4mm Cairo;color:#2a1f1a">مثّلها… بس ولا كلمة! · Scan to play</p>
  </div></div>'''
item('table-tent-a5-fold', 148, 210, doc(148, 210, f'''<div class="trim">{tent_face(True)}{tent_face(False)}
<div style="position:absolute;left:-{BLEED}mm;right:-{BLEED}mm;top:105mm;border-top:.3mm dashed #b3a184"></div>
<span style="position:absolute;top:103mm;left:2mm;font-size:2.4mm;color:#b3a184;direction:ltr">fold</span></div>
<div class="band" style="top:0;height:5mm"></div><div class="band" style="bottom:0;height:5mm"></div>'''))

# 2. Poster A3 (297 x 420 mm) with write-in spaces
def line(label):
    return f'<div style="display:flex;gap:5mm;align-items:end"><h2 style="font-size:12mm;flex:none">{label}</h2><span style="flex:1;border-bottom:1mm dashed #7a6650;height:12mm"></span></div>'
item('poster-a3', 297, 420, doc(297, 420, f'''<div class="band" style="top:0;height:12mm"></div>
<div class="trim">
  <img src="{F('brand','logo','lockup','lockup-arabic-horizontal-on-light.svg')}" style="position:absolute;top:22mm;left:50%;transform:translateX(-50%);height:30mm">
  <div style="position:absolute;top:68mm;left:0;right:0;text-align:center;display:grid;gap:4mm"><span style="justify-self:center;background:#b5121b;color:#fff8ee;font:800 9mm Cairo;padding:2mm 10mm;border-radius:20mm">ليلة</span>
  <h1 style="font-size:40mm">ولا كلمة</h1><p style="font:600 11mm Cairo">طاولة ضد طاولة… بس ولا كلمة!</p></div>
  <img src="{M('cool')}" style="position:absolute;top:150mm;left:50%;transform:translateX(-50%);width:120mm">
  <div style="position:absolute;top:268mm;left:28mm;right:28mm;display:grid;gap:9mm">{line('اليوم:')}{line('الساعة:')}{line('الجائزة:')}</div>
  <div style="position:absolute;bottom:22mm;left:28mm;right:28mm;display:flex;justify-content:space-between;align-items:center">
    <p style="font:800 7mm Cairo;color:#2a1f1a">امسح والعب <span style="color:#7a6650;font-weight:600;font-size:5.5mm">· Game night: scan to play</span></p>
    <div class="qrbox qr" style="width:38mm;height:38mm">{QR}</div></div>
</div><div class="band" style="bottom:0;height:12mm"></div>'''))

# 3. Round window sticker, 150 mm. The red runs 3 mm past the cut; the cut path is its own file.
item('window-sticker-150mm', 150, 150, doc(150, 150, f'''<div style="position:absolute;inset:0;border-radius:50%;background:#b5121b"></div>
<div class="trim"><img src="{F('brand','logo','partner','partner-badge-arabic.svg')}" style="position:absolute;inset:0;width:150mm;height:150mm"></div>''', 'body{background:#fff} .weave{display:none}'))
item('window-sticker-150mm-dieline', 150, 150, doc(150, 150, f'''<div class="trim" style="border-radius:50%;border:.25mm solid #ec008c"></div>
<p style="position:absolute;bottom:1mm;left:0;right:0;text-align:center;direction:ltr;font-size:2.2mm;color:#ec008c">cut path, 150 mm circle. Do not print.</p>''', 'body{background:#fff} .weave{display:none}'))

# 4. Table card A6 (105 x 148 mm): how to play + QR
steps = [('١', 'جيبوا جوال واحد وامسحوا الكود'), ('٢', 'واحد بمثّل البطاقة بالحركات بس'), ('٣', 'الطاولة بتحزر قبل ما يخلص الوقت')]
item('table-card-a6', 105, 148, doc(105, 148, f'''<div class="band" style="top:0;height:6mm"></div>
<div class="trim" style="padding:9mm 8mm 7mm;display:grid;grid-template-rows:auto auto 1fr auto;gap:4mm">
  <img src="{F('brand','logo','lockup','lockup-arabic-horizontal-on-light.svg')}" style="height:11mm;justify-self:center">
  <h1 style="font-size:8mm;text-align:center">كيف نلعب؟</h1>
  <ol style="margin:0;padding:0;list-style:none;display:grid;gap:3mm;align-content:start">{''.join(f'<li style="display:flex;gap:3mm;align-items:center"><span style="flex:none;width:8mm;height:8mm;border-radius:50%;background:#b5121b;color:#fff8ee;display:grid;place-items:center;font:800 4.5mm Almarai">{n}</span><span style="font:800 4.2mm Cairo">{t}</span></li>' for n, t in steps)}</ol>
  <div style="display:flex;gap:4mm;align-items:center;justify-content:center"><div class="qrbox qr" style="width:30mm;height:30mm">{QR}</div>
  <img src="{M('shh')}" style="width:30mm"></div>
</div>'''))

# 5. Partner guide, A4 (210 x 297 mm), one page
guide = [
  ('قبل الليلة', ['اختاروا يوم ثابت بالأسبوع وساعة (مثلاً الخميس ٨ مساءً).', 'حطّوا البوستر على الباب وستاند الطاولة على كل طاولة.', 'انشروا ستوري «ليلة ولا كلمة» قبلها بيومين، ويوم الليلة.']),
  ('بالليلة', ['كل طاولتين جنب بعض بيتحدّوا على جوال واحد: كل طاولة فريق.', 'نفس الإعدادات للكل: وضع «تمثيل»، ٦٠ ثانية للدور، ٣ جولات.', 'الطاولات الفايزة بتلعب النهائي قدّام الكل، والفايز بياخذ الجائزة.']),
  ('أفكار للجائزة', ['خصم على الفاتورة للطاولة الفايزة.', 'مشروب أو حلو مجاني.', 'طاولة محجوزة للأسبوع الجاي.']),
  ('بعد الليلة', ['صوّروا الفريق الفايز (بموافقتهم) وانشروا مع #ولا_كلمة.', 'تاجونا @walakelmeh لنعيد النشر ونذكر محلّكم.', 'ابعتولنا شو انبسطوا عليه وشو بدكم نضيف.']),
]
cols = ''.join(f'<section style="background:#fbf6ec;border:.4mm solid #dccbae;border-radius:5mm;padding:6mm;display:grid;gap:3mm;align-content:start"><h2 style="font-size:7mm;color:#b5121b">{h}</h2><ul style="margin:0;padding-inline-start:5mm;display:grid;gap:2mm;font:600 4mm/1.6 Cairo">{"".join(f"<li>{x}</li>" for x in li)}</ul></section>' for h, li in guide)
item('partner-guide-a4', 210, 297, doc(210, 297, f'''<div class="band" style="top:0;height:9mm"></div>
<div class="trim" style="padding:16mm 14mm 12mm;display:grid;grid-template-rows:auto auto 1fr auto;gap:7mm">
  <div style="display:flex;justify-content:space-between;align-items:center"><img src="{F('brand','logo','lockup','lockup-arabic-horizontal-on-light.svg')}" style="height:14mm"><span style="font:800 4mm Cairo;color:#7a6650">دليل الشريك</span></div>
  <div style="display:flex;gap:8mm;align-items:center"><div style="display:grid;gap:3mm;flex:1"><h1 style="font-size:11mm">كيف تعملوا <span style="white-space:nowrap">«ليلة ولا كلمة»</span></h1>
    <p style="font:600 4.4mm/1.7 Cairo">ليلة تمثيل وتخمين بمحلّكم: الزبائن بيلعبوا من جوالاتهم، طاولة ضد طاولة، والفريق الفايز بياخذ جائزة منكم. ما بدها أجهزة، واللعبة بتشتغل بدون إنترنت.</p></div>
    <img src="{M('wink')}" style="width:42mm"></div>
  <div style="display:grid;grid-template-columns:1fr 1fr;gap:5mm">{cols}</div>
  <div style="display:flex;justify-content:space-between;align-items:center;border-top:.4mm dashed #c7b08a;padding-top:5mm">
    <div style="display:grid;gap:1mm"><b style="font:800 5mm Almarai">بالكيت</b><span style="font:600 3.8mm Cairo;color:#7a6650">ستاند طاولة · بوستر A3 · بطاقة طاولة · ستيكر الواجهة · قالب ستوري</span>
    <span style="font:600 3.8mm Cairo;color:#7a6650">أي سؤال: <b style="color:#2a1f1a;direction:ltr;unicode-bidi:isolate">hello@walakelmeh.com</b></span></div>
    <div class="qrbox qr" style="width:26mm;height:26mm">{QR}</div></div>
</div><div class="band" style="bottom:0;height:7mm"></div>'''))

os.makedirs(os.path.join(OUT, 'previews'), exist_ok=True)
jobs = []
for name, w, h, html in ITEMS:
    f = os.path.join(HERE, 'html', name + '.html'); os.makedirs(os.path.dirname(f), exist_ok=True)
    open(f, 'w', encoding='utf-8').write(html)
    jobs.append({'src': f, 'pdf': os.path.join(OUT, name + '.pdf'), 'png': os.path.join(OUT, 'previews', name + '.png'), 'w': w + 2 * BLEED, 'h': h + 2 * BLEED})
json.dump(jobs, open(os.path.join(HERE, 'jobs.json'), 'w'))
open(os.path.join(HERE, 'render.cjs'), 'w').write('''const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const jobs = require(process.argv[2]);
(async () => { const b = await chromium.launch(); const p = await b.newPage();
  for (const j of jobs) {
    const px = (mm) => Math.round(mm / 25.4 * 96);
    await p.setViewportSize({ width: px(j.w), height: px(j.h) });
    await p.goto('file://' + j.src); await p.waitForTimeout(900);
    await p.pdf({ path: j.pdf, width: j.w + 'mm', height: j.h + 'mm', printBackground: true, pageRanges: '1' });
    await p.screenshot({ path: j.png, scale: 'device' });
  }
  await b.close(); })();''')
subprocess.run(['node', os.path.join(HERE, 'render.cjs'), os.path.join(HERE, 'jobs.json')], check=True, timeout=300)
print('built', [i[0] for i in ITEMS], 'QR ->', URL)
