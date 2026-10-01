"""Generate wireframes.html: flow overviews + a clickable PDF prototype.

Run: python3 build_wireframes.py, then print wireframes.html to PDF
(Chromium keeps the #anchor links as clickable PDF links).
"""
import re

# ---------------------------------------------------------------- helpers
def hs(target, inner, cls="btn", style=""):
    """Hotspot: a link to another prototype screen."""
    return f'<a class="hs {cls}" href="#{target}" style="{style}">{inner}</a>'

def lines(*widths):
    return "".join(f'<div class="ln" style="width:{w}%"></div>' for w in widths)

def tabbar(active, links=True):
    items = [("Today", "s06"), ("Course", None), ("Songs", None), ("Progress", "s15")]
    out = []
    for name, tgt in items:
        cls = "on" if name == active else ""
        cell = f'<i></i>{name}'
        if links and tgt and name != active:
            out.append(f'<a class="hs tab {cls}" href="#{tgt}">{cell}</a>')
        else:
            out.append(f'<div class="tab {cls}">{cell}</div>')
    return f'<div class="tabbar">{"".join(out)}</div>'

def chord(c, state="done"):
    return f'<span class="ch ch-{state}">{c}</span>'

def path_row(states):
    parts = []
    for i, (c, st) in enumerate(states):
        if i:
            parts.append(f'<span class="pl {"pl-on" if st == "done" else ""}"></span>')
        parts.append(chord(c, st))
    return f'<div class="path">{"".join(parts)}</div>'

def top(title="", back=None, right=""):
    b = hs(back, "‹", "icon") if back else '<span class="icon ghost"></span>'
    return f'<div class="nav">{b}<span class="navt">{title}</span><span class="icon ghost">{right}</span></div>'

def progress(step, total):
    return f'<div class="prog"><div style="width:{step/total*100:.0f}%"></div></div><div class="cap">Step {step} of {total}</div>'

# ---------------------------------------------------------------- screens
S = {}

S["s01"] = dict(name="Welcome", group=1, body=f'''
<div class="pad" style="padding-top:26px;text-align:center">
  <div class="box" style="height:210px">Justin intro video · 20 s</div>
  <div class="h" style="margin-top:20px">Learn guitar with Justin</div>
  <div class="sub" style="margin:8px 18px 0">Play your first real song in your first weeks.</div>
</div>
<div class="bottom">{hs("s02","Get started")}<div class="link" style="margin-top:10px">I already have an account</div></div>''',
  why="Lead with the teacher people trust. Justin's face and voice come before any form.",
  hot=["Get started → Experience"])

S["s02"] = dict(name="Experience", group=1, body=f'''
{top("", "s01")}
<div class="pad">{progress(1,4)}
  <div class="h" style="margin-top:12px">Have you played guitar before?</div>
  <div class="opts" style="margin-top:16px">
    {hs("s03",'<b>Never</b><span>Start from your first chord</span>',"opt sel")}
    <div class="opt"><b>A few chords</b><span>Start at Module 3</span></div>
    <div class="opt"><b>I play songs</b><span>Take a 2-min check</span></div>
  </div>
</div>''',
  why="One question sets the starting module, so beginners are never shown content above their level.",
  hot=["Never → Why song"])

S["s03"] = dict(name="Why song", group=1, body=f'''
{top("", "s02")}
<div class="pad">{progress(2,4)}
  <div class="h" style="margin-top:12px">Which song made you pick up a guitar?</div>
  <div class="search">⌕  Search 1,500+ songs</div>
  <div class="cap" style="margin-top:12px">Great first songs</div>
  <div class="opts">
    <div class="opt row sel"><span class="art"></span><span style="flex:1"><b>Three Little Birds</b><span>A · D · E · ~3 weeks</span></span><span class="tick">✓</span></div>
    <div class="opt row"><span class="art"></span><span style="flex:1"><b>Knockin' on Heaven's Door</b><span>G · D · Am · C · ~5 weeks</span></span></div>
    <div class="opt row"><span class="art"></span><span style="flex:1"><b>Wonderwall</b><span>Em · G · D · A · ~6 weeks</span></span></div>
  </div>
</div>
<div class="bottom">{hs("s04","Build my path")}</div>''',
  why="The user's own reason becomes the goal. The estimate is honest, and the easy songs are listed first.",
  hot=["Build my path → Path preview"])

S["s04"] = dict(name="Path & rhythm", group=1, body=f'''
{top("", "s03")}
<div class="pad">{progress(3,4)}
  <div class="h" style="margin-top:12px">Your path to Three Little Birds</div>
  <div class="card" style="margin-top:12px">{path_row([("A","now"),("D","lock"),("E","lock"),("♪","lock")])}
    <div class="sub" style="margin-top:8px">3 chords · about 3 weeks at 10 min a day</div></div>
  <div class="h2" style="margin-top:18px">How many days a week can you play?</div>
  <div class="seg"><span>2</span><span>3</span><span class="sel">4</span><span>5</span></div>
  <div class="sub" style="margin-top:8px">Rest days are good for sore fingertips. Missing a day never resets anything.</div>
</div>
<div class="bottom">{hs("s05","Continue")}</div>''',
  why="The path makes the curriculum visible. A weekly rhythm with no streak to break replaces daily streaks.",
  hot=["Continue → Mic priming"])

S["s05"] = dict(name="Mic priming", group=1, body=f'''
{top("", "s04")}
<div class="pad" style="text-align:center">{progress(4,4)}
  <div class="circle" style="margin:26px auto 0">🎙</div>
  <div class="h" style="margin-top:16px">Let Justin's exercises listen</div>
  <div class="sub" style="margin:8px 6px 0">The app counts your chord changes so you can keep both hands on the guitar. Audio never leaves your phone.</div>
</div>
<div class="bottom">{hs("s06","Allow microphone")}{hs("s06","Not now: I'll tap to count","link")}</div>''',
  why="Explain the mic before the system prompt appears. Saying no still leads to a complete experience.",
  hot=["Allow → Today", "Not now → Today"])

S["s06"] = dict(name="Today", group=2, body=f'''
<div class="pad" style="padding-top:8px">
  <div class="cap">Tuesday</div><div class="h">Hey Sam</div>
  {hs("s12",f'<div class="cap">Your path to</div><b style="font-size:13px">Three Little Birds</b>{path_row([("A","done"),("D","done"),("E","now"),("♪","lock")])}<div class="sub" style="margin-top:6px">1 chord to go</div>',"card blk",style="margin-top:10px")}
  <div class="card" style="margin-top:8px">
    <div class="row sp"><b>Today · 10 min</b><span class="cap">Module 2</span></div>
    <div class="li"><span>▶ Meet the E chord</span><span>3m</span></div>
    <div class="li"><span>⏱ One Minute Changes · D ⇄ E</span><span>3m</span></div>
    <div class="li"><span>♪ Strum along · A–D</span><span>4m</span></div>
    {hs("s07","Start session",style="margin-top:8px;padding:9px")}
  </div>
  <div class="card row" style="margin-top:8px;gap:10px"><span class="dots"><i class="f"></i><i class="f"></i><i class="o"></i><i></i></span><span class="sub"><b>2 of 4 days</b> this week</span></div>
  {hs("s14",'Preview: what a comeback looks like ›',"link",style="margin-top:8px")}
</div>
{tabbar("Today")}''',
  why="Home is the Practice Assistant turned into one button. The path card shows the goal song every day.",
  hot=["Start session → Lesson", "Path card → Song unlocked (demo shortcut)", "Progress tab", "Comeback preview"])

S["s07"] = dict(name="Lesson video", group=2, body=f'''
{top("1 of 3 · Lesson", "s06", "✕")}
<div class="box" style="height:178px;margin:0 0 0 0;border-radius:0">Justin · Meet the E chord · 3:12</div>
<div class="pad">
  <div class="h2" style="margin-top:12px">The E chord</div>
  <div class="row" style="gap:12px;margin-top:10px;align-items:flex-start">
    <div class="box" style="width:96px;height:112px;flex:none">Chord diagram</div>
    <div style="flex:1">{lines(95,80,90,60)}<div class="tip">Tip: lots of beginners lift finger 1 too early. Keep it down.</div></div>
  </div>
</div>
<div class="bottom">{hs("s08","Next: One Minute Changes")}</div>''',
  why="Same lesson content as the website, so there are no dead references to videos missing from the app.",
  hot=["Next → One Minute Changes"])

S["s08"] = dict(name="OMC · ready", group=2, body=f'''
{top("2 of 3 · One Minute Changes", "s07", "?")}
<div class="pad" style="text-align:center">
  <div class="row" style="justify-content:center;gap:14px;margin-top:22px">{chord("D","big")}<span style="font-size:20px">⇄</span>{chord("E","big")}</div>
  <div class="sub" style="margin-top:14px">Switch between D and E as many times as you can in one minute. Clean changes only.</div>
  <div class="ring" style="margin:22px auto 0"><span>1:00</span></div>
  <div class="row sp card" style="margin-top:18px"><span class="sub">Your best</span><b>22</b><span class="sub">Justin's goal</span><b>60</b></div>
</div>
<div class="bottom">{hs("s09","Start (3·2·1)")}{hs("s09","Tap to count instead","link")}</div>''',
  why="A clear goal, a personal best and a fallback that doesn't need the mic, all before the timer starts.",
  hot=["Start → Counting"])

S["s09"] = dict(name="OMC · counting", group=2, body=f'''
{top("Listening…", None, "")}
<div class="pad" style="text-align:center">
  <div class="row" style="justify-content:center;gap:14px;margin-top:10px">{chord("D","lock big")}<span style="font-size:20px">⇄</span>{chord("E","done big")}</div>
  <div class="ring live" style="margin:22px auto 0"><span>27</span><em>0:21 left</em></div>
  <div class="wave">{"".join(f'<i style="height:{h}px"></i>' for h in [8,16,24,12,20,9,18,25,11,6,15,21,8,14])}</div>
  <div class="cap" style="margin-top:6px">E sounds clean ✓</div>
  <div class="card row sp" style="margin-top:14px"><span class="sub">On pace for</span><b>+5 vs best</b></div>
</div>
<div class="bottom">{hs("s10","Simulate: timer ends","btn ghost")}</div>''',
  why="Hands stay on the guitar. When detection is unsure it doesn't count and doesn't scold.",
  hot=["Timer ends → Result"])

S["s10"] = dict(name="OMC · result", group=2, body=f'''
{top("", None, "✕")}
<div class="pad" style="text-align:center">
  <div class="cap" style="margin-top:4px">New personal best</div>
  <div class="big">31</div>
  <div class="sub">D ⇄ E changes in one minute · +9 since Friday</div>
  <div class="card" style="margin-top:14px;text-align:left">
    <div class="row sp"><b>Last 7 tries</b><span class="cap">changes / min</span></div>
    <svg viewBox="0 0 220 70" width="100%" style="margin-top:6px"><line x1="0" y1="62" x2="220" y2="62" stroke="#ccc"/><polyline points="6,52 40,48 74,46 108,40 142,34 176,30 212,18" fill="none" stroke="#141414" stroke-width="2"/><circle cx="212" cy="18" r="4" fill="#FF7A00"/></svg>
  </div>
  <div class="quote">"Over 30 and the shapes start to become automatic. Lovely work." (Justin)</div>
</div>
<div class="bottom">{hs("s11","Continue")}</div>''',
  why="Turns progress you'd never notice into a number and a line. The only comparison is with the learner's own past.",
  hot=["Continue → Session done"])

S["s11"] = dict(name="Session done", group=2, body=f'''
<div class="pad" style="text-align:center;padding-top:30px">
  <div class="circle">✓</div>
  <div class="h" style="margin-top:14px">Session done</div>
  <div class="sub">10 min · that's 3 of 4 days this week</div>
  <div class="card" style="margin-top:16px;text-align:left">
    <div class="cap">Your path</div>{path_row([("A","done"),("D","done"),("E","done"),("♪","now")])}
    <div class="sub" style="margin-top:8px"><b>E is in the bag.</b> You know every chord in Three Little Birds.</div>
  </div>
</div>
<div class="bottom">{hs("s12","Unlock my song")}{hs("s06","Back to Today","link")}</div>''',
  why="Every session ends by showing how it moved the user along the path, which links the effort to the goal.",
  hot=["Unlock my song → Song unlocked", "Back to Today"])

S["s12"] = dict(name="Song unlocked", group=3, body=f'''
<div class="pad" style="text-align:center;padding-top:22px">
  <div class="box" style="height:100px">Celebration · waveform + sparkle animation</div>
  <div class="cap" style="margin-top:14px">✦ Song unlocked ✦</div>
  <div class="h">Three Little Birds</div>
  <div class="row" style="justify-content:center;gap:6px;margin-top:10px">{chord("A")}{chord("D")}{chord("E")}</div>
  <div class="card" style="margin-top:14px;text-align:left">
    <div class="row sp"><span class="sub">Tempo</span><b>70% → 100%</b></div>
    <div class="row sp" style="margin-top:6px"><span class="sub">Strum</span><b>↓ ↓ ↓ ↓</b></div>
    <div class="row sp" style="margin-top:6px"><span class="sub">Band &amp; vocals</span><b>On</b></div>
  </div>
</div>
<div class="bottom">{hs("s13","Play with the band")}<div class="link">Share my first song</div></div>''',
  why="The payoff. Instant Play starts slow so the first play-through feels like a success.",
  hot=["Play with the band → Play-along"])

S["s13"] = dict(name="Play-along", group=3, body=f'''
{top("Three Little Birds", "s12", "⚙")}
<div class="pad">
  <div class="row" style="gap:6px;margin-top:4px">{chord("A")}<span class="cap">next →</span>{chord("D","lock")}</div>
  <div class="lyr"><span class="c">A</span>Don't worry about a thing</div>
  <div class="lyr now"><span class="c">D</span>'Cause every little thing <span class="c">A</span>gonna be all right</div>
  <div class="lyr dim">Singin' don't worry about a thing</div>
  <div class="lyr dim"><span class="c">D</span>'Cause every little thing <span class="c">A</span>gonna be…</div>
  <div class="card" style="margin-top:12px"><div class="row sp"><span class="sub">Tempo</span><b>70%</b></div><div class="track"><div style="width:70%"></div></div>
  <div class="row sp" style="margin-top:8px"><span class="sub">Simplified chords</span><span class="tog on"></span></div></div>
</div>
<div class="bottom row" style="gap:8px"><span class="btn ghost" style="flex:1">❚❚</span>{hs("s06","Finish song",style="flex:3")}</div>''',
  why="The existing play-along player with Instant Play. Simplified chords are always available, so there are no dead ends.",
  hot=["Finish song → Today (next song on the path)"])

S["s14"] = dict(name="Comeback", group=3, body=f'''
<div class="pad" style="padding-top:6px">
  <div class="notif"><span class="appi"></span><div><div class="row sp"><b>JustinGuitar</b><span class="cap">now</span></div>Your fingers remember more than you think. Two minutes of D ⇄ E?</div></div>
  <div style="text-align:center;margin-top:22px"><div class="h">Welcome back, Sam</div>
  <div class="sub" style="margin-top:6px">Six days off is normal, and your calluses are still there.</div></div>
  <div class="card" style="margin-top:14px"><b>2-minute warm-up</b><div class="sub">A ⇄ D, then strum at 60%</div>{hs("s08","Ease back in",style="margin-top:8px;padding:9px")}</div>
  <div class="card" style="margin-top:8px"><b>Want a lighter rhythm?</b><div class="seg" style="margin-top:8px"><span>2</span><span class="sel">3</span><span>4</span></div></div>
  <div class="cap" style="text-align:center;margin-top:10px">Your path progress is safe · 2 of 3 chords</div>
</div>''',
  why="Re-entry is shorter than a normal session. No streak shaming, and lowering the goal counts as a success.",
  hot=["Ease back in → One Minute Changes"])

S["s15"] = dict(name="Progress", group=3, body=f'''
<div class="pad" style="padding-top:8px">
  <div class="cap">Your progress</div><div class="h">2.4× faster than on day 1</div>
  <div class="card" style="margin-top:10px"><div class="row sp"><b>Changes / min</b><span class="cap">A⇄D · D⇄E</span></div>
    <svg viewBox="0 0 220 80" width="100%" style="margin-top:6px"><line x1="0" y1="72" x2="220" y2="72" stroke="#ccc"/><polyline points="4,62 30,60 56,56 82,54 108,46 134,42 160,36 186,30 214,22" fill="none" stroke="#141414" stroke-width="2"/><polyline points="108,66 134,58 160,52 186,44 214,40" fill="none" stroke="#999" stroke-width="2" stroke-dasharray="4 3"/></svg></div>
  <div class="row" style="gap:8px;margin-top:8px"><div class="card" style="flex:1"><div class="big s">3</div><div class="cap">chords you own</div></div><div class="card" style="flex:1"><div class="big s">2h 40</div><div class="cap">played this month</div></div></div>
  <div class="card row" style="margin-top:8px;gap:8px"><span class="art"></span><span class="sub"><b>Songs you can play:</b> Three Little Birds</span></div>
  <div class="cap" style="margin-top:8px;text-align:center">✓ Synced with justinguitar.com · 2 min ago</div>
</div>
{tabbar("Progress")}''',
  why="Every skill shown is one the app actually measures. The sync status answers the most common store complaint.",
  hot=["Today tab"])

ORDER = list(S.keys())
GROUPS = {1: ("Onboarding", "From install to a personal path in under two minutes"),
          2: ("Daily practice loop", "Ten focused minutes, with progress made visible"),
          3: ("Payoff & return", "The first song, the play-along, coming back and progress")}

# ---------------------------------------------------------------- render
def phone(key, scale_cls=""):
    return f'<div class="ph {scale_cls}"><div class="sc"><div class="sb"><span>9:41</span><span class="isl"></span><span>▮▮▮</span></div>{S[key]["body"]}</div></div>'

def thumb(key, z):
    html = phone(key, "th").replace('class="ph th"', f'class="ph th" style="zoom:{z}"', 1)
    # thumbnails link to their prototype page; strip inner links
    html = re.sub(r'<a class="hs ([^"]*)" href="#[^"]*"', r'<span class="\1"', html).replace("</a>", "</span>")
    i = ORDER.index(key) + 1
    return f'<a class="tw" href="#{key}">{html}<div class="tl"><b>{i:02d}</b> {S[key]["name"]}</div><div class="tn" style="width:{int(290*z)}px">{S[key]["why"]}</div></a>'

CSS = open("wireframes.css").read()
pages = []

pages.append(f'''<section class="page cover">
  <div class="kick">Musopia · Senior Product Designer application · Kira Krysanov</div>
  <h1>First 30 Days<br><span>Wireframes &amp; clickable prototype</span></h1>
  <p class="lead">15 screens across onboarding, the daily practice loop and the payoff moments. These are the low-fidelity companion to the "First 30 Days" concept deck.</p>
  <div class="how">
    <div><b>1</b><span>Open this PDF in a viewer that supports links: Preview, Acrobat or a browser.</span></div>
    <div><b>2</b><span>Jump to {hs("s01","▶ Start the prototype","inl")} or pick a screen from the flow maps.</span></div>
    <div><b>3</b><span>Tap anything outlined in <i class="o">orange</i>. That's a hotspot. "Flow map" on every page brings you back.</span></div>
  </div>
  <div class="mini">{"".join(f'<a href="#{k}"><b>{i+1:02d}</b> {S[k]["name"]}</a>' for i,k in enumerate(ORDER))}</div>
  <div class="disc">Independent, unsolicited concept, not affiliated with Musopia or JustinGuitar. Song titles and data are illustrative.</div>
</section>''')

for g, (gname, gsub) in GROUPS.items():
    keys = [k for k in ORDER if S[k]["group"] == g]
    z = {1: .52, 2: .45, 3: .58}[g]
    arrows = '<span class="arr">→</span>'.join(thumb(k, z) for k in keys)
    pages.append(f'''<section class="page" id="flow{g}">
  <div class="kick">Flow map {g} of 3</div><h2>{gname}</h2><p class="lead s">{gsub}</p>
  <div class="flow">{arrows}</div>
  <div class="foot"><span>First 30 Days · wireframes · Kira Krysanov</span><span>Tap a screen to open it in the prototype</span></div>
</section>''')

for i, k in enumerate(ORDER):
    s = S[k]
    prev_k = ORDER[i - 1] if i else None
    next_k = ORDER[i + 1] if i + 1 < len(ORDER) else None
    navs = []
    if prev_k: navs.append(f'<a href="#{prev_k}">‹ {S[prev_k]["name"]}</a>')
    navs.append(f'<a href="#flow{s["group"]}">Flow map</a>')
    if next_k: navs.append(f'<a href="#{next_k}">{S[next_k]["name"]} ›</a>')
    hot = "".join(f"<li>{h}</li>" for h in s["hot"])
    pages.append(f'''<section class="page proto" id="{k}">
  <div class="stage">{phone(k)}</div>
  <div class="side">
    <div class="kick">Prototype · {GROUPS[s["group"]][0]}</div>
    <div class="idx">{i+1:02d}<span>/15</span></div>
    <h2>{s["name"]}</h2>
    <p class="why">{s["why"]}</p>
    <div class="hl">Hotspots</div><ul>{hot}</ul>
    <div class="pn">{"".join(navs)}</div>
  </div>
  <div class="foot"><span>First 30 Days · clickable prototype · Kira Krysanov</span><span>Orange outline = tap target</span></div>
</section>''')

pages.append('''<section class="page cover end">
  <h1>Thanks for clicking through.<br><span>Happy to walk you through it live.</span></h1>
  <p class="lead">Kira Krysanov · kira.krysanov@gmail.com</p>
  <p class="lead s">Next steps I'd take: test this flow with 5 or 6 beginners holding a real guitar, check mic detection accuracy with engineering, then A/B test the onboarding and the weekly rhythm.</p>
</section>''')

html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>First 30 Days Wireframes</title>
<link href="fonts/fonts.css" rel="stylesheet"><style>{CSS}</style></head>
<body>{"".join(pages)}</body></html>'''
open("wireframes.html", "w").write(html)
print("pages:", len(pages))
