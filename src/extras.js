// ── award figures that count up, and the toolbox filter ──

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

// Toolbox: the buttons above the logo grid show one group at a time.
(() => {
  const box = document.querySelector('.toolbox');
  if (!box) return;
  const buttons = [...box.querySelectorAll('[data-filter]')];
  const tiles = [...box.querySelectorAll('.tb-grid li')];
  const count = box.querySelector('.tb-count');
  buttons.forEach((b) => b.addEventListener('click', () => {
    const f = b.dataset.filter;
    buttons.forEach((x) => x.setAttribute('aria-pressed', String(x === b)));
    let shown = 0;
    tiles.forEach((li) => {
      const on = f === 'all' || li.dataset.group === f;
      li.hidden = !on;
      if (on) { li.style.setProperty('--i', shown++); li.classList.remove('pop'); void li.offsetWidth; li.classList.add('pop'); }
    });
    count.textContent = `${shown} tools`;
  }));
})();
