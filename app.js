// ── shared behaviour: light/dark switch, nav highlight, scroll fade-in, clock ──
const REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;

// Light/dark switch. The head script picks the starting theme (saved choice, else the system's).
(() => {
  const root = document.documentElement, btn = document.querySelector('.theme-toggle');
  const meta = document.querySelector('meta[name="theme-color"]');
  const sync = () => {
    const dark = root.dataset.theme === 'dark';
    btn?.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
    meta?.setAttribute('content', dark ? '#0f0f11' : '#ffffff');
  };
  btn?.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('theme', root.dataset.theme); } catch (e) {}
    sync();
    dispatchEvent(new Event('themechange'));
  });
  sync();
})();

// Highlight the nav link for the section on screen.
(() => {
  const links = [...document.querySelectorAll('.nav-links a')];
  const byId = new Map(links.map((a) => [a.getAttribute('href').slice(1), a]));
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      links.forEach((a) => a.removeAttribute('aria-current'));
      byId.get(e.target.id)?.setAttribute('aria-current', 'true');
    }
  }, { rootMargin: '-45% 0px -50% 0px' });
  byId.forEach((_, id) => { const s = document.getElementById(id); if (s) io.observe(s); });
})();

// Fade things up as they scroll into view.
(() => {
  const els = document.querySelectorAll('.card, .proj, .page, .pcard, .hob, .sec-head, .toolbox, .ledger-row, .about-text');
  if (REDUCED || !('IntersectionObserver' in window)) return;
  els.forEach((el) => el.classList.add('pre'));
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  }, { rootMargin: '0px 0px -8% 0px' });
  els.forEach((el) => io.observe(el));
})();

// Local time in Ithaca.
(() => {
  const els = document.querySelectorAll('.clock');
  const fmt = new Intl.DateTimeFormat('en-US', { timeZone: 'America/New_York', hour: 'numeric', minute: '2-digit' });
  const tick = () => { const t = fmt.format(new Date()).toLowerCase(); els.forEach((e) => { e.textContent = t; }); };
  tick(); setInterval(tick, 20000);
})();

// Polaroids on the hero "table": drag them anywhere, and they lean
// gently toward the cursor while you move around.
(() => {
  const table = document.getElementById('table');
  if (!table) return;
  const pols = [...table.querySelectorAll('.polaroid')];
  let z = 10;

  pols.forEach((p) => {
    let sx = 0, sy = 0, ox = 0, oy = 0, dragging = false;
    p.dataset.dx = 0; p.dataset.dy = 0;
    // stop the browser's native image drag, which would cancel ours
    p.addEventListener('dragstart', (e) => e.preventDefault());
    p.addEventListener('pointerdown', (e) => {
      e.preventDefault();
      dragging = true; p.setPointerCapture(e.pointerId);
      p.classList.add('dragging'); p.style.zIndex = ++z;
      sx = e.clientX; sy = e.clientY; ox = +p.dataset.dx; oy = +p.dataset.dy;
    });
    p.addEventListener('pointermove', (e) => {
      if (!dragging) return;
      p.dataset.dx = ox + e.clientX - sx; p.dataset.dy = oy + e.clientY - sy;
      place(p, 0, 0);
    });
    const end = () => { dragging = false; p.classList.remove('dragging'); };
    p.addEventListener('pointerup', end); p.addEventListener('pointercancel', end);
    // the drop-in animation owns transform until it finishes
    p.addEventListener('animationend', () => { p.classList.remove('drop'); place(p, 0, 0); });
  });

  function place(p, px, py) {
    p.style.translate = `${+p.dataset.dx + px}px ${+p.dataset.dy + py}px`;
  }

  if (REDUCED) return;
  const hero = document.getElementById('hero');
  hero.addEventListener('pointermove', (e) => {
    const r = hero.getBoundingClientRect();
    const fx = (e.clientX - r.left) / r.width - 0.5, fy = (e.clientY - r.top) / r.height - 0.5;
    pols.forEach((p, i) => {
      if (p.classList.contains('dragging')) return;
      const depth = 6 + (i % 3) * 5;
      place(p, fx * depth, fy * depth);
    });
  });
})();

// The hero background: a live Julia set.

// Hero: a Julia set rendered on the GPU. The cursor steers c, so moving
// the mouse anywhere reshapes the fractal; when idle, c drifts on its own.
// The set's edge is drawn from a distance estimate, so it stays a crisp hairline
// at any resolution; around it sit a soft colour glow and faint contour lines.
// Light mode reads like an etching on paper, dark mode like light on black.
(() => {
  const canvas = document.getElementById('julia');
  const hero = document.getElementById('hero');
  const out = document.getElementById('cval');
  const gl = canvas?.getContext('webgl', { antialias: false, premultipliedAlpha: false });
  if (!gl) { document.body.classList.add('no-webgl'); return; }
  const derivs = !!gl.getExtension('OES_standard_derivatives');

  const vs = 'attribute vec2 p; void main(){ gl_Position = vec4(p, 0., 1.); }';
  const fs = `${derivs ? '#extension GL_OES_standard_derivatives : enable\n#define DERIVS' : ''}
    precision highp float;
    uniform vec2 res; uniform vec2 c; uniform float zoom; uniform float dark;
    const int ITER = 160;

    // pastel stops: mint → sky → lavender → rose → peach
    vec3 pal(float t){
      vec3 a = vec3(.56,.86,.76), b = vec3(.56,.74,.94), d = vec3(.74,.64,.95), e = vec3(.95,.62,.74), f = vec3(.99,.74,.58);
      t = fract(t) * 4.0;
      if (t < 1.) return mix(a, b, t);
      if (t < 2.) return mix(b, d, t - 1.);
      if (t < 3.) return mix(d, e, t - 2.);
      return mix(e, f, t - 3.);
    }
    float hash(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }

    void main(){
      float unit = min(res.x, res.y);
      vec2 uv = (gl_FragCoord.xy - .5 * res) / unit * zoom;
      float px = zoom / unit;                       // one pixel, in fractal units
      vec2 z = uv, dz = vec2(1., 0.);
      float n = 0.;
      for (int i = 0; i < ITER; i++) {
        dz = 2. * vec2(z.x * dz.x - z.y * dz.y, z.x * dz.y + z.y * dz.x);
        z = vec2(z.x * z.x - z.y * z.y, 2. * z.x * z.y) + c;
        if (dot(z, z) > 1024.) break;
        n += 1.;
      }
      bool inside = n >= float(ITER) - 1.;
      float r = length(z);
      float de = inside ? 0. : .5 * r * log(r) / max(length(dz), 1e-6);
      float sn = inside ? float(ITER) : n - log2(log2(dot(z, z))) + 4.;

      // paper, or night
      vec2 q = gl_FragCoord.xy / res;
      vec3 bg = mix(mix(vec3(.976, .972, .962), vec3(.952, .950, .968), q.y),
                    mix(vec3(.030, .030, .042), vec3(.052, .044, .078), q.y), dark);

      float edge = inside ? 1. : exp(-de / (px * 1.1));     // the hairline
      float glow = inside ? 1. : exp(-de / (px * 70.));     // wide soft halo
      vec3 hue = pal(sqrt(sn / float(ITER)) * 1.8 + q.x * .35 + .1);

      // keep the middle calm behind the name; the set blooms toward the edges
      vec2 m = (q - .5) * vec2(res.x / unit, 1.) * vec2(1.25, 2.1);
      float focus = mix(.22, 1., smoothstep(.18, .75, length(m)));
      edge *= focus; glow *= mix(.55, 1., focus);

      // contour lines on the escape-time field, faded where they'd crowd
      float x = sn * .35, line = 0.;
      #ifdef DERIVS
        float w = fwidth(x);
        float f = fract(x), dl = min(f, 1. - f);
        line = (1. - smoothstep(0., w * 1.2, dl)) * smoothstep(.45, .08, w);
      #endif
      line *= inside ? 0. : 1.;

      vec3 col = bg;
      // light: watercolour halo, graphite contours, ink filament
      vec3 ink = mix(vec3(.10, .09, .18), hue * .42, .45);
      vec3 lightCol = mix(bg, hue, glow * .42);
      lightCol = mix(lightCol, ink, line * .07);
      lightCol = mix(lightCol, inside ? mix(bg, vec3(.80, .74, .93), .30 * focus) : ink, inside ? 1. : edge * .9);
      // dark: glowing halo, faint silver contours, luminous filament
      vec3 darkCol = bg + hue * glow * .30;
      darkCol += vec3(.75, .78, .9) * line * .05;
      darkCol = inside ? mix(bg, vec3(.20, .15, .32), .55 * focus) : mix(darkCol, mix(hue, vec3(1.), .35), edge * .95);
      col = mix(lightCol, darkCol, dark);

      // vignette (mostly in dark) and a little grain so gradients don't band
      float v = dot(q - .5, q - .5);
      col *= 1. - v * mix(.12, .9, dark);
      col += (hash(gl_FragCoord.xy) - .5) * mix(.018, .028, dark);
      gl_FragColor = vec4(col, 1.);
    }`;
  const sh = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return s; };
  const prog = gl.createProgram();
  gl.attachShader(prog, sh(gl.VERTEX_SHADER, vs)); gl.attachShader(prog, sh(gl.FRAGMENT_SHADER, fs));
  gl.linkProgram(prog);
  if (!gl.getProgramParameter(prog, gl.LINK_STATUS)) { document.body.classList.add('no-webgl'); return; }
  gl.useProgram(prog);
  const buf = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, buf);
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1,-1, 1,-1, -1,1, 1,1]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(prog, 'p'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  const uRes = gl.getUniformLocation(prog, 'res'), uC = gl.getUniformLocation(prog, 'c'), uZoom = gl.getUniformLocation(prog, 'zoom'), uDark = gl.getUniformLocation(prog, 'dark');

  // render near device resolution so the hairlines stay sharp
  const SCALE = Math.min(devicePixelRatio || 1, 1.5);
  function resize() {
    canvas.width = Math.round(canvas.clientWidth * SCALE);
    canvas.height = Math.round(canvas.clientHeight * SCALE);
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.uniform2f(uRes, canvas.width, canvas.height);
    gl.uniform1f(uZoom, canvas.clientWidth < 500 ? 3.4 : 2.6);
  }

  // c lives on a ring near the edge of the Mandelbrot set, where Julia sets are prettiest.
  let angle = 2.1, radius = 0.7885, targetA = angle, targetR = radius, idle = 0;
  hero.addEventListener('pointermove', (e) => {
    const r = hero.getBoundingClientRect();
    const fx = (e.clientX - r.left) / r.width, fy = (e.clientY - r.top) / r.height;
    targetA = 1.2 + fx * 2.6;
    targetR = 0.74 + fy * 0.07;
    idle = 0;
  });

  let visible = true;
  new IntersectionObserver(([e]) => { visible = e.isIntersecting; }).observe(hero);

  // the theme switch fades between palettes instead of snapping
  const isDark = () => (document.documentElement.dataset.theme === 'dark' ? 1 : 0);
  let dark = isDark();

  function frame() {
    if (visible && !document.hidden) {
      idle++;
      if (idle > 120 && !REDUCED) targetA += 0.0016;
      angle += (targetA - angle) * 0.04;
      radius += (targetR - radius) * 0.04;
      dark = REDUCED ? isDark() : dark + (isDark() - dark) * 0.08;
      const cx = radius * Math.cos(angle), cy = radius * Math.sin(angle);
      gl.uniform2f(uC, cx, cy);
      gl.uniform1f(uDark, dark);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      if (out) out.textContent = `c = ${cx.toFixed(3)} ${cy < 0 ? '−' : '+'} ${Math.abs(cy).toFixed(3)}i`;
    }
    if (!REDUCED) requestAnimationFrame(frame);
  }
  resize();
  addEventListener('resize', resize);
  frame();
  if (REDUCED) {
    hero.addEventListener('pointermove', () => requestAnimationFrame(frame));
    addEventListener('themechange', () => requestAnimationFrame(frame));
  }
})();

// The penguins: they watch the cursor, blink, and one slides down the timeline.

// Every penguin on the page watches the cursor and blinks now and then.
(() => {
  const eyes = [...document.querySelectorAll('[data-eye]')].map((g) => ({
    g, pupil: g.querySelector('.pupil'), glint: g.querySelector('.glint'), lid: g.querySelector('.lid'),
    cx: +g.querySelector('.white').getAttribute('cx'), cy: +g.querySelector('.white').getAttribute('cy'),
  }));
  let mx = innerWidth / 2, my = innerHeight / 3, raf = 0;
  addEventListener('pointermove', (e) => { mx = e.clientX; my = e.clientY; if (!raf) raf = requestAnimationFrame(look); }, { passive: true });
  addEventListener('scroll', () => { if (!raf) raf = requestAnimationFrame(look); }, { passive: true });

  function look() {
    raf = 0;
    for (const e of eyes) {
      const svg = e.g.ownerSVGElement, r = svg.getBoundingClientRect();
      if (r.bottom < 0 || r.top > innerHeight) continue;
      const k = r.width / 200; // viewBox → px
      const ex = r.left + e.cx * k, ey = r.top + e.cy * k;
      const a = Math.atan2(my - ey, mx - ex), d = Math.min(4.5, Math.hypot(mx - ex, my - ey) / 40);
      const dx = Math.cos(a) * d, dy = Math.sin(a) * d;
      e.pupil.setAttribute('transform', `translate(${dx} ${dy})`);
      e.glint.setAttribute('transform', `translate(${dx} ${dy})`);
    }
  }
  look();

  // blink: both eyes of a penguin together
  const byPenguin = new Map();
  eyes.forEach((e) => { const p = e.g.ownerSVGElement; byPenguin.set(p, [...(byPenguin.get(p) || []), e]); });
  byPenguin.forEach((list) => {
    const blink = () => {
      list.forEach((e) => e.lid.setAttribute('ry', 12));
      setTimeout(() => list.forEach((e) => e.lid.setAttribute('ry', 0)), 120);
      setTimeout(blink, 2500 + Math.random() * 4000);
    };
    if (!REDUCED) setTimeout(blink, 1200 + Math.random() * 2500);
  });
})();

// A second penguin belly-slides down the experience timeline as you scroll.
(() => {
  const slider = document.querySelector('.slider');
  const tl = document.querySelector('.timeline');
  if (!slider || !tl) return;
  let last = -1, stopT = 0;
  const update = () => {
    const r = tl.getBoundingClientRect();
    const target = innerHeight * 0.45;
    const t = Math.max(0, Math.min(1, (target - r.top) / r.height));
    const y = t * (r.height - 60);
    slider.style.transform = `translateY(${y}px)`;
    if (Math.abs(y - last) > 0.5 && t > 0 && t < 1) {
      slider.classList.add('moving');
      clearTimeout(stopT); stopT = setTimeout(() => slider.classList.remove('moving'), 180);
    }
    last = y;
  };
  addEventListener('scroll', () => requestAnimationFrame(update), { passive: true });
  addEventListener('resize', update);
  update();
})();

// ── award figures that count up ──

// Count each award's headline number up from zero when it scrolls into view.
(() => {
  const els = document.querySelectorAll('.ledger .count');
  if (REDUCED || !('IntersectionObserver' in window)) return;
  const run = (el) => {
    const text = el.textContent, m = text.match(/\d[\d,]*/);
    if (!m) return;
    const target = +m[0].replace(/,/g, ''), commas = m[0].includes(',');
    if (target < 10) return;  // "#1" reads better without counting from #0
    const fmt = (n) => (commas ? n.toLocaleString('en-US') : String(n));
    const t0 = performance.now(), dur = 1100;
    const step = (t) => {
      const p = Math.min(1, (t - t0) / dur), eased = 1 - Math.pow(1 - p, 3);
      el.textContent = text.replace(m[0], fmt(Math.round(target * eased)));
      if (p < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) if (e.isIntersecting) { run(e.target); io.unobserve(e.target); }
  }, { rootMargin: '0px 0px -15% 0px' });
  els.forEach((el) => io.observe(el));
})();


// ── analytics: what visitors looked at and clicked (only runs when GA_ID is set) ──
(() => {
  if (typeof gtag !== 'function') return;
  const track = (name, params) => gtag('event', name, params);

  // Each section, the first time half of it (or the whole screen's worth) is on screen.
  const seen = new Set();
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting || seen.has(e.target.id)) continue;
      seen.add(e.target.id);
      track('section_view', { section: e.target.id });
      io.unobserve(e.target);
    }
  }, { threshold: 0.3 });
  document.querySelectorAll('section[id]').forEach((s) => io.observe(s));

  // How far down the page they got.
  const marks = [25, 50, 75, 100], hit = new Set();
  addEventListener('scroll', () => {
    const pct = (scrollY + innerHeight) / document.documentElement.scrollHeight * 100;
    for (const m of marks) if (pct >= m - 1 && !hit.has(m)) { hit.add(m); track('scroll_depth', { percent: m }); }
  }, { passive: true });

  // Which "What I built" lists they opened, and which links they clicked.
  const cardName = (el) => el.closest('.pcard, .exp-card')?.querySelector('h3')?.textContent.replace('↗', '').trim() || '';
  document.querySelectorAll('.built').forEach((d) => d.addEventListener('toggle', () => {
    if (d.open) track('open_details', { item: cardName(d) });
  }));
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a[href]');
    if (a) track('link_click', { label: a.textContent.replace('↗', '').trim().slice(0, 60), item: cardName(a), url: a.href });
    if (e.target.closest('.theme-toggle')) track('theme_toggle', { theme: document.documentElement.dataset.theme });
  });
})();
