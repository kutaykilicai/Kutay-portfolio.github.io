// Kutay Kılıç portfolyosu v3. Kütüphane yok; içerik JS olmadan da tam görünür.
(() => {
  const root = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = matchMedia('(hover: hover) and (pointer: fine)').matches;

  // Belirme: aynı listedeki kardeşler 100 ms arayla
  const rv = [...document.querySelectorAll('.rv')];
  rv.forEach((el) => {
    const sib = [...el.parentElement.children].filter((c) => c.classList.contains('rv'));
    el.style.setProperty('--i', Math.min(sib.indexOf(el) % 6, 5));
  });
  if (reduce || !('IntersectionObserver' in window)) rv.forEach((el) => el.classList.add('in'));
  else {
    const io = new IntersectionObserver((es) => es.forEach((e) => {
      if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
    }), { threshold: 0.1, rootMargin: '0px 0px -5% 0px' });
    rv.forEach((el) => io.observe(el));
  }

  // Klavyeyle odaklanan öğe henüz belirmediyse hemen göster
  document.addEventListener('focusin', (e) => { const r = e.target.closest('.rv'); if (r) r.classList.add('in'); });

  // İş kartları: imleci izleyen ark ışığı, kart üstten çıkarken hafif küçülüp solma
  if (!reduce) {
    const arts = [...document.querySelectorAll('.wk article')];
    if (fine) document.querySelectorAll('.wk-stage').forEach((st) => {
      const gl = st.querySelector('.glow');
      st.addEventListener('mouseenter', () => st.style.setProperty('--sh', st.clientHeight + 'px'));
      st.addEventListener('mousemove', (e) => {
        const r = st.getBoundingClientRect();
        gl.style.transform = `translate3d(${e.clientX - r.left}px, ${e.clientY - r.top}px, 0)`;
      });
    });
    let tick = false;
    const shrink = () => {
      tick = false;
      const top = innerHeight * 0.12;
      arts.forEach((a) => {
        const r = a.parentElement.getBoundingClientRect();
        const p = Math.min(Math.max((top - r.top) / Math.max(r.height, 1), 0), 1);
        a.style.transform = p ? `scale(${1 - 0.07 * p})` : '';
        a.style.opacity = p ? String(1 - 0.35 * p) : '';
      });
    };
    addEventListener('scroll', () => { if (!tick) { tick = true; requestAnimationFrame(shrink); } }, { passive: true });
  }

  // E-posta bağlantısı önce sorar: araçlarımdaki onay adımının küçük bir örneği. Adresi kopyalama seçeneği de var.
  const ask = document.querySelector('.ask');
  let askFrom = null;
  const closeAsk = () => { if (ask.hidden) return; ask.classList.remove('on'); ask.hidden = true; if (askFrom) askFrom.focus(); askFrom = null; };
  document.querySelectorAll('a[data-ask]').forEach((a) => a.addEventListener('click', (e) => {
    e.preventDefault(); askFrom = a;
    ask.hidden = false;
    const r = a.getBoundingClientRect();
    const x = Math.min(r.left, innerWidth - ask.offsetWidth - 16);
    const y = r.bottom + 10 + ask.offsetHeight > innerHeight ? r.top - ask.offsetHeight - 10 : r.bottom + 10;
    ask.style.left = Math.max(16, x) + 'px'; ask.style.top = Math.max(16, y) + 'px';
    void ask.offsetWidth; ask.classList.add('on');
    ask.querySelector('.ask-open').focus();
  }));
  ask.querySelector('.ask-x').addEventListener('click', closeAsk);
  ask.querySelector('.ask-open').addEventListener('click', () => setTimeout(closeAsk, 50));
  const cp = ask.querySelector('.ask-copy');
  cp.addEventListener('click', async () => {
    try { await navigator.clipboard.writeText(ask.querySelector('.ask-a').textContent); cp.lastChild.previousSibling.textContent = cp.dataset.done; } catch (err) { /* pano yoksa adres zaten görünür */ }
  });
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeAsk(); });
  document.addEventListener('pointerdown', (e) => { if (!ask.hidden && !ask.contains(e.target) && !e.target.closest('a[data-ask]')) closeAsk(); });

  // Menü: kaydırınca zemin, bulunulan bölüm işareti
  const onScroll = () => root.classList.toggle('scrolled', scrollY > 40);
  addEventListener('scroll', onScroll, { passive: true }); onScroll();
  const map = { work: 'work', lab: 'lab', all: 'lab', about: 'about', tools: 'about', jury: 'about', contact: 'contact' };
  const links = [...document.querySelectorAll('.nl[data-sec]')];
  const spy = new IntersectionObserver((es) => es.forEach((e) => {
    if (!e.isIntersecting) return;
    const k = map[e.target.id];
    links.forEach((a) => a.toggleAttribute('aria-current', false));
    const a = links.find((l) => l.dataset.sec === k);
    if (a) a.setAttribute('aria-current', 'true');
  }), { rootMargin: '-45% 0px -50% 0px' });
  ['top', ...Object.keys(map)].forEach((id) => { const s = document.getElementById(id); if (s) spy.observe(s); });

  // Jüri alıntıları: soldurarak geçiş, sayaç
  const qbox = document.querySelector('.qbox');
  if (qbox) {
    const qs = [...qbox.querySelectorAll('.q')];
    const now = qbox.querySelector('.q-now');
    let k = 0, tm = 0;
    qs.forEach((q, j) => { if (j) q.hidden = true; });
    const go = (d) => {
      const old = qs[k];
      qs.forEach((q) => { if (q !== old) q.hidden = true; });
      clearTimeout(tm);
      old.classList.remove('on');
      k = (k + d + qs.length) % qs.length;
      const nw = qs[k];
      nw.hidden = false; void nw.offsetWidth; nw.classList.add('on');
      now.textContent = String(k + 1).padStart(3, '0');
      tm = setTimeout(() => { if (old !== nw) old.hidden = true; }, reduce ? 0 : 460);
    };
    qbox.querySelectorAll('.q-btn').forEach((b) => b.addEventListener('click', () => go(+b.dataset.d)));
    qbox.addEventListener('keydown', (e) => {
      if (e.key === 'ArrowRight') go(1);
      if (e.key === 'ArrowLeft') go(-1);
    });
  }

  // Tablo satırında imleci izleyen önizleme (yalnızca masaüstü)
  const peek = document.querySelector('.peek');
  if (peek && fine && !reduce) {
    const [pc, pn, ps] = peek.children;
    let x = 0, y = 0, tx = 0, ty = 0, raf = 0, on = false;
    const step = () => {
      x += (tx - x) * 0.18; y += (ty - y) * 0.18;
      peek.style.transform = `translate3d(${x}px, ${y}px, 0)`;
      raf = on || Math.abs(tx - x) > 0.5 ? requestAnimationFrame(step) : 0;
    };
    document.querySelectorAll('.pt tbody tr').forEach((tr) => {
      tr.addEventListener('mouseenter', (e) => {
        pc.textContent = tr.dataset.c; pn.textContent = tr.dataset.n; ps.textContent = tr.dataset.s;
        tx = e.clientX + 24; ty = e.clientY + 18;
        if (!on) { x = tx; y = ty; }
        on = true; peek.classList.add('on');
        if (!raf) raf = requestAnimationFrame(step);
      });
      tr.addEventListener('mousemove', (e) => {
        tx = Math.min(e.clientX + 24, innerWidth - 240); ty = Math.min(e.clientY + 18, innerHeight - 140);
      });
    });
    document.querySelector('.pt tbody').addEventListener('mouseleave', () => { on = false; peek.classList.remove('on'); });
  }

  // Girişte yavaş akan ipek: kendi küçük fragment shader'ım. Azaltılmış harekette ya da WebGL yoksa CSS degradesi kalır.
  const cv = document.querySelector('.silk');
  if (!cv || reduce) return;
  const gl = cv.getContext('webgl', { antialias: false, alpha: false, powerPreference: 'low-power' });
  if (!gl) return;
  const vs = 'attribute vec2 a;void main(){gl_Position=vec4(a,0.,1.);}';
  const fs = `precision mediump float;uniform vec2 R;uniform float T;
void main(){vec2 uv=gl_FragCoord.xy/R;vec2 p=(gl_FragCoord.xy-.5*R)/R.y;float t=T*.06;vec2 q=p*1.15;
for(int i=1;i<5;i++){float f=float(i);q.x+=.42/f*sin(f*1.4*q.y+t*.9+f*.7);q.y+=.30/f*cos(f*1.1*q.x-t*.7+f*1.9);}
float ph=q.x*2.6-q.y*1.9+t*.45;float s=sin(ph);float body=.5+.5*s;float edge=pow(1.-abs(s),14.);
float ph2=q.x*1.2+q.y*2.4-t*.35;float m=.55+.45*sin(ph2);
vec3 deep=vec3(.035,.039,.047),navy=vec3(.07,.145,.25),graph=vec3(.085,.09,.10);
vec3 c=mix(deep,navy,body*body*m);c=mix(c,graph,.35*(1.-body)*smoothstep(.1,.9,uv.y));
c+=vec3(.36,.78,.98)*edge*m*.36;c+=vec3(.16,.48,.85)*exp(-2.6*length(p-vec2(.62,.30)))*.16;
c*=mix(.62,1.,smoothstep(0.,.85,uv.x));c=mix(c,deep,smoothstep(.32,0.,uv.y));
gl_FragColor=vec4(c,1.);}`;
  const sh = (type, src) => { const s = gl.createShader(type); gl.shaderSource(s, src); gl.compileShader(s); return gl.getShaderParameter(s, gl.COMPILE_STATUS) ? s : null; };
  const v = sh(gl.VERTEX_SHADER, vs), f = sh(gl.FRAGMENT_SHADER, fs);
  if (!v || !f) return;
  const pr = gl.createProgram(); gl.attachShader(pr, v); gl.attachShader(pr, f); gl.linkProgram(pr);
  if (!gl.getProgramParameter(pr, gl.LINK_STATUS)) return;
  gl.useProgram(pr);
  gl.bindBuffer(gl.ARRAY_BUFFER, gl.createBuffer());
  gl.bufferData(gl.ARRAY_BUFFER, new Float32Array([-1, -1, 3, -1, -1, 3]), gl.STATIC_DRAW);
  const loc = gl.getAttribLocation(pr, 'a'); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, 2, gl.FLOAT, false, 0, 0);
  const uR = gl.getUniformLocation(pr, 'R'), uT = gl.getUniformLocation(pr, 'T');
  const size = () => {
    const s = Math.min(devicePixelRatio || 1, 1.5) * 0.5;
    cv.width = Math.max(2, Math.round(cv.clientWidth * s)); cv.height = Math.max(2, Math.round(cv.clientHeight * s));
    gl.viewport(0, 0, cv.width, cv.height); gl.uniform2f(uR, cv.width, cv.height);
  };
  size(); addEventListener('resize', size, { passive: true });
  let vis = true, id = 0;
  const t0 = performance.now() - 20000;
  const draw = (now) => { gl.uniform1f(uT, (now - t0) / 1000); gl.drawArrays(gl.TRIANGLES, 0, 3); id = vis && !document.hidden ? requestAnimationFrame(draw) : 0; };
  const start = () => { if (!id && vis && !document.hidden) id = requestAnimationFrame(draw); };
  new IntersectionObserver((es) => { vis = es[0].isIntersecting; start(); }).observe(cv);
  document.addEventListener('visibilitychange', start);
  requestAnimationFrame((n) => { draw(n); cv.classList.add('on'); });
})();
