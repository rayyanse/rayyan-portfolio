/* Inner pages: menu, films and motion. Everything here is progressive
   enhancement: the HTML is complete on its own, `js-motion` start states are
   only set when motion is allowed (in <head>) and are cleared if GSAP never
   loads. Timings follow the human-web-design motion kit (expo/out curves,
   0.08 stagger, 8px blur reveals, lerped parallax). */
(function () {
  var d = document.documentElement;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = matchMedia('(pointer: fine)').matches;
  var desktop = matchMedia('(min-width: 1001px)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- mobile menu ---------- */
  var mb = $('.menu-btn'), mm = $('#mmenu');
  if (mb && mm) {
    var setMenu = function (open) {
      mm.classList.toggle('open', open);
      document.body.classList.toggle('menu-open', open);
      mb.setAttribute('aria-expanded', open ? 'true' : 'false');
      mb.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
    };
    mb.addEventListener('click', function () { setMenu(!mm.classList.contains('open')); });
    mm.addEventListener('click', function (ev) { if (ev.target.closest('a')) setMenu(false); });
    addEventListener('keydown', function (ev) { if (ev.key === 'Escape' && mm.classList.contains('open')) { setMenu(false); mb.focus(); } });
  }

  /* ---------- topbar: stuck, hides on scroll down, returns on scroll up; progress ---------- */
  var bar = $('#topbar'), prog = $('#scrollbar'), pct = $('#framePct'), lastY = 0;
  function onScroll() {
    var y = scrollY, h = document.documentElement.scrollHeight - innerHeight, p = h > 0 ? y / h : 0;
    if (bar) {
      bar.classList.toggle('stuck', y > 12);
      bar.classList.toggle('hide', y > 260 && y > lastY && !document.body.classList.contains('menu-open'));
    }
    if (prog) prog.style.width = p * 100 + '%';
    if (pct) pct.textContent = String(Math.round(p * 100)).padStart(2, '0') + '%';
    lastY = y;
  }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* ---------- hero background film: desktop only, after load, so the poster stays the LCP ---------- */
  function startHeroFilm() {
    $$('.xhero-bg video[data-src], .phone video[data-src]').forEach(function (v) {
      v.src = v.getAttribute('data-src'); v.muted = true;
      v.addEventListener('playing', function () { v.classList.add('on'); }, { once: true });
      v.play().catch(function () {});
    });
  }
  if (desktop && !reduce) {
    if (document.readyState === 'complete') setTimeout(startHeroFilm, 300);
    else addEventListener('load', function () { setTimeout(startHeroFilm, 300); });
  }

  /* ---------- section film: plays while visible ---------- */
  $$('.how-film video').forEach(function (v) {
    v.muted = true;
    if (reduce || !('IntersectionObserver' in window)) return;
    new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (e.isIntersecting) { if (!v.src) v.src = v.getAttribute('data-src'); v.play().catch(function () {}); } else v.pause();
      });
    }, { threshold: 0.2 }).observe(v);
  });

  /* ---------- watch with sound: native <dialog> ---------- */
  var dlg = $('#filmModal');
  if (dlg) {
    var mv = $('video', dlg);
    $$('[data-watch]').forEach(function (b) {
      b.addEventListener('click', function () {
        mv.src = b.getAttribute('data-watch'); mv.poster = b.getAttribute('data-poster') || '';
        dlg.classList.toggle('tall', b.hasAttribute('data-tall'));
        if (dlg.showModal) dlg.showModal(); else dlg.setAttribute('open', '');
        mv.muted = false; mv.play().catch(function () {});
      });
    });
    var closeDlg = function () { mv.pause(); mv.removeAttribute('src'); mv.load(); if (dlg.close) dlg.close(); else dlg.removeAttribute('open'); };
    $('.x', dlg).addEventListener('click', closeDlg);
    dlg.addEventListener('click', function (e) { if (e.target === dlg) closeDlg(); });
    dlg.addEventListener('cancel', function () { mv.pause(); });
  }

  /* ---------- steps: the one in view lights up, meter tracks progress ---------- */
  var steps = $$('.step'), meter = $('.meter b'), meterTxt = $('.meter span');
  var stepIO;
  if (steps.length && 'IntersectionObserver' in window) {
    stepIO = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        if (!e.isIntersecting) return;
        var i = steps.indexOf(e.target);
        steps.forEach(function (s, j) { s.classList.toggle('on', j === i); });
        if (meter) meter.style.width = ((i + 1) / steps.length) * 100 + '%';
        if (meterTxt) meterTxt.textContent = String(i + 1).padStart(2, '0') + ' / ' + String(steps.length).padStart(2, '0');
      });
    }, { rootMargin: '-45% 0px -45% 0px' });
    steps.forEach(function (s) { stepIO.observe(s); });
  }

  /* ---------- custom cursor: lerped ring that grows on interactive things ---------- */
  if (fine && !reduce) {
    var cur = document.createElement('div'); cur.className = 'cursor'; cur.setAttribute('aria-hidden', 'true'); document.body.appendChild(cur);
    var cx = innerWidth / 2, cy = innerHeight / 2, tx = cx, ty = cy;
    addEventListener('mousemove', function (e) { tx = e.clientX; ty = e.clientY; cur.classList.add('on'); }, { passive: true });
    document.addEventListener('mouseleave', function () { cur.classList.remove('on'); });
    document.addEventListener('mouseover', function (e) { cur.classList.toggle('big', !!e.target.closest('a,button,summary,.pcard,.next')); });
    (function loop() { cx += (tx - cx) * 0.18; cy += (ty - cy) * 0.18; cur.style.transform = 'translate3d(' + cx + 'px,' + cy + 'px,0)'; requestAnimationFrame(loop); })();
  }

  /* ---------- counters ---------- */
  function countUp(el) {
    var to = parseFloat(el.getAttribute('data-count')), suf = el.getAttribute('data-suffix') || '';
    if (isNaN(to)) return;
    if (reduce || !window.gsap) { el.textContent = to + suf; return; }
    var o = { v: 0 };
    gsap.to(o, { v: to, duration: 1.6, ease: 'power3.out', onUpdate: function () { el.textContent = Math.round(o.v) + suf; } });
  }

  if (!d.classList.contains('js-motion') || !window.gsap) {
    d.classList.remove('js-motion');
    $$('[data-count]').forEach(countUp);
    return;
  }
  window.__motionOK = true;
  gsap.registerPlugin(ScrollTrigger);

  /* ---------- inertial scroll, synced to ScrollTrigger ---------- */
  var lenis = null;
  if (window.Lenis && desktop) {
    lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
    $$('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) { var t = $(a.getAttribute('href')); if (t) { e.preventDefault(); lenis.scrollTo(t, { offset: -70 }); } });
    });
  }

  /* ---------- hero entrance: lines rise from a mask, copy follows, glass settles in ---------- */
  var tl = gsap.timeline({ defaults: { ease: 'expo.out' } });
  tl.to('.xhero h1 .ln>span', { y: 0, duration: 1.15, stagger: 0.09 }, 0.05)
    .to('.xhero [data-hi]', { opacity: 1, y: 0, duration: 0.9, stagger: 0.06 }, 0.3)
    .fromTo('.glass', { opacity: 0, y: 30, scale: 0.96 }, { opacity: 1, y: 0, scale: 1, duration: 1.2, stagger: 0.12 }, 0.5)
    .fromTo('.phone', { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 1.3 }, 0.35)
    .fromTo('.xhero-bg', { scale: 1.08 }, { scale: 1, duration: 2.4, ease: 'power2.out' }, 0);

  /* ---------- mouse parallax on three depth layers: background, glass, phone ---------- */
  if (fine && desktop) {
    var layers = $$('[data-depth]').map(function (el) {
      return { el: el, d: parseFloat(el.getAttribute('data-depth')), x: gsap.quickTo(el, 'x', { duration: 1.2, ease: 'power3.out' }), y: gsap.quickTo(el, 'y', { duration: 1.2, ease: 'power3.out' }) };
    });
    var hero = $('.xhero');
    if (hero) hero.addEventListener('mousemove', function (e) {
      var nx = e.clientX / innerWidth - 0.5, ny = e.clientY / innerHeight - 0.5;
      layers.forEach(function (l) { l.x(nx * l.d * 60); l.y(ny * l.d * 40); });
    });
  }

  /* ---------- hero copy drifts up and fades as you leave it ---------- */
  gsap.to('.xhero-in', { yPercent: -12, opacity: 0.2, ease: 'none', scrollTrigger: { trigger: '.xhero', start: 'top top', end: 'bottom top', scrub: true } });

  /* ---------- scroll reveals ---------- */
  ScrollTrigger.batch('[data-rv]', {
    start: 'top 88%', once: true,
    onEnter: function (els) { gsap.to(els, { opacity: 1, y: 0, filter: 'blur(0px)', duration: 0.95, ease: 'power3.out', stagger: 0.08 }); }
  });

  /* ---------- big statement on paper: words light up as you scroll ---------- */
  $$('.quote').forEach(function (q) {
    gsap.fromTo(q, { opacity: 0.25 }, { opacity: 1, ease: 'none', scrollTrigger: { trigger: q, start: 'top 85%', end: 'top 40%', scrub: true } });
  });

  /* ---------- counters start when visible ---------- */
  $$('[data-count]').forEach(function (el) { ScrollTrigger.create({ trigger: el, start: 'top 90%', once: true, onEnter: function () { countUp(el); } }); });

  /* ---------- proof track: pinned horizontal scroll on desktop ---------- */
  var track = $('.track');
  if (track && desktop) {
    var dist = function () { return Math.max(0, track.scrollWidth - innerWidth); };
    if (dist() > 40) gsap.to(track, { x: function () { return -dist(); }, ease: 'none', scrollTrigger: { trigger: '.track-wrap', start: 'center center', end: function () { return '+=' + dist(); }, pin: '.proof', scrub: 0.8, invalidateOnRefresh: true } });
  }

  /* ---------- next-case image eases in as it arrives ---------- */
  $$('.next img').forEach(function (img) {
    gsap.fromTo(img, { yPercent: -8 }, { yPercent: 8, ease: 'none', scrollTrigger: { trigger: img.parentNode, start: 'top bottom', end: 'bottom top', scrub: true } });
  });

  /* ---------- magnetic buttons ---------- */
  if (fine) $$('.btn-primary,.nav-cta,.next .go i').forEach(function (b) {
    var xTo = gsap.quickTo(b, 'x', { duration: 0.5, ease: 'power3.out' }), yTo = gsap.quickTo(b, 'y', { duration: 0.5, ease: 'power3.out' });
    b.addEventListener('mousemove', function (e) { var r = b.getBoundingClientRect(); xTo((e.clientX - r.left - r.width / 2) * 0.28); yTo((e.clientY - r.top - r.height / 2) * 0.32); });
    b.addEventListener('mouseleave', function () { xTo(0); yTo(0); });
  });

  addEventListener('load', function () { ScrollTrigger.refresh(); });
})();
