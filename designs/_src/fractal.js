// ── FRACTAL edition ──

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

// Project cards: each draws its own classic fractal when it scrolls into view.
(() => {
  const ink = 'rgba(12,10,9,0.72)';
  const draw = {
    dragon(ctx, w, h, steps) {
      // Heighway dragon via turn sequence
      const n = 12, total = 2 ** n;
      let x = w * 0.76, y = h * 0.36, dir = 0, len = Math.min(w, h) / 92;
      ctx.beginPath(); ctx.moveTo(x, y);
      for (let i = 1; i <= Math.min(total, steps); i++) {
        const turn = (((i & -i) << 1) & i) !== 0 ? -1 : 1;
        x += Math.cos(dir * Math.PI / 2) * len; y += Math.sin(dir * Math.PI / 2) * len;
        ctx.lineTo(x, y);
        dir = (dir + turn + 4) % 4;
      }
      ctx.stroke();
      return total;
    },
    sierpinski(ctx, w, h, steps) {
      const s = Math.min(w, h) * 0.8, cx = w / 2, top = (h - s * 0.866) / 2;
      const P = [[cx, top], [cx - s / 2, top + s * 0.866], [cx + s / 2, top + s * 0.866]];
      let x = cx, y = h / 2; let seed = 7;
      const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
      ctx.fillStyle = ink;
      for (let i = 0, n = Math.min(steps, 6000) * 6; i < n; i++) {
        const p = P[Math.floor(rnd() * 3)];
        x = (x + p[0]) / 2; y = (y + p[1]) / 2;
        if (i > 10) ctx.fillRect(x, y, 1, 1);
      }
      return 6000;
    },
    koch(ctx, w, h, steps) {
      const s = Math.min(w, h) * 0.62, cx = w / 2, cy = h / 2 + s * 0.08;
      const r = s / Math.sqrt(3);
      let pts = [0, 1, 2].map((k) => [cx + r * Math.cos(-Math.PI / 2 + k * 2 * Math.PI / 3), cy + r * Math.sin(-Math.PI / 2 + k * 2 * Math.PI / 3)]);
      pts.push(pts[0]);
      for (let d = 0; d < 4; d++) {
        const next = [];
        for (let i = 0; i < pts.length - 1; i++) {
          const [ax, ay] = pts[i], [bx, by] = pts[i + 1];
          const dx = (bx - ax) / 3, dy = (by - ay) / 3;
          const p1 = [ax + dx, ay + dy], p2 = [ax + 2 * dx, ay + 2 * dy];
          const px = p1[0] + dx * 0.5 + dy * 0.866, py = p1[1] + dy * 0.5 - dx * 0.866;
          next.push([ax, ay], p1, [px, py], p2);
        }
        next.push(pts[pts.length - 1]); pts = next;
      }
      ctx.beginPath(); ctx.moveTo(...pts[0]);
      for (let i = 1; i < Math.min(pts.length, steps); i++) ctx.lineTo(...pts[i]);
      ctx.stroke();
      return pts.length;
    },
    fern(ctx, w, h, steps) {
      let x = 0, y = 0; let seed = 3;
      const rnd = () => ((seed = (seed * 16807) % 2147483647) / 2147483647);
      ctx.fillStyle = ink;
      const sc = h / 11, ox = w / 2;
      for (let i = 0, n = Math.min(steps, 5000) * 8; i < n; i++) {
        const r = rnd(); let nx, ny;
        if (r < 0.01) { nx = 0; ny = 0.16 * y; }
        else if (r < 0.86) { nx = 0.85 * x + 0.04 * y; ny = -0.04 * x + 0.85 * y + 1.6; }
        else if (r < 0.93) { nx = 0.2 * x - 0.26 * y; ny = 0.23 * x + 0.22 * y + 1.6; }
        else { nx = -0.15 * x + 0.28 * y; ny = 0.26 * x + 0.24 * y + 0.44; }
        x = nx; y = ny;
        ctx.fillRect(ox + x * sc, h - 10 - y * sc * 0.95, 1, 1);
      }
      return 5000;
    },
    tree(ctx, w, h, steps) {
      let count = 0;
      const branch = (x, y, len, ang, depth) => {
        if (depth === 0 || count >= steps) return;
        const x2 = x + Math.cos(ang) * len, y2 = y + Math.sin(ang) * len;
        ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x2, y2); ctx.stroke(); count++;
        branch(x2, y2, len * 0.72, ang - 0.42, depth - 1);
        branch(x2, y2, len * 0.72, ang + 0.36, depth - 1);
      };
      branch(w / 2, h * 0.92, h * 0.24, -Math.PI / 2, 11);
      return 2047;
    },
  };

  function render(canvas, progress) {
    const dpr = Math.min(devicePixelRatio || 1, 2);
    const w = canvas.clientWidth, h = canvas.clientHeight;
    if (canvas.width !== w * dpr) { canvas.width = w * dpr; canvas.height = h * dpr; }
    const ctx = canvas.getContext('2d');
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    ctx.clearRect(0, 0, w, h);
    ctx.strokeStyle = ink; ctx.lineWidth = 0.9; ctx.lineJoin = 'round';
    return draw[canvas.dataset.kind](ctx, w, h, progress);
  }

  const canvases = document.querySelectorAll('canvas.fractal');
  const io = new IntersectionObserver((entries) => {
    for (const e of entries) {
      if (!e.isIntersecting) continue;
      io.unobserve(e.target);
      const c = e.target;
      if (REDUCED) { render(c, 1e9); continue; }
      const total = render(c, 1);
      let p = 1; const t0 = performance.now();
      const step = (now) => {
        p = Math.ceil(total * Math.min(1, (now - t0) / 1800));
        render(c, p);
        if (p < total) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    }
  }, { rootMargin: '0px 0px -10% 0px' });
  canvases.forEach((c) => io.observe(c));
  addEventListener('resize', () => canvases.forEach((c) => render(c, 1e9)));
})();

// Footer: a Barnsley fern that grows row of fronds across the bottom.
(() => {
  const c = document.getElementById('fern');
  if (!c) return;
  const io = new IntersectionObserver(([e]) => {
    if (!e.isIntersecting) return;
    io.disconnect();
    const dpr = Math.min(devicePixelRatio || 1, 2), w = c.clientWidth, h = c.clientHeight;
    c.width = w * dpr; c.height = h * dpr;
    const ctx = c.getContext('2d'); ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    const cols = ['#7fcfb7', '#8fb3dc', '#b5a1d8', '#dda1b1', '#eaae8c'];
    const plants = Math.max(3, Math.round(w / 160));
    const state = Array.from({ length: plants }, (_, i) => ({ x: 0, y: 0, ox: (i + 0.5) * w / plants, sc: h / 11 * (0.7 + ((i * 37) % 10) / 25), col: cols[i % cols.length], flip: i % 2 ? -1 : 1 }));
    let n = 0;
    const tick = () => {
      for (const s of state) {
        ctx.fillStyle = s.col;
        for (let k = 0; k < 220; k++) {
          const r = Math.random(); let nx, ny; const { x, y } = s;
          if (r < 0.01) { nx = 0; ny = 0.16 * y; }
          else if (r < 0.86) { nx = 0.85 * x + 0.04 * y; ny = -0.04 * x + 0.85 * y + 1.6; }
          else if (r < 0.93) { nx = 0.2 * x - 0.26 * y; ny = 0.23 * x + 0.22 * y + 1.6; }
          else { nx = -0.15 * x + 0.28 * y; ny = 0.26 * x + 0.24 * y + 0.44; }
          s.x = nx; s.y = ny;
          ctx.fillRect(s.ox + s.flip * nx * s.sc, h - ny * s.sc, 1.1, 1.1);
        }
      }
      if (++n < (REDUCED ? 1 : 90)) requestAnimationFrame(tick);
    };
    if (REDUCED) { for (let i = 0; i < 90; i++) tick(); } else tick();
  });
  io.observe(c);
})();
