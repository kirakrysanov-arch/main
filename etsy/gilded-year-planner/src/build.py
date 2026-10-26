"""Generates the Gilded Year planner HTML. Run: python3 build.py > planner.html"""
from pathlib import Path

MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
WEEKS_PER_MONTH = 5
DAILY_PAGES = 14
FONTS = ("https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,500;1,300;1,400"
         "&family=Montserrat:wght@300;400;500;600&display=swap")


def mid(i):
    return MONTHS[i][:3].lower()


def rail(active):
    tabs = [("year", "Year", "year"), ("goals", "Goals", "vision")]
    tabs += [(mid(i), MONTHS[i][:3], mid(i)) for i in range(12)]
    tabs += [("daily", "Daily", "daily"), ("habits", "Habits", "habits-jan"),
             ("money", "Money", "budget"), ("self", "Self", "selfcare"), ("notes", "Notes", "notes")]
    out = []
    for n, (key, label, target) in enumerate(tabs):
        cls = []
        if key == active:
            cls.append("on")
        if n in (2, 14):
            cls.append("sep")
        out.append(f'<a href="#{target}" class="{" ".join(cls)}">{label}</a>')
    return f'<nav class="rail">{"".join(out)}</nav>'


def header(kicker, title, right=""):
    return (f'<header class="ph"><div style="display:flex;align-items:flex-end;gap:14px">'
            f'<a href="#index" class="home"><span>G</span></a>'
            f'<div><span class="kicker">{kicker}</span><h1>{title}</h1></div></div>{right}</header>')


def page(pid, active, body, cls=""):
    return f'<section class="page {cls}" id="{pid}"><div class="main">{body}</div>{rail(active)}</section>'


def box(label, inner='<div class="lines"></div>', style=""):
    return f'<div class="box" style="{style}"><span class="lbl">{label}</span>{inner}</div>'


def checks(n, cls=""):
    return "".join(f'<div class="check {cls}"></div>' for _ in range(n))


def circles(n, numbered=False):
    return '<div class="circles">' + "".join(f"<i>{k + 1 if numbered else ''}</i>" for k in range(n)) + "</div>"


# ---------------------------------------------------------------- pages

def cover():
    return ('<section class="page cover" id="cover"><div class="frame"></div><div class="inner">'
            '<div class="monogram"><span>G</span></div>'
            '<h1>The <em>Gilded</em><br>Year</h1>'
            '<div class="sub">Undated Luxury Planner</div>'
            '<div class="ornament"><b></b></div>'
            '<div class="owner">This year belongs to<span></span></div>'
            '<a class="btn" href="#index" style="margin-top:40px;color:#E3CD95;border-color:rgba(201,170,107,.6)">Enter</a>'
            '</div><div class="foot">Plan beautifully &middot; Live intentionally</div></section>')


def welcome():
    body = header("A note before you begin", "<em>Welcome</em>")
    body += ('<div class="prose">'
             '<p class="lead">Your year deserves the same care you give to everything you love. '
             'This planner was designed to make every plan feel like a quiet luxury.</p>'
             '<p>The Gilded Year is fully undated, so you can begin on any day, in any month, of any year. '
             'Every page is hyperlinked: tap the tabs along the right edge to move between months and sections, '
             'and tap the gold diamond in the corner of any page to return to the index.</p></div>'
             '<div class="steps">'
             '<div><h4><em>i.</em>Import</h4><p>Open the PDF in GoodNotes, Notability, Noteshelf, Xodo or any PDF '
             'annotation app. Import as a new notebook so the links stay active.</p></div>'
             '<div><h4><em>ii.</em>Navigate</h4><p>Use the side tabs for months and sections. On each month, tap '
             'Week 1&ndash;5, Habits or Review to jump straight to that page.</p></div>'
             '<div><h4><em>iii.</em>Personalise</h4><p>Write your own dates into the small circles on each calendar. '
             'Duplicate any page in your app whenever you need more.</p></div>'
             '<div><h4><em>iv.</em>Print</h4><p>Prefer paper? Print on US Letter or A4 with &ldquo;fit to page&rdquo;. '
             'Heavyweight ivory or cream stock gives the most luxurious finish.</p></div>'
             '</div>'
             '<div style="flex:1"></div>'
             '<div class="ornament" style="margin-bottom:10px"><b></b></div>'
             '<p class="serif" style="text-align:center;font-style:italic;color:var(--muted);font-size:13px">'
             'For personal use only. Thank you for supporting a small studio.</p>')
    return page("welcome", None, body)


def index():
    entries = [("year", "Year at a Glance"), ("vision", "Vision Board"), ("goals", "Annual Goals")]
    entries += [(mid(i), MONTHS[i]) for i in range(12)]
    entries += [("daily", "Daily Ritual"), ("habits-jan", "Habit Trackers"), ("budget", "Monthly Budget"),
                ("expenses", "Expense Log"), ("savings", "Savings Tracker"), ("selfcare", "Self-Care Menu"),
                ("meals", "Meal Planner"), ("notes", "Notes")]
    links = "".join(f'<a href="#{t}"><span class="n">{n + 1:02d}</span><span class="t">{label}</span>'
                    f'<span class="go">&rarr;</span></a>' for n, (t, label) in enumerate(entries))
    body = header("Contents", "The <em>Index</em>") + f'<div class="toc">{links}</div>'
    body += ('<div style="flex:1"></div><div class="ornament"><b></b></div>'
             '<p class="serif" style="text-align:center;font-style:italic;color:var(--muted);font-size:14px;margin-top:10px">'
             '&ldquo;She designed a life she loved.&rdquo;</p>')
    return page("index", None, body)


def mini_grid():
    heads = "".join(f"<b>{d[0]}</b>" for d in DAYS)
    return f'<div class="mg">{heads}{"<i></i>" * 42}</div>'


def year():
    blocks = "".join(f'<a class="mini" href="#{mid(i)}"><h3>{MONTHS[i]}<small>{i + 1:02d}</small></h3>{mini_grid()}</a>'
                     for i in range(12))
    body = header("Undated &middot; Twelve months", "Year at a <em>Glance</em>",
                  '<div style="text-align:right"><span class="lbl">Year</span>'
                  '<div style="width:90px;border-bottom:1px solid var(--hair);height:18px"></div></div>')
    body += f'<div class="year">{blocks}</div>'
    return page("year", "year", body)


def vision():
    areas = ["Wealth", "Wellness", "Love &amp; Family", "Career", "Home", "Travel &amp; Adventure"]
    cells = "".join(box(a, '<div class="dots"></div>', "flex:1") for a in areas)
    body = header("Manifest", "Vision <em>Board</em>")
    body += ('<div class="box" style="margin-bottom:14px"><span class="lbl">My word for the year</span>'
             '<div class="lines" style="flex:none;height:30px"></div></div>')
    body += f'<div style="display:grid;grid-template-columns:1fr 1fr;grid-template-rows:repeat(3,1fr);gap:14px;flex:1">{cells}</div>'
    return page("vision", "goals", body)


def goals():
    q = "".join(box(f"Quarter {n}", f'<span class="serif" style="font-size:12px;font-style:italic;color:var(--muted);margin-bottom:4px">Goal</span>'
                    f'<div class="lines" style="flex:none;height:48px"></div>'
                    f'<span class="serif" style="font-size:12px;font-style:italic;color:var(--muted);margin:6px 0 4px">Steps</span>{checks(4, "dia")}',
                    "flex:1") for n in ("I", "II", "III", "IV"))
    body = header("Intentions", "Annual <em>Goals</em>")
    body += f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;flex:1">{q}</div>'
    body += '<div class="row" style="margin-top:14px;height:150px">'
    body += box("Habits to build", checks(5), "flex:1") + box("Habits to release", checks(5), "flex:1") + "</div>"
    return page("goals", "goals", body)


def month(i):
    m = mid(i)
    btns = "".join(f'<a class="btn" href="#{m}-w{w}">Week {w}</a>' for w in range(1, WEEKS_PER_MONTH + 1))
    btns += f'<a class="btn solid" href="#habits-{m}">Habits</a><a class="btn solid" href="#review-{m}">Review</a>'
    heads = "".join(f"<b>{d[:3]}</b>" for d in DAYS)
    body = header(f"Month {i + 1:02d} &middot; Undated", f"<em>{MONTHS[i]}</em>")
    body += f'<div class="weeks" style="margin-bottom:14px">{btns}</div>'
    body += f'<div class="cal">{heads}{"<i></i>" * 42}</div>'
    body += '<div class="row" style="height:176px;margin-top:14px">'
    body += box("Monthly focus", '<div class="lines"></div>', "flex:1.2")
    body += box("Priorities", checks(5, "dia"), "flex:1")
    body += box("Important dates", '<div class="lines"></div>', "flex:1") + "</div>"
    return page(m, m, body)


def week(i, w):
    m = mid(i)
    days = "".join(f'<div class="day"><div class="dh"><span>{d}</span><small>Date</small></div><div class="lines tight"></div></div>'
                   for d in DAYS)
    nav = (f'<div style="display:flex;gap:6px">'
           + (f'<a class="btn" href="#{m}-w{w - 1}">&larr;</a>' if w > 1 else "")
           + f'<a class="btn solid" href="#{m}">{MONTHS[i][:3]}</a>'
           + (f'<a class="btn" href="#{m}-w{w + 1}">&rarr;</a>' if w < WEEKS_PER_MONTH else "")
           + "</div>")
    body = header(f"{MONTHS[i]} &middot; Week {w}", "This <em>Week</em>", nav)
    body += '<div class="row fill">'
    body += f'<div class="col" style="flex:1.75;gap:8px">{days}</div>'
    body += '<div class="col" style="flex:1">'
    body += box("Top three", checks(3, "dia"))
    body += box("To do", checks(9))
    body += box("Self-care", circles(7))
    body += box("Gratitude", '<div class="lines"></div>', "flex:1")
    body += box("Notes", '<div class="dots"></div>', "flex:1.2")
    body += "</div></div>"
    return page(f"{m}-w{w}", m, body)


def review(i):
    m = mid(i)
    body = header(f"{MONTHS[i]} &middot; Reflection", "Monthly <em>Review</em>",
                  f'<a class="btn solid" href="#{m}">Back to {MONTHS[i][:3]}</a>')
    body += box("Rate this month", circles(10, True), "margin-bottom:14px")
    body += '<div style="display:grid;grid-template-columns:1fr 1fr;grid-template-rows:1fr 1fr;gap:14px;flex:1">'
    body += box("Wins &amp; highlights") + box("Lessons learned") + box("Grateful for") + box("Let go of")
    body += "</div>"
    body += '<div class="row" style="height:170px;margin-top:14px">'
    body += box("Next month, I will", checks(5, "dia"), "flex:1") + box("A memory to keep", '<div class="lines"></div>', "flex:1")
    body += "</div>"
    return page(f"review-{m}", m, body)


def habits(i):
    m = mid(i)
    cells = '<div class="hd first">Habit</div>' + "".join(f'<div class="hd">{d}</div>' for d in range(1, 32))
    cells += ('<div class="hn"></div>' + "<div></div>" * 31) * 16
    body = header(f"{MONTHS[i]} &middot; Rituals", "Habit <em>Tracker</em>",
                  f'<a class="btn solid" href="#{m}">Back to {MONTHS[i][:3]}</a>')
    body += f'<div class="habit">{cells}</div>'
    months = "".join(f'<a class="btn{" solid" if j == i else ""}" href="#habits-{mid(j)}" style="padding:5px 6px">{MONTHS[j][:3]}</a>'
                     for j in range(12))
    body += f'<div class="weeks" style="margin-top:12px;justify-content:space-between">{months}</div>'
    return page(f"habits-{m}", "habits", body)


def divider(pid, active, num, title, quote, links=""):
    return (f'<section class="page divider" id="{pid}"><div class="frame"></div><div class="inner">'
            f'<div class="num">{num}</div><h2>{title}</h2><div class="ornament"><b></b></div>'
            f'<div class="q">{quote}</div><div class="links">{links}</div></div>{rail(active)}</section>')


def daily(n):
    hours = "".join(f'<div class="hr"><span>{h % 12 or 12}{"am" if h < 12 else "pm"}</span></div>' for h in range(6, 22))
    body = header(f"Daily ritual &middot; {n:02d}", "<em>Today</em>",
                  '<div style="display:flex;gap:18px">'
                  + "".join(f'<div><span class="lbl">{x}</span><div style="width:64px;border-bottom:1px solid var(--hair);height:14px"></div></div>'
                            for x in ("Date", "Day")) + "</div>")
    body += box("Today's intention", '<div class="lines" style="flex:none;height:24px"></div>', "margin-bottom:14px")
    body += '<div class="row fill">'
    body += box("Schedule", f'<div class="sched">{hours}</div>', "flex:1.15")
    body += '<div class="col" style="flex:1">'
    body += box("Top three", checks(3, "dia"))
    body += box("To do", checks(6))
    body += box("Water", circles(8))
    body += box("Mood", '<div class="circles">' + "".join(f'<i style="width:auto;border-radius:10px;padding:0 6px;height:16px;font-size:6px;letter-spacing:1px">{x}</i>'
                                                          for x in ("RADIANT", "CALM", "TIRED", "LOW")) + "</div>")
    body += box("Grateful for", '<div class="lines"></div>', "flex:1")
    body += "</div></div>"
    return page(f"daily-{n}", "daily", body)


def budget():
    inc = "".join(f'<tr><td class="cat">{c}</td><td></td><td></td></tr>' for c in ("Salary", "Business", "Investments", "Other"))
    cats = ["Home", "Utilities", "Groceries", "Dining", "Transport", "Beauty &amp; Wellness", "Wardrobe",
            "Travel", "Subscriptions", "Gifts", "Savings", "Investing", "Giving", ""]
    exp = "".join(f'<tr><td class="cat">{c}</td><td></td><td></td><td></td></tr>' for c in cats)
    body = header("Wealth", "Monthly <em>Budget</em>",
                  '<div><span class="lbl">Month</span><div style="width:90px;border-bottom:1px solid var(--hair);height:14px"></div></div>')
    body += '<div class="box" style="margin-bottom:14px"><span class="lbl">Income</span>'
    body += f'<table class="tbl"><tr><th>Source</th><th>Expected</th><th>Actual</th></tr>{inc}</table></div>'
    body += '<div class="box fill"><span class="lbl">Expenses</span>'
    body += f'<table class="tbl"><tr><th>Category</th><th>Budget</th><th>Actual</th><th>Difference</th></tr>{exp}</table></div>'
    body += '<div class="row" style="margin-top:14px">'
    body += "".join(box(x, '<div style="height:22px;border-bottom:1px solid var(--hair-soft)"></div>', "flex:1")
                    for x in ("Total income", "Total spent", "Left to save"))
    body += "</div>"
    return page("budget", "money", body)


def expenses():
    rows = '<tr><td></td><td></td><td class="cat"></td><td></td></tr>' * 30
    body = header("Wealth", "Expense <em>Log</em>")
    body += f'<div class="box fill"><table class="tbl"><tr><th style="width:70px">Date</th><th>Description</th><th style="width:110px">Category</th><th style="width:80px">Amount</th></tr>{rows}</table></div>'
    return page("expenses", "money", body)


def savings():
    body = header("Wealth", "Savings <em>Tracker</em>")
    body += '<div class="row" style="margin-bottom:14px">'
    body += "".join(box(x, '<div style="height:22px;border-bottom:1px solid var(--hair-soft)"></div>', "flex:1")
                    for x in ("Saving for", "Goal amount", "Target date"))
    body += "</div>"
    body += box("Colour one in for every milestone", '<div class="circles" style="gap:10px;justify-content:center">'
                + "".join(f'<i style="width:36px;height:36px;font-size:8px">{(k + 1) * 2}%</i>' for k in range(50)) + "</div>",
                "margin-bottom:14px")
    rows = '<tr><td></td><td></td><td></td></tr>' * 10
    body += f'<div class="box fill"><span class="lbl">Deposits</span><table class="tbl"><tr><th>Date</th><th>Amount</th><th>Running total</th></tr>{rows}</table></div>'
    return page("savings", "money", body)


def selfcare():
    groups = {"Body": ["Morning walk", "Stretch or yoga", "Long bath", "Early night"],
              "Mind": ["Read for pleasure", "Journal", "Digital detox", "Meditate"],
              "Soul": ["Fresh flowers", "Call someone dear", "Gallery or museum", "Slow dinner"],
              "Indulge": ["Spa ritual", "Silk pyjama day", "Afternoon tea", "Something beautiful"]}
    cells = "".join(box(g, "".join(f'<div class="check">{x and f"<span class=serif style=font-size:14px>{x}</span>"}</div>' for x in items)
                        + checks(8), "flex:1") for g, items in groups.items())
    body = header("Wellness", "Self-Care <em>Menu</em>")
    body += f'<div style="display:grid;grid-template-columns:1fr 1fr;gap:14px;flex:1">{cells}</div>'
    body += box("How I want to feel", '<div class="lines"></div>', "height:130px;margin-top:14px")
    return page("selfcare", "self", body)


def meals():
    rows = "".join(f'<tr><td class="cat" style="height:54px">{d}</td><td></td><td></td><td></td></tr>' for d in DAYS)
    body = header("Wellness", "Meal <em>Planner</em>")
    body += ('<div class="box" style="margin-bottom:14px"><table class="tbl">'
             f'<tr><th style="width:90px">Day</th><th>Breakfast</th><th>Lunch</th><th>Dinner</th></tr>{rows}</table></div>')
    body += '<div class="row fill">'
    body += box("Grocery list", '<div style="columns:2;column-gap:14px">' + checks(26) + "</div>", "flex:1.4")
    body += box("Prep notes", '<div class="lines"></div>', "flex:1") + "</div>"
    return page("meals", "self", body)


def note(n, kind):
    inner = {"lined": '<div class="lines"></div>', "dotted": '<div class="dots"></div>', "grid": '<div class="grid"></div>'}[kind]
    body = header(f"Notes &middot; {n:02d}", "<em>Notes</em>",
                  '<div><span class="lbl">Topic</span><div style="width:120px;border-bottom:1px solid var(--hair);height:14px"></div></div>')
    body += f'<div class="fill" style="display:flex">{inner}</div>'
    return page(f"note-{n}", "notes", body)


def build():
    pages = [cover(), welcome(), index(), year(), vision(), goals()]
    for i in range(12):
        pages.append(month(i))
        pages += [week(i, w) for w in range(1, WEEKS_PER_MONTH + 1)]
        pages.append(review(i))
    day_links = "".join(f'<a href="#daily-{n}">{n:02d}</a>' for n in range(1, DAILY_PAGES + 1))
    pages.append(divider("daily", "daily", "Chapter II", "Daily <em>Ritual</em>",
                         "&ldquo;How we spend our days is, of course, how we spend our lives.&rdquo;", day_links))
    pages += [daily(n) for n in range(1, DAILY_PAGES + 1)]
    pages += [habits(i) for i in range(12)]
    pages += [budget(), expenses(), savings(), selfcare(), meals()]
    kinds = ["lined"] * 4 + ["dotted"] * 3 + ["grid"] * 3
    note_links = "".join(f'<a href="#note-{n}">{k} {n:02d}</a>' for n, k in enumerate(kinds, 1))
    pages.append(divider("notes", "notes", "Chapter III", "<em>Notes</em>",
                         "A place for every thought worth keeping.", note_links))
    pages += [note(n, k) for n, k in enumerate(kinds, 1)]
    css = Path(__file__).with_name("planner.css").read_text()
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8"><title>The Gilded Year</title>'
            f'<link rel="stylesheet" href="{FONTS}"><style>{css}</style></head><body>{"".join(pages)}</body></html>'), len(pages)


if __name__ == "__main__":
    html, count = build()
    Path(__file__).with_name("planner.html").write_text(html)
    print(f"{count} pages")
