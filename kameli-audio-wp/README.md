# Kameli Audio – WordPress-teema

A WordPress block theme for the Kameli Audio website, built on the page structure of the Canva
mockups (Palvelut, Ota yhteyttä) and the copy in `Kameli_Audio-projekti.docx`.

Look: charcoal with the Kameli Audio green (#52B489), wide Archivo headings that echo
the logo's lettering, and the logo's waveform line repeated at the bottom of the page headers.

## Install

1. In WordPress: **Appearance → Themes → Add New → Upload Theme**, choose `kameli-audio.zip`, then **Activate**.
2. On first activation the theme creates automatically:
   - pages **Etusivu**, **Palvelut**, **Palvelut › Yritykset**, **Palvelut › Yksityiset**, **Palvelut › Artistit**, **Ota yhteyttä**, **Blogi**
   - the main menu (Palvelut · Yritykset · Yksityiset · Artistit · Blogi · Ota yhteyttä)
   - the blog: categories **Asiakastarinat** and **Artikkelit**, Blogi as the posts page, and 8 drafts (see Blog below)
   - Etusivu as the site's front page, and clean URLs (`/palvelut/yritykset/`) if the site still used the default `?p=123` format.
   Existing pages with the same address are never overwritten.
3. **Site that already had content** (e.g. an existing kameliaudio.fi): the theme never changes existing
   pages on its own, so an old front page or old pages at the same addresses would keep their old content.
   Go to **Appearance → Kameli Audio -asennus** (a notice links there), keep the pages ticked and click
   **Käytä teeman sivuja**. Their old content is saved in each page's revisions (or as a "Vanha: …" draft
   if revisions are disabled), Etusivu becomes the front page and Blogi the posts page.
   Note: *Live Preview* before activation shows the site's current content in the new theme and will look
   empty – the theme's pages only exist after activation.
4. **Settings → General**: set *Site Title* to `Kameli Audio`, *Site Language* to `Suomi`,
   and *Yhteydenottojen vastaanottaja* to the email address that should receive contact-form messages.

Requires WordPress 6.6 or newer (tested on 7.1).

## Editing

- **Page content** (texts, images, lists): *Pages* → open the page. Every section is a normal editable block.
- **Logo**: the Kameli Audio logo ships with the theme and shows automatically. To use a different file: *Appearance → Editor → Patterns → Header* → Site Logo.
- **Menu**: *Appearance → Editor → Navigation*.
- **Ready-made sections** (hero, cards, contact form …) are under the *Kameli Audio* category in the block inserter's *Patterns* tab.

## Blog and case studies

- Blog: `/blogi/`, with filter buttons Kaikki · Artikkelit · Asiakastarinat.
- Case studies (references) are blog posts in the **Asiakastarinat** category, at `/category/asiakastarinat/`.
  The three newest also appear on Etusivu and Palvelut.
- **New case study:** *Posts → Add New* → choose the *Asiakastarina (pohja)* pattern (fact box, Lähtötilanne,
  Ratkaisu, Lopputulos, customer quote) → set category *Asiakastarinat* → add a featured image → Publish.
- **New article:** *Posts → Add New*; new posts go to *Artikkelit* by default.
- Drafts created on activation (not visible until published): 3 case study templates and 5 articles based on the
  January video topics in the project plan.
- Posts without a featured image show the green waveform in the card instead of a photo.
- Every post ends with the "Pyydä tarjous" band and the contact form.

## Contact form

The form is the shortcode `[kameli_yhteydenotto]` (already on every page). Every message is
**saved in WordPress** under **Yhteydenotot** in the admin menu *and* emailed to the recipient set in
Settings → General. If the host's email delivery is unreliable, install an SMTP plugin
(e.g. *WP Mail SMTP*) – messages are kept in Yhteydenotot either way. Spam protection: hidden
honeypot field + WordPress nonce.

## Placeholders to replace

| Where | What |
|---|---|
| Etusivu, Yksityiset, Artistit | Draft copy – replace with final texts |
| Blog | 3–5 case studies before launch (project plan), featured images |
| Ota yhteyttä | Phone numbers (`+358 XX XXX XXXX`), check the email addresses, team photos |
| Footer, contact sections | Check the email addresses |

## Rebuilding the zip

After changing files in `kameli-audio/`, run `./build-zip.sh`.

## Structure

```
kameli-audio/
├── style.css, theme.json      theme info, colours, fonts (Archivo, self-hosted), spacing
├── functions.php
├── inc/markup.php             helpers that generate the repeated sections
├── inc/contact-form.php       contact form, message storage, settings field
├── inc/starter-content.php    creates pages + menu on first activation
├── patterns/                  one pattern per page, case study template, CTA, contact, footer
├── templates/, parts/         page, blog, category, post and 404 templates, header, footer
└── assets/                    CSS, font, icons, placeholder images
```

Project plan and status: [`docs/projektisuunnitelma.md`](docs/projektisuunnitelma.md).
