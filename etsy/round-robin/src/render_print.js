// Renders draw-sheets.html and guide.html to PDFs plus page previews. Run: node render_print.js
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const jobs = [['draw-sheets.html', 'Tennis-Round-Robin-Draw-Sheets.pdf'], ['guide.html', 'READ-ME-FIRST.pdf']];
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 816, height: 1056 }, deviceScaleFactor: 2.5 });
  fs.mkdirSync(path.join(__dirname, 'previews'), { recursive: true });
  for (const [src, out] of jobs) {
    await page.goto('file://' + path.join(__dirname, src), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({ path: path.join(__dirname, '..', 'listing', 'upload', out), width: '8.5in', height: '11in', printBackground: true, preferCSSPageSize: true });
    const pages = await page.locator('section.page').all();
    for (let i = 0; i < pages.length; i++) {
      await pages[i].screenshot({ path: path.join(__dirname, 'previews', `${src.replace('.html', '')}-${i + 1}.png`) });
    }
  }
  await browser.close();
})();
