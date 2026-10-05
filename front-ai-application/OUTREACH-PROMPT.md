# Outreach prompt

Copy everything between the lines, fill in the [brackets], attach screenshots, and send.

---

I want to send a cold outreach to a company and build the deliverables for it, the same way we did for Front AI / reChanneld (DC Thomson, Reach, Mirror, Express, M.E.N).

**About me**
Kira Krysanov, Finland. Ex-Leadoo and Ex-Videobot. I offer semi-automated, deeply personalised outreach packs for B2B sales teams, plus explainer and personalised video. Contact: kira.krysanov@gmail.com [+ phone / LinkedIn URL].

**Target company**
- Name and website: [ ]
- What they sell (my understanding): [ ]
- Person I'm contacting, title and LinkedIn: [ ]
- How I found them / any connection: [ ]
- Anything I already know (funding, hiring, new markets, news): [ ]

**What I want this time** (delete what you don't need)
- [ ] Step 1: Research the company
- [ ] Step 2: Review their website and LinkedIn
- [ ] Step 3: Pick 1–2 of THEIR likely target customers (or use these: [ ])
- [ ] Step 4: Build a sample pitch pack for one of their target customers
- [ ] Step 5: Write my cold outreach to the company (LinkedIn note + email)
- [ ] Step 6: Explainer video idea or storyboard

**Attached screenshots**
- Their website: [homepage, product page, pricing, contact or help page]
- Their product UI, if I have it: [ ]
- Their target customer's site: [homepage, contact or help page, subscribe or pricing page, footer]

**How to do it**

1. **Research deeply first.** Use recent sources (results, funding, hires, news, leadership). Link sources. Clearly mark anything you could not verify, and never invent numbers, names or quotes.
2. **Find the one sharp angle.** I want one concrete, checkable finding, such as "no Help link anywhere", "two sites show two prices" or "the only form is for investors". Explain why it matters now (deadline, renewal, new rules, funding, expansion).
3. **Client deliverables, built as two PDFs:**
   - **Proposal pack, about 10–14 A4 pages:** cover → summary letter (signed by the person who will send it) → company today → audit with findings and a scorecard → concept overview with numbered notes → before/after → recommended structure → timing angle → value model (assumptions clearly marked) → pilot → video storyboard → about the product, with real facts only → CTA.
   - **Concept page, long 1440px:** the customer's REAL site from my screenshots, unchanged, with only the product layered on top. No redesigns. Yellow numbered markers must match the notes in the pack.
4. **Product accuracy:**
   - Draw the product's UI only from real screenshots or the product's own website.
   - If you have to assume something the product can do, say so and give me a question to ask.
   - Mark all illustrative numbers (analytics, waiting times) as illustrative.
5. **Tone of the deliverables:** professional, respectful and confident, written from the reader's side. No blame and no hype. Facts with dates.
6. **My messages:**
   - **LinkedIn connection note:** max 200 characters, with the character count shown.
   - **Email:** short, casual Finnish style, confident. Say what I made, the one sharp finding, and a 20-minute call ask.
   - **If asked about automation:** say "semi-automated, I set the strategy and quality-check everything". Use "automation" language, not "AI".
   - **Versions:** English, plus Finnish if the recipient is Finnish.
7. **Don't give away too much for free.** One sample pack is enough. The next step is a call, then a paid pilot.
8. **Afterwards, tell me:**
   - what to check before sending
   - what's still assumed
   - which files to attach

Commit the files to `front-ai-application/<company-name>/` and send them to me here.

---

## Automatic prospect finding (step 0)

Add this to the prompt when you don't know the targets yet:

> **Find prospects for me first.** Before building anything:
> 1. Find who [company] sells to today (customer logos, case studies, press releases, partner and event pages). Summarise their ideal customer: industry, size and country.
> 2. List 8–10 look-alike prospects in the market they're targeting, with sources.
> 3. For each, check for a visible problem the product fixes (contact or help page, footer, reviews, pricing) and a "why now" (news, leadership change, launch, price change, regulation).
> 4. Score each on: fit, a problem I can screenshot, why now, a named buyer. Show the top 3 in a table with the reason and the person to contact (title, plus name if public).
> 5. Stop and let me pick one. If the sites are reachable, run `tools/capture.js` on the chosen prospect to take the screenshots. If not, tell me exactly which pages to screenshot.

## Taking screenshots automatically

`tools/capture.js` saves full-page screenshots of a site's homepage, its contact, help and subscribe/pricing pages, and the footer. It also writes `links.json`, a list of every navigation and footer link, which is how findings like "no Contact Us in 100 footer links" are spotted.

- **In this cloud session:** it only works once the sites are allowed in the environment's network settings (Network access → a broader level, or Custom with the domains added).
- **On your own computer:** install Node, run `npm i playwright` and `npx playwright install chromium`, then `node capture.js https://www.example.com`. Upload the `captures/` folder here.

## Short version (when I'm in a hurry)

> New outreach. Company: [name, website]. Contact: [name, title]. Their likely targets: [names or "pick for me"]. Screenshots attached. Do the full pack like Reach/Mirror: research, sharp finding, proposal PDF + concept on the real site, LinkedIn note (≤200 chars) and a short casual email from me. Mark everything unverified.

## Checklist before I send anything

- [ ] Every number has a source or is marked illustrative
- [ ] Prices and phone numbers checked on the live site today
- [ ] Product UI matches the real product
- [ ] Recipient name, title and email checked on LinkedIn
- [ ] Placeholders filled in ([e-mail], [phone])
- [ ] Message under 200 characters for LinkedIn
- [ ] Only the client-facing files attached (not internal notes)
