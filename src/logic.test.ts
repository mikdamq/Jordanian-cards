import { describe, expect, it } from 'vitest';
import { CARDS, CATEGORIES } from './data/cards';
import { DEFAULT_SETTINGS, DEFAULT_TEAMS, defaultPlayer, newGame, nextGuesser, normalizeSettings, reduce, winners, type Game, type Settings } from './game';
import { buildDeck, eligibleCards } from './lib/deck';
import { nextTiltState, screenFacing } from './lib/tilt';

describe('cards', () => {
  it('has ~200 family cards plus a shabab pack, with unique ids and no duplicate prompts', () => {
    const family = CARDS.filter((c) => c.category !== 'shabab');
    expect(family.length).toBeGreaterThanOrEqual(190);
    expect(CARDS.filter((c) => c.category === 'shabab').length).toBeGreaterThanOrEqual(25);
    expect(new Set(CARDS.map((c) => c.id)).size).toBe(CARDS.length);
    expect(new Set(CARDS.map((c) => c.ar)).size).toBe(CARDS.length);
  });

  it('every category has cards and every card has both scripts', () => {
    for (const cat of CATEGORIES) expect(CARDS.some((c) => c.category === cat.id)).toBe(true);
    for (const c of CARDS) {
      expect(c.ar.trim()).not.toBe('');
      expect(c.arabizi.trim()).not.toBe('');
    }
  });
});

describe('deck', () => {
  it('only includes shabab cards when the toggle is on', () => {
    expect(eligibleCards(['food'], false).every((c) => c.category === 'food')).toBe(true);
    expect(eligibleCards(['food'], true).some((c) => c.category === 'shabab')).toBe(true);
  });

  it('puts unseen cards first', () => {
    const seen = new Set(eligibleCards(['food'], false).slice(0, 10).map((c) => c.id));
    const deck = buildDeck(['food'], false, seen);
    const firstStale = deck.findIndex((c) => seen.has(c.id));
    expect(firstStale).toBe(deck.length - seen.size);
  });
});

describe('tilt', () => {
  it('reads upright as neutral and tilts either way regardless of landscape side', () => {
    expect(screenFacing(0, 90)).toBeCloseTo(0);
    expect(screenFacing(0, -90)).toBeCloseTo(0);
    expect(screenFacing(0, 0)).toBeCloseTo(1); // face up
    expect(screenFacing(180, 0)).toBeCloseTo(-1); // face down
  });

  it('requires returning to upright before the next tilt', () => {
    let s = nextTiltState('neutral', -0.8);
    expect(s).toBe('down');
    s = nextTiltState(s, -0.4);
    expect(s).toBe('down');
    s = nextTiltState(s, 0.1);
    expect(s).toBe('neutral');
    expect(nextTiltState(s, 0.7)).toBe('up');
  });
});

describe('game flow', () => {
  const play = (g: Game, ...actions: Parameters<typeof reduce>[1][]) => actions.reduce(reduce, g);

  it('scores a turn, rotates teams, and ends after the last round', () => {
    const settings = { ...DEFAULT_SETTINGS, rounds: 3, teams: DEFAULT_TEAMS.slice(0, 2) };
    let g = newGame(settings, buildDeck(settings.categories, false, new Set()));
    g = play(g, { type: 'countdown' }, { type: 'play' }, { type: 'answer', correct: true }, { type: 'answer', correct: false }, { type: 'answer', correct: true }, { type: 'timeUp' });
    expect(g.phase).toBe('summary');
    g = play(g, { type: 'toggle', index: 1 }, { type: 'confirmTurn' });
    expect(g.scores).toEqual([3, 0]);
    expect(g.phase).toBe('scores');
    g = reduce(g, { type: 'nextTurn' });
    expect([g.team, g.round]).toEqual([1, 1]);

    for (let t = 0; t < 5; t++) {
      g = play(g, { type: 'countdown' }, { type: 'play' }, { type: 'timeUp' }, { type: 'confirmTurn' });
      if (g.phase === 'scores') g = reduce(g, { type: 'nextTurn' });
    }
    expect(g.phase).toBe('final');
    expect(winners(g.scores)).toEqual([0]);
  });

  it('ends the game when the deck runs out', () => {
    const settings = { ...DEFAULT_SETTINGS, teams: DEFAULT_TEAMS.slice(0, 2) };
    let g = newGame(settings, CARDS.slice(0, 2));
    g = play(g, { type: 'countdown' }, { type: 'play' }, { type: 'answer', correct: true }, { type: 'answer', correct: true });
    expect(g.phase).toBe('summary');
    expect(reduce(g, { type: 'confirmTurn' }).phase).toBe('final');
  });

  it('reports ties', () => {
    expect(winners([4, 4, 1])).toEqual([0, 1]);
  });
});

describe('settings', () => {
  it('upgrades settings saved by the first version', () => {
    const old = { ...DEFAULT_SETTINGS, teams: ['أ', 'ب'], rounds: 7 } as unknown as Settings;
    const s = normalizeSettings(old);
    expect(s.teams).toEqual([
      { name: 'أ', avatar: 'falcon' },
      { name: 'ب', avatar: 'oryx' },
    ]);
    expect(s.rounds).toBe(7);
    expect(normalizeSettings({ ...DEFAULT_SETTINGS, rounds: 40 }).rounds).toBe(10);
  });

  it('turns damaged settings into playable defaults instead of crashing', () => {
    const junk = [null, 'oops', 42, {}, { teams: [{ name: 5 }, null], categories: ['nope', 'food'], seconds: 45, mode: 'x' }];
    for (const j of junk) {
      const s = normalizeSettings(j as unknown as Settings);
      expect(s.teams.length).toBeGreaterThanOrEqual(2);
      expect(s.teams.every((t) => typeof t.name === 'string')).toBe(true);
      expect([30, 60, 90]).toContain(s.seconds);
      expect(['classic', 'headsup']).toContain(s.mode);
    }
    const repaired = normalizeSettings(junk[4] as unknown as Settings);
    expect(repaired.categories).toEqual(['food']);
    expect(repaired.teams[0]).toEqual({ name: 'النشامى', avatar: 'falcon' });
  });
});

describe('مين أسرع؟ (fastest) mode', () => {
  const play = (g: Game, ...actions: Parameters<typeof reduce>[1][]) => actions.reduce(reduce, g);
  const players = [0, 1, 2, 3].map(defaultPlayer);

  it('gives each point to the first guesser and rotates the actor through every player', () => {
    const settings = { ...DEFAULT_SETTINGS, mode: 'fastest' as const, players, rounds: 1 };
    let g = newGame(settings, CARDS.slice(0, 50));
    expect(g.scores).toEqual([0, 0, 0, 0]);
    // Player 0 acts; players 2, 2 and 3 guess, one card skipped
    g = play(g, { type: 'countdown' }, { type: 'play' },
      { type: 'answer', correct: true, guesser: 2 },
      { type: 'answer', correct: true, guesser: 2 },
      { type: 'answer', correct: false },
      { type: 'answer', correct: true, guesser: 3 },
      { type: 'timeUp' }, { type: 'confirmTurn' });
    expect(g.scores).toEqual([0, 0, 2, 1]);
    for (let actor = 1; actor < 4; actor++) {
      g = reduce(g, { type: 'nextTurn' });
      expect(g.team).toBe(actor);
      g = play(g, { type: 'countdown' }, { type: 'play' }, { type: 'answer', correct: true, guesser: 0 }, { type: 'timeUp' }, { type: 'confirmTurn' });
    }
    expect(g.phase).toBe('final');
    expect(g.scores).toEqual([3, 0, 2, 1]);
  });

  it('fixing a result cycles skip → each non-actor player → skip', () => {
    expect(nextGuesser(undefined, 0, 4)).toBe(1);
    expect(nextGuesser(1, 2, 4)).toBe(3);
    expect(nextGuesser(3, 0, 4)).toBeUndefined();
    const settings = { ...DEFAULT_SETTINGS, mode: 'fastest' as const, players: players.slice(0, 3), rounds: 1 };
    let g = play(newGame(settings, CARDS.slice(0, 5)), { type: 'countdown' }, { type: 'play' }, { type: 'answer', correct: false }, { type: 'timeUp' });
    g = reduce(g, { type: 'toggle', index: 0 });
    expect(g.turn[0]).toMatchObject({ correct: true, guesser: 1 });
    g = reduce(g, { type: 'toggle', index: 0 });
    expect(g.turn[0]).toMatchObject({ correct: true, guesser: 2 });
    g = reduce(g, { type: 'toggle', index: 0 });
    expect(g.turn[0].correct).toBe(false);
    expect(g.turn[0].guesser).toBeUndefined();
  });

  it('keeps up to 12 players and restores defaults when missing', () => {
    const many = Array.from({ length: 15 }, (_, i) => ({ name: `p${i}`, avatar: 'camel' }));
    expect(normalizeSettings({ ...DEFAULT_SETTINGS, players: many } as unknown as Settings).players).toHaveLength(12);
    expect(normalizeSettings({ mode: 'fastest' } as unknown as Settings).players).toHaveLength(4);
    expect(normalizeSettings({ mode: 'fastest' } as unknown as Settings).mode).toBe('fastest');
  });
});
