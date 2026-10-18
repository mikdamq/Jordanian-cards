import { useEffect, useReducer, useRef, useState } from 'react';
import { PromptCard, Screen, sizeClass } from '../components';
import { currentCard, isLastTurn, newGame, reduce, winners, type Game, type Settings } from '../game';
import { useCountdown, useTilt, useWakeLock } from '../hooks';
import { buildDeck, markSeen } from '../lib/deck';
import { feedback } from '../lib/feedback';
import { requestTiltPermission } from '../lib/tilt';

type Dispatch = (a: Parameters<typeof reduce>[1]) => void;

interface Props {
  settings: Settings;
  onExit: () => void;
  onReplay: () => void;
}

export function GameView({ settings, onExit, onReplay }: Props) {
  const [g, dispatch] = useReducer(reduce, settings, (s) => newGame(s, buildDeck(s.categories, s.shabab)));
  useWakeLock(g.phase !== 'final');

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

const teamName = (g: Game, i = g.team) => g.settings.teams[i];

function TurnIntro({ g, dispatch }: { g: Game; dispatch: Dispatch }) {
  const [denied, setDenied] = useState(false);
  const headsUp = g.settings.mode === 'headsup';

  const ready = async () => {
    feedback.unlock();
    if (headsUp && !(await requestTiltPermission())) setDenied(true);
    dispatch({ type: 'countdown' });
  };

  return (
    <Screen className="center-screen">
      <p className="muted">
        الجولة {g.round} من {g.settings.rounds}
      </p>
      <h1 className={`team-title team-${g.team}`}>دور {teamName(g)}</h1>
      <div className="panel instructions">
        {headsUp ? (
          <>
            <p>📱 واحد منكم يحط الجوال على جبينه والشاشة لبرّا.</p>
            <p>⬇️ نزّله إذا عرفها · ⬆️ ارفعه ليتخطّى</p>
            <p className="muted">اقلب الجوال بالعرض للأحسن.</p>
          </>
        ) : (
          <>
            <p>🎭 أعطوا الجوال للممثّل. باقي الفريق لا يطّلع عالشاشة!</p>
            <p>🤐 تذكّر: ولا كلمة!</p>
          </>
        )}
        {denied && <p className="warn">ما قدرنا نوصل لحساس الحركة — استعمل الأزرار عالشاشة.</p>}
      </div>
      <button className="btn btn--primary btn--xl" onClick={ready}>
        جاهزين ({g.settings.seconds} ثانية)
      </button>
    </Screen>
  );
}

function Countdown({ g, dispatch }: { g: Game; dispatch: Dispatch }) {
  const [n, setN] = useState(3);

  useEffect(() => {
    if (n === 0) {
      feedback.go();
      dispatch({ type: 'play' });
      return;
    }
    feedback.tick();
    const id = setTimeout(() => setN(n - 1), 900);
    return () => clearTimeout(id);
  }, [n, dispatch]);

  return (
    <Screen className="center-screen">
      {g.settings.mode === 'headsup' && <p className="countdown__hint">حط الجوال على جبينك 📱</p>}
      <div className="countdown__num" key={n}>
        {n || 'يلا!'}
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

function TimerBar({ left, total }: { left: number; total: number }) {
  return (
    <div className={`timer ${left <= 10 ? 'timer--low' : ''}`}>
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
  const answer = (correct: boolean) => {
    if (correct) feedback.correct();
    else feedback.skip();
    dispatch({ type: 'answer', correct });
  };

  return (
    <Screen className="play">
      <div className="play__top">
        <span className={`team-pill team-${g.team}`}>{teamName(g)}</span>
        <span className="score-pill">✓ {turnScore(g)}</span>
      </div>
      <TimerBar left={left} total={g.settings.seconds} />
      {card && <PromptCard card={card} />}
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
      <div className="hu__timer">{left}</div>
      {card && (
        <div className="hu__card">
          <h2 className={`hu__ar ${sizeClass(card.ar)}`}>{card.ar}</h2>
          <p className="hu__en" dir="ltr">
            {card.arabizi}
          </p>
        </div>
      )}
      <div className={`hu__buttons ${tilt ? 'hu__buttons--quiet' : ''}`}>
        <button className="btn btn--skip" onClick={() => answer(false)}>
          تخطّي ⬆️
        </button>
        <button className="btn btn--correct" onClick={() => answer(true)}>
          صح ⬇️
        </button>
      </div>
      {flash && (
        <div className={`hu__flash hu__flash--${flash}`}>{flash === 'correct' ? 'صح! ✓' : 'تخطّي'}</div>
      )}
    </div>
  );
}

function Summary({ g, dispatch }: { g: Game; dispatch: Dispatch }) {
  const confirm = () => {
    markSeen(g.turn.map((r) => r.card.id));
    dispatch({ type: 'confirmTurn' });
  };
  const outOfCards = g.deckPos >= g.deck.length;

  return (
    <Screen>
      <div className="summary__head">
        <h1>{outOfCards ? 'خلصت البطاقات! 🃏' : 'خلص الوقت! ⏰'}</h1>
        <p className={`team-title team-${g.team}`}>
          {teamName(g)}: {turnScore(g)} نقاط
        </p>
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
            </button>
          </li>
        ))}
      </ul>
      <button className="btn btn--primary btn--xl" onClick={confirm}>
        تمام
      </button>
    </Screen>
  );
}

function Standings({ g }: { g: Game }) {
  const max = Math.max(1, ...g.scores);
  const order = g.scores.map((s, i) => ({ s, i })).sort((a, b) => b.s - a.s);
  return (
    <ol className="standings">
      {order.map(({ s, i }) => (
        <li key={i} className={`team-${i}`}>
          <span className="standings__name">{teamName(g, i)}</span>
          <span className="standings__bar">
            <i style={{ width: `${(s / max) * 100}%` }} />
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
  return (
    <Screen className="center-screen">
      <h1>النتيجة</h1>
      <p className="muted">{lastTeam ? `خلصت الجولة ${g.round}` : `الجولة ${g.round} من ${g.settings.rounds}`}</p>
      <Standings g={g} />
      <button className="btn btn--primary btn--xl" onClick={() => dispatch({ type: 'nextTurn' })}>
        دور {teamName(g, next)} ←
      </button>
    </Screen>
  );
}

function Final({ g, onHome, onReplay }: { g: Game; onHome: () => void; onReplay: () => void }) {
  const top = winners(g.scores);
  const tie = top.length > 1;
  const endedEarly = !isLastTurn(g);
  return (
    <Screen className="center-screen final">
      <div className="final__crown">{tie ? '🤝' : '🏆'}</div>
      <h1>{tie ? 'تعادل!' : `مبروك ${teamName(g, top[0])}!`}</h1>
      <p className="muted">{endedEarly ? 'خلصت البطاقات — لعبتوها كلها! 🔥' : tie ? 'ما حدا أحسن من حدا 😄' : 'نشامى والله!'}</p>
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
