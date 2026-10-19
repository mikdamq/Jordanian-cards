import { useEffect, useState } from 'react';
import { DEFAULT_SETTINGS, normalizeSettings, type Settings } from './game';
import { useTheme } from './hooks';
import { load, save } from './lib/storage';
import { GameView } from './screens/Game';
import { Home } from './screens/Home';
import { HowTo } from './screens/HowTo';
import { Setup } from './screens/Setup';

type View = 'home' | 'howto' | 'setup' | 'game';

const SETTINGS_KEY = 'wk.settings';

export default function App() {
  const [view, setView] = useState<View>('home');
  const [settings, setSettings] = useState<Settings>(() => normalizeSettings(load(SETTINGS_KEY, DEFAULT_SETTINGS)));
  const [theme, cycleTheme] = useTheme();
  // Bumped to remount the game for "play again" with a fresh deck.
  const [gameId, setGameId] = useState(0);

  useEffect(() => {
    save(SETTINGS_KEY, settings);
  }, [settings]);
  // Braces matter: newer Chrome returns a Promise from scrollTo, and React
  // would try to call any returned value as the effect's cleanup.
  useEffect(() => {
    window.scrollTo(0, 0);
  }, [view]);

  switch (view) {
    case 'home':
      return <Home onPlay={() => setView('setup')} onHowTo={() => setView('howto')} theme={theme} onTheme={cycleTheme} />;
    case 'howto':
      return <HowTo onBack={() => setView('home')} />;
    case 'setup':
      return (
        <Setup
          settings={settings}
          onChange={setSettings}
          onBack={() => setView('home')}
          onStart={() => {
            setSettings({ ...settings, teams: settings.teams.map((t) => ({ ...t, name: t.name.trim() })) });
            setGameId((n) => n + 1);
            setView('game');
          }}
        />
      );
    case 'game':
      return <GameView key={gameId} settings={settings} onExit={() => setView('home')} onReplay={() => setGameId((n) => n + 1)} />;
  }
}
