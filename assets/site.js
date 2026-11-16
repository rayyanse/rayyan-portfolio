/* Every generated page (light design): menu, pill nav, boot screen (homepage), hero, example
   feed, work cards, films, "What I build" viewer, archive filters, steps, counters and scroll
   motion. Each part only runs when its elements are on the page. Progressive enhancement
   only: the HTML is complete without it, `js-motion` start states are set in <head> only when
   motion is allowed and are cleared after 2.5 s if GSAP never arrives (window.__motionOK).
   Boot, decode, scan-line reveals, cursor light and the process line are ported from the
   original homepage. */
(function () {
  var d = document.documentElement;
  var reduce = matchMedia('(prefers-reduced-motion: reduce)').matches;
  var fine = matchMedia('(hover: hover) and (pointer: fine)').matches;
  var desktop = matchMedia('(min-width: 1001px)').matches;
  var $ = function (s, r) { return (r || document).querySelector(s); };
  var $$ = function (s, r) { return Array.prototype.slice.call((r || document).querySelectorAll(s)); };

  /* ---------- phone menu sheet ---------- */
  var mb = $('.pill-menu'), sheet = $('#sheet');
  if (mb && sheet) {
    var setMenu = function (open) {
      sheet.classList.toggle('open', open);
      mb.setAttribute('aria-expanded', open ? 'true' : 'false');
      mb.setAttribute('aria-label', open ? 'Close menu' : 'Open menu');
      document.body.style.overflow = open ? 'hidden' : '';
    };
    mb.addEventListener('click', function () { setMenu(!sheet.classList.contains('open')); });
    sheet.addEventListener('click', function (ev) { if (ev.target.closest('a')) setMenu(false); });
    addEventListener('keydown', function (ev) { if (ev.key === 'Escape' && sheet.classList.contains('open')) { setMenu(false); mb.focus(); } });
  }

  /* ---------- pill nav: shadow once scrolled, an indicator slides to the section in view ---------- */
  var pill = $('#pill'), ind = $('.pill-ind'), navLinks = $$('.pill-links a[href^="#"]');
  addEventListener('scroll', function () { if (pill) pill.classList.toggle('scrolled', scrollY > 24); }, { passive: true });
  function moveInd(a) {
    if (!ind) return;
    navLinks.forEach(function (x) { x.classList.toggle('on', x === a); });
    if (!a) { ind.style.opacity = 0; return; }
    ind.style.opacity = 1; ind.style.width = a.offsetWidth + 'px'; ind.style.transform = 'translateX(' + a.offsetLeft + 'px)';
  }
  if ('IntersectionObserver' in window && navLinks.length) {
    var secIO = new IntersectionObserver(function (es) {
      es.forEach(function (e) {
        var a = navLinks.filter(function (x) { return x.getAttribute('href') === '#' + e.target.id; })[0];
        if (e.isIntersecting) moveInd(a);
        else if (a && a.classList.contains('on') && e.boundingClientRect.top > 0) moveInd(null);
      });
    }, { rootMargin: '-45% 0px -50% 0px' });
    navLinks.forEach(function (a) { var s = $(a.getAttribute('href')); if (s) secIO.observe(s); });
  }

  /* ---------- copy email ---------- */
  $$('.copy').forEach(function (b) {
    b.addEventListener('click', function () {
      var t = b.getAttribute('data-copy'), ok = function () { b.classList.add('done'); setTimeout(function () { b.classList.remove('done'); }, 1800); };
      if (navigator.clipboard) navigator.clipboard.writeText(t).then(ok, function () { location.href = 'mailto:' + t; });
      else location.href = 'mailto:' + t;
    });
  });

  /* ---------- work cards: the film plays on hover (fine pointers, loaded on first hover) ---------- */
  if (fine && !reduce) $$('.work').forEach(function (w) {
    var sc = $('.screen', w), v = sc && $('video', sc); if (!v) return;
    w.addEventListener('mouseenter', function () {
      if (!v.src) v.src = v.getAttribute('data-src');
      v.muted = true; v.play().then(function () { sc.classList.add('playing'); }).catch(function () {});
    });
    w.addEventListener('mouseleave', function () { v.pause(); sc.classList.remove('playing'); });
  });

  /* ---------- cursor light on cards ---------- */
  if (fine) $$('.stage,.tile').forEach(function (c) {
    c.addEventListener('pointermove', function (e) {
      var r = c.getBoundingClientRect();
      c.style.setProperty('--mx', ((e.clientX - r.left) / r.width * 100) + '%');
      c.style.setProperty('--my', ((e.clientY - r.top) / r.height * 100) + '%');
    });
  });

  /* ---------- films that play in place: hero screens and the "how it works" screen ----------
     Desktop only (phones keep the poster and save data), after `load` so the poster stays the
     LCP, and only while on screen. data-start skips a film's title card. */
  function playInPlace(sc) {
    var v = $('video', sc); if (!v) return;
    var start = parseFloat(v.getAttribute('data-start')) || 0;
    if (!v.src) {
      /* #t= asks the browser to start there; the currentTime set below covers browsers that ignore it */
      v.src = v.getAttribute('data-src') + (start ? '#t=' + start : ''); v.muted = true;
      v.addEventListener('loadedmetadata', function () { if (start) v.currentTime = start; }, { once: true });
      v.addEventListener('playing', function () { sc.classList.add('playing'); }, { once: true });
    }
    v.play().catch(function () {});
  }
  var inPlace = $$('.screen.auto,.how-film .screen');
  function startInPlace() {
    if (!('IntersectionObserver' in window)) return;
    var io = new IntersectionObserver(function (es) {
      es.forEach(function (e) { var v = $('video', e.target); if (e.isIntersecting) playInPlace(e.target); else if (v && v.src) v.pause(); });
    }, { threshold: 0.25 });
    inPlace.forEach(function (sc) { io.observe(sc); });
  }
  if (inPlace.length && desktop && !reduce) {
    if (document.readyState === 'complete') setTimeout(startInPlace, 300);
    else addEventListener('load', function () { setTimeout(startInPlace, 300); }, { once: true });
  }

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

  /* ---------- archive filters: every project is in the HTML; filtering only hides cards ---------- */
  var filters = $$('.pj-f'), pjs = $$('.pj');
  filters.forEach(function (b) {
    b.addEventListener('click', function () {
      var f = b.getAttribute('data-f'), k = 0;
      filters.forEach(function (x) { var on = x === b; x.classList.toggle('on', on); x.setAttribute('aria-pressed', on ? 'true' : 'false'); });
      pjs.forEach(function (c) {
        c.hidden = f !== 'all' && c.getAttribute('data-cat') !== f;
        c.classList.remove('pop');
        if (!c.hidden && !reduce) { void c.offsetWidth; c.style.animationDelay = Math.min(k++, 8) * 45 + 'ms'; c.classList.add('pop'); }
      });
      if (window.ScrollTrigger) ScrollTrigger.refresh();
    });
  });

  /* ---------- case steps: the one in view lights up, the meter tracks progress ---------- */
  var steps = $$('.step'), meter = $('.meter b'), meterTxt = $('.meter span');
  if (steps.length && 'IntersectionObserver' in window) {
    steps[0].classList.add('on');
    var stepIO = new IntersectionObserver(function (es) {
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

  /* ---------- "What I build": pick a capability, the viewer draws its scene ----------
     Auto-advances every CAP_MS while the section is on screen and nobody has clicked. */
  var CAP_MS = 6000;
  var caps = $$('.cap'), viewer = $('.viewer'), box = viewer && $('.proj-viz', viewer);
  var vName = viewer && $('#vName'), vNum = viewer && $('#vNum'), capI = 0, capAuto = !reduce, capTween = null, capVisible = false;
  function showCap(i, user) {
    if (!caps.length) return;
    capI = (i + caps.length) % caps.length;
    caps.forEach(function (c, j) {
      var on = j === capI; c.classList.toggle('on', on);
      $('button', c).setAttribute('aria-expanded', on ? 'true' : 'false');
    });
    var c = caps[capI];
    if (box && c.getAttribute('data-viz') && box.getAttribute('data-viz') !== c.getAttribute('data-viz')) {
      box.setAttribute('data-viz', c.getAttribute('data-viz'));
      if (window.Scenes) window.Scenes.show(box);
    }
    if (vName) vName.textContent = $('h3', c).textContent;
    if (vNum) vNum.textContent = String(capI + 1).padStart(2, '0') + ' / ' + String(caps.length).padStart(2, '0');
    if (user) capAuto = false;
    runCapBar();
  }
  function runCapBar() {
    if (capTween) { capTween.kill(); capTween = null; }
    caps.forEach(function (c) { var i = $('.bar i', c); if (i) i.style.transform = 'scaleX(0)'; });
    if (!capAuto || !capVisible || !window.gsap) return;
    var bar = $('.bar i', caps[capI]);
    capTween = gsap.fromTo(bar, { scaleX: 0 }, { scaleX: 1, duration: CAP_MS / 1000, ease: 'none', onComplete: function () { showCap(capI + 1); } });
  }
  caps.forEach(function (c, i) { $('button', c).addEventListener('click', function () { showCap(i, true); }); });
  if (caps.length && 'IntersectionObserver' in window) new IntersectionObserver(function (es) {
    capVisible = es[0].isIntersecting; runCapBar();
  }, { threshold: 0.25 }).observe($('.build') || caps[0]);

  /* ---------- example feed beside the photo: three slots, events rotate through them ----------
     Labelled "Example events" on the page: each one is something a shipped system does. */
  var FEED_MS = 2600;
  var EVENTS = [
    /* the first three match the HTML (FEED in tools/build_pages.py); rotation starts at the fourth */
    ['WA', 'lead.inbound', 'New WhatsApp lead, answered'],
    ['AI', 'ai.qualify', 'Intent scored, routed to an agent'],
    ['CRM', 'crm.sync', 'Contact and notes written'],
    ['☎', 'call.urdu', 'Urdu call answered, visit booked'],
    ['PDF', 'quote.sent', '2-page quote sent on WhatsApp'],
    ['✓', 'followup.sent', 'Follow-up sent on schedule'],
  ];
  var notes = $$('.note'), evI = notes.length;
  function swapNote() {
    var slot = notes[evI % notes.length], ev = EVENTS[evI % EVENTS.length]; evI++;
    var a = slot.animate ? slot.animate([{ opacity: 1, transform: 'translateY(0) scale(1)' }, { opacity: 0, transform: 'translateY(-8px) scale(.96)' }], { duration: 260, easing: 'ease-in', fill: 'forwards' }) : null;
    var fill = function () {
      $('i', slot).textContent = ev[0]; $('b', slot).textContent = ev[1]; $('span', slot).textContent = ev[2];
      slot.classList.toggle('hot', ev[1] === 'call.urdu');
      if (slot.animate) slot.animate([{ opacity: 0, transform: 'translateY(10px) scale(.96)' }, { opacity: 1, transform: 'translateY(0) scale(1)' }], { duration: 520, easing: 'cubic-bezier(.16,1,.3,1)', fill: 'forwards' });
    };
    if (a) a.onfinish = fill; else fill();
  }

  /* ---------- counters ---------- */
  function countUp(el) {
    var to = parseFloat(el.getAttribute('data-count')), suf = el.getAttribute('data-suffix') || '';
    if (isNaN(to)) return;
    if (reduce || !window.gsap) { el.textContent = to + suf; return; }
    var o = { v: 0 };
    gsap.to(o, { v: to, duration: 1.6, ease: 'power3.out', onUpdate: function () { el.textContent = Math.round(o.v) + suf; } });
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

  /* ---------- intro: after the boot screen, or straight away ---------- */
  var introQueue = [], introDone = false;
  function onIntro(f) { if (introDone) f(); else introQueue.push(f); }
  function heroIntro() {
    if (introDone) return; introDone = true;
    window.__heroGo = true; dispatchEvent(new Event('hero:intro'));   /* assets/net.js waits for this */
    introQueue.forEach(function (f) { f(); }); introQueue = [];
    if (!reduce && notes.length) setInterval(function () { if (!document.hidden && scrollY < innerHeight) swapNote(); }, FEED_MS);
  }
  /* boot screen, first visit per session: a real load bar (caps at 90% until `load`), four log
     lines, then it slides away. BOOT_MAX_MS caps it; the <head> script has a 4.5 s safety cap. */
  var BOOT_MAX_MS = 2600;
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
      var a = el.animate ? el.animate([{ clipPath: 'inset(0 0 0 0)' }, { clipPath: 'inset(0 0 100% 0)' }], { duration: 760, delay: 160, easing: 'cubic-bezier(.77,0,.175,1)', fill: 'forwards' }) : null;
      if (a) a.onfinish = function () { d.classList.remove('booting'); }; else d.classList.remove('booting');
      setTimeout(heroIntro, 420);
    }
    (function tick(t) {
      var e = t - t0, target = Math.min(loaded ? 1 : .9, e / 1150);
      p += (target - p) * .14; if (target >= 1 && p > .99) p = 1;
      bar.style.transform = 'scaleX(' + p.toFixed(3) + ')'; pct.textContent = String(Math.round(p * 100)).padStart(3, '0');
      while (shown < steps.length && p >= steps[shown][0]) { var li = document.createElement('li'); li.innerHTML = '<b>[ ok ]</b><span>' + steps[shown][1] + '</span>'; log.appendChild(li); shown++; }
      if (p >= 1 || e > BOOT_MAX_MS) finish(); else requestAnimationFrame(tick);
    })(t0);
  }

  showCap(0);

  if (!d.classList.contains('js-motion') || !window.gsap) {
    d.classList.remove('js-motion');
    $$('[data-count]').forEach(countUp);
    boot();
    return;
  }
  window.__motionOK = true;
  gsap.registerPlugin(ScrollTrigger);

  /* ---------- inertial scroll (desktop), synced to ScrollTrigger ---------- */
  if (window.Lenis && desktop) {
    var lenis = new Lenis({ lerp: 0.1, smoothWheel: true });
    lenis.on('scroll', ScrollTrigger.update);
    gsap.ticker.add(function (t) { lenis.raf(t * 1000); });
    gsap.ticker.lagSmoothing(0);
    $$('a[href^="#"]').forEach(function (a) {
      a.addEventListener('click', function (e) { var t = $(a.getAttribute('href')); if (t) { e.preventDefault(); lenis.scrollTo(t, { offset: -84 }); } });
    });
  }

  /* ---------- hero entrance ---------- */
  var tl = gsap.timeline({ paused: true, defaults: { ease: 'expo.out' } });
  tl.to('.hero h1 .ln>span', { y: 0, duration: 1.2, stagger: 0.1 }, 0.05)
    .to('.hero [data-hi]', { opacity: 1, y: 0, filter: 'blur(0px)', duration: 0.9, stagger: 0.07 }, 0.35)
    /* the lede is the LCP element: visible from the first paint, it only moves */
    .fromTo('.hero .lede', { y: 18 }, { y: 0, duration: 1 }, 0.4);
  /* the homepage's photo and example feed (absent on inner pages) */
  if ($('.me')) tl.to('.me', { y: 0, rotation: -3.5, scale: 1, duration: 1.6, ease: 'elastic.out(1,.75)' }, 0.25)
    .fromTo('.note', { opacity: 0, y: 24, scale: 0.9 }, { opacity: 1, y: 0, scale: 1, duration: 0.9, stagger: 0.18 }, 0.9)
    .fromTo('.feed-label', { opacity: 0 }, { opacity: 1, duration: 0.8 }, 1.4);
  onIntro(function () {
    tl.play();
    setTimeout(function () { $$('.hero .stats [data-count]').forEach(countUp); }, 700);
  });

  /* ---------- photo: floats, tilts toward the cursor; notes move more (parallax depth) ---------- */
  var me = $('.me');
  if (me && !reduce) {
    gsap.to(me, { yPercent: -3, duration: 3.2, ease: 'sine.inOut', yoyo: true, repeat: -1, delay: 2 });
    if (fine && desktop) {
      var vis = $('.hero-vis');
      var rx = gsap.quickTo(me, 'rotationY', { duration: 0.9, ease: 'power3.out' }), ry = gsap.quickTo(me, 'rotationX', { duration: 0.9, ease: 'power3.out' });
      var layers = $$('[data-depth]').map(function (el) { var k = parseFloat(el.getAttribute('data-depth')); return { k: k, x: gsap.quickTo(el, 'x', { duration: 1.2, ease: 'power3.out' }), y: gsap.quickTo(el, 'y', { duration: 1.2, ease: 'power3.out' }) }; });
      gsap.set(me, { transformPerspective: 900 });
      $('.hero').addEventListener('mousemove', function (e) {
        var r = vis.getBoundingClientRect(), nx = (e.clientX - r.left) / r.width - 0.5, ny = (e.clientY - r.top) / r.height - 0.5;
        rx(nx * 14); ry(-ny * 10);
        layers.forEach(function (l) { l.x(nx * l.k * 50); l.y(ny * l.k * 36); });
      });
      $('.hero').addEventListener('mouseleave', function () { rx(0); ry(0); layers.forEach(function (l) { l.x(0); l.y(0); }); });
    }
  }

  /* ---------- scroll reveals (from the original homepage) ----------
     cards wipe open behind a scan line and their title decodes; labels decode; the rest rises in. */
  var EASE = 'cubic-bezier(.16,1,.3,1)', CARD = '.work,.tile,.cap,.proc>li,.pj,.offer>li,.next-card';
  function play(u, delay) {
    gsap.set(u, { opacity: 1 });
    if (u.matches(CARD) && u.animate) {
      u.animate([{ clipPath: 'inset(0 0 100% 0)' }, { clipPath: 'inset(0 0 0% 0)' }], { duration: 820, delay: delay, easing: EASE, fill: 'backwards' });
      var ln = document.createElement('i'); ln.className = 'scanln'; ln.setAttribute('aria-hidden', 'true'); u.appendChild(ln);
      var h = u.offsetHeight;
      ln.animate([{ transform: 'translateY(0)', opacity: 1 }, { transform: 'translateY(' + h + 'px)', opacity: 1, offset: .9 }, { transform: 'translateY(' + h + 'px)', opacity: 0 }],
        { duration: 820, delay: delay, easing: EASE, fill: 'both' }).onfinish = function () { ln.parentNode && ln.parentNode.removeChild(ln); };
      var t = u.querySelector('.kind,.n'); if (t) setTimeout(function () { scramble(t); }, delay + 120);
    } else if (u.matches('.label')) {
      if (u.animate) u.animate([{ opacity: 0 }, { opacity: 1 }], { duration: 120, delay: delay, fill: 'backwards' });
      setTimeout(function () { scramble(u); }, delay);
    } else if (u.matches('h2')) {
      gsap.fromTo(u, { opacity: 0, y: 40, filter: 'blur(10px)' }, { opacity: 1, y: 0, filter: 'blur(0px)', duration: 1.1, delay: delay / 1000, ease: 'expo.out' });
      var dim = u.querySelector('.dim'); if (dim) gsap.fromTo(dim, { opacity: 0, x: -14 }, { opacity: 1, x: 0, duration: 1, delay: delay / 1000 + 0.35, ease: 'expo.out' });
    } else {
      gsap.fromTo(u, { opacity: 0, y: 16, filter: 'blur(8px)' }, { opacity: 1, y: 0, filter: 'blur(0px)', duration: 0.9, delay: delay / 1000, ease: 'power3.out' });
    }
  }
  ScrollTrigger.batch('[data-rv]', {
    start: 'top 88%', once: true,
    onEnter: function (els) { els.forEach(function (u, i) { play(u, Math.min(i, 6) * 90); }); }
  });

  /* ---------- dark band: grows in from the side margins ---------- */
  var band = $('.band');
  if (band) gsap.fromTo(band, { clipPath: 'inset(6% 4% 6% 4% round 40px)' }, { clipPath: 'inset(0% 0% 0% 0% round 40px)', ease: 'none', scrollTrigger: { trigger: band, start: 'top 95%', end: 'top 35%', scrub: true } });

  /* ---------- process: line scrubbed by scroll, numbers fill as it passes ---------- */
  var proc = $('.proc'), procItems = $$('.proc>li');
  if (proc) ScrollTrigger.create({ trigger: proc, start: 'top 80%', end: 'bottom 55%', scrub: 0.6,
    onUpdate: function (s) {
      proc.style.setProperty('--p', s.progress.toFixed(3));
      procItems.forEach(function (li, i) { li.classList.toggle('lit', s.progress >= i / Math.max(1, procItems.length - 1) * .97); });
    } });

  /* ---------- counters outside the hero start when visible ---------- */
  $$('[data-count]').forEach(function (el) {
    if (el.closest('.hero')) return;
    ScrollTrigger.create({ trigger: el, start: 'top 90%', once: true, onEnter: function () { countUp(el); } });
  });

  /* ---------- magnetic buttons ---------- */
  if (fine) $$('.btn-ink,.pill-cta,.work-body .go').forEach(function (b) {
    var xTo = gsap.quickTo(b, 'x', { duration: 0.5, ease: 'power3.out' }), yTo = gsap.quickTo(b, 'y', { duration: 0.5, ease: 'power3.out' });
    b.addEventListener('mousemove', function (e) { var r = b.getBoundingClientRect(); xTo((e.clientX - r.left - r.width / 2) * 0.28); yTo((e.clientY - r.top - r.height / 2) * 0.32); });
    b.addEventListener('mouseleave', function () { xTo(0); yTo(0); });
  });

  addEventListener('load', function () { ScrollTrigger.refresh(); });
  boot();
})();
