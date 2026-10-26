"""Builds the Etsy listing-image slides for one style. Run: python3 build_listing.py <club|retro|rally>"""
import sys
from pathlib import Path

THEME = sys.argv[1] if len(sys.argv) > 1 else "club"

FONTS = {
    "club": "family=Bodoni+Moda:ital@0;1&family=Cormorant+Garamond:ital,wght@0,400;0,500;1,400&family=Montserrat:wght@400;500;600",
    "retro": "family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,800;1,9..144,400&family=Barlow+Semi+Condensed:wght@500;600;700",
    "rally": "family=Anton&family=Inter:wght@400;500;600;700",
}

# Per-style tokens: dark and light slide colours, fonts, and how the big titles are painted.
TOKENS = {
    "club": """
  --dark-bg: radial-gradient(ellipse at 28% 40%, #2B5440 0%, #1D3A2A 60%, #152B1F 100%); --dark-ink: #EFE3C2; --dark-accent: #D6BE82;
  --light-bg: radial-gradient(ellipse at 50% 30%, #FFFDF6 0%, #EEE6D2 85%); --light-ink: #1D3A2A; --light-accent: #A07F42; --light-em: #7E6230;
  --display: 'Bodoni Moda', serif; --serif: 'Cormorant Garamond', serif; --sans: 'Montserrat', sans-serif;
  --title-dark: linear-gradient(120deg, #7E6230 0%, #B39457 25%, #E6D3A0 47%, #C2A263 64%, #8A6C35 86%, #B8975A 100%);
  --rule: linear-gradient(90deg, #8A6C35, #E6D3A0, #8A6C35); --frame: #0E1511; --frame-edge: #2F3B33; --chip: rgba(214,190,130,.6);
  --title-weight: 400; --title-case: none; --title-spacing: 0;""",
    "retro": """
  --dark-bg: #1B2B4B; --dark-ink: #F6EDD9; --dark-accent: #E2614B;
  --light-bg: #F6EDD9; --light-ink: #1B2B4B; --light-accent: #C2412D; --light-em: #C2412D;
  --display: 'Fraunces', serif; --serif: 'Fraunces', serif; --sans: 'Barlow Semi Condensed', sans-serif;
  --title-dark: linear-gradient(#F6EDD9, #F6EDD9);
  --rule: linear-gradient(to bottom, #1F6B3B 0 3px, transparent 3px 6px, #C2412D 6px 9px); --frame: #14213A; --frame-edge: #2E3F63; --chip: rgba(246,237,217,.6);
  --title-weight: 800; --title-case: none; --title-spacing: -2px;""",
    "rally": """
  --dark-bg: #111111; --dark-ink: #FFFFFF; --dark-accent: #D7F04A;
  --light-bg: #FFFFFF; --light-ink: #111111; --light-accent: #111111; --light-em: #111111;
  --display: 'Anton', sans-serif; --serif: 'Inter', sans-serif; --sans: 'Inter', sans-serif;
  --title-dark: linear-gradient(#D7F04A, #D7F04A);
  --rule: linear-gradient(#D7F04A, #D7F04A); --frame: #1C1C1C; --frame-edge: #3A3A3A; --chip: rgba(255,255,255,.55);
  --title-weight: 400; --title-case: uppercase; --title-spacing: 1px;""",
}

# Extra per-style decoration.
EXTRA = {
    "club": "",
    "retro": """
.hero { background: #F6EDD9; color: #1B2B4B; }
.hero::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 120px;
  background: repeating-linear-gradient(90deg, #1F6B3B 0 60px, #F6EDD9 60px 120px); }
.hero::after { content: ""; position: absolute; top: 120px; left: 0; right: 0; height: 30px;
  background: radial-gradient(circle at 30px 0, #1F6B3B 29px, transparent 30px) 0 0 / 120px 30px repeat-x; }
.hero .ttl { background: none; -webkit-background-clip: border-box; background-clip: border-box; color: #1B2B4B; }
.hero .ttl em { color: #C2412D; }
.hero .k { color: #1F6B3B; } .hero .sub { color: #1F6B3B; } .hero .compat { color: #1B2B4B; }
.hero .badges span { border-color: #1B2B4B; color: #1B2B4B; }
.dark .ttl em { color: #E2614B; -webkit-text-fill-color: #E2614B; }
.light h2 em { font-style: italic; }
.rule { height: 9px; }
""",
    "rally": """
.hero { background: #D7F04A; color: #111; }
.hero .ttl { background: none; -webkit-background-clip: border-box; background-clip: border-box; color: #111; }
.hero .k, .hero .sub, .hero .compat { color: #111; }
.hero .badges span { border: 2px solid #111; color: #111; font-weight: 700; }
.hero .rule { background: #111; }
h1 { line-height: .9; }
h2 { line-height: 1.12; }
.light h2 em { background: #D7F04A; padding: 0 10px; font-style: normal; -webkit-box-decoration-break: clone; box-decoration-break: clone; }
.sub { font-style: normal !important; font-weight: 600; text-transform: uppercase; letter-spacing: 3px; font-size: 26px !important; }
.list div, .grid figcaption, .call, .files div b { font-style: normal !important; }
.call b, .files .ic { border-radius: 0; }
""",
}

EDITION = {"club": "Club Edition", "retro": "Retro Club Edition", "rally": "Rally Edition"}


def p(name):
    return f"previews/{THEME}/{name}.png"


CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
:root {%TOKENS%}
.slide { width: 1600px; height: 1200px; position: relative; overflow: hidden; font-family: var(--sans); }
.dark, .hero { background: var(--dark-bg); color: var(--dark-ink); }
.light { background: var(--light-bg); color: var(--light-ink); }
.k { font-size: 15px; letter-spacing: 7px; text-transform: uppercase; font-weight: 600; color: var(--dark-accent); }
.light .k { color: var(--light-accent); }
h1, h2 { font-family: var(--display); font-weight: var(--title-weight); text-transform: var(--title-case); letter-spacing: var(--title-spacing); }
h1 { font-size: 118px; line-height: 1; }
h2 { font-size: 78px; line-height: 1.05; }
h1 em, h2 em { font-style: italic; }
.ttl { background: var(--title-dark); -webkit-background-clip: text; background-clip: text; color: transparent; }
.light h2 { color: var(--light-ink); }
.light h2 em { color: var(--light-em); }
.sub { font-family: var(--serif); font-size: 40px; font-style: italic; margin-top: 22px; }
.rule { height: 3px; width: 130px; background: var(--rule); margin: 34px 0; }
.badges { display: flex; gap: 14px; flex-wrap: wrap; }
.badges span { border: 1px solid var(--chip); padding: 14px 22px; font-size: 15px; letter-spacing: 4px; text-transform: uppercase; font-weight: 600; }
.compat { margin-top: 40px; font-size: 16px; letter-spacing: 3px; text-transform: uppercase; opacity: .8; }
.dev { position: absolute; border-radius: 28px; background: var(--frame); padding: 22px; box-shadow: 0 40px 80px rgba(0,0,0,.45), 0 0 0 2px var(--frame-edge); }
.dev img { display: block; width: 100%; border-radius: 6px; }
.grid { position: absolute; inset: 250px 80px 60px; display: grid; grid-template-columns: repeat(6, 1fr); gap: 28px; }
.grid figure { display: flex; flex-direction: column; align-items: center; }
.grid img { width: 100%; box-shadow: 0 18px 36px rgba(0,0,0,.18); }
.grid figcaption { font-family: var(--serif); font-size: 24px; margin-top: 14px; font-style: italic; }
.list div { font-family: var(--serif); font-size: 31px; border-top: 1px solid currentColor; border-color: rgba(127,127,127,.35); padding: 14px 0; }
.list div small { display: block; font-family: var(--sans); font-size: 13px; letter-spacing: 3px; text-transform: uppercase; font-weight: 600; color: var(--dark-accent); margin-bottom: 4px; }
.light .list div small { color: var(--light-accent); }
.call { position: absolute; display: flex; align-items: center; gap: 20px; font-family: var(--serif); font-size: 32px; }
.call b { width: 46px; height: 46px; border: 2px solid var(--dark-accent); border-radius: 50%; display: flex; align-items: center; justify-content: center;
  font-family: var(--sans); font-size: 17px; color: var(--dark-accent); flex: none; }
.call small { display: block; font-family: var(--sans); font-size: 16px; opacity: .7; margin-top: 6px; }
.screen { position: absolute; background: #0E0E0E; border-radius: 22px 22px 0 0; padding: 20px 20px 26px; box-shadow: 0 40px 80px rgba(0,0,0,.35); }
.screen img { display: block; width: 100%; background: #fff; }
.base { position: absolute; height: 26px; background: linear-gradient(#C9CCC6, #8E928B); border-radius: 0 0 20px 20px; }
.files { display: grid; grid-template-columns: repeat(3, 1fr); gap: 34px; position: absolute; left: 110px; right: 110px; top: 400px; }
.files div { border: 1px solid rgba(127,127,127,.4); padding: 64px 36px; text-align: center; }
.files .ic { width: 92px; height: 92px; margin: 0 auto 26px; border: 2px solid var(--light-accent); border-radius: 50%; display: flex; align-items: center;
  justify-content: center; font-family: var(--sans); font-weight: 700; font-size: 20px; letter-spacing: 2px; color: var(--light-accent); }
.files b { display: block; font-family: var(--serif); font-size: 38px; font-weight: 500; margin-bottom: 12px; }
.files span { font-size: 20px; line-height: 1.6; opacity: .8; }
.steps3 { position: absolute; left: 160px; right: 160px; bottom: 210px; display: flex; justify-content: space-between; font-size: 18px; letter-spacing: 3px; text-transform: uppercase; font-weight: 600; }
.steps3 span b { color: var(--light-accent); margin-right: 10px; }
"""


def slides():
    ed = EDITION[THEME]
    return f"""
<section class="slide hero" id="s1">
  <div style="position:absolute;left:110px;top:230px;width:640px">
    <div class="k">Tennis journal &middot; {ed}</div>
    <h1 class="ttl" style="margin-top:30px">The <em>Match</em><br>Book</h1>
    <div class="sub">Journal &amp; Stats Tracker</div>
    <div class="rule"></div>
    <div class="badges"><span>131 Pages</span><span>Hyperlinked</span><span>+ Stats Sheet</span></div>
    <div class="compat">GoodNotes &middot; Notability &middot; Print &middot; Google Sheets</div>
  </div>
  <div class="dev" style="width:470px;left:1050px;top:190px;transform:rotate(4deg)"><img src="{p('m01-post')}"></div>
  <div class="dev" style="width:500px;left:770px;top:270px;transform:rotate(-5deg)"><img src="{p('cover')}"></div>
</section>

<section class="slide light" id="s2">
  <div style="position:absolute;top:80px;left:0;right:0;text-align:center">
    <div class="k">131 hyperlinked pages</div>
    <h2 style="margin-top:18px">What&rsquo;s <em>Inside</em></h2>
  </div>
  <div class="grid">
    <figure><img src="{p('profile')}"><figcaption>Player Profile</figcaption></figure>
    <figure><img src="{p('season')}"><figcaption>Season Goals</figcaption></figure>
    <figure><img src="{p('m01-pre')}"><figcaption>30 Match Plans</figcaption></figure>
    <figure><img src="{p('m01-post')}"><figcaption>30 Match Reviews</figcaption></figure>
    <figure><img src="{p('scout-01')}"><figcaption>20 Scouting Reports</figcaption></figure>
    <figure><img src="{p('results')}"><figcaption>Results Log</figcaption></figure>
    <figure><img src="{p('train-1')}"><figcaption>Training Log</figcaption></figure>
    <figure><img src="{p('drills-1')}"><figcaption>20 Drill Cards</figcaption></figure>
    <figure><img src="{p('body-1')}"><figcaption>Body &amp; Recovery</figcaption></figure>
    <figure><img src="{p('gear')}"><figcaption>String Log</figcaption></figure>
    <figure><img src="{p('coach-1')}"><figcaption>Coach Notes</figcaption></figure>
    <figure><img src="{p('note-5')}"><figcaption>Court Diagrams</figcaption></figure>
  </div>
</section>

<section class="slide dark" id="s3">
  <div style="position:absolute;left:0;right:0;top:80px;text-align:center">
    <div class="k">Before &middot; After</div>
    <h2 class="ttl" style="margin-top:18px">Plan it. <em>Play it.</em> Learn from it.</h2>
  </div>
  <div class="dev" style="width:560px;left:190px;top:280px;transform:rotate(-2deg)"><img src="{p('m01-pre')}"></div>
  <div class="dev" style="width:560px;left:850px;top:280px;transform:rotate(2deg)"><img src="{p('m01-post')}"></div>
</section>

<section class="slide light" id="s4">
  <div style="position:absolute;left:100px;top:170px;width:480px">
    <div class="k">Bonus spreadsheet</div>
    <h2 style="margin-top:18px">Know your <em>numbers</em></h2>
    <div class="rule"></div>
    <div class="list">
      <div><small>Automatic dashboard</small>Win rate, serve %, break points</div>
      <div><small>Surface &amp; month</small>See where you win and why</div>
      <div><small>Head to head</small>Your record against every rival</div>
      <div><small>Works everywhere</small>Google Sheets, Excel &amp; Numbers</div>
    </div>
  </div>
  <div class="screen" style="width:900px;left:640px;top:260px"><img src="{p('dashboard')}"></div>
  <div class="base" style="width:1000px;left:590px;top:907px"></div>
</section>

<section class="slide dark" id="s5">
  <div style="position:absolute;left:110px;top:130px;width:640px">
    <div class="k">Tap &middot; jump &middot; done</div>
    <h2 class="ttl" style="margin-top:20px">Fully <em>hyperlinked</em></h2>
    <div class="rule"></div>
  </div>
  <div class="call" style="left:110px;top:470px"><b>1</b><div>Side tabs on every page<small>Jump to any section in one tap</small></div></div>
  <div class="call" style="left:110px;top:610px"><b>2</b><div>Before &amp; After buttons<small>Each match plan links to its review</small></div></div>
  <div class="call" style="left:110px;top:750px"><b>3</b><div>Clickable index<small>Thirty matches, twenty opponents</small></div></div>
  <div class="call" style="left:110px;top:890px"><b>4</b><div>Home button<small>Back to the index from anywhere</small></div></div>
  <div class="dev" style="width:640px;left:850px;top:110px"><img src="{p('matches')}"></div>
</section>

<section class="slide light" id="s6">
  <div style="position:absolute;left:110px;top:210px;width:600px">
    <div class="k">Gift ready</div>
    <h2 style="margin-top:20px">Made for <em>competitors</em></h2>
    <div class="rule"></div>
    <div class="list">
      <div><small>Junior players</small>&amp; the tennis parents behind them</div>
      <div><small>League &amp; club players</small>chasing the next rating</div>
      <div><small>College hopefuls</small>building a season record</div>
      <div><small>Coaches</small>who want players to reflect</div>
    </div>
  </div>
  <div class="dev" style="width:480px;left:1040px;top:170px;transform:rotate(4deg)"><img src="{p('drills-1')}"></div>
  <div class="dev" style="width:500px;left:780px;top:260px;transform:rotate(-4deg)"><img src="{p('scout-01')}"></div>
</section>

<section class="slide light" id="s7">
  <div style="position:absolute;top:120px;left:0;right:0;text-align:center">
    <div class="k">Instant download</div>
    <h2 style="margin-top:18px">What you <em>receive</em></h2>
  </div>
  <div class="files">
    <div><div class="ic">PDF</div><b>The Match Book</b><span>131-page hyperlinked journal<br>for tablets or printing</span></div>
    <div><div class="ic">XLSX</div><b>Stats Tracker</b><span>Automatic dashboard for<br>Google Sheets, Excel &amp; Numbers</span></div>
    <div><div class="ic">PDF</div><b>Read Me First</b><span>Simple setup steps<br>for every app</span></div>
  </div>
  <div class="steps3"><span><b>01</b>Purchase</span><span><b>02</b>Download from Etsy</span><span><b>03</b>Import &amp; start playing</span></div>
</section>
"""


html = (f'<!doctype html><html><head><meta charset="utf-8">'
        f'<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{FONTS[THEME]}&display=swap">'
        f'<style>{CSS.replace("%TOKENS%", TOKENS[THEME])}{EXTRA[THEME]}</style></head><body>{slides()}</body></html>')
Path(__file__).with_name(f"listing-{THEME}.html").write_text(html)
print(f"listing-{THEME}.html")
