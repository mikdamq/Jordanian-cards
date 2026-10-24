// Captures real game screens at 1080x1920 (360x640 @3x) for the store kit.
const { chromium } = require('/opt/node22/lib/node_modules/playwright');
const URL = 'http://localhost:4173/';
(async () => {
  const b = await chromium.launch();
  const phone = (scheme = 'light', w = 360, h = 640) => b.newPage({ viewport: { width: w, height: h }, deviceScaleFactor: 3, colorScheme: scheme, isMobile: true, hasTouch: true });
  const btn = (p, name) => p.getByRole('button', { name }).first();
  const toSetup = async (p, mode) => {
    await p.goto(URL); await p.waitForTimeout(900);
    await btn(p, 'يلا نلعب').click(); await p.waitForTimeout(400);
    if (mode) { await p.getByText(mode, { exact: false }).first().click(); await p.waitForTimeout(300); }
  };
  const shot = (p, name) => p.screenshot({ path: `../../store/raw/${name}.png` });

  // 1. Home, light and dark
  for (const s of ['light', 'dark']) { const p = await phone(s); await p.goto(URL); await p.waitForTimeout(1200); await shot(p, `home-${s}`); await p.close(); }

  // 2. Setup: modes and teams; 3. categories
  { const p = await phone(); await toSetup(p); await shot(p, 'setup');
    await p.getByText('الفئات').first().scrollIntoViewIfNeeded(); await p.evaluate(() => window.scrollBy(0, -20)); await p.waitForTimeout(300); await shot(p, 'categories'); await p.close(); }

  // 4. Classic: a card mid-turn, the review, and the winner (full one-round game)
  { const p = await phone(); p.on('dialog', d => d.accept());
    await toSetup(p); await p.getByText('30 ثانية').click(); await p.locator('.slider__ticks button').first().click();
    await btn(p, 'يلا نبلّش!').click(); await p.waitForTimeout(400);
    await shot(p, 'intro');
    for (let turn = 0; turn < 2; turn++) {
      await btn(p, /جاهزين/).click(); await p.waitForTimeout(4200);
      if (turn === 0) { await btn(p, /عرفوها/).click(); await p.waitForTimeout(500); await btn(p, /عرفوها/).click(); await p.waitForTimeout(900); await shot(p, 'play'); }
      for (let k = 0; k < (turn ? 4 : 4); k++) { await btn(p, /عرفوها/).click().catch(() => {}); await p.waitForTimeout(450); }
      await p.waitForTimeout(27500);
      if (turn === 0) await shot(p, 'review');
      await btn(p, 'تمام').click(); await p.waitForTimeout(900);
      for (let s = 0; s < 3; s++) {
        if (await p.getByRole('button', { name: /جاهزين/ }).count()) break;
        const labels = await p.$$eval('button', els => els.map(e => e.innerText.trim()).filter(t => t && t !== '✕'));
        if (turn === 1) break;
        const go = labels[labels.length - 1]; if (!go) break;
        await btn(p, go).click(); await p.waitForTimeout(700);
      }
    }
    await p.waitForTimeout(1500); await shot(p, 'final'); await p.close(); }

  // 5. Dark mode card
  { const p = await phone('dark'); await toSetup(p); await btn(p, 'يلا نبلّش!').click(); await p.waitForTimeout(400);
    await btn(p, /جاهزين/).click(); await p.waitForTimeout(4400); await shot(p, 'play-dark'); await p.close(); }

  // 6. Who's fastest: the "who got it first?" picker
  { const p = await phone(); await toSetup(p, 'مين أسرع؟'); await shot(p, 'setup-fastest');
    await btn(p, 'يلا نبلّش!').click(); await p.waitForTimeout(400); await btn(p, /جاهزين/).click(); await p.waitForTimeout(4200);
    await btn(p, /عرفوها|عرفها/).click().catch(() => {}); await p.waitForTimeout(700); await shot(p, 'fastest'); await p.close(); }

  // 7. Heads up, in landscape
  { const p = await phone('light', 640, 360); await toSetup(p, 'عالجبين');
    await btn(p, 'يلا نبلّش!').click(); await p.waitForTimeout(400); await btn(p, /جاهزين/).click(); await p.waitForTimeout(4500); await shot(p, 'headsup'); await p.close(); }

  await b.close();
  console.log('done');
})();
