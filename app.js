// ── shared behaviour: nav highlight, scroll fade-in, clock ──
const REDUCED = matchMedia('(prefers-reduced-motion: reduce)').matches;

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
  const els = document.querySelectorAll('.card, .proj, .page, .pcard, .hob, .sec-head, .skills, .about-text');
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
    p.addEventListener('pointerdown', (e) => {
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
(() => {
  const canvas = document.getElementById('julia');
  const hero = document.getElementById('hero');
  const out = document.getElementById('cval');
  const gl = canvas?.getContext('webgl', { antialias: false, premultipliedAlpha: false });
  if (!gl) { document.body.classList.add('no-webgl'); return; }

  const vs = 'attribute vec2 p; void main(){ gl_Position = vec4(p, 0., 1.); }';
  const fs = `
    precision highp float;
    uniform vec2 res; uniform vec2 c; uniform float zoom;
    vec3 pal(float t){
      // pastel stops: mint → sky → lavender → rose → peach
      vec3 a = vec3(.655,.898,.827), b = vec3(.659,.784,.910), d = vec3(.784,.722,.878), e = vec3(.910,.722,.769), f = vec3(.957,.773,.659);
      t = fract(t) * 4.0;
      if (t < 1.) return mix(a, b, t);
      if (t < 2.) return mix(b, d, t - 1.);
      if (t < 3.) return mix(d, e, t - 2.);
      return mix(e, f, t - 3.);
    }
    void main(){
      vec2 uv = (gl_FragCoord.xy - .5 * res) / min(res.x, res.y) * zoom;
      vec2 z = uv; float n = 0.;
      for (int i = 0; i < 140; i++) {
        z = vec2(z.x*z.x - z.y*z.y, 2.*z.x*z.y) + c;
        if (dot(z, z) > 256.) break;
        n += 1.;
      }
      vec3 bg = vec3(.961);
      if (n >= 139.) { gl_FragColor = vec4(mix(bg, vec3(.784,.722,.878), .55), 1.); return; }
      float sn = n - log2(log2(dot(z, z))) + 4.;
      float t = sqrt(sn / 140.);
      vec3 col = pal(t * 2.2 + .15);
      float strength = smoothstep(.02, .45, t);
      gl_FragColor = vec4(mix(bg, col, strength * .95), 1.);
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
  const uRes = gl.getUniformLocation(prog, 'res'), uC = gl.getUniformLocation(prog, 'c'), uZoom = gl.getUniformLocation(prog, 'zoom');

  const SCALE = 0.6; // render at lower resolution; it's soft anyway
  function resize() {
    canvas.width = Math.round(canvas.clientWidth * SCALE);
    canvas.height = Math.round(canvas.clientHeight * SCALE);
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.uniform2f(uRes, canvas.width, canvas.height);
    gl.uniform1f(uZoom, canvas.width < 500 ? 3.4 : 2.6);
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

  function frame() {
    if (visible && !document.hidden) {
      idle++;
      if (idle > 120 && !REDUCED) targetA += 0.0016;
      angle += (targetA - angle) * 0.04;
      radius += (targetR - radius) * 0.04;
      const cx = radius * Math.cos(angle), cy = radius * Math.sin(angle);
      gl.uniform2f(uC, cx, cy);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      if (out) out.textContent = `c = ${cx.toFixed(3)} ${cy < 0 ? '−' : '+'} ${Math.abs(cy).toFixed(3)}i`;
    }
    if (!REDUCED) requestAnimationFrame(frame);
  }
  resize();
  addEventListener('resize', resize);
  frame();
  if (REDUCED) hero.addEventListener('pointermove', () => requestAnimationFrame(frame));
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
