// Ottaa HTML-sivuista PNG-kuvat: node kuvakaappaus.js <leveys> <korkeus> <html> <png> [<html> <png> ...]
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [w, h, ...files] = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: +w, height: +h } });
  for (let i = 0; i < files.length; i += 2) {
    await page.goto('file://' + path.resolve(files[i]), { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: files[i + 1] });
  }
  await browser.close();
})();
