import type { ReactNode } from 'react';
import { categoryById, type Card } from './data/cards';

function starPoints(points: number, outer: number, inner: number, c = 50): string {
  return Array.from({ length: points * 2 }, (_, i) => {
    const r = i % 2 ? inner : outer;
    const a = (Math.PI * i) / points - Math.PI / 2;
    return `${(c + r * Math.cos(a)).toFixed(2)},${(c + r * Math.sin(a)).toFixed(2)}`;
  }).join(' ');
}

/** The seven-pointed star from the Jordanian flag. */
export function Star({ size = 40, className }: { size?: number; className?: string }) {
  return (
    <svg width={size} height={size} viewBox="0 0 100 100" className={className} aria-hidden>
      <polygon points={starPoints(7, 48, 22)} fill="currentColor" />
    </svg>
  );
}

export function Logo({ small }: { small?: boolean }) {
  return (
    <div className={`logo ${small ? 'logo--small' : ''}`}>
      <div className="logo__badge">
        <Star size={small ? 22 : 34} />
      </div>
      <div>
        <div className="logo__ar">ولا كلمة</div>
        {!small && <div className="logo__en">Wala Kilmeh</div>}
      </div>
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
        <i key={n} className={n <= level ? 'on' : ''} />
      ))}
    </span>
  );
}

/** Long prompts get a smaller size so they still fit on one screen. */
export function sizeClass(text: string): string {
  if (text.length > 22) return 'len-xl';
  if (text.length > 14) return 'len-l';
  if (text.length > 8) return 'len-m';
  return 'len-s';
}

export function PromptCard({ card }: { card: Card }) {
  const cat = categoryById(card.category);
  return (
    <article className="prompt" key={card.id}>
      <div className="shemagh" />
      <div className="prompt__meta">
        <span className="chip">
          {cat.emoji} {cat.ar}
        </span>
        <Difficulty level={card.difficulty} />
      </div>
      <h2 className={`prompt__ar ${sizeClass(card.ar)}`}>{card.ar}</h2>
      <p className="prompt__en" dir="ltr">
        {card.arabizi}
      </p>
    </article>
  );
}
