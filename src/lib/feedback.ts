let ctx: AudioContext | null = null;

function audio(): AudioContext | null {
  try {
    ctx ??= new AudioContext();
    if (ctx.state === 'suspended') void ctx.resume();
    return ctx;
  } catch {
    return null;
  }
}

function tone(freq: number, ms: number, delay = 0, type: OscillatorType = 'sine') {
  const ac = audio();
  if (!ac) return;
  const start = ac.currentTime + delay / 1000;
  const osc = ac.createOscillator();
  const gain = ac.createGain();
  osc.type = type;
  osc.frequency.value = freq;
  gain.gain.setValueAtTime(0.0001, start);
  gain.gain.exponentialRampToValueAtTime(0.25, start + 0.01);
  gain.gain.exponentialRampToValueAtTime(0.0001, start + ms / 1000);
  osc.connect(gain).connect(ac.destination);
  osc.start(start);
  osc.stop(start + ms / 1000 + 0.05);
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
    tone(660, 120);
    tone(990, 180, 100);
    buzz(60);
  },
  skip() {
    tone(300, 200, 0, 'triangle');
    buzz([30, 40, 30]);
  },
  tick: () => tone(880, 60, 0, 'square'),
  go: () => tone(1046, 250),
  end() {
    tone(523, 180);
    tone(392, 180, 180);
    tone(262, 400, 360);
    buzz([200, 80, 200]);
  },
};
