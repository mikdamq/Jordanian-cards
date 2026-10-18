import { Logo, Screen, Star } from '../components';
import { CARDS } from '../data/cards';

export function Home({ onPlay, onHowTo }: { onPlay: () => void; onHowTo: () => void }) {
  return (
    <Screen className="home">
      <div className="home__hero">
        <Star size={220} className="home__star" />
        <Logo />
        <p className="home__tag">مثّلها وخلّي فريقك يحزر… بس ولا كلمة! 🤐</p>
      </div>
      <div className="stack">
        <button className="btn btn--primary btn--xl" onClick={onPlay}>
          يلا نلعب
        </button>
        <button className="btn btn--ghost" onClick={onHowTo}>
          طريقة اللعب
        </button>
        <p className="muted center">{CARDS.length} بطاقة · تمثيل وعالجبين</p>
      </div>
    </Screen>
  );
}
