(() => {
  const path = window.location.pathname;
  const navItems = [
    ['/learn/', 'Learn'],
    ['/gear/', 'Gear'],
    ['/data/', 'Data'],
    ['/stories/', 'Stories'],
    ['/about/', 'About']
  ];
  const buttondownEndpoint = 'https://buttondown.com/api/emails/embed-subscribe/pickleballcosmos';
  const briefingForm = (source, buttonLabel = 'Join the Briefing') => `<form class="newsletter-form" action="${buttondownEndpoint}" method="post" aria-label="Subscribe to Cosmos Briefing">
    <label class="eyebrow" for="briefing-email-${source}">Email address</label>
    <input id="briefing-email-${source}" type="email" name="email" placeholder="you@example.com" autocomplete="email" inputmode="email" required>
    <input type="hidden" name="embed" value="1">
    <input type="hidden" name="tag" value="cosmos-${source}">
    <button type="submit">${buttonLabel}</button>
    <p class="newsletter-note">Free weekly email. Unsubscribe anytime. <a href="/privacy.html">Privacy →</a></p>
  </form>`;

  document.querySelectorAll('.masthead').forEach((header) => {
    const container = header.querySelector('.container');
    if (!container) return;

    const brand = container.querySelector('.brand');
    if (brand) {
      const span = brand.querySelector('span');
      if (span) span.textContent = 'Pickleball Cosmos';
      brand.setAttribute('href', '/');
    }

    const nav = container.querySelector('.main-nav');
    if (nav) {
      nav.innerHTML = navItems.map(([href, label]) => {
        const active = path.startsWith(href) || (href === '/about/' && ['/editorial/', '/methodology/', '/corrections/'].some((p) => path.startsWith(p)));
        return `<a${active ? ' class="active"' : ''} href="${href}">${label}</a>`;
      }).join('');
    }

    container.querySelectorAll('.mast-actions').forEach((node) => node.remove());
  });

  const menu = document.querySelector('.menu');
  const nav = document.querySelector('.main-nav');
  if (menu && nav) {
    menu.addEventListener('click', () => {
      nav.classList.toggle('open');
      menu.setAttribute('aria-expanded', nav.classList.contains('open') ? 'true' : 'false');
    });
  }

  if (path === '/' || path === '/index.html') {
    const homeNewsletter = [...document.querySelectorAll('.newsletter')].find((node) => !node.dataset.cosmosBriefing);
    if (homeNewsletter && homeNewsletter.children[1] && !homeNewsletter.querySelector('form.newsletter-form')) {
      homeNewsletter.children[1].innerHTML = `${briefingForm('homepage')}<div class="newsletter-launch">A compact weekly read from Pickleball Cosmos. Want more context first? <a href="/briefing/">See what the briefing covers →</a></div>`;
    }
  }

  const article = document.querySelector('.article');
  const skipArticleBriefing = [
    '/about/',
    '/editorial/',
    '/methodology/',
    '/corrections/',
    '/privacy.html',
    '/disclosure.html'
  ].some((prefix) => path.startsWith(prefix));
  if (article && !skipArticleBriefing && !article.querySelector('[data-cosmos-briefing]')) {
    const briefing = document.createElement('section');
    briefing.className = 'newsletter';
    briefing.dataset.cosmosBriefing = 'true';
    briefing.style.marginTop = '42px';
    briefing.innerHTML = `<div><div class="eyebrow">Cosmos Briefing</div><h2>One useful pickleball email a week.</h2><p>Rules changes, original data, rankings, equipment developments and the strongest new reporting — without daily churn.</p><div class="newsletter-meta"><span>Weekly</span><span>Free</span><span>Evidence-led</span></div></div><div>${briefingForm('article')}</div>`;
    const sourceBox = article.querySelector('.source-box');
    if (sourceBox) sourceBox.insertAdjacentElement('beforebegin', briefing);
    else article.appendChild(briefing);
  }

  if (path === '/data/pickleball-courts-by-state-2026/' || path === '/data/pickleball-courts-by-state-2026/index.html') {
    const article = document.querySelector('.article');
    if (article && !article.querySelector('[data-cosmos-infrastructure-visual]')) {
      const makeFigure = (src, alt, caption) => {
        const figure = document.createElement('figure');
        figure.dataset.cosmosInfrastructureVisual = 'true';
        figure.style.margin = '34px 0';
        figure.innerHTML = `<img src="${src}" alt="${alt}" loading="lazy" style="width:100%;height:auto;display:block;border:1px solid #21303d;border-radius:12px;background:#07111b"><figcaption style="margin-top:10px;color:#92a0aa;font-size:.82rem;line-height:1.5">${caption}</figcaption>`;
        return figure;
      };

      const headings = [...article.querySelectorAll('h2')];
      const perCapita = headings.find((h) => h.textContent.trim() === 'The states with the most courts per 100,000 residents');
      if (perCapita) {
        perCapita.insertAdjacentElement('beforebegin', makeFigure(
          '/assets/us-courts-per-capita-tilemap-2026.svg',
          'Tile map of all 50 U.S. states showing known pickleball courts per 100,000 residents in the 2026 Pickleball Cosmos infrastructure baseline.',
          'Pickleball Cosmos 2026 court-density tile map. Court counts come from the dated Pickleheads state-directory snapshot; population denominators are U.S. Census Bureau Vintage 2025 estimates. The colors describe listed infrastructure density, not participation demand.'
        ));
      }

      const reversals = headings.find((h) => h.textContent.trim() === 'The biggest rank reversals');
      if (reversals) {
        const nextHeading = headings[headings.indexOf(reversals) + 1];
        const rankFigure = makeFigure(
          '/assets/us-court-rank-shifts-2026.svg',
          'Chart comparing total-court rank with courts-per-capita rank for the twelve U.S. states with the largest rank shifts.',
          'The 12 largest differences between total-court rank and courts-per-capita rank. A higher per-capita position does not imply stronger demand; it means listed court supply is high relative to resident population.'
        );
        if (nextHeading) nextHeading.insertAdjacentElement('beforebegin', rankFigure);
        else article.appendChild(rankFigure);
      }
    }

    const datasetRecord = document.querySelector('#dataset-record tbody');
    if (datasetRecord && !datasetRecord.querySelector('[data-dataset-terms-row]')) {
      const row = document.createElement('tr');
      row.dataset.datasetTermsRow = 'true';
      row.innerHTML = '<td><strong>Use terms</strong></td><td><a class="source-link" href="/data/dataset-terms/">Dataset Use Terms — third-party source rights preserved</a></td>';
      datasetRecord.appendChild(row);
    }
  }

  if (path === '/data/' || path === '/data/index.html') {
    const finder = document.querySelector('#data-finder-form');
    if (finder) {
      const query = finder.querySelector('#data-finder-query');
      const topic = finder.querySelector('#data-finder-topic');
      const geography = finder.querySelector('#data-finder-geo');
      const metric = finder.querySelector('#data-finder-metric');
      const state = finder.querySelector('#data-finder-state');
      const results = document.querySelector('#data-finder-results');
      const summary = document.querySelector('#data-finder-summary');
      const reset = document.querySelector('#data-finder-reset');
      const params = new URLSearchParams(window.location.search);
      const resources = [
        { title: 'The State of Pickleball in the U.S. 2026', url: '/data/state-of-pickleball-us-2026/', label: 'Flagship report', description: 'Participation, core players, demographics, courts and professional economics—with definitions and limits.', topics: ['participation', 'courts'], geographies: ['us'], metrics: ['headline', 'trend', 'courts', 'download'], terms: '24.3 million 7.5 million players age demographics membership market report csv sources' },
        { title: 'Pickleball Courts by State', url: '/data/pickleball-courts-by-state-2026/', label: '50-state dataset', description: 'Listed courts, locations, density and ranks for all 50 states.', topics: ['courts'], geographies: ['states', 'state', 'us'], metrics: ['courts', 'download'], terms: 'state florida california texas vermont courts locations per capita density census csv infrastructure' },
        { title: 'Court Supply Gap', url: '/data/pickleball-court-supply-gap-2026/', label: 'Original analysis', description: 'States above and below the 50-state court-per-capita benchmark. Not a demand forecast.', topics: ['courts'], geographies: ['states', 'state', 'us'], metrics: ['gap', 'courts'], terms: 'supply gap benchmark california texas new york court shortage density infrastructure' },
        { title: 'Facility Scale by State', url: '/data/pickleball-facility-scale-by-state-2026/', label: '50-state comparison', description: 'Courts per listed location: a concentration measure, not a facility-quality score.', topics: ['courts'], geographies: ['states', 'state', 'us'], metrics: ['facility', 'courts', 'download'], terms: 'facility locations concentration arizona courts per location venues state csv' },
        { title: 'Pickleball vs Tennis Participation', url: '/data/pickleball-vs-tennis-participation/', label: 'Participation series', description: 'The 2020–2025 comparison, growth rates and the shrinking participation gap.', topics: ['participation'], geographies: ['us'], metrics: ['trend', 'headline'], terms: 'tennis comparison growth trend series players 2020 2025' },
        { title: 'The Rise of Pickleball', url: '/data/rise-of-pickleball/', label: 'Participation series', description: 'The reported U.S. participation series from 2020 to 2025, with context and limits.', topics: ['participation'], geographies: ['us'], metrics: ['trend', 'headline'], terms: 'participation growth history 4.2 24.3 million players sfia trend' },
        { title: 'Pickleball World Rankings', url: '/data/pickleball-world-rankings/', label: 'Dated rankings record', description: 'PPA and GPA rankings, definitions and preserved August 2026 source snapshots.', topics: ['rankings'], geographies: ['global'], metrics: ['ranking', 'download'], terms: 'ben johns anna leigh waters ppa gpa pro player ranking points archive' },
        { title: 'State of the Game: Media & Citation Guide', url: '/data/state-of-pickleball-us-2026/media/', label: 'Sources & downloads', description: 'Key figures, definitions, citation guidance and downloadable data for the flagship report.', topics: ['participation', 'courts'], geographies: ['us'], metrics: ['download', 'headline'], terms: 'citation methodology source notes press media download csv definitions' }
      ];
      let stateRows = [];
      const format = new Intl.NumberFormat('en-US');
      const escapeHtml = (value) => String(value).replace(/[&<>'"]/g, (char) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', "'": '&#39;', '"': '&quot;' }[char]));
      const matchValue = (value, allowed) => value === 'all' || allowed.includes(value);
      const normalize = (value) => value.toLowerCase().replace(/[^a-z0-9]+/g, ' ').trim();

      ['q', 'topic', 'geography', 'metric', 'state'].forEach((name) => {
        const field = finder.elements[name];
        if (field && params.has(name)) field.value = params.get(name);
      });

      const render = () => {
        const selected = { q: normalize(query.value), topic: topic.value, geography: geography.value, metric: metric.value, state: state.value };
        const filtered = resources.filter((resource) => {
          const searchable = normalize(`${resource.title} ${resource.label} ${resource.description} ${resource.terms}`);
          return matchValue(selected.topic, resource.topics)
            && matchValue(selected.geography, resource.geographies)
            && matchValue(selected.metric, resource.metrics)
            && (!selected.q || searchable.includes(selected.q) || selected.q.split(' ').every((word) => searchable.includes(word)));
        });
        const stateRow = stateRows.find((row) => row.state === selected.state);
        const cards = [];
        if (stateRow) {
          const aboveBelow = Number(stateRow.vs_us_avg_pct) >= 0 ? 'above' : 'below';
          cards.push(`<a class="data-finder-result state-result" href="/data/pickleball-courts-by-state-2026/"><div class="eyebrow">State lookup · 2026 baseline</div><h3>${escapeHtml(stateRow.state)}</h3><p><strong>${format.format(Number(stateRow.courts))}</strong> listed courts across <strong>${format.format(Number(stateRow.locations))}</strong> listed locations · <strong>${Number(stateRow.courts_per_100k).toFixed(1)}</strong> courts per 100,000 residents · No. <strong>${stateRow.rank_courts}</strong> by total courts and No. <strong>${stateRow.rank_courts_per_100k}</strong> per capita. That is ${Math.abs(Number(stateRow.vs_us_avg_pct)).toFixed(1)}% ${aboveBelow} the 50-state rate.</p><div class="foot">Open the full 50-state dataset →</div></a>`);
        }
        cards.push(...filtered.slice(0, 6).map((resource) => `<a class="data-finder-result" href="${resource.url}"><div class="eyebrow">${resource.label}</div><h3>${resource.title}</h3><p>${resource.description}</p><div class="foot">Open data →</div></a>`));
        results.innerHTML = cards.length ? cards.join('') : '<div class="data-finder-empty">No published Cosmos data page exactly matches that combination yet. Try a broader topic or browse the 50-state court index and the State of the Game report.</div>';
        const filters = [selected.topic !== 'all', selected.geography !== 'all', selected.metric !== 'all', Boolean(selected.q), Boolean(selected.state)].filter(Boolean).length;
        summary.textContent = filters ? `${cards.length} relevant result${cards.length === 1 ? '' : 's'} shown.` : 'Showing the current data library.';
        const updated = new URLSearchParams();
        if (query.value.trim()) updated.set('q', query.value.trim());
        if (topic.value !== 'all') updated.set('topic', topic.value);
        if (geography.value !== 'all') updated.set('geography', geography.value);
        if (metric.value !== 'all') updated.set('metric', metric.value);
        if (state.value) updated.set('state', state.value);
        const search = updated.toString();
        window.history.replaceState({}, '', `${window.location.pathname}${search ? `?${search}` : ''}`);
      };

      const loadStates = fetch('/data/us-state-court-infrastructure-2026.csv')
        .then((response) => response.ok ? response.text() : Promise.reject(new Error('Dataset unavailable')))
        .then((csv) => {
          const [header, ...lines] = csv.trim().split(/\r?\n/);
          const keys = header.split(',');
          stateRows = lines.map((line) => Object.fromEntries(line.split(',').map((value, index) => [keys[index], value])));
          stateRows.forEach((row) => state.insertAdjacentHTML('beforeend', `<option value="${escapeHtml(row.state)}">${escapeHtml(row.state)}</option>`));
          if (params.has('state')) state.value = params.get('state');
          render();
        })
        .catch(() => render());

      finder.addEventListener('submit', (event) => { event.preventDefault(); render(); });
      [query, topic, geography, metric].forEach((field) => field.addEventListener('change', render));
      state.addEventListener('change', () => {
        if (state.value) geography.value = 'state';
        render();
      });
      query.addEventListener('input', () => window.clearTimeout(query._finderTimer) || (query._finderTimer = window.setTimeout(render, 180)));
      reset.addEventListener('click', () => { finder.reset(); render(); query.focus(); });
      render();
      void loadStates;
    }
  }

  document.querySelectorAll('.footer').forEach((footer) => {
    footer.innerHTML = `<div class="container">
      <div class="footer-top">
        <div>
          <a class="brand" href="/"><img src="/assets/logo.svg" alt=""><span>Pickleball Cosmos</span></a>
          <p>Rules, gear, data and stories — reported with clear sourcing and editorial independence.</p>
        </div>
        <div class="footer-links">
          <div><h4>Explore</h4><a href="/learn/">Learn</a><a href="/gear/">Gear</a><a href="/data/">Data</a><a href="/stories/">Stories</a></div>
          <div><h4>Publication</h4><a href="/briefing/">Cosmos Briefing</a><a href="/about/">About</a><a href="/editorial/">Editorial</a><a href="/methodology/">Methodology</a><a href="/contact/">Contact</a></div>
          <div><h4>Standards</h4><a href="/corrections/">Corrections</a><a href="/disclosure.html">Disclosure</a><a href="/privacy.html">Privacy</a></div>
        </div>
      </div>
      <div class="footer-bottom"><span>© <span data-current-year></span> Pickleball Cosmos.</span><span>Independent pickleball media.</span></div>
    </div>`;
  });

  document.querySelectorAll('[data-current-year]').forEach((node) => {
    node.textContent = new Date().getFullYear();
  });
})();
