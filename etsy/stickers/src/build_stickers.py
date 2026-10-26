"""Builds the tennis sticker designs (stickers.html), one element per sticker. Run: python3 build_stickers.py"""
import json
from pathlib import Path

G, N, R, C, Y, GOLD, SKY, W = "#1F6B3B", "#1B2B4B", "#C2412D", "#F6EDD9", "#D7F04A", "#E0B44C", "#9CC3E6", "#FFFFFF"
FONTS = ("https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,800;1,9..144,400;1,9..144,700"
         "&family=Barlow+Semi+Condensed:wght@600;700;800&family=Anton&display=swap")


def svg(body, w=200, h=200):
    return f'<svg viewBox="0 0 {w} {h}" width="{w}" height="{h}" xmlns="http://www.w3.org/2000/svg">{body}</svg>'


def seams(cx=100, cy=100, r=88, color=W, w=8):
    k = r * 0.83
    return (f'<path d="M{cx-k} {cy-r*.55} C{cx-r*.35} {cy-r*.25} {cx-r*.35} {cy+r*.25} {cx-k} {cy+r*.55}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>'
            f'<path d="M{cx+k} {cy-r*.55} C{cx+r*.35} {cy-r*.25} {cx+r*.35} {cy+r*.25} {cx+k} {cy+r*.55}" fill="none" stroke="{color}" stroke-width="{w}" stroke-linecap="round"/>')


def ball(fill=Y, cx=100, cy=100, r=88, stroke=N):
    return f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" stroke="{stroke}" stroke-width="{max(r/14, 2.5):.1f}"/>' + seams(cx, cy, r, W, r / 11)


def racquet(frame=R, grip=N):
    strings = "".join(f'<line x1="{x}" y1="0" x2="{x}" y2="140" stroke="#C9C2B0" stroke-width="2"/>' for x in range(56, 150, 11))
    strings += "".join(f'<line x1="40" y1="{y}" x2="160" y2="{y}" stroke="#C9C2B0" stroke-width="2"/>' for y in range(14, 136, 11))
    wraps = "".join(f'<line x1="91" y1="{y}" x2="109" y2="{y + 6}" stroke="{C}" stroke-width="2.5"/>' for y in range(156, 190, 8))
    return (f'<clipPath id="h{frame[1:]}"><ellipse cx="100" cy="72" rx="48" ry="58"/></clipPath>'
            f'<ellipse cx="100" cy="72" rx="48" ry="58" fill="{W}"/><g clip-path="url(#h{frame[1:]})">{strings}</g>'
            f'<ellipse cx="100" cy="72" rx="48" ry="58" fill="none" stroke="{frame}" stroke-width="10"/>'
            f'<path d="M74 118 L100 150 L126 118" fill="none" stroke="{frame}" stroke-width="9" stroke-linejoin="round"/>'
            f'<rect x="90" y="148" width="20" height="46" rx="5" fill="{grip}"/>{wraps}')


def court(fill=G):
    return (f'<rect x="40" y="6" width="120" height="188" rx="6" fill="{fill}" stroke="{N}" stroke-width="5"/>'
            '<g fill="none" stroke="#fff" stroke-width="3"><rect x="52" y="18" width="96" height="164"/>'
            '<line x1="64" y1="18" x2="64" y2="182"/><line x1="136" y1="18" x2="136" y2="182"/>'
            '<line x1="64" y1="58" x2="136" y2="58"/><line x1="64" y1="142" x2="136" y2="142"/>'
            '<line x1="100" y1="58" x2="100" y2="142"/></g><line x1="44" y1="100" x2="156" y2="100" stroke="' + N + '" stroke-width="5"/>'
            + ball(Y, 122, 76, 9))


def cloud(fill=W):
    return (f'<path d="M50 140 C25 140 22 105 48 100 C46 70 82 58 98 80 C108 55 150 58 150 92 C178 92 182 140 150 140 Z" '
            f'fill="{fill}" stroke="{N}" stroke-width="6" stroke-linejoin="round"/>')


ICONS = {
    "ball": svg(ball()),
    "ball-red": svg(ball(R)),
    "racquet": svg(racquet()),
    "racquet-green": svg(racquet(G)),
    "crossed-racquets": svg(f'<g transform="rotate(-32 100 100) translate(10 8) scale(.9)">{racquet(R)}</g>'
                            f'<g transform="rotate(32 100 100) translate(10 8) scale(.9)">{racquet(G)}</g>' + ball(Y, 100, 168, 18)),
    "trophy": svg(f'<path d="M58 70 C30 70 28 110 66 112" fill="none" stroke="{N}" stroke-width="9"/>'
                  f'<path d="M142 70 C170 70 172 110 134 112" fill="none" stroke="{N}" stroke-width="9"/>'
                  f'<path d="M55 36 H145 V72 C145 108 124 128 100 130 C76 128 55 108 55 72 Z" fill="{GOLD}" stroke="{N}" stroke-width="6"/>'
                  f'<rect x="90" y="128" width="20" height="24" fill="{GOLD}" stroke="{N}" stroke-width="5"/>'
                  f'<rect x="62" y="150" width="76" height="22" rx="4" fill="{N}"/>' + ball(Y, 100, 78, 18)),
    "medal": svg(f'<polygon points="62,12 92,12 112,92 82,92" fill="{R}" stroke="{N}" stroke-width="5"/>'
                 f'<polygon points="138,12 108,12 88,92 118,92" fill="{G}" stroke="{N}" stroke-width="5"/>'
                 f'<circle cx="100" cy="132" r="50" fill="{GOLD}" stroke="{N}" stroke-width="6"/>'
                 f'<polygon points="100,104 108,124 130,125 113,138 119,159 100,147 81,159 87,138 70,125 92,124" fill="{C}" stroke="{N}" stroke-width="3"/>'),
    "ball-tube": svg(f'<rect x="66" y="30" width="68" height="154" rx="16" fill="{C}" stroke="{N}" stroke-width="6"/>'
                     f'<rect x="60" y="18" width="80" height="26" rx="7" fill="{R}" stroke="{N}" stroke-width="6"/>'
                     f'<rect x="69" y="88" width="62" height="54" fill="{G}"/>' + ball(Y, 100, 115, 17)),
    "court": svg(court()),
    "court-clay": svg(court("#B8572F")),
    "net": svg(f'<rect x="18" y="58" width="12" height="112" rx="3" fill="{N}"/><rect x="170" y="58" width="12" height="112" rx="3" fill="{N}"/>'
               f'<rect x="30" y="72" width="140" height="70" fill="{C}" stroke="{N}" stroke-width="4"/>'
               + "".join(f'<line x1="{x}" y1="72" x2="{x}" y2="142" stroke="{N}" stroke-width="2"/>' for x in range(40, 170, 10))
               + "".join(f'<line x1="30" y1="{y}" x2="170" y2="{y}" stroke="{N}" stroke-width="2"/>' for y in range(82, 142, 10))
               + f'<rect x="26" y="64" width="148" height="12" rx="3" fill="{W}" stroke="{N}" stroke-width="4"/>' + ball(Y, 150, 44, 16)),
    "water-bottle": svg(f'<rect x="84" y="20" width="32" height="26" rx="6" fill="{N}"/>'
                        f'<rect x="70" y="44" width="60" height="140" rx="20" fill="{G}" stroke="{N}" stroke-width="6"/>'
                        f'<rect x="73" y="96" width="54" height="42" fill="{C}"/>' + ball(Y, 100, 117, 13)),
    "cap": svg(f'<path d="M110 122 L186 128 C192 130 192 146 184 148 L110 144 Z" fill="{N}" stroke="{N}" stroke-width="4" stroke-linejoin="round"/>'
               f'<path d="M14 134 C14 60 56 34 92 34 C128 34 152 64 152 134 Z" fill="{R}" stroke="{N}" stroke-width="6" stroke-linejoin="round"/>'
               f'<path d="M92 36 V134 M54 48 C64 80 66 108 64 134 M130 48 C120 80 118 108 120 134" fill="none" stroke="{N}" stroke-width="3"/>'
               f'<rect x="10" y="126" width="146" height="14" rx="6" fill="{C}" stroke="{N}" stroke-width="4"/>'
               f'<circle cx="92" cy="34" r="8" fill="{N}"/>'),
    "heart-ball": svg(f'<path d="M100 172 C40 132 18 98 18 70 C18 44 38 26 62 26 C80 26 92 36 100 50 C108 36 120 26 138 26 C162 26 182 44 182 70 C182 98 160 132 100 172 Z" '
                      f'fill="{R}" stroke="{N}" stroke-width="6"/>'
                      f'<path d="M44 52 C68 74 68 104 52 122 M156 52 C132 74 132 104 148 122" fill="none" stroke="{W}" stroke-width="7" stroke-linecap="round"/>'),
    "scoreboard": svg(f'<rect x="20" y="46" width="160" height="108" rx="10" fill="{N}"/>'
                      + "".join(f'<rect x="{x}" y="{y}" width="26" height="30" rx="3" fill="{C}"/>' for x in (92, 122, 152) for y in (60, 108))
                      + "".join(f'<text x="{x + 13}" y="{y + 23}" font-family="Barlow Semi Condensed" font-weight="800" font-size="22" text-anchor="middle" fill="{N}">{t}</text>'
                                for (x, y), t in zip([(92, 60), (122, 60), (152, 60), (92, 108), (122, 108), (152, 108)], "647365"))
                      + f'<text x="32" y="83" font-family="Barlow Semi Condensed" font-weight="800" font-size="20" fill="{Y}">ME</text>'
                      + f'<text x="32" y="131" font-family="Barlow Semi Condensed" font-weight="800" font-size="20" fill="{C}">OPP</text>', 200, 200),
    "lightning": svg(f'<polygon points="118,10 46,112 94,112 78,190 156,80 106,80" fill="{Y}" stroke="{N}" stroke-width="7" stroke-linejoin="round"/>'),
    "sun": svg("".join(f'<line x1="100" y1="16" x2="100" y2="40" stroke="{N}" stroke-width="8" stroke-linecap="round" transform="rotate({a} 100 100)"/>' for a in range(0, 360, 45))
               + f'<circle cx="100" cy="100" r="46" fill="{GOLD}" stroke="{N}" stroke-width="7"/>'),
    "cloud": svg(cloud()),
    "rain": svg(cloud(SKY) + "".join(f'<line x1="{x}" y1="152" x2="{x - 8}" y2="176" stroke="{N}" stroke-width="7" stroke-linecap="round"/>' for x in (66, 100, 134))),
    "wind": svg(f'<path d="M24 74 H126 C150 74 152 40 128 40 C112 40 108 56 116 62" fill="none" stroke="{N}" stroke-width="10" stroke-linecap="round"/>'
                f'<path d="M24 108 H150 C176 108 178 146 150 146 C134 146 128 130 138 122" fill="none" stroke="{G}" stroke-width="10" stroke-linecap="round"/>'
                f'<path d="M24 140 H92" fill="none" stroke="{N}" stroke-width="10" stroke-linecap="round"/>'),
    "string-reel": svg(f'<circle cx="100" cy="100" r="78" fill="{N}"/><circle cx="100" cy="100" r="58" fill="{G}"/>'
                       + "".join(f'<circle cx="100" cy="100" r="{r}" fill="none" stroke="{Y}" stroke-width="3"/>' for r in (52, 44, 36))
                       + f'<circle cx="100" cy="100" r="22" fill="{C}" stroke="{N}" stroke-width="5"/>'
                       f'<path d="M150 46 C176 30 186 54 172 66" fill="none" stroke="{Y}" stroke-width="4"/>'),
    "sweatband": svg(f'<ellipse cx="100" cy="100" rx="74" ry="56" fill="{R}" stroke="{N}" stroke-width="6"/>'
                     f'<ellipse cx="100" cy="100" rx="46" ry="30" fill="{W}" stroke="{N}" stroke-width="6"/>'
                     f'<path d="M30 92 C60 58 140 58 170 92" fill="none" stroke="{C}" stroke-width="8"/>'),
}

# Word stickers: (style, text, background, text colour)
WORDS = [
    ("pill", "Match day", G, C), ("pill", "Practice", N, C), ("pill", "Lesson", Y, N), ("pill", "Tournament", R, C),
    ("pill", "League night", N, Y), ("pill", "Doubles", G, Y), ("pill", "Singles", C, N), ("pill", "Rest day", C, G),
    ("pill", "Gym", N, C), ("pill", "Recovery", G, C), ("pill", "Restring", R, C), ("pill", "Warm up", Y, N),
    ("pill", "Travel day", C, R), ("pill", "Team practice", R, C),
    ("banner", "Game · Set · Match", R, C), ("banner", "Love all", G, C), ("banner", "Finals", N, Y), ("banner", "Qualified", G, C),
    ("badge", "Win", G, C), ("badge", "Loss", N, C), ("burst", "Ace!", Y, N), ("badge", "Deuce", R, C), ("burst", "New PB", Y, R),
    ("tag", "Break point", N, C), ("tag", "Set point", G, C), ("tag", "Match point", R, C), ("tag", "Tie-break", Y, N),
    ("script", "Game face", R, None), ("script", "Let’s go!", G, None), ("script", "Vamos!", N, None), ("script", "Come on!", R, None),
]

QUOTES = [
    ("One point<br>at a time", G, C), ("Play the ball,<br>not the opponent", N, C), ("Born to<br>rally", R, C),
    ("Tennis is my<br>therapy", Y, N), ("Eat · Sleep ·<br>Tennis · Repeat", C, N), ("Nerves mean<br>it matters", G, Y),
]

PLANNER = {
    "scorecard": f'''<div class="card" style="width:250px"><div class="clbl">Score</div><table class="sc"><tr><th></th><th>1</th><th>2</th><th>3</th></tr>
        <tr><td>Me</td><td></td><td></td><td></td></tr><tr><td>Opp</td><td></td><td></td><td></td></tr></table></div>''',
    "versus": f'<div class="card row" style="width:250px"><span class="big">vs</span><span class="line"></span></div>',
    "court-time": f'<div class="card row" style="width:270px"><span class="clbl">Court</span><span class="line s"></span><span class="clbl">Time</span><span class="line s"></span></div>',
    "result-w": f'<div class="dot" style="background:{G};color:{C}">W</div>',
    "result-l": f'<div class="dot" style="background:{R};color:{C}">L</div>',
    "bag-checklist": '<div class="card" style="width:200px"><div class="clbl">Match bag</div>'
                     + "".join(f'<div class="chk">{x}</div>' for x in ("Racquets", "Water", "Balls", "Snacks", "Towel")) + "</div>",
    "week-dots": '<div class="card row" style="width:300px;gap:6px">' + "".join(f'<span class="wd">{d}</span>' for d in "MTWTFSS") + "</div>",
    "todays-focus": '<div class="card" style="width:240px"><div class="clbl">Today’s focus</div><div class="ln"></div><div class="ln"></div></div>',
    "energy": f'<div class="card row" style="width:230px"><span class="clbl">Energy</span><span class="bat">{"<i></i>" * 5}</span></div>',
    "date": '<div class="card dc"><div class="clbl">Date</div></div>',
}

CSS = f"""
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{ background: transparent; font-family: 'Barlow Semi Condensed', sans-serif; }}
.wrap {{ display: flex; flex-wrap: wrap; gap: 30px; padding: 30px; width: 1500px; align-items: center; }}
.st {{ display: inline-block; padding: 16px; }}
.cut {{ filter: drop-shadow(4px 0 0 #fff) drop-shadow(-4px 0 0 #fff) drop-shadow(0 4px 0 #fff) drop-shadow(0 -4px 0 #fff)
        drop-shadow(3px 3px 0 #fff) drop-shadow(-3px -3px 0 #fff) drop-shadow(0 3px 5px rgba(0,0,0,.28)); }}
.cut svg {{ display: block; width: 150px; height: 150px; }}
.pill {{ border-radius: 999px; padding: 12px 26px; font-weight: 800; font-size: 26px; letter-spacing: 3px; text-transform: uppercase; border: 3px solid {N}; white-space: nowrap; }}
.banner {{ padding: 14px 54px; font-family: 'Fraunces', serif; font-weight: 800; font-size: 30px; white-space: nowrap;
          clip-path: polygon(0 0, 100% 0, calc(100% - 22px) 50%, 100% 100%, 0 100%, 22px 50%); }}
.badge {{ width: 130px; height: 130px; border-radius: 50%; display: flex; align-items: center; justify-content: center;
          font-family: 'Fraunces', serif; font-weight: 800; font-size: 34px; border: 4px solid {N}; box-shadow: inset 0 0 0 6px rgba(255,255,255,.55); }}
.burst {{ width: 150px; height: 150px; display: flex; align-items: center; justify-content: center; font-family: 'Anton', sans-serif; font-size: 34px;
          text-transform: uppercase; letter-spacing: 1px;
          clip-path: polygon(50% 0, 61% 18%, 82% 9%, 80% 31%, 100% 38%, 86% 54%, 98% 73%, 76% 76%, 73% 98%, 55% 86%, 38% 100%, 31% 79%, 9% 82%, 16% 60%, 0 45%, 18% 33%, 12% 12%, 34% 16%); }}
.tag {{ padding: 12px 22px 12px 44px; font-weight: 800; font-size: 24px; letter-spacing: 2.5px; text-transform: uppercase; white-space: nowrap; position: relative;
        clip-path: polygon(20px 0, 100% 0, 100% 100%, 20px 100%, 0 50%); }}
.tag::before {{ content: ""; position: absolute; left: 22px; top: 50%; width: 10px; height: 10px; margin-top: -5px; border-radius: 50%; background: {C}; }}
.script {{ font-family: 'Fraunces', serif; font-style: italic; font-weight: 700; font-size: 54px; white-space: nowrap; padding: 4px 8px; }}
.quote {{ padding: 22px 28px; font-family: 'Fraunces', serif; font-weight: 800; font-size: 30px; line-height: 1.12; text-align: center; border: 3px solid {N}; border-radius: 14px; }}
.card {{ background: {W}; border: 3px solid {N}; border-radius: 12px; padding: 12px 14px; color: {N}; }}
.card.row {{ display: flex; align-items: center; gap: 10px; }}
.clbl {{ font-weight: 800; font-size: 15px; letter-spacing: 2.5px; text-transform: uppercase; color: {R}; }}
.big {{ font-family: 'Fraunces', serif; font-style: italic; font-weight: 700; font-size: 34px; color: {G}; }}
.line {{ flex: 1; border-bottom: 2.5px solid {N}; height: 26px; }}
.line.s {{ height: 22px; }}
.sc {{ border-collapse: collapse; width: 100%; margin-top: 6px; }}
.sc th {{ font-size: 14px; color: {G}; font-weight: 800; }}
.sc td {{ border: 2px solid {N}; height: 30px; font-weight: 800; font-size: 15px; text-transform: uppercase; text-align: center; }}
.sc td:first-child {{ width: 58px; border-left: none; text-align: left; }}
.dot {{ width: 70px; height: 70px; border-radius: 50%; border: 4px solid {N}; display: flex; align-items: center; justify-content: center;
        font-family: 'Fraunces', serif; font-weight: 800; font-size: 34px; }}
.chk {{ display: flex; align-items: center; gap: 8px; font-weight: 700; font-size: 18px; height: 28px; border-bottom: 1.5px solid #E2D6BA; }}
.chk::before {{ content: ""; width: 14px; height: 14px; border: 2.5px solid {G}; border-radius: 3px; }}
.wd {{ width: 32px; height: 32px; border-radius: 50%; border: 2.5px solid {G}; display: flex; align-items: center; justify-content: center; font-weight: 800; font-size: 15px; }}
.ln {{ border-bottom: 2px solid {N}; height: 28px; }}
.bat {{ display: flex; gap: 4px; border: 3px solid {N}; border-radius: 6px; padding: 4px; position: relative; }}
.bat::after {{ content: ""; position: absolute; right: -9px; top: 9px; width: 5px; height: 12px; background: {N}; border-radius: 0 3px 3px 0; }}
.bat i {{ width: 18px; height: 20px; border-radius: 2px; background: {G}; }}
.bat i:nth-child(n+4) {{ background: #E2D6BA; }}
.dc {{ width: 110px; height: 110px; border-radius: 50%; display: flex; align-items: flex-start; justify-content: center; padding-top: 22px; }}
"""


def slug(text):
    return "".join(c if c.isalnum() else "-" for c in text.lower().replace("’", "")).strip("-").replace("--", "-").replace("--", "-")


stickers = []  # (id, category, html)
for k, s in ICONS.items():
    stickers.append((f"icon-{k}", "icons", f'<div class="cut">{s}</div>'))
for style, text, bg, fg in WORDS:
    inner = (f'<div class="{style}" style="color:{bg}">{text}</div>' if style == "script"
             else f'<div class="{style}" style="background:{bg};color:{fg}">{text}</div>')
    stickers.append((f"word-{slug(text)}", "words", f'<div class="cut">{inner}</div>'))
for k, html in PLANNER.items():
    stickers.append((f"planner-{k}", "planner", f'<div class="cut">{html}</div>'))
for text, bg, fg in QUOTES:
    stickers.append((f"quote-{slug(text.replace('<br>', ' '))}", "quotes",
                     f'<div class="cut"><div class="quote" style="background:{bg};color:{fg}">{text}</div></div>'))

body = "".join(f'<div class="st" id="{sid}" data-cat="{cat}">{html}</div>' for sid, cat, html in stickers)
here = Path(__file__).parent
(here / "stickers.html").write_text(f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}">'
                                    f'<style>{CSS}</style></head><body><div class="wrap">{body}</div></body></html>')
(here / "stickers.json").write_text(json.dumps([{"id": s, "cat": c} for s, c, _ in stickers], indent=1))
print(len(stickers), "stickers")
