import { useEffect, useRef, useState } from 'react';
import { nextTiltState, screenFacing, type TiltState } from './lib/tilt';

/** Counts down while running; returns whole seconds left. */
export function useCountdown(seconds: number, running: boolean, onEnd: () => void, onTick?: (left: number) => void) {
  const [left, setLeft] = useState(seconds);
  const cb = useRef({ onEnd, onTick });
  cb.current = { onEnd, onTick };

  useEffect(() => {
    if (!running) return;
    const endAt = Date.now() + seconds * 1000;
    let last = seconds;
    setLeft(seconds);
    const id = setInterval(() => {
      const now = Math.max(0, Math.ceil((endAt - Date.now()) / 1000));
      if (now === last) return;
      last = now;
      setLeft(now);
      cb.current.onTick?.(now);
      if (now === 0) {
        clearInterval(id);
        cb.current.onEnd();
      }
    }, 100);
    return () => clearInterval(id);
  }, [seconds, running]);

  return left;
}

/** Fires once per forehead tilt: 'down' (screen to floor) or 'up' (screen to sky). */
export function useTilt(enabled: boolean, onTilt: (dir: 'down' | 'up') => void) {
  const [available, setAvailable] = useState(false);
  const cb = useRef(onTilt);
  cb.current = onTilt;

  useEffect(() => {
    if (!enabled) return;
    let state: TiltState = 'neutral';
    // Ignore tilts until the phone has been held upright once, so the
    // turn doesn't start by scoring however the phone happened to be lying.
    let armed = false;
    const handle = (e: DeviceOrientationEvent) => {
      if (e.beta == null || e.gamma == null) return;
      setAvailable(true);
      const facing = screenFacing(e.beta, e.gamma);
      if (!armed) {
        armed = Math.abs(facing) < 0.3;
        return;
      }
      const next = nextTiltState(state, facing);
      if (next !== state && next !== 'neutral') cb.current(next);
      state = next;
    };
    window.addEventListener('deviceorientation', handle);
    return () => window.removeEventListener('deviceorientation', handle);
  }, [enabled]);

  return available;
}

/** Keeps the screen awake during a game where supported. */
export function useWakeLock(active: boolean) {
  useEffect(() => {
    if (!active || !('wakeLock' in navigator)) return;
    let lock: WakeLockSentinel | null = null;
    let cancelled = false;
    const acquire = () =>
      navigator.wakeLock
        .request('screen')
        .then((l) => {
          if (cancelled) void l.release();
          else lock = l;
        })
        .catch(() => {});
    acquire();
    const onVisible = () => document.visibilityState === 'visible' && acquire();
    document.addEventListener('visibilitychange', onVisible);
    return () => {
      cancelled = true;
      document.removeEventListener('visibilitychange', onVisible);
      void lock?.release();
    };
  }, [active]);
}
