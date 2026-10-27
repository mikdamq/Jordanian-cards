/** Public site address, used in the shared result image. */
export const SITE_URL = 'walakelmeh.com';

export const CONTACT_EMAIL = 'hello@walakelmeh.com';

/**
 * GoatCounter site code (the "xyz" in xyz.goatcounter.com). Analytics stay
 * off until this is set.
 */
export const GOATCOUNTER_CODE = 'walakelmeh';

/**
 * Optional analytics that load only after the player agrees on the consent banner.
 * Google Analytics 4 measurement ID ("G-…") and Microsoft Clarity project ID.
 * Empty turns the tool, and the banner, off. The website reads these too.
 */
export const GA_ID = 'G-QGHEHC3BEF';
export const CLARITY_ID = '';

/**
 * The "شو رأيك باللعبة؟" card on the winner screen. It shows after this many finished
 * games (each at least REVIEW_MIN_MINUTES long), and once more REVIEW_ASK_AGAIN games
 * after a "مش هلّق". Answers go to the website's form endpoint, which emails them.
 */
export const REVIEW_AFTER_GAMES = 2;
export const REVIEW_MIN_MINUTES = 5;
export const REVIEW_ASK_AGAIN = 5;
export const REVIEW_ENDPOINT = '/api/send.php';
