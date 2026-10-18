import { Screen } from '../components';
import { CARDS, CATEGORIES, SHABAB, type CategoryId } from '../data/cards';
import { DEFAULT_TEAMS, type Mode, type Settings } from '../game';
import { eligibleCards } from '../lib/deck';

interface Props {
  settings: Settings;
  onChange: (s: Settings) => void;
  onStart: () => void;
  onBack: () => void;
}

const MODES: { id: Mode; title: string; emoji: string; desc: string }[] = [
  { id: 'classic', title: 'تمثيل', emoji: '🎭', desc: 'مثّل البطاقة بدون حكي وفريقك يحزر' },
  { id: 'headsup', title: 'عالجبين', emoji: '📱', desc: 'الجوال على جبينك وفريقك يمثّل لك' },
];

function Segmented<T extends number>({
  value,
  options,
  onChange,
  suffix,
}: {
  value: T;
  options: T[];
  onChange: (v: T) => void;
  suffix: string;
}) {
  return (
    <div className="segmented" role="radiogroup">
      {options.map((o) => (
        <button key={o} role="radio" aria-checked={o === value} className={o === value ? 'on' : ''} onClick={() => onChange(o)}>
          {o} {suffix}
        </button>
      ))}
    </div>
  );
}

export function Setup({ settings, onChange, onStart, onBack }: Props) {
  const set = (patch: Partial<Settings>) => onChange({ ...settings, ...patch });
  const count = eligibleCards(settings.categories, settings.shabab).length;
  const teamsValid = settings.teams.every((t) => t.trim());

  const toggleCategory = (id: CategoryId) =>
    set({
      categories: settings.categories.includes(id)
        ? settings.categories.filter((c) => c !== id)
        : [...settings.categories, id],
    });

  const renameTeam = (i: number, name: string) =>
    set({ teams: settings.teams.map((t, j) => (j === i ? name : t)) });

  const addTeam = () =>
    set({ teams: [...settings.teams, DEFAULT_TEAMS.find((d) => !settings.teams.includes(d)) ?? `فريق ${settings.teams.length + 1}`] });

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
            <button key={m.id} className={`mode ${settings.mode === m.id ? 'on' : ''}`} onClick={() => set({ mode: m.id })} aria-pressed={settings.mode === m.id}>
              <span className="mode__emoji">{m.emoji}</span>
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
            <div className="team-row" key={i}>
              <span className={`team-dot team-${i}`} />
              <input value={t} maxLength={20} onChange={(e) => renameTeam(i, e.target.value)} aria-label={`اسم الفريق ${i + 1}`} />
              {settings.teams.length > 2 && (
                <button className="icon-btn" onClick={() => set({ teams: settings.teams.filter((_, j) => j !== i) })} aria-label="احذف الفريق">
                  ✕
                </button>
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
        <div className="chips">
          {CATEGORIES.filter((c) => c.id !== SHABAB).map((c) => {
            const on = settings.categories.includes(c.id);
            return (
              <button key={c.id} className={`chip chip--toggle ${on ? 'on' : ''}`} onClick={() => toggleCategory(c.id)} aria-pressed={on}>
                {c.emoji} {c.ar}
              </button>
            );
          })}
        </div>
        <label className="switch-row">
          <span>
            <b>😎 باكيت الشباب</b>
            <small>حكي شباب ومواقف مهضومة من الحياة اليومية</small>
          </span>
          <input type="checkbox" className="switch" checked={settings.shabab} onChange={(e) => set({ shabab: e.target.checked })} />
        </label>
      </section>

      <section>
        <h3 className="label">وقت الدور</h3>
        <Segmented value={settings.seconds} options={[30, 60, 90]} suffix="ث" onChange={(seconds) => set({ seconds })} />
      </section>

      <section>
        <h3 className="label">عدد الجولات</h3>
        <Segmented value={settings.rounds} options={[3, 5, 7]} suffix="جولات" onChange={(rounds) => set({ rounds })} />
      </section>

      <div className="sticky-cta">
        <button className="btn btn--primary btn--xl" disabled={!count || !teamsValid} onClick={onStart}>
          {count ? 'يلا نبلّش!' : 'اختار فئة وحدة على الأقل'}
        </button>
        <p className="muted center">
          {count} من {CARDS.length} بطاقة
        </p>
      </div>
    </Screen>
  );
}
