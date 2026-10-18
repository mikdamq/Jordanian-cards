// Renders the game's sound files to WAV.
// Usage: node scripts/make-sounds.mjs [out-dir]   (default: public/sounds)
import { mkdirSync, writeFileSync } from 'node:fs';
import { join } from 'node:path';

const RATE = 44100;
const out = process.argv[2] ?? 'public/sounds';
mkdirSync(out, { recursive: true });

const buffer = (seconds) => new Float32Array(Math.ceil(seconds * RATE));

function addTone(buf, start, freq, dur, { partials = [[1, 1]], decay = 6, attack = 0.004, gain = 0.3 } = {}) {
  const s0 = Math.floor(start * RATE);
  const n = Math.floor(dur * RATE);
  for (let i = 0; i < n && s0 + i < buf.length; i++) {
    const t = i / RATE;
    const env = Math.min(1, t / attack) * Math.exp(-decay * t);
    let v = 0;
    for (const [ratio, amp, pdecay = 0] of partials) v += amp * Math.sin(2 * Math.PI * freq * ratio * t) * Math.exp(-pdecay * t);
    buf[s0 + i] += gain * env * v;
  }
}

/** Short room reverb so synth tones don't sound dry. */
function reverb(buf, mix = 0.18) {
  const taps = [0.029, 0.043, 0.061, 0.083].map((s) => Math.floor(s * RATE));
  const outBuf = Float32Array.from(buf);
  for (let i = 0; i < buf.length; i++) for (const [k, d] of taps.entries()) if (i >= d) outBuf[i] += outBuf[i - d] * mix * (0.8 - k * 0.15);
  return outBuf;
}

function writeWav(name, data) {
  const peak = Math.max(...data.map(Math.abs)) || 1;
  const pcm = Buffer.alloc(44 + data.length * 2);
  pcm.write('RIFF', 0);
  pcm.writeUInt32LE(36 + data.length * 2, 4);
  pcm.write('WAVEfmt ', 8);
  pcm.writeUInt32LE(16, 16);
  pcm.writeUInt16LE(1, 20);
  pcm.writeUInt16LE(1, 22);
  pcm.writeUInt32LE(RATE, 24);
  pcm.writeUInt32LE(RATE * 2, 28);
  pcm.writeUInt16LE(2, 32);
  pcm.writeUInt16LE(16, 34);
  pcm.write('data', 36);
  pcm.writeUInt32LE(data.length * 2, 40);
  data.forEach((v, i) => pcm.writeInt16LE(Math.round((v / peak) * 0.85 * 32767), 44 + i * 2));
  writeFileSync(join(out, name), pcm);
}

// Correct answer: sparkly "coin" chime
{
  const b = buffer(0.9);
  const soft = [[1, 1], [3, 0.25], [5, 0.1]];
  addTone(b, 0, 987.77, 0.09, { partials: soft, decay: 2, gain: 0.25 });
  addTone(b, 0.08, 1318.5, 0.8, { partials: soft, decay: 5, gain: 0.25 });
  [2637, 3136, 3951].forEach((f, i) => addTone(b, 0.12 + i * 0.05, f, 0.4, { decay: 10, gain: 0.06 }));
  writeWav('correct.wav', reverb(b, 0.12));
}

console.log('wrote sounds to', out);
