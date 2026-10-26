import { track } from './analytics';
import { load, save } from './storage';

/**
 * "Add to home screen". Android browsers hand us an install prompt we can open with
 * one tap; iPhone has no such API, so there we show the Share → Add to Home Screen
 * steps; in-app browsers (Instagram, TikTok…) can't install at all.
 */
type PromptEvent = Event & {
  prompt: () => Promise<void>;
  userChoice: Promise<{ outcome: 'accepted' | 'dismissed' }>;
};

export type InstallMode = 'prompt' | 'ios' | 'inapp' | 'manual';

const KEY = 'wk.install';
const SNOOZE_DAYS = 14;

let deferred: PromptEvent | null = null;
const listeners = new Set<() => void>();
const notify = () => listeners.forEach((l) => l());

/** The website's install button opens the game with ?install=1. */
export const askedToInstall = new URLSearchParams(location.search).has('install');

export function initInstall() {
  window.addEventListener('beforeinstallprompt', (e) => {
    e.preventDefault();
    deferred = e as PromptEvent;
    notify();
  });
  window.addEventListener('appinstalled', () => {
    deferred = null;
    save(KEY, { ...load(KEY, {}), installed: true });
    track('install', { step: 'installed' });
    notify();
  });
  if (askedToInstall) history.replaceState(null, '', location.pathname + location.hash);
}

export function subscribe(listener: () => void) {
  listeners.add(listener);
  return () => {
    listeners.delete(listener);
  };
}

const ua = navigator.userAgent;
const standalone = () =>
  matchMedia('(display-mode: standalone)').matches || (navigator as Navigator & { standalone?: boolean }).standalone === true;
const ios = () => /iPhone|iPad|iPod/.test(ua) || (navigator.platform === 'MacIntel' && navigator.maxTouchPoints > 1);
const inApp = () => /Instagram|FBAN|FBAV|FB_IAB|TikTok|musical_ly|BytedanceWebview|Snapchat|Line\//i.test(ua);
const phone = () => matchMedia('(pointer: coarse)').matches;

/** How this browser can install the game, or null when it's installed or can't. */
export function installMode(): InstallMode | null {
  if (standalone() || load(KEY, { installed: false }).installed) return null;
  if (inApp()) return 'inapp';
  if (deferred) return 'prompt';
  if (ios()) return 'ios';
  return phone() ? 'manual' : null;
}

/** Opens Android's own install dialog. True when the player accepted. */
export async function promptInstall(): Promise<boolean> {
  const e = deferred;
  if (!e) return false;
  deferred = null;
  await e.prompt();
  const { outcome } = await e.userChoice;
  track('install', { step: `prompt-${outcome}` });
  notify();
  return outcome === 'accepted';
}

/** The after-game invite stays away for two weeks once closed. */
export const inviteSnoozed = () => Date.now() < load(KEY, { snoozedUntil: 0 }).snoozedUntil;
export const snoozeInvite = () => save(KEY, { ...load(KEY, {}), snoozedUntil: Date.now() + SNOOZE_DAYS * 864e5 });
