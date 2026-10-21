import { AVATARS, type AvatarId } from './art';
import { CATEGORIES, type Card, type CategoryId } from './data/cards';

export type Mode = 'classic' | 'headsup' | 'fastest';

export interface Team {
  name: string;
  avatar: AvatarId;
}

export interface Settings {
  mode: Mode;
  teams: Team[];
  /** Individual players for "مين أسرع؟", where there are no teams. */
  players: Team[];
  categories: CategoryId[];
  shabab: boolean;
  seconds: 30 | 60 | 90;
  rounds: number;
}

export const MIN_ROUNDS = 1;
export const MAX_ROUNDS = 10;
export const MAX_TEAMS = 4;
export const MIN_PLAYERS = 2;
export const MAX_PLAYERS = 12;

export const DEFAULT_TEAMS: Team[] = [
  { name: 'النشامى', avatar: 'falcon' },
  { name: 'المها', avatar: 'oryx' },
  { name: 'الخيّالة', avatar: 'horse' },
  { name: 'الهجّانة', avatar: 'camel' },
];

export const playerName = (i: number) => `لاعب ${i + 1}`;
export const playerAvatar = (i: number): AvatarId => AVATARS[i % AVATARS.length].id;
export const defaultPlayer = (i: number): Team => ({ name: playerName(i), avatar: playerAvatar(i) });

export const DEFAULT_SETTINGS: Settings = {
  mode: 'classic',
  teams: DEFAULT_TEAMS.slice(0, 2),
  players: [0, 1, 2, 3].map(defaultPlayer),
  // The four easiest to act out; the rest are one tap away in setup.
  categories: ['screen', 'food', 'places', 'life'],
  shabab: false,
  seconds: 60,
  rounds: 3,
};

/**
 * Repairs settings saved by older versions or damaged in storage: anything
 * missing or malformed falls back to its default instead of crashing a screen.
 */
export function normalizeSettings(raw: Settings): Settings {
  const s = (raw && typeof raw === 'object' ? raw : {}) as Partial<Record<keyof Settings, unknown>>;
  const validAvatar = (a: unknown): a is AvatarId => AVATARS.some((x) => x.id === a);
  const validCategory = (c: unknown): c is CategoryId => CATEGORIES.some((x) => x.id === c);

  const parse = (list: unknown, max: number, fallback: (i: number) => Team): Team[] =>
    (Array.isArray(list) ? list : []).slice(0, max).map((t, i): Team => {
      if (typeof t === 'string') return { name: t, avatar: fallback(i).avatar };
      const obj = (t && typeof t === 'object' ? t : {}) as Partial<Record<keyof Team, unknown>>;
      return {
        name: typeof obj.name === 'string' ? obj.name : fallback(i).name,
        avatar: validAvatar(obj.avatar) ? obj.avatar : fallback(i).avatar,
      };
    });
  const teams = parse(s.teams, MAX_TEAMS, (i) => DEFAULT_TEAMS[i % 4]);
  while (teams.length < 2) teams.push(DEFAULT_TEAMS[teams.length]);
  const players = Array.isArray(s.players) ? parse(s.players, MAX_PLAYERS, defaultPlayer) : DEFAULT_SETTINGS.players;
  while (players.length < MIN_PLAYERS) players.push(defaultPlayer(players.length));

  const categories = Array.isArray(s.categories) ? s.categories.filter(validCategory) : DEFAULT_SETTINGS.categories;

  return {
    mode: s.mode === 'headsup' || s.mode === 'fastest' ? s.mode : 'classic',
    teams,
    players,
    categories,
    shabab: s.shabab === true,
    seconds: s.seconds === 30 || s.seconds === 90 ? s.seconds : 60,
    rounds: Math.min(MAX_ROUNDS, Math.max(MIN_ROUNDS, Math.round(Number(s.rounds)) || DEFAULT_SETTINGS.rounds)),
  };
}

export interface TurnResult {
  card: Card;
  correct: boolean;
  /** In "مين أسرع؟": the player who guessed it first. */
  guesser?: number;
}

/** Who takes turns and scores: teams, or individual players in "مين أسرع؟". */
export const sides = (s: Settings): Team[] => (s.mode === 'fastest' ? s.players : s.teams);

export type Phase = 'intro' | 'countdown' | 'play' | 'summary' | 'scores' | 'final';

export interface Game {
  settings: Settings;
  phase: Phase;
  deck: Card[];
  deckPos: number;
  /** Index into sides(): the team whose turn it is, or the acting player. */
  team: number;
  round: number;
  scores: number[];
  turn: TurnResult[];
}

export type Action =
  | { type: 'countdown' }
  | { type: 'play' }
  | { type: 'answer'; correct: boolean; guesser?: number }
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
    scores: sides(settings).map(() => 0),
    turn: [],
  };
}

export const currentCard = (g: Game): Card | undefined => g.deck[g.deckPos];

export const isLastTurn = (g: Game): boolean =>
  g.round === g.settings.rounds && g.team === sides(g.settings).length - 1;

export function reduce(g: Game, action: Action): Game {
  switch (action.type) {
    case 'countdown':
      return { ...g, phase: 'countdown', turn: [] };
    case 'play':
      return { ...g, phase: 'play' };
    case 'answer': {
      const card = currentCard(g);
      if (g.phase !== 'play' || !card) return g;
      const result: TurnResult = { card, correct: action.correct };
      if (action.correct && action.guesser != null) result.guesser = action.guesser;
      const next = { ...g, deckPos: g.deckPos + 1, turn: [...g.turn, result] };
      // Out of cards ends the turn early rather than showing an empty screen.
      return next.deckPos >= g.deck.length ? { ...next, phase: 'summary' } : next;
    }
    case 'timeUp':
      return g.phase === 'play' ? { ...g, phase: 'summary' } : g;
    case 'toggle':
      return {
        ...g,
        turn: g.turn.map((r, i) => {
          if (i !== action.index) return r;
          if (g.settings.mode !== 'fastest') return { ...r, correct: !r.correct };
          const guesser = nextGuesser(r.guesser, g.team, g.settings.players.length);
          return guesser == null ? { card: r.card, correct: false } : { ...r, correct: true, guesser };
        }),
      };
    case 'confirmTurn': {
      const scores = [...g.scores];
      for (const r of g.turn) {
        if (!r.correct) continue;
        // Teams score their own turn; in "مين أسرع؟" the first guesser takes the point.
        const who = g.settings.mode === 'fastest' ? r.guesser : g.team;
        if (who != null) scores[who] += 1;
      }
      return { ...g, scores, phase: isLastTurn(g) || g.deckPos >= g.deck.length ? 'final' : 'scores' };
    }
    case 'nextTurn': {
      const lastTeam = g.team === sides(g.settings).length - 1;
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

/** Fixing a result in "مين أسرع؟": skip → each player except the actor → skip. */
export function nextGuesser(current: number | undefined, actor: number, players: number): number | undefined {
  for (let i = current == null ? 0 : current + 1; i < players; i++) if (i !== actor) return i;
  return undefined;
}
