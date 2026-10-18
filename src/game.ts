import { AVATARS, type AvatarId } from './art';
import { CATEGORIES, SHABAB, type Card, type CategoryId } from './data/cards';

export type Mode = 'classic' | 'headsup';

export interface Team {
  name: string;
  avatar: AvatarId;
}

export interface Settings {
  mode: Mode;
  teams: Team[];
  categories: CategoryId[];
  shabab: boolean;
  seconds: 30 | 60 | 90;
  rounds: number;
}

export const MIN_ROUNDS = 1;
export const MAX_ROUNDS = 10;

export const DEFAULT_TEAMS: Team[] = [
  { name: 'النشامى', avatar: 'falcon' },
  { name: 'المها', avatar: 'oryx' },
  { name: 'الخيّالة', avatar: 'horse' },
  { name: 'الهجّانة', avatar: 'camel' },
];

export const DEFAULT_SETTINGS: Settings = {
  mode: 'classic',
  teams: DEFAULT_TEAMS.slice(0, 2),
  categories: CATEGORIES.map((c) => c.id).filter((id) => id !== SHABAB),
  shabab: false,
  seconds: 60,
  rounds: 3,
};

/** Repairs settings saved by older versions (plain team names, fixed round options). */
export function normalizeSettings(s: Settings): Settings {
  const teams = (s.teams as (Team | string)[]).map((t, i) =>
    typeof t === 'string' ? { name: t, avatar: DEFAULT_TEAMS[i % 4].avatar } : t,
  );
  const validAvatar = (a: AvatarId) => AVATARS.some((x) => x.id === a);
  return {
    ...s,
    teams: teams.map((t, i) => (validAvatar(t.avatar) ? t : { ...t, avatar: DEFAULT_TEAMS[i % 4].avatar })),
    rounds: Math.min(MAX_ROUNDS, Math.max(MIN_ROUNDS, Math.round(Number(s.rounds) || 3))),
  };
}

export interface TurnResult {
  card: Card;
  correct: boolean;
}

export type Phase = 'intro' | 'countdown' | 'play' | 'summary' | 'scores' | 'final';

export interface Game {
  settings: Settings;
  phase: Phase;
  deck: Card[];
  deckPos: number;
  team: number;
  round: number;
  scores: number[];
  turn: TurnResult[];
}

export type Action =
  | { type: 'countdown' }
  | { type: 'play' }
  | { type: 'answer'; correct: boolean }
  | { type: 'timeUp' }
  | { type: 'toggle'; index: number }
  | { type: 'confirmTurn' }
  | { type: 'nextTurn' };

export function newGame(settings: Settings, deck: Card[]): Game {
  return {
    settings,
    phase: 'intro',
    deck,
    deckPos: 0,
    team: 0,
    round: 1,
    scores: settings.teams.map(() => 0),
    turn: [],
  };
}

export const currentCard = (g: Game): Card | undefined => g.deck[g.deckPos];

export const isLastTurn = (g: Game): boolean =>
  g.round === g.settings.rounds && g.team === g.settings.teams.length - 1;

export function reduce(g: Game, action: Action): Game {
  switch (action.type) {
    case 'countdown':
      return { ...g, phase: 'countdown', turn: [] };
    case 'play':
      return { ...g, phase: 'play' };
    case 'answer': {
      const card = currentCard(g);
      if (g.phase !== 'play' || !card) return g;
      const next = { ...g, deckPos: g.deckPos + 1, turn: [...g.turn, { card, correct: action.correct }] };
      // Out of cards ends the turn early rather than showing an empty screen.
      return next.deckPos >= g.deck.length ? { ...next, phase: 'summary' } : next;
    }
    case 'timeUp':
      return g.phase === 'play' ? { ...g, phase: 'summary' } : g;
    case 'toggle':
      return {
        ...g,
        turn: g.turn.map((r, i) => (i === action.index ? { ...r, correct: !r.correct } : r)),
      };
    case 'confirmTurn': {
      const points = g.turn.filter((r) => r.correct).length;
      const scores = g.scores.map((s, i) => (i === g.team ? s + points : s));
      return { ...g, scores, phase: isLastTurn(g) || g.deckPos >= g.deck.length ? 'final' : 'scores' };
    }
    case 'nextTurn': {
      const lastTeam = g.team === g.settings.teams.length - 1;
      return {
        ...g,
        phase: 'intro',
        team: lastTeam ? 0 : g.team + 1,
        round: lastTeam ? g.round + 1 : g.round,
        turn: [],
      };
    }
  }
}

/** Indexes of the team(s) with the top score. */
export function winners(scores: number[]): number[] {
  const best = Math.max(...scores);
  return scores.flatMap((s, i) => (s === best ? [i] : []));
}
