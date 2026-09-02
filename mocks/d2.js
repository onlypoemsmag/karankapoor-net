/* D2 interactions: Lenis smooth scroll (ONLY POEMS recipe) + baseline-rise reveal */
(function () {
  var reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Lenis — lerp .075, wheelMultiplier .9 (measured from onlypoems.com)
  if (!reduced && window.Lenis) {
    var lenis = new Lenis({ lerp: 0.075, wheelMultiplier: 0.9, smoothWheel: true });
    function raf(t) { lenis.raf(t); requestAnimationFrame(raf); }
    requestAnimationFrame(raf);
  }

  // Baseline-rise reveal (below fold only; dies under reduced motion)
  var hidden = document.querySelectorAll('.rise[data-hidden]');
  if (reduced) {
    hidden.forEach(function (el) { el.removeAttribute('data-hidden'); });
    return;
  }
  hidden.forEach(function (el) {
    if (el.getBoundingClientRect().top < innerHeight * 0.96) el.removeAttribute('data-hidden');
  });
  var lastY = scrollY, lastT = performance.now();
  var io = new IntersectionObserver(function (entries) {
    var now = performance.now();
    var fast = Math.abs(scrollY - lastY) / Math.max(1, now - lastT) > 3;
    lastY = scrollY; lastT = now;
    var i = 0;
    entries.forEach(function (e) {
      if (!e.isIntersecting) return;
      var el = e.target;
      io.unobserve(el);
      if (fast) { el.removeAttribute('data-hidden'); return; }
      setTimeout(function () { el.classList.add('revealed'); el.removeAttribute('data-hidden'); }, i++ * 70);
    });
  }, { rootMargin: '0px 0px -4% 0px' });
  document.querySelectorAll('.rise[data-hidden]').forEach(function (el) { io.observe(el); });
})();
