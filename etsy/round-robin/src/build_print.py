"""Builds the printable Draw Sheets and the Read Me First guide (HTML). Run: python3 build_print.py"""
from pathlib import Path

FONTS = ("https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,700;0,9..144,800;"
         "1,9..144,400&family=Barlow+Semi+Condensed:wght@500;600;700&display=swap")

CSS = """
@page { size: 8.5in 11in; margin: 0; }
* { box-sizing: border-box; margin: 0; padding: 0; }
:root { --paper: #FBF6EA; --cream: #EBDDBC; --green: #1F6B3B; --navy: #1B2B4B; --red: #C2412D; --hair: #D8C9A5; --soft: #E8DCBF; }
html, body { background: var(--paper); -webkit-print-color-adjust: exact; print-color-adjust: exact; }
body { font-family: 'Barlow Semi Condensed', sans-serif; color: var(--navy); }
.page { width: 816px; height: 1056px; padding: 0 56px 48px; position: relative; overflow: hidden; background: var(--paper);
  display: flex; flex-direction: column; break-after: page; }
.page:last-child { break-after: auto; }
.awning { height: 46px; margin: 0 -56px 30px; background: repeating-linear-gradient(90deg, var(--green) 0 34px, var(--paper) 34px 68px); position: relative; }
.awning::after { content: ""; position: absolute; left: 0; right: 0; top: 46px; height: 17px;
  background: radial-gradient(circle at 17px 0, var(--green) 16.5px, transparent 17px) 0 0 / 68px 17px repeat-x; }
.kicker { font-size: 11px; letter-spacing: 3px; text-transform: uppercase; color: var(--red); font-weight: 700; }
h1 { font-family: 'Fraunces', serif; font-weight: 800; font-size: 40px; letter-spacing: -1px; line-height: 1.05; margin: 6px 0 4px; }
h1 em { font-weight: 400; color: var(--red); }
.rule { height: 6px; margin: 12px 0 18px; background: linear-gradient(to bottom, var(--green) 0 2px, transparent 2px 4px, var(--red) 4px 6px); }
.fields { display: flex; gap: 18px; margin-bottom: 18px; }
.fields div { flex: 1; font-size: 10px; letter-spacing: 2px; text-transform: uppercase; font-weight: 700; color: var(--green); }
.fields div span { display: block; border-bottom: 1.5px solid var(--navy); height: 22px; }
table { width: 100%; border-collapse: collapse; }
th { background: var(--green); color: #F6EDD9; font-size: 10px; letter-spacing: 1.5px; text-transform: uppercase; font-weight: 700; padding: 6px 4px; border: 1px solid var(--green); }
td { border: 1px solid var(--hair); height: 30px; text-align: center; font-size: 13px; }
td.name { text-align: left; padding-left: 8px; width: 150px; }
td.num { width: 30px; font-weight: 700; color: var(--green); background: #F4EAD3; }
td.x { background: repeating-linear-gradient(45deg, var(--navy) 0 2px, #F4EAD3 2px 7px); }
.note { font-family: 'Fraunces', serif; font-style: italic; font-size: 13px; color: #6B6250; margin-top: 12px; }
.box { border: 1.5px solid var(--navy); padding: 14px 16px; }
.lbl { font-size: 10px; letter-spacing: 2.5px; text-transform: uppercase; font-weight: 700; color: var(--red); margin-bottom: 8px; display: block; }
.rungs { display: grid; grid-template-columns: 1fr 1fr; grid-template-rows: repeat(10, auto); grid-auto-flow: column; gap: 0 26px; }
.rung { display: flex; align-items: flex-end; height: 50px; border-bottom: 1px solid var(--hair); }
.rung b { font-family: 'Fraunces', serif; font-weight: 800; font-size: 20px; width: 40px; color: var(--green); }
.pairs { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
.pairs table td { height: 32px; font-size: 15px; font-weight: 600; }
.foot { margin-top: auto; padding-top: 14px; font-size: 10px; letter-spacing: 3px; text-transform: uppercase; color: var(--green); text-align: center; font-weight: 700; }
.prose p { font-family: 'Fraunces', serif; font-size: 15px; line-height: 1.55; margin-bottom: 10px; }
.prose p.lead { font-size: 19px; font-style: italic; color: var(--green); }
.steps { display: grid; grid-template-columns: 1fr 1fr; gap: 14px; margin: 6px 0 16px; }
.steps div { border: 1.5px solid var(--navy); padding: 14px; }
.steps h4 { font-family: 'Fraunces', serif; font-weight: 800; font-size: 17px; margin-bottom: 6px; }
.steps h4 em { color: var(--red); font-weight: 400; margin-right: 6px; }
.steps p { font-size: 13.5px; line-height: 1.45; }
"""


def page(kicker, title, body, foot="Every point tells you something"):
    return (f'<section class="page"><div class="awning"></div><div class="kicker">{kicker}</div><h1>{title}</h1>'
            f'<div class="rule"></div>{body}<div class="foot">{foot}</div></section>')


def fields(*names):
    return '<div class="fields">' + "".join(f"<div>{n}<span></span></div>" for n in names) + "</div>"


def score_grid(n):
    head = "<tr><th></th><th>Player</th>" + "".join(f"<th>{j}</th>" for j in range(1, n + 1)) + \
           "<th>Won</th><th>Lost</th><th>Games</th><th>Pts</th><th>Pos</th></tr>"
    rows = "".join(
        f'<tr><td class="num">{i}</td><td class="name"></td>'
        + "".join('<td class="x"></td>' if i == j else "<td></td>" for j in range(1, n + 1))
        + "<td></td>" * 5 + "</tr>" for i in range(1, n + 1))
    cols = '<col style="width:28px"><col style="width:118px">' + "<col>" * n + '<col style="width:38px">' * 5
    return f'<table style="table-layout:fixed"><colgroup>{cols}</colgroup>{head}{rows}</table>'


def grid_page(n):
    body = fields("Event", "Date", "Courts", "Format")
    body += score_grid(n).replace("<td", f'<td style="height:{68 if n <= 8 else 47}px"')
    body += ('<p class="note">Write each score in the row player&rsquo;s line, their games first (6&ndash;4). '
             'Shade the box for a win. Points: a win counts 1, a tie &frac12;, unless your event says otherwise.</p>')
    return page("Round robin · draw sheet", f"Score Grid <em>&middot; up to {n} players</em>", body)


def schedule_page():
    rows = "".join("<tr>" + "<td></td>" * 6 + "</tr>" for _ in range(24))
    body = fields("Event", "Date", "Start time")
    body += ('<table><tr><th style="width:60px">Round</th><th style="width:60px">Court</th><th>Player / team A</th>'
             '<th style="width:80px">Score</th><th>Player / team B</th><th style="width:110px">Winner</th></tr>'
             f'{rows}</table>')
    body += '<p class="note">Use the pairing charts on the next page to fill in who plays whom.</p>'
    return page("Round robin · draw sheet", "Match <em>Schedule</em>", body)


def circle(n):
    """Pairings by player number for every round (circle method). Odd n gets a bye seat."""
    m = n + n % 2
    rounds = []
    for r in range(m - 1):
        pairs = [(r, m - 1)] + [((r + k) % (m - 1), (r - k) % (m - 1)) for k in range(1, m // 2)]
        rounds.append([(a + 1, b + 1) for a, b in pairs])
    return rounds


def pairs_page():
    blocks = ""
    for n in (4, 6, 8):
        rows = "".join(f"<tr><td class='num'>{r + 1}</td>" + "".join(f"<td>{a} v {b}</td>" for a, b in rnd) + "</tr>"
                       for r, rnd in enumerate(circle(n)))
        heads = "".join(f"<th>Court {c}</th>" for c in range(1, n // 2 + 1))
        blocks += (f'<div><span class="lbl">{n - 1} or {n} players</span>'
                   f'<table><tr><th>Rd</th>{heads}</tr>{rows}</table></div>')
    body = '<div class="pairs" style="grid-template-columns:0.55fr 0.8fr 1.05fr;align-items:start">' + blocks + "</div>"
    rows = "".join(f"<tr><td class='num'>{r + 1}</td>" + "".join(f"<td>{a} v {b}</td>" for a, b in rnd) + "</tr>"
                   for r, rnd in enumerate(circle(10)))
    heads = "".join(f"<th>Court {c}</th>" for c in range(1, 6))
    body += (f'<div class="pairs" style="grid-template-columns:1fr;margin-top:22px"><div><span class="lbl">9 or 10 players</span>'
             f'<table><tr><th>Rd</th>{heads}</tr>{rows}</table></div></div>')
    body += ('<div class="box" style="margin-top:24px"><span class="lbl">How to use</span>'
             '<p class="note" style="margin:0">Number your players 1, 2, 3&hellip; Each round, the pairs in that row play. '
             'Everyone meets everyone once. With an odd number of players, whoever is drawn against the missing '
             'highest number rests that round (for 7 players, anyone drawn against 8 has a bye).</p></div>')
    return page("Round robin · draw sheet", "Pairing <em>Charts</em>", body)


def ladder_page():
    rungs = "".join(f'<div class="rung"><b>{i}</b></div>' for i in range(1, 21))
    body = fields("Ladder name", "Season")
    body += f'<div class="rungs">{rungs}</div>'
    body += ('<div class="box" style="margin-top:22px"><span class="lbl">Suggested rules</span>'
             '<p class="note" style="margin:0">You may challenge anyone up to three places above you. Matches are played '
             'within seven days of the challenge. If the challenger wins, they take the defender&rsquo;s place and '
             'everyone in between moves down one. If the defender wins, the ladder stays the same.</p></div>')
    return page("Season ladder · draw sheet", "Challenge <em>Ladder</em>", body)


def guide():
    p1 = ('<div class="prose"><p class="lead">Thank you for choosing the Round Robin &amp; Ladder Organizer. '
          'It takes the paperwork out of running social tennis, leagues and club ladders.</p></div>'
          '<div class="box" style="margin-bottom:16px"><span class="lbl">What&rsquo;s included</span>'
          '<p style="font-size:14.5px;line-height:1.6"><b>Round Robin &amp; Ladder Organizer</b> &mdash; Excel file that also works '
          'in Google Sheets and Apple Numbers<br><b>Draw Sheets</b> &mdash; printable score grids, schedule, pairing charts '
          'and a ladder board<br><b>This guide</b> &mdash; setup steps and tips</p></div>'
          '<div class="steps">'
          '<div><h4><em>i.</em>Setup</h4><p>Name your event, enter the number of courts and the points for a win or tie, '
          'then list up to 16 players or doubles teams from the top, with no gaps.</p></div>'
          '<div><h4><em>ii.</em>Schedule</h4><p>The full schedule builds itself: everyone meets everyone once, with court '
          'numbers. With an odd number of players, one player rests each round.</p></div>'
          '<div><h4><em>iii.</em>Scores</h4><p>Type the games each side won, for example 6 and 4. '
          'The winner, standings and results grid all update instantly.</p></div>'
          '<div><h4><em>iv.</em>Standings</h4><p>Players are ranked by points, then game difference, then games won. '
          'Print the standings for the noticeboard.</p></div></div>'
          '<div class="box"><span class="lbl">Before your first event</span><p style="font-size:14.5px;line-height:1.6">'
          'The sample players and scores show how everything works. Clear the cream cells on Setup, the Games columns '
          'on Schedule, and the Ladder and Challenges tabs, then add your own.</p></div>')
    p1 += ('<div style="margin-top:16px"><span class="lbl">Round robin sizes at a glance</span>'
           '<table><tr><th>Players</th><th>Rounds</th><th>Matches</th><th>Courts for no waiting</th>'
           '<th>Time with 25-minute rounds</th></tr><tr><td>4</td><td>3</td><td>6</td><td>2</td><td>about 1 h 15 min</td></tr><tr><td>5</td><td>5</td><td>10</td><td>2</td><td>about 2 h 05 min</td></tr><tr><td>6</td><td>5</td><td>15</td><td>3</td><td>about 2 h 05 min</td></tr><tr><td>8</td><td>7</td><td>28</td><td>4</td><td>about 2 h 55 min</td></tr><tr><td>10</td><td>9</td><td>45</td><td>5</td><td>about 3 h 45 min</td></tr><tr><td>12</td><td>11</td><td>66</td><td>6</td><td>about 4 h 35 min</td></tr><tr><td>16</td><td>15</td><td>120</td><td>8</td><td>about 6 h 15 min</td></tr></table></div>')
    p2 = ('<div class="steps">'
          '<div><h4><em>i.</em>Google Sheets</h4><p>Upload the .xlsx file to Google Drive, open it, then choose '
          'File &rsaquo; Save as Google Sheets.</p></div>'
          '<div><h4><em>ii.</em>Excel &amp; Numbers</h4><p>Open the file directly. Everything works in Microsoft Excel '
          'and Apple Numbers.</p></div>'
          '<div><h4><em>iii.</em>Ladder</h4><p>List players in starting order on the Ladder tab. Log each challenge on '
          'the Challenges tab: pick the challenger, the defender and who won. The live ladder updates by itself.</p></div>'
          '<div><h4><em>iv.</em>Paper days</h4><p>Print the Draw Sheets PDF for events without a laptop. The pairing '
          'charts tell you who plays whom in every round.</p></div></div>'
          '<div class="box" style="margin-bottom:16px"><span class="lbl">Tips for great round robins</span>'
          '<p style="font-size:14.5px;line-height:1.6">Short formats keep everyone moving: one set to 6, a pro set to 8, '
          'or timed rounds of 20&ndash;25 minutes with the score as it stands. In timed rounds a tie is fine &mdash; '
          'set the points for a tie on the Setup tab. If players change after scores are entered, clear the scores first.</p></div>'
          '<div class="steps" style="margin-bottom:0">'
          '<div><h4>Need help?</h4><p>Send me a message on Etsy and I&rsquo;ll reply as soon as I can. If you enjoy the '
          'organizer, a review helps a small studio more than you know.</p></div>'
          '<div><h4>Terms of use</h4><p>For use by the buyer, their club or their team. Please don&rsquo;t share, resell '
          'or redistribute the files. Not affiliated with any tennis tournament, tour or governing body.</p></div></div>')
    return page("Read me first", "Thank <em>you</em>", p1) + page("Read me first", "Quick <em>tips</em>", p2)


def html(pages):
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>Round Robin Organizer</title>'
            f'<link rel="stylesheet" href="{FONTS}"><style>{CSS}</style></head><body>{"".join(pages)}</body></html>')


here = Path(__file__).parent
(here / "draw-sheets.html").write_text(html([grid_page(8), grid_page(12), schedule_page(), pairs_page(), ladder_page()]))
(here / "guide.html").write_text(html([guide()]))
print("draw-sheets.html, guide.html")
