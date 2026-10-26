"""Generates The Match Book tennis journal HTML. Run: python3 build.py [club|retro|clay|rally]"""
import sys
from pathlib import Path

MATCHES = 30
SCOUTS = 20
TRAIN_WEEKS = 12
DRILL_PAGES = 10
BODY_WEEKS = 6
COACH_PAGES = 6
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
THEME = sys.argv[1] if len(sys.argv) > 1 else "club"
FONTS = {
    "club": "family=Bodoni+Moda:ital,wght@0,400;0,500;1,400&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400"
            "&family=Montserrat:wght@400;500;600",
    "retro": "family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,700;0,9..144,800;1,9..144,400"
             "&family=Barlow+Semi+Condensed:wght@500;600;700",
    "clay": "family=DM+Serif+Display:ital@0;1&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400"
            "&family=Montserrat:wght@400;500;600",
    "rally": "family=Anton&family=Inter:wght@400;500;600;700",
}
FONT_URL = f"https://fonts.googleapis.com/css2?{FONTS[THEME]}&display=swap"


def ball(color="var(--brass)", sw=1.2):
    return (f'<svg viewBox="0 0 24 24" fill="none" stroke="{color}" stroke-width="{sw}">'
            '<circle cx="12" cy="12" r="10.5"/>'
            '<path d="M3.2 6.5c3.6 2.2 3.6 8.8 0 11"/><path d="M20.8 6.5c-3.6 2.2-3.6 8.8 0 11"/></svg>')


def court(stroke="var(--hair)", sw=0.28, net="var(--brass)"):
    # Doubles court 36ft x 78ft, top-down, with singles sidelines, service boxes and centre marks.
    return (f'<svg viewBox="-3 -3 42 84" fill="none" stroke="{stroke}" stroke-width="{sw}" '
            'preserveAspectRatio="xMidYMid meet">'
            '<rect x="0" y="0" width="36" height="78"/>'
            '<line x1="4.5" y1="0" x2="4.5" y2="78"/><line x1="31.5" y1="0" x2="31.5" y2="78"/>'
            '<line x1="4.5" y1="18" x2="31.5" y2="18"/><line x1="4.5" y1="60" x2="31.5" y2="60"/>'
            '<line x1="18" y1="18" x2="18" y2="60"/>'
            '<line x1="18" y1="0" x2="18" y2="1"/><line x1="18" y1="77" x2="18" y2="78"/>'
            f'<line x1="-2" y1="39" x2="38" y2="39" stroke="{net}" stroke-width="{sw * 1.8}"/></svg>')


TABS = [("season", "Season", "season"), ("results", "Results", "results"), ("matches", "Matches", "matches"),
        ("scout", "Scout", "scouting"), ("train", "Train", "train-1"), ("drills", "Drills", "drills-1"),
        ("body", "Body", "body-1"), ("gear", "Gear", "gear"), ("coach", "Coach", "coach-1"), ("notes", "Notes", "note-1")]


def rail(active):
    return '<nav class="rail">' + "".join(
        f'<a href="#{t}" class="{"on" if k == active else ""}">{label}</a>' for k, label, t in TABS) + "</nav>"


def header(kicker, title, right=""):
    return (f'<header class="ph"><div style="display:flex;align-items:flex-end;gap:14px">'
            f'<a href="#index" class="home">{ball()}</a>'
            f'<div><span class="kicker">{kicker}</span><h1>{title}</h1></div></div>{right}</header>')


def page(pid, active, body):
    return f'<section class="page" id="{pid}"><div class="main">{body}</div>{rail(active)}</section>'


def box(label, inner='<div class="lines"></div>', style=""):
    return f'<div class="box" style="{style}"><span class="lbl">{label}</span>{inner}</div>'


def checks(n, items=(), cls=""):
    items = list(items) + [""] * (n - len(items))
    return "".join(f'<div class="check {cls}">{x}</div>' for x in items)


def circles(n, numbered=False):
    return '<div class="circles">' + "".join(f"<i>{k + 1 if numbered else ''}</i>" for k in range(n)) + "</div>"


def fields(*names):
    return '<div class="row" style="margin-bottom:12px">' + "".join(
        f'<div class="field"><span class="lbl">{n}</span><div class="ln"></div></div>' for n in names) + "</div>"


def opts(*names):
    return '<div class="opts">' + "".join(f"<span>{n}</span>" for n in names) + "</div>"


def table(heads, rows, widths=(), first=()):
    ths = "".join(f'<th style="{f"width:{widths[i]}" if i < len(widths) and widths[i] else ""}">{h}</th>'
                  for i, h in enumerate(heads))
    first = list(first) + [""] * (rows - len(first))
    trs = "".join(f'<tr><td class="cat">{first[r]}</td>' + "<td></td>" * (len(heads) - 1) + "</tr>" for r in range(rows))
    return f'<table class="tbl"><tr>{ths}</tr>{trs}</table>'


# ---------------------------------------------------------------- pages

def cover():
    return ('<section class="page cover" id="cover">'
            f'<div class="lines-bg">{court("var(--cover-line)", 0.12, "var(--cover-accent)")}</div>'
            '<div class="inner"><div class="plate">'
            f'<div class="ball">{ball("var(--cover-accent)", 1)}</div>'
            '<div class="est">Tennis Performance Journal</div>'
            '<h1>The <em>Match</em><br>Book</h1>'
            '<div class="sub">Plan &middot; Play &middot; Reflect &middot; Rise</div>'
            '<div class="owner">Player<span></span></div>'
            '</div></div><div class="foot">Every point tells you something</div></section>')


def welcome():
    body = header("Before the first serve", "<em>Welcome</em>")
    body += ('<div class="prose">'
             '<p class="lead">The best players don\'t just play more. They pay closer attention to each match, '
             'to each opponent and to every session on court.</p>'
             '<p>The Match Book is your private record of the game. Plan each match before you walk on court, '
             'reflect honestly when you walk off, scout the players you meet again and again, and watch your '
             'game sharpen over the season. Every page is hyperlinked: use the tabs on the right, and tap the '
             'tennis ball in the corner of any page to return to the index.</p></div>'
             '<div class="steps">'
             '<div><h4><em>i.</em>Before</h4><p>Fill in the pre-match page the night before or during warm-up: '
             'three keys, serve and return plans, and your mindset word.</p></div>'
             '<div><h4><em>ii.</em>After</h4><p>Within an hour of the match, record the score, your key stats '
             'and an honest rating. Note what worked and one thing to change.</p></div>'
             '<div><h4><em>iii.</em>Scout</h4><p>Keep a page for every regular opponent. Mark their patterns on the '
             'court diagram and log your head-to-head record.</p></div>'
             '<div><h4><em>iv.</em>Train</h4><p>Turn each &ldquo;what to change&rdquo; into a practice focus. Use the '
             'training log, drill library and coach notes to close the loop.</p></div>'
             f'</div><div class="court" style="margin:24px 0 16px">{court()}</div>'
             '<p class="serif" style="text-align:center;font-style:italic;color:var(--muted);font-size:13px">'
             'Works in GoodNotes, Notability, Noteshelf and any PDF app &middot; Printable on US Letter or A4<br>'
             'For personal use only. Thank you for supporting a small studio.</p>')
    return page("welcome", None, body)


def index():
    entries = [("profile", "Player Profile"), ("season", "Season Goals"), ("calendar", "Season Calendar"),
               ("results", "Results Log"), ("matches", "Match Pages"), ("scouting", "Opponent Scouting"),
               ("train-1", "Training Log"), ("drills-1", "Drill Library"), ("body-1", "Body &amp; Recovery"),
               ("gear", "String &amp; Racquet Log"), ("kit", "Match-Day Kit"), ("coach-1", "Coach Notes"),
               ("note-1", "Notes"), ("note-5", "Court Diagrams")]
    links = "".join(f'<a href="#{t}"><span class="n">{n + 1:02d}</span><span class="t">{label}</span>'
                    f'<span class="go">&rarr;</span></a>' for n, (t, label) in enumerate(entries))
    body = header("Contents", "The <em>Index</em>") + f'<div class="toc">{links}</div>'
    body += (f'<div class="court" style="margin:30px 0 10px">{court()}</div>'
             '<p class="serif" style="text-align:center;font-style:italic;color:var(--muted);font-size:14px">'
             '&ldquo;Play the ball, not the opponent.&rdquo;</p>')
    return page("index", None, body)


def profile():
    body = header("The player", "Player <em>Profile</em>")
    body += fields("Name", "Club") + fields("Rating / ranking", "Coach") + fields("Age group / division", "Since")
    body += '<div class="row" style="margin-bottom:12px">'
    body += box("Plays", opts("Right-handed", "Left-handed"), "flex:1")
    body += box("Backhand", opts("One-handed", "Two-handed"), "flex:1") + "</div>"
    body += box("Game style", opts("Aggressive baseliner", "Counter-puncher", "All-court", "Serve &amp; volley", "Big server"),
                "margin-bottom:12px")
    body += '<div class="row" style="margin-bottom:12px">'
    body += box("Favourite surface", opts("Hard", "Clay", "Grass", "Indoor"), "flex:1")
    body += box("Racquet &amp; strings", '<div class="lines" style="flex:none;height:48px"></div>', "flex:1") + "</div>"
    body += '<div class="row fill">'
    body += box("My weapons") + box("Working on") + "</div>"
    return page("profile", "season", body)


def season():
    body = header("This season", "Season <em>Goals</em>", '<div class="nav"><a class="btn solid" href="#calendar">Calendar</a></div>')
    body += box("Outcome goals &middot; results I want", checks(3, cls="rnd"), "margin-bottom:12px")
    body += box("Performance goals &middot; numbers I will improve",
                table(["Measure", "Start", "Mid-season", "Target"], 5,
                      first=["1st serve %", "Unforced errors / set", "Break points won %", "Net points won %", ""]),
                "margin-bottom:12px")
    body += box("Process goals &middot; habits I will own", checks(4, cls="rnd"), "margin-bottom:12px")
    body += '<div class="row fill">' + box("Why this season matters") + box("Rewards along the way") + "</div>"
    return page("season", "season", body)


def calendar():
    body = header("Plan the year", "Season <em>Calendar</em>")
    body += '<div class="box fill">' + table(["Month", "Tournaments / league", "Dates", "Surface", "Entry by", "Result"],
                                               24, ("78px", "", "60px", "56px", "56px", "60px"),
                                               [m if i % 2 == 0 else "" for m in MONTHS for i in range(2)]) + "</div>"
    return page("calendar", "season", body)


def results():
    body = header("Every match, at a glance", "Results <em>Log</em>")
    body += '<div class="box fill">' + table(["Date", "Event", "Opponent", "Surface", "Score", "W / L"], 30,
                                               ("54px", "", "", "52px", "84px", "40px")) + "</div>"
    return page("results", "results", body)


def matches():
    slots = "".join(f'<a href="#m{n:02d}-pre"><span class="n">Match {n:02d}</span><span class="w">vs</span>'
                    f'<span class="go">Plan &rarr;</span></a>' for n in range(1, MATCHES + 1))
    body = header(f"{MATCHES} match spreads", "Match <em>Pages</em>")
    body += f'<div class="slots">{slots}</div>'
    return page("matches", "matches", body)


def match_nav(n, current):
    return ('<div class="nav">'
            f'<a class="btn{" solid" if current == "pre" else ""}" href="#m{n:02d}-pre">Before</a>'
            f'<a class="btn{" solid" if current == "post" else ""}" href="#m{n:02d}-post">After</a>'
            '<a class="btn" href="#matches">All</a></div>')


def match_pre(n):
    body = header(f"Match {n:02d} &middot; Before", "Match <em>Plan</em>", match_nav(n, "pre"))
    body += fields("Opponent", "Event", "Round") + fields("Date", "Time", "Court")
    body += '<div class="row" style="margin-bottom:12px">'
    body += box("Surface", opts("Hard", "Clay", "Grass", "Indoor"), "flex:1.2")
    body += box("Conditions", opts("Sun", "Wind", "Heat", "Cold"), "flex:1") + "</div>"
    body += box("Game plan &middot; three keys", checks(3, cls="rnd"), "margin-bottom:12px")
    body += '<div class="row" style="height:118px;margin-bottom:12px">' + box("Serve plan") + box("Return plan") + "</div>"
    body += '<div class="row" style="height:118px;margin-bottom:12px">' + box("Their strengths") + box("Their weaknesses") + "</div>"
    body += '<div class="row fill">'
    body += box("Warm-up ritual", checks(6, ["Dynamic stretch", "Mini tennis", "Groundstrokes", "Volleys &amp; overheads",
                                                "Serves &amp; returns", "Breathe &amp; visualise"]), "flex:1")
    body += ('<div class="col" style="flex:1">'
             + box("Mindset word", '<div class="ln" style="border-bottom:1px solid var(--hair);height:22px"></div>')
             + box("If it gets tough, I will", '<div class="lines"></div>', "flex:1") + "</div>")
    body += "</div>"
    return page(f"m{n:02d}-pre", "matches", body)


def match_post(n):
    body = header(f"Match {n:02d} &middot; After", "Match <em>Review</em>", match_nav(n, "post"))
    body += ('<div class="row" style="margin-bottom:12px;align-items:stretch">'
             '<table class="score" style="flex:1"><tr><th style="text-align:left;padding-left:10px">Player</th>'
             '<th>Set 1</th><th>Set 2</th><th>Set 3</th></tr>'
             '<tr><td class="who">Me</td><td></td><td></td><td></td></tr>'
             '<tr><td class="who">Opponent</td><td></td><td></td><td></td></tr></table>'
             f'{box("Result", opts("Win", "Loss") + "<div style=height:10px></div>" + opts("Ret.", "W/O"), "width:130px")}</div>')
    stats = ["Aces", "Double faults", "1st serve %", "Winners", "Unforced errors", "Break pts won"]
    body += ('<div style="display:grid;grid-template-columns:repeat(6,1fr);gap:8px;margin-bottom:12px">'
             + "".join(f'<div class="stat"><span>{s}</span><b></b></div>' for s in stats) + "</div>")
    parts = ["Serve", "Return", "Forehand", "Backhand", "Net game", "Movement", "Mental game"]
    body += '<div class="row" style="margin-bottom:12px">'
    body += box("Rate each part of my game", "".join(f'<div class="rate"><span>{p}</span>{circles(5, True)}</div>' for p in parts), "flex:1")
    body += ('<div class="col" style="flex:1">'
             + box("Overall performance", circles(10, True))
             + box("Key moment of the match", '<div class="lines"></div>', "flex:1") + "</div></div>")
    body += '<div class="row fill">' + box("What worked") + box("What to change") + "</div>"
    body += box("Next practice focus", checks(2, cls="rnd"), "margin-top:12px")
    return page(f"m{n:02d}-post", "matches", body)


def scouting():
    slots = "".join(f'<a href="#scout-{n:02d}"><span class="n">No. {n:02d}</span><span class="w">Name</span>'
                    f'<span class="go">Open &rarr;</span></a>' for n in range(1, SCOUTS + 1))
    body = header("Know your opponent", "Opponent <em>Scouting</em>")
    body += f'<div class="slots">{slots}</div>'
    body += (f'<div class="court" style="margin-top:22px">{court()}</div>')
    return page("scouting", "scout", body)


def scout(n):
    body = header(f"Scouting report &middot; No. {n:02d}", "The <em>Opponent</em>",
                  '<div class="nav"><a class="btn" href="#scouting">All opponents</a></div>')
    body += fields("Name", "Club", "Rating")
    body += '<div class="row" style="margin-bottom:12px">'
    body += box("Plays", opts("Right", "Left"), "flex:1") + box("Backhand", opts("One-hand", "Two-hand"), "flex:1.2") + "</div>"
    body += box("Style", opts("Big hitter", "Pusher", "Counter-puncher", "All-court", "Net rusher", "Moonballer"), "margin-bottom:12px")
    body += '<div class="row fill" style="margin-bottom:12px">'
    body += '<div class="col" style="flex:1.1">' + box("Strengths", '<div class="lines"></div>', "flex:1") + box("Weaknesses", '<div class="lines"></div>', "flex:1")
    body += box("Serve tendencies &middot; first / second", '<div class="lines"></div>', "flex:.8") + "</div>"
    body += box("Patterns &amp; targets", f'<div class="court">{court("var(--hair)", 0.3)}</div>', "flex:1") + "</div>"
    body += box("Head to head", table(["Date", "Event", "Score", "W / L", "What decided it"], 4, ("56px", "", "80px", "42px", "")))
    return page(f"scout-{n:02d}", "scout", body)


def train(n):
    nav = ('<div class="nav">' + (f'<a class="btn" href="#train-{n - 1}">&larr;</a>' if n > 1 else "")
           + (f'<a class="btn" href="#train-{n + 1}">&rarr;</a>' if n < TRAIN_WEEKS else "") + "</div>")
    body = header(f"Training log &middot; Week {n:02d}", "On <em>Court</em>", nav)
    body += fields("Week of", "Hours this week", "Matches played")
    body += box("This week's focus", '<div class="lines" style="flex:none;height:48px"></div>', "margin-bottom:12px")
    body += '<div class="box fill">' + table(["Day", "Session focus", "Mins", "Effort", "Notes"], 21,
                                               ("70px", "", "38px", "42px", ""),
                                               [d if i == 0 else "" for d in DAYS for i in range(3)]) + "</div>"
    body += '<div class="row" style="height:110px;margin-top:12px">' + box("Breakthroughs") + box("Still working on") + "</div>"
    return page(f"train-{n}", "train", body)


def drill_card(k):
    return ('<div class="box fill" style="flex-direction:row;gap:14px">'
            f'<div style="width:150px;display:flex;flex-direction:column"><span class="lbl">Drill {k:02d}</span>'
            f'<div class="court">{court("var(--hair)", 0.3)}</div></div>'
            '<div style="flex:1;display:flex;flex-direction:column">'
            + fields("Drill name", "Players")
            + '<div class="row" style="margin-bottom:8px">' + opts("Warm-up", "Technique", "Tactics", "Fitness", "Pressure") + "</div>"
            + '<span class="lbl" style="margin-top:4px">Objective &middot; setup &middot; scoring</span><div class="lines"></div>'
            + '<span class="lbl" style="margin-top:8px">Make it harder</span><div class="lines" style="flex:none;height:48px"></div>'
            + "</div></div>")


def drills(n):
    nav = ('<div class="nav">' + (f'<a class="btn" href="#drills-{n - 1}">&larr;</a>' if n > 1 else "")
           + (f'<a class="btn" href="#drills-{n + 1}">&rarr;</a>' if n < DRILL_PAGES else "") + "</div>")
    body = header("Drill library", "Drill <em>Cards</em>", nav)
    body += f'<div class="col fill">{drill_card(n * 2 - 1)}{drill_card(n * 2)}</div>'
    return page(f"drills-{n}", "drills", body)


def body_week(n):
    rows = "".join(f'<tr><td class="cat">{d}</td><td></td><td>{circles(5)}</td><td>{circles(5)}</td><td></td><td></td></tr>' for d in DAYS)
    tbl = ('<table class="tbl"><tr><th style="width:70px">Day</th><th style="width:44px">Sleep</th><th style="width:88px">Energy</th>'
           f'<th style="width:88px">Soreness</th><th>Fitness work</th><th style="width:60px">Water</th></tr>{rows}</table>')
    nav = ('<div class="nav">' + (f'<a class="btn" href="#body-{n - 1}">&larr;</a>' if n > 1 else "")
           + (f'<a class="btn" href="#body-{n + 1}">&rarr;</a>' if n < BODY_WEEKS else "") + "</div>")
    body = header(f"Body &amp; recovery &middot; Week {n:02d}", "Body <em>&amp; Recovery</em>", nav)
    body += fields("Week of", "Weight (optional)", "Resting heart rate")
    body += f'<div class="box" style="margin-bottom:12px">{tbl}</div>'
    body += '<div class="row" style="margin-bottom:12px">'
    body += box("Recovery ritual", checks(6, ["Stretch / mobility", "Foam roll", "Ice or contrast bath", "Protein within an hour",
                                                 "Eight hours of sleep", "Rest day"]), "flex:1")
    body += box("Strength &amp; conditioning", checks(6), "flex:1") + "</div>"
    body += '<div class="row fill">' + box("Niggles &amp; injuries to watch") + box("Fuel &amp; hydration notes") + "</div>"
    return page(f"body-{n}", "body", body)


def gear():
    body = header("Equipment", "Strings <em>&amp; Racquets</em>")
    body += '<div class="row" style="margin-bottom:12px">'
    for k in (1, 2):
        body += box(f"Racquet {k}", fields("Model", "Grip") + fields("String", "Tension"), "flex:1")
    body += "</div>"
    body += '<div class="box fill"><span class="lbl">Restring log</span>' + table(
        ["Date", "Racquet", "String", "Tension", "Hours", "Feel"], 22, ("60px", "60px", "", "56px", "46px", "")) + "</div>"
    return page("gear", "gear", body)


def kit():
    items = ["Racquets (strung)", "Spare overgrips", "Vibration dampener", "Shoes", "Spare socks", "Shirt &amp; change of clothes",
             "Hat or visor", "Sunscreen", "Water bottles", "Electrolytes", "Banana &amp; snacks", "Towel",
             "Balls", "Tape &amp; plasters", "Ice pack", "Phone &amp; charger", "Membership / ID", "This Match Book"]
    body = header("Never forget a thing", "Match-Day <em>Kit</em>")
    body += '<div class="row fill">'
    body += box("The bag", f'<div style="columns:2;column-gap:16px">{checks(len(items), items)}</div>', "flex:1")
    body += "</div>"
    body += '<div class="row" style="height:200px;margin-top:12px">' + box("Pre-match meal") + box("Between-sets routine") + "</div>"
    return page("kit", "gear", body)


def coach(n):
    nav = ('<div class="nav">' + (f'<a class="btn" href="#coach-{n - 1}">&larr;</a>' if n > 1 else "")
           + (f'<a class="btn" href="#coach-{n + 1}">&rarr;</a>' if n < COACH_PAGES else "") + "</div>")
    body = header(f"Lesson notes &middot; {n:02d}", "Coach <em>Notes</em>", nav)
    body += fields("Date", "Coach", "Lesson focus")
    body += '<div class="row fill" style="margin-bottom:12px">'
    body += box("Technical cues", '<div class="lines"></div>', "flex:1.3")
    body += box("Court sketch", f'<div class="court">{court("var(--hair)", 0.3)}</div>', "flex:1") + "</div>"
    body += '<div class="row" style="height:150px">' + box("Homework", checks(4, cls="rnd"), "flex:1") + box("Questions for next time", '<div class="lines"></div>', "flex:1") + "</div>"
    return page(f"coach-{n}", "coach", body)


def note(n, kind):
    if kind == "courts":
        inner = ('<div style="display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:12px;flex:1">'
                 + "".join(f'<div class="box"><span class="lbl">Diagram</span><div class="court">{court("var(--hair)", 0.3)}</div></div>' for _ in range(4))
                 + "</div>")
    else:
        inner = {"lined": '<div class="lines"></div>', "dotted": '<div class="dots"></div>'}[kind]
    body = header(f"Notes &middot; {n:02d}", "<em>Notes</em>" if kind != "courts" else "Court <em>Diagrams</em>")
    body += f'<div class="fill" style="display:flex">{inner}</div>'
    return page(f"note-{n}", "notes", body)


def build():
    pages = [cover(), welcome(), index(), profile(), season(), calendar(), results(), matches()]
    for n in range(1, MATCHES + 1):
        pages += [match_pre(n), match_post(n)]
    pages.append(scouting())
    pages += [scout(n) for n in range(1, SCOUTS + 1)]
    pages += [train(n) for n in range(1, TRAIN_WEEKS + 1)]
    pages += [drills(n) for n in range(1, DRILL_PAGES + 1)]
    pages += [body_week(n) for n in range(1, BODY_WEEKS + 1)]
    pages += [gear(), kit()]
    pages += [coach(n) for n in range(1, COACH_PAGES + 1)]
    pages += [note(n, k) for n, k in enumerate(["lined", "lined", "dotted", "dotted", "courts", "courts"], 1)]
    here = Path(__file__).parent
    css = (here / "journal.css").read_text()
    if THEME != "club":
        css += (here / "themes" / f"{THEME}.css").read_text()
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>The Match Book</title>'
            f'<link rel="stylesheet" href="{FONT_URL}"><style>{css}</style></head><body>{"".join(pages)}</body></html>'), len(pages)


if __name__ == "__main__":
    html, count = build()
    name = "journal.html" if THEME == "club" else f"journal-{THEME}.html"
    Path(__file__).with_name(name).write_text(html)
    print(f"{count} pages")
