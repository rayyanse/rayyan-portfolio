/* Motion and film controls for the inner pages. Content is visible without JS:
   the `js-motion` start states are only applied when motion is allowed (set in <head>),
   and they're cleared if GSAP fails to load. */
(function () {
  var d = document.documentElement;
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = window.matchMedia('(pointer: fine)').matches;
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* mobile menu: the button toggles, a link or Escape closes, page scroll locks while open */
  var mb = document.querySelector('.menu-btn'), mm = document.getElementById('mmenu');
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

  /* topbar + scroll progress */
  var bar = document.getElementById('topbar'), prog = document.getElementById('scrollbar');
  function onScroll() {
    var y = window.scrollY, h = document.documentElement.scrollHeight - innerHeight;
    if (bar) bar.classList.toggle('stuck', y > 12);
    if (prog) prog.style.width = (h > 0 ? (y / h) * 100 : 0) + '%';
  }
  addEventListener('scroll', onScroll, { passive: true }); onScroll();

  /* films: muted autoplay (unless reduced motion), sound toggle, pause off-screen */
  $$('.film').forEach(function (f) {
    var v = f.querySelector('video'), btn = f.querySelector('.film-sound');
    if (!v) return;
    if (!reduce) { v.muted = true; v.play().catch(function () {}); }
    if ('IntersectionObserver' in window && !reduce) {
      new IntersectionObserver(function (es) {
        es.forEach(function (e) { if (e.isIntersecting) { v.play().catch(function () {}); } else { v.pause(); } });
      }, { threshold: 0.25 }).observe(v);
    }
    if (btn) btn.addEventListener('click', function () {
      var on = v.muted;
      v.muted = !on;
      if (on) { v.currentTime = 0; v.controls = true; }
      v.play().catch(function () {});
      btn.querySelector('span').textContent = on ? 'Sound on' : 'Play with sound';
      btn.setAttribute('aria-pressed', on ? 'true' : 'false');
    });
  });

  /* counters */
  function countUp(el) {
    var to = parseFloat(el.getAttribute('data-count')), suf = el.getAttribute('data-suffix') || '';
    if (isNaN(to)) return;
    if (reduce || !window.gsap) { el.textContent = to + suf; return; }
    var o = { v: 0 };
    gsap.to(o, { v: to, duration: 1.4, ease: 'power3.out', onUpdate: function () { el.textContent = Math.round(o.v) + suf; } });
  }

  if (!d.classList.contains('js-motion') || !window.gsap) {
    d.classList.remove('js-motion');
    $$('[data-count]').forEach(countUp);
    return;
  }
  window.__motionOK = true;
  gsap.registerPlugin(ScrollTrigger);

  /* hero entrance: headline lines rise from a mask, then copy, then the film settles in */
  var tl = gsap.timeline({ defaults: { ease: 'expo.out' } });
  tl.to('.phero h1 .ln>span', { y: 0, duration: 1.1, stagger: 0.09 }, 0.1)
    .to('.phero [data-hi]', { opacity: 1, y: 0, duration: 0.9, stagger: 0.07 }, 0.35)
    .to('.film', { opacity: 1, scale: 1, duration: 1.3 }, 0.25);

  /* scroll reveals: opacity, blur 8px -> 0, y 24px -> 0 */
  ScrollTrigger.batch('[data-rv]', {
    start: 'top 88%', once: true,
    onEnter: function (els) { gsap.to(els, { opacity: 1, y: 0, filter: 'blur(0px)', duration: 0.9, ease: 'power3.out', stagger: 0.08 }); }
  });

  /* step rail draws as you scroll through the steps */
  $$('.steps').forEach(function (s) {
    var rail = s.querySelector('.rail');
    if (rail) gsap.to(rail, { height: 'calc(100% - 16px)', ease: 'none', scrollTrigger: { trigger: s, start: 'top 75%', end: 'bottom 60%', scrub: 0.6 } });
  });

  /* counters start when visible */
  $$('[data-count]').forEach(function (el) {
    ScrollTrigger.create({ trigger: el, start: 'top 90%', once: true, onEnter: function () { countUp(el); } });
  });

  /* the hero film drifts slower than the page */
  $$('.phero .film').forEach(function (f) {
    gsap.to(f, { yPercent: -6, ease: 'none', scrollTrigger: { trigger: f, start: 'top top+=120', end: 'bottom top', scrub: true } });
  });

  /* magnetic primary buttons */
  if (fine) $$('.btn-primary,.nav-cta').forEach(function (b) {
    var xTo = gsap.quickTo(b, 'x', { duration: 0.5, ease: 'power3.out' }), yTo = gsap.quickTo(b, 'y', { duration: 0.5, ease: 'power3.out' });
    b.addEventListener('mousemove', function (e) { var r = b.getBoundingClientRect(); xTo((e.clientX - r.left - r.width / 2) * 0.25); yTo((e.clientY - r.top - r.height / 2) * 0.3); });
    b.addEventListener('mouseleave', function () { xTo(0); yTo(0); });
  });
})();
