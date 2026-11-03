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
