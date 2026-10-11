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
