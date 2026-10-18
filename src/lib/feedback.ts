let ctx: AudioContext | null = null;
let noise: AudioBuffer | null = null;

function audio(): AudioContext | null {
  try {
    ctx ??= new AudioContext();
    if (ctx.state === 'suspended') void ctx.resume();
    return ctx;
  } catch {
    return null;
  }
}

function noiseBuffer(ac: AudioContext): AudioBuffer {
  if (noise) return noise;
  noise = ac.createBuffer(1, ac.sampleRate * 0.3, ac.sampleRate);
  const data = noise.getChannelData(0);
  for (let i = 0; i < data.length; i++) data[i] = Math.random() * 2 - 1;
  return noise;
}

function envelope(ac: AudioContext, start: number, peak: number, ms: number): GainNode {
  const gain = ac.createGain();
  gain.gain.setValueAtTime(0.0001, start);
  gain.gain.exponentialRampToValueAtTime(peak, start + 0.005);
  gain.gain.exponentialRampToValueAtTime(0.0001, start + ms / 1000);
  gain.connect(ac.destination);
  return gain;
}

function tone(freq: number, ms: number, delay = 0, type: OscillatorType = 'sine', peak = 0.22) {
  const ac = audio();
  if (!ac) return;
  const start = ac.currentTime + delay / 1000;
  const osc = ac.createOscillator();
  osc.type = type;
  osc.frequency.value = freq;
  osc.connect(envelope(ac, start, peak, ms));
  osc.start(start);
  osc.stop(start + ms / 1000 + 0.05);
}

/** Darbuka "doum": the deep centre stroke. */
function doum(delay = 0, peak = 0.7) {
  const ac = audio();
  if (!ac) return;
  const start = ac.currentTime + delay / 1000;
  const osc = ac.createOscillator();
  osc.frequency.setValueAtTime(140, start);
  osc.frequency.exponentialRampToValueAtTime(55, start + 0.25);
  osc.connect(envelope(ac, start, peak, 380));
  osc.start(start);
  osc.stop(start + 0.45);
}

/** Darbuka "tak": the sharp rim stroke. */
function tak(delay = 0, peak = 0.45) {
  const ac = audio();
  if (!ac) return;
  const start = ac.currentTime + delay / 1000;
  const src = ac.createBufferSource();
  src.buffer = noiseBuffer(ac);
  const filter = ac.createBiquadFilter();
  filter.type = 'bandpass';
  filter.frequency.value = 3200;
  filter.Q.value = 1.2;
  src.connect(filter).connect(envelope(ac, start, peak, 70));
  src.start(start);
  src.stop(start + 0.1);
  tone(820, 40, delay, 'triangle', peak * 0.25);
}

type Stroke = 'D' | 'T' | 't' | '.';

/** Plays a rhythm, one stroke per step: D = doum, T = tak, t = soft tak. */
function rhythm(pattern: string, stepMs: number) {
  [...pattern].forEach((s, i) => {
    const at = i * stepMs;
    if ((s as Stroke) === 'D') doum(at);
    else if (s === 'T') tak(at);
    else if (s === 't') tak(at, 0.2);
  });
}

function buzz(pattern: number | number[]) {
  try {
    navigator.vibrate?.(pattern);
  } catch {
    // Not supported (e.g. iOS Safari).
  }
}

export const feedback = {
  /** Call from a tap so browsers allow audio later in the turn. */
  unlock: () => void audio(),
  correct() {
    rhythm('TT', 90);
    tone(988, 160, 140, 'sine', 0.15);
    buzz(60);
  },
  skip() {
    doum(0, 0.5);
    buzz([30, 40, 30]);
  },
  tick: () => tak(0, 0.25),
  go: () => rhythm('DTT', 150),
  end() {
    rhythm('D.D.D', 140);
    tone(392, 500, 700, 'sawtooth', 0.08);
    buzz([200, 80, 200]);
  },
  /** Maqsum, the classic dabke/party rhythm, twice through. */
  celebrate: () => rhythm('DT.TD.T.DT.TD.TTT', 130),
  select: () => buzz(8),
};
