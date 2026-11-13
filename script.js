// Kutay Kılıç portfolio. Plain JS, no libraries.
(() => {
  const reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  const fine = window.matchMedia('(pointer: fine)').matches;
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];

  // ===== Preloader + hero entrance =====
  const preloader = $('#preloader');
  const start = () => {
    preloader && preloader.classList.add('hide');
    document.body.classList.add('loaded');
  };
  if (reduce) start();
  else if (document.readyState === 'complete') setTimeout(start, 500);
  else window.addEventListener('load', () => setTimeout(start, 500));
  setTimeout(start, 3000); // never block the page

  // ===== Navbar, active link, dock =====
  const navbar = $('#navbar');
  const dock = $('.floating-dock');
  const navToggle = $('#navToggle');
  const navLinks = $('.nav-links');
  navToggle.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    navToggle.classList.toggle('active', open);
    navToggle.setAttribute('aria-expanded', open);
  });
  $$('.nav-link').forEach(l => l.addEventListener('click', () => {
    navLinks.classList.remove('open');
    navToggle.classList.remove('active');
    navToggle.setAttribute('aria-expanded', 'false');
  }));
  const links = new Map($$('.nav-link').map(l => [l.getAttribute('href').slice(1), l]));
  const sectionObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting && links.has(e.target.id)) {
        links.forEach(l => l.classList.remove('active'));
        links.get(e.target.id).classList.add('active');
      }
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  $$('section[id]').forEach(s => sectionObs.observe(s));

  // ===== Scroll-driven bits (one rAF) =====
  const tl = $('.timeline');
  const tlFill = $('.tl-line i');
  const tlItems = $$('.tl-item');
  const blobs = $$('.aurora-blob');
  let ticking = false;
  const onScroll = () => {
    const y = window.scrollY;
    navbar.classList.toggle('scrolled', y > 40);
    dock && dock.classList.toggle('show', y > window.innerHeight * 0.8);
    if (tl && tlFill) {
      const r = tl.getBoundingClientRect();
      const mid = window.innerHeight * 0.6;
      const p = Math.min(1, Math.max(0, (mid - r.top) / r.height));
      tlFill.parentElement.style.setProperty('--p', p.toFixed(3));
      tlItems.forEach(it => {
        const t = it.getBoundingClientRect().top;
        it.classList.toggle('lit', t < mid);
      });
    }
    if (!reduce) blobs.forEach((b, i) => { b.style.translate = `0 ${(y * (i + 1) * 0.04).toFixed(1)}px`; });
    ticking = false;
  };
  window.addEventListener('scroll', () => { if (!ticking) { ticking = true; requestAnimationFrame(onScroll); } }, { passive: true });
  onScroll();

  // ===== Reveal on scroll =====
  const revealObs = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) { e.target.classList.add('in'); revealObs.unobserve(e.target); }
    });
  }, { threshold: 0.12, rootMargin: '0px 0px -40px 0px' });
  $$('[data-reveal]').forEach(el => reduce ? el.classList.add('in') : revealObs.observe(el));

  // ===== Counters =====
  const count = el => {
    const target = +el.dataset.count;
    if (reduce) { el.textContent = target; return; }
    const t0 = performance.now(), dur = 1400;
    const step = now => {
      const k = Math.min(1, (now - t0) / dur);
      el.textContent = Math.round(target * (1 - Math.pow(1 - k, 3)));
      if (k < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  };
  const countObs = new IntersectionObserver(entries => {
    entries.forEach(e => { if (e.isIntersecting) { count(e.target); countObs.unobserve(e.target); } });
  }, { threshold: 0.6 });
  $$('[data-count]').forEach(el => countObs.observe(el));

  // ===== Project diagrams animate only while visible =====
  const liveObs = new IntersectionObserver(entries => {
    entries.forEach(e => e.target.classList.toggle('live', e.isIntersecting && !reduce));
  }, { threshold: 0.2 });
  $$('.project-visual').forEach(v => liveObs.observe(v));

  // ===== Card spotlight (pointer only) =====
  if (fine) {
    $$('.spot').forEach(c => c.addEventListener('pointermove', e => {
      const r = c.getBoundingClientRect();
      c.style.setProperty('--mx', `${e.clientX - r.left}px`);
      c.style.setProperty('--my', `${e.clientY - r.top}px`);
    }));
    const pc = $('.profile-card');
    const hero = $('.hero');
    if (pc && !reduce) {
      hero.addEventListener('pointermove', e => {
        const x = e.clientX / window.innerWidth - 0.5, y = e.clientY / window.innerHeight - 0.5;
        pc.style.setProperty('--ry', `${x * 8}deg`);
        pc.style.setProperty('--rx', `${y * -8}deg`);
      });
      hero.addEventListener('pointerleave', () => { pc.style.setProperty('--ry', '0deg'); pc.style.setProperty('--rx', '0deg'); });
    }
  }

  // ===== Hero canvas: agent network with pulses =====
  const cv = $('#net');
  if (cv && cv.getContext) {
    const ctx = cv.getContext('2d');
    let W = 0, H = 0, dpr = 1, nodes = [], pulses = [], running = false, raf = 0;
    const mouse = { x: -9999, y: -9999 };
    const LINK = 150;
    const resize = () => {
      dpr = Math.min(window.devicePixelRatio || 1, 2);
      W = cv.clientWidth; H = cv.clientHeight;
      cv.width = W * dpr; cv.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      const n = Math.max(28, Math.min(90, Math.round(W * H / 15000)));
      nodes = Array.from({ length: n }, (_, i) => ({
        x: Math.random() * W, y: Math.random() * H,
        vx: (Math.random() - 0.5) * 0.25, vy: (Math.random() - 0.5) * 0.25,
        r: i % 9 === 0 ? 3.2 : 1.6 + Math.random() * 1.2,
        hub: i % 9 === 0,
        z: 0.4 + Math.random() * 0.6
      }));
      pulses = [];
    };
    const draw = (move) => {
      ctx.clearRect(0, 0, W, H);
      const px = (mouse.x - W / 2) * 0.015, py = (mouse.y - H / 2) * 0.015;
      for (const n of nodes) {
        if (move) {
          n.x += n.vx; n.y += n.vy;
          if (n.x < -20) n.x = W + 20; if (n.x > W + 20) n.x = -20;
          if (n.y < -20) n.y = H + 20; if (n.y > H + 20) n.y = -20;
        }
        n.dx = n.x + (mouse.x > -999 ? px * n.z : 0);
        n.dy = n.y + (mouse.x > -999 ? py * n.z : 0);
      }
      ctx.lineWidth = 1;
      for (let i = 0; i < nodes.length; i++) {
        const a = nodes[i];
        for (let j = i + 1; j < nodes.length; j++) {
          const b = nodes[j];
          const dx = a.dx - b.dx, dy = a.dy - b.dy, d2 = dx * dx + dy * dy;
          if (d2 < LINK * LINK) {
            const o = (1 - Math.sqrt(d2) / LINK) * 0.28;
            ctx.strokeStyle = `rgba(120,170,230,${o})`;
            ctx.beginPath(); ctx.moveTo(a.dx, a.dy); ctx.lineTo(b.dx, b.dy); ctx.stroke();
            if (move && (a.hub || b.hub) && Math.random() < 0.0035 && pulses.length < 14) pulses.push({ a, b, t: 0 });
          }
        }
      }
      for (const n of nodes) {
        const md = Math.hypot(n.dx - mouse.x, n.dy - mouse.y);
        const glow = md < 160 ? 1 - md / 160 : 0;
        ctx.fillStyle = n.hub ? `rgba(45,212,239,${0.75 + glow * 0.25})` : `rgba(160,180,215,${0.45 + glow * 0.5})`;
        ctx.beginPath(); ctx.arc(n.dx, n.dy, n.r + glow * 1.5, 0, 6.283); ctx.fill();
        if (n.hub) {
          ctx.strokeStyle = 'rgba(45,212,239,.25)';
          ctx.beginPath(); ctx.arc(n.dx, n.dy, n.r + 5, 0, 6.283); ctx.stroke();
        }
      }
      for (let k = pulses.length - 1; k >= 0; k--) {
        const p = pulses[k];
        if (move) p.t += 0.018;
        if (p.t >= 1) { pulses.splice(k, 1); continue; }
        const x = p.a.dx + (p.b.dx - p.a.dx) * p.t, y = p.a.dy + (p.b.dy - p.a.dy) * p.t;
        const g = ctx.createRadialGradient(x, y, 0, x, y, 9);
        g.addColorStop(0, 'rgba(160,140,255,.95)'); g.addColorStop(1, 'rgba(139,124,246,0)');
        ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, 9, 0, 6.283); ctx.fill();
      }
    };
    const loop = () => { draw(true); raf = requestAnimationFrame(loop); };
    const play = () => { if (!running && !reduce) { running = true; raf = requestAnimationFrame(loop); } };
    const stop = () => { running = false; cancelAnimationFrame(raf); };
    resize(); draw(false);
    let rt;
    window.addEventListener('resize', () => { clearTimeout(rt); rt = setTimeout(() => { resize(); draw(false); }, 150); });
    if (fine) {
      $('.hero').addEventListener('pointermove', e => { const r = cv.getBoundingClientRect(); mouse.x = e.clientX - r.left; mouse.y = e.clientY - r.top; });
      $('.hero').addEventListener('pointerleave', () => { mouse.x = mouse.y = -9999; });
    }
    new IntersectionObserver(([e]) => e.isIntersecting ? play() : stop()).observe(cv);
    document.addEventListener('visibilitychange', () => document.hidden ? stop() : play());
  }
})();
