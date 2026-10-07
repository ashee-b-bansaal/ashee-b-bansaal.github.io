// ── shared behaviour (all three designs) ──
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
  const els = document.querySelectorAll('.card, .proj, .page, .hob, .sec-head, .skills, .about-text');
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

// ── PENGUIN edition ──

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

// Pebble (the hero penguin) waves when hovered or tapped and says something.
(() => {
  const p = document.getElementById('pebble');
  const speech = document.getElementById('speech');
  if (!p) return;
  const lines = [
    'hi! i’m pebble.',
    'ashee is open to summer 2027 internships.',
    'psst, the résumé button is right there →',
    'penguins give pebbles to people they like. here: ●',
    'did you know ashee writes poems?',
    'i also slide down the timeline. scroll and see.',
  ];
  let i = 0, busy = false;
  const poke = () => {
    if (busy) return; busy = true;
    p.classList.add('wave', 'waddle');
    i = (i + 1) % lines.length;
    speech.textContent = lines[i];
    setTimeout(() => { p.classList.remove('wave', 'waddle'); busy = false; }, 1800);
  };
  p.addEventListener('pointerenter', poke);
  document.getElementById('pebble-btn')?.addEventListener('click', poke);
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

// Footer penguin waves when it scrolls into view.
(() => {
  const fp = document.querySelector('.foot-penguin');
  if (!fp || REDUCED) return;
  new IntersectionObserver(([e]) => { if (e.isIntersecting) { fp.classList.add('wave'); setTimeout(() => fp.classList.remove('wave'), 2000); } }).observe(fp);
})();
