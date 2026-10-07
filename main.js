// Mark the nav link for whichever section is on screen.
(() => {
  const links = [...document.querySelectorAll('.bar-links a')];
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

// Hero: a tiny live CalibraType. Every tap in the hero is treated as an
// attempt to hit the Résumé "key". We keep a Bayesian estimate of where taps
// really land (prior centered on the key) and draw its 1σ/2σ ellipses.
(() => {
  const hero = document.getElementById('hero');
  const canvas = document.getElementById('touch');
  const key = document.getElementById('key');
  const stats = document.getElementById('stats');
  const blobCanvas = document.getElementById('blob');
  const bctx = blobCanvas?.getContext('2d');
  if (!hero || !canvas || !key) return;

  const ctx = canvas.getContext('2d');
  const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const css = (v) => getComputedStyle(document.documentElement).getPropertyValue(v).trim();
  const WINDOW = 40;      // only the most recent taps count, so it adapts
  const KAPPA = 3;        // prior strength, in "pseudo-taps"
  const PRIOR_SD = 40;    // px

  let taps = [];          // {x, y, t} relative to key center
  let shown = null;       // ellipse currently drawn (eases toward target)
  let w = 0, h = 0, dpr = 1, cx = 0, cy = 0;

  function measure() {
    const r = hero.getBoundingClientRect();
    const k = key.getBoundingClientRect();
    dpr = Math.min(devicePixelRatio || 1, 2);
    w = r.width; h = r.height;
    canvas.width = w * dpr; canvas.height = h * dpr;
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    if (bctx) { blobCanvas.width = w * dpr; blobCanvas.height = h * dpr; bctx.setTransform(dpr, 0, 0, dpr, 0, 0); }
    cx = k.left - r.left + k.width / 2;
    cy = k.top - r.top + k.height / 2;
  }

  // Posterior mean/covariance with a conjugate-style prior at the key center.
  function fit() {
    const n = taps.length;
    let sx = 0, sy = 0;
    for (const p of taps) { sx += p.x; sy += p.y; }
    const mx = sx / (n + KAPPA), my = sy / (n + KAPPA);
    let a = KAPPA * PRIOR_SD ** 2, b = 0, c = KAPPA * PRIOR_SD ** 2;
    for (const p of taps) {
      const dx = p.x - mx, dy = p.y - my;
      a += dx * dx; b += dx * dy; c += dy * dy;
    }
    a /= n + KAPPA; b /= n + KAPPA; c /= n + KAPPA;
    const tr = (a + c) / 2, d = Math.sqrt(((a - c) / 2) ** 2 + b * b);
    return { mx, my, s1: Math.sqrt(tr + d), s2: Math.sqrt(Math.max(tr - d, 1)), th: 0.5 * Math.atan2(2 * b, a - c), n };
  }

  function lerp(a, b, t) { return a + (b - a) * t; }
  function lerpAngle(a, b, t) {
    let d = b - a;
    while (d > Math.PI / 2) d -= Math.PI;
    while (d < -Math.PI / 2) d += Math.PI;
    return a + d * t;
  }

  function draw(now) {
    const target = fit();
    if (!shown || still) shown = { ...target };
    else {
      const k = 0.12;
      shown.mx = lerp(shown.mx, target.mx, k); shown.my = lerp(shown.my, target.my, k);
      shown.s1 = lerp(shown.s1, target.s1, k); shown.s2 = lerp(shown.s2, target.s2, k);
      shown.th = lerpAngle(shown.th, target.th, k);
    }

    ctx.clearRect(0, 0, w, h);
    const accent = css('--accent'), ink = css('--ink-3');
    const ex = cx + shown.mx, ey = cy + shown.my;

    // the big soft blob: the same Gaussian, blown up to fill the hero
    if (bctx) {
      bctx.clearRect(0, 0, w, h);
      const R = Math.min(Math.max(w, h) * 0.42, 560);
      const sx = Math.max(shown.s1 / 40, 0.55), sy = Math.max(shown.s2 / 40, 0.45);
      bctx.save();
      bctx.translate(ex, ey); bctx.rotate(shown.th); bctx.scale(sx, sy * 0.8);
      const g = bctx.createRadialGradient(0, 0, 0, 0, 0, R);
      g.addColorStop(0, 'rgba(39,65,245,0.40)');
      g.addColorStop(0.45, 'rgba(39,65,245,0.17)');
      g.addColorStop(1, 'rgba(39,65,245,0)');
      bctx.fillStyle = g;
      bctx.beginPath(); bctx.arc(0, 0, R, 0, Math.PI * 2); bctx.fill();
      bctx.restore();
    }

    // ellipses
    ctx.save();
    ctx.translate(ex, ey); ctx.rotate(shown.th);
    ctx.strokeStyle = accent; ctx.lineWidth = 1.2;
    ctx.globalAlpha = 0.9; ctx.beginPath(); ctx.ellipse(0, 0, shown.s1, shown.s2, 0, 0, Math.PI * 2); ctx.stroke();
    ctx.setLineDash([3, 4]); ctx.globalAlpha = 0.45;
    ctx.beginPath(); ctx.ellipse(0, 0, shown.s1 * 2, shown.s2 * 2, 0, 0, Math.PI * 2); ctx.stroke();
    ctx.restore();

    // mean crosshair
    ctx.strokeStyle = accent; ctx.globalAlpha = 0.9; ctx.setLineDash([]);
    ctx.beginPath(); ctx.moveTo(ex - 5, ey); ctx.lineTo(ex + 5, ey); ctx.moveTo(ex, ey - 5); ctx.lineTo(ex, ey + 5); ctx.stroke();

    // taps: fresh ones pop, older ones settle into faint dots
    for (const p of taps) {
      const age = (now - p.t) / 1000;
      const pop = still ? 0 : Math.max(0, 1 - age / 0.6);
      ctx.globalAlpha = 0.35 + 0.5 * Math.max(0, 1 - age / 6);
      ctx.fillStyle = ink;
      ctx.beginPath(); ctx.arc(cx + p.x, cy + p.y, 2.6, 0, Math.PI * 2); ctx.fill();
      if (pop > 0) {
        ctx.strokeStyle = accent; ctx.globalAlpha = pop;
        ctx.beginPath(); ctx.arc(cx + p.x, cy + p.y, 3 + (1 - pop) * 16, 0, Math.PI * 2); ctx.stroke();
      }
    }
    ctx.globalAlpha = 1;

    const f = (v) => (v >= 0 ? '+' : '−') + Math.abs(Math.round(v));
    stats.textContent = `n = ${target.n} taps    μ = (${f(target.mx)}, ${f(target.my)}) px off-center\nσ = ${Math.round(target.s1)} × ${Math.round(target.s2)} px    θ = ${Math.round(target.th * 180 / Math.PI)}°`;
  }

  let raf = 0, last = 0;
  function loop(now) {
    draw(now);
    // keep animating while something is still moving or popping
    if (!still && now - last < 1800) raf = requestAnimationFrame(loop);
    else raf = 0;
  }
  function kick() { last = performance.now(); if (!raf) raf = requestAnimationFrame(loop); }

  function add(x, y) {
    taps.push({ x: x - cx, y: y - cy, t: performance.now() });
    if (taps.length > WINDOW) taps.shift();
    kick();
  }

  hero.addEventListener('pointerdown', (e) => {
    if (e.target.closest('.readout a, .scroll-cue')) return;
    const r = hero.getBoundingClientRect();
    add(e.clientX - r.left, e.clientY - r.top);
  });

  // A few simulated thumbs to start: aimed at the key, landing low and right
  // (which is what real thumbs tend to do).
  function seed() {
    const g = () => { let u = 0; for (let i = 0; i < 6; i++) u += Math.random(); return u - 3; };
    const demo = Array.from({ length: 7 }, () => [16 + g() * 34, 12 + g() * 15]);
    if (still) { demo.forEach(([x, y]) => add(cx + x, cy + y)); return; }
    demo.forEach(([x, y], i) => setTimeout(() => add(cx + x, cy + y), 1300 + i * 260));
  }

  addEventListener('resize', () => { measure(); kick(); });
  hero.addEventListener('animationend', () => { measure(); kick(); });
  document.fonts?.ready.then(() => { measure(); kick(); });
  measure(); kick(); seed();
})();

// Local time in Ithaca, for the corner and the footer.
(() => {
  const els = document.querySelectorAll('.clock');
  if (!els.length) return;
  const fmt = new Intl.DateTimeFormat('en-US', { timeZone: 'America/New_York', hour: 'numeric', minute: '2-digit' });
  const tick = () => { const t = fmt.format(new Date()).toLowerCase(); els.forEach((e) => { e.textContent = t; }); };
  tick(); setInterval(tick, 20000);
})();
