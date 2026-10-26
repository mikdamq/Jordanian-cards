import { useEffect, useId, useMemo, useRef, useState, type CSSProperties, type ReactNode } from 'react';
import { avatarById, CATEGORY_ART, TATREEZ_BAND, type AvatarId, type StitchArt, type Thread } from './art';
import { categoryById, type Card } from './data/cards';
import { useFitText, useInstallMode, type ThemePref } from './hooks';
import { askedToInstall, inviteSnoozed, promptInstall, snoozeInvite, type InstallMode } from './lib/install';
import { track } from './lib/analytics';
import { consentNeeded, consentPlural, consentToolsAr, getConsent, setConsent } from './lib/consent';

const THREADS: Thread[] = ['r', 'g', 'y', 'k', 'b'];

/** Path data for every X stitch of one thread colour. */
function stitchPath(art: StitchArt, thread: Thread, dx = 0, dy = 0): string {
  let d = '';
  art.forEach((row, y) =>
    [...row].forEach((c, x) => {
      if (c !== thread) return;
      const a = x + dx, b = y + dy;
      d += `M${a + 0.17} ${b + 0.17}L${a + 0.83} ${b + 0.83}M${a + 0.83} ${b + 0.17}L${a + 0.17} ${b + 0.83}`;
    }),
  );
  return d;
}

function StitchPaths({ art }: { art: StitchArt }) {
  return (
    <>
      {THREADS.map((t) => {
        const d = stitchPath(art, t);
        return d ? <path key={t} d={d} className={`th th-${t}`} /> : null;
      })}
    </>
  );
}

/** Cross-stitch artwork, centred in a square. */
export function Stitch({ art, size = 40, className }: { art: StitchArt; size?: number; className?: string }) {
  const w = Math.max(...art.map((r) => r.length));
  const h = art.length;
  const side = Math.max(w, h);
  return (
    <svg
      width={size}
      height={size}
      viewBox={`${-(side - w) / 2} ${-(side - h) / 2} ${side} ${side}`}
      className={`stitch ${className ?? ''}`}
      aria-hidden
    >
      <StitchPaths art={art} />
    </svg>
  );
}

/** Round embroidered fabric patch holding a stitch motif. */
export function Patch({ art, size = 56, ring, className = '' }: { art: StitchArt; size?: number; ring?: string; className?: string }) {
  return (
    <span className={`patch ${className}`} style={{ width: size, height: size, ...(ring ? { '--ring': ring } : {}) } as CSSProperties}>
      <Stitch art={art} size={size * 0.62} />
    </span>
  );
}

export function TeamAvatar({ avatar, team, size = 56 }: { avatar: AvatarId; team: number; size?: number }) {
  return <Patch art={avatarById(avatar).art} size={size} ring={`var(--team-${team})`} className="patch--team" />;
}

export function CategoryIcon({ id, size = 44 }: { id: keyof typeof CATEGORY_ART; size?: number }) {
  return <Patch art={CATEGORY_ART[id]} size={size} />;
}

/** Full-width embroidered border: a repeating chain of tatreez diamonds. */
export function TatreezBand({ cell = 4, className = '' }: { cell?: number; className?: string }) {
  const id = useId().replace(/:/g, '');
  const w = TATREEZ_BAND[0].length;
  const h = TATREEZ_BAND.length;
  return (
    <svg className={`band ${className}`} width="100%" height={h * cell} aria-hidden>
      <defs>
        <pattern id={id} width={w * cell} height={h * cell} patternUnits="userSpaceOnUse">
          <g transform={`scale(${cell})`}>
            <StitchPaths art={TATREEZ_BAND} />
          </g>
        </pattern>
      </defs>
      <rect width="100%" height="100%" fill={`url(#${id})`} />
    </svg>
  );
}

export function Logo() {
  // Brand lockup: the red patch and the stitched wordmarks. Each wordmark has a light and a dark
  // version; CSS shows the one that matches the current theme.
  return (
    <div className="logo">
      <img className="logo__symbol" src="brand/symbol-primary.svg" alt="" width={104} height={104} />
      <h1 className="logo__name">
        <img className="logo__ar logo--on-light" src="brand/wordmark-arabic-on-light.svg" alt="ولا كلمة" width={742} height={266} />
        <img className="logo__ar logo--on-dark" src="brand/wordmark-arabic-on-dark.svg" alt="ولا كلمة" width={742} height={266} />
      </h1>
      <img className="logo__en logo--on-light" src="brand/wordmark-english-on-light.svg" alt="Wala Kelmeh" width={1456} height={210} />
      <img className="logo__en logo--on-dark" src="brand/wordmark-english-on-dark.svg" alt="" width={1456} height={210} />
    </div>
  );
}

export function Screen({ children, className = '' }: { children: ReactNode; className?: string }) {
  return <main className={`screen ${className}`}>{children}</main>;
}

export function Difficulty({ level }: { level: number }) {
  return (
    <span className="dots" aria-label={`صعوبة ${level} من 3`}>
      {[1, 2, 3].map((n) => (
        <svg key={n} viewBox="0 0 1 1" className={n <= level ? 'on' : ''}>
          <path d="M.17 .17L.83 .83M.83 .17L.17 .83" />
        </svg>
      ))}
    </span>
  );
}

const SWIPE_DISTANCE = 70;

/** The prompt card. In classic mode it can be swiped: right = got it, left = skip. */
export function PromptCard({ card, onSwipe }: { card: Card; onSwipe?: (correct: boolean) => void }) {
  const cat = categoryById(card.category);
  const [dx, setDx] = useState(0);
  const [leaving, setLeaving] = useState<0 | 1 | -1>(0);
  const [dragging, setDragging] = useState(false);
  const drag = useRef<{ x: number; dx: number } | null>(null);
  const [box, text] = useFitText<HTMLDivElement, HTMLHeadingElement>(card.ar, 64, 22);

  const release = () => {
    const d = drag.current;
    if (!d) return;
    drag.current = null;
    setDragging(false);
    if (Math.abs(d.dx) < SWIPE_DISTANCE || !onSwipe) return setDx(0);
    const dir = d.dx > 0 ? 1 : -1;
    setLeaving(dir);
    setTimeout(() => onSwipe(dir > 0), 180);
  };

  const transform = leaving
    ? `translateX(${leaving * 130}%) rotate(${leaving * 18}deg)`
    : `translateX(${dx}px) rotate(${dx / 18}deg)`;
  const strength = Math.min(1, Math.abs(dx) / SWIPE_DISTANCE);

  return (
    <article
      className={`prompt ${onSwipe ? 'prompt--swipe' : ''} ${dragging ? 'is-dragging' : ''}`}
      style={{ transform }}
      onPointerDown={(e) => {
        if (!onSwipe || leaving) return;
        drag.current = { x: e.clientX, dx: 0 };
        setDragging(true);
        e.currentTarget.setPointerCapture(e.pointerId);
      }}
      onPointerMove={(e) => {
        const d = drag.current;
        if (!d) return;
        d.dx = e.clientX - d.x;
        setDx(d.dx);
      }}
      onPointerUp={release}
      onPointerCancel={release}
    >
      <TatreezBand cell={4} />
      <div className="prompt__meta">
        <span className="prompt__cat">
          <CategoryIcon id={card.category} size={34} />
          {cat.ar}
        </span>
        <Difficulty level={card.difficulty} />
      </div>
      <div className="prompt__box" ref={box}>
        <h2 className="prompt__ar" ref={text}>
          {card.ar}
        </h2>
      </div>
      <p className="prompt__en" dir="ltr">
        {card.arabizi}
      </p>
      <TatreezBand cell={4} className="band--flip" />
      {onSwipe && (
        <>
          <span className="stamp stamp--ok" style={{ opacity: dx > 0 ? strength : 0 }}>
            عرفوها ✓
          </span>
          <span className="stamp stamp--skip" style={{ opacity: dx < 0 ? strength : 0 }}>
            تخطّي
          </span>
        </>
      )}
    </article>
  );
}

/** Heads-up word, sized to fill whatever space the landscape screen has left. */
export function HeadsUpWord({ card }: { card: Card }) {
  const [box, text] = useFitText<HTMLDivElement, HTMLDivElement>(card.ar, 200, 18);
  return (
    <div className="hu__card" ref={box}>
      <div className="hu__fit" ref={text}>
        <h2 className="hu__ar">{card.ar}</h2>
        <p className="hu__en" dir="ltr">
          {card.arabizi}
        </p>
      </div>
    </div>
  );
}

export function roundsLabel(n: number): string {
  if (n === 1) return 'جولة وحدة';
  if (n === 2) return 'جولتين';
  return `${n} جولات`;
}

export function Slider({
  value,
  min,
  max,
  onChange,
  label,
}: {
  value: number;
  min: number;
  max: number;
  onChange: (v: number) => void;
  label: string;
}) {
  const pct = ((value - min) / (max - min)) * 100;
  const steps = Array.from({ length: max - min + 1 }, (_, i) => min + i);
  return (
    <div className="slider">
      <input
        type="range"
        min={min}
        max={max}
        step={1}
        value={value}
        aria-label={label}
        aria-valuetext={roundsLabel(value)}
        style={{ '--pct': `${pct}%` } as CSSProperties}
        onChange={(e) => onChange(Number(e.target.value))}
      />
      <div className="slider__ticks" aria-hidden>
        {steps.map((s) => (
          <button key={s} tabIndex={-1} className={s === value ? 'on' : s < value ? 'past' : ''} onClick={() => onChange(s)}>
            {s}
          </button>
        ))}
      </div>
    </div>
  );
}

const THEME_ICON: Record<ThemePref, string> = { auto: '◐', light: '☀', dark: '☾' };
const THEME_LABEL: Record<ThemePref, string> = { auto: 'تلقائي', light: 'فاتح', dark: 'غامق' };

export function ThemeToggle({ pref, onCycle }: { pref: ThemePref; onCycle: () => void }) {
  return (
    <button className="chip-btn" onClick={onCycle} aria-label={`المظهر: ${THEME_LABEL[pref]}`}>
      <span className="chip-btn__icon">{THEME_ICON[pref]}</span>
      {THEME_LABEL[pref]}
    </button>
  );
}

const CONFETTI_COLORS = ['var(--th-r)', 'var(--th-g)', 'var(--th-y)', 'var(--th-b)', '#F7F0E3'];

/** Falling cross-stitches in thread colours. */
export function Confetti({ count = 70 }: { count?: number }) {
  const pieces = useMemo(
    () =>
      Array.from({ length: count }, (_, i) => ({
        left: Math.random() * 100,
        delay: Math.random() * 1.2,
        duration: 2.4 + Math.random() * 2,
        size: 10 + Math.random() * 12,
        color: CONFETTI_COLORS[i % CONFETTI_COLORS.length],
        spin: Math.random() > 0.5 ? 1 : -1,
      })),
    [count],
  );
  return (
    <div className="confetti" aria-hidden>
      {pieces.map((p, i) => (
        <svg
          key={i}
          viewBox="0 0 1 1"
          style={
            {
              left: `${p.left}%`,
              width: p.size,
              height: p.size,
              animationDelay: `${p.delay}s`,
              animationDuration: `${p.duration}s`,
              '--spin': p.spin,
              stroke: p.color,
            } as CSSProperties
          }
        >
          <path d="M.15 .15L.85 .85M.85 .15L.15 .85" />
        </svg>
      ))}
    </div>
  );
}

/** Side view: head with the phone on the forehead, tilting down then up. */
export function TiltDemo() {
  return (
    <svg className="tilt-demo" viewBox="0 0 230 150" aria-hidden>
      <path
        className="tilt-demo__head"
        d="M42 142 C34 118 30 96 34 76 C38 44 58 24 84 24 C104 24 116 38 116 56 L116 70 L124 82 L116 86 L117 96 C117 104 112 110 104 112 L98 116 L98 142 Z"
      />
      <g className="tilt-demo__phone">
        <rect x="130" y="22" width="11" height="62" rx="4" />
      </g>
      <g className="tilt-demo__label tilt-demo__label--down">
        <text x="185" y="132">✓ صح</text>
      </g>
      <g className="tilt-demo__label tilt-demo__label--up">
        <text x="185" y="30">تخطّي</text>
      </g>
    </svg>
  );
}

export function TiltTutorial({ onDone }: { onDone: () => void }) {
  return (
    <div className="overlay" role="dialog" aria-modal="true" aria-labelledby="tilt-title">
      <div className="sheet">
        <h2 id="tilt-title">كيف تلعب عالجبين؟</h2>
        <TiltDemo />
        <ol className="steps">
          <li>
            <b>امسك الجوال بالعرض</b> بإيديك الثنتين، وحطه على جبينك والشاشة لبرّا.
          </li>
          <li>
            عرفتها؟ <b>نزّل الجوال لتحت</b> ⬇️
          </li>
          <li>
            بدك تتخطّى؟ <b>ارفعه لفوق</b> ⬆️
          </li>
          <li>رجّعه على جبينك قبل البطاقة الجاية.</li>
        </ol>
        <button className="btn btn--primary btn--xl" onClick={onDone}>
          فهمت، يلا!
        </button>
      </div>
    </div>
  );
}

export function RotatePrompt() {
  return (
    <div className="overlay overlay--rotate" role="alert">
      <div className="rotate-phone" aria-hidden>
        <span />
      </div>
      <p>اقلب الجوال بالعرض</p>
      <small>عشان الكلمة تبيّن كبيرة لفريقك</small>
    </div>
  );
}

const ShareIcon = () => (
  <svg className="install-ico" viewBox="0 0 24 24" aria-hidden>
    <path d="M12 3v12M7.5 7.5 12 3l4.5 4.5M6 11H5v10h14V11h-1" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" />
  </svg>
);
const AddIcon = () => (
  <svg className="install-ico" viewBox="0 0 24 24" aria-hidden>
    <rect x="4" y="4" width="16" height="16" rx="4" fill="none" stroke="currentColor" strokeWidth="2" />
    <path d="M12 8.5v7M8.5 12h7" stroke="currentColor" strokeWidth="2" strokeLinecap="round" />
  </svg>
);

/** Steps for browsers that can't open an install prompt, plus Android's when it needs a tap first. */
export function InstallSheet({ mode, onClose }: { mode: InstallMode; onClose: () => void }) {
  const [copied, setCopied] = useState(false);
  const closeRef = useRef<HTMLButtonElement>(null);
  useEffect(() => {
    closeRef.current?.focus();
    const esc = (e: KeyboardEvent) => e.key === 'Escape' && onClose();
    addEventListener('keydown', esc);
    return () => removeEventListener('keydown', esc);
  }, [onClose]);
  const copy = async () => {
    try {
      await navigator.clipboard.writeText(location.origin + location.pathname);
      setCopied(true);
    } catch {
      setCopied(false);
    }
  };
  return (
    <div
      className="overlay"
      role="dialog"
      aria-modal="true"
      aria-labelledby="install-title"
      onClick={(e) => e.target === e.currentTarget && onClose()}
    >
      <div className="sheet install-sheet">
        <img className="install-sheet__icon" src="icon-192.png" width={72} height={72} alt="" />
        <h2 id="install-title">{mode === 'inapp' ? 'افتحها بالمتصفح أوّل' : 'ثبّتها على جوالك'}</h2>
        {mode === 'ios' && (
          <ol className="steps install-steps">
            <li>
              اكبس زر المشاركة <ShareIcon /> <small>(تحت بسفاري، أو فوق بكروم)</small>
            </li>
            <li>
              انزل شوي واختار <b>«إضافة إلى الشاشة الرئيسية»</b> <AddIcon />
            </li>
            <li>
              اكبس <b>«إضافة»</b>… وصارت ولا كلمة عشاشتك، وبتشتغل بدون إنترنت!
            </li>
          </ol>
        )}
        {mode === 'manual' && (
          <ol className="steps install-steps">
            <li>
              افتح قائمة المتصفح <b>⋮</b>
            </li>
            <li>
              اختار <b>«تثبيت التطبيق»</b> أو <b>«إضافة للشاشة الرئيسية»</b>
            </li>
          </ol>
        )}
        {mode === 'inapp' && (
          <>
            <p className="muted center">انت فاتحها من جوّا تطبيق (انستغرام، تيك توك…)، وهون ما بنقدر نثبّتها.</p>
            <ol className="steps install-steps">
              <li>
                اكبس <b>⋯</b> فوق، واختار <b>«فتح في المتصفح»</b>
              </li>
              <li>
                من هناك اكبس <b>«ثبّتها على جوالك»</b>
              </li>
            </ol>
            <button className="btn btn--ghost" onClick={copy}>
              {copied ? 'انتسخ الرابط ✓' : 'انسخ الرابط'}
            </button>
          </>
        )}
        {mode === 'prompt' && <p className="muted center">بكبسة وحدة بتصير عشاشتك، وبتفتح بدون إنترنت.</p>}
        {mode === 'prompt' ? (
          <button ref={closeRef} className="btn btn--primary btn--xl" onClick={() => promptInstall().finally(onClose)}>
            ثبّتها
          </button>
        ) : (
          <button ref={closeRef} className="btn btn--primary btn--xl" onClick={onClose}>
            تمام
          </button>
        )}
      </div>
    </div>
  );
}

/** «ثبّتها على جوالك»: one tap on Android, the steps everywhere else, hidden once installed. */
export function InstallButton({
  className = 'btn btn--dashed',
  label = 'ثبّتها على جوالك 📲',
  autoOpen = false,
  from,
}: {
  className?: string;
  label?: string;
  autoOpen?: boolean;
  from: string;
}) {
  const mode = useInstallMode();
  const [open, setOpen] = useState(autoOpen && askedToInstall);
  if (!mode) return null;
  const click = async () => {
    track('install', { step: 'tap', from, mode });
    if (mode === 'prompt') await promptInstall();
    else setOpen(true);
  };
  return (
    <>
      <button className={className} onClick={click}>
        {label}
      </button>
      {open && <InstallSheet mode={mode} onClose={() => setOpen(false)} />}
    </>
  );
}

/** After a game, the moment people most want the game one tap away. */
export function InstallInvite() {
  const mode = useInstallMode();
  const [hidden, setHidden] = useState(inviteSnoozed);
  if (!mode || hidden) return null;
  return (
    <div className="install-invite">
      <button className="install-invite__close" aria-label="سكّر" onClick={() => (snoozeInvite(), setHidden(true))}>
        ×
      </button>
      <p>
        <b>انبسطتوا؟</b> ثبّتوها على جوالكم، وبتلاقوها بكبسة حتى بدون إنترنت.
      </p>
      <InstallButton className="btn btn--primary" label="ثبّتها على جوالك" from="final" />
    </div>
  );
}

/** Asks before Google Analytics and Clarity load. Shown on the home screen only, never mid-game. */
export function ConsentBanner({ forceOpen = false, onDone }: { forceOpen?: boolean; onDone?: () => void }) {
  const [open, setOpen] = useState(() => consentNeeded && (forceOpen || getConsent() === null));
  useEffect(() => {
    if (forceOpen && consentNeeded) setOpen(true);
  }, [forceOpen]);
  if (!open) return null;
  const answer = (granted: boolean) => {
    setConsent(granted);
    setOpen(false);
    onDone?.();
  };
  return (
    <div className="consent" role="region" aria-label="الإحصائيات">
      <p>
        بنستعمل {consentToolsAr} لنفهم كيف بتنلعب ولا كلمة ونحسّنها. {consentPlural ? 'بنشغّلهم' : 'بنشغّله'} بس إذا وافقت، وبتقدر
        تغيّر رأيك وقت ما بدك. <a href="privacy.html">الخصوصية</a>
      </p>
      <div className="consent__btns">
        <button className="btn btn--primary" onClick={() => answer(true)}>
          تمام
        </button>
        <button className="btn btn--ghost" onClick={() => answer(false)}>
          لا، شكراً
        </button>
      </div>
    </div>
  );
}
