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
