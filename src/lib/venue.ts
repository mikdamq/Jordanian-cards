import { DEFAULT_SETTINGS, type Settings } from '../game';
import { track } from './analytics';

/**
 * Café links: /play/?ref=<venue>&night=1 opens setup ready for «ليلة ولا كلمة»: two teams
 * (one per table), charades, 60 seconds, 3 rounds and the family-friendly default categories.
 * The ref stays in the address so GoatCounter also lists it as the referrer.
 */
const params = new URLSearchParams(location.search);
export const venueRef = (params.get('ref') || '').replace(/[^\w-]/g, '').slice(0, 40);
export const venueNight = params.get('night') === '1';

export function nightSettings(current: Settings): Settings {
  return {
    ...current,
    mode: 'classic',
    seconds: 60,
    rounds: 3,
    teams: current.teams.length >= 2 ? current.teams.slice(0, 2) : DEFAULT_SETTINGS.teams,
    categories: DEFAULT_SETTINGS.categories,
    shabab: false,
  };
}

/** One count per scan, by venue (and whether it was a night link). */
export function trackVenue() {
  if (venueRef) track('venue', venueNight ? { ref: venueRef, night: 'night' } : { ref: venueRef });
}
