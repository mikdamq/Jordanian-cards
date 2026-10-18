import { useEffect, useReducer, useRef, useState } from 'react';
import {
  CategoryIcon,
  Confetti,
  PromptCard,
  RotatePrompt,
  Screen,
  sizeClass,
  TatreezBand,
  TeamAvatar,
  TiltTutorial,
} from '../components';
import { categoryById } from '../data/cards';
import { currentCard, isLastTurn, newGame, reduce, winners, type Game, type Settings } from '../game';
import { useCountdown, useLandscape, useTilt, useWakeLock } from '../hooks';
import { buildDeck, markSeen } from '../lib/deck';
import { feedback } from '../lib/feedback';
import { loadList, save } from '../lib/storage';
import { requestTiltPermission } from '../lib/tilt';

type Dispatch = (a: Parameters<typeof reduce>[1]) => void;

interface Props {
  settings: Settings;
  onExit: () => void;
  onReplay: () => void;
}

/** Fullscreen + landscape lock where the browser allows it (Android); a no-op elsewhere. */
async function enterLandscape() {
  try {
    if (!document.fullscreenElement) await document.documentElement.requestFullscreen?.();
    await (screen.orientation as ScreenOrientation & { lock?: (o: string) => Promise<void> }).lock?.('landscape');
  } catch {
    // iOS and desktop browsers don't support this; the rotate prompt covers it.
  }
}

function leaveLandscape() {
  try {
    screen.orientation.unlock?.();
    if (document.fullscreenElement) void document.exitFullscreen();
  } catch {
    // Nothing to undo.
  }
}

export function GameView({ settings, onExit, onReplay }: Props) {
  const [g, dispatch] = useReducer(reduce, settings, (s) => newGame(s, buildDeck(s.categories, s.shabab)));
  useWakeLock(g.phase !== 'final');

  useEffect(() => {
    if (g.phase !== 'countdown' && g.phase !== 'play') leaveLandscape();
  }, [g.phase]);
  useEffect(() => leaveLandscape, []);

  const exit = () => {
    if (g.phase === 'final' || window.confirm('بدك تطلع من اللعبة؟ النتيجة رح تروح.')) onExit();
  };

  const body = (() => {
    switch (g.phase) {
      case 'intro':
        return <TurnIntro g={g} dispatch={dispatch} />;
      case 'countdown':
        return <Countdown g={g} dispatch={dispatch} />;
      case 'play':
        return g.settings.mode === 'classic' ? <PlayClassic g={g} dispatch={dispatch} /> : <PlayHeadsUp g={g} dispatch={dispatch} />;
      case 'summary':
        return <Summary g={g} dispatch={dispatch} />;
      case 'scores':
        return <Scores g={g} dispatch={dispatch} />;
      case 'final':
        return <Final g={g} onHome={onExit} onReplay={onReplay} />;
    }
  })();

  return (
    <div className={`game game--${g.phase} game--${g.settings.mode}`}>
      {g.phase !== 'final' && (
        <button className="icon-btn exit" onClick={exit} aria-label="اطلع من اللعبة">
          ✕
        </button>
      )}
      {body}
    </div>
  );
}

const team = (g: Game, i = g.team) => g.settings.teams[i];

function RoundDots({ g }: { g: Game }) {
  return (
    <div className="round-dots" aria-label={`الجولة ${g.round} من ${g.settings.rounds}`}>
      {Array.from({ length: g.settings.rounds }, (_, i) => (
        <svg key={i} viewBox="0 0 1 1" className={i < g.round - 1 ? 'done' : i === g.round - 1 ? 'now' : ''}>
          <path d="M.17 .17L.83 .83M.83 .17L.17 .83" />
        </svg>
      ))}
    </div>
  );
}

const TUTORIAL_KEY = 'wk.tiltTutorial';

function TurnIntro({ g, dispatch }: { g: Game; dispatch: Dispatch }) {
  const headsUp = g.settings.mode === 'headsup';
  const [denied, setDenied] = useState(false);
  const [tutorial, setTutorial] = useState(() => headsUp && loadList(TUTORIAL_KEY).length === 0);
  const t = team(g);

  const closeTutorial = () => {
    save(TUTORIAL_KEY, ['seen']);
    setTutorial(false);
  };

  const ready = async () => {
    feedback.unlock();
    if (headsUp) {
      if (!(await requestTiltPermission())) setDenied(true);
      await enterLandscape();
    }
    dispatch({ type: 'countdown' });
  };

  return (
    <Screen className="center-screen intro">
      <RoundDots g={g} />
      <p className="muted">
        الجولة {g.round} من {g.settings.rounds}
      </p>
      <div className={`intro__team team-${g.team}`}>
        <TeamAvatar avatar={t.avatar} team={g.team} size={124} />
        <span className="intro__turn">دور</span>
        <h1 className="team-title">{t.name}</h1>
      </div>
      <div className="panel seam instructions">
        {headsUp ? (
          <>
            <p>📱 واحد منكم يمسك الجوال <b>بالعرض</b> على جبينه والشاشة لبرّا.</p>
            <p>⬇️ نزّله إذا عرفها · ⬆️ ارفعه ليتخطّى</p>
            <button className="link-btn" onClick={() => setTutorial(true)}>
              شوف شرح الحركة
            </button>
          </>
        ) : (
          <>
            <p>🎭 أعطوا الجوال للممثّل. باقي الفريق لا يطّلع عالشاشة!</p>
            <p>👉 اسحب يمين إذا عرفوها · 👈 يسار للتخطّي</p>
          </>
        )}
        {denied && <p className="warn">ما قدرنا نوصل لحساس الحركة — استعمل الأزرار عالشاشة.</p>}
      </div>
      <button className="btn btn--primary btn--xl" onClick={ready}>
        جاهزين · {g.settings.seconds} ثانية
      </button>
      {tutorial && <TiltTutorial onDone={closeTutorial} />}
    </Screen>
  );
}

function Countdown({ g, dispatch }: { g: Game; dispatch: Dispatch }) {
  const [n, setN] = useState(3);
  const landscape = useLandscape();
  const waiting = g.settings.mode === 'headsup' && !landscape;

  useEffect(() => {
    if (waiting) return;
    if (n === 0) {
      feedback.go();
      dispatch({ type: 'play' });
      return;
    }
    feedback.tick();
    const id = setTimeout(() => setN(n - 1), 900);
    return () => clearTimeout(id);
  }, [n, dispatch, waiting]);

  if (waiting) return <RotatePrompt />;

  return (
    <Screen className="center-screen countdown">
      {g.settings.mode === 'headsup' && <p className="countdown__hint">حط الجوال على جبينك 📱</p>}
      <div className="countdown__ring" key={n}>
        <span>{n || 'يلا!'}</span>
      </div>
    </Screen>
  );
}

function useTurnTimer(g: Game, dispatch: Dispatch) {
  return useCountdown(
    g.settings.seconds,
    true,
    () => {
      feedback.end();
      dispatch({ type: 'timeUp' });
    },
    (left) => left > 0 && left <= 5 && feedback.tick(),
  );
}

function TimerThread({ left, total }: { left: number; total: number }) {
  return (
    <div className={`timer ${left <= 10 ? 'timer--low' : ''}`} role="timer" aria-label={`${left} ثانية`}>
      <div className="timer__track">
        <div className="timer__fill" style={{ width: `${(left / total) * 100}%` }} />
      </div>
      <span className="timer__num">{left}</span>
    </div>
  );
}

const turnScore = (g: Game) => g.turn.filter((r) => r.correct).length;

function PlayClassic({ g, dispatch }: { g: Game; dispatch: Dispatch }) {
  const left = useTurnTimer(g, dispatch);
  const card = currentCard(g);
  const t = team(g);
  const answer = (correct: boolean) => {
    if (correct) feedback.correct();
    else feedback.skip();
    dispatch({ type: 'answer', correct });
  };

  return (
    <Screen className="play">
      <div className="play__top">
        <span className={`team-pill team-${g.team}`}>
          <TeamAvatar avatar={t.avatar} team={g.team} size={30} />
          {t.name}
        </span>
        <span className="score-pill">✓ {turnScore(g)}</span>
      </div>
      <TimerThread left={left} total={g.settings.seconds} />
      <div className="play__deck">{card && <PromptCard key={card.id} card={card} onSwipe={answer} />}</div>
      <p className="swipe-hint muted center">👈 تخطّي · اسحب البطاقة · عرفوها 👉</p>
      <div className="play__actions">
        <button className="btn btn--skip" onClick={() => answer(false)}>
          تخطّي
        </button>
        <button className="btn btn--correct" onClick={() => answer(true)}>
          عرفوها ✓
        </button>
      </div>
    </Screen>
  );
}

function PlayHeadsUp({ g, dispatch }: { g: Game; dispatch: Dispatch }) {
  const left = useTurnTimer(g, dispatch);
  const landscape = useLandscape();
  const [flash, setFlash] = useState<'correct' | 'skip' | null>(null);
  const flashTimer = useRef<ReturnType<typeof setTimeout>>(undefined);
  const card = currentCard(g);

  const answer = (correct: boolean) => {
    if (flash) return;
    if (correct) feedback.correct();
    else feedback.skip();
    dispatch({ type: 'answer', correct });
    setFlash(correct ? 'correct' : 'skip');
    flashTimer.current = setTimeout(() => setFlash(null), 750);
  };
  useEffect(() => () => clearTimeout(flashTimer.current), []);

  const tilt = useTilt(true, (dir) => answer(dir === 'down'));

  return (
    <div className="hu">
      <TatreezBand cell={5} />
      <div className="hu__bar">
        <span className={`hu__timer ${left <= 10 ? 'is-low' : ''}`}>{left}</span>
        {card && (
          <span className="hu__cat">
            <CategoryIcon id={card.category} size={34} />
            {categoryById(card.category).ar}
          </span>
        )}
        <span className="score-pill">✓ {turnScore(g)}</span>
      </div>
      {card && (
        <div className="hu__card" key={card.id}>
          <h2 className={`hu__ar ${sizeClass(card.ar)}`}>{card.ar}</h2>
          <p className="hu__en" dir="ltr">
            {card.arabizi}
          </p>
        </div>
      )}
      <div className={`hu__buttons ${tilt ? 'hu__buttons--quiet' : ''}`}>
        <button className="btn btn--skip" onClick={() => answer(false)}>
          ⬆️ تخطّي
        </button>
        <button className="btn btn--correct" onClick={() => answer(true)}>
          ⬇️ صح
        </button>
      </div>
      <TatreezBand cell={5} className="band--flip" />
      {flash && <div className={`hu__flash hu__flash--${flash}`}>{flash === 'correct' ? 'صح! ✓' : 'تخطّي'}</div>}
      {!landscape && <RotatePrompt />}
    </div>
  );
}

function Summary({ g, dispatch }: { g: Game; dispatch: Dispatch }) {
  const confirm = () => {
    markSeen(g.turn.map((r) => r.card.id));
    dispatch({ type: 'confirmTurn' });
  };
  const outOfCards = g.deckPos >= g.deck.length;
  const t = team(g);
  const points = turnScore(g);

  return (
    <Screen className="summary">
      <div className="summary__head">
        <h1>{outOfCards ? 'خلصت البطاقات! 🃏' : 'خلص الوقت! ⏰'}</h1>
        <div className={`summary__score team-${g.team}`}>
          <TeamAvatar avatar={t.avatar} team={g.team} size={56} />
          <span>
            <b>{t.name}</b>
            <span className="summary__points">
              {points} <small>{points === 1 ? 'نقطة' : 'نقاط'}</small>
            </span>
          </span>
        </div>
        {g.turn.length > 0 && <p className="muted">اكبس على أي بطاقة لتصلّح النتيجة</p>}
      </div>
      <ul className="results">
        {g.turn.length === 0 && <li className="muted center">ولا بطاقة هالدور 😅</li>}
        {g.turn.map((r, i) => (
          <li key={r.card.id}>
            <button className={`result ${r.correct ? 'result--ok' : 'result--skip'}`} onClick={() => dispatch({ type: 'toggle', index: i })}>
              <span className="result__mark">{r.correct ? '✓' : '✕'}</span>
              <span className="result__text">
                {r.card.ar}
                <small dir="ltr">{r.card.arabizi}</small>
              </span>
              <CategoryIcon id={r.card.category} size={34} />
            </button>
          </li>
        ))}
      </ul>
      <div className="sticky-cta">
        <button className="btn btn--primary btn--xl" onClick={confirm}>
          تمام
        </button>
      </div>
    </Screen>
  );
}

function Standings({ g }: { g: Game }) {
  const max = Math.max(1, ...g.scores);
  const order = g.scores.map((s, i) => ({ s, i })).sort((a, b) => b.s - a.s);
  return (
    <ol className="standings">
      {order.map(({ s, i }, rank) => (
        <li key={i} className={`team-${i} ${rank === 0 && s > 0 ? 'lead' : ''}`}>
          <TeamAvatar avatar={team(g, i).avatar} team={i} size={44} />
          <span className="standings__main">
            <span className="standings__name">{team(g, i).name}</span>
            <span className="standings__bar">
              <i style={{ width: `${(s / max) * 100}%` }} />
            </span>
          </span>
          <b>{s}</b>
        </li>
      ))}
    </ol>
  );
}

function Scores({ g, dispatch }: { g: Game; dispatch: Dispatch }) {
  const lastTeam = g.team === g.settings.teams.length - 1;
  const next = lastTeam ? 0 : g.team + 1;
  const t = team(g, next);
  return (
    <Screen className="center-screen scores">
      <h1>النتيجة</h1>
      <RoundDots g={g} />
      <p className="muted">{lastTeam ? `خلصت الجولة ${g.round} من ${g.settings.rounds}` : `الجولة ${g.round} من ${g.settings.rounds}`}</p>
      <Standings g={g} />
      <TatreezBand cell={4} />
      <button className="btn btn--primary btn--xl btn--team" onClick={() => dispatch({ type: 'nextTurn' })}>
        <TeamAvatar avatar={t.avatar} team={next} size={36} />
        دور {t.name}
      </button>
    </Screen>
  );
}

function Final({ g, onHome, onReplay }: { g: Game; onHome: () => void; onReplay: () => void }) {
  const top = winners(g.scores);
  const tie = top.length > 1;
  const endedEarly = !isLastTurn(g);
  const champ = team(g, top[0]);

  useEffect(() => {
    feedback.celebrate();
  }, []);

  return (
    <Screen className="center-screen final">
      <Confetti />
      {tie ? (
        <div className="final__tie">
          {top.map((i) => (
            <TeamAvatar key={i} avatar={team(g, i).avatar} team={i} size={96} />
          ))}
        </div>
      ) : (
        <div className={`final__champ team-${top[0]}`}>
          <span className="final__crown">👑</span>
          <TeamAvatar avatar={champ.avatar} team={top[0]} size={140} />
        </div>
      )}
      <h1 className="final__title">{tie ? 'تعادل!' : `مبروك يا ${champ.name}!`}</h1>
      <p className="muted">{endedEarly ? 'خلصت البطاقات — لعبتوها كلها! 🔥' : tie ? 'ما حدا أحسن من حدا 😄' : 'نشامى والله! 🇯🇴'}</p>
      <Standings g={g} />
      <div className="stack">
        <button className="btn btn--primary btn--xl" onClick={onReplay}>
          العبوا كمان مرة
        </button>
        <button className="btn btn--ghost" onClick={onHome}>
          الرئيسية
        </button>
      </div>
    </Screen>
  );
}
