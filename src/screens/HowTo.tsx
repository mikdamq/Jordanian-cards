import { Screen } from '../components';

export function HowTo({ onBack }: { onBack: () => void }) {
  return (
    <Screen>
      <header className="bar">
        <button className="icon-btn" onClick={onBack} aria-label="رجوع">
          →
        </button>
        <h1>طريقة اللعب</h1>
      </header>

      <section className="panel">
        <h2>🎭 تمثيل</h2>
        <ol>
          <li>واحد من الفريق بمسك الجوال وبشوف البطاقة.</li>
          <li>بمثّلها بالإشارات والحركات بس — ممنوع الحكي، وممنوع تحرك شفايفك!</li>
          <li>فريقه بحاول يحزر قبل ما يخلص الوقت.</li>
          <li>اكبس <b>عرفوها</b> إذا حزروا، أو <b>تخطّي</b> إذا علقت.</li>
        </ol>
      </section>

      <section className="panel">
        <h2>📱 عالجبين</h2>
        <ol>
          <li>حط الجوال على جبينك والشاشة لبرّا — أنت ما بتشوف الكلمة.</li>
          <li>فريقك بمثّلها إلك بدون ولا كلمة.</li>
          <li>نزّل الجوال لتحت ⬇️ إذا عرفتها، ارفعه لفوق ⬆️ لتتخطّى.</li>
          <li>رجّع الجوال على جبينك قبل البطاقة الجاية.</li>
        </ol>
      </section>

      <section className="panel">
        <h2>🏆 النقاط</h2>
        <p>كل بطاقة صح بنقطة. بعد كل دور بتقدروا تصلّحوا النتيجة إذا صار غلط. الفرق بتتناوب، واللي بجمع أكثر بعد آخر جولة بربح.</p>
      </section>

      <button className="btn btn--primary" onClick={onBack}>
        فهمت، يلا!
      </button>
    </Screen>
  );
}
