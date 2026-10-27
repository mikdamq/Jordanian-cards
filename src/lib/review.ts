import { REVIEW_AFTER_GAMES, REVIEW_ASK_AGAIN, REVIEW_MIN_MINUTES } from '../config';
import { load, save } from './storage';

/**
 * When to ask "شو رأيك باللعبة؟". Counts finished games on this device; asks after the
 * second one, once more after a "مش هلّق", and never again once the player has answered.
 */
export interface ReviewState {
  games: number;
  askAt: number;
  snoozed: number;
  done: boolean;
}

const KEY = 'wk.review';
export const FRESH: ReviewState = { games: 0, askAt: REVIEW_AFTER_GAMES, snoozed: 0, done: false };

/** A finished game. Short test runs don't count. */
export const afterGame = (s: ReviewState, minutes: number): ReviewState =>
  minutes >= REVIEW_MIN_MINUTES ? { ...s, games: s.games + 1 } : s;

export const isDue = (s: ReviewState) => !s.done && s.games >= s.askAt;

/**
 * The card was shown. Unless the player sends an answer, that counts as a "مش هلّق":
 * ask once more later, and a second time without an answer is final.
 */
export const afterAsk = (s: ReviewState): ReviewState =>
  s.snoozed >= 1 ? { ...s, snoozed: s.snoozed + 1, done: true } : { ...s, snoozed: s.snoozed + 1, askAt: s.games + REVIEW_ASK_AGAIN };

/** Counts the game that just ended and says whether to show the card on this screen. */
export function countGameAndCheck(minutes: number): boolean {
  const s = afterGame(load(KEY, FRESH), minutes);
  const due = isDue(s);
  save(KEY, due ? afterAsk(s) : s);
  return due;
}

export const finishReview = () => save(KEY, { ...load(KEY, FRESH), done: true });
export const gamesPlayed = () => load(KEY, FRESH).games;
