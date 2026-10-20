// Avrel redesign — shared behaviour: nav, reveals, progress, counters,
// home signal toast, communities directory, contact form.

// Mobile nav
const burger = document.getElementById('navBurger');
const navLinks = document.getElementById('navLinks');
if (burger && navLinks) {
  burger.addEventListener('click', () => {
    const open = navLinks.classList.toggle('open');
    burger.setAttribute('aria-expanded', String(open));
  });
  navLinks.querySelectorAll('a').forEach(a =>
    a.addEventListener('click', () => navLinks.classList.remove('open')));
}

// Scroll progress bar
const progress = document.getElementById('scrollProgress');
if (progress) {
  addEventListener('scroll', () => {
    const h = document.documentElement;
    const max = h.scrollHeight - h.clientHeight;
    progress.style.width = (max > 0 ? (h.scrollTop / max) * 100 : 0) + '%';
  }, { passive: true });
}

// Reveal on scroll
const io = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (e.isIntersecting) { e.target.classList.add('in'); io.unobserve(e.target); }
  });
}, { threshold: 0.12 });
document.querySelectorAll('.reveal').forEach(el => io.observe(el));

// Animated counters
const fmt = n => n.toLocaleString('en-IN');
const cio = new IntersectionObserver(entries => {
  entries.forEach(e => {
    if (!e.isIntersecting) return;
    const el = e.target, target = Number(el.dataset.count), t0 = performance.now();
    const tick = now => {
      const p = Math.min((now - t0) / 1400, 1);
      el.textContent = fmt(Math.round(target * (1 - Math.pow(1 - p, 3))));
      if (p < 1) requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
    cio.unobserve(el);
  });
}, { threshold: 0.4 });
document.querySelectorAll('[data-count]').forEach(el => cio.observe(el));

// Home: simulated live-signal toast (cycles example signals into view)
const toast = document.getElementById('signalToast');
if (toast) {
  const signals = [
    ['New Hot signal · 94', "“Looking for a Shopify developer — my store's checkout is broken and I'm losing sales.” · r/shopify"],
    ['New Warm signal · 76', '“Who do you use for Google Ads that actually reports properly?” · Facebook Group, Ecommerce Owners'],
    ['New Hot signal · 88', '“Need a logo + brand kit for a coffee brand launching next month.” · r/DesignJobs'],
    ['Follow-up due', "Jenna K. hasn't replied in 3 days — your day-3 bump is drafted and ready."],
  ];
  const title = document.getElementById('toastTitle');
  const text = document.getElementById('toastText');
  let i = 0;
  const cycle = () => {
    const [t, x] = signals[i % signals.length]; i++;
    title.textContent = t; text.textContent = x;
    toast.hidden = false;
    requestAnimationFrame(() => toast.classList.add('show'));
    setTimeout(() => {
      toast.classList.remove('show');
      setTimeout(() => { toast.hidden = true; }, 500);
    }, 5600);
  };
  setTimeout(cycle, 3500);
  setInterval(cycle, 14000);
}

// Communities directory: search + service filter over the real dataset
const grid = document.getElementById('dirGrid');
if (grid) {
  const search = document.getElementById('dirSearch');
  const count = document.getElementById('dirCount');
  const empty = document.getElementById('dirEmpty');
  let data = [], service = 'all';
  const short = n => n >= 1000 ? (n / 1000).toFixed(1).replace(/\.0$/, '') + 'K' : String(n);
  const render = () => {
    const q = (search.value || '').trim().toLowerCase();
    const rows = data.filter(c =>
      (service === 'all' || c.services.includes(service)) &&
      (!q || (c.name + ' ' + c.description).toLowerCase().includes(q)));
    grid.innerHTML = rows.map(c => `
      <article class="comm-card">
        <span class="comm-svc">${c.services[0]}</span>
        <h3><a href="${c.url}" target="_blank" rel="noopener">${c.name}</a></h3>
        <p>${c.description}</p>
        <div class="comm-stats">
          <span><b>${short(c.visitors)}</b>weekly visitors</span>
          <span><b>${c.contributions.toLocaleString('en-IN')}</b>posts &amp; comments / wk</span>
        </div>
      </article>`).join('');
    count.textContent = `Showing ${rows.length} of ${data.length} communities on this page · ranked by visitors & activity`;
    empty.hidden = rows.length > 0;
  };
  fetch('communities-data.json')
    .then(r => r.json())
    .then(j => { data = j; render(); })
    .catch(() => { count.textContent = 'The directory could not load here — the full 500 are inside the Avrel dashboard.'; });
  search.addEventListener('input', render);
  document.querySelectorAll('#dirChips .d-chip').forEach(chip =>
    chip.addEventListener('click', () => {
      document.querySelectorAll('#dirChips .d-chip').forEach(c => c.classList.remove('is-on'));
      chip.classList.add('is-on');
      service = chip.dataset.service;
      render();
    }));
}

// Contact form → opens the visitor's email app, pre-addressed
const form = document.getElementById('contactForm');
if (form) {
  form.addEventListener('submit', e => {
    e.preventDefault();
    const topic = document.getElementById('cfTopic').value;
    const dest = topic === 'Agency plan / sales' ? 'info@avrel.in' : 'support@avrel.in';
    const name = document.getElementById('cfName').value.trim();
    const email = document.getElementById('cfEmail').value.trim();
    const msg = document.getElementById('cfMsg').value.trim();
    const subject = encodeURIComponent(`[Avrel website] ${topic} — ${name}`);
    const body = encodeURIComponent(`${msg}\n\n— ${name} (${email})`);
    location.href = `mailto:${dest}?subject=${subject}&body=${body}`;
  });
}
