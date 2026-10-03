from brands import widget, mk

RED = 'var(--red)'; AMB = 'var(--amber)'; GRN = '#0e8f6a'

def ev_box(img, hls, width, note=''):
    h = ''.join(f'<div class="hl" style="left:{l}px;top:{t}px;width:{w}px;height:{hh}px;{st}"></div>' for l, t, w, hh, st in hls)
    return f'<div style="position:relative;width:{width}px"><img src="{img}" style="width:{width}px;display:block">{h}{note}</div>'

def scene3(left, right):
    return (f'<div id="s3" style="display:grid;grid-template-columns:600px 1fr;gap:26px;align-items:start">'
            f'<div class="browser" style="position:relative">{left}</div>'
            f'<div class="card" style="padding:24px 20px;position:relative">{right}</div></div>')

def bb(url):
    return f'<div class="bbar"><i></i><i></i><i></i><div class="url">{url}</div></div>'

CK = lambda **k: k
VIDEO_BG = ['', '', 'background:#0a3b3a', '', '', 'background:linear-gradient(135deg,#0c0d12,#3b3b3b)']

# =========================================================== MIRROR
s = 600 / 1000
mirror_left = bb('mirror.co.uk · footer') + '<div style="padding:16px;background:#262641;position:relative">' + ev_box('img/b/mirror-footer.png', [
    (323, 55, 50, 15, ''),
    (8, 114, 260, 17, 'border-color:var(--blue);box-shadow:0 0 0 5px rgba(11,79,208,.2)'),
    (275, 114, 130, 17, 'border-color:var(--blue);box-shadow:0 0 0 5px rgba(11,79,208,.2)'),
], 568) + '</div>' + mk(5, 'left:-50px;top:110px') + (
    '<div style="padding:18px 22px;font:600 14px/1.5 Lato">'
    '<div style="display:flex;gap:10px;margin-bottom:8px"><span style="width:12px;height:12px;border:3px solid var(--red);border-radius:3px;flex:none;margin-top:4px"></span><span><b>“Contact Us”</b> is link 19 of 38 in the footer, between “About Us” and “Work for us”. There is no “Help” or “Manage my subscription”.</span></div>'
    '<div style="display:flex;gap:10px"><span style="width:12px;height:12px;border:3px solid var(--blue);border-radius:3px;flex:none;margin-top:4px"></span><span>Print and tablet subscriptions each have their own route, separate from Mirror+.</span></div></div>')
mirror_right = mk(6, 'right:-56px;top:20px') + widget('Mirror+', ['Can\'t log in', 'Still seeing ads', 'Billing', 'Renewal &amp; price', 'Cancel'], 3, [
    CK(icon='📅', tone='k', title='Check my renewal', text='See your renewal date and price in My Account, and set a reminder.', btn='Open My Account', foot='Resolve immediately', pop=True),
    CK(icon='i', tone='m', title='Learn more', text='Your first year is £19.99. From year two Mirror+ is £39.99 a year, still under £1 a week.', btn='Read about renewals ↗', foot='Login not required'),
    CK(icon='✕', tone='m', title='Cancel online', text='Turn off auto-renew in a few clicks. You keep access until the end of your year.', btn='Manage auto-renew', foot='Takes about 1 minute'),
], small=True) + '<div class="rule">✓ Cancel online is always an equal, visible choice. Alternatives sit next to it, never in front of it.</div>'

MIRROR = dict(
    key='mirror', name='The Mirror', domain='mirror.co.uk', glow='rgba(200,16,46,.30)', concept_pdf='reChanneld-Mirror-Concept.pdf',
    launcher='Mirror+ &amp; subscriber help',
    c_h1='The Mirror, exactly as it is.<br><em>Plus one front door</em> for Mirror+ readers.',
    c_lead='No redesign. These are mirror.co.uk pages as they are today, with the standard reChanneld widget added and configured with the Mirror\'s own topics: Mirror+, print delivery and vouchers, and the tablet edition.',
    s1_tag='Homepage', s1_h='A Mirror+ subscriber has a question. Today, where do they go?',
    s1_sub='The homepage and top bar link to InYourArea, funeral notices, the shop, competitions, offers and newsletters. There\'s no “Help”. reChanneld adds one small button for subscribers. Nothing else moves.',
    s2_tag='Mirror+ subscribe page', s2_h='From “Already a Mirror+ member? Login” to real help.',
    s2_sub='Today the subscribe page offers existing members only a login button, and its FAQ starts “Not a Digital Subscriber yet?”. With reChanneld, members pick their product and need, and get the fastest fix first.',
    s2_top=(['📱 Mirror+', '📰 Newspaper delivery or vouchers', '📲 Tablet edition', '❓ Something else'], 0),
    s2_crumb='Mirror+', s2_subs=['Can\'t log in', 'Still seeing ads', 'Billing', 'Renewal &amp; price', 'Cancel'], s2_sel=0,
    s2_cards=[CK(icon='🔑', tone='k', title='Reset password', text='Get a log-in link by e-mail. Works on the app and website.', btn='Send log-in link', foot='Resolve immediately', pop=True),
              CK(icon='i', tone='m', title='Learn more', text='Signing in to Mirror+ on each device, step by step.', btn='Read log-in help ↗', foot='Login not required'),
              CK(icon='✉️', tone='l', title='E-mail support', text='Still stuck? Our subscriptions team will help.', btn='Send a message', foot='Reply within 1 working day')],
    s2_h_px=880,
    s3_tag='Footer &amp; renewals', s3_h='June 2027: the first annual Mirror+ renewals double in price.',
    s3_sub='Annual Mirror+ is £19.99 for the first year, then £39.99. The first renewals arrive in June 2027, just after new UK subscription rules start. A “Renewal &amp; price” topic answers the question before it becomes a call, or a cancellation.',
    s3_html=scene3(mirror_left, mirror_right),
    s4_sub='On the Mirror app the widget opens as a stacked view. In the admin panel the Customer team sees widget loads, sessions, top topics and channels for the Mirror in real time.',
    ph_crumb='Mirror+', ph_subs=['Still seeing ads', 'Can\'t log in', 'Billing'],
    ph_c1=CK(title='Sign in again', text='The ad-lite experience works when you\'re signed in on this device.', btn='Sign in', foot='Resolve immediately', tone='k'),
    ph_c2=CK(title='Learn more', text='How the Mirror+ ad-lite experience works.', btn='Read help ↗', foot='Login not required', tone='m'),
    kpis=[('Widget loads', '64,300'), ('Sessions', '14,820'), ('Finished sessions', '12,450')],
    topics=[('Can\'t log in', 90), ('Still seeing ads', 72), ('Renewal &amp; price', 58), ('Paper didn\'t arrive', 44), ('Vouchers', 30)],
    chans=[('My Account', 88), ('Help articles', 64), ('E-mail', 26), ('Phone', 18)],
    # proposal
    cover_tag='Mirror+ &amp; subscriber help · review, concept &amp; business case',
    cover_h1='Every Mirror+<br>reader, to the <em>right place</em>,<br>first time.',
    cover_sub='How one reChanneld front door on mirror.co.uk can support Mirror+ members and print subscribers, get ready for the first annual renewals in June 2027, and serve as the template for every Reach brand.',
    salute='Dear George and the Reach Customer team,',
    letter='''<p>Four months after launch, Mirror+ is one of the most visible parts of Reach's subscription push: the fourth national brand behind a paywall, at £3.99 a month or £19.99 for the first year. Every new member is a customer who will, sooner or later, need help.</p>
  <p>We looked at mirror.co.uk as a Mirror+ member would. There is no “Help” in the navigation. “Contact Us” is link 19 of 38 in the footer. The subscribe page offers existing members only a login button, and its FAQ is written for people who haven't subscribed yet. Print and tablet subscriptions each have their own separate route.</p>
  <p>Meanwhile the first annual Mirror+ renewals arrive in <b>June 2027</b>, when the price doubles to £39.99, just after the new UK subscription rules take effect in January 2027.</p>
  <p>reChanneld is a channel-strategy platform from Helsinki. Its plug-and-play widget asks readers what they need and shows the best channel for it: self-service first, with honest opening hours and waiting times. It sits on top of the pages and systems you already have.</p>''',
    inc1='mirror.co.uk reviewed as a Mirror+ member: 8 findings and a scorecard.',
    inc3='Renewal timing, the 2027 rules, a value model and an 8-week pilot on the Mirror.',
    today_h='A national brand learning to be a subscription business',
    today_lead='One of the UK\'s biggest news brands is moving from reach to recurring revenue, at a moment when search traffic is falling and every subscriber counts.',
    facts=[('20.7 M', 'monthly audience (June 2025, Ipsos iris via Press Gazette)'), ('Jun 2026', 'Mirror+ launched: Reach\'s 15th paywall, 4th national'),
           ('£3.99', 'a month, or £19.99 for year one, then £39.99'), ('£29.99', 'a month for print by vouchers or home delivery (“save 62%”)')],
    timeline=[('2025', 'Google Discover referrals to Reach fall by almost half in the second half of the year.'),
              ('Early 2026', 'Chloe Hubbard, from The Independent, becomes Mirror editor-in-chief.'),
              ('Jun 2026', 'Mirror+ launches with an ad-lite app, exclusive columns, newsletters and offers.'),
              ('Aug 2026', 'Reach passes 50,000 digital subscribers. Mirror North opens in Manchester.'),
              ('Jan 2027', 'UK subscription rules (DMCC Act) start: easy exit, cooling-off, reminders.'),
              ('Jun 2027', 'First annual Mirror+ renewals, at £39.99 instead of £19.99.')],
    means=[('A new kind of customer.', 'Mirror+ members ask about log-in, ads, billing and renewal, questions the print business never had.'),
           ('Three products, three routes.', 'Mirror+, print (vouchers or home delivery) and the tablet edition are sold and supported separately.'),
           ('A renewal price step.', 'Doubling from £19.99 to £39.99 is fair value, but needs explaining before members decide to leave.'),
           ('Print readers still matter.', 'Many still prefer the phone, so honest phone routes stay in the mix.')],
    opp='give Mirror+ members a clear front door before the first renewals in June 2027.',
    src_today='Sources: Press Gazette (Mirror+ launch, Jun 2026; audience data), InPublishing, Reach results and announcements; mirror.co.uk subscribe page (3 Oct 2026).',
    ev_h='mirror.co.uk, seen by a Mirror+ member',
    ev_lead='Screenshots taken on 3 October 2026.',
    ev_html='''<div class="grid2" style="grid-template-columns:1fr 1fr;gap:5mm">
    <figure style="border:1px solid var(--line);border-radius:3mm;overflow:hidden"><img src="img/b/mirror-price.png" style="width:100%;display:block"><figcaption class="small" style="padding:2mm 3mm;background:var(--bg)"><b>Subscribe page.</b> Clear offers: £3.99 a month, or £19.99 for the first year, “then £39.99”.</figcaption></figure>
    <figure style="border:1px solid var(--line);border-radius:3mm;overflow:hidden"><div style="height:62mm;overflow:hidden"><img src="img/b/mirror-faq.jpg" style="width:100%;display:block"></div><figcaption class="small" style="padding:2mm 3mm;background:var(--bg)"><b>FAQ.</b> Ten questions, all for people who haven't subscribed yet. Existing members get a login button.</figcaption></figure>
  </div>
  <figure style="margin-top:5mm;border:1px solid var(--line);border-radius:3mm;overflow:hidden"><div style="background:#262641;padding:3mm;position:relative"><img src="img/b/mirror-footer.png" style="width:100%;display:block">
    <div class="hl" style="left:58.5%;top:33%;width:10%;height:9%"></div></div><figcaption class="small" style="padding:2mm 3mm;background:var(--bg)"><b>Footer.</b> 38 links, from Mirror Bingo to Mahjong. “Contact Us” is the 19th. Print and tablet subscriptions have their own links. No “Help” or “Manage my subscription”.</figcaption></figure>''',
    score=[('2/10', 'Finding help', RED), ('3/10', 'Help for members', RED), ('4/10', 'Renewal clarity', AMB), ('5/10', 'Print routes', AMB), ('8/10', 'Offer clarity', GRN)],
    findings=[('No “Help” anywhere in the navigation', 't-red', 'Critical', 'The top bar serves InYourArea, funeral notices, shop, competitions, offers, newsletters and social. Help is missing.', 'A “Mirror+ &amp; subscriber help” button on every page, opening the widget.'),
              ('“Contact Us” is link 19 of 38 in the footer', 't-red', 'Critical', 'Members have to scroll past games, betting and shopping links to find it.', 'Footer links stay as they are; “Contact Us” opens the widget instead of a generic page.'),
              ('Existing members get only a login button', 't-red', 'High', '“Already a Mirror+ member? Login” is the only route on the subscribe page.', 'A members\' topic list: log-in, ads, billing, renewal, cancel.'),
              ('The FAQ is written for non-subscribers', 't-amb', 'High', 'It opens with “Not a Digital Subscriber yet?”. None of its ten questions covers log-in problems or ads still showing.', 'Member questions answered by the widget, with the FAQ kept for prospects.'),
              ('Renewal doubles the price in June 2027', 't-amb', 'High', '£19.99 for year one, then £39.99. Fair, but a classic moment for “why did I pay more?” and cancellations.', 'A “Renewal &amp; price” topic linked from the reminder e-mail.'),
              ('Three products, three separate routes', 't-amb', 'Medium', 'Mirror+, print (vouchers, home delivery) and the tablet edition each have their own subscribe link.', 'One first question: “Which subscription do you have?”'),
              ('“Still seeing ads” will be a top question', 't-blue', 'Medium', 'Ad-lite only works when the member is signed in on that device, which is easy to miss.', 'Answer it in the app with “Sign in again”.'),
              ('No view of what members need', 't-blue', 'Low', 'With routes spread across pages and inboxes, nobody sees the full picture.', 'reChanneld analytics: topics and channels in real time.')],
    notes=[('“Mirror+ &amp; subscriber help” button', 'on mirror.co.uk. The homepage stays as it is. Finding 01.'),
           ('First question: which subscription?', 'Mirror+, newspaper delivery or vouchers, tablet edition, or something else. Finding 06.'),
           ('Members\' topics.', 'Can\'t log in, still seeing ads, billing, renewal &amp; price, cancel. Findings 03 and 04.'),
           ('“Most popular choice”.', 'Self-service first, e.g. “Send log-in link”, marked “Resolve immediately”.'),
           ('Footer evidence.', '“Contact Us” is link 19 of 38; print and tablet have separate links. Finding 02.'),
           ('Renewal &amp; price.', 'Explains £19.99 → £39.99 before June 2027, with cancel online as an equal choice. Finding 05.'),
           ('In the app.', '“Still seeing ads” → “Sign in again”. Finding 07.'),
           ('Analytics.', 'Widget loads, sessions, top topics and channels for the Mirror. Finding 08.'),
           ('What changes:', 'no design changes, plug-and-play, live in a few days, GDPR compliant with no cookies.')],
    why_no='mirror.co.uk is a high-traffic news site built for advertising and audience. reChanneld doesn\'t compete with it: it adds the missing member path on top, so it can go live in days.',
    cap2='Subscribe page with the widget open: Mirror+ → Can\'t log in → Send log-in link',
    cap3='Footer evidence, and a Renewal &amp; price topic ready for June 2027',
    tree=[('📱 Mirror+', [('Can\'t log in', 'Self-service', 'g'), ('Still seeing ads', 'Article', 'b'), ('Billing', 'My Account', 'g'), ('Renewal &amp; price', 'My Account', 'g'), ('Cancel', 'Equal choice', 'y')]),
          ('📰 Newspaper delivery or vouchers', [('Paper didn\'t arrive', 'Self-service', 'g'), ('Vouchers', 'Self-service', 'g'), ('Payment or price', 'Article → phone', 'b'), ('Holiday stop', 'Self-service', 'g'), ('Cancel or change', 'Equal choice', 'y')]),
          ('📲 Tablet edition', [('Download or log-in', 'Guide', 'b'), ('Billing (app store)', 'Article', 'b'), ('Switch to Mirror+', 'Self-service', 'g')]),
          ('❓ Something else', [('A story or tip', 'Newsdesk form', 'b'), ('Complaint or correction', 'How to complain', 'b'), ('Advertising', 'Reach Solutions', 'b'), ('Anything else', 'Contact form', 'y')])],
    template_note='The Mirror\'s configuration can be copied to the Express, Daily Star, Daily Record and every Reach brand, with each brand\'s own wording and look.',
    ren_h='June 2027: the first Mirror+ renewals',
    ren_lead='Annual Mirror+ members pay £19.99 for their first year. From June 2027 their renewal is £39.99. Explaining that step well is the biggest retention lever the Mirror has.',
    ren_table='''<table class="calc" style="width:100%;border-collapse:collapse"><tr><th>Plan</th><th>Year one</th><th>Then</th><th>First renewals</th></tr>
    <tr><td>Mirror+ monthly</td><td>£3.99 a month</td><td>£3.99 a month</td><td>Every month</td></tr>
    <tr><td>Mirror+ annual</td><td>£19.99</td><td><b>£39.99</b> a year</td><td><b>From June 2027</b></td></tr>
    <tr><td>Print (vouchers / delivery)</td><td>£29.99 a month</td><td>As advertised</td><td>Every month</td></tr></table>''',
    ren_opts='switch to monthly, check what\'s included',
    ren_punch='members who understand what £39.99 buys renew, and those who want to leave can do so in a minute.',
    arpu_label='annual plan', arpu='£39.99', ret_val='≈ £8,000',
    pilot_lead='Suggested scope: Mirror+ members on mirror.co.uk and the Mirror app, starting well ahead of the June 2027 renewals.',
    pilot_where='mirror.co.uk (subscribe, account and footer “Contact Us”) and in the Mirror app',
    kpis_pilot=[('Member contacts per 1,000 Mirror+ members', 'Your data, before vs during'), ('Top topics and channels', 'reChanneld analytics'), ('Finished sessions', 'reChanneld analytics'),
                ('Log-in and “ads” contacts', 'Your data, before vs during'), ('Renewal-topic choices', 'reChanneld analytics'), ('Mirror+ churn', 'Your data')],
    video_h='“Welcome to Mirror+”: a 40-second onboarding video',
    video_lead='Most log-in and “still seeing ads” questions come in a member\'s first week. A short welcome video in the confirmation e-mail and app shows how to sign in on every device and where to find help.',
    video=[('0:00–0:06', '➕ “Welcome to Mirror+”', 'The Mirror+ cross lights up on a phone.', 'Welcome to Mirror+. Great to have you.'),
           ('0:06–0:16', '📱💻 Sign in once<br>on each device', 'Phone, laptop and tablet each show the sign-in.', 'Sign in on each device, and fewer ads follow you.'),
           ('0:16–0:24', '✨ Exclusive columns<br>· newsletters', 'A quick tour of Mirror+ extras.', 'Exclusive columns, newsletters and offers, just for members.'),
           ('0:24–0:32', '👋 “Hey, how may<br>we help you?”', 'The reChanneld widget: Can\'t log in → Send log-in link.', 'Any question? The help button sorts it in seconds.'),
           ('0:32–0:36', '📅 Your plan,<br>your choice', 'Renewal &amp; price topic.', 'Check your renewal or change your plan, any time.'),
           ('0:36–0:40', 'Mirror+<br>Help: one tap away', 'End card in Mirror red.', 'Enjoy your Mirror.')],
    video_where='The Mirror+ confirmation e-mail, the app\'s first launch, and the help page. A 15-second cut can run before the June 2027 renewal reminders.',
)

# =========================================================== EXPRESS
s = 600 / 960
express_left = bb('express.co.uk · footer') + '<div style="background:#2b2524;padding:0">' + ev_box('img/b/express-footer.png', [
    (int(556*s), int(381*s), int(92*s), int(19*s), ''),
    (int(556*s), int(402*s), int(108*s), int(19*s), ''),
    (int(556*s), int(316*s), int(54*s), int(19*s), 'border-color:var(--amber);box-shadow:0 0 0 4px rgba(201,129,0,.2)'),
], 600) + '</div>' + mk(5, 'left:-50px;top:250px') + (
    '<div style="padding:18px 22px;font:600 14px/1.5 Lato">'
    '<div style="display:flex;gap:10px;margin-bottom:8px"><span style="width:12px;height:12px;border:3px solid var(--red);border-radius:3px;flex:none;margin-top:4px"></span><span>Over 100 footer links, and <b>no “Contact Us”</b>. The only help-like links are “How to Complain” and “Report a Tech Issue”.</span></div>'
    '<div style="display:flex;gap:10px"><span style="width:12px;height:12px;border:3px solid var(--amber);border-radius:3px;flex:none;margin-top:4px"></span><span>“About Us” is the nearest thing to a company contact.</span></div></div>')
express_right = mk(6, 'right:-56px;top:20px') + widget('Express Premium', ['Can\'t log in', 'Billing', 'Price after the offer', 'Commenting', 'Cancel'], 2, [
    CK(icon='📅', tone='k', title='Check my plan', text='See your next payment date and price in My Account.', btn='Open My Account', foot='Resolve immediately', pop=True),
    CK(icon='i', tone='m', title='Learn more', text='Launch offers end: monthly goes from £1 to £6.99; annual from £52 to £69.99 a year.', btn='Read about prices ↗', foot='Login not required'),
    CK(icon='✕', tone='m', title='Cancel online', text='Turn off auto-renew in a few clicks. You keep access to the end of your period.', btn='Manage auto-renew', foot='Takes about 1 minute'),
], small=True) + '<div class="rule">✓ Cancel online is always an equal, visible choice. Alternatives sit next to it, never in front of it.</div>'

EXPRESS = dict(
    key='express', name='The Express', domain='express.co.uk', glow='rgba(0,51,160,.40)', concept_pdf='reChanneld-Express-Concept.pdf',
    launcher='Premium &amp; subscriber help',
    c_h1='The Express, exactly as it is.<br><em>Plus one front door</em> for Premium readers.',
    c_lead='No redesign. These are express.co.uk pages as they are today, with the standard reChanneld widget added and configured with the Express\'s own topics: Express Premium, print subscriptions and commenting.',
    s1_tag='Homepage', s1_h='“Go Premium”, Login and Register. But nothing called Help.',
    s1_sub='The Express header invites readers to subscribe, log in and register. Once they have, there\'s no visible way to get help. reChanneld adds one small button for subscribers. Nothing else moves.',
    s2_tag='Express Premium page', s2_h='From “Already a Premium member? Login” to real help.',
    s2_sub='Today existing members get a login button, and the FAQ starts “Not a Digital Subscriber yet?”. With reChanneld, members pick their product and need, and get the fastest fix first.',
    s2_top=(['⭐ Express Premium', '📰 Newspaper delivery or vouchers', '💬 Comments &amp; my account', '❓ Something else'], 0),
    s2_crumb='Express Premium', s2_subs=['Can\'t log in', 'Billing', 'Price after the offer', 'Commenting', 'Cancel'], s2_sel=0,
    s2_cards=[CK(icon='🔑', tone='k', title='Reset password', text='Get a log-in link by e-mail. Works on the Express app and website.', btn='Send log-in link', foot='Resolve immediately', pop=True),
              CK(icon='i', tone='m', title='Learn more', text='Signing in to Express Premium on each device, step by step.', btn='Read log-in help ↗', foot='Login not required'),
              CK(icon='✉️', tone='l', title='E-mail support', text='Still stuck? Our subscriptions team will help.', btn='Send a message', foot='Reply within 1 working day')],
    s2_h_px=880,
    s3_tag='Footer &amp; price steps', s3_h='More than 100 footer links. No “Contact Us”.',
    s3_sub='Express Premium launch offers start at £1, then step up to £6.99 a month, or from £52 to £69.99 a year. A “Price after the offer” topic explains it before the first renewals in early 2027, just as the new UK subscription rules start.',
    s3_html=scene3(express_left, express_right),
    s4_sub='On the Express app the widget opens as a stacked view. In the admin panel the Customer team sees widget loads, sessions, top topics and channels for the Express in real time.',
    ph_crumb='Express Premium', ph_subs=['Commenting', 'Can\'t log in', 'Billing'],
    ph_c1=CK(title='Set up my profile', text='Choose a display name to join comments and Q&amp;As with Express writers.', btn='Open my profile', foot='Resolve immediately', tone='k'),
    ph_c2=CK(title='Learn more', text='Community standards and how commenting works.', btn='Read help ↗', foot='Login not required', tone='m'),
    kpis=[('Widget loads', '58,900'), ('Sessions', '13,640'), ('Finished sessions', '11,410')],
    topics=[('Price after the offer', 86), ('Can\'t log in', 80), ('Commenting', 52), ('Paper didn\'t arrive', 40), ('Vouchers', 28)],
    chans=[('My Account', 86), ('Help articles', 60), ('E-mail', 28), ('Phone', 24)],
    cover_tag='Express Premium &amp; subscriber help · review, concept &amp; business case',
    cover_h1='Every Express<br>reader, to the <em>right place</em>,<br>first time.',
    cover_sub='How one reChanneld front door on express.co.uk can support Premium members and loyal print readers, explain the step from launch offers to full price, and get ready for the 2027 subscription rules.',
    salute='Dear George and the Reach Customer team,',
    letter='''<p>Express Premium is one of Reach's most ambitious subscription products: ad-lite reading, exclusive journalism, commenting and Q&amp;As with Express writers, events and a newsletter from the Editor. The launch offers are generous, with £1 for the first month or £1 a week for the first year.</p>
  <p>We looked at express.co.uk as a Premium member would. The header says “Go Premium”, “Login” and “Register”, but nothing says Help. The footer has more than 100 links and <b>no “Contact Us”</b>; the nearest are “How to Complain” and “Report a Tech Issue”. Existing members get a login button, and the FAQ is written for people who haven't subscribed yet.</p>
  <p>Next, launch offers step up to £6.99 a month or £69.99 a year. For annual members that happens in early 2027, the same months the new UK subscription rules take effect.</p>
  <p>reChanneld is a channel-strategy platform from Helsinki. Its plug-and-play widget asks readers what they need and shows the best channel: self-service first, with honest opening hours and waiting times. It sits on top of the pages and systems you already have.</p>''',
    inc1='express.co.uk reviewed as a Premium member: 8 findings and a scorecard.',
    inc3='Price-step timing, the 2027 rules, a value model and an 8-week pilot on the Express.',
    today_h='A campaigning brand turning loyal readers into members',
    today_lead='The Express has one of the UK\'s largest news audiences and a loyal print readership, and is now asking its readers to pay online.',
    facts=[('18.5 M', 'monthly audience (June 2025, up 31% year on year)'), ('£1', 'launch offers, then £6.99 a month or £69.99 a year'),
           ('93,865', 'Daily Express weekday print sale (Dec 2025, −20%)'), ('£29.99', 'a month for print by vouchers or home delivery (“save 62%”)')],
    timeline=[('2025', 'Google Discover referrals to Reach fall by almost half in the second half of the year.'),
              ('Early 2026', 'Express Premium launches, among Reach\'s first national paywalls alongside the Daily Record and Daily Star.'),
              ('Easter 2026', 'Ten Reach brands now sell subscriptions.'),
              ('Aug 2026', 'Reach passes 50,000 digital subscribers.'),
              ('Oct 2026', 'New weekly podcast “Royals Unscripted”, adding to the Daily Expresso video show.'),
              ('Jan 2027', 'UK subscription rules start. First annual Premium renewals at £69.99.')],
    means=[('Engaged members, more questions.', 'Commenting, Q&amp;As and events add account and community questions on top of log-in and billing.'),
           ('Generous offers, bigger steps.', '£1 → £6.99 a month and £52 → £69.99 a year need clear explanation to keep members.'),
           ('Loyal print readers.', 'Many prefer the phone, so honest phone routes with real hours stay in the mix.'),
           ('No contact route today.', 'Without “Contact Us”, questions end up in complaints or tech-issue forms.')],
    opp='give Express members a clear front door before the first price steps and renewals in early 2027.',
    src_today='Sources: Press Gazette and journalism.co.uk (Express Premium; audience and ABC data), InPublishing, Reach results; express.co.uk Premium page (3 Oct 2026).',
    ev_h='express.co.uk, seen by a Premium member',
    ev_lead='Screenshots taken on 3 October 2026.',
    ev_html='''<div class="grid2" style="grid-template-columns:1fr 1fr;gap:5mm">
    <figure style="border:1px solid var(--line);border-radius:3mm;overflow:hidden"><img src="img/b/express-price1.png" style="width:100%;display:block"><figcaption class="small" style="padding:2mm 3mm;background:var(--bg)"><b>Monthly offer.</b> £1 for the first month, then £6.99: a sevenfold step after month one.</figcaption></figure>
    <figure style="border:1px solid var(--line);border-radius:3mm;overflow:hidden"><img src="img/b/express-price2.png" style="width:100%;display:block"><figcaption class="small" style="padding:2mm 3mm;background:var(--bg)"><b>Annual offer.</b> £52 for the first year, then £69.99. Print £29.99 a month.</figcaption></figure>
  </div>
  <figure style="margin-top:5mm;border:1px solid var(--line);border-radius:3mm;overflow:hidden;position:relative"><div style="height:78mm;overflow:hidden;position:relative"><img src="img/b/express-footer.png" style="width:100%;display:block"><div class="hl" style="left:57.8%;top:48.8%;width:10.4%;height:3%"></div><div class="hl" style="left:57.8%;top:51.5%;width:12%;height:3%"></div></div><figcaption class="small" style="padding:2mm 3mm;background:var(--bg)"><b>Footer.</b> Over 100 links, from VPN deals to Black Friday, and no “Contact Us”. The only help-like links: “How to Complain” and “Report a Tech Issue”.</figcaption></figure>''',
    score=[('1/10', 'Finding help', RED), ('3/10', 'Help for members', RED), ('3/10', 'Price-step clarity', AMB), ('5/10', 'Print routes', AMB), ('8/10', 'Offer clarity', GRN)],
    findings=[('No “Contact Us” on express.co.uk', 't-red', 'Critical', 'More than 100 footer links, and none is a general contact route. Members fall back on complaints or tech-issue forms.', 'A “Premium &amp; subscriber help” button on every page, opening the widget.'),
              ('The header sells, but doesn\'t help', 't-red', 'Critical', '“Go Premium”, “Login” and “Register” are prominent. Help is missing.', 'Add the help button next to Login, without changing the header design.'),
              ('Existing members get only a login button', 't-red', 'High', '“Already a Premium member? Login” is the only route on the Premium page.', 'A members\' topic list: log-in, billing, price after the offer, commenting, cancel.'),
              ('Big steps after launch offers', 't-amb', 'High', '£1 → £6.99 a month after month one; £52 → £69.99 a year at the first renewal, in early 2027.', 'A “Price after the offer” topic, linked from reminder e-mails.'),
              ('The FAQ is written for non-subscribers', 't-amb', 'Medium', 'It opens with “Not a Digital Subscriber yet?”. Member questions aren\'t covered.', 'Member questions answered by the widget, with the FAQ kept for prospects.'),
              ('Community features create new questions', 't-amb', 'Medium', 'Enhanced commenting, Q&amp;As and events bring profile, moderation and access questions.', 'A “Comments &amp; my account” topic with clear self-service.'),
              ('Print readers need an honest phone route', 't-blue', 'Medium', 'Loyal print readers often prefer to call, but no subscriber number or hours are shown on the site.', 'Phone support card with today\'s hours and typical waiting time.'),
              ('No view of what members need', 't-blue', 'Low', 'Questions are scattered across complaints, tech issues and inboxes.', 'reChanneld analytics: topics and channels in real time.')],
    notes=[('“Premium &amp; subscriber help” button', 'on express.co.uk, next to the existing header. Findings 01 and 02.'),
           ('First question: which subscription?', 'Express Premium, newspaper delivery or vouchers, comments &amp; account, or something else.'),
           ('Members\' topics.', 'Can\'t log in, billing, price after the offer, commenting, cancel. Findings 03 and 05.'),
           ('“Most popular choice”.', 'Self-service first, e.g. “Send log-in link”, marked “Resolve immediately”.'),
           ('Footer evidence.', 'Over 100 links, no “Contact Us”. Finding 01.'),
           ('Price after the offer.', 'Explains £1 → £6.99 and £52 → £69.99, with cancel online as an equal choice. Finding 04.'),
           ('In the app.', 'Commenting → “Set up my profile”. Finding 06.'),
           ('Analytics.', 'Widget loads, sessions, top topics and channels for the Express. Finding 08.'),
           ('What changes:', 'no design changes, plug-and-play, live in a few days, GDPR compliant with no cookies.')],
    why_no='express.co.uk is a busy, well-known news site. reChanneld doesn\'t compete with it: it adds the missing member path on top, so it can go live in days.',
    cap2='Premium page with the widget open: Express Premium → Can\'t log in → Send log-in link',
    cap3='Footer evidence (no “Contact Us”), and a Price after the offer topic',
    tree=[('⭐ Express Premium', [('Can\'t log in', 'Self-service', 'g'), ('Billing', 'My Account', 'g'), ('Price after the offer', 'Article', 'b'), ('Events &amp; Q&amp;As', 'Article', 'b'), ('Cancel', 'Equal choice', 'y')]),
          ('📰 Newspaper delivery or vouchers', [('Paper didn\'t arrive', 'Self-service', 'g'), ('Vouchers', 'Self-service', 'g'), ('Payment or price', 'Article → phone', 'b'), ('Holiday stop', 'Self-service', 'g'), ('Cancel or change', 'Equal choice', 'y')]),
          ('💬 Comments &amp; my account', [('Set up my profile', 'Self-service', 'g'), ('A comment was removed', 'Community standards', 'b'), ('Newsletters', 'Preference centre', 'g')]),
          ('❓ Something else', [('A story or tip', 'Newsdesk form', 'b'), ('Complaint or correction', 'How to complain', 'b'), ('Technical issue', 'Report a tech issue', 'b'), ('Anything else', 'Contact form', 'y')])],
    template_note='The Express configuration can be copied to the Mirror, Daily Star, Daily Record and every Reach brand, with each brand\'s own wording and look.',
    ren_h='Early 2027: launch offers end, rules begin',
    ren_lead='Express Premium launch offers are generous. The steps that follow are fair, but large, and they land just as the new UK subscription rules start.',
    ren_table='''<table class="calc" style="width:100%;border-collapse:collapse"><tr><th>Plan</th><th>Launch offer</th><th>Then</th><th>Step</th></tr>
    <tr><td>Premium monthly</td><td>£1 first month</td><td><b>£6.99</b> a month</td><td>×7 after month one</td></tr>
    <tr><td>Premium annual</td><td>£52 first year (£1 a week)</td><td><b>£69.99</b> a year</td><td>+35% at first renewal</td></tr>
    <tr><td>Print (vouchers / delivery)</td><td>£29.99 a month</td><td>As advertised</td><td>Monthly</td></tr></table>''',
    ren_opts='switch plan, check what\'s included',
    ren_punch='members who understand what £6.99 or £69.99 buys stay, and those who want to leave can do so in a minute.',
    arpu_label='monthly plan', arpu='£83.88', ret_val='≈ £16,800',
    pilot_lead='Suggested scope: Express Premium members on express.co.uk and the Express app, live before the first annual renewals in early 2027.',
    pilot_where='express.co.uk (Premium page, account and footer) and in the Express app',
    kpis_pilot=[('Member contacts per 1,000 Premium members', 'Your data, before vs during'), ('Top topics and channels', 'reChanneld analytics'), ('Finished sessions', 'reChanneld analytics'),
                ('Complaints and tech-issue forms used for help', 'Your data, before vs during'), ('“Price after the offer” choices', 'reChanneld analytics'), ('Premium churn after month one', 'Your data')],
    video_h='“Welcome to Express Premium”: a 40-second onboarding video',
    video_lead='Most log-in, commenting and “what will I pay?” questions come early. A short welcome video in the confirmation e-mail and app shows how to sign in, set up a profile, and where to find help.',
    video=[('0:00–0:06', '🇬🇧 “Welcome to<br>Express Premium”', 'The Premium crest on a phone.', 'Welcome to Express Premium. Thank you for backing the Express.'),
           ('0:06–0:16', '📱💻 Sign in once<br>on each device', 'Phone, laptop and tablet each show the sign-in.', 'Sign in on each device, and fewer ads follow you.'),
           ('0:16–0:24', '💬 Comments · Q&amp;As<br>· events', 'Set up a profile and join a Q&amp;A.', 'Join the conversation with Express writers.'),
           ('0:24–0:32', '👋 “Hey, how may<br>we help you?”', 'The reChanneld widget: Can\'t log in → Send log-in link.', 'Any question? The help button sorts it in seconds.'),
           ('0:32–0:36', '📅 Your plan,<br>your price', 'Price after the offer topic.', 'See exactly what you\'ll pay next, any time.'),
           ('0:36–0:40', 'Express Premium<br>Help: one tap away', 'End card in Express blue.', 'Enjoy your Express.')],
    video_where='The Premium confirmation e-mail, the app\'s first launch, and the help page. A 15-second cut can run with reminders before offers end.',
)

# =========================================================== MEN
men_left = bb('manchestereveningnews.co.uk → reachsubs.co.uk') + (
    '<div style="padding:16px;display:grid;gap:12px;background:#f7f7f7">'
    '<div style="position:relative;background:#fff;border:1px solid #ddd;border-radius:10px;overflow:hidden"><div style="font:800 11px Plus Jakarta Sans;padding:6px 10px;background:#f0b800">1 · On the M.E.N subscribe page</div><img src="img/b/men-price.png" style="width:100%;display:block;margin-top:-250px"><div class="hl" style="left:262px;top:72px;width:92px;height:52px"></div></div>'
    '<div style="position:relative;background:#fff;border:1px solid #ddd;border-radius:10px;overflow:hidden"><div style="font:800 11px Plus Jakarta Sans;padding:6px 10px;background:#fcc14a">2 · At checkout on Reachsubs</div><img src="img/b/rs-offer.png" style="width:100%;display:block"><div class="hl" style="left:50px;top:74px;width:390px;height:46px"></div></div>'
    '</div>') + mk(5, 'left:-50px;top:200px') + (
    '<div style="padding:16px 22px;font:600 14px/1.5 Lato">The M.E.N page promises print at <b>£31.85 a month, “save 50%”</b>. The first voucher checkout we reached on Reachsubs, a separate site, offers <b>£57.33 a month, “10% off”</b>. Readers will ask why.</div>')
men_right = mk(6, 'right:-56px;top:20px') + widget('Get the paper', ['Vouchers', 'Home delivery', 'Postal', 'Print + digital'], 0, [
    CK(icon='🎟️', tone='k', title='Subscribe online', text='Choose M.E.N or M.E.N + Sunday, then your start date. Prices shown before you pay.', btn='See voucher offers', foot='Resolve immediately', pop=True),
    CK(icon='i', tone='m', title='Learn more', text='How vouchers work at your newsagent, and what\'s included with free digital edition access.', btn='Read about vouchers ↗', foot='Login not required'),
    CK(icon='📞', tone='l', title='Talk to us', text='Questions about which package suits you? Our subscriptions team can help.', btn='Call us', foot='Waiting time 5–10 minutes', hours='Open today 08:00 – 18:00'),
], small=True)

MEN = dict(
    key='men', name='Manchester Evening News', domain='manchestereveningnews.co.uk', glow='rgba(240,184,0,.30)', concept_pdf='reChanneld-MEN-Concept.pdf',
    launcher='Premium &amp; subscriber help',
    c_h1='The M.E.N, exactly as it is.<br><em>Plus one front door</em> for every subscriber.',
    c_lead='No redesign. These are manchestereveningnews.co.uk and Reachsubs pages as they are today, with the standard reChanneld widget added and configured with the M.E.N\'s own topics: Premium, print delivery and vouchers.',
    s1_tag='Homepage', s1_h='Buy a paper, funeral notices, jobs, public notices… and no Help.',
    s1_sub='The M.E.N top bar serves many local needs, but subscribers have nowhere to go. reChanneld adds one small button for Premium and print subscribers. Nothing else moves.',
    s2_tag='M.E.N Premium page', s2_h='One front door for Premium and print subscribers.',
    s2_sub='Today Premium lives on manchestereveningnews.co.uk while print subscriptions live on Reachsubs, a separate site. reChanneld asks which one the reader has, and sends them to the fastest fix, with an honest phone option.',
    s2_top=(['🐝 M.E.N Premium', '📰 Newspaper delivery or vouchers', '❓ Something else'], 1),
    s2_crumb='Newspaper delivery or vouchers', s2_subs=['Paper didn\'t arrive', 'Vouchers', 'Payment', 'Holiday stop', 'Cancel or change'], s2_sel=0,
    s2_cards=[CK(icon='👤', tone='k', title='My Account', text='Report a missed delivery on Reachsubs. We\'ll credit your account and let your newsagent know.', btn='Report missed paper', foot='Resolve immediately', pop=True),
              CK(icon='i', tone='m', title='Learn more', text='What happens when a paper is missed, and how credits and redeliveries work.', btn='Read delivery help ↗', foot='Login not required'),
              CK(icon='📞', tone='l', title='Phone support', text='Home delivery subscriptions team: 0333 202 8000.', btn='Call us', foot='Waiting time 5–10 minutes', hours='Open today 08:00 – 18:00')],
    s2_h_px=880,
    s3_tag='Print offers on two sites', s3_h='Two sites, two prices: the reader does the maths.',
    s3_sub='The M.E.N subscribe page and the Reachsubs checkout are run separately and show different print prices. reChanneld can turn “which paper subscription is right for me?” into a clear choice, with a person on hand.',
    s3_html=scene3(men_left, men_right),
    s4_sub='On the M.E.N app the widget opens as a stacked view. In the admin panel the Customer team sees widget loads, sessions, top topics and channels for the M.E.N in real time.',
    ph_crumb='M.E.N Premium', ph_subs=['Can\'t log in', 'Daily Briefing', 'Billing'],
    ph_c1=CK(title='Reset password', text='Get a log-in link by e-mail. Works on the M.E.N app and website.', btn='Send log-in link', foot='Resolve immediately', tone='k'),
    ph_c2=CK(title='Learn more', text='Signing in on each device, step by step.', btn='Read help ↗', foot='Login not required', tone='m'),
    kpis=[('Widget loads', '41,200'), ('Sessions', '9,860'), ('Finished sessions', '8,310')],
    topics=[('Paper didn\'t arrive', 84), ('Can\'t log in', 76), ('Which subscription?', 60), ('Renewal &amp; price', 48), ('Vouchers', 36)],
    chans=[('My Account', 82), ('Help articles', 58), ('Phone', 30), ('E-mail', 22)],
    cover_tag='M.E.N Premium &amp; subscriber help · review, concept &amp; business case',
    cover_h1='Every M.E.N<br>reader, to the <em>right place</em>,<br>first time.',
    cover_sub='How one reChanneld front door can connect M.E.N Premium and Reachsubs print subscribers, clear up print offers across two sites, and support the first annual Premium renewals from November 2026.',
    salute='Dear George and the Reach Customer team,',
    letter='''<p>The Manchester Evening News is where Reach's subscription story began: the first Reach brand behind a paywall, in November 2025, and the UK's largest local newsbrand with 12.6 million monthly readers. Its Premium product is clear and well made, with the Daily Briefing, Unmissable and expert Man Utd and Man City coverage.</p>
  <p>We looked at the M.E.N as a subscriber would. The top bar offers “Buy a paper”, funeral notices, jobs and public notices, but no Help. Premium lives on the M.E.N site; print lives on Reachsubs, a separate site with a different look. The M.E.N page advertises print at <b>£31.85 a month, “save 50%”</b>; the first voucher checkout we reached on Reachsubs offered <b>£57.33 a month, “10% off”</b>.</p>
  <p>And the first annual Premium members, who joined in November 2025, <b>renew next month</b>.</p>
  <p>reChanneld is a channel-strategy platform from Helsinki. Its plug-and-play widget asks readers what they need and shows the best channel: self-service first, with honest opening hours and waiting times. It sits on top of the sites and systems you already have.</p>''',
    inc1='The M.E.N and Reachsubs reviewed as a subscriber: 8 findings and a scorecard.',
    inc3='First renewals, the 2027 rules, a value model and an 8-week pilot on the M.E.N.',
    today_h='Reach\'s first paywall, and its template',
    today_lead='What works at the M.E.N is copied across Reach. That makes it the natural place to design subscriber help for every brand.',
    facts=[('12.6 M', 'monthly audience: the UK\'s largest local newsbrand (+14.6%)'), ('Nov 2025', 'M.E.N Premium launched: Reach\'s first paywall'),
           ('£4.99', 'a month after a £1 first month, or £39.99 a year'), ('£31.85', 'a month for print, as advertised on the M.E.N page')],
    timeline=[('Nov 2025', 'M.E.N Premium launches with an editor\'s letter from Sarah Lester; thousands sign up.'),
              ('Early 2026', 'Liverpool Echo, Wales Online, Chronicle Live and others follow the M.E.N model.'),
              ('Aug 2026', 'Reach passes 50,000 digital subscribers. Mirror North opens in Manchester.'),
              ('Sep 2026', '“Active engaged time” becomes Reach\'s north-star metric.'),
              ('Nov 2026', 'First annual M.E.N Premium members renew at £39.99.'),
              ('Jan 2027', 'UK subscription rules (DMCC Act) start: easy exit, cooling-off, reminders.')],
    means=[('Two customer bases, two sites.', 'Premium on manchestereveningnews.co.uk, print on Reachsubs. Readers don\'t know which to contact.'),
           ('Consistent offers matter.', 'Different print prices on two sites create questions, and distrust.'),
           ('Renewals start now.', 'The first annual members renew in November 2026.'),
           ('The template for Reach.', 'A help journey designed here can be copied to 25 brands.')],
    opp='design subscriber help on the M.E.N first, and copy it to every Reach brand.',
    src_today='Sources: Press Gazette (local audience 2026), InPublishing and journalism.co.uk (M.E.N Premium launch), Reach results; manchestereveningnews.co.uk and reachsubs.co.uk (3 Oct 2026).',
    ev_h='manchestereveningnews.co.uk and Reachsubs, seen by a subscriber',
    ev_lead='Screenshots taken on 3 October 2026, following the print subscription journey from the M.E.N site to checkout.',
    ev_html='''<div class="grid2" style="grid-template-columns:1fr 1fr;gap:5mm">
    <figure style="border:1px solid var(--line);border-radius:3mm;overflow:hidden"><img src="img/b/men-price.png" style="width:100%;display:block"><figcaption class="small" style="padding:2mm 3mm;background:var(--bg)"><b>1 · M.E.N subscribe page.</b> Premium £1 then £4.99, or £39.99 a year. Print: <b>£31.85 a month, “save 50%”</b>.</figcaption></figure>
    <div style="display:grid;gap:4mm">
      <figure style="border:1px solid var(--line);border-radius:3mm;overflow:hidden"><img src="img/b/rs-type.jpg" style="width:100%;display:block"><figcaption class="small" style="padding:2mm 3mm;background:var(--bg)"><b>2 · Reachsubs, a separate site.</b> Vouchers from £13.23 a week, delivery £14.73, postal £22.80 (“save 10%”).</figcaption></figure>
      <figure style="border:1px solid var(--line);border-radius:3mm;overflow:hidden"><img src="img/b/rs-offer.png" style="width:100%;display:block"><figcaption class="small" style="padding:2mm 3mm;background:var(--bg)"><b>3 · Checkout.</b> Vouchers: <b>£57.33 a month, “10% off”</b>; 3 months £171.99; 12 months £687.96.</figcaption></figure>
    </div>
  </div>
  <div class="box dark" style="margin-top:5mm"><p style="margin:0;font:700 9.8pt/1.45 'Plus Jakarta Sans'">£31.85 and “save 50%” on the M.E.N page; £57.33 and “10% off” at the first checkout we reached. <span style="color:var(--teal)">The packages may differ, but the reader can't tell, and that's when they call, or leave.</span></p></div>''',
    score=[('2/10', 'Finding help', RED), ('3/10', 'One journey across sites', RED), ('3/10', 'Print offer clarity', AMB), ('6/10', 'Premium clarity', AMB), ('8/10', 'Premium value story', GRN)],
    findings=[('No Help in the M.E.N navigation', 't-red', 'Critical', 'The top bar offers Buy a paper, funeral notices, jobs, advertising, newsletters, public notices and offers. Subscribers have no route.', 'A “Premium &amp; subscriber help” button on every page, opening the widget.'),
              ('Print and Premium live on two different sites', 't-red', 'Critical', 'Premium is on the M.E.N site; print is on Reachsubs, with a different look and “Reach Publishing Services Ltd” in the footer.', 'One first question: “Which subscription do you have?”, then the right site.'),
              ('Print prices don\'t match across the journey', 't-red', 'High', '£31.85 a month “save 50%” on the M.E.N page; £57.33 a month “10% off” at the first voucher checkout we reached.', 'A “Get the paper” topic that explains packages and prices in one place.'),
              ('First annual Premium renewals arrive in November 2026', 't-amb', 'High', 'Members who joined at launch renew at £39.99. Price questions and cancellations peak now.', 'A “Renewal &amp; price” topic linked from reminder e-mails.'),
              ('The FAQ is for non-subscribers', 't-amb', 'Medium', '“Not a subscriber yet? … take a look below.” Member questions aren\'t covered.', 'Member questions answered by the widget, with the FAQ kept for prospects.'),
              ('Existing members get only a login button', 't-amb', 'Medium', '“Already a Premium member? Login” is the only route on the subscribe page.', 'A members\' topic list: log-in, Daily Briefing, billing, renewal, cancel.'),
              ('Print readers need an honest phone route', 't-blue', 'Medium', 'Reachsubs shows Home, FAQ and Contact links, but the M.E.N site gives no number or hours.', 'Phone support card with today\'s hours and typical waiting time.'),
              ('No shared view of subscriber needs', 't-blue', 'Low', 'Premium and print contacts are handled in different places.', 'reChanneld analytics across both journeys.')],
    notes=[('“Premium &amp; subscriber help” button', 'on manchestereveningnews.co.uk. The site stays as it is. Finding 01.'),
           ('First question: which subscription?', 'M.E.N Premium, newspaper delivery or vouchers, or something else. Finding 02.'),
           ('Print topics.', 'Paper didn\'t arrive, vouchers, payment, holiday stop, cancel or change.'),
           ('Honest phone option.', 'Today\'s hours and typical waiting time on the phone card. Finding 07.'),
           ('Evidence across two sites.', 'M.E.N page vs Reachsubs checkout prices. Finding 03.'),
           ('“Get the paper”.', 'Vouchers, delivery, postal or print + digital, explained in one place, with a person on hand.'),
           ('In the app.', 'Premium log-in help. Findings 05 and 06.'),
           ('Analytics.', 'Widget loads, sessions, top topics and channels for the M.E.N. Finding 08.'),
           ('What changes:', 'no design changes, plug-and-play, live in a few days, GDPR compliant with no cookies.')],
    why_no='The M.E.N site and Reachsubs both work. reChanneld doesn\'t replace either: it adds one front door on top and sends each reader to the right one, so it can go live in days.',
    cap2='Premium page with the widget open: Newspaper delivery → Paper didn\'t arrive → Report missed paper',
    cap3='Print offers across two sites, and a Get the paper topic that explains them in one place',
    tree=[('🐝 M.E.N Premium', [('Can\'t log in', 'Self-service', 'g'), ('Daily Briefing &amp; app', 'Guide', 'b'), ('Billing', 'My Account', 'g'), ('Renewal &amp; price', 'My Account', 'g'), ('Cancel', 'Equal choice', 'y')]),
          ('📰 Newspaper delivery or vouchers', [('Paper didn\'t arrive', 'Reachsubs account', 'g'), ('Vouchers', 'Reachsubs account', 'g'), ('Payment or price', 'Article → phone', 'b'), ('Holiday stop', 'Self-service', 'g'), ('Cancel or change', 'Equal choice', 'y')]),
          ('🛒 Get the paper', [('Vouchers', 'Reachsubs', 'g'), ('Home delivery', 'Reachsubs', 'g'), ('Postal', 'Reachsubs', 'g'), ('Print + digital', 'Talk to us', 'y')]),
          ('❓ Something else', [('A story or tip', 'Newsdesk form', 'b'), ('Funeral &amp; public notices', 'Notices pages', 'b'), ('Advertising', 'Book an ad', 'b'), ('Complaint', 'How to complain', 'b')])],
    template_note='The M.E.N was Reach\'s first paywall. Its configuration can be copied to the Liverpool Echo, Wales Online, Chronicle Live and every Reach brand.',
    ren_h='November 2026: the first M.E.N renewals',
    ren_lead='Annual members who joined at launch in November 2025 renew next month. Monthly members already moved from £1 to £4.99. How these moments are handled sets churn for the year ahead.',
    ren_table='''<table class="calc" style="width:100%;border-collapse:collapse"><tr><th>Plan</th><th>Offer</th><th>Then</th><th>Renewal moment</th></tr>
    <tr><td>Premium monthly</td><td>£1 first month</td><td><b>£4.99</b> a month</td><td>After month one</td></tr>
    <tr><td>Premium annual</td><td>£39.99 a year</td><td>£39.99 a year</td><td><b>From November 2026</b></td></tr>
    <tr><td>Print (vouchers)</td><td>£31.85 a month on M.E.N</td><td>£57.33 a month at checkout</td><td>Monthly</td></tr></table>''',
    ren_opts='switch to annual, check what\'s included',
    ren_punch='members who see what Premium gives them renew, and those who want to leave can do so in a minute.',
    arpu_label='annual plan', arpu='£39.99', ret_val='≈ £8,000',
    pilot_lead='Suggested scope: the M.E.N site and app plus the Reachsubs M.E.N pages, starting with the November 2026 renewals. The M.E.N then becomes the template for every Reach brand.',
    pilot_where='manchestereveningnews.co.uk, the M.E.N app and the Reachsubs M.E.N pages',
    kpis_pilot=[('Subscriber contacts per 1,000 subscribers', 'Your data, before vs during'), ('Top topics and channels', 'reChanneld analytics'), ('Finished sessions', 'reChanneld analytics'),
                ('Missed-paper contacts by phone', 'Your data, before vs during'), ('Renewal-topic choices', 'reChanneld analytics'), ('Annual renewal rate', 'Your data')],
    video_h='“Welcome to M.E.N Premium”: a 40-second onboarding video',
    video_lead='Most log-in and “where do I find…?” questions come in a member\'s first week. A short welcome video in the confirmation e-mail and app shows how to sign in, where the Daily Briefing lives, and where to find help.',
    video=[('0:00–0:06', '🐝 “Welcome to<br>M.E.N Premium”', 'The M.E.N bee on a phone.', 'Welcome to M.E.N Premium. Thanks for backing Manchester journalism.'),
           ('0:06–0:16', '📱💻 Sign in once<br>on each device', 'Phone, laptop and tablet each show the sign-in.', 'Sign in on each device, and fewer ads follow you.'),
           ('0:16–0:24', '☕ Daily Briefing<br>· Unmissable', 'Morning briefing in the app.', 'Your Daily Briefing, Unmissable and expert United and City insight.'),
           ('0:24–0:32', '👋 “Hey, how may<br>we help you?”', 'The reChanneld widget: Can\'t log in → Send log-in link.', 'Any question? The help button sorts it in seconds.'),
           ('0:32–0:36', '📅 Your plan,<br>your choice', 'Renewal &amp; price topic.', 'Check your renewal or change your plan, any time.'),
           ('0:36–0:40', 'M.E.N Premium<br>Help: one tap away', 'End card in M.E.N yellow.', 'Enjoy your M.E.N.')],
    video_where='The Premium confirmation e-mail, the M.E.N app\'s first launch, and the help page. A 15-second cut can run with the November renewal reminders.',
)

for B in (MIRROR, EXPRESS, MEN):
    B['video'] = [v + (VIDEO_BG[i],) for i, v in enumerate(B['video'])]
BRANDS = [MIRROR, EXPRESS, MEN]
