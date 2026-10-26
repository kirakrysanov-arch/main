// Renders listing.html slides to Etsy listing images (3200x2400). Run: node render-listing.js
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 1200 }, deviceScaleFactor: 2 });
  await page.goto('file://' + path.join(__dirname, 'listing.html'), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  const names = ['01-hero', '02-whats-inside', '03-hyperlinked', '04-digital-and-print', '05-features'];
  for (let i = 0; i < names.length; i++) {
    await page.locator('#s' + (i + 1)).screenshot({ path: path.join(__dirname, '..', 'listing-images', names[i] + '.jpg'), type: 'jpeg', quality: 92 });
  }
  await browser.close();
})();
