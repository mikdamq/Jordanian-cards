import { GOATCOUNTER_CODE } from '../config';
import { loadOptional } from './consent';

/**
 * Usage counts. GoatCounter (anonymous, no cookies) always runs; Google Analytics and
 * Microsoft Clarity get the same events once the player has agreed (see consent.ts).
 * Events have a name and a few values, e.g. track('game_start', { mode: 'classic' }),
 * which GoatCounter shows as the path "game-start/classic".
 */
type GoatCounter = { count: (opts: { path: string; title?: string; event?: boolean }) => void };

declare global {
  interface Window {
    goatcounter?: GoatCounter & { no_onload?: boolean; allow_local?: boolean };
  }
}

let started = false;

export function startAnalytics() {
  if (started) return;
  started = true;
  loadOptional();
  if (!GOATCOUNTER_CODE) return;
  const s = document.createElement('script');
  s.async = true;
  s.src = 'https://gc.zgo.at/count.js';
  s.dataset.goatcounter = `https://${GOATCOUNTER_CODE}.goatcounter.com/count`;
  document.head.appendChild(s);
}

export function track(name: string, params: Record<string, string | number> = {}) {
  const path = [name, ...Object.values(params)].join('/').replace(/_/g, '-');
  // Each tool may be blocked (ad blockers, offline); the game never waits on them.
  try {
    if (GOATCOUNTER_CODE) window.goatcounter?.count({ path, title: path, event: true });
  } catch {
    /* ignore */
  }
  try {
    window.gtag?.('event', name, params);
  } catch {
    /* ignore */
  }
  try {
    window.clarity?.('event', name);
  } catch {
    /* ignore */
  }
}
