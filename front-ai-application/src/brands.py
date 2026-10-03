"""Generate reChanneld concept page + proposal pack for Mirror, Express and MEN."""
import html

SCR = '/tmp/claude-0/-home-user-main/8841ce66-6ddd-5dbc-87d4-373a29e45e36/scratchpad/'
C_STYLE = open(SCR + 'c-style.html').read()
P_STYLE = open(SCR + 'p-style.html').read()
SC = 1200 / 1748  # screenshot scale in concept page


def card(c, small=False):
    badge = '<span class="badge"><i>✓</i>Most popular choice</span>' if c.get('pop') else ''
    hours = f'<div class="oh">{c["hours"]}</div>' if c.get('hours') else ''
    pad = ' style="padding:24px 10px 12px"' if small else ''
    fs = (lambda a, b: f' style="font-size:{b if small else a}"')
    return (f'<div class="cd"{pad}>{badge}<div class="ico {c["tone"]}">{c["icon"]}</div>'
            f'<div class="ct"{fs("17px","15px")}>{c["title"]}</div><div class="cx"{fs("12px","11px")}>{c["text"]}</div>{hours}'
            f'<div class="btn {c["tone"]}"{fs("12.5px","11.5px")}>{c["btn"]}</div><div class="ft"{fs("11.5px","10.5px")}>{c["foot"]}</div></div>')


def widget(crumb, subs, sel, cards, top=None, small=False, style=''):
    t = ''
    if top:
        t = '<div class="subs" style="margin-bottom:16px">' + ''.join(
            f'<span class="sp{" on" if i == top[1] else ""}">{x}</span>' for i, x in enumerate(top[0])) + '</div><div style="border-top:1px solid #eee;padding-top:16px">'
    s = ''.join(f'<span class="sp{" on" if i == sel else ""}">{x}</span>' for i, x in enumerate(subs))
    hd = 'font-size:20px' if small else ''
    out = (f'<div class="rw" style="{style}"><div class="hd" style="{hd}">👋 Hey, how may we help you?</div>'
           f'<div class="sb">Select the option that best describes your need, and we\'ll assist you to the best service channel.</div>{t}'
           f'<div class="crumb"><span class="cb">‹ Back</span><span class="cb on">↺ {crumb}</span></div>'
           f'<div class="subs" style="margin-bottom:22px">{s}</div><div class="cards">{"".join(card(c, small) for c in cards)}</div>')
    if top:
        out += '</div>'
    return out + '</div>'


def mk(n, pos):
    return f'<div class="mk" style="{pos}">{n}</div>'


def browser(url, img, inner='', h=None, extra=''):
    hs = f'height:{h}px;overflow:hidden;' if h else ''
    return (f'<div class="browser" {extra}><div class="bbar"><i></i><i></i><i></i><div class="url">{url}</div></div>'
            f'<div class="shot" style="{hs}"><img src="{img}">{inner}</div></div>')


def phone(brand, crumb, subs, c1, c2):
    sp = ''.join(f'<span class="sp{" on" if i == 0 else ""}" style="font-size:9.5px;padding:4px 9px">{x}</span>' for i, x in enumerate(subs))
    def mini(c, pop):
        b = '<span class="badge" style="font-size:8.5px"><i>✓</i>Most popular choice</span>' if pop else ''
        return (f'<div class="cd" style="padding:16px 12px 10px;margin-bottom:12px">{b}<div class="ct" style="font-size:13px;margin-bottom:4px">{c["title"]}</div>'
                f'<div class="cx" style="font-size:9.5px;min-height:0">{c["text"]}</div><div class="btn {c["tone"]}" style="font-size:10px;padding:7px;margin-top:8px">{c["btn"]}</div><div class="ft" style="font-size:9px">{c["foot"]}</div></div>')
    return (f'<div class="phone" style="height:560px;width:270px"><div class="rw" style="padding:14px 10px;border-radius:0;height:100%;overflow:hidden">'
            f'<div style="font:800 11px \'Plus Jakarta Sans\';color:#999;margin-bottom:6px">{brand} · app</div>'
            f'<div class="hd" style="font-size:15px">👋 Hey, how may we help you?</div><div class="sb" style="font-size:9.5px;margin:4px 0 10px">Select the option that best describes your need, and we\'ll assist you to the best service channel.</div>'
            f'<div class="crumb" style="gap:5px;margin-bottom:8px"><span class="cb" style="font-size:9.5px;padding:4px 9px">‹ Back</span><span class="cb on" style="font-size:9.5px;padding:4px 9px">↺ {crumb}</span></div>'
            f'<div class="subs" style="gap:5px;margin-bottom:14px">{sp}</div>{mini(c1, True)}{mini(c2, False)}</div></div>')


def analytics(brand, kpis, topics, chans):
    tb = lambda rows: ''.join(f'<div class="tb"><span>{a}</span><em><i style="width:{b}%"></i></em></div>' for a, b in rows)
    k = ''.join(f'<div style="border:1px solid #eee;border-radius:8px;padding:10px"><div style="font:600 10.5px \'Lato\';color:#777">{a}</div><b style="font:800 20px \'Plus Jakarta Sans\'">{b}</b></div>' for a, b in kpis)
    return (f'<div style="display:grid;grid-template-columns:150px 1fr;border-radius:22px;overflow:hidden">'
            f'<div style="background:#1e2128;color:#c9ccd4;padding:22px 16px;font:600 13px \'Lato\';line-height:2.4"><div>⌂ Overview</div><div>☰ Topics</div><div style="background:#2c313b;border-radius:6px;padding:0 8px;color:#fff">▤ Analytics</div><div>⚙ Settings</div></div>'
            f'<div style="padding:22px 24px;background:#fff"><div style="display:flex;justify-content:space-between;align-items:center"><span style="font:800 20px \'Plus Jakarta Sans\'">Analytics</span><span style="font:700 10.5px \'Lato\';color:#777;letter-spacing:.06em">{brand.upper()} · <b style="color:#111;background:#eee;padding:3px 6px;border-radius:4px">LAST MONTH</b></span></div>'
            f'<div style="font:600 11px \'Lato\';color:#777;margin:6px 0 14px">Illustrative data</div>'
            f'<div style="display:grid;grid-template-columns:repeat(3,1fr) 1.1fr;gap:10px;margin-bottom:16px">{k}<div style="border:1px solid #eee;border-radius:8px;padding:10px;display:flex;align-items:center;gap:8px"><div style="width:38px;height:38px;border-radius:50%;background:conic-gradient(#14c3a6 0 84%,#f39a3d 84% 100%);-webkit-mask:radial-gradient(circle,transparent 11px,#000 12px)"></div><div style="font:600 10px \'Lato\';color:#777">● Finished<br>● Unfinished</div></div></div>'
            f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:12px"><div style="border:1px solid #eee;border-radius:8px;padding:12px 14px"><div style="font:700 12px \'Lato\';margin-bottom:10px">Top topics</div>{tb(topics)}</div>'
            f'<div style="border:1px solid #eee;border-radius:8px;padding:12px 14px"><div style="font:700 12px \'Lato\';margin-bottom:10px">Top channels</div>{tb(chans)}</div></div></div></div>')


# ---------------------------------------------------------------- concept
def concept(B):
    k = B['key']
    s = []
    s.append(f'<div class="concept"><b>Concept</b>: reChanneld on the existing {B["domain"]}, prepared for Reach plc · October 2026 · Screenshots taken 3 Oct 2026 · Yellow numbers match the notes in the proposal</div>')
    s.append(f'<section class="top" style="background-image:radial-gradient(700px 400px at 90% 0%,{B["glow"]},transparent 60%),radial-gradient(700px 400px at 0% 100%,rgba(20,214,192,.22),transparent 60%)"><div class="wrap">'
             f'<div class="logo">RECHANNELD × {B["name"].upper()}</div><h1>{B["c_h1"]}</h1><p>{B["c_lead"]}</p>'
             f'<div class="pills"><span class="pill"><b>0</b> design changes</span><span class="pill"><b>Plug-and-play</b> widget</span><span class="pill">Live in <b>a few days</b></span><span class="pill">GDPR · <b>no cookies</b></span></div></div></section>')
    # scene 1
    launch = (mk(1, 'right:300px;bottom:34px') +
              f'<div class="launch" style="right:24px;bottom:26px"><div class="ic">💬</div><div>{B["launcher"]}<small>Sorted in 2 taps</small></div></div>')
    s.append(f'<section class="scene"><div class="wrap"><div class="sh"><span class="sn">Scene 1 · {B["s1_tag"]}</span></div><div class="h2">{B["s1_h"]}</div><div class="sub">{B["s1_sub"]}</div>'
             + browser(B['domain'], f'img/b/{k}-home.jpg', launch, h=820) + '</div></section>')
    # scene 2
    w2 = widget(B['s2_crumb'], B['s2_subs'], B['s2_sel'], B['s2_cards'], top=B.get('s2_top'),
                style='position:absolute;left:50%;top:50px;transform:translateX(-50%);width:880px;padding:30px 34px 26px;box-shadow:0 30px 80px rgba(0,0,0,.45)')
    marks = mk(2, 'left:110px;top:120px') + mk(3, 'left:110px;top:' + ('330' if B.get('s2_top') else '250') + 'px') + mk(4, 'right:110px;top:' + ('560' if B.get('s2_top') else '470') + 'px')
    s.append(f'<section class="scene"><div class="wrap"><div class="sh"><span class="sn">Scene 2 · {B["s2_tag"]}</span></div><div class="h2">{B["s2_h"]}</div><div class="sub">{B["s2_sub"]}</div>'
             + browser(f'{B["domain"]}/subscribe', f'img/b/{k}-sub.jpg', '<div class="dim"></div>' + w2 + marks, h=B.get('s2_h_px', 820)) + '</div></section>')
    # scene 3
    s.append(f'<section class="scene"><div class="wrap"><div class="sh"><span class="sn">Scene 3 · {B["s3_tag"]}</span></div><div class="h2">{B["s3_h"]}</div><div class="sub">{B["s3_sub"]}</div>'
             f'{B["s3_html"]}</div></section>')
    # scene 4
    p = phone(B['name'], B['ph_crumb'], B['ph_subs'], B['ph_c1'], B['ph_c2'])
    s.append(f'<section class="scene"><div class="wrap"><div class="sh"><span class="sn">Scene 4 · Mobile and analytics</span></div><div class="h2">Same help in the app. Live insight for the Customer team.</div>'
             f'<div class="sub">{B["s4_sub"]}</div><div style="display:grid;grid-template-columns:300px 1fr;gap:28px;align-items:start">'
             f'<div class="card" style="padding:20px;position:relative">{mk(7, "left:-56px;top:20px")}{p}</div>'
             f'<div class="card" style="padding:0;position:relative">{mk(8, "right:-56px;top:20px")}{analytics(B["name"], B["kpis"], B["topics"], B["chans"])}</div></div></div></section>')
    s.append('<section class="chg"><div class="wrap">' + mk(9, 'left:-50px;top:-6px') + f'<div class="h2">What changes on {B["domain"]}</div><div class="ctab">'
             '<div class="ct2"><span class="k">Design</span><b>Nothing</b><p>Your pages stay exactly as they are. The widget adapts to the site\'s design and typography.</p></div>'
             '<div class="ct2"><span class="k">Set-up</span><b>Plug-and-play</b><p>An easy-to-install widget for the website and app, with its own configuration for this brand.</p></div>'
             '<div class="ct2"><span class="k">Time to live</span><b>A few days</b><p>Topics and channels managed in the cloud admin panel by the Customer team, not IT.</p></div>'
             '<div class="ct2 add"><span class="k">Compliance</span><b>GDPR, no cookies</b><p>Audited for security and accessibility. Nothing to replace in your systems.</p></div></div></div></section>')
    s.append('<div class="foot">reChanneld · Better choices. Happier customers. · Concept for discussion: topics, wording, hours, waiting times and analytics figures are illustrative.</div>')
    head = f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>reChanneld on {B["name"]}</title>\n<link href="fonts.css" rel="stylesheet">\n{C_STYLE}{B.get("c_css","")}\n</head>\n<body>\n'
    return head + '\n'.join(s) + '\n</body>\n</html>\n'


# ---------------------------------------------------------------- proposal
def pf(B, n):
    return f'<div class="pf"><span><b>RECHANNELD</b> · for {B["name"]} (Reach plc)</span><span>{n}</span></div>'


def proposal(B):
    n = B['name']
    P = []
    P.append(f'''<div class="page cover reach" style="background-image:radial-gradient(150mm 120mm at 100% 0%,{B["glow"]},transparent 60%),radial-gradient(120mm 100mm at 0% 100%,rgba(20,214,192,.22),transparent 60%)">
  <div class="top"><span class="logo">RECHANNELD</span><span>Prepared for {n} · Reach plc · October 2026</span></div>
  <div class="pfor" style="margin-top:34mm">{B["cover_tag"]}</div>
  <h1>{B["cover_h1"]}</h1>
  <p class="sub">{B["cover_sub"]}</p>
  <div class="toc" style="grid-template-columns:repeat(4,1fr)">
    <div><b>01</b>Summary</div><div><b>02</b>{n} today</div><div><b>03</b>Subscriber journey audit</div><div><b>04</b>reChanneld on {B["domain"]}</div>
    <div><b>05</b>Topic map</div><div><b>06</b>Renewals &amp; 2027 rules</div><div><b>07</b>Business case &amp; pilot</div><div><b>+</b>Concept on your site (separate PDF)</div>
  </div>
  <div class="bot"><div><b>Touko Laakkonen</b><span>Service Channel Strategy · reChanneld</span></div><div class="tagl">Better choices.<br>Happier customers.</div></div>
</div>''')
    P.append(f'''<div class="page letter">
  <div class="kick">01 · Summary</div>
  <h2>{B["salute"]}</h2>
  {B["letter"]}
  <p>This pack contains:</p>
  <div class="three">
    <div class="box bg"><div class="num">1</div><h4 style="margin-top:2mm">Audit</h4><p class="small muted" style="margin:0">{B["inc1"]}</p></div>
    <div class="box bg"><div class="num">2</div><h4 style="margin-top:2mm">Concept</h4><p class="small muted" style="margin:0">The real reChanneld widget on {B["domain"]}, configured with {n}'s own topics. Nothing redesigned.</p></div>
    <div class="box bg"><div class="num">3</div><h4 style="margin-top:2mm">Business case</h4><p class="small muted" style="margin:0">{B["inc3"]}</p></div>
  </div>
  <p>We'd welcome 20 minutes with you or the subscriptions team to walk through it.</p>
  <p style="margin-top:4mm">Kind regards,</p>
  <div style="font:800 13pt 'Plus Jakarta Sans'">Touko Laakkonen</div>
  <p class="muted small">Service Channel Strategy, reChanneld · [e-mail] · [phone]</p>
  {pf(B,2)}
</div>''')
    facts = ''.join(f'<div class="fact"><b>{a}</b><span>{b}</span></div>' for a, b in B['facts'])
    tl = ''.join(f'<div><b>{a}</b>{b}</div>' for a, b in B['timeline'])
    means = ''.join(f'<li><b>{a}</b> {b}</li>' for a, b in B['means'])
    P.append(f'''<div class="page">
  <div class="kick">02 · {n} today</div>
  <h2>{B["today_h"]}</h2>
  <p class="lead">{B["today_lead"]}</p>
  <div class="facts" style="grid-template-columns:repeat(4,1fr);margin-bottom:5mm">{facts}</div>
  <div class="grid2">
    <div><h3>Timeline</h3><div class="tl">{tl}</div></div>
    <div><h3>What this means for subscriber help</h3><ul class="clean small">{means}</ul>
      <div class="box dark" style="margin-top:3mm"><p style="margin:0;font:700 9.8pt/1.45 'Plus Jakarta Sans'">The opportunity: <span style="color:var(--teal)">{B["opp"]}</span></p></div></div>
  </div>
  <p class="src" style="position:absolute;left:17mm;right:17mm;bottom:15mm">{B["src_today"]}</p>
  {pf(B,3)}
</div>''')
    P.append(f'''<div class="page">
  <div class="kick">03 · Subscriber journey audit</div>
  <h2 style="font-size:20pt">{B["ev_h"]}</h2>
  <p class="muted small" style="margin-bottom:4mm">{B["ev_lead"]}</p>
  {B["ev_html"]}
  {pf(B,4)}
</div>''')
    sc = ''.join(f'<div class="sc"><b style="color:{c}">{v}</b><span>{l}</span></div>' for v, l, c in B['score'])
    fd = ''.join(f'<div class="find"><div class="n">{i+1:02d}</div><div><h4>{h} <span class="tag {t}">{tl_}</span></h4><p>{p}</p><div class="fix">{fx}</div></div></div>'
                 for i, (h, t, tl_, p, fx) in enumerate(B['findings']))
    P.append(f'''<div class="page">
  <div class="kick">03 · Subscriber journey audit, continued</div>
  <h2 style="font-size:20pt">{len(B["findings"])} findings</h2>
  <div class="score" style="grid-template-columns:repeat(5,1fr)">{sc}</div>
  {fd}
  <p class="src" style="position:absolute;left:17mm;right:17mm;bottom:15mm">Reviewed on {B["domain"]} on 3 October 2026. Scores are our view.</p>
  {pf(B,5)}
</div>''')
    notes = ''.join(f'<div><span class="mkk">{i+1}</span><div><b>{a}</b> {b}</div></div>' for i, (a, b) in enumerate(B['notes']))
    P.append(f'''<div class="page">
  <div class="kick">04 · reChanneld on {B["domain"]}</div>
  <div style="display:grid;grid-template-columns:58mm 1fr;gap:7mm">
    <div style="height:250mm;overflow:hidden;border-radius:3mm;border:1px solid var(--line)"><img src="img/b/{B["key"]}-cfull.jpg" style="width:100%;display:block"></div>
    <div>
      <h2 style="font-size:19pt">Your pages, exactly as they are. Plus one front door.</h2>
      <p class="muted small">Screenshots of {B["domain"]} as it is today, with the standard reChanneld widget added and configured with {n}'s own topics. The full page is in <b>{B["concept_pdf"]}</b>, and each yellow number matches a note below.</p>
      <div class="notes" style="margin-top:3mm">{notes}</div>
      <div class="box bg" style="margin-top:4mm"><h4>Why no redesign</h4><p class="small" style="margin:0">{B["why_no"]}</p></div>
    </div>
  </div>
  {pf(B,6)}
</div>''')
    P.append(f'''<div class="page">
  <div class="kick">04 · Before and after</div>
  <h2 style="font-size:20pt">The same pages, a very different experience</h2>
  <figure style="margin-top:4mm;border-radius:3mm;overflow:hidden;border:1px solid var(--line)"><div style="height:120mm;overflow:hidden"><img src="img/b/{B["key"]}-scene2.jpg" style="width:100%;display:block"></div><figcaption style="font:800 7.3pt 'Plus Jakarta Sans';letter-spacing:.08em;text-transform:uppercase;padding:2mm 3mm;background:var(--ink);color:var(--teal)">{B["cap2"]}</figcaption></figure>
  <figure style="margin-top:5mm;border-radius:3mm;overflow:hidden;border:1px solid var(--line)"><div style="height:98mm;overflow:hidden"><img src="img/b/{B["key"]}-scene3.jpg" style="width:100%;display:block"></div><figcaption style="font:800 7.3pt 'Plus Jakarta Sans';letter-spacing:.08em;text-transform:uppercase;padding:2mm 3mm;background:var(--ink);color:var(--teal)">{B["cap3"]}</figcaption></figure>
  {pf(B,7)}
</div>''')
    tree = ''
    for title, rows in B['tree']:
        tree += f'<div class="tn"><b>{title}</b>' + ''.join(f'<div>{a} <span class="ch {c}">{b}</span></div>' for a, b, c in rows) + '</div>'
    P.append(f'''<div class="page">
  <div class="kick">05 · Topic map</div>
  <h2 style="font-size:20pt">Proposed starting configuration for {n}</h2>
  <p class="muted small" style="margin-bottom:4mm">First-level topics, sub-topics and the recommended channel for each. Built from public information; in a pilot, your own contact data decides the final structure and wording.</p>
  <div class="tree">{tree}</div>
  <div class="grid2" style="margin-top:5mm">
    <div class="box bg"><h4>Managed by the Customer team</h4><p class="small" style="margin:0">Topics, texts, buttons, hours and the “Most popular choice” are edited in reChanneld's cloud admin panel and change instantly, without IT tickets or releases.</p></div>
    <div class="box bg"><h4>One template, every Reach brand</h4><p class="small" style="margin:0">{B["template_note"]}</p></div>
  </div>
  {pf(B,8)}
</div>''')
    P.append(f'''<div class="page">
  <div class="kick">06 · Renewals &amp; 2027 rules</div>
  <h2>{B["ren_h"]}</h2>
  <p class="lead">{B["ren_lead"]}</p>
  {B["ren_table"]}
  <div class="grid2" style="margin-top:5mm">
    <div>
      <h3>UK subscription rules, from January 2027</h3>
      <ul class="clean small">
        <li><b>Easy exit.</b> Consumers can end a contract with a clear statement, without unnecessary steps.</li>
        <li><b>Cooling-off.</b> A 14-day cooling-off period at the start, and again after renewal.</li>
        <li><b>Reminders.</b> Notices before renewals and before a free or discounted period ends.</li>
      </ul>
      <p class="small muted">Summary of the DMCC Act 2024 subscription regime from public guidance, not legal advice.</p>
    </div>
    <div>
      <h3>How the widget helps</h3>
      <ul class="clean small">
        <li><b>Reminder e-mails link to a “Renewal &amp; price” topic,</b> so questions land in self-service, not in the inbox.</li>
        <li><b>Honest options side by side:</b> {B["ren_opts"]}, and cancel online, all as equal choices.</li>
        <li><b>Evidence:</b> analytics show how many readers chose each option, useful for the Customer team and for compliance.</li>
      </ul>
    </div>
  </div>
  <div class="box dark" style="margin-top:4mm"><p style="margin:0;font:700 9.8pt/1.45 'Plus Jakarta Sans'">Retention by service, not by friction: <span style="color:var(--teal)">{B["ren_punch"]}</span></p></div>
  {pf(B,9)}
</div>''')
    P.append(f'''<div class="page">
  <div class="kick">07 · Business case</div>
  <h2>A simple model to fill in together</h2>
  <p class="lead" style="margin-bottom:4mm">We don't know {n}'s subscriber or contact volumes, so this is a worked example per 10,000 subscribers, with clearly stated assumptions. In the first call we'd replace them with real figures.</p>
  <div class="grid2">
    <div>
      <table class="calc" style="width:100%;border-collapse:collapse">
        <tr><th>Per 10,000 subscribers</th><th class="rr">Example</th></tr>
        <tr><td>Contacts per subscriber per year</td><td class="rr">0.4</td></tr>
        <tr><td>Subscriber contacts per year</td><td class="rr">4,000</td></tr>
        <tr><td>Share moved to self-service by nudging</td><td class="rr">30%</td></tr>
        <tr><td>Contacts avoided per year</td><td class="rr">1,200</td></tr>
        <tr><td>Cost per assisted contact (reChanneld's ROI basis: €5)</td><td class="rr">≈ £4.30</td></tr>
        <tr class="tot"><td>Service saving per year</td><td class="rr" style="white-space:nowrap">≈ £5,200</td></tr>
        <tr><td>Subscribers kept at renewal (+2 percentage points)</td><td class="rr">200</td></tr>
        <tr><td>Value of a kept subscriber per year ({B["arpu_label"]})</td><td class="rr">{B["arpu"]}</td></tr>
        <tr class="tot"><td>Retained revenue per year</td><td class="rr" style="white-space:nowrap">{B["ret_val"]}</td></tr>
      </table>
    </div>
    <div>
      <h3>Where the value comes from</h3>
      <ul class="clean small">
        <li><b>Retention first.</b> At {n}'s prices, keeping subscribers at renewal is worth more than service savings.</li>
        <li><b>Fewer assisted contacts.</b> Log-in, billing and delivery questions move to self-service.</li>
        <li><b>Faster help for those who call.</b> Shorter queues for complex cases.</li>
        <li><b>Insight.</b> Real-time data on what readers need, for the Customer and product teams.</li>
      </ul>
      <div class="box bg" style="margin-top:3mm"><h4>reChanneld's own benchmark</h4><p class="small" style="margin:0">On reChanneld's published plans, ROI is reached by nudging around 5% of traffic, assuming €5 per contact. Clients typically see 79% of channel selections go to self-service, automation and leads.</p></div>
    </div>
  </div>
  <div class="box dark" style="margin-top:5mm"><p style="margin:0;font:700 9.8pt/1.45 'Plus Jakarta Sans'">Scale: <span style="color:var(--teal)">the same configuration can be copied to every Reach subscription brand (25 by October), so the value multiplies across a base heading for 75,000 digital subscribers.</span></p></div>
  {pf(B,10)}
</div>''')
    kp = ''.join(f'<tr><td>{a}</td><td>{b}</td></tr>' for a, b in B['kpis_pilot'])
    P.append(f'''<div class="page">
  <div class="kick">07 · 8-week pilot</div>
  <h2>Prove it on {n}, with your own data</h2>
  <p class="lead" style="margin-bottom:4mm">{B["pilot_lead"]}</p>
  <div class="steps" style="margin-bottom:6mm">
    <div class="st"><span>Weeks 1–2</span><b>Map</b><p>Review three months of {n} contact reasons, agree topics, channels and wording, and set the baseline. The widget itself can be live within days.</p></div>
    <div class="st"><span>Weeks 3–8</span><b>Guide</b><p>Widget live on {B["pilot_where"]}. Wording and recommended channels adjusted weekly from the analytics.</p></div>
    <div class="st"><span>Week 9</span><b>Decide</b><p>Review results together, then copy the configuration to the next Reach brands.</p></div>
  </div>
  <div class="grid2">
    <div><h3>What we'll measure</h3><table class="kpi" style="width:100%;border-collapse:collapse"><tr><th>KPI</th><th>How</th></tr>{kp}</table></div>
    <div><h3>Who does what</h3>
      <div class="box bg" style="margin-bottom:3mm"><h4>reChanneld</h4><ul class="clean small" style="margin:0"><li>Configuration, topics and copy</li><li>Analytics access and weekly check-ins</li><li>Final report and rollout plan</li></ul></div>
      <div class="box bg"><h4>Reach</h4><ul class="clean small" style="margin:0"><li>One Customer-team contact, about 2 hours a week</li><li>Contact-reason data and current help links</li><li>Adding the widget to the agreed pages</li></ul></div>
    </div>
  </div>
  <div class="box dark" style="margin-top:5mm"><p style="margin:0;font:700 9.8pt/1.45 'Plus Jakarta Sans'">No redesign, no new chatbot and no change to subscription platforms. <span style="color:var(--teal)">If it doesn't show results in 8 weeks, you stop.</span></p></div>
  {pf(B,11)}
</div>''')
    fr = ''.join(f'<div class="fr"><div class="scr" style="{bg}"><span class="tc">{tc}</span>{sc_}</div><div class="bd"><b>Visual</b><br>{v}<div class="vo">“{vo}”</div></div></div>' for tc, sc_, v, vo, bg in B['video'])
    P.append(f'''<div class="page">
  <div class="kick">07 · Launch support</div>
  <h2 style="font-size:20pt">{B["video_h"]}</h2>
  <p class="muted small" style="margin-bottom:4mm">{B["video_lead"]}</p>
  <div class="sb">{fr}</div>
  <div class="grid2" style="margin-top:6mm">
    <div class="box bg"><h4>Formats</h4><p class="small" style="margin:0">9:16 for the app and social, 16:9 for web, plus a GIF and a 15-second cut for e-mails. Captioned throughout.</p></div>
    <div class="box bg"><h4>Where it lives</h4><p class="small" style="margin:0">{B["video_where"]}</p></div>
  </div>
  {pf(B,12)}
</div>''')
    P.append(f'''<div class="page">
  <div class="kick">About reChanneld</div>
  <h2>Better choices. Happier customers. Lower costs.</h2>
  <div class="grid2" style="margin:3mm 0 5mm;grid-template-columns:1.15fr 1fr">
    <div><div style="border-radius:3mm;overflow:hidden;border:1px solid var(--line)"><img src="img/rech-widget.png" style="width:100%;display:block"></div>
      <p class="small muted" style="margin-top:1.6mm">The reChanneld widget as it works today: topic, sub-topic, channel cards and the “Most popular choice”.</p></div>
    <div>
      <p class="small">reChanneld is a channel strategy platform from Helsinki, Finland. A plug-and-play widget uses behavioural economics and digital nudges to guide customers to the best service channel. Customer service teams manage it themselves in a cloud admin panel, and it works on top of their existing website and channels.</p>
      <div class="facts" style="grid-template-columns:1fr 1fr;gap:2.4mm">
        <div class="fact"><b>4M+</b><span>annual sessions</span></div><div class="fact"><b>79%</b><span>channel selections to self-service, automation and leads</span></div>
        <div class="fact"><b>87%</b><span>of end users found reChanneld easy and clear</span></div><div class="fact"><b>Days</b><span>to define and implement a channel strategy</span></div>
      </div>
    </div>
  </div>
  <div class="grid2" style="margin-bottom:5mm">
    <div class="box bg"><p style="font:700 10pt/1.5 'Plus Jakarta Sans';margin-bottom:2mm">“Within just a few days we were able to nail our service channel strategy with reChanneld. Nudges work excellently, and we offer a far more intuitive experience to our customers than before!”</p><p class="small muted" style="margin:0">Teresa Alander, Head of Operations, Lippu.fi (part of CTS Eventim)</p></div>
    <div class="box"><h4>Used by</h4><p class="small" style="margin-bottom:2mm">S-Bank, Nets, Lippu.fi, PAM, Sportson, Laurea, Varha and Satakunta wellbeing services county. They cover banking, payments, ticketing, retail, education and the public sector.</p>
      <h4>Enterprise-ready</h4><p class="small" style="margin:0">Audited for security and accessibility, GDPR compliant, no cookies. White-labelled per brand. Enterprise plan with unlimited admin users and integrations.</p></div>
  </div>
  <div class="cta"><div><h3>Shall we take 20 minutes?</h3><p>We'd love to hear how {n} subscriber help works today, and where it hurts most.</p></div><div class="c">Touko Laakkonen<span>reChanneld · [e-mail] · [phone]</span></div></div>
  <p class="src" style="position:absolute;left:17mm;right:17mm;bottom:15mm">Figures, quote, plans and customer names from rechanneld.com (October 2026).</p>
  {pf(B,13)}
</div>''')
    head = f'<!doctype html>\n<html lang="en">\n<head>\n<meta charset="utf-8">\n<title>reChanneld for {n}</title>\n<link href="fonts.css" rel="stylesheet">\n{P_STYLE}\n</head>\n<body>\n'
    return head + '\n\n'.join(P) + '\n</body>\n</html>\n'
