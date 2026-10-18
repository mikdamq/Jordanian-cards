import { describe, expect, it } from 'vitest';
import { CARDS, CATEGORIES } from './data/cards';
import { DEFAULT_SETTINGS, newGame, reduce, winners, type Game } from './game';
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
    const settings = { ...DEFAULT_SETTINGS, rounds: 3 as const, teams: ['أ', 'ب'] };
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
    const settings = { ...DEFAULT_SETTINGS, teams: ['أ', 'ب'] };
    let g = newGame(settings, CARDS.slice(0, 2));
    g = play(g, { type: 'countdown' }, { type: 'play' }, { type: 'answer', correct: true }, { type: 'answer', correct: true });
    expect(g.phase).toBe('summary');
    expect(reduce(g, { type: 'confirmTurn' }).phase).toBe('final');
  });

  it('reports ties', () => {
    expect(winners([4, 4, 1])).toEqual([0, 1]);
  });
});
