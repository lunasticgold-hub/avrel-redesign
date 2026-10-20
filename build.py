#!/usr/bin/env python3
"""Avrel redesign — multi-page static site builder.
Shared head/nav/footer live here once; each page body is defined below and
written out as a plain .html file. Run: python3 build.py
"""
import re, pathlib

ROOT = pathlib.Path(__file__).parent
LOGIN = "https://www.avrel.in/login"
SIGNUP = "https://www.avrel.in/signup"
ZIP = "https://www.avrel.in/downloads/Avrel.zip"

NAV_LINKS = [
    ("features.html", "Features", "features"),
    ("extension.html", "Extension", "extension"),
    ("communities.html", "Communities", "communities"),
    ("pricing.html", "Pricing", "pricing"),
    ("blog.html", "Blog", "blog"),
    ("about.html", "About", "about"),
    ("faq.html", "FAQ", "faq"),
]

PROMO_BANNER = """
<div class="promo-banner" role="region" aria-label="Prepay offer">
  <p><strong>Prepay &amp; save:</strong> Save 20% when you pay 3 months together.
  <span class="promo-count" id="promoCountdown">Ends soon</span></p>
  <a href="pricing.html">See plans →</a>
</div>
"""

CONSULT_BAND = """
<section class="consult-band">
  <div class="wrap consult-in reveal">
    <div>
      <h2>Book a focused consultation.</h2>
      <p>Bring your current lead process, your questions, or an extension issue — leave with a plan.</p>
    </div>
    <a class="btn btn-lime btn-lg" href="https://calendly.com/lunasticgold/consultation" target="_blank" rel="noopener">Schedule a consultation</a>
  </div>
</section>
"""

ASSISTANT = """
<button class="assistant-btn" id="assistantBtn" aria-label="Open the Avrel product assistant" aria-expanded="false">
  <svg width="22" height="22" viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M21 11.5a8.5 8.5 0 0 1-8.5 8.5c-1.3 0-2.6-.3-3.7-.8L3 20l.9-5.3A8.5 8.5 0 1 1 21 11.5Z" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>
  <span>Ask Avrel</span>
</button>
<div class="assistant-panel" id="assistantPanel" hidden role="dialog" aria-label="Avrel product assistant">
  <div class="assistant-head">
    <strong>Avrel assistant</strong>
    <span>Quick answers, no waiting</span>
    <button class="assistant-close" id="assistantClose" aria-label="Close assistant">✕</button>
  </div>
  <div class="assistant-body" id="assistantBody">
    <div class="a-msg a-bot">Hi — ask me about pricing, how scanning works, safety, the free trial, or the refund guarantee. Tap a topic or type your question.</div>
  </div>
  <div class="assistant-chips" id="assistantChips">
    <button type="button" data-q="pricing">Pricing</button>
    <button type="button" data-q="scan">How scanning works</button>
    <button type="button" data-q="safe">Is it safe?</button>
    <button type="button" data-q="trial">Free trial</button>
    <button type="button" data-q="refund">Refund guarantee</button>
    <button type="button" data-q="human">Talk to a human</button>
  </div>
  <form class="assistant-form" id="assistantForm">
    <input type="text" id="assistantInput" placeholder="Type a question…" aria-label="Type a question" autocomplete="off">
    <button type="submit">Ask</button>
  </form>
</div>
"""

def head(title, desc):
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="icon" href="assets/avrel-mark.svg" type="image/svg+xml">
<link href="https://api.fontshare.com/v2/css?f[]=cabinet-grotesk@500,700,800,900&f[]=satoshi@400,500,700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="styles.css">
</head>
<body>
<div class="scroll-progress" id="scrollProgress" aria-hidden="true"></div>
"""

def _nav_link(href, label, key, active):
    cls = ' class="active" aria-current="page"' if key == active else ""
    return f'<a href="{href}"{cls}>{label}</a>'

def nav(active):
    links = "\n      ".join(
        _nav_link(href, label, key, active) for href, label, key in NAV_LINKS
    )
    return f"""
<header class="nav" id="top">
  <div class="wrap nav-in">
    <a class="brand" href="index.html" aria-label="Avrel home">
      <img src="assets/avrel-mark.svg" alt="" width="36" height="36">
      <span class="brand-word">avrel<i>.</i></span>
    </a>
    <nav class="nav-links" id="navLinks" aria-label="Main">
      {links}
    </nav>
    <div class="nav-cta">
      <a class="btn btn-ghost" href="{LOGIN}">Log in</a>
      <a class="btn btn-lime" href="{SIGNUP}">Start free</a>
      <button class="nav-burger" id="navBurger" aria-label="Open menu" aria-expanded="false">
        <span></span><span></span><span></span>
      </button>
    </div>
  </div>
</header>
"""

FOOTER = CONSULT_BAND + """
<footer class="footer">
  <div class="wrap foot-in">
    <a class="brand" href="index.html">
      <img src="assets/avrel-mark.svg" alt="" width="30" height="30">
      <span class="brand-word">avrel<i>.</i></span>
    </a>
    <nav aria-label="Footer">
      <a href="features.html">Features</a>
      <a href="extension.html">Extension</a>
      <a href="communities.html">Communities</a>
      <a href="pricing.html">Pricing</a>
      <a href="blog.html">Blog</a>
      <a href="about.html">About</a>
      <a href="contact.html">Contact</a>
    </nav>
    <nav aria-label="Legal">
      <a href="privacy.html">Privacy</a>
      <a href="terms.html">Terms</a>
      <a href="cookie-policy.html">Cookies</a>
    </nav>
    <p>© 2026 Avrel · Built in Bhubaneswar, India · Photos: Pexels</p>
  </div>
</footer>
""" + ASSISTANT + """
<script src="script.js"></script>
</body>
</html>
"""

CTA_BAND = """
  <section class="cta-band">
    <div class="wrap cta-in reveal">
      <img src="assets/avrel-mark.svg" alt="" width="56" height="56">
      <h2>Someone is asking<br>for what you sell. <em>Today.</em></h2>
      <a class="btn btn-lime btn-lg" href="https://www.avrel.in/signup">Be the first reply — start free</a>
      <p>7-day free trial · No revenue in 30 days, full refund</p>
    </div>
  </section>
"""

def page(filename, title, desc, active, body):
    html = head(title, desc) + PROMO_BANNER + nav(active) + "\n<main>\n" + body + "\n</main>\n" + FOOTER
    (ROOT / filename).write_text(html)
    print("built", filename)

# ---------------------------------------------------------------- home ----
def build_home():
    """Reuse the v2 one-pager body; swap in the shared nav/footer, retarget
    in-page links, and inject the photo band, counters and signal toast."""
    src = (ROOT / "index.html").read_text()
    body = src[src.index("<main>"):src.index("</main>") + len("</main>")]
    # drop the old final CTA band (the shared CTA_BAND is added below)
    body = body[:body.rindex('<section class="cta-band">')] + CTA_BAND + "\n</main>"
    # in-page anchors that now live on their own pages
    body = body.replace('href="#features"', 'href="features.html"')
    body = body.replace('href="#communities"', 'href="communities.html"')
    body = body.replace('href="#pricing"', 'href="pricing.html"')
    body = body.replace('href="#faq"', 'href="faq.html"')

    photo_band = """
  <!-- ============ PHOTO BAND + COUNTERS ============ -->
  <section class="section section-line">
    <div class="wrap">
      <p class="eyebrow reveal">Who it's for</p>
      <h2 class="reveal">Built for the person who <em>is</em> the sales team.</h2>
      <div class="photo-duo">
        <figure class="photo-card reveal">
          <img src="assets/photo-3769021.jpg" alt="A freelancer smiling at her laptop" loading="lazy">
          <figcaption><strong>The solo freelancer</strong><span>No SDR, no agency retainer — just you, a laptop, and buyers asking in public.</span></figcaption>
        </figure>
        <figure class="photo-card reveal">
          <img src="assets/photo-3184291.jpg" alt="A small agency team shaking hands with a new client" loading="lazy">
          <figcaption><strong>The small agency</strong><span>Three people, forty communities, one pipeline that never sleeps.</span></figcaption>
        </figure>
      </div>
      <div class="counters reveal">
        <div class="counter"><strong><span data-count="56981">0</span></strong><span>communities analysed</span></div>
        <div class="counter"><strong><span data-count="500">0</span></strong><span>curated into your dashboard</span></div>
        <div class="counter"><strong><span data-count="10">0</span></strong><span>platforms, one extension</span></div>
        <div class="counter"><strong>30-day</strong><span>money-back guarantee</span></div>
      </div>
    </div>
  </section>
"""
    marker = "  <!-- ============ HOW IT WORKS ============ -->"
    if "photo-duo" not in body:
        body = body.replace(marker, photo_band + "\n" + marker)

    toast = """
<div class="signal-toast" id="signalToast" role="status" aria-live="polite" hidden>
  <span class="toast-dot"></span>
  <div><strong id="toastTitle">New signal</strong><span id="toastText"></span></div>
</div>
"""
    lead_calc = """
  <!-- ============ LEAD CALCULATOR ============ -->
  <section class="section section-line">
    <div class="wrap calc-wrap">
      <div class="reveal">
        <p class="eyebrow">Lead calculator</p>
        <h2>How many buyers are<br>you <em>walking past?</em></h2>
        <p class="section-sub">The working model behind Avrel: an active scanner finds roughly <strong>10–15 qualified leads per platform, per day</strong>. Move the slider — that's a 22-day working month.</p>
      </div>
      <div class="calc-card reveal" id="leadCalc">
        <label class="calc-label">Platforms you scan <strong id="lcPlatformsOut">2</strong></label>
        <input type="range" id="lcPlatforms" min="1" max="5" step="1" value="2" aria-label="Platforms you scan">
        <div class="calc-outputs">
          <div><strong id="lcDaily">20–30</strong><span>qualified leads / day</span></div>
          <div><strong id="lcMonthly">440–660</strong><span>qualified leads / month</span></div>
        </div>
        <p class="calc-plan" id="lcPlan">Fits the <b>Starter</b> plan — 1,000 saved-lead credits cover it.</p>
        <p class="calc-note">An average for illustration, not a guarantee. Your niche, keywords and platform activity decide the real number.</p>
      </div>
    </div>
  </section>
"""
    feat_marker = "  <!-- ============ FEATURES (spec sheet) ============ -->"
    if 'id="leadCalc"' not in body:
        body = body.replace(feat_marker, lead_calc + "\n" + feat_marker)

    html = head(
        "Avrel — The first reply wins the client",
        "Buyers ask strangers who to hire — in Reddit threads, LinkedIn feeds and Facebook Groups. Avrel finds those posts first, scores them, and writes your reply.",
    ) + PROMO_BANNER + nav("home") + "\n" + body + "\n" + toast + FOOTER
    (ROOT / "index.html").write_text(html)
    print("built index.html")

# ------------------------------------------------------------ features ----
FEATURES_BODY = """
  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow reveal">Features</p>
      <h1 class="reveal">Everything between “someone's asking”<br>and <em>“booked call”.</em></h1>
      <p class="page-sub reveal">Six tools, one job: get you into the right conversation first, with a reply ready and a follow-up that doesn't depend on your memory.</p>
    </div>
  </section>

  <section class="section" style="padding-top:20px">
    <div class="wrap feat-rows">

      <article class="feat-row reveal">
        <div class="feat-copy">
          <span class="spec-no">F—01 · WHY-NOW ENGINE</span>
          <h3>Scores you can cross-examine</h3>
          <p>Most tools hand you a number and ask you to trust it. Avrel shows its working: intent, urgency, budget signals and fit, each tied to the exact words in the post. Read the “why now” and decide in five seconds whether this lead deserves your next ten minutes.</p>
          <ul class="tick-list">
            <li>Hot / Warm / Review temperatures at a glance</li>
            <li>Negative signals exposed too — job-seekers filtered out</li>
            <li>Your keywords, your threshold, your call</li>
          </ul>
        </div>
        <div class="feat-visual">
          <div class="score-demo">
            <div class="score-ring"><strong>92</strong><span>Hot</span></div>
            <ul class="score-reasons">
              <li><b>+35</b> “Need a designer” — direct hiring intent</li>
              <li><b>+15</b> Budget mentioned in the post</li>
              <li><b>+10</b> Posted 4 minutes ago — unanswered</li>
              <li><b>+5</b> Business owner, your exact market</li>
            </ul>
          </div>
        </div>
      </article>

      <article class="feat-row feat-flip reveal">
        <div class="feat-copy">
          <span class="spec-no">F—02 · LEAD LIBRARY</span>
          <h3>Search that finds the one post</h3>
          <p>Three weeks from now you'll half-remember a perfect lead. Type two words and it's back: full-text search over names, posts, communities and keywords — filtered by platform, temperature, status, score and date, with bulk actions when the list gets long.</p>
          <ul class="tick-list">
            <li>Every lead keeps its source post attached</li>
            <li>CSV export when a client asks “show me the pipeline”</li>
            <li>A real timeline per lead — found, drafted, sent, replied</li>
          </ul>
        </div>
        <div class="feat-visual">
          <div class="chip-cloud">
            <span class="f-chip is-on">Hot only</span><span class="f-chip">Reddit</span><span class="f-chip">Score 70+</span><span class="f-chip">“shopify”</span><span class="f-chip">This week</span><span class="f-chip">Follow-up due</span><span class="f-chip">LinkedIn</span><span class="f-chip">Replied</span>
          </div>
        </div>
      </article>

      <article class="feat-row reveal">
        <div class="feat-copy">
          <span class="spec-no">F—03 · PIPELINE HYGIENE</span>
          <h3>Follow-ups that refuse to be forgotten</h3>
          <p>Leads rarely die dramatically. They die quietly — a “let me think about it” you never circled back to. Avrel keeps an overdue list and a “needs a nudge” queue, so the second message (the one that actually closes) always goes out.</p>
          <ul class="tick-list">
            <li>Overdue badges you can't unsee</li>
            <li>One click to schedule the next touch</li>
            <li>Follow-up drafts written alongside the first</li>
          </ul>
        </div>
        <div class="feat-visual">
          <div class="nudge big"><span class="nudge-dot"></span> 3 follow-ups due today <b>· oldest: 2 days</b></div>
          <div class="nudge"><span class="nudge-dot"></span> Jenna K. — Shopify redesign <b>· day 3 bump ready</b></div>
          <div class="nudge"><span class="nudge-dot"></span> r/SEO lead — traffic drop <b>· replied, awaiting scope</b></div>
        </div>
      </article>

      <article class="feat-row feat-flip reveal">
        <div class="feat-copy">
          <span class="spec-no">F—04 · OUTREACH ENGINE</span>
          <h3>Sequences with a seatbelt</h3>
          <p>Turn an approved draft into a Day 0 / Day 3 / Day 7 sequence. You set the daily cap and the pacing; the engine honours both, pauses when a platform pushes back, and stops the moment a reply lands. Ambition included. Recklessness not.</p>
          <ul class="tick-list">
            <li>Per-platform daily caps, set by you</li>
            <li>Auto-pause on replies, captchas and rate limits</li>
            <li>One-tap kill switch in the extension</li>
          </ul>
        </div>
        <div class="feat-visual">
          <div class="seq seq-vertical">
            <span>Day 0 · Intro — your approved draft</span><i></i>
            <span>Day 3 · The bump — short, human, specific</span><i></i>
            <span>Day 7 · The breakup — doors close politely</span><i></i>
            <span class="seq-stop">Reply lands → sequence stops. Always.</span>
          </div>
        </div>
      </article>

      <article class="feat-row reveal">
        <div class="feat-copy">
          <span class="spec-no">F—05 · EXTENSION</span>
          <h3>One extension, ten platforms</h3>
          <p>The scanner lives where the conversations live: inside your browser. Install once, connect with a code, and any feed you open on ten platforms becomes scannable — leads sync to the dashboard with the source attached.</p>
          <a class="cell-link" href="extension.html">See how the extension works →</a>
        </div>
        <div class="feat-visual feat-photo">
          <img src="assets/photo-1181244.jpg" alt="Working from a café table with a laptop and phone" loading="lazy">
        </div>
      </article>

      <article class="feat-row feat-flip reveal">
        <div class="feat-copy">
          <span class="spec-no">F—06 · THE 500</span>
          <h3>Rooms picked for your trade</h3>
          <p>You shouldn't have to discover communities by wandering. Your dashboard deals fresh picks daily from the best 500 of 56,981 analysed — or deal by service: hiring boards, founder rooms, marketing, design, content.</p>
          <a class="cell-link" href="communities.html">Browse the communities →</a>
        </div>
        <div class="feat-visual">
          <div class="chip-cloud">
            <span class="f-chip is-on">Hiring &amp; gig boards</span><span class="f-chip">Startups &amp; owners</span><span class="f-chip">SEO &amp; marketing</span><span class="f-chip">Web, design &amp; video</span><span class="f-chip">Content &amp; social</span><span class="f-chip">Freelancers &amp; agencies</span>
          </div>
        </div>
      </article>

    </div>
  </section>
""" + CTA_BAND

# ----------------------------------------------------------- extension ----
EXTENSION_BODY = """
  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow reveal">The extension</p>
      <h1 class="reveal">It does the walking.<br>You do the <em>talking.</em></h1>
      <p class="page-sub reveal">The Avrel extension sits in your browser and reads the feeds you already open — checking every post for buying intent and sending the matches to your dashboard. Two minutes to install, no new tab to babysit.</p>
      <div class="hero-cta reveal">
        <a class="btn btn-lime btn-lg" href="https://www.avrel.in/downloads/Avrel.zip">Download the extension</a>
        <a class="btn btn-outline btn-lg" href="#install">How installation works ↓</a>
      </div>
    </div>
  </section>

  <section class="section" id="install" style="padding-top:30px">
    <div class="wrap">
      <p class="eyebrow reveal">Install in 2 minutes</p>
      <h2 class="reveal">Four steps. <em>No store, no waiting.</em></h2>
      <div class="steps">
        <article class="step reveal">
          <span class="step-num">01</span>
          <h3>Download &amp; unzip</h3>
          <p>Grab the extension zip and extract it. You'll get one folder called <b>Extension</b> — keep it somewhere it won't get deleted.</p>
        </article>
        <article class="step reveal">
          <span class="step-num">02</span>
          <h3>Load it in Chrome</h3>
          <p>Open <b>chrome://extensions</b>, switch on Developer mode, click “Load unpacked” and pick the Extension folder. The Avrel logo appears in your toolbar.</p>
        </article>
        <article class="step reveal">
          <span class="step-num">03</span>
          <h3>Connect with a code</h3>
          <p>Click the extension, choose “Get my login code”, copy the code from the Avrel tab that opens, paste it back. Your browser and dashboard are now paired.</p>
        </article>
      </div>
      <div class="install-note reveal">
        <strong>Then just browse.</strong> Open a subreddit, a Facebook group or your LinkedIn feed and hit <b>Start scan</b>. Avrel checks the posts as you scroll — matches appear in your dashboard, scored, with drafts attached.
      </div>
    </div>
  </section>

  <section class="section section-line">
    <div class="wrap">
      <p class="eyebrow reveal">Coverage</p>
      <h2 class="reveal">Ten platforms. <em>One scanner.</em></h2>
      <div class="plat-grid">
        <div class="plat reveal"><strong>Reddit</strong><span>Subreddits, home feed, search</span><em>Starter +</em></div>
        <div class="plat reveal"><strong>Facebook Groups</strong><span>Group feeds &amp; search</span><em>Starter +</em></div>
        <div class="plat reveal"><strong>LinkedIn</strong><span>Feed, groups, search</span><em>Pro +</em></div>
        <div class="plat reveal"><strong>X</strong><span>Timelines &amp; search</span><em>Agency</em></div>
        <div class="plat reveal"><strong>Product Hunt</strong><span>Launches &amp; forums</span><em>Agency</em></div>
        <div class="plat reveal"><strong>Indie Hackers</strong><span>Feed &amp; groups</span><em>Agency</em></div>
        <div class="plat reveal"><strong>Discord</strong><span>Servers you belong to</span><em>Agency</em></div>
        <div class="plat reveal"><strong>Slack</strong><span>Workspaces you're in</span><em>Agency</em></div>
        <div class="plat reveal"><strong>Telegram</strong><span>Public channels &amp; groups</span><em>Agency</em></div>
        <div class="plat reveal"><strong>WhatsApp</strong><span>Communities</span><em>Agency</em></div>
      </div>
    </div>
  </section>

  <section class="section section-line">
    <div class="wrap guard-grid">
      <div class="reveal">
        <p class="eyebrow">Straight talk</p>
        <h2>What it does.<br>What it <em>doesn't.</em></h2>
      </div>
      <div class="guard-cols reveal">
        <div class="guard-card">
          <h3>It does</h3>
          <ul class="tick-list">
            <li>Read posts already visible on your screen</li>
            <li>Score them against your keywords and intent signals</li>
            <li>Draft replies in your voice, for your review</li>
            <li>Run approved sequences under caps you set</li>
          </ul>
        </div>
        <div class="guard-card">
          <h3>It doesn't</h3>
          <ul class="cross-list">
            <li>Scrape anything behind a login you don't have</li>
            <li>Send anything you haven't approved or scheduled</li>
            <li>Touch your password — pairing is by one-time code</li>
            <li>Pretend a lead is hot when it can't say why</li>
          </ul>
        </div>
      </div>
    </div>
  </section>
""" + CTA_BAND

# --------------------------------------------------------- communities ----
COMMUNITIES_BODY = """
  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow reveal">Communities</p>
      <h1 class="reveal">Rooms full of buyers,<br>picked by <em>real numbers.</em></h1>
      <p class="page-sub reveal">We analysed 56,981 Reddit communities and kept the 500 where service-buyers actually show up — ranked by weekly visitors and posting activity. Below is a working slice of the directory: search it, filter it by the service you sell. The full 500 live in your dashboard.</p>
    </div>
  </section>

  <section class="section" style="padding-top:26px">
    <div class="wrap">
      <div class="dir-controls reveal">
        <input type="search" id="dirSearch" placeholder="Search the directory — try “hiring”, “seo”, “startup”…" aria-label="Search communities">
        <div class="dir-chips" id="dirChips" role="group" aria-label="Filter by service">
          <button type="button" class="d-chip is-on" data-service="all">All services</button>
          <button type="button" class="d-chip" data-service="Hiring & gig boards">Hiring &amp; gig boards</button>
          <button type="button" class="d-chip" data-service="Startups & business owners">Startups &amp; business owners</button>
          <button type="button" class="d-chip" data-service="SEO & marketing">SEO &amp; marketing</button>
          <button type="button" class="d-chip" data-service="Web, design & video">Web, design &amp; video</button>
          <button type="button" class="d-chip" data-service="Content & social media">Content &amp; social media</button>
          <button type="button" class="d-chip" data-service="Freelancers & agencies">Freelancers &amp; agencies</button>
        </div>
      </div>
      <p class="dir-count" id="dirCount">Loading the directory…</p>
      <div class="comm-grid" id="dirGrid"></div>
      <p class="dir-empty" id="dirEmpty" hidden>No community matches that yet — try a different word or service.</p>
      <div class="dir-note reveal">
        <p><strong>This page shows 48 of the 500.</strong> The full directory — refreshed daily, dealt randomly or by your service — is inside the Avrel dashboard, one click from the extension scanner.</p>
        <a class="btn btn-lime" href="https://www.avrel.in/signup">Get the full 500 — start free</a>
      </div>
    </div>
  </section>
""" + CTA_BAND

# -------------------------------------------------------------- pricing ----
PRICING_BODY = """
  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow reveal">Pricing</p>
      <h1 class="reveal">One client covers <em>a year.</em></h1>
      <p class="page-sub reveal">Start free for 7 days. Every plan is month-to-month, and every plan carries the same guarantee — written below in letters too big to miss.</p>
    </div>
  </section>

  <section class="section" style="padding-top:16px">
    <div class="wrap">
      <div class="guarantee reveal">
        <span class="g-mark">THE GUARANTEE</span>
        <p>No revenue in your first 30 days of using Avrel? <strong>Full refund</strong> — claim it any time within 60 days of your first payment. We'd rather earn the renewal than argue about the refund.</p>
      </div>

      <div class="pricing-grid">
        <article class="price-card reveal">
          <h3>Starter</h3>
          <p class="price"><strong>$129</strong><span>/month</span></p>
          <p class="price-for">Solo freelancers landing their first community clients.</p>
          <ul>
            <li>Reddit + Facebook Groups</li>
            <li>1,000 lead credits / month</li>
            <li>1 seat</li>
            <li>Extension scanning + scoring</li>
            <li>Drafts &amp; follow-up reminders</li>
          </ul>
          <a class="btn btn-outline w-full" href="https://www.avrel.in/signup">Start free trial</a>
        </article>
        <article class="price-card price-featured reveal">
          <span class="price-badge">Most picked</span>
          <h3>Pro</h3>
          <p class="price"><strong>$229</strong><span>/month</span></p>
          <p class="price-for">Freelancers and small agencies working several platforms at once.</p>
          <ul>
            <li>Everything in Starter + LinkedIn</li>
            <li>5,000 lead credits / month</li>
            <li>3 seats</li>
            <li>Sequences with daily caps</li>
            <li>Communities recommended by service</li>
          </ul>
          <a class="btn btn-lime w-full" href="https://www.avrel.in/signup">Start free trial</a>
        </article>
        <article class="price-card reveal">
          <h3>Agency</h3>
          <p class="price"><strong>Custom</strong></p>
          <p class="price-for">Teams running outreach across many clients and brands.</p>
          <ul>
            <li>All 10 platforms</li>
            <li>Custom credits &amp; seats</li>
            <li>Multiple workspaces</li>
            <li>Priority support</li>
          </ul>
          <a class="btn btn-outline w-full" href="contact.html">Talk to us</a>
        </article>
      </div>
      <p class="pricing-note reveal">Pay for 3 months upfront and save 20%. Prices in USD.</p>

      <h2 class="reveal" style="margin-top:84px">Side by <em>side.</em></h2>
      <div class="table-wrap reveal">
        <table class="comm-table compare-table">
          <thead><tr><th>What you get</th><th>Starter</th><th>Pro</th><th>Agency</th></tr></thead>
          <tbody>
            <tr><td><strong>Platforms</strong></td><td>Reddit, Facebook Groups</td><td>+ LinkedIn</td><td>All 10</td></tr>
            <tr><td><strong>Lead credits / month</strong></td><td>1,000</td><td>5,000</td><td>Custom</td></tr>
            <tr><td><strong>Seats</strong></td><td>1</td><td>3</td><td>Custom</td></tr>
            <tr><td><strong>Extension scanning</strong></td><td>Included</td><td>Included</td><td>Included</td></tr>
            <tr><td><strong>Scoring + why-now</strong></td><td>Included</td><td>Included</td><td>Included</td></tr>
            <tr><td><strong>Follow-up queue</strong></td><td>Included</td><td>Included</td><td>Included</td></tr>
            <tr><td><strong>Sequences with caps</strong></td><td>—</td><td>Included</td><td>Included</td></tr>
            <tr><td><strong>Communities by service</strong></td><td>—</td><td>Included</td><td>Included</td></tr>
            <tr><td><strong>Multiple workspaces</strong></td><td>—</td><td>—</td><td>Included</td></tr>
            <tr><td><strong>Support</strong></td><td>Email</td><td>Email</td><td>Priority</td></tr>
          </tbody>
        </table>
      </div>

      <div class="calc-wrap roi-wrap reveal">
        <div>
          <p class="eyebrow">ROI calculator</p>
          <h2>Do the maths<br>before you <em>pay.</em></h2>
          <p class="section-sub">Feed in your own numbers — how many leads you'd work, how often you close, what a client is worth. If the maths doesn't beat the plan price, don't buy the plan.</p>
        </div>
        <div class="calc-card" id="roiCalc">
          <div class="roi-grid">
            <label class="calc-label">Leads you work / month
              <input type="number" id="roiLeads" value="220" min="0" step="10">
            </label>
            <label class="calc-label">Close rate <strong id="roiRateOut">5%</strong>
              <input type="range" id="roiRate" min="1" max="30" step="1" value="5" aria-label="Close rate percent">
            </label>
            <label class="calc-label">Average client value ($)
              <input type="number" id="roiValue" value="1500" min="0" step="50">
            </label>
            <label class="calc-label">Plan
              <select id="roiPlan">
                <option value="129" selected>Starter — $129/mo</option>
                <option value="229">Pro — $229/mo</option>
              </select>
            </label>
          </div>
          <div class="calc-outputs">
            <div><strong id="roiClients">11</strong><span>new clients / month</span></div>
            <div><strong id="roiRevenue">$16,500</strong><span>expected revenue</span></div>
            <div><strong id="roiMultiple">128×</strong><span>return on the plan</span></div>
          </div>
          <p class="calc-note">Illustrative only — your offer, niche and follow-up decide the real result. The guarantee covers the downside: no revenue in 30 days, full refund.</p>
        </div>
      </div>

      <div class="faq-list" style="margin-top:64px">
        <details class="faq reveal">
          <summary>How does the free trial work?</summary>
          <p>Seven days free: one platform, 50 saved-lead credits and 50 draft credits — enough to run the full loop from scan to reply. No sales call required to start, and if you later pay and see no revenue in 30 days, the guarantee has you covered anyway.</p>
        </details>
        <details class="faq reveal">
          <summary>What is a lead credit?</summary>
          <p>One credit covers one lead saved to your dashboard (or one drafted outreach) in a month. Scanning and reading posts is unlimited — credits only count the leads you keep.</p>
        </details>
        <details class="faq reveal">
          <summary>Can I change plans later?</summary>
          <p>Yes — upgrade when you need LinkedIn, more credits or more seats; downgrade when a project ends. Changes apply from the next billing cycle.</p>
        </details>
        <details class="faq reveal">
          <summary>How do I claim the refund?</summary>
          <p>Email support within 60 days of your first payment, after at least 30 days of use, and say the words. We process it — no exit interview, no forms in triplicate.</p>
        </details>
      </div>
    </div>
  </section>
""" + CTA_BAND

# ---------------------------------------------------------------- about ----
ABOUT_BODY = """
  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow reveal">About Avrel</p>
      <h1 class="reveal">Built by people who<br>sell services <em>for a living.</em></h1>
      <p class="page-sub reveal">Avrel isn't a big-tech side project. It's the tool a small agency in Bhubaneswar, India built for itself — because finding clients in communities worked, and doing it by hand didn't scale.</p>
    </div>
  </section>

  <section class="section" style="padding-top:26px">
    <div class="wrap about-grid">
      <div class="about-copy reveal">
        <h2>The short <em>version.</em></h2>
        <p>ContentOra Media runs growth for clients — SEO, content, outreach. The work that consistently brought in business wasn't ads or cold email blasts. It was showing up in the right Reddit thread or Facebook group <strong>the day someone asked for help</strong>, with a useful answer.</p>
        <p>The problem: those moments are rare, scattered across hundreds of communities, and dead within hours. So we started keeping lists — which rooms, which keywords, which posts were real buyers. The lists became a script. The script became Avrel.</p>
        <p>Today the analysis behind it covers <strong>56,981 communities</strong>, and the product is used by freelancers and agencies who'd rather reply to a buyer than pitch a stranger. We're still small, still in Bhubaneswar, and still answering support email ourselves.</p>
      </div>
      <figure class="about-photo reveal">
        <img src="assets/photo-3184291.jpg" alt="A small team closing a deal with a handshake" loading="lazy">
        <figcaption>The moment every lead is supposed to end in.</figcaption>
      </figure>
    </div>
  </section>

  <section class="section section-line">
    <div class="wrap">
      <p class="eyebrow reveal">How we build</p>
      <h2 class="reveal">Four rules we <em>don't bend.</em></h2>
      <div class="principles">
        <article class="principle reveal"><span>01</span><h3>Scores explain themselves</h3><p>If the product can't say why a lead is hot — in plain words, tied to the post — it doesn't get to call it hot.</p></article>
        <article class="principle reveal"><span>02</span><h3>Humans approve the send</h3><p>Drafts and sequences start from your words and your caps. Automation serves your judgement; it doesn't replace it.</p></article>
        <article class="principle reveal"><span>03</span><h3>Real numbers or none</h3><p>Our community data is measured — visitors, activity, the lot — and we show it in the product instead of rounding it into marketing.</p></article>
        <article class="principle reveal"><span>04</span><h3>No revenue, no cost</h3><p>The refund guarantee isn't a promotion. It's the business model: Avrel earns when you do.</p></article>
      </div>
      <figure class="wide-photo reveal">
        <img src="assets/photo-3184339.jpg" alt="An agency team collaborating around a table of laptops" loading="lazy">
      </figure>
    </div>
  </section>
""" + CTA_BAND

# ------------------------------------------------------------------ faq ----
FAQ_ITEMS = [
    ("So… how does it actually find the leads?",
     "You install the Chrome extension, connect it with a one-time code, and open the communities where your buyers spend time. Avrel reads what's on your screen, checks each post against your keywords and buying-intent signals, scores the matches and parks them in your dashboard — source post attached, draft included."),
    ("Is my Reddit / LinkedIn account safe?",
     "Avrel reads only what's already on your screen and writes drafts for your review — nothing posts itself without your setup. Sequences, if you turn them on, run under daily caps and pacing you choose. Your accounts stay yours; the final click stays human."),
    ("Which platforms does it cover?",
     "Ten: Reddit, LinkedIn, Facebook Groups, X, Product Hunt, Indie Hackers, Discord, Slack, Telegram and WhatsApp Communities. Starter opens Reddit + Facebook Groups, Pro adds LinkedIn, Agency unlocks the full ten."),
    ("Do I need the extension to use Avrel?",
     "For scanning, yes — that's how posts get from the platforms into your dashboard. The dashboard itself (search, follow-ups, drafts, sequences) works in any browser once leads are in. Install takes about two minutes."),
    ("What counts as a lead credit?",
     "Credits are your monthly allowance for the work Avrel stores for you — saved leads and drafted outreach. Your plan page shows the allowance (Starter 1,000/month, Pro 5,000/month); the 7-day free trial includes 50 saved-lead and 50 draft credits so you can feel the full loop before paying."),
    ("And if it makes me no money?",
     "Then it costs you no money. Use it for 30 days — no revenue means a full refund, claimable within 60 days of your first payment. It's on the pricing page in big letters, on purpose."),
    ("I'm a solo freelancer, not an agency. Worth it?",
     "That's who Starter was built for. Your dashboard even deals communities by trade — hiring boards when you need a gig this week, founder rooms when you're building toward retainers."),
    ("Which plan do I need for LinkedIn?",
     "Pro and above. Starter covers Reddit and Facebook Groups — which, honestly, is where most service buyers ask first."),
    ("How are the 500 communities chosen?",
     "From 56,981 communities we measured: weekly visitors, weekly posts and comments, and how often buying conversations actually happen there. Dead rooms and spam farms don't make the cut, whatever their size."),
    ("Can my team share one account?",
     "Pro includes 3 seats and Agency is built for teams, with multiple workspaces for different clients. Each person pairs their own browser with their own code."),
]
FAQ_BODY = """
  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow reveal">FAQ</p>
      <h1 class="reveal">Asked in communities,<br>answered <em>here.</em></h1>
      <p class="page-sub reveal">The questions freelancers and agencies ask before they start — answered the way we'd want them answered. Something missing? <a class="text-link" href="contact.html">Ask us directly</a>.</p>
    </div>
  </section>
  <section class="section" style="padding-top:16px">
    <div class="wrap faq-wrap">
      <div class="faq-list">
""" + "\n".join(
    f'        <details class="faq reveal"><summary>{q}</summary><p>{a}</p></details>'
    for q, a in FAQ_ITEMS
) + """
      </div>
    </div>
  </section>
""" + CTA_BAND

# -------------------------------------------------------------- contact ----
CONTACT_BODY = """
  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow reveal">Contact</p>
      <h1 class="reveal">Talk to a <em>human.</em></h1>
      <p class="page-sub reveal">A small team in Bhubaneswar reads every message itself. Pick a door — they all lead to the same people.</p>
    </div>
  </section>

  <section class="section" style="padding-top:26px">
    <div class="wrap">
      <div class="contact-cards">
        <article class="contact-card reveal">
          <span class="spec-no">SUPPORT</span>
          <h3>Something's broken?</h3>
          <p>Bugs, billing, account help — or a refund claim under the guarantee.</p>
          <a href="mailto:support@avrel.in">support@avrel.in</a>
        </article>
        <article class="contact-card reveal">
          <span class="spec-no">SALES</span>
          <h3>Agency plan questions</h3>
          <p>Custom credits, seats and workspaces — tell us how your team sells.</p>
          <a href="mailto:info@avrel.in">info@avrel.in</a>
        </article>
        <article class="contact-card reveal">
          <span class="spec-no">DIRECT</span>
          <h3>Everything else</h3>
          <p>Partnerships, press, or “your product got this wrong” — we read those twice.</p>
          <a href="mailto:abhigyan@avrel.in">abhigyan@avrel.in</a>
        </article>
      </div>

      <div class="promise-strip reveal">
        <p><strong>Response time:</strong> we reply within two business days — usually much sooner.</p>
        <p><strong>Who we serve:</strong> freelancers, agencies, founders, and growth teams worldwide.</p>
      </div>

      <div class="contact-form-wrap reveal">
        <h2>Or write it <em>here.</em></h2>
        <p class="form-note">This form opens your own email app with the message addressed and written — nothing is stored on this page. The more of it you fill, the faster the fix.</p>
        <form id="contactForm" class="contact-form">
          <label>Your name<input type="text" id="cfName" required autocomplete="name"></label>
          <label>Your email<input type="email" id="cfEmail" required autocomplete="email"></label>
          <label>Topic
            <select id="cfTopic">
              <option>Support</option><option>Agency plan / sales</option><option>Feedback</option><option>Something else</option>
            </select>
          </label>
          <label>Are you…
            <select id="cfStatus">
              <option>Just exploring</option><option>In my free trial</option><option>A paying customer</option>
            </select>
          </label>
          <label>What were you using?
            <select id="cfPage">
              <option>The dashboard</option><option>The Chrome extension</option><option>The leads page</option><option>Billing</option><option>Signup or login</option><option>Something else</option>
            </select>
          </label>
          <label>What did you expect to happen? (optional)<input type="text" id="cfExpect" placeholder="e.g. the scan would pick up the posts in my group"></label>
          <label class="form-wide">Message<textarea id="cfMsg" rows="6" required placeholder="Tell us what's up — the page you were on, what happened, any error message you saw."></textarea></label>
          <button type="submit" class="btn btn-lime btn-lg">Open in my email app →</button>
        </form>
      </div>
    </div>
  </section>
"""

# ------------------------------------------------------------------ blog ----
BLOG_POSTS = [
    ("find-freelance-clients-on-reddit-without-getting-banned", "Reddit",
     "Find Freelance Clients on Reddit Without Getting Banned",
     "The subreddits worth your time, the posts that signal a real buyer, and the behaviour that gets freelancers shadow-banned."),
    ("linkedin-lead-generation-for-small-agencies-manual-playbook", "LinkedIn",
     "LinkedIn Lead Generation for Small Agencies: The Manual Playbook",
     "A sustainable, human-run LinkedIn routine for small agencies — no automation spam, no burned accounts."),
    ("best-facebook-groups-for-freelancers-to-find-us-clients", "Facebook",
     "Best Facebook Groups for Freelancers to Find US Clients",
     "How to spot the groups where US clients actually hire, and the ones that are just freelancers shouting at each other."),
    ("complete-guide-to-lead-scoring-community-sourced-leads", "Guide",
     "The Complete Guide to Lead Scoring for Community-Sourced Leads",
     "Intent, urgency, fit and timing — how to score a community post so your follow-up list sorts itself."),
    ("how-to-write-manual-outreach-reply-that-doesnt-sound-like-spam", "Outreach",
     "How to Write a Manual Outreach Reply That Doesn't Sound Like Spam",
     "The anatomy of a reply that gets answered: specific, short, and clearly written by a person who read the post."),
    ("manual-safe-community-outreach", "Guide",
     "Manual, Safe Community Outreach: The Playbook",
     "Avrel's ground rules for community outreach that respects platform rules and community norms — and still books calls."),
    ("how-many-leads-per-day-from-one-community-platform", "Research",
     "How Many Leads Per Day Can One Community Platform Actually Give You?",
     "The honest maths behind the 10–15 qualified leads per platform per day model, and what moves the number."),
    ("where-us-founders-ask-for-help-slack-discord-communities", "Research",
     "Where US Founders Ask for Help: Slack & Discord Communities",
     "Founder communities are where urgent, time-boxed requests surface first. Here's how to be in the room, usefully."),
    ("community-led-growth-vs-cold-outreach-2026", "Growth",
     "Community-Led Growth vs Cold Outreach (2026)",
     "Reply rates, trust, and cost per conversation — how showing up where buyers ask compares with cold blasting."),
    ("can-spam-and-platform-tos-basics-for-community-outreach", "Compliance",
     "CAN-SPAM and Platform ToS Basics for Community Outreach",
     "The legal and platform rules that govern outreach, in plain English — what you can do, and what gets accounts killed."),
    ("how-to-build-a-weekly-seo-content-system-for-community-led-saas", "Content",
     "How to Build a Weekly SEO Content System for a Community-Led SaaS",
     "Turn the questions your buyers ask in communities into a content engine that compounds."),
]
BLOG_BODY = """
  <section class="page-hero">
    <div class="wrap">
      <p class="eyebrow reveal">The Avrel blog</p>
      <h1 class="reveal">Field notes on finding<br>clients in <em>communities.</em></h1>
      <p class="page-sub reveal">Everything we publish comes from the work itself — scanning rooms, scoring posts, writing replies that get answered. Full articles open on avrel.in.</p>
    </div>
  </section>
  <section class="section" style="padding-top:26px">
    <div class="wrap">
      <div class="blog-grid">
""" + "\n".join(
    f'''        <article class="post-card reveal">
          <span class="comm-svc">{tag}</span>
          <h3><a href="https://www.avrel.in/blog/{slug}" target="_blank" rel="noopener">{title}</a></h3>
          <p>{excerpt}</p>
          <div class="post-meta"><span>Sep 2026</span><a href="https://www.avrel.in/blog/{slug}" target="_blank" rel="noopener">Read on avrel.in →</a></div>
        </article>'''
    for slug, tag, title, excerpt in BLOG_POSTS
) + """
      </div>
    </div>
  </section>
""" + CTA_BAND

# ----------------------------------------------------------------- legal ----
def legal_body(title, intro, sections, extra=""):
    secs = "\n".join(
        f'        <section class="legal-sec reveal"><h2>{h}</h2><p>{b}</p></section>'
        for h, b in sections
    )
    return f"""
  <section class="page-hero">
    <div class="wrap legal-wrap">
      <p class="eyebrow reveal">Legal</p>
      <h1 class="reveal">{title}</h1>
      <p class="page-sub reveal">{intro}</p>
      <p class="legal-updated">Last updated October 2026</p>
    </div>
  </section>
  <section class="section" style="padding-top:6px">
    <div class="wrap legal-wrap">
{secs}
{extra}
    </div>
  </section>
"""

PRIVACY_BODY = legal_body(
    "Privacy Policy",
    "How Avrel handles lead data, knowledge documents and retention — and what the extension does and does not collect.",
    [
        ("What this product does",
         "avrel.in operates Avrel for visible community opportunity research, customer and market intelligence, and human-reviewed action preparation."),
        ("What the extension reads",
         "The extension scans only visible content on pages you open, and only after you start a scan manually. It does not read pages in the background, and it does not access content behind logins you have not opened yourself."),
        ("What syncs to your workspace",
         "When sync is enabled, we store lead snippets, source URLs, matched signals, scores, status, notes, knowledge-base context, and usage events in your workspace."),
        ("Knowledge documents",
         "Uploaded knowledge documents are limited to PDF, DOCX, and TXT files up to 10 MB per file."),
        ("Retention and deletion",
         "Default lead retention is 90 days unless you delete leads earlier. You can delete leads and uploaded knowledge files at any time from the dashboard."),
        ("What we never do",
         "We do not collect platform passwords, do not bypass private access, and do not auto-send outreach of any kind."),
    ],
    extra="""      <div class="legal-card reveal">
        <h2>Questions about your data</h2>
        <p>Email <a href="mailto:support@avrel.in">support@avrel.in</a> and we will respond within two business days.</p>
      </div>""",
)

TERMS_BODY = legal_body(
    "Terms of Service",
    "What you're buying, what the trial includes, what you are responsible for, and the refund guarantee — in plain words.",
    [
        ("What you are buying",
         "avrel.in provides Avrel for compliant lead research, lead qualification, knowledge-base assisted drafting, and manual outreach workflows."),
        ("Trial",
         "The 7-day trial includes 50 saved lead credits and 50 Conversation draft credits on one platform of your choice. After the trial, continued access requires a paid plan."),
        ("Your responsibilities",
         "You are responsible for complying with the terms of each platform you scan, the rules of the communities you participate in, applicable consent requirements, and applicable privacy laws including CAN-SPAM."),
        ("What this product will not do",
         "Automatic DM sending, automatic comments, automatic replies, automatic posts, auto follow-up blasting, scraping hidden data, and evasion behaviour are not part of this product and will not be added."),
        ("Refund guarantee",
         "Use Avrel for 30 days. If it produced no revenue for you, claim a full refund of your first payment within 60 days of paying — email support@avrel.in and we process it."),
        ("Changes to these terms",
         "We will email account holders at least 14 days before any material change to these terms takes effect."),
    ],
)

COOKIE_BODY = legal_body(
    "Cookie Policy",
    "Avrel uses essential cookies for authentication and may use product analytics cookies where enabled. Nothing exotic, nothing sold.",
    [
        ("What cookies do here",
         "Cookies support login sessions, workspace access, security, preferences, and product analytics."),
        ("Essential cookies",
         "Authentication and security cookies keep you signed in and protect your workspace. The site does not work without these, so they are always on."),
        ("Analytics cookies",
         "Where analytics is enabled, product analytics cookies help us understand which pages and features get used, so we can fix what confuses people. They are product analytics — not advertising trackers."),
        ("Your controls",
         "You can block or clear cookies in your browser settings at any time; signing in again will simply set fresh essential cookies. Questions: support@avrel.in."),
    ],
)

# ----------------------------------------------------------------- main ----
if __name__ == "__main__":
    build_home()
    page("features.html", "Features — Avrel",
         "Scoring you can cross-examine, a follow-up queue that won't let leads die, sequences with a seatbelt, one extension for ten platforms.",
         "features", FEATURES_BODY)
    page("extension.html", "The Extension — Avrel",
         "Install in two minutes, connect with a code, and scan Reddit, LinkedIn, Facebook Groups and seven more platforms for buyer intent.",
         "extension", EXTENSION_BODY)
    page("communities.html", "Communities — Avrel",
         "The best 500 of 56,981 analysed communities, ranked by real visitor and activity numbers — searchable by the service you sell.",
         "communities", COMMUNITIES_BODY)
    page("pricing.html", "Pricing — Avrel",
         "Starter $129, Pro $229, Agency custom. 7-day free trial and a 30-day no-revenue full-refund guarantee on every plan.",
         "pricing", PRICING_BODY)
    page("about.html", "About — Avrel",
         "Avrel is built by ContentOra Media in Bhubaneswar — the community lead-finding tool a small agency made for itself, now open to freelancers and agencies.",
         "about", ABOUT_BODY)
    page("faq.html", "FAQ — Avrel",
         "How Avrel finds leads, platform coverage, account safety, credits, plans and the refund guarantee — answered plainly.",
         "faq", FAQ_BODY)
    page("contact.html", "Contact — Avrel",
         "Support, sales and direct email for Avrel — a small team in Bhubaneswar that reads every message itself.",
         "contact", CONTACT_BODY)
    page("blog.html", "Blog — Avrel",
         "Field notes on finding clients in online communities: Reddit, LinkedIn and Facebook playbooks, lead scoring, outreach craft and compliance basics.",
         "blog", BLOG_BODY)
    page("privacy.html", "Privacy Policy — Avrel",
         "How Avrel handles lead data, knowledge documents, retention, and what the extension does and does not collect.",
         "", PRIVACY_BODY)
    page("terms.html", "Terms of Service — Avrel",
         "What you are buying, the trial, your responsibilities, and the no-revenue full-refund guarantee.",
         "", TERMS_BODY)
    page("cookie-policy.html", "Cookie Policy — Avrel",
         "Essential cookies for authentication and security, product analytics where enabled, and your controls.",
         "", COOKIE_BODY)
    print("done")
