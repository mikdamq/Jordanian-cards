import { Patch, Screen, TatreezBand, TiltDemo } from '../components';
import { MODE_ART } from '../art';

export function HowTo({ onBack }: { onBack: () => void }) {
  return (
    <Screen>
      <header className="bar">
        <button className="icon-btn" onClick={onBack} aria-label="رجوع">
          →
        </button>
        <h1>طريقة اللعب</h1>
      </header>

      <section className="panel seam">
        <div className="panel__head">
          <Patch art={MODE_ART.classic} size={52} />
          <h2>تمثيل</h2>
        </div>
        <ol>
          <li>واحد من الفريق بمسك الجوال وبشوف البطاقة.</li>
          <li>بمثّلها بالإشارات والحركات بس — ممنوع الحكي، وممنوع تحرك شفايفك!</li>
          <li>فريقه بحاول يحزر قبل ما يخلص الوقت.</li>
          <li>
            اسحب البطاقة <b>يمين</b> أو اكبس <b>عرفوها</b> إذا حزروا، واسحبها <b>يسار</b> أو اكبس <b>تخطّي</b> إذا علقت.
          </li>
        </ol>
      </section>

      <section className="panel seam">
        <div className="panel__head">
          <Patch art={MODE_ART.headsup} size={52} />
          <h2>عالجبين</h2>
        </div>
        <TiltDemo />
        <ol>
          <li>امسك الجوال بالعرض بإيديك الثنتين وحطه على جبينك، والشاشة لبرّا.</li>
          <li>فريقك بمثّل الكلمة إلك بدون ولا كلمة.</li>
          <li>نزّل الجوال لتحت ⬇️ إذا عرفتها، ارفعه لفوق ⬆️ لتتخطّى.</li>
          <li>رجّعه على جبينك قبل البطاقة الجاية.</li>
        </ol>
      </section>

      <section className="panel seam">
        <h2>🏆 النقاط</h2>
        <p>كل بطاقة صح بنقطة. بعد كل دور بتقدروا تصلّحوا النتيجة إذا صار غلط. الفرق بتتناوب، واللي بجمع أكثر بعد آخر جولة بربح.</p>
      </section>

      <TatreezBand cell={4} />

      <button className="btn btn--primary btn--xl" onClick={onBack}>
        فهمت، يلا!
      </button>
    </Screen>
  );
}
