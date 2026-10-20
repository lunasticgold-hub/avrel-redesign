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
    const status = document.getElementById('cfStatus')?.value || '';
    const pageUsed = document.getElementById('cfPage')?.value || '';
    const expect = (document.getElementById('cfExpect')?.value || '').trim();
    const subject = encodeURIComponent(`[Avrel website] ${topic} — ${name}`);
    const lines = [msg, ''];
    if (status) lines.push(`Status: ${status}`);
    if (pageUsed) lines.push(`Was using: ${pageUsed}`);
    if (expect) lines.push(`Expected: ${expect}`);
    lines.push('', `— ${name} (${email})`);
    const body = encodeURIComponent(lines.join('\n'));
    location.href = `mailto:${dest}?subject=${subject}&body=${body}`;
  });
}

// Promo countdown → ends at the end of the current month
const promoCount = document.getElementById('promoCountdown');
if (promoCount) {
  const pad = n => String(n).padStart(2, '0');
  const tickPromo = () => {
    const now = new Date();
    const end = new Date(now.getFullYear(), now.getMonth() + 1, 0, 23, 59, 59);
    let s = Math.max(0, Math.floor((end - now) / 1000));
    const d = Math.floor(s / 86400); s -= d * 86400;
    const h = Math.floor(s / 3600); s -= h * 3600;
    const m = Math.floor(s / 60); const sec = s - m * 60;
    promoCount.textContent = `Ends in ${d}d ${pad(h)}:${pad(m)}:${pad(sec)}`;
  };
  tickPromo();
  setInterval(tickPromo, 1000);
}

// Product assistant — quick rule-based answers from real product facts
const aBtn = document.getElementById('assistantBtn');
const aPanel = document.getElementById('assistantPanel');
if (aBtn && aPanel) {
  const aBody = document.getElementById('assistantBody');
  const aInput = document.getElementById('assistantInput');
  const ANSWERS = {
    pricing: 'Starter is <b>$129/mo</b> (Reddit + Facebook Groups, 1,000 lead + 1,000 draft credits). Pro is <b>$229/mo</b> — adds LinkedIn, 5,000 + 5,000 credits, 3 seats. Agency is custom. Full details on the <a href="pricing.html">pricing page</a>.',
    scan: 'Install the extension, pair it with a one-time code, then open a community feed and hit <b>Start scan</b>. Avrel reads the posts on your screen, scores them for buying intent, and sends matches to your dashboard with a draft attached. Walkthrough: <a href="extension.html">the extension page</a>.',
    safe: 'Avrel reads only what is already visible on your screen, and drafts are yours to review. Sequences — if you switch them on — run under daily caps and pacing you set. Your platform password is never asked for; pairing is by one-time code.',
    trial: 'The trial is <b>7 days free</b>: one platform of your choice, 50 saved-lead credits and 50 draft credits — enough to run the full loop from scan to reply. Start from any <b>Start free</b> button on this site.',
    refund: 'The guarantee: use Avrel for 30 days — if it produced <b>no revenue</b>, claim a <b>full refund</b> of your first payment within 60 days of paying. Email support@avrel.in and it gets processed.',
    platforms: 'Scanning today: Reddit, Facebook Groups, LinkedIn, Slack, Discord and Indie Hackers. On the roadmap (V2): X, Product Hunt, Telegram and WhatsApp Communities. Which ones you can use depends on your plan — see <a href="pricing.html">pricing</a>.',
    human: 'Of course — email <b>support@avrel.in</b> (product/billing help) or <b>info@avrel.in</b> (sales), or use the <a href="contact.html">contact page</a>. A small team in Bhubaneswar replies within two business days, usually sooner.',
    fallback: 'I can answer quick questions about pricing, scanning, safety, the trial, platforms and the refund guarantee. For anything else, a human is better: <a href="contact.html">contact page</a> or support@avrel.in.',
  };
  const answerFor = raw => {
    const q = raw.toLowerCase();
    if (/(price|pricing|cost|plan|pay)/.test(q)) return ANSWERS.pricing;
    if (/(refund|guarantee|money back)/.test(q)) return ANSWERS.refund;
    if (/(trial|free)/.test(q)) return ANSWERS.trial;
    if (/(safe|ban|risk|allowed|tos)/.test(q)) return ANSWERS.safe;
    if (/(platform|reddit|linkedin|facebook|slack|discord)/.test(q)) return ANSWERS.platforms;
    if (/(scan|extension|install|chrome|work)/.test(q)) return ANSWERS.scan;
    if (/(human|contact|email|support|talk|call)/.test(q)) return ANSWERS.human;
    return ANSWERS.fallback;
  };
  const addMsg = (html, who) => {
    const div = document.createElement('div');
    div.className = 'a-msg ' + (who === 'user' ? 'a-user' : 'a-bot');
    div.innerHTML = html;
    aBody.appendChild(div);
    aBody.scrollTop = aBody.scrollHeight;
  };
  const toggle = open => {
    aPanel.hidden = !open;
    aBtn.setAttribute('aria-expanded', String(open));
    if (open) aInput.focus();
  };
  aBtn.addEventListener('click', () => toggle(aPanel.hidden));
  document.getElementById('assistantClose').addEventListener('click', () => toggle(false));
  document.querySelectorAll('#assistantChips button').forEach(chip =>
    chip.addEventListener('click', () => addMsg(ANSWERS[chip.dataset.q] || ANSWERS.fallback, 'bot')));
  document.getElementById('assistantForm').addEventListener('submit', e => {
    e.preventDefault();
    const v = aInput.value.trim();
    if (!v) return;
    addMsg(v.replace(/</g, '&lt;'), 'user');
    aInput.value = '';
    setTimeout(() => addMsg(answerFor(v), 'bot'), 250);
  });
}

// Lead calculator (home) — live model: 10–15 leads/platform/day, 22 days
const lc = document.getElementById('leadCalc');
if (lc) {
  const slider = document.getElementById('lcPlatforms');
  const out = document.getElementById('lcPlatformsOut');
  const daily = document.getElementById('lcDaily');
  const monthly = document.getElementById('lcMonthly');
  const plan = document.getElementById('lcPlan');
  const update = () => {
    const p = Number(slider.value);
    const lo = p * 10, hi = p * 15;
    out.textContent = p;
    daily.textContent = `${lo}–${hi}`;
    monthly.textContent = `${(lo * 22).toLocaleString('en-IN')}–${(hi * 22).toLocaleString('en-IN')}`;
    if (p <= 2) plan.innerHTML = 'Fits the <b>Starter</b> plan — 1,000 saved-lead credits cover it.';
    else if (p === 3) plan.innerHTML = 'You want <b>Pro</b> — the 3-platform club, 5,000 saved-lead credits.';
    else plan.innerHTML = 'That is <b>Agency</b> territory — the 5-platform club, 25,000 credits.';
  };
  slider.addEventListener('input', update);
  update();
}

// ROI calculator (pricing)
const rc = document.getElementById('roiCalc');
if (rc) {
  const leads = document.getElementById('roiLeads');
  const rate = document.getElementById('roiRate');
  const rateOut = document.getElementById('roiRateOut');
  const value = document.getElementById('roiValue');
  const planSel = document.getElementById('roiPlan');
  const clients = document.getElementById('roiClients');
  const revenue = document.getElementById('roiRevenue');
  const multiple = document.getElementById('roiMultiple');
  const money = n => '$' + Math.round(n).toLocaleString('en-US');
  const update = () => {
    const L = Math.max(0, Number(leads.value) || 0);
    const R = Number(rate.value);
    const V = Math.max(0, Number(value.value) || 0);
    const C = Number(planSel.value);
    const cl = L * R / 100;
    const rev = cl * V;
    rateOut.textContent = R + '%';
    clients.textContent = (Math.round(cl * 10) / 10).toLocaleString('en-US');
    revenue.textContent = money(rev);
    multiple.textContent = C > 0 && rev > 0 ? Math.round(rev / C).toLocaleString('en-US') + '×' : '—';
  };
  [leads, rate, value, planSel].forEach(el => el.addEventListener('input', update));
  update();
}
