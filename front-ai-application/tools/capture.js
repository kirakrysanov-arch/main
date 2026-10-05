// Capture full-page screenshots of a prospect's key pages.
//
// Usage:
//   node capture.js https://www.example.com [more start URLs...]
//
// For each site it saves the homepage, then finds and saves the pages a
// customer would use for help: contact, help/support/FAQ, subscribe/pricing.
// It also saves a crop of the footer, and writes links.json listing every
// footer and navigation link (useful for "no Help link" style findings).
// Output goes to ./captures/<domain>/.
//
// Needs Node 18+ and Playwright (npm i playwright). In Claude Code cloud
// sessions the bundled Chromium is used automatically.

const { chromium } = require('playwright');
const fs = require('fs');
const path = require('path');

const KEYWORDS = {
  contact: /contact|yhteys|ota yhteytt|kontakt/i,
  help: /help|support|faq|asiakaspalvelu|tuki|customer service|kundtjänst/i,
  subscribe: /subscribe|subscription|pricing|price|plans|tilaa|tilaus|hinnasto|premium/i,
};
const MAX_PER_KIND = 1;

function chromePath() {
  const p = '/opt/pw-browsers/chromium-1194/chrome-linux/chrome';
  return fs.existsSync(p) ? p : undefined;
}

async function dismissCookies(page) {
  const labels = [/accept all/i, /accept/i, /agree/i, /hyväksy/i, /salli kaikki/i, /godkänn/i, /ok/i];
  for (const re of labels) {
    const b = page.getByRole('button', { name: re }).first();
    try { if (await b.isVisible({ timeout: 800 })) { await b.click({ timeout: 1500 }); await page.waitForTimeout(800); return; } } catch {}
  }
}

async function shoot(page, url, file) {
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 45000 });
  await page.waitForTimeout(2500);
  await dismissCookies(page);
  // scroll to trigger lazy images
  await page.evaluate(async () => { for (let y = 0; y < document.body.scrollHeight; y += 800) { window.scrollTo(0, y); await new Promise(r => setTimeout(r, 120)); } window.scrollTo(0, 0); });
  await page.waitForTimeout(800);
  await page.screenshot({ path: file, fullPage: true });
  const footer = page.locator('footer').last();
  try { if (await footer.count()) await footer.screenshot({ path: file.replace('.png', '-footer.png') }); } catch {}
}

async function links(page) {
  return page.evaluate(() => {
    const grab = sel => [...document.querySelectorAll(sel + ' a')].map(a => ({ text: a.innerText.trim(), href: a.href })).filter(l => l.text);
    return { nav: grab('header, nav'), footer: grab('footer'), all: [...document.querySelectorAll('a')].map(a => ({ text: a.innerText.trim(), href: a.href })).filter(l => l.text) };
  });
}

(async () => {
  const starts = process.argv.slice(2);
  if (!starts.length) { console.log('Usage: node capture.js https://www.example.com [...]'); process.exit(1); }
  const browser = await chromium.launch({ executablePath: chromePath() });
  for (const start of starts) {
    const domain = new URL(start).hostname.replace(/^www\./, '');
    const dir = path.join('captures', domain);
    fs.mkdirSync(dir, { recursive: true });
    const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1.5 });
    try {
      await shoot(page, start, path.join(dir, '01-home.png'));
      const l = await links(page);
      fs.writeFileSync(path.join(dir, 'links.json'), JSON.stringify({ nav: l.nav, footer: l.footer }, null, 2));
      let n = 2;
      for (const [kind, re] of Object.entries(KEYWORDS)) {
        const hits = [...new Map(l.all.filter(a => re.test(a.text) || re.test(a.href)).map(a => [a.href, a])).values()].slice(0, MAX_PER_KIND);
        for (const h of hits) {
          const f = path.join(dir, `${String(n++).padStart(2, '0')}-${kind}.png`);
          try { await shoot(page, h.href, f); console.log('saved', f, '←', h.href); } catch (e) { console.log('skip', h.href, e.message); }
        }
        if (!hits.length) console.log(`no ${kind} link found on ${domain}`);
      }
      console.log('done', domain, '→', dir);
    } catch (e) {
      console.log('failed', start, e.message);
    }
    await page.close();
  }
  await browser.close();
})();
