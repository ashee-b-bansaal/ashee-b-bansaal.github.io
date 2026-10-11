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
