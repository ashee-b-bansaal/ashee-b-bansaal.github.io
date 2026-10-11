// ── Edit mode (only loaded by editor.py on your own machine) ──
(() => {
  const HEADERS = { 'Content-Type': 'application/json', 'X-Portfolio-Editor': '1' };
  const edits = new Map(); // "PROJECTS.2.text" → new value
  document.documentElement.classList.add('editing');

  // keep only simple formatting from contenteditable
  const clean = (el) => el.innerHTML
    .replace(/<br\s*\/?>/gi, ' ').replace(/<\/?(div|p)\b[^>]*>/gi, ' ')
    .replace(/<(?!\/?(em|strong|b|i)\b)[^>]*>/gi, '')
    .replace(/\s+/g, ' ')
    .replace(/^(?:&nbsp;|\s)+|(?:&nbsp;|\s)+$/g, '') // stray spaces the browser adds at the ends
    .replace(/&nbsp; | &nbsp;/g, ' ');

  const track = (path, value, orig, el) => {
    value === orig ? edits.delete(path) : edits.set(path, value);
    el?.classList.toggle('ed-changed', edits.has(path));
    refresh();
  };

  // 1. every tagged piece of text becomes editable in place
  document.querySelectorAll('[data-edit]').forEach((el) => {
    el.contentEditable = 'true';
    const orig = clean(el);
    el.addEventListener('input', () => track(el.dataset.edit, clean(el), orig, el));
    el.addEventListener('keydown', (e) => { if (e.key === 'Enter') { e.preventDefault(); el.blur(); } });
    el.addEventListener('paste', (e) => {
      e.preventDefault();
      document.execCommand('insertText', false, e.clipboardData.getData('text/plain'));
    });
  });

  // links don't navigate while editing (in-page # links still do)
  document.addEventListener('click', (e) => {
    const a = e.target.closest('a');
    if (a && !a.closest('.ed-ui') && !(a.getAttribute('href') || '').startsWith('#')) e.preventDefault();
  }, true);

  const linkButton = (path, current, onSet) => {
    const b = document.createElement('button');
    b.type = 'button'; b.className = 'ed-ui ed-link'; b.textContent = 'Link';
    b.title = 'Change where this goes';
    b.addEventListener('click', (e) => {
      e.preventDefault(); e.stopPropagation();
      const url = prompt('Link address (use # if you don’t have one yet):', current());
      if (url !== null) { onSet(url.trim()); track(path, url.trim(), b.dataset.orig, b); }
    });
    b.dataset.orig = current();
    return b;
  };

  // 2. buttons / hobby links get a small "link" control next to them
  document.querySelectorAll('[data-edit-href]').forEach((a) => {
    if (a.closest('.pcard h3')) return; // project titles use the card toolbar instead
    a.after(linkButton(a.dataset.editHref, () => a.getAttribute('href'), (u) => a.setAttribute('href', u)));
  });

  // 3. a toolbar on every project card
  const cards = [...document.querySelectorAll('.pcard[data-project]')];
  cards.forEach((card, idx) => {
    const i = +card.dataset.project;
    const bar = document.createElement('div');
    bar.className = 'ed-ui ed-tools';
    const btn = (label, title, fn, disabled) => {
      const b = document.createElement('button');
      b.type = 'button'; b.textContent = label; b.title = title; b.disabled = !!disabled;
      b.addEventListener('click', fn); bar.append(b); return b;
    };
    btn('↑', 'Move earlier', () => save([{ op: 'up', i }]), idx === 0);
    btn('↓', 'Move later', () => save([{ op: 'down', i }]), idx === cards.length - 1);
    const file = Object.assign(document.createElement('input'), { type: 'file', accept: 'image/*', hidden: true });
    file.addEventListener('change', () => {
      const f = file.files[0]; if (!f) return;
      const r = new FileReader();
      r.onload = () => save([{ op: 'image', i, name: f.name, data: r.result }]);
      r.readAsDataURL(f);
    });
    bar.append(file);
    btn('Image', 'Upload a screenshot or photo', () => file.click());
    const art = card.querySelector('.card-art');
    const fitBtn = btn('', 'Show the whole image, or fill the box', () => {
      const next = card.dataset.fit === 'cover' ? 'contain' : 'cover';
      card.dataset.fit = next;
      art?.classList.toggle('is-cover', next === 'cover');
      const img = art?.querySelector('img'); if (img) img.style.objectFit = next;
      fitBtn.textContent = next === 'cover' ? 'Fill' : 'Fit';
      track(`PROJECTS.${i}.fit`, next, fitBtn.dataset.orig, fitBtn);
    });
    fitBtn.dataset.orig = card.dataset.fit;
    fitBtn.textContent = card.dataset.fit === 'cover' ? 'Fill' : 'Fit';
    bar.append(linkButton(`PROJECTS.${i}.link`, () => card.dataset.link, (u) => { card.dataset.link = u; }));
    btn('Copy', 'Duplicate this project', () => save([{ op: 'duplicate', i }]));
    const del = btn('Delete', 'Delete this project', () => {
      if (confirm(`Delete “${card.querySelector('h3').textContent.replace('↗', '').trim()}”?`)) save([{ op: 'delete', i }]);
    }, cards.length === 1);
    del.classList.add('ed-danger');
    card.prepend(bar);
  });
  const grid = document.querySelector('.pgrid');
  if (grid) {
    const add = document.createElement('button');
    add.type = 'button'; add.className = 'ed-ui ed-add'; add.textContent = '+ Add a project';
    add.addEventListener('click', () => save([{ op: 'new' }]));
    grid.after(add);
  }

  // 4. the save bar
  const bar = document.createElement('div');
  bar.className = 'ed-ui ed-bar';
  bar.innerHTML = '<span class="ed-msg"></span><button type="button" class="ed-discard">Discard</button><button type="button" class="ed-save">Save</button>';
  document.body.append(bar);
  const msg = bar.querySelector('.ed-msg'), saveBtn = bar.querySelector('.ed-save'), discard = bar.querySelector('.ed-discard');
  function refresh(text) {
    const n = edits.size;
    msg.textContent = text || (n ? `${n} unsaved change${n > 1 ? 's' : ''}` : 'Edit mode · click any text to change it');
    saveBtn.disabled = discard.disabled = !n;
  }
  saveBtn.addEventListener('click', () => save());
  discard.addEventListener('click', () => { if (confirm('Throw away your unsaved changes?')) { edits.clear(); reload(); } });
  addEventListener('keydown', (e) => { if ((e.metaKey || e.ctrlKey) && e.key === 's') { e.preventDefault(); if (edits.size) save(); } });
  addEventListener('beforeunload', (e) => { if (edits.size) e.preventDefault(); });

  function reload() {
    try { sessionStorage.setItem('ed-scroll', String(scrollY)); } catch (_) {}
    location.reload();
  }
  async function save(ops = []) {
    refresh('Saving…'); saveBtn.disabled = true;
    try {
      const res = await fetch('/_save', {
        method: 'POST', headers: HEADERS,
        body: JSON.stringify({ edits: [...edits].map(([path, value]) => ({ path, value })), ops }),
      });
      const out = await res.json();
      if (!out.ok) throw new Error(out.error);
      edits.clear(); reload();
    } catch (err) {
      refresh('Couldn’t save: ' + err.message); saveBtn.disabled = false;
    }
  }

  try {
    const y = sessionStorage.getItem('ed-scroll');
    if (y) { sessionStorage.removeItem('ed-scroll'); history.scrollRestoration = 'manual'; scrollTo(0, +y); }
  } catch (_) {}
  refresh();
})();
