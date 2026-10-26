// Renders listing-<theme>.html slides to Etsy listing images (3200x2400). Run: node render-listing.js <club|retro|rally>
const { chromium } = require('playwright');
const path = require('path');
const theme = process.argv[2] || 'club';
const names = ['01-hero', '02-whats-inside', '03-before-after', '04-stats-tracker', '05-hyperlinked', '06-who-its-for', '07-what-you-receive'];
(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1600, height: 1200 }, deviceScaleFactor: 2 });
  await page.goto('file://' + path.join(__dirname, `listing-${theme}.html`), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  for (let i = 0; i < names.length; i++) {
    await page.locator('#s' + (i + 1)).screenshot({ path: path.join(__dirname, '..', 'listings', theme, 'images', names[i] + '.jpg'), type: 'jpeg', quality: 92 });
  }
  await browser.close();
})();
