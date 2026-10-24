const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 640, height: 360 }, deviceScaleFactor: 3, colorScheme: 'light', isMobile: true, hasTouch: true });
  const btn = (name) => p.getByRole('button', { name }).first();
  await p.goto('http://localhost:4173/'); await p.waitForTimeout(900);
  await btn('يلا نلعب').click(); await p.waitForTimeout(400);
  await p.getByText('عالجبين').first().click(); await p.waitForTimeout(300);
  await btn('يلا نبلّش!').click(); await p.waitForTimeout(500);
  if (await p.getByRole('button', { name: 'فهمت، يلا!' }).count()) { await btn('فهمت، يلا!').click(); await p.waitForTimeout(500); }
  await btn(/جاهزين/).click(); await p.waitForTimeout(600);
  if (await p.getByRole('button', { name: 'فهمت، يلا!' }).count()) { await btn('فهمت، يلا!').click(); await p.waitForTimeout(500); }
  await p.waitForTimeout(4500);
  await p.screenshot({ path: '../../store/raw/headsup.png' });
  console.log((await p.innerText('body')).replace(/\s+/g, ' ').slice(0, 120));
  await b.close();
})();
