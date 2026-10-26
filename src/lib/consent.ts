import { CLARITY_ID, GA_ID } from '../config';

/**
 * Consent for the optional analytics (Google Analytics, Microsoft Clarity). Stored under one
 * key that the website shares with the game (same origin), so one answer covers both.
 * GoatCounter is cookie-free and anonymous, so it runs without asking.
 */
export type Consent = 'granted' | 'denied' | null;

const KEY = 'wk.consent';
export const consentNeeded = Boolean(GA_ID || CLARITY_ID);

type Gtag = (...args: unknown[]) => void;
type Clarity = ((...args: unknown[]) => void) & { q?: unknown[] };

declare global {
  interface Window {
    dataLayer?: unknown[];
    gtag?: Gtag;
    clarity?: Clarity;
  }
}

export function getConsent(): Consent {
  try {
    const v = JSON.parse(localStorage.getItem(KEY) || 'null');
    return v?.analytics === 'granted' || v?.analytics === 'denied' ? v.analytics : null;
  } catch {
    return null;
  }
}

export function setConsent(granted: boolean) {
  try {
    localStorage.setItem(KEY, JSON.stringify({ analytics: granted ? 'granted' : 'denied', at: Date.now() }));
  } catch {
    // Private mode: the banner will simply ask again next time.
  }
  if (granted) loadOptional();
  else revoke();
}

/** Forget the answer so the banner shows again. */
export function resetConsent() {
  try {
    localStorage.removeItem(KEY);
  } catch {
    // Nothing stored anyway.
  }
}

function inject(src: string) {
  const s = document.createElement('script');
  s.async = true;
  s.src = src;
  document.head.appendChild(s);
}

/** Loads Google Analytics and Clarity, once, and only with consent. */
export function loadOptional() {
  if (getConsent() !== 'granted') return;
  if (GA_ID && !window.gtag) {
    window.dataLayer = window.dataLayer || [];
    window.gtag = function gtag() {
      // gtag.js expects the arguments object itself, not an array copy.
      // eslint-disable-next-line prefer-rest-params
      window.dataLayer!.push(arguments);
    };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID);
    inject(`https://www.googletagmanager.com/gtag/js?id=${GA_ID}`);
  }
  if (CLARITY_ID && !window.clarity) {
    const clarity: Clarity = (...args: unknown[]) => {
      (clarity.q = clarity.q || []).push(args);
    };
    window.clarity = clarity;
    inject(`https://www.clarity.ms/tag/${CLARITY_ID}`);
    window.clarity('consent');
  }
}

/** Saying no later: stop Clarity, drop Google's cookies, and reload without either. */
function revoke() {
  if (!window.gtag && !window.clarity) return;
  try {
    window.clarity?.('consent', false);
  } catch {
    // Already gone.
  }
  for (const c of document.cookie.split(';')) {
    const name = c.split('=')[0].trim();
    if (/^(_ga|_gid|_gat|_clck|_clsk|CLID|ANONCHK|MR|MUID|SM)/.test(name)) {
      for (const domain of ['', `; domain=${location.hostname}`, `; domain=.${location.hostname.replace(/^www\./, '')}`]) {
        document.cookie = `${name}=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/${domain}`;
      }
    }
  }
  location.reload();
}
