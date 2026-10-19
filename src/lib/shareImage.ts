import { avatarById, TATREEZ_BAND, type StitchArt } from '../art';
import { SITE_URL } from '../config';
import type { Team } from '../game';

const W = 1080;
const H = 1350;

const C = {
  cream: '#f7f0e3',
  card: '#fbf6ec',
  ink: '#2a1f1a',
  muted: '#7a6650',
  line: '#dccbae',
  red: '#b5121b',
  red2: '#8e0e16',
};

const THREAD: Record<string, string> = { r: '#b5121b', g: '#4f6b2c', y: '#c9962a', k: '#2a1f1a', b: '#3b3f7a' };
const TEAM_COLORS = ['#b5121b', '#4f6b2c', '#3b3f7a', '#b9861f'];

function stitches(ctx: CanvasRenderingContext2D, art: StitchArt, x: number, y: number, cell: number) {
  ctx.lineWidth = cell * 0.3;
  ctx.lineCap = 'round';
  art.forEach((row, r) =>
    [...row].forEach((c, col) => {
      if (c === '.') return;
      const a = x + col * cell;
      const b = y + r * cell;
      ctx.strokeStyle = THREAD[c];
      ctx.beginPath();
      ctx.moveTo(a + cell * 0.17, b + cell * 0.17);
      ctx.lineTo(a + cell * 0.83, b + cell * 0.83);
      ctx.moveTo(a + cell * 0.83, b + cell * 0.17);
      ctx.lineTo(a + cell * 0.17, b + cell * 0.83);
      ctx.stroke();
    }),
  );
}

function patch(ctx: CanvasRenderingContext2D, art: StitchArt, cx: number, cy: number, r: number, ring: string) {
  ctx.fillStyle = ring;
  ctx.beginPath();
  ctx.arc(cx, cy, r + 8, 0, Math.PI * 2);
  ctx.fill();
  ctx.fillStyle = C.card;
  ctx.beginPath();
  ctx.arc(cx, cy, r, 0, Math.PI * 2);
  ctx.fill();
  ctx.setLineDash([6, 6]);
  ctx.strokeStyle = 'rgba(120, 90, 50, 0.35)';
  ctx.lineWidth = 2;
  ctx.beginPath();
  ctx.arc(cx, cy, r - 10, 0, Math.PI * 2);
  ctx.stroke();
  ctx.setLineDash([]);
  const cols = Math.max(...art.map((row) => row.length));
  const side = Math.max(cols, art.length);
  const cell = (r * 1.25) / side;
  stitches(ctx, art, cx - (cols * cell) / 2, cy - (art.length * cell) / 2, cell);
}

function shemagh(ctx: CanvasRenderingContext2D, height: number) {
  ctx.fillStyle = C.cream;
  ctx.fillRect(0, 0, W, height);
  ctx.save();
  ctx.beginPath();
  ctx.rect(0, 0, W, height);
  ctx.clip();
  ctx.fillStyle = C.red;
  const t = 36;
  for (let y = 0; y < height + t; y += t) {
    for (let x = 0; x < W + t; x += t) {
      ctx.beginPath();
      ctx.moveTo(x, y - t / 2 + 3);
      ctx.lineTo(x + t / 2 - 3, y);
      ctx.lineTo(x, y + t / 2 - 3);
      ctx.lineTo(x - t / 2 + 3, y);
      ctx.closePath();
      ctx.moveTo(x, y - t / 4 + 1);
      ctx.lineTo(x - t / 4 + 1, y);
      ctx.lineTo(x, y + t / 4 - 1);
      ctx.lineTo(x + t / 4 - 1, y);
      ctx.closePath();
      ctx.fill('evenodd');
      ctx.fillRect(x + t / 2 - 3, y + t / 2 - 3, 6, 6);
    }
  }
  ctx.restore();
  ctx.fillStyle = C.red;
  ctx.fillRect(0, height - 6, W, 6);
  // Tassels
  for (let x = 40; x < W - 40; x += 18) ctx.fillRect(x, height, 6, 22);
}

function band(ctx: CanvasRenderingContext2D, y: number, cell: number) {
  const tile = TATREEZ_BAND[0].length * cell;
  for (let x = 40; x < W - 40 - tile + 1; x += tile) stitches(ctx, TATREEZ_BAND, x, y, cell);
}

function star(ctx: CanvasRenderingContext2D, cx: number, cy: number, outer: number, inner: number) {
  ctx.beginPath();
  for (let i = 0; i < 14; i++) {
    const r = i % 2 ? inner : outer;
    const a = (Math.PI * i) / 7 - Math.PI / 2;
    ctx[i ? 'lineTo' : 'moveTo'](cx + r * Math.cos(a), cy + r * Math.sin(a));
  }
  ctx.closePath();
  ctx.fill();
}

function fitText(ctx: CanvasRenderingContext2D, text: string, maxWidth: number, size: number, weight = 800, family = 'Almarai') {
  let s = size;
  do {
    ctx.font = `${weight} ${s}px ${family}, Cairo, sans-serif`;
    s -= 2;
  } while (ctx.measureText(text).width > maxWidth && s > 18);
}

export interface ShareResult {
  teams: Team[];
  scores: number[];
  winners: number[];
}

export async function renderResultImage({ teams, scores, winners }: ShareResult): Promise<Blob> {
  await Promise.all(['800 80px Almarai', '700 40px Almarai', '600 40px Cairo'].map((f) => document.fonts?.load(f)));

  const canvas = document.createElement('canvas');
  canvas.width = W;
  canvas.height = H;
  const ctx = canvas.getContext('2d')!;
  ctx.direction = 'rtl';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';

  ctx.fillStyle = C.cream;
  ctx.fillRect(0, 0, W, H);
  shemagh(ctx, 190);

  // Logo badge
  ctx.save();
  ctx.translate(W / 2, 200);
  ctx.rotate(Math.PI / 4);
  ctx.fillStyle = C.cream;
  ctx.fillRect(-70, -70, 140, 140);
  ctx.fillStyle = C.red;
  ctx.beginPath();
  ctx.roundRect(-60, -60, 120, 120, 30);
  ctx.fill();
  ctx.restore();
  ctx.fillStyle = C.cream;
  star(ctx, W / 2, 200, 40, 18);

  ctx.fillStyle = C.ink;
  ctx.font = '800 60px Almarai, Cairo, sans-serif';
  ctx.fillText('ولا كلمة', W / 2, 315);

  const tie = winners.length > 1;
  const champ = teams[winners[0]];
  if (tie) {
    const gap = 230;
    winners.slice(0, 3).forEach((i, k, arr) => {
      const cx = W / 2 + (k - (arr.length - 1) / 2) * gap;
      patch(ctx, avatarById(teams[i].avatar).art, cx, 500, 85, TEAM_COLORS[i]);
    });
  } else {
    patch(ctx, avatarById(champ.avatar).art, W / 2, 510, 100, TEAM_COLORS[winners[0]]);
    ctx.font = '84px sans-serif';
    ctx.fillText('👑', W / 2, 400);
  }

  ctx.fillStyle = C.ink;
  fitText(ctx, tie ? 'تعادل!' : `مبروك يا ${champ.name}!`, W - 160, 72);
  ctx.fillText(tie ? 'تعادل!' : `مبروك يا ${champ.name}!`, W / 2, 685);

  // Scoreboard: rows shrink so up to four teams fit above the border
  const order = scores.map((s, i) => ({ s, i })).sort((a, b) => b.s - a.s);
  const top = 760;
  const rowH = Math.min(96, (H - 225 - top) / order.length - 14);
  order.forEach(({ s, i }, rank) => {
    const y = top + rank * (rowH + 14);
    ctx.fillStyle = C.card;
    ctx.strokeStyle = rank === 0 && !tie ? TEAM_COLORS[i] : C.line;
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.roundRect(120, y, W - 240, rowH, 26);
    ctx.fill();
    ctx.stroke();
    patch(ctx, avatarById(teams[i].avatar).art, W - 180, y + rowH / 2, rowH / 3, TEAM_COLORS[i]);
    ctx.textAlign = 'right';
    ctx.fillStyle = TEAM_COLORS[i];
    fitText(ctx, teams[i].name, 520, Math.round(rowH * 0.46), 800);
    ctx.fillText(teams[i].name, W - 240, y + rowH / 2 + 2);
    ctx.textAlign = 'left';
    ctx.fillStyle = C.ink;
    ctx.font = `800 ${Math.round(rowH * 0.58)}px Almarai, Cairo, sans-serif`;
    ctx.fillText(String(s), 170, y + rowH / 2 + 4);
    ctx.textAlign = 'center';
  });

  band(ctx, H - 200, 10);

  ctx.fillStyle = C.muted;
  ctx.font = '700 34px Almarai, Cairo, sans-serif';
  ctx.fillText('العبوها مع عيلتكم وصحابكم 👇', W / 2, H - 92);
  ctx.fillStyle = C.red;
  ctx.direction = 'ltr';
  ctx.font = '700 32px Almarai, Cairo, sans-serif';
  ctx.fillText(`${SITE_URL}  ·  #ولا_كلمة`, W / 2, H - 46);

  return new Promise((resolve, reject) => canvas.toBlob((b) => (b ? resolve(b) : reject(new Error('canvas'))), 'image/png'));
}

/** Opens the share sheet with the image where supported (phones), otherwise downloads it. */
export async function shareResult(result: ShareResult): Promise<'shared' | 'downloaded' | 'cancelled'> {
  const blob = await renderResultImage(result);
  const file = new File([blob], 'wala-kilmeh.png', { type: 'image/png' });
  const text = `لعبنا ولا كلمة 🇯🇴 العبوها: https://${SITE_URL}`;
  if (navigator.canShare?.({ files: [file] })) {
    try {
      await navigator.share({ files: [file], text });
      return 'shared';
    } catch {
      return 'cancelled';
    }
  }
  const url = URL.createObjectURL(blob);
  const a = document.createElement('a');
  a.href = url;
  a.download = file.name;
  a.click();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  return 'downloaded';
}
