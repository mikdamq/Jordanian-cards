import { GOATCOUNTER_CODE } from '../config';

/**
 * Anonymous, cookie-free usage counts via GoatCounter. No personal data:
 * only page views and named game events such as "game-start/headsup".
 */
type GoatCounter = { count: (opts: { path: string; title?: string; event?: boolean }) => void };

declare global {
  interface Window {
    goatcounter?: GoatCounter & { no_onload?: boolean; allow_local?: boolean };
  }
}

let started = false;

export function startAnalytics() {
  if (started || !GOATCOUNTER_CODE) return;
  started = true;
  const s = document.createElement('script');
  s.async = true;
  s.src = 'https://gc.zgo.at/count.js';
  s.dataset.goatcounter = `https://${GOATCOUNTER_CODE}.goatcounter.com/count`;
  document.head.appendChild(s);
}

export function track(event: string) {
  if (!GOATCOUNTER_CODE) return;
  try {
    window.goatcounter?.count({ path: event, title: event, event: true });
  } catch {
    // Blocked by an ad blocker or offline: the game doesn't care.
  }
}
