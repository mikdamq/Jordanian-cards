import type { CategoryId } from './data/cards';

/**
 * Cross-stitch (tatreez) artwork. Each string row is one row of stitches:
 * '.' is bare fabric, a letter is an X stitch in that thread colour.
 */
export type Thread = 'r' | 'g' | 'y' | 'k' | 'b';
export type StitchArt = string[];

export const CATEGORY_ART: Record<CategoryId, StitchArt> = {
  // Old TV with antenna and a play mark
  screen: [
    '..k....k..',
    '...k..k...',
    '....kk....',
    'rrrrrrrrrr',
    'r........r',
    'r...y....r',
    'r...yy...r',
    'r...y....r',
    'rrrrrrrrrr',
    '.k......k.',
  ],
  // Mansaf on its tray
  food: [
    '...k..k...',
    '....k..k..',
    '....yy....',
    '...yyyy...',
    '..yyykyy..',
    '.yyyyyyyy.',
    'rrrrrrrrrr',
    '.rrrrrrrr.',
  ],
  // Al-Khazneh, Petra
  places: [
    '....rr....',
    '...rrrr...',
    '..rrrrrr..',
    '.rrrrrrrr.',
    'rrrrrrrrrr',
    '.r.r..r.r.',
    '.r.r..r.r.',
    '.r.r..r.r.',
    'rrrrrrrrrr',
  ],
  // Yellow Amman taxi
  life: [
    '....kk....',
    '...yyyy...',
    '..ybbbby..',
    '.yyyyyyyy.',
    'yyyyyyyyyy',
    'ykyyyyyyky',
    '.kk....kk.',
  ],
  // Speech bubble
  sayings: [
    '.rrrrrrrrr.',
    'r.........r',
    'r..k.k.k..r',
    'r.........r',
    '.rrrrrrrrr.',
    '..rr.......',
    '.r.........',
  ],
  // Dalleh coffee pot
  heritage: [
    '....k......',
    '...kyk.....',
    '....y......',
    '...yyy.....',
    '..yyyyy...y',
    '..yyyyy..y.',
    '..yyyyyyy..',
    '.yyyyyyy...',
    'yyyyyyyyy..',
    '.kkkkkkk...',
  ],
  // Football
  fun: [
    '...kkkk...',
    '.kk....kk.',
    '.k..kk..k.',
    'k..kkkk..k',
    'k..kkkk..k',
    'k...kk...k',
    '.k......k.',
    '.kk....kk.',
    '...kkkk...',
  ],
  // Cat face
  animals: [
    'k.......k',
    'kk.....kk',
    'kyk...kyk',
    'kyyyyyyyk',
    'yykyyykyy',
    'yyyyyyyyy',
    'yyyykyyyy',
    '.yykkkyy.',
    '..yyyyy..',
  ],
  // Builder's hard hat
  jobs: [
    '...yyyy...',
    '..yyyyyy..',
    '.yyykyyyy.',
    '.yyykyyyy.',
    'yyyykyyyyy',
    'yyyyyyyyyy',
    'kkkkkkkkkk',
  ],
  // Laptop
  office: [
    '.kkkkkkkk.',
    '.kbbbbbbk.',
    '.kbyybbbk.',
    '.kbbbbbbk.',
    '.kkkkkkkk.',
    'kkkkkkkkkk',
    '.kkkkkkkk.',
  ],
  // Engagement ring
  weddings: [
    '....b....',
    '...bbb...',
    '....b....',
    '..yyyyy..',
    '.y.....y.',
    'y.......y',
    'y.......y',
    '.y.....y.',
    '..yyyyy..',
  ],
  // Cassette tape
  nineties: [
    'kkkkkkkkkkk',
    'k.........k',
    'k.kkk.kkk.k',
    'k.k.k.k.k.k',
    'k.kkk.kkk.k',
    'k.........k',
    'k..rrrrr..k',
    'kkkkkkkkkkk',
  ],
  // White-stone houses on Amman's hills
  amman: [
    '....yy....',
    '...yyyy...',
    '.yy.yyyy..',
    '.yy.ykyy..',
    'yyyyyyyyyy',
    'ykyykyykyy',
    'yyyyyyyyyy',
    'ykyykyykyy',
  ],
  // Crescent and star
  ramadan: [
    '..yyy.....',
    '.yyy......',
    'yyy....y..',
    'yyy...yyy.',
    'yyy....y..',
    'yyy.......',
    '.yyy......',
    '..yyy.....',
  ],
  // Running figure
  actions: [
    '....kk....',
    '....kk....',
    '..kkkkk...',
    '.k..kk.k..',
    '....kk..k.',
    '...k..k...',
    '..k....k..',
    '.k......k.',
  ],
  // Cool face with sunglasses
  shabab: [
    '...yyyyy...',
    '.yyyyyyyyy.',
    '.yyyyyyyyy.',
    'kkkkkkkkkkk',
    'ykkkyyykkky',
    'yykyyyyykyy',
    'yyyyyyyyyyy',
    '.yykyyykyy.',
    '.yyykkkyyy.',
    '...yyyyy...',
  ],
};

export type AvatarId = 'falcon' | 'oryx' | 'camel' | 'horse' | 'iris' | 'olive';

export const AVATARS: { id: AvatarId; ar: string; art: StitchArt }[] = [
  {
    id: 'falcon',
    ar: 'صقر',
    art: [
      '....kkkk..',
      '..kkkkkkkk',
      '.kkyykkkkk',
      'kkkyykkkkk',
      'yykkkkkkkk',
      '.y.kkkkkkk',
      '...kyyyykk',
      '...yyyyyyk',
      '...kyyyykk',
      '....kkkkk.',
    ],
  },
  {
    id: 'oryx',
    ar: 'مها',
    art: [
      'k........k',
      '.k......k.',
      '..k....k..',
      '...k..k...',
      '...kkkk...',
      '..kyyyyk..',
      '..kkyykk..',
      '...kyyk...',
      '...kyyk...',
      '....kk....',
    ],
  },
  {
    id: 'camel',
    ar: 'جمل',
    art: [
      '.kk...........',
      'kyyk..........',
      '.yy....yy.....',
      '.yy...yyyy....',
      '.yy..yyyyyy...',
      '.yyyyyyyyyyy..',
      '..yyyyyyyyyyy.',
      '...y.y...y.y.y',
      '...y.y...y.y..',
      '...k.k...k.k..',
    ],
  },
  {
    id: 'horse',
    ar: 'حصان',
    art: [
      '....k.k...',
      '...kkkkr..',
      '..kkykkr..',
      '.kkkkkkr..',
      'kkkkkkkkr.',
      'kk..kkkkr.',
      '....kkkkr.',
      '...kkkkkkr',
      '..kkkkkkkk',
      '.rrrrrrrrr',
    ],
  },
  {
    id: 'iris',
    ar: 'سوسنة',
    art: [
      '....b.....',
      '...bbb....',
      '..bbkbb...',
      'b.bbkbb.b.',
      'bbbbbbbbb.',
      '.bbbbbbb..',
      '..bbbbb...',
      '....g.....',
      '..g.g.g...',
      '...ggg....',
    ],
  },
  {
    id: 'olive',
    ar: 'زيتونة',
    art: [
      '...gggg...',
      '.ggggggggg',
      'gggkggggg.',
      'ggggggkggg',
      '.gggggggg.',
      '...gkkg...',
      '....kk....',
      '....kk....',
      '...kkkk...',
    ],
  },
];

export const avatarById = (id: AvatarId) => AVATARS.find((a) => a.id === id) ?? AVATARS[0];

/** One repeat of the border band: a chain of diamonds between running stitches. */
export const TATREEZ_BAND: StitchArt = [
  'y.y.y.',
  '...r..',
  '..r.r.',
  '.r.g.r',
  'r.ggg.',
  '.r.g.r',
  '..r.r.',
  '...r..',
  'y.y.y.',
];

export const MODE_ART: Record<'classic' | 'headsup' | 'fastest', StitchArt> = {
  // Zipped mouth: "not a word"
  classic: [
    '...yyyyy...',
    '.yyyyyyyyy.',
    'yyykyyykyyy',
    'yyyyyyyyyyy',
    'ykkkkkkkkky',
    'yykykykykyy',
    'yyyyyyyyyyy',
    '.yyyyyyyyy.',
    '...yyyyy...',
  ],
  // Phone held sideways on the forehead
  headsup: [
    'kkkkkkkkkkk',
    'kbbbbbbbbbk',
    'kkkkkkkkkkk',
    '...yyyyy...',
    '..yyyyyyy..',
    '..ykyyyky..',
    '..yyyyyyy..',
    '...yykyy...',
    '....yyy....',
  ],
  // Stopwatch: first to answer wins
  fastest: [
    '....kkk....',
    '.....k.....',
    '...kkkkk...',
    '..k.....k..',
    '.k...r...k.',
    '.k...r...k.',
    '.k...rrr.k.',
    '.k.......k.',
    '..k.....k..',
    '...kkkkk...',
  ],
};
