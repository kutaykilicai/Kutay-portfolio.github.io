// Kutay Kılıç portfolyosu. Kütüphane yok; içerik JS olmadan da tam görünür.
(() => {
  const bar = document.querySelector('.bar');
  const btn = document.querySelector('.menu-btn');
  const links = [...document.querySelectorAll('.nav-list a')];

  // Telefon menüsü
  const setOpen = (open) => { bar.classList.toggle('open', open); btn.setAttribute('aria-expanded', String(open)); };
  btn.addEventListener('click', () => setOpen(!bar.classList.contains('open')));
  links.forEach((a) => a.addEventListener('click', () => setOpen(false)));
  document.addEventListener('keydown', (e) => { if (e.key === 'Escape' && bar.classList.contains('open')) { setOpen(false); btn.focus(); } });

  // İşaretler (vurgu ve tik) görünür alana girince bir kez çizilir
  const draw = new IntersectionObserver((entries) => {
    entries.forEach((e) => { if (e.isIntersecting) { e.target.classList.add('is-drawn'); draw.unobserve(e.target); } });
  }, { threshold: 0.35 });
  document.querySelectorAll('.bar, .hero, .legend, .proj').forEach((el) => draw.observe(el));

  // Menüde bulunulan bölümü işaretle
  const byId = new Map(links.map((a) => [a.hash.slice(1), a]));
  const spy = new IntersectionObserver((entries) => {
    entries.forEach((e) => {
      if (!e.isIntersecting) return;
      links.forEach((a) => a.removeAttribute('aria-current'));
      byId.get(e.target.id)?.setAttribute('aria-current', 'true');
    });
  }, { rootMargin: '-45% 0px -50% 0px' });
  byId.forEach((_, id) => { const s = document.getElementById(id); if (s) spy.observe(s); });
})();
