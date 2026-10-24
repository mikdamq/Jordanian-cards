import { CategoryIcon, InstallButton, Logo, Screen, TatreezBand, ThemeToggle } from '../components';
import { CARDS, CATEGORIES } from '../data/cards';
import type { ThemePref } from '../hooks';
import { CONTACT_EMAIL } from '../config';

interface Props {
  onPlay: () => void;
  onHowTo: () => void;
  theme: ThemePref;
  onTheme: () => void;
}

export function Home({ onPlay, onHowTo, theme, onTheme }: Props) {
  return (
    <Screen className="home">
      <div className="home__fabric" aria-hidden>
        <div className="fringe" />
      </div>
      <div className="home__top">
        <ThemeToggle pref={theme} onCycle={onTheme} />
      </div>

      <div className="home__hero">
        <Logo />
        <p className="home__tag">مثّلها وخلّي فريقك يحزر… بس ولا كلمة! 🤐</p>
      </div>

      <TatreezBand cell={5} />

      <div className="home__patches" aria-hidden>
        {CATEGORIES.slice(0, 8).map((c, i) => (
          <span key={c.id} style={{ animationDelay: `${i * 0.06}s` }}>
            <CategoryIcon id={c.id} size={52} />
          </span>
        ))}
      </div>

      <div className="stack home__cta">
        <button className="btn btn--primary btn--xl" onClick={onPlay}>
          يلا نلعب
        </button>
        <button className="btn btn--ghost" onClick={onHowTo}>
          طريقة اللعب
        </button>
        <InstallButton autoOpen from="home" />
        <p className="muted center">
          {CARDS.length} بطاقة · {CATEGORIES.length} فئات · تمثيل وعالجبين
        </p>
        <nav className="home__links">
          <a href={`mailto:${CONTACT_EMAIL}?subject=${encodeURIComponent('ولا كلمة — ملاحظات')}`}>ملاحظات</a>
          <span aria-hidden>·</span>
          <a href="privacy.html">الخصوصية</a>
        </nav>
      </div>
    </Screen>
  );
}
