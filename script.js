// Kutay Kılıç portfolyosu. Kütüphane yok; içerik JS olmadan da tam görünür.
(() => {
  const root = document.documentElement;
  const reduce = matchMedia('(prefers-reduced-motion: reduce)');

  // Yan panel (telefon ve tablet)
  const btn = document.querySelector('.side-btn');
  const side = document.getElementById('side');
  const scrim = document.querySelector('.scrim');
  const setOpen = (open) => {
    root.classList.toggle('side-open', open);
    btn.setAttribute('aria-expanded', String(open));
    scrim.hidden = !open;
    if (open) side.querySelector('a')?.focus();
  };
  btn.addEventListener('click', () => setOpen(!root.classList.contains('side-open')));
  scrim.addEventListener('click', () => setOpen(false));
  side.querySelectorAll('a').forEach((a) => a.addEventListener('click', () => setOpen(false)));
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && root.classList.contains('side-open')) { setOpen(false); btn.focus(); }
  });

  // Görünür alana giren öğeler bir kez belirir
  const io = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); } });
  }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' });
  document.querySelectorAll('.rv').forEach((el) => io.observe(el));

  // Bulunulan bölüm: yan panelde işaret, araç çubuğunda ad
  const links = [...side.querySelectorAll('a[data-sec]')];
  const here = document.querySelector('.here-t');
  const sbHere = document.querySelector('.sb-here');
  const names = JSON.parse(here.dataset.secNames);
  let cur = 'top';
  const mark = (id) => {
    if (id === cur) return;
    cur = id;
    links.forEach((a) => { if (a.dataset.sec === id) a.setAttribute('aria-current', 'true'); else a.removeAttribute('aria-current'); });
    if (sbHere) sbHere.textContent = names[id];
    if (reduce.matches) { here.textContent = names[id]; return; }
    here.classList.add('swap');
    setTimeout(() => { here.textContent = names[id]; here.classList.remove('swap'); }, 160);
  };
  links[0].setAttribute('aria-current', 'true');
  if (sbHere) sbHere.textContent = names.top;
  const spy = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) mark(e.target.id); });
  }, { rootMargin: '-40% 0px -55% 0px' });
  links.forEach((a) => { const s = document.getElementById(a.dataset.sec); if (s) spy.observe(s); });

  // Proje süzgeci: seçim hapı kayar, kartlar yumuşakça değişir
  const filter = document.querySelector('.filter');
  const pill = filter.querySelector('.pill');
  const chips = [...filter.querySelectorAll('.chip')];
  const items = [...document.querySelectorAll('#projects [data-g]')];
  const status = document.getElementById('f-status');
  const place = (chip) => {
    pill.style.width = chip.offsetWidth + 'px';
    pill.style.height = chip.offsetHeight + 'px';
    pill.style.transform = `translate(${chip.offsetLeft}px, ${chip.offsetTop}px)`;
  };
  const apply = (f) => {
    let n = 0;
    items.forEach((el) => { const show = f === 'all' || el.dataset.g === f; el.classList.toggle('out', !show); if (show) n++; });
    document.querySelectorAll('.rows').forEach((ul) => {
      let first = true;
      ul.querySelectorAll('.row').forEach((r) => { r.classList.toggle('first', first && !r.classList.contains('out')); if (!r.classList.contains('out')) first = false; });
    });
    const label = chips.find((c) => c.dataset.f === f).firstChild.textContent;
    status.textContent = `${label}: ${n}`;
  };
  chips.forEach((chip) => chip.addEventListener('click', () => {
    if (chip.getAttribute('aria-pressed') === 'true') return;
    chips.forEach((c) => c.setAttribute('aria-pressed', String(c === chip)));
    place(chip);
    const f = chip.dataset.f;
    if (reduce.matches) { apply(f); return; }
    const visible = items.filter((el) => !el.classList.contains('out'));
    visible.forEach((el) => el.classList.add('fading'));
    setTimeout(() => {
      apply(f);
      const now = items.filter((el) => !el.classList.contains('out'));
      now.forEach((el) => { el.classList.add('fading', 'in'); });
      requestAnimationFrame(() => requestAnimationFrame(() => now.forEach((el) => el.classList.remove('fading'))));
    }, 180);
  }));
  const start = () => place(chips.find((c) => c.getAttribute('aria-pressed') === 'true'));
  if (document.fonts?.ready) document.fonts.ready.then(start); else start();
  addEventListener('resize', start, { passive: true });
  filter.addEventListener('scroll', start, { passive: true });
})();
