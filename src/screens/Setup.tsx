import { useState } from 'react';
import { AVATARS, MODE_ART, type AvatarId } from '../art';
import { CategoryIcon, Patch, roundsLabel, Screen, Slider, TeamAvatar } from '../components';
import { CARDS, CATEGORIES, SHABAB, type CategoryId } from '../data/cards';
import { DEFAULT_TEAMS, MAX_ROUNDS, MIN_ROUNDS, type Mode, type Settings } from '../game';
import { eligibleCards } from '../lib/deck';
import { feedback } from '../lib/feedback';

interface Props {
  settings: Settings;
  onChange: (s: Settings) => void;
  onStart: () => void;
  onBack: () => void;
}

const MODES: { id: Mode; title: string; desc: string }[] = [
  { id: 'classic', title: 'تمثيل', desc: 'مثّل البطاقة بدون حكي وفريقك يحزر' },
  { id: 'headsup', title: 'عالجبين', desc: 'الجوال على جبينك وفريقك يمثّل لك' },
];

const countIn = (id: CategoryId) => CARDS.filter((c) => c.category === id).length;

export function Setup({ settings, onChange, onStart, onBack }: Props) {
  const [picking, setPicking] = useState<number | null>(null);
  const set = (patch: Partial<Settings>) => onChange({ ...settings, ...patch });
  const count = eligibleCards(settings.categories, settings.shabab).length;
  const teamsValid = settings.teams.every((t) => t.name.trim());

  const toggleCategory = (id: CategoryId) => {
    feedback.select();
    set({
      categories: settings.categories.includes(id)
        ? settings.categories.filter((c) => c !== id)
        : [...settings.categories, id],
    });
  };

  const updateTeam = (i: number, patch: Partial<Settings['teams'][number]>) =>
    set({ teams: settings.teams.map((t, j) => (j === i ? { ...t, ...patch } : t)) });

  const addTeam = () => {
    const unusedName = DEFAULT_TEAMS.find((d) => !settings.teams.some((t) => t.name === d.name));
    const unusedAvatar = AVATARS.find((a) => !settings.teams.some((t) => t.avatar === a.id))!.id;
    set({ teams: [...settings.teams, { name: unusedName?.name ?? `فريق ${settings.teams.length + 1}`, avatar: unusedAvatar }] });
  };

  const pickAvatar = (i: number, avatar: AvatarId) => {
    feedback.select();
    updateTeam(i, { avatar });
    setPicking(null);
  };

  return (
    <Screen className="setup">
      <header className="bar">
        <button className="icon-btn" onClick={onBack} aria-label="رجوع">
          →
        </button>
        <h1>جهّز اللعبة</h1>
      </header>

      <section>
        <h3 className="label">طريقة اللعب</h3>
        <div className="modes">
          {MODES.map((m) => (
            <button
              key={m.id}
              className={`mode seam ${settings.mode === m.id ? 'on' : ''}`}
              onClick={() => set({ mode: m.id })}
              aria-pressed={settings.mode === m.id}
            >
              <Patch art={MODE_ART[m.id]} size={60} />
              <b>{m.title}</b>
              <small>{m.desc}</small>
            </button>
          ))}
        </div>
      </section>

      <section>
        <h3 className="label">الفرق</h3>
        <div className="stack stack--tight">
          {settings.teams.map((t, i) => (
            <div key={i} className="team-block">
              <div className={`team-row team-${i}`}>
                <button
                  className="team-row__avatar"
                  onClick={() => setPicking(picking === i ? null : i)}
                  aria-label={`غيّر شعار ${t.name}`}
                  aria-expanded={picking === i}
                >
                  <TeamAvatar avatar={t.avatar} team={i} size={46} />
                  <span className="team-row__edit">✎</span>
                </button>
                <input value={t.name} maxLength={20} onChange={(e) => updateTeam(i, { name: e.target.value })} aria-label={`اسم الفريق ${i + 1}`} />
                {settings.teams.length > 2 && (
                  <button
                    className="icon-btn icon-btn--bare"
                    onClick={() => {
                      setPicking(null);
                      set({ teams: settings.teams.filter((_, j) => j !== i) });
                    }}
                    aria-label={`احذف ${t.name}`}
                  >
                    ✕
                  </button>
                )}
              </div>
              {picking === i && (
                <div className="avatar-picker" role="radiogroup" aria-label="اختار شعار">
                  {AVATARS.map((a) => (
                    <button key={a.id} role="radio" aria-checked={t.avatar === a.id} className={t.avatar === a.id ? 'on' : ''} onClick={() => pickAvatar(i, a.id)}>
                      <Patch art={a.art} size={48} />
                      <small>{a.ar}</small>
                    </button>
                  ))}
                </div>
              )}
            </div>
          ))}
          {settings.teams.length < 4 && (
            <button className="btn btn--dashed" onClick={addTeam}>
              + زيد فريق
            </button>
          )}
        </div>
      </section>

      <section>
        <h3 className="label">الفئات</h3>
        <div className="cat-grid">
          {CATEGORIES.filter((c) => c.id !== SHABAB).map((c) => {
            const on = settings.categories.includes(c.id);
            return (
              <button key={c.id} className={`cat-tile ${on ? 'on' : ''}`} onClick={() => toggleCategory(c.id)} aria-pressed={on}>
                <CategoryIcon id={c.id} size={44} />
                <span className="cat-tile__text">
                  <b>{c.ar}</b>
                  <small>{countIn(c.id)} بطاقة</small>
                </span>
                <span className="cat-tile__check" aria-hidden>
                  ✓
                </span>
              </button>
            );
          })}
        </div>
        <label className={`switch-row seam ${settings.shabab ? 'on' : ''}`}>
          <CategoryIcon id={SHABAB} size={44} />
          <span className="switch-row__text">
            <b>باكيت الشباب</b>
            <small>حكي شباب ومواقف مهضومة · {countIn(SHABAB)} بطاقة</small>
          </span>
          <input
            type="checkbox"
            className="switch"
            checked={settings.shabab}
            onChange={(e) => {
              feedback.select();
              set({ shabab: e.target.checked });
            }}
          />
        </label>
      </section>

      <section>
        <h3 className="label">وقت الدور</h3>
        <div className="segmented" role="radiogroup">
          {([30, 60, 90] as const).map((o) => (
            <button key={o} role="radio" aria-checked={o === settings.seconds} className={o === settings.seconds ? 'on' : ''} onClick={() => set({ seconds: o })}>
              {o} ثانية
            </button>
          ))}
        </div>
      </section>

      <section>
        <div className="label-row">
          <h3 className="label">عدد الجولات</h3>
          <span className="label-value">{roundsLabel(settings.rounds)}</span>
        </div>
        <Slider
          value={settings.rounds}
          min={MIN_ROUNDS}
          max={MAX_ROUNDS}
          label="عدد الجولات"
          onChange={(rounds) => {
            if (rounds !== settings.rounds) feedback.select();
            set({ rounds });
          }}
        />
      </section>

      <div className="sticky-cta">
        <button className="btn btn--primary btn--xl" disabled={!count || !teamsValid} onClick={onStart}>
          {!count ? 'اختار فئة وحدة على الأقل' : !teamsValid ? 'سمّي كل الفرق' : 'يلا نبلّش!'}
        </button>
        <p className="muted center">
          {count} من {CARDS.length} بطاقة
        </p>
      </div>
    </Screen>
  );
}
