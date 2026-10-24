const { chromium } = require('/opt/node22/lib/node_modules/playwright');
(async () => {
  const b = await chromium.launch();
  const phone = () => b.newPage({ viewport: { width: 360, height: 640 }, deviceScaleFactor: 3, colorScheme: 'light', isMobile: true, hasTouch: true });
  { const p = await phone(); const btn = (n) => p.getByRole('button', { name: n }).first();
    await p.goto('http://localhost:4173/'); await p.waitForTimeout(900); await btn('يلا نلعب').click(); await p.waitForTimeout(400);
    await p.getByRole('button', { name: 'اختار الكل' }).evaluate(el => el.closest('section, .panel, div').scrollIntoView({ block: 'start' }));
    await p.waitForTimeout(400); await p.screenshot({ path: '../../store/raw/categories.png' }); await p.close(); }
  { const p = await phone(); p.on('dialog', d => d.accept()); const btn = (n) => p.getByRole('button', { name: n }).first();
    await p.goto('http://localhost:4173/'); await p.waitForTimeout(900); await btn('يلا نلعب').click(); await p.waitForTimeout(400);
    await p.getByText('30 ثانية').click(); await p.locator('.slider__ticks button').first().click();
    await btn('يلا نبلّش!').click(); await p.waitForTimeout(400);
    for (let turn = 0; turn < 2; turn++) {
      await btn(/جاهزين/).click(); await p.waitForTimeout(4200);
      for (let k = 0; k < (turn ? 4 : 6); k++) { await btn(/عرفوها/).click().catch(() => {}); await p.waitForTimeout(450); }
      await p.waitForTimeout(27500); await btn('تمام').click(); await p.waitForTimeout(900);
      if (turn === 0) for (let s = 0; s < 3; s++) { if (await p.getByRole('button', { name: /جاهزين/ }).count()) break;
        const l = await p.$$eval('button', els => els.map(e => e.innerText.trim()).filter(t => t && t !== '✕')); await btn(l[l.length - 1]).click(); await p.waitForTimeout(700); }
    }
    await p.waitForTimeout(6000); await p.screenshot({ path: '../../store/raw/final.png' }); await p.close(); }
  await b.close(); console.log('ok');
})();
