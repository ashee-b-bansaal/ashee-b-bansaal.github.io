"""Builds the site (index.html, style.css, app.js in the repo root) from the files in src/.

    python3 src/build.py           build once
    python3 src/build.py --watch   rebuild every time you save something in src/
    python3 src/editor.py          edit the site in your browser instead (see README)
"""
import os
import re
import subprocess
import sys
import time
sys.dont_write_bytecode = True  # content.py changes often; never run a stale cached copy of it
from content import *

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)  # the site is written to the repo root

for _p in PROJECTS:
    _p.setdefault("id", re.sub(r"[^a-z0-9]+", "-", _p["name"].lower()).strip("-"))


def bust(html):
    # add ?v=<content hash> to local files so browsers never show a stale copy after an update
    import hashlib
    def stamp(m):
        f = os.path.join(ROOT, m.group(2))
        if not os.path.isfile(f):
            return m.group(0)
        v = hashlib.md5(open(f, "rb").read()).hexdigest()[:8]
        return f'{m.group(1)}="{m.group(2)}?v={v}"'
    return re.sub(r'(src|href)="((?:photos|logos)/[^"?]+|style\.css|app\.js|favicon\.svg|favicon\.png|apple-touch-icon\.png|resume\.pdf)"', stamp, html)


def save(path, html):
    # lets content.py use a bare "&" (e.g. "R&D") without breaking the HTML
    html = re.sub(r"&(?![a-zA-Z]+;|#\d+;|#x[0-9a-fA-F]+;)", "&amp;", html)
    html = bust(html)
    open(path, "w").write(html)

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
  <link rel="icon" href="favicon.svg" type="image/svg+xml">
  <link rel="icon" href="favicon.png" sizes="32x32" type="image/png">
  <link rel="apple-touch-icon" href="apple-touch-icon.png">
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


def section_head(num, title, epi_key, cls="", title_key=None):
    epi = EPIGRAPHS.get(epi_key)
    epi_html = f'\n        <p class="epigraph">“<span data-edit="EPIGRAPHS.{epi_key}">{epi}</span>”</p>' if epi else ""
    tk = f' data-edit="TITLES.{title_key}"' if title_key else ""
    return f'''<header class="sec-head {cls}">
        <p class="eyebrow">{num}</p>
        <h2{tk}>{title}</h2>{epi_html}
      </header>'''


def about(num, portrait_extra=""):
    paras = "\n".join(f'          <p data-edit="ABOUT.{i}">{p}</p>' for i, p in enumerate(ABOUT))
    return f'''
    <section id="about" class="sec about-sec">
      <div class="wrap about">
        <figure class="portrait">
          <span class="mono" aria-hidden="true">AB</span>
          <img src="photos/me.jpg" alt="{NAME}" width="400" height="500" loading="lazy" onerror="this.remove()">{portrait_extra}
        </figure>
        <div class="about-text">
          <p class="eyebrow">{num}</p>
          <h2 data-edit="ABOUT_HEAD">{ABOUT_HEAD}</h2>
{paras}
          <p class="seeking" data-edit="SEEKING">{SEEKING}</p>
          <p class="cta-row"><a class="btn btn-primary" href="resume.pdf" target="_blank" rel="noopener">Résumé</a><a class="btn btn-outline" href="mailto:{EMAIL}">Email Me</a></p>
        </div>
      </div>
    </section>
'''


def logo(e, k):
    if e.get("logo_img"):
        return f'<span class="logo has-img{" tile" if e.get("logo_tile") else ""}" aria-hidden="true"><img src="{e["logo_img"]}" alt=""></span>'
    return f'<span class="logo" aria-hidden="true" data-edit="{k}.logo">{e["logo"]}</span>'


def experience(num, title, extra_inside_timeline="", title_key=None):
    items = []
    for i, e in enumerate(EXPERIENCE):
        k = f"EXPERIENCE.{i}"
        tags = "".join(f'<li data-edit="{k}.tags.{j}">{t}</li>' for j, t in enumerate(e["tags"]))
        venue = f'<p class="venue" data-edit="{k}.venue">{e["venue"]}</p>' if e.get("venue") else ""
        items.append(f'''          <li class="t-item{' is-now' if e['now'] else ''}">
            <article class="card exp-card">
              <header class="card-head">
                {logo(e, k)}
                <div><h3 data-edit="{k}.role">{e['role']}</h3><p class="org" data-edit="{k}.org">{e['org']}</p>{venue}</div>
              </header>
              <p class="when"><span data-edit="{k}.when">{e['when']}</span> <span data-edit="{k}.where">{e['where']}</span></p>
              <p data-edit="{k}.text">{e['text']}</p>
              <ul class="tags">{tags}</ul>
            </article>
          </li>''')
    return f'''
    <section id="experience" class="sec exp-sec">
      <div class="wrap">
        {section_head(num, title, "experience", title_key=title_key)}
        <div class="tl-wrap">{extra_inside_timeline}
        <ol class="timeline">
{chr(10).join(items)}
        </ol>
        </div>
      </div>
    </section>
'''


def hobbies(num, title, render, title_key=None):
    cards = "\n".join(render(h) for h in HOBBIES)
    return f'''
    <section id="hobbies" class="sec hob-sec">
      <div class="wrap">
        {section_head(num, title, "hobbies", title_key=title_key)}
        <div class="hob-grid">
{cards}
        </div>
      </div>
    </section>
'''


def skills(num):
    tints = ["lilac", "mint", "coral", "lime"]
    chips = lambda i, items: "".join(f'<li data-edit="SKILLS.{i}.1.{j}">{t}</li>' for j, t in enumerate(items))
    cols = "".join(
        f'<div class="skill-card tint-{tints[i % len(tints)]}"><h3 data-edit="SKILLS.{i}.0">{name}</h3><ul class="tags">{chips(i, items)}</ul></div>'
        for i, (name, items) in enumerate(SKILLS))
    return f'''
    <section id="skills" class="sec skills-sec">
      <div class="wrap">
        {section_head(num, TITLES["skills"], None, title_key="skills")}
        <div class="skills">{cols}</div>
        <p class="edu" data-edit="EDU">{EDU}</p>
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


# ── hero photos ───────────────────────────────────────────────────────────────
POLAROIDS = [  # (photo file, caption, x%, y%, rotation, tint, focal point); phones show the first four
    ("photos/ithaca-summer.jpg", "ithaca, summer", 6, 16, -8, "lime", "50% 50%"),
    ("photos/arte-museum.jpg", "arte museum", 76, 10, 6, "lilac", "50% 45%"),
    ("photos/nyc-night.jpg", "nyc, after dark", 3, 58, 5, "coral", "50% 55%"),
    ("photos/pittsburgh.jpg", "pittsburgh, summer", 80, 56, -6, "mint", "50% 70%"),
    ("photos/dessert.jpg", "dessert first", 22, 74, -3, "pink", "50% 55%"),
    ("photos/magnolia.jpg", "magnolia season", 62, 76, 8, "cream", "50% 72%"),
]


def polaroid(src, cap, tint, cls="", style="", pos="50% 50%"):
    return f'''<figure class="polaroid {cls}" style="{style}">
        <span class="tape" aria-hidden="true"></span>
        <div class="photo tint-{tint}"><img src="{src}" alt="{cap}" width="400" height="400" style="object-position:{pos}" {"" if "drop" in cls else 'loading="lazy" '}onerror="this.remove()"><span class="ph" aria-hidden="true">your photo</span></div>
        <figcaption>{cap}</figcaption>
      </figure>'''


def build_page():
    pol = "\n      ".join(
        polaroid(s, c, t, "drop", f"--x:{x}%;--y:{y}%;--r:{r}deg;--d:{i*0.12+0.2:.2f}s", pos)
        for i, (s, c, x, y, r, t, pos) in enumerate(POLAROIDS))
    tints = ["lilac", "mint", "coral", "lime", "pink", "cream"]
    empty = lambda v: "" if (v or "").strip() else " is-empty"  # hidden on the site, shown in edit mode

    def card(i, p):
        k = f"PROJECTS.{i}"
        link = p.get("link", "")
        img, name = p.get("image", ""), p["name"]
        fit, focus = p.get("fit", "contain"), p.get("focus", "50% 50%")
        art = (f'<img src="{img}" alt="{name}" loading="lazy" style="object-fit:{fit};object-position:{focus}">' if img
               else f'<span class="hand">{name.lower()}</span>')
        art = f'<div class="card-art tint-{tints[i % len(tints)]}{" is-cover" if img and fit == "cover" else ""}">{art}</div>'
        title = f'<span data-edit="{k}.name">{p["name"]}</span>'
        if link and link != "#":  # "#" = placeholder, not clickable yet
            title = f'<a href="{link}" target="_blank" rel="noopener" data-edit-href="{k}.link">{title}<span class="go" aria-hidden="true">↗</span></a>'
            art = f'<a class="art-link" href="{link}" target="_blank" rel="noopener" tabindex="-1" aria-hidden="true">{art}</a>'
        tags = "".join(f'<li data-edit="{k}.tags.{j}">{t}</li>' for j, t in enumerate(p.get("tags", [])))
        newtab = lambda u: "" if u == "#" else ' target="_blank" rel="noopener"'
        details = "".join(f'<p class="detail"><span data-edit="{k}.details.{j}.0">{a}</span>: <b data-edit="{k}.details.{j}.1">{b}</b></p>' for j, (a, b) in enumerate(p.get("details", [])))
        buttons = "".join(f'<a class="link-pill" href="{u}"{newtab(u)} data-edit-href="{k}.buttons.{j}.1"><span data-edit="{k}.buttons.{j}.0">{l}</span> <span aria-hidden="true">↗</span></a>' for j, (l, u) in enumerate(p.get("buttons", [])))
        return f'''          <article class="pcard" id="{p['id']}" data-project="{i}" data-link="{link}" data-fit="{fit}">
            <h3>{title}</h3>
            <p class="sub{empty(p.get('subtitle'))}" data-edit="{k}.subtitle">{p.get('subtitle', '')}</p>
            <p class="venue{empty(p.get('venue'))}" data-edit="{k}.venue">{p.get('venue', '')}</p>
            {art}
            <p class="desc" data-edit="{k}.text">{p['text']}</p>
            <ul class="tags ptags">{tags}</ul>
            <div class="details">{details}</div>
            {f'<div class="proj-links">{buttons}</div>' if buttons else ''}
          </article>'''
    cards = "\n".join(card(i, p) for i, p in enumerate(PROJECTS))

    def hob(h):
        k = f"HOBBIES.{HOBBIES.index(h)}"
        link = f'<a class="link-pill" href="{h["link"][1]}" data-edit-href="{k}.link.1"><span data-edit="{k}.link.0">{h["link"][0]}</span> ↗</a>' if h["link"] else ""
        return f'''          <article class="hob ticket tint-{h['tint']}">
            <span class="hob-icon" aria-hidden="true">{ICONS[h['icon']]}</span>
            <h3 data-edit="{k}.title">{h['title']}</h3>
            <p data-edit="{k}.text">{h['text']}</p>{link}
          </article>'''

    marquee_items = ["SWE", "ML", "Cornell ’28", "poet", "flautist", "keys", "always carrying a camera", "Ithaca, NY", "open to Summer 2027"]
    mq = "".join(f"<span>{m}</span><i>✶</i>" for m in marquee_items)
    html = head("scrapbook", "family=Inter+Tight:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Gochi+Hand", "Portfolio.")
    html += f'''
  <header class="hero" id="hero">
    <canvas id="julia" aria-hidden="true"></canvas>
    <div class="hero-veil" aria-hidden="true"></div>
    <div class="table" id="table">
      {pol}
    </div>
    <div class="hero-inner">
      <h1 class="reveal"><span class="hero-name"><span data-edit="NAME">{NAME}</span>{penguin_svg("name-penguin")}</span></h1>
      <p class="hero-sub reveal" data-edit="TAGLINE">{TAGLINE}</p>
      <p class="cta-row reveal"><a class="btn btn-primary" href="resume.pdf" target="_blank" rel="noopener">Résumé</a><a class="btn btn-outline" href="#projects">See Projects</a></p>
      <p class="hand hint reveal">psst, you can move the photos around</p>
    </div>
    <a class="scroll-cue" href="#about" aria-label="Scroll to content"><svg viewBox="0 0 24 24"><path d="M5 9l7 7 7-7"/></svg></a>
  </header>
  <div class="marquee" aria-hidden="true"><div class="marquee-track">{mq}{mq}</div></div>
'''
    html += nav(NAME)
    html += "  <main>"
    html += about("About", '\n          <span class="tape" aria-hidden="true"></span><figcaption class="hand">hi, it’s me</figcaption>')
    slider = f'\n          <div class="slider" aria-hidden="true">{penguin_svg("slide-penguin")}</div>'
    html += experience("01 — Experience", TITLES["experience"], slider, title_key="experience")
    html += f'''
    <section id="projects" class="sec proj-sec">
      <div class="wrap">
        {section_head("02 — Projects", TITLES["projects"], "projects", title_key="projects")}
        <div class="pgrid">
{cards}
        </div>
        <p class="more">More on <a href="{GITHUB}">GitHub</a>.</p>
      </div>
    </section>
'''
    html += hobbies("03 — Off the clock", TITLES["hobbies"], hob, title_key="hobbies")
    html += skills("04 — Toolbox")
    html += "  </main>"
    html += foot(extra_top='\n      <p class="hand sign">— ashee</p>')
    save(os.path.join(ROOT, "index.html"), html)


# ── the penguin (beside the name, and sliding down the timeline) ─────────────
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


def build_assets():
    read = lambda f: open(os.path.join(HERE, f), encoding="utf-8").read()
    open(os.path.join(ROOT, "style.css"), "w").write(read("base.css") + "\n" + read("theme.css"))
    open(os.path.join(ROOT, "app.js"), "w").write("\n".join(read(f) for f in ("base.js", "photos.js", "julia.js", "penguin.js")))


if "--watch" in sys.argv:
    # rebuild in a fresh process whenever anything in src/ changes
    stamp = lambda: {f: os.path.getmtime(os.path.join(HERE, f)) for f in os.listdir(HERE) if f.endswith((".py", ".css", ".js"))}
    last = None
    print("watching src/ for changes (Ctrl+C to stop)", flush=True)
    while True:
        now = stamp()
        if now != last:
            r = subprocess.run([sys.executable, os.path.abspath(__file__)], capture_output=True, text=True)
            print(time.strftime("%H:%M:%S"), "rebuilt" if r.returncode == 0 else "ERROR:\n" + r.stderr.strip().splitlines()[-1], flush=True)
            last = now
        time.sleep(0.7)

build_assets()  # first, so the page can stamp style.css / app.js with their new hashes
build_page()
print("built")
