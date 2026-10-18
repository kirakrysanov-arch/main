# Kameli Audio – WordPress-teema

A WordPress block theme for the Kameli Audio website, built on the page structure of the Canva
mockups (Palvelut, Ota yhteyttä) and the copy in `Kameli_Audio-projekti.docx`.

Look: charcoal with the Kameli Audio green (#52B489), wide Archivo headings that echo
the logo's lettering, and the logo's waveform line repeated at the bottom of the page headers.

## Install

1. In WordPress: **Appearance → Themes → Add New → Upload Theme**, choose `kameli-audio.zip`, then **Activate**.
2. On first activation the theme creates automatically:
   - pages **Etusivu**, **Palvelut**, **Palvelut › Yritykset**, **Palvelut › Yksityiset**, **Palvelut › Artistit**, **Ota yhteyttä**
   - the main menu (Palvelut · Yritykset · Yksityiset · Artistit · Ota yhteyttä)
   - Etusivu as the site's front page, and clean URLs (`/palvelut/yritykset/`) if the site still used the default `?p=123` format.
   Existing pages with the same address are never overwritten.
3. **Settings → General**: set *Site Title* to `Kameli Audio`, *Site Language* to `Suomi`,
   and *Yhteydenottojen vastaanottaja* to the email address that should receive contact-form messages.

Requires WordPress 6.6 or newer (tested on 7.1).

## Editing

- **Page content** (texts, images, lists): *Pages* → open the page. Every section is a normal editable block.
- **Logo**: the Kameli Audio logo ships with the theme and shows automatically. To use a different file: *Appearance → Editor → Patterns → Header* → Site Logo.
- **Menu**: *Appearance → Editor → Navigation*.
- **Ready-made sections** (hero, cards, contact form …) are under the *Kameli Audio* category in the block inserter's *Patterns* tab.

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
├── patterns/                  one pattern per page + footer
├── templates/, parts/         page/post/404 templates, header, footer
└── assets/                    CSS, font, icons, placeholder images
```
