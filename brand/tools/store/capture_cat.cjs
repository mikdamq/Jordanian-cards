const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 360, height: 640 }, deviceScaleFactor: 3, colorScheme: 'light', isMobile: true, hasTouch: true });
  await p.goto('http://localhost:4173/'); await p.waitForTimeout(900);
  await p.getByRole('button', { name: 'يلا نلعب' }).click(); await p.waitForTimeout(400);
  const all = p.getByRole('button', { name: 'اختار الكل' });
  await all.click(); await p.waitForTimeout(400);
  await p.getByText('الفئات', { exact: true }).first().evaluate(el => el.scrollIntoView({ block: 'start' })); await p.evaluate(() => document.scrollingElement.scrollBy(0, -12)); await p.waitForTimeout(400);
  await p.screenshot({ path: '../../store/raw/categories.png' });
  console.log((await p.innerText('body')).match(/\d+ من \d+ بطاقة/));
  await b.close();
})();
