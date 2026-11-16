/* Every page: menu, films, showreel, archive filters and motion. Everything here is progressive
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
  /* ---------- homepage showreel: the framed screen cycles through REEL films ----------
     Each film plays SHOT_MS from its start second, then the next one fades in. The
     ambient blur, the caption link and the counter follow. Pauses while off screen. */
  var SHOT_MS = 9000, SKIP_MS = 4000;
  function startReel() {
    var fig = $('.screen[data-reel]');
    if (!fig) return;
    var list; try { list = JSON.parse(fig.getAttribute('data-reel')); } catch (err) { return; }
    var v = $('video', fig), img = $('.screen-in img', fig), amb = $('.xhero-bg .amb'), cap = $('figcaption a', fig), cnt = $('.reel-n', fig);
    var i = -1, timer = null, visible = true;
    var pad = function (n) { return String(n).padStart(2, '0'); };
    v.muted = true;
    function show(k) {
      i = k % list.length; var r = list[i];
      clearTimeout(timer);
      v.classList.remove('on');
      cap.textContent = r.name; cap.href = r.href;
      if (cnt) cnt.textContent = pad(i + 1) + ' / ' + pad(list.length);
      setTimeout(function () {
        img.src = r.poster; if (amb) amb.src = r.poster;
        v.src = r.src + '#t=' + r.start;
        if (visible) v.play().catch(function () {});
      }, k === 0 ? 0 : 450);
    }
    v.addEventListener('playing', function () {
      v.classList.add('on');
      clearTimeout(timer); timer = setTimeout(function () { show(i + 1); }, SHOT_MS);
    });
    v.addEventListener('error', function () { clearTimeout(timer); timer = setTimeout(function () { show(i + 1); }, SKIP_MS); });
    if ('IntersectionObserver' in window) new IntersectionObserver(function (es) {
      visible = es[0].isIntersecting;
      if (visible) { if (v.src) v.play().catch(function () {}); } else { v.pause(); clearTimeout(timer); }
    }, { threshold: 0.1 }).observe(fig);
    show(0);
  }
  function startFilms() { startHeroFilm(); startReel(); }
  if (desktop && !reduce) {
    if (document.readyState === 'complete') setTimeout(startFilms, 300);
    else addEventListener('load', function () { setTimeout(startFilms, 300); });
  }

  /* ---------- case index: a row's film plays on hover (fine pointers, loaded on first hover) ---------- */
  if (fine && !reduce) $$('.ci').forEach(function (a) {
    var v = $('video', a); if (!v) return;
    a.addEventListener('mouseenter', function () { if (!v.src) v.src = v.getAttribute('data-src'); v.play().then(function () { v.classList.add('on'); }).catch(function () {}); });
    a.addEventListener('mouseleave', function () { v.pause(); v.classList.remove('on'); });
  });

  /* ---------- archive filters: every project is in the HTML; filtering only hides cards ---------- */
  var filters = $$('.pj-f'), cards = $$('.pj');
  filters.forEach(function (b) {
    b.addEventListener('click', function () {
      var f = b.getAttribute('data-f');
      filters.forEach(function (x) { var on = x === b; x.classList.toggle('on', on); x.setAttribute('aria-pressed', on ? 'true' : 'false'); });
      cards.forEach(function (c) { c.hidden = f !== 'all' && c.getAttribute('data-cat') !== f; });
      if (window.ScrollTrigger) ScrollTrigger.refresh();
    });
  });

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

  /* ---------- hero intro: runs after the boot screen (homepage) or straight away ---------- */
  var introQueue = [], introDone = false;
  function onIntro(f) { if (introDone) f(); else introQueue.push(f); }
  function heroIntro() {
    if (introDone) return; introDone = true;
    window.__heroGo = true; dispatchEvent(new Event('hero:intro'));   /* assets/net.js waits for this */
    introQueue.forEach(function (f) { f(); }); introQueue = [];
  }
  /* boot screen, first visit per session: a real load bar (caps at 90% until `load`),
     four log lines, then it slides away. Never longer than 2.6 s. */
  function boot() {
    var el = $('#boot');
    if (!el || !d.classList.contains('booting')) { heroIntro(); return; }
    var log = $('#bootLog'), bar = $('#bootBar'), pct = $('#bootPct');
    var steps = [[.1, 'mounting agents'], [.36, 'wiring ' + (el.getAttribute('data-systems') || 'the') + ' systems'], [.64, 'opening network'], [.9, 'handshake ok']];
    var shown = 0, p = 0, loaded = document.readyState === 'complete', done = false, t0 = performance.now();
    addEventListener('load', function () { loaded = true; }, { once: true });
    function finish() {
      if (done) return; done = true;
      bar.style.transform = 'scaleX(1)'; pct.textContent = '100';
      try { sessionStorage.setItem('booted', '1'); } catch (err) {}
      var a = el.animate ? el.animate([{ transform: 'translateY(0)' }, { transform: 'translateY(-100%)' }], { duration: 760, delay: 160, easing: 'cubic-bezier(.77,0,.175,1)', fill: 'forwards' }) : null;
      if (a) a.onfinish = function () { d.classList.toggle('booting', false); }; else d.classList.toggle('booting', false);
      setTimeout(heroIntro, 420);
    }
    (function tick(t) {
      var e = t - t0, target = Math.min(loaded ? 1 : .9, e / 1150);
      p += (target - p) * .14; if (target >= 1 && p > .99) p = 1;
      bar.style.transform = 'scaleX(' + p.toFixed(3) + ')'; pct.textContent = String(Math.round(p * 100)).padStart(3, '0');
      while (shown < steps.length && p >= steps[shown][0]) { var li = document.createElement('li'); li.innerHTML = '<b>[ ok ]</b><span>' + steps[shown][1] + '</span>'; log.appendChild(li); shown++; }
      if (p >= 1 || e > 2600) finish(); else requestAnimationFrame(tick);
    })(t0);
  }

  /* ---------- text decode: characters scramble, then lock in left to right ---------- */
  var GLY = '!<>-_\\/[]{}=+*^?#0123456789';
  function scramble(el, dur) {
    if (!el || el.children.length || !el.textContent.trim()) return;
    var txt = el.getAttribute('data-txt') || el.textContent; el.setAttribute('data-txt', txt);
    var n = txt.length, t0 = performance.now(); dur = dur || Math.min(900, 260 + n * 18);
    (function f(t) {
      var p = Math.min((t - t0) / dur, 1), lock = Math.floor(n * (p * p * (3 - 2 * p))), o = '';
      for (var i = 0; i < n; i++) { var c = txt[i]; o += (i < lock || c === ' ') ? c : GLY[(Math.random() * GLY.length) | 0]; }
      el.textContent = p < 1 ? o : txt; if (p < 1) requestAnimationFrame(f);
    })(t0);
  }

  /* ---------- cursor light on cards (border on dark cards, spotlight on paper) ---------- */
  if (fine) $$('.pj,.pcard,.offer.caps>li').forEach(function (c) {
    c.addEventListener('pointermove', function (e) {
      var r = c.getBoundingClientRect();
      c.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100) + '%');
      c.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100) + '%');
    });
  });

  if (!d.classList.contains('js-motion') || !window.gsap) {
    d.classList.remove('js-motion');
    $$('[data-count]').forEach(countUp);
    boot();
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
  var tl = gsap.timeline({ paused: true, defaults: { ease: 'expo.out' } });
  onIntro(function () { tl.play(); setTimeout(function () { scramble($('.xhero h1 .grad'), 950); }, 500); });
  /* only the pieces this page has (the homepage has a screen, service pages a phone) */
  var has = function (s) { return !!$(s); };
  tl.to('.xhero h1 .ln>span,.pj-hero h1 .ln>span', { y: 0, duration: 1.15, stagger: 0.09 }, 0.05)
    .to('.xhero [data-hi],.pj-hero [data-hi]', { opacity: 1, y: 0, duration: 0.9, stagger: 0.06 }, 0.3);
  if (has('.glass')) tl.fromTo('.glass', { opacity: 0, y: 30, scale: 0.96 }, { opacity: 1, y: 0, scale: 1, duration: 1.2, stagger: 0.12 }, 0.5);
  if (has('.phone')) tl.fromTo('.phone', { opacity: 0, y: 40 }, { opacity: 1, y: 0, duration: 1.3 }, 0.35);
  if (has('.screen-wrap')) tl.fromTo('.screen-wrap', { y: 50, rotationX: 8 }, { y: 0, rotationX: 0, duration: 1.5 }, 0.25);  /* no fade: its poster is the LCP and stays visible */
  if (has('.xhero-bg')) tl.fromTo('.xhero-bg', { scale: 1.08 }, { scale: 1, duration: 2.4, ease: 'power2.out' }, 0);

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
  if (has('.xhero-in')) gsap.to('.xhero-in', { yPercent: -12, opacity: 0.2, ease: 'none', scrollTrigger: { trigger: '.xhero', start: 'top top', end: 'bottom top', scrub: true } });

  /* ---------- scroll reveals ---------- */
  /* cards wipe open top-down behind a scan line and their title decodes; headings and labels
     decode; everything else rises in. Ported from the original homepage. */
  var EASE = 'cubic-bezier(.16,1,.3,1)', CARD = '.pj,.pcard,.offer>li,.case-index>li,.proc>li,.ways';
  function play(u, delay) {
    gsap.set(u, { opacity: 1, y: 0, filter: 'none' });
    if (u.matches(CARD) && u.animate) {
      u.animate([{ clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0% 0)' }], { duration: 760, delay: delay, easing: EASE, fill: 'backwards' });
      var ln = document.createElement('i'); ln.className = 'scanln'; ln.setAttribute('aria-hidden', 'true'); u.appendChild(ln);
      var h = u.offsetHeight;
      ln.animate([{ transform: 'translateY(0)', opacity: 1 }, { transform: 'translateY(' + h + 'px)', opacity: 1, offset: .9 }, { transform: 'translateY(' + h + 'px)', opacity: 0 }],
        { duration: 760, delay: delay, easing: EASE, fill: 'both' }).onfinish = function () { ln.parentNode && ln.parentNode.removeChild(ln); };
      var t = u.querySelector('h2,h3,.ci-t b'); if (t) setTimeout(function () { scramble(t); }, delay + 120);
    } else if (u.matches('h2,h3,.label')) {
      if (u.animate) u.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 120, delay: delay, fill: 'backwards' });
      setTimeout(function () { scramble(u); }, delay);
    } else {
      gsap.fromTo(u, { opacity: 0, y: 14, filter: 'blur(8px)' }, { opacity: 1, y: 0, filter: 'blur(0px)', duration: 0.9, delay: delay / 1000, ease: 'power3.out' });
    }
  }
  ScrollTrigger.batch('[data-rv]', {
    start: 'top 88%', once: true,
    onEnter: function (els) { els.forEach(function (u, i) { play(u, Math.min(i, 6) * 80); }); }
  });

  /* ---------- process: line scrubbed by scroll, numbers light as it passes ---------- */
  var proc = $('.proc'), procItems = $$('.proc>li');
  if (proc) ScrollTrigger.create({ trigger: proc, start: 'top 80%', end: 'bottom 55%', scrub: 0.6,
    onUpdate: function (s) {
      proc.style.setProperty('--p', s.progress.toFixed(3));
      procItems.forEach(function (li, i) { li.classList.toggle('lit', s.progress >= i / Math.max(1, procItems.length - 1) * .97); });
    } });

  /* archive filter: shown cards pop in */
  $$('.pj-f').forEach(function (b) {
    b.addEventListener('click', function () {
      var k = 0;
      $$('.pj').forEach(function (c) { c.classList.toggle('pop', false); if (!c.hidden) { void c.offsetWidth; c.style.animationDelay = Math.min(k++, 8) * 45 + 'ms'; c.classList.add('pop'); } });
    });
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
  boot();
})();
