import { CARDS, SHABAB, type Card, type CategoryId } from '../data/cards';
import { loadList, save } from './storage';

const SEEN_KEY = 'wk.seen';

export function shuffle<T>(items: T[], random: () => number = Math.random): T[] {
  const out = [...items];
  for (let i = out.length - 1; i > 0; i--) {
    const j = Math.floor(random() * (i + 1));
    [out[i], out[j]] = [out[j], out[i]];
  }
  return out;
}

export function eligibleCards(categories: CategoryId[], shabab: boolean): Card[] {
  const wanted = new Set<CategoryId>(categories.filter((c) => c !== SHABAB));
  if (shabab) wanted.add(SHABAB);
  return CARDS.filter((c) => wanted.has(c.category));
}

/**
 * Shuffled deck that puts cards not seen in earlier games first, so repeat
 * game nights don't keep surfacing the same prompts.
 */
export function buildDeck(
  categories: CategoryId[],
  shabab: boolean,
  seen: Set<string> = new Set(loadList(SEEN_KEY)),
  random: () => number = Math.random,
): Card[] {
  const pool = eligibleCards(categories, shabab);
  const fresh = pool.filter((c) => !seen.has(c.id));
  const stale = pool.filter((c) => seen.has(c.id));
  return [...shuffle(fresh, random), ...shuffle(stale, random)];
}

export function markSeen(ids: string[]): void {
  const seen = new Set(loadList(SEEN_KEY));
  ids.forEach((id) => seen.add(id));
  // Once nearly everything has been played, start the rotation over.
  save(SEEN_KEY, seen.size >= CARDS.length - 20 ? ids : [...seen]);
}
