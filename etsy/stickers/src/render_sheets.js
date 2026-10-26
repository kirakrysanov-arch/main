// Renders the printable sticker sheets and the guide to PDFs plus page previews. Run: node render_sheets.js
const { chromium } = require('playwright');
const path = require('path');
const fs = require('fs');
const jobs = [['print-sheets.html', 'Tennis-Stickers-Printable-Sheets.pdf', '8.5in', '11in', 816, 1056],
              ['guide.html', 'READ-ME-FIRST.pdf', '8.5in', '11in', 816, 1056]];
(async () => {
  const browser = await chromium.launch();
  fs.mkdirSync(path.join(__dirname, 'previews'), { recursive: true });
  for (const [src, out, pw, ph, vw, vh] of jobs) {
    const page = await browser.newPage({ viewport: { width: vw, height: vh }, deviceScaleFactor: 2 });
    await page.goto('file://' + path.join(__dirname, src), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.pdf({ path: path.join(__dirname, '..', 'listing', 'upload', out), width: pw, height: ph, printBackground: true, preferCSSPageSize: true });
    const pages = await page.locator('section.page').all();
    for (let i = 0; i < pages.length; i++) {
      await pages[i].screenshot({ path: path.join(__dirname, 'previews', `${src.replace('.html', '')}-${i + 1}.png`) });
    }
    await page.close();
  }
  await browser.close();
})();
