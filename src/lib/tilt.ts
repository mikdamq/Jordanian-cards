/**
 * How much the screen faces the sky, from deviceorientation angles:
 * +1 lying face up, 0 upright (on the forehead), -1 facing the floor.
 * This is the world-up component of the screen normal, so it reads the same
 * in portrait and in either landscape direction.
 */
export function screenFacing(betaDeg: number, gammaDeg: number): number {
  const rad = Math.PI / 180;
  return Math.cos(betaDeg * rad) * Math.cos(gammaDeg * rad);
}

export type TiltState = 'neutral' | 'down' | 'up';

const TRIGGER = 0.55; // ~33° away from upright
const REARM = 0.3; // must come back near upright before the next tilt counts

export function nextTiltState(prev: TiltState, facing: number): TiltState {
  if (prev === 'neutral') {
    if (facing <= -TRIGGER) return 'down';
    if (facing >= TRIGGER) return 'up';
    return 'neutral';
  }
  return Math.abs(facing) < REARM ? 'neutral' : prev;
}

type PermissionFn = () => Promise<'granted' | 'denied'>;

/** iOS needs an explicit permission prompt, triggered by a user tap. */
export async function requestTiltPermission(): Promise<boolean> {
  const DOE = (globalThis as { DeviceOrientationEvent?: { requestPermission?: PermissionFn } })
    .DeviceOrientationEvent;
  if (!DOE) return false;
  if (typeof DOE.requestPermission !== 'function') return true;
  try {
    return (await DOE.requestPermission()) === 'granted';
  } catch {
    return false;
  }
}
