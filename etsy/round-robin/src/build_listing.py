"""Builds the Etsy listing-image slides for the organizer. Run: python3 build_listing.py"""
from pathlib import Path

FONTS = ("https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,400;0,9..144,800;1,9..144,400"
         "&family=Barlow+Semi+Condensed:wght@500;600;700&display=swap")

CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }
:root { --paper: #F6EDD9; --green: #1F6B3B; --navy: #1B2B4B; --red: #C2412D; --coral: #E2614B; }
.slide { width: 1600px; height: 1200px; position: relative; overflow: hidden; font-family: 'Barlow Semi Condensed', sans-serif; }
.light { background: var(--paper); color: var(--navy); }
.dark { background: var(--navy); color: var(--paper); }
.awning::before { content: ""; position: absolute; top: 0; left: 0; right: 0; height: 110px;
  background: repeating-linear-gradient(90deg, var(--green) 0 60px, var(--paper) 60px 120px); }
.awning::after { content: ""; position: absolute; top: 110px; left: 0; right: 0; height: 30px;
  background: radial-gradient(circle at 30px 0, var(--green) 29px, transparent 30px) 0 0 / 120px 30px repeat-x; }
.k { font-size: 17px; letter-spacing: 7px; text-transform: uppercase; font-weight: 700; color: var(--red); }
.dark .k { color: var(--coral); }
h1, h2 { font-family: 'Fraunces', serif; font-weight: 800; letter-spacing: -2px; line-height: 1.02; }
h1 { font-size: 104px; } h2 { font-size: 76px; }
h1 em, h2 em { font-weight: 400; font-style: italic; color: var(--red); letter-spacing: -1px; }
.dark h2 em { color: var(--coral); }
.rule { height: 9px; width: 140px; margin: 30px 0; background: linear-gradient(to bottom, var(--green) 0 3px, transparent 3px 6px, var(--red) 6px 9px); }
.dark .rule { background: linear-gradient(to bottom, var(--paper) 0 3px, transparent 3px 6px, var(--coral) 6px 9px); }
.badges { display: flex; gap: 14px; flex-wrap: wrap; }
.badges span { border: 2px solid var(--navy); padding: 14px 22px; font-size: 17px; letter-spacing: 3px; text-transform: uppercase; font-weight: 700; }
.list div { font-family: 'Fraunces', serif; font-size: 30px; border-top: 1px solid rgba(127,127,127,.4); padding: 13px 0; }
.list div small { display: block; font-family: 'Barlow Semi Condensed', sans-serif; font-size: 14px; letter-spacing: 3px;
  text-transform: uppercase; font-weight: 700; color: var(--red); margin-bottom: 3px; }
.dark .list div small { color: var(--coral); }
.screen { position: absolute; background: #121212; border-radius: 20px 20px 0 0; padding: 18px 18px 24px; box-shadow: 0 40px 80px rgba(0,0,0,.35); }
.screen .inner { background: #fff; overflow: hidden; }
.screen img { display: block; width: 100%; }
.base { position: absolute; height: 24px; background: linear-gradient(#C9CCC6, #8E928B); border-radius: 0 0 20px 20px; }
.paper { position: absolute; box-shadow: 0 26px 50px rgba(27,43,75,.28); }
.paper img { display: block; width: 100%; }
.card { position: absolute; background: #fff; box-shadow: 0 24px 48px rgba(27,43,75,.22); padding: 14px; }
.card img { display: block; width: 100%; }
.step { position: absolute; width: 440px; }
.step .n { font-family: 'Fraunces', serif; font-weight: 800; font-size: 64px; color: var(--red); line-height: 1; }
.step b { display: block; font-family: 'Fraunces', serif; font-size: 34px; margin: 8px 0 6px; }
.step span { font-size: 21px; line-height: 1.45; }
.step .img { margin-top: 24px; background: #fff; padding: 12px; box-shadow: 0 20px 40px rgba(27,43,75,.18); height: 330px; overflow: hidden; }
.step .img img { width: 165%; display: block; }
.files { display: grid; grid-template-columns: repeat(3, 1fr); gap: 34px; position: absolute; left: 110px; right: 110px; top: 380px; }
.files div { border: 2px solid var(--navy); padding: 56px 34px; text-align: center; background: #FBF6EA; }
.files .ic { width: 96px; height: 96px; margin: 0 auto 24px; border: 3px solid var(--red); border-radius: 50%; display: flex; align-items: center;
  justify-content: center; font-weight: 700; font-size: 21px; letter-spacing: 2px; color: var(--red); }
.files b { display: block; font-family: 'Fraunces', serif; font-size: 34px; margin-bottom: 10px; }
.files span { font-size: 20px; line-height: 1.5; }
.who { position: absolute; left: 110px; right: 110px; bottom: 120px; text-align: center; font-size: 20px; letter-spacing: 3px; text-transform: uppercase; font-weight: 700; color: var(--green); }
"""

P = "previews/"
SLIDES = f"""
<section class="slide light awning" id="s1">
  <div style="position:absolute;left:100px;top:230px;width:620px">
    <div class="k">Tennis · spreadsheet + printables</div>
    <h1 style="margin-top:24px;font-size:92px">Round Robin <em>&amp;&nbsp;Ladder</em> Organizer</h1>
    <div class="rule"></div>
    <div class="badges"><span>Auto schedule</span><span>Live standings</span><span>Ladder</span></div>
    <div style="margin-top:36px;font-size:19px;letter-spacing:3px;text-transform:uppercase;font-weight:600">Google Sheets · Excel · Numbers · Print</div>
  </div>
  <div class="screen" style="width:760px;left:800px;top:250px"><div class="inner" style="height:520px"><img src="{P}schedule.png"></div></div>
  <div class="base" style="width:850px;left:755px;top:812px"></div>
  <div class="paper" style="width:330px;left:1210px;top:610px;transform:rotate(5deg)"><img src="{P}draw-sheets-1.png"></div>
</section>

<section class="slide light" id="s2">
  <div style="position:absolute;top:90px;left:0;right:0;text-align:center">
    <div class="k">Three steps · no formulas to learn</div>
    <h2 style="margin-top:16px">How it <em>works</em></h2>
  </div>
  <div class="step" style="left:90px;top:330px"><div class="n">1</div><b>Add your players</b><span>Up to 16 players or doubles teams, plus courts and points.</span>
    <div class="img"><img src="{P}setup.png"></div></div>
  <div class="step" style="left:580px;top:330px"><div class="n">2</div><b>Get the schedule</b><span>Every round and court appears instantly. Byes handled.</span>
    <div class="img"><img src="{P}schedule.png"></div></div>
  <div class="step" style="left:1070px;top:330px"><div class="n">3</div><b>Enter scores</b><span>Winners, standings and the results grid update themselves.</span>
    <div class="img"><img src="{P}standings.png"></div></div>
</section>

<section class="slide dark" id="s3">
  <div style="position:absolute;left:100px;top:170px;width:520px">
    <div class="k">Fair &amp; instant</div>
    <h2 style="margin-top:18px">The schedule <em>builds itself</em></h2>
    <div class="rule"></div>
    <div class="list">
      <div><small>Everyone plays everyone</small>Each pair meets exactly once</div>
      <div><small>Courts &amp; byes</small>Court numbers and rest rounds included</div>
      <div><small>Singles or doubles</small>Up to 16 players or teams</div>
      <div><small>Print it</small>Ready for the clubhouse noticeboard</div>
    </div>
  </div>
  <div class="screen" style="width:860px;left:680px;top:200px"><div class="inner" style="height:640px"><img src="{P}schedule.png"></div></div>
  <div class="base" style="width:950px;left:635px;top:882px"></div>
</section>

<section class="slide light" id="s4">
  <div style="position:absolute;left:100px;top:150px;width:470px">
    <div class="k">Updates as you play</div>
    <h2 style="margin-top:18px">Live <em>standings</em></h2>
    <div class="rule"></div>
    <div class="list">
      <div><small>Ranked automatically</small>Points, game difference, games won</div>
      <div><small>Results grid</small>Every score at a glance</div>
      <div><small>Your rules</small>Set points for a win or a tie</div>
    </div>
  </div>
  <div class="card" style="width:900px;left:620px;top:140px"><img src="{P}standings.png"></div>
  <div class="card" style="width:760px;left:700px;top:560px;transform:rotate(-1.5deg)"><img src="{P}results-grid.png"></div>
</section>

<section class="slide dark" id="s5">
  <div style="position:absolute;left:100px;top:170px;width:500px">
    <div class="k">Season-long play</div>
    <h2 style="margin-top:18px">Challenge <em>ladder</em></h2>
    <div class="rule"></div>
    <div class="list">
      <div><small>Up to 20 players</small>Start in any order you like</div>
      <div><small>Log a challenge</small>Pick challenger, defender, winner</div>
      <div><small>Moves by itself</small>Winners climb, arrows show who moved</div>
    </div>
  </div>
  <div class="card" style="width:880px;left:640px;top:150px"><img src="{P}ladder.png"></div>
  <div class="card" style="width:820px;left:690px;top:640px;transform:rotate(1.5deg)"><img src="{P}challenges.png"></div>
</section>

<section class="slide light awning" id="s6">
  <div style="position:absolute;top:190px;left:0;right:0;text-align:center">
    <div class="k">Bonus PDF · 5 pages</div>
    <h2 style="margin-top:16px">Printable <em>draw sheets</em></h2>
  </div>
  <div class="paper" style="width:330px;left:110px;top:430px;transform:rotate(-5deg)"><img src="{P}draw-sheets-1.png"></div>
  <div class="paper" style="width:330px;left:430px;top:400px;transform:rotate(-1.5deg)"><img src="{P}draw-sheets-3.png"></div>
  <div class="paper" style="width:330px;left:750px;top:400px;transform:rotate(1.5deg)"><img src="{P}draw-sheets-4.png"></div>
  <div class="paper" style="width:330px;left:1070px;top:430px;transform:rotate(5deg)"><img src="{P}draw-sheets-5.png"></div>
  <div style="position:absolute;left:0;right:0;bottom:70px;text-align:center;font-size:20px;letter-spacing:3px;text-transform:uppercase;font-weight:700">
    Score grids · Match schedule · Pairing charts · Ladder board</div>
</section>

<section class="slide light" id="s7">
  <div style="position:absolute;top:120px;left:0;right:0;text-align:center">
    <div class="k">Instant download</div>
    <h2 style="margin-top:16px">What you <em>receive</em></h2>
  </div>
  <div class="files">
    <div><div class="ic">XLSX</div><b>The Organizer</b><span>Round robin, standings,<br>results grid &amp; ladder</span></div>
    <div><div class="ic">PDF</div><b>Draw Sheets</b><span>Printable grids, schedule,<br>pairing charts &amp; ladder</span></div>
    <div><div class="ic">PDF</div><b>Read Me First</b><span>Setup steps<br>&amp; tips</span></div>
  </div>
  <div class="who">Perfect for club organizers · league captains · coaches · social tennis hosts</div>
</section>
"""

html = (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}">'
        f'<style>{CSS}</style></head><body>{SLIDES}</body></html>')
Path(__file__).with_name("listing.html").write_text(html)
print("listing.html")
