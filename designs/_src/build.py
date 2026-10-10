import os
from content import *

OUT = "/Users/asheebbansaal/Documents/portfolio/designs"

SOCIAL = f'''<ul class="nav-icons">
      <li><a href="mailto:{EMAIL}" aria-label="Email"><svg viewBox="0 0 24 24"><rect x="3" y="5.5" width="18" height="13" rx="1.5"/><path d="M3.5 6.5l8.5 6.5 8.5-6.5"/></svg></a></li>
      <li><a href="{GITHUB}" aria-label="GitHub"><svg viewBox="0 0 24 24" class="fill"><path d="M12 2.5a9.5 9.5 0 0 0-3 18.5c.5.1.7-.2.7-.5v-1.7c-2.6.6-3.2-1.2-3.2-1.2-.4-1.1-1-1.4-1-1.4-.9-.6 0-.6 0-.6 1 .1 1.5 1 1.5 1 .8 1.5 2.3 1 2.8.8.1-.6.3-1 .6-1.2-2.1-.2-4.3-1-4.3-4.7 0-1 .4-1.9 1-2.6-.1-.3-.4-1.2.1-2.5 0 0 .8-.3 2.6 1a9 9 0 0 1 4.8 0c1.8-1.3 2.6-1 2.6-1 .5 1.3.2 2.2.1 2.5.6.7 1 1.6 1 2.6 0 3.7-2.2 4.5-4.3 4.7.3.3.6.9.6 1.8v2.6c0 .3.2.6.7.5A9.5 9.5 0 0 0 12 2.5z"/></svg></a></li>
      <li><a href="{LINKEDIN}" aria-label="LinkedIn"><svg viewBox="0 0 24 24" class="fill"><path d="M4.5 3.5a2 2 0 1 1 0 4 2 2 0 0 1 0-4zM3 9h3v11.5H3zM9 9h2.9v1.6c.4-.8 1.4-1.8 3.2-1.8 3.2 0 3.9 2.1 3.9 4.9v6.6h-3v-5.8c0-1.4 0-3.1-1.9-3.1s-2.2 1.5-2.2 3v5.9H9z"/></svg></a></li>
    </ul>'''


def head(title_suffix, fonts, desc, theme="#ffffff"):
    return f'''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{NAME}</title>
  <meta name="description" content="{NAME}: software and machine learning engineering, CS at Cornell. {desc}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?{fonts}&display=swap" rel="stylesheet">
  <meta name="theme-color" content="{theme}">
  <link rel="stylesheet" href="style.css">
</head>
<body class="{title_suffix}">
  <a class="skip" href="#about">Skip to content</a>
'''


def nav(name_html):
    return f'''
  <nav class="nav" aria-label="Primary">
    {SOCIAL}
    <a class="nav-name" href="#">{name_html}</a>
    <ul class="nav-links">
      <li><a href="#about">About</a></li>
      <li><a href="#experience">Experience</a></li>
      <li><a href="#projects">Projects</a></li>
      <li><a href="#hobbies">Hobbies</a></li>
    </ul>
  </nav>
'''


def section_head(num, title, epi_key, cls=""):
    epi = EPIGRAPHS.get(epi_key)
    epi_html = f'\n        <p class="epigraph">“{epi}”</p>' if epi else ""
    return f'''<header class="sec-head {cls}">
        <p class="eyebrow">{num}</p>
        <h2>{title}</h2>{epi_html}
      </header>'''


def about(num, portrait_extra=""):
    paras = "\n".join(f"          <p>{p}</p>" for p in ABOUT)
    return f'''
    <section id="about" class="sec about-sec">
      <div class="wrap about">
        <figure class="portrait">
          <span class="mono" aria-hidden="true">AB</span>
          <img src="photos/me.jpg" alt="{NAME}" width="400" height="500" loading="lazy" onerror="this.remove()">{portrait_extra}
        </figure>
        <div class="about-text">
          <p class="eyebrow">{num}</p>
          <h2>{ABOUT_HEAD}</h2>
{paras}
          <p class="seeking">{SEEKING}</p>
          <p class="cta-row"><a class="btn btn-primary" href="resume.pdf" target="_blank" rel="noopener">Résumé</a><a class="btn btn-outline" href="mailto:{EMAIL}">Email Me</a></p>
        </div>
      </div>
    </section>
'''


def experience(num, title, extra_inside_timeline=""):
    items = []
    for e in EXPERIENCE:
        tags = "".join(f"<li>{t}</li>" for t in e["tags"])
        items.append(f'''          <li class="t-item{' is-now' if e['now'] else ''}">
            <article class="card exp-card">
              <header class="card-head">
                <span class="logo" aria-hidden="true">{e['logo']}</span>
                <div><h3>{e['role']}</h3><p class="org">{e['org']}</p></div>
              </header>
              <p class="when">{e['when']} <span>{e['where']}</span></p>
              <p>{e['text']}</p>
              <ul class="tags">{tags}</ul>
            </article>
          </li>''')
    return f'''
    <section id="experience" class="sec exp-sec">
      <div class="wrap">
        {section_head(num, title, "experience")}
        <div class="tl-wrap">{extra_inside_timeline}
        <ol class="timeline">
{chr(10).join(items)}
        </ol>
        </div>
      </div>
    </section>
'''


def chips(p):
    return "".join(f"<li>{c}</li>" for c in p["chips"])


def stats(p):
    return "".join(f'<div class="stat"><b>{n}</b><span>{l}</span></div>' for n, l in p["stats"])


def links(p):
    return "".join(f'<a class="link-pill" href="{h}">{l} <span aria-hidden="true">↗</span></a>' for l, h in p["links"])


def hobbies(num, title, render):
    cards = "\n".join(render(h) for h in HOBBIES)
    return f'''
    <section id="hobbies" class="sec hob-sec">
      <div class="wrap">
        {section_head(num, title, "hobbies")}
        <div class="hob-grid">
{cards}
        </div>
      </div>
    </section>
'''


def skills(num):
    cols = "".join(f"<div><h3>{a}</h3><p>{b}</p></div>" for a, b in SKILLS)
    return f'''
    <section id="skills" class="sec skills-sec">
      <div class="wrap">
        {section_head(num, "Toolbox", None)}
        <div class="skills">{cols}</div>
        <p class="edu">{EDU}</p>
      </div>
    </section>
'''


def foot(extra_top="", extra_bottom=""):
    return f'''
  <footer class="foot">
    <div class="wrap">{extra_top}
      <p class="cta"><em>Say hello</em>: <a href="mailto:{EMAIL}">{EMAIL}</a></p>
      <p class="small"><span>Hand-written HTML, CSS &amp; JS · Last updated October 2026</span><span>It’s <span class="clock">--:--</span> in Ithaca</span></p>
    </div>{extra_bottom}
  </footer>
  <script src="app.js" defer></script>
</body>
</html>
'''


def hobby_basic(h):
    link = f'<a class="link-pill" href="{h["link"][1]}">{h["link"][0]} <span aria-hidden="true">↗</span></a>' if h["link"] else ""
    return f'''          <article class="hob tint-{h['tint']}">
            <span class="hob-icon" aria-hidden="true">{ICONS[h['icon']]}</span>
            <h3>{h['title']}</h3>
            <p>{h['text']}</p>{link}
          </article>'''


# ───────────────────────── FRACTAL ─────────────────────────
def build_fractal():
    def card(i, p):
        flip = " flip" if i % 2 else ""
        return f'''        <article class="proj{flip}" id="{p['id']}">
          <div class="proj-art tint-{p['tint']}"><canvas class="fractal" data-kind="{p['kind']}" aria-hidden="true"></canvas><span class="art-label">{p['kind'].replace('sierpinski','sierpiński')}</span></div>
          <div class="proj-body">
            <p class="proj-ctx">{p['ctx']}</p>
            <h3>{p['name']}</h3>
            <p class="proj-tag">{p['tagline']}</p>
            <p>{p['text']}</p>
            <div class="stats">{stats(p)}</div>
            <ul class="tags">{chips(p)}</ul>
            <div class="proj-links">{links(p)}</div>
          </div>
        </article>'''
    projects = "\n".join(card(i, p) for i, p in enumerate(PROJECTS))
    html = head("fractal", "family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;1,6..72,300&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400", "Fractal edition.", "#f5f5f5")
    html += f'''
  <header class="hero" id="hero">
    <canvas id="julia" aria-hidden="true"></canvas>
    <div class="hero-veil" aria-hidden="true"></div>
    <div class="hero-inner">
      <p class="eyebrow reveal">Portfolio · Fall 2026</p>
      <h1 class="reveal">{NAME}</h1>
      <p class="hero-sub reveal">{TAGLINE}</p>
      <p class="cta-row reveal"><a class="btn btn-primary" href="resume.pdf" target="_blank" rel="noopener">Résumé</a><a class="btn btn-outline" href="#projects">See Projects</a></p>
    </div>
    <p class="formula" aria-hidden="true"><span>z ↦ z² + c</span><span id="cval">c = 0.000 + 0.000i</span><span class="hint">move your cursor to reshape it</span></p>
    <a class="scroll-cue" href="#about" aria-label="Scroll to content"><svg viewBox="0 0 24 24"><path d="M5 9l7 7 7-7"/></svg></a>
  </header>
'''
    html += nav(f"<em>{NAME}</em>")
    html += "  <main>"
    html += about("I · About")
    html += experience("II · Experience", "Where I’ve worked")
    html += f'''
    <section id="projects" class="sec proj-sec">
      <div class="wrap">
        {section_head("III · Projects", "Things I’ve built", "projects")}
        <div class="proj-list">
{projects}
        </div>
        <p class="more">More on <a href="{GITHUB}">GitHub</a>.</p>
      </div>
    </section>
'''
    html += hobbies("IV · Off the clock", "When I’m not coding", hobby_basic)
    html += skills("V · Toolbox")
    html += "  </main>"
    html += foot(extra_bottom='\n    <canvas id="fern" class="fern" aria-hidden="true"></canvas>')
    open(f"{OUT}/fractal/index.html", "w").write(html)


# ───────────────────────── SCRAPBOOK ─────────────────────────
POLAROIDS = [  # (photo file, caption, x%, y%, rotation, tint)
    ("photos/1.jpg", "ithaca, fall", 6, 16, -8, "lime"),
    ("photos/2.jpg", "the gorges", 76, 10, 6, "lilac"),
    ("photos/3.jpg", "lab, 2am", 3, 58, 5, "coral"),
    ("photos/4.jpg", "pittsburgh, summer", 80, 56, -6, "mint"),
    ("photos/5.jpg", "flute practice", 22, 74, -3, "pink"),
    ("photos/6.jpg", "a good sky", 62, 76, 8, "cream"),
]


def polaroid(src, cap, tint, cls="", style=""):
    return f'''<figure class="polaroid {cls}" style="{style}">
        <span class="tape" aria-hidden="true"></span>
        <div class="photo tint-{tint}"><img src="{src}" alt="" width="400" height="400" {"" if "drop" in cls else 'loading="lazy" '}onerror="this.remove()"><span class="ph" aria-hidden="true">your photo</span></div>
        <figcaption>{cap}</figcaption>
      </figure>'''


def build_scrapbook():
    pol = "\n      ".join(
        polaroid(s, c, t, "drop", f"--x:{x}%;--y:{y}%;--r:{r}deg;--d:{i*0.12+0.2:.2f}s")
        for i, (s, c, x, y, r, t) in enumerate(POLAROIDS))
    blocks = ["lime", "lilac", "mint", "coral", "pink"]

    def page(i, p):
        flip = " flip" if i % 2 else ""
        note_rot = [-3, 2.5, -2, 3, -2.5][i]
        return f'''        <article class="page block-{blocks[i % len(blocks)]}{flip}" id="{p['id']}">
          <div class="page-art">
            {polaroid(p['photo'], p['name'].lower(), 'cream', 'page-pol')}
            <div class="sticky" style="--r:{note_rot}deg">{stats(p)}</div>
          </div>
          <div class="page-body">
            <p class="eyebrow">{p['ctx']}</p>
            <h3>{p['name']}</h3>
            <p class="proj-tag">{p['tagline']}</p>
            <p>{p['text']}</p>
            <ul class="tags">{chips(p)}</ul>
            <div class="proj-links">{links(p)}</div>
          </div>
        </article>'''
    pages = "\n".join(page(i, p) for i, p in enumerate(PROJECTS))

    def hob(h):
        link = f'<a class="link-pill" href="{h["link"][1]}">{h["link"][0]} ↗</a>' if h["link"] else ""
        return f'''          <article class="hob ticket tint-{h['tint']}">
            <span class="hob-icon" aria-hidden="true">{ICONS[h['icon']]}</span>
            <h3>{h['title']}</h3>
            <p>{h['text']}</p>{link}
            <span class="stub" aria-hidden="true">ADMIT ONE · {h['title'].upper()}</span>
          </article>'''

    marquee_items = ["SWE", "ML", "Cornell ’28", "poet", "flautist", "keys", "always carrying a camera", "Ithaca, NY", "open to Summer 2027"]
    mq = "".join(f"<span>{m}</span><i>✶</i>" for m in marquee_items)
    html = head("scrapbook", "family=Inter+Tight:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Gochi+Hand", "Scrapbook edition.")
    html += f'''
  <header class="hero" id="hero">
    <canvas id="julia" aria-hidden="true"></canvas>
    <div class="hero-veil" aria-hidden="true"></div>
    <div class="table" id="table">
      {pol}
    </div>
    <div class="hero-inner">
      <p class="eyebrow reveal">Portfolio · Fall 2026</p>
      <h1 class="reveal"><span class="hero-name">{NAME}{penguin_svg("name-penguin")}</span></h1>
      <p class="hero-sub reveal">{TAGLINE}</p>
      <p class="cta-row reveal"><a class="btn btn-primary" href="resume.pdf" target="_blank" rel="noopener">Résumé</a><a class="btn btn-outline" href="#projects">See Projects</a></p>
      <p class="hand hint reveal">psst, you can move the photos around</p>
    </div>
    <a class="scroll-cue" href="#about" aria-label="Scroll to content"><svg viewBox="0 0 24 24"><path d="M5 9l7 7 7-7"/></svg></a>
  </header>
  <div class="marquee" aria-hidden="true"><div class="marquee-track">{mq}{mq}</div></div>
'''
    html += nav(NAME)
    html += "  <main>"
    html += about("01 — About", '\n          <span class="tape" aria-hidden="true"></span><figcaption class="hand">hi, it’s me</figcaption>')
    slider = f'\n          <div class="slider" aria-hidden="true">{penguin_svg("slide-penguin")}</div>'
    html += experience("02 — Experience", "Where I’ve worked", slider)
    html += f'''
    <section id="projects" class="sec proj-sec">
      <div class="wrap">
        {section_head("03 — Projects", "Pages from the build log", "projects")}
        <div class="pages">
{pages}
        </div>
        <p class="more">More on <a href="{GITHUB}">GitHub</a>.</p>
      </div>
    </section>
'''
    html += hobbies("04 — Off the clock", "When I’m not coding", hob)
    html += skills("05 — Toolbox")
    html += "  </main>"
    html += foot(extra_top='\n      <p class="hand sign">— ashee</p>')
    open(f"{OUT}/scrapbook/index.html", "w").write(html)


# ───────────────────────── PENGUIN ─────────────────────────
_peng_n = 0


def penguin_svg(cls="", ident=""):
    # Chubby penguin with a heart-shaped face, Cornell-red scarf and soft shading.
    # Eye groups keep .white/.pupil/.glint/.lid (penguin.js tracks and blinks them);
    # the viewBox stays 200 wide because penguin.js maps eye coords with width/200.
    global _peng_n
    _peng_n += 1
    u = f"pg{_peng_n}"
    eye = lambda x: f'''<g class="eye" data-eye><circle class="white" cx="{x}" cy="78" r="10" fill="none"/><ellipse class="pupil" cx="{x}" cy="78" rx="7" ry="8" fill="#141826"/><circle class="glint" cx="{x + 2.6}" cy="74.6" r="2.6" fill="#fff"/><ellipse class="lid" cx="{x}" cy="78" rx="9" ry="0" fill="#fff"/></g>'''
    return f'''<svg class="penguin {cls}" {ident} viewBox="0 0 200 240" aria-hidden="true">
        <defs>
          <radialGradient id="{u}b" cx=".34" cy=".26" r=".85"><stop offset="0" stop-color="#3a4363"/><stop offset=".55" stop-color="#1f2539"/><stop offset="1" stop-color="#121625"/></radialGradient>
          <linearGradient id="{u}w" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffffff"/><stop offset="1" stop-color="#e9edf5"/></linearGradient>
          <linearGradient id="{u}o" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ffb347"/><stop offset="1" stop-color="#f08a24"/></linearGradient>
          <linearGradient id="{u}s" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#d42a2a"/><stop offset="1" stop-color="#a51818"/></linearGradient>
        </defs>
        <ellipse class="shadow" cx="100" cy="227" rx="54" ry="7" fill="rgba(20,24,38,.14)"/>
        <g class="feet" fill="url(#{u}o)"><path d="M62 212c-10 3-14 13-3 14h28c6 0 6-12-3-14z"/><path d="M138 212c10 3 14 13 3 14h-28c-6 0-6-12 3-14z"/></g>
        <g class="bodyg">
          <g class="flip-l"><path fill="#1a1f30" d="M42 118c-20 14-30 44-26 60 3 7 12 4 18-4 8-14 14-36 16-50z"/></g>
          <g class="flip-r"><path fill="#1a1f30" d="M158 118c20 14 30 44 26 60-3 7-12 4-18-4-8-14-14-36-16-50z"/></g>
          <path fill="url(#{u}b)" d="M100 16c-46 0-66 44-66 102 0 64 26 102 66 102s66-38 66-102c0-58-20-102-66-102z"/>
          <path fill="url(#{u}w)" d="M100 98c-32 0-46 30-46 62 0 36 18 54 46 54s46-18 46-54c0-32-14-62-46-62z"/>
          <path fill="url(#{u}w)" d="M100 58c-10-18-44-20-46 12-2 28 20 42 46 42s48-14 46-42c-2-32-36-30-46-12z"/>
          <ellipse cx="72" cy="34" rx="16" ry="7" fill="#fff" opacity=".13" transform="rotate(-28 72 34)"/>
          <path d="M98 17c-4-8 1-14 7-15-3 4-2 9 2 13" fill="none" stroke="#1f2539" stroke-width="3" stroke-linecap="round"/>
          {eye(82)}
          {eye(118)}
          <ellipse class="blush" cx="68" cy="95" rx="8" ry="4.5" fill="#ff9fb2" opacity=".6"/><ellipse class="blush" cx="132" cy="95" rx="8" ry="4.5" fill="#ff9fb2" opacity=".6"/>
          <path fill="url(#{u}o)" d="M90 90c5-4 15-4 20 0-2 7-6 11-10 11s-8-4-10-11z"/>
          <path d="M92 93c4 2 12 2 16 0" fill="none" stroke="#c96a12" stroke-width="1.4" stroke-linecap="round" opacity=".7"/>
          <g class="scarf">
            <path fill="url(#{u}s)" d="M46 114c34 16 74 16 108 0l3 13c-36 18-78 18-114 0z"/>
            <path fill="url(#{u}s)" d="M122 128l14 38-15 4-9-38z"/>
            <path d="M58 122c28 10 56 10 84 0M126 144l12-3M129 154l12-3" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" opacity=".85"/>
            <path d="M122 170l-2 6M127 169l-1 6M132 168l0 6" stroke="#a51818" stroke-width="2" stroke-linecap="round"/>
          </g>
        </g>
      </svg>'''


def build_penguin():
    def card(i, p):
        return f'''        <article class="proj tint-{p['tint']}" id="{p['id']}">
          <div class="proj-top">
            <p class="proj-ctx">{p['ctx']}</p>
            <h3>{p['name']}</h3>
            <p class="proj-tag">{p['tagline']}</p>
          </div>
          <p>{p['text']}</p>
          <div class="stats">{stats(p)}</div>
          <ul class="tags">{chips(p)}</ul>
          <div class="proj-links">{links(p)}</div>
        </article>'''
    projects = "\n".join(card(i, p) for i, p in enumerate(PROJECTS))
    flakes = "".join(f'<i style="--x:{(i*37)%100}%;--d:{6+(i*7)%9}s;--delay:-{(i*13)%11}s;--s:{0.5+((i*5)%6)/10}"></i>' for i in range(26))
    html = head("penguin", "family=Inter:wght@400;500;600;700&family=Fraunces:ital,opsz,wght@1,9..144,500", "Penguin edition.", "#eef6fd")
    html += f'''
  <header class="hero" id="hero">
    <div class="snow" aria-hidden="true">{flakes}</div>
    <div class="hero-inner">
      <p class="pill-badge reveal">Open to Summer 2027 internships</p>
      <h1 class="reveal">Hi, I’m Ashee. <span>I build software and ML systems.</span></h1>
      <p class="hero-sub reveal">CS @ Cornell ’28 · backend, real-time ML, GPU &amp; training infra</p>
      <p class="cta-row reveal"><a class="btn btn-primary" href="resume.pdf" target="_blank" rel="noopener">Résumé</a><a class="btn btn-outline" href="#projects">See Projects</a></p>
    </div>
    <div class="floe" aria-hidden="true">
      <div class="speech" id="speech" aria-live="polite">hi! i’m pebble.</div>
      <button class="pebble-btn" id="pebble-btn" type="button" aria-label="Say hi to Pebble the penguin">{penguin_svg("hero-penguin", 'id="pebble"')}</button>
      <svg class="ice" viewBox="0 0 400 60"><path d="M10 20 L60 6 L150 10 L240 2 L330 12 L392 22 L380 44 L260 56 L120 54 L24 44 Z"/><path class="ice-shine" d="M70 16 L140 14 M250 10 L300 14"/></svg>
    </div>
    <a class="scroll-cue" href="#about" aria-label="Scroll to content"><svg viewBox="0 0 24 24"><path d="M5 9l7 7 7-7"/></svg></a>
  </header>
'''
    html += nav(f'{NAME}')
    html += "  <main>"
    html += about("About")
    slider = f'\n          <div class="slider" aria-hidden="true">{penguin_svg("slide-penguin")}</div>'
    html += experience("Experience", "Where I’ve worked", slider)
    html += f'''
    <section id="projects" class="sec proj-sec">
      <div class="wrap">
        {section_head("Projects", "Things I’ve built", "projects")}
        <div class="proj-grid">
{projects}
        </div>
        <p class="more">More on <a href="{GITHUB}">GitHub</a>.</p>
      </div>
    </section>
'''
    html += hobbies("Off the clock", "When I’m not coding", hobby_basic)
    html += skills("Toolbox")
    html += "  </main>"
    html += foot(extra_top=f'\n      <div class="foot-peng">{penguin_svg("foot-penguin")}</div>')
    open(f"{OUT}/penguin/index.html", "w").write(html)


build_fractal()
build_scrapbook()
build_penguin()

HERE = os.path.dirname(os.path.abspath(__file__))
base_css, base_js = open(f"{HERE}/base.css").read(), open(f"{HERE}/base.js").read()
for v in ("fractal", "scrapbook", "penguin"):
    open(f"{OUT}/{v}/style.css", "w").write(base_css + "\n" + open(f"{HERE}/{v}.css").read())
    theme_js = open(f"{HERE}/{v}.js").read()
    if v == "scrapbook":
        theme_js += "\n" + open(f"{HERE}/fractal.js").read()
        theme_js += "\n" + open(f"{HERE}/penguin.js").read()
    open(f"{OUT}/{v}/app.js", "w").write(base_js + "\n" + theme_js)
print("built")
