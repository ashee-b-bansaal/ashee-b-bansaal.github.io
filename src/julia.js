// The hero background: a live Julia set.

// Hero: a Julia set rendered on the GPU. The cursor steers c, so moving
// the mouse anywhere reshapes the fractal; when idle, c drifts on its own.
// The set's edge is drawn from a distance estimate, so it stays a crisp hairline
// at any resolution; around it sit a soft colour glow and faint contour lines.
// Light mode reads like an etching on paper, dark mode like light on black.
(() => {
  const canvas = document.getElementById('julia');
  const hero = document.getElementById('hero');
  const out = document.getElementById('cval');
  const gl = canvas?.getContext('webgl', { antialias: false, premultipliedAlpha: false });
  if (!gl) { document.body.classList.add('no-webgl'); return; }
  const derivs = !!gl.getExtension('OES_standard_derivatives');

  const vs = 'attribute vec2 p; void main(){ gl_Position = vec4(p, 0., 1.); }';
  const fs = `${derivs ? '#extension GL_OES_standard_derivatives : enable\n#define DERIVS' : ''}
    precision highp float;
    uniform vec2 res; uniform vec2 c; uniform float zoom; uniform float dark;
    const int ITER = 160;

    // pastel stops: mint → sky → lavender → rose → peach
    vec3 pal(float t){
      vec3 a = vec3(.56,.86,.76), b = vec3(.56,.74,.94), d = vec3(.74,.64,.95), e = vec3(.95,.62,.74), f = vec3(.99,.74,.58);
      t = fract(t) * 4.0;
      if (t < 1.) return mix(a, b, t);
      if (t < 2.) return mix(b, d, t - 1.);
      if (t < 3.) return mix(d, e, t - 2.);
      return mix(e, f, t - 3.);
    }
    float hash(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }

    void main(){
      float unit = min(res.x, res.y);
      vec2 uv = (gl_FragCoord.xy - .5 * res) / unit * zoom;
      float px = zoom / unit;                       // one pixel, in fractal units
      vec2 z = uv, dz = vec2(1., 0.);
      float n = 0.;
      for (int i = 0; i < ITER; i++) {
        dz = 2. * vec2(z.x * dz.x - z.y * dz.y, z.x * dz.y + z.y * dz.x);
        z = vec2(z.x * z.x - z.y * z.y, 2. * z.x * z.y) + c;
        if (dot(z, z) > 1024.) break;
        n += 1.;
      }
      bool inside = n >= float(ITER) - 1.;
      float r = length(z);
      float de = inside ? 0. : .5 * r * log(r) / max(length(dz), 1e-6);
      float sn = inside ? float(ITER) : n - log2(log2(dot(z, z))) + 4.;

      // paper, or night
      vec2 q = gl_FragCoord.xy / res;
      vec3 bg = mix(mix(vec3(.976, .972, .962), vec3(.952, .950, .968), q.y),
                    mix(vec3(.030, .030, .042), vec3(.052, .044, .078), q.y), dark);

      float edge = inside ? 1. : exp(-de / (px * 1.1));     // the hairline
      float glow = inside ? 1. : exp(-de / (px * 70.));     // wide soft halo
      vec3 hue = pal(sqrt(sn / float(ITER)) * 1.8 + q.x * .35 + .1);

      // keep the middle calm behind the name; the set blooms toward the edges
      vec2 m = (q - .5) * vec2(res.x / unit, 1.) * vec2(1.25, 2.1);
      float focus = mix(.22, 1., smoothstep(.18, .75, length(m)));
      edge *= focus; glow *= mix(.55, 1., focus);

      // contour lines on the escape-time field, faded where they'd crowd
      float x = sn * .35, line = 0.;
      #ifdef DERIVS
        float w = fwidth(x);
        float f = fract(x), dl = min(f, 1. - f);
        line = (1. - smoothstep(0., w * 1.2, dl)) * smoothstep(.45, .08, w);
      #endif
      line *= inside ? 0. : 1.;

      vec3 col = bg;
      // light: watercolour halo, graphite contours, ink filament
      vec3 ink = mix(vec3(.10, .09, .18), hue * .42, .45);
      vec3 lightCol = mix(bg, hue, glow * .42);
      lightCol = mix(lightCol, ink, line * .07);
      lightCol = mix(lightCol, inside ? mix(bg, vec3(.80, .74, .93), .30 * focus) : ink, inside ? 1. : edge * .9);
      // dark: glowing halo, faint silver contours, luminous filament
      vec3 darkCol = bg + hue * glow * .30;
      darkCol += vec3(.75, .78, .9) * line * .05;
      darkCol = inside ? mix(bg, vec3(.20, .15, .32), .55 * focus) : mix(darkCol, mix(hue, vec3(1.), .35), edge * .95);
      col = mix(lightCol, darkCol, dark);

      // vignette (mostly in dark) and a little grain so gradients don't band
      float v = dot(q - .5, q - .5);
      col *= 1. - v * mix(.12, .9, dark);
      col += (hash(gl_FragCoord.xy) - .5) * mix(.018, .028, dark);
      gl_FragColor = vec4(col, 1.);
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
  const uRes = gl.getUniformLocation(prog, 'res'), uC = gl.getUniformLocation(prog, 'c'), uZoom = gl.getUniformLocation(prog, 'zoom'), uDark = gl.getUniformLocation(prog, 'dark');

  // render near device resolution so the hairlines stay sharp
  const SCALE = Math.min(devicePixelRatio || 1, 1.5);
  function resize() {
    canvas.width = Math.round(canvas.clientWidth * SCALE);
    canvas.height = Math.round(canvas.clientHeight * SCALE);
    gl.viewport(0, 0, canvas.width, canvas.height);
    gl.uniform2f(uRes, canvas.width, canvas.height);
    gl.uniform1f(uZoom, canvas.clientWidth < 500 ? 3.4 : 2.6);
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

  // the theme switch fades between palettes instead of snapping
  const isDark = () => (document.documentElement.dataset.theme === 'dark' ? 1 : 0);
  let dark = isDark();

  function frame() {
    if (visible && !document.hidden) {
      idle++;
      if (idle > 120 && !REDUCED) targetA += 0.0016;
      angle += (targetA - angle) * 0.04;
      radius += (targetR - radius) * 0.04;
      dark = REDUCED ? isDark() : dark + (isDark() - dark) * 0.08;
      const cx = radius * Math.cos(angle), cy = radius * Math.sin(angle);
      gl.uniform2f(uC, cx, cy);
      gl.uniform1f(uDark, dark);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      if (out) out.textContent = `c = ${cx.toFixed(3)} ${cy < 0 ? '−' : '+'} ${Math.abs(cy).toFixed(3)}i`;
    }
    if (!REDUCED) requestAnimationFrame(frame);
  }
  resize();
  addEventListener('resize', resize);
  frame();
  if (REDUCED) {
    hero.addEventListener('pointermove', () => requestAnimationFrame(frame));
    addEventListener('themechange', () => requestAnimationFrame(frame));
  }
})();
