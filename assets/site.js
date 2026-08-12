(() => {
  const path = window.location.pathname;
  const navItems = [
    ['/learn/', 'Learn'],
    ['/gear/', 'Gear'],
    ['/data/', 'Data'],
    ['/stories/', 'Stories'],
    ['/about/', 'About']
  ];

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

  document.querySelectorAll('.byline span:first-child').forEach((node) => {
    if (node.querySelector('a')) return;
    if (node.textContent.trim() === 'By Pickleball Cosmos Editorial') {
      node.innerHTML = 'By <a class="source-link" href="/editorial/">Pickleball Cosmos Editorial</a>';
    }
  });

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
          <div><h4>Publication</h4><a href="/about/">About</a><a href="/editorial/">Editorial</a><a href="/methodology/">Methodology</a></div>
          <div><h4>Standards</h4><a href="/corrections/">Corrections</a><a href="/disclosure.html">Disclosure</a><a href="/privacy.html">Privacy</a></div>
        </div>
      </div>
      <div class="footer-bottom"><span>© <span data-current-year></span> Pickleball Cosmos.</span><span>Independent pickleball media.</span></div>
    </div>`;
  });

  document.querySelectorAll('[data-current-year]').forEach((node) => {
    node.textContent = new Date().getFullYear();
  });

  const socialImage = 'https://www.pickleballcosmos.com/assets/social-card.svg';
  const ensureMeta = (selector, attr, value) => {
    let node = document.querySelector(selector);
    if (!node) {
      node = document.createElement('meta');
      const [key, name] = selector.includes('property=') ? ['property', selector.match(/property="([^"]+)/)[1]] : ['name', selector.match(/name="([^"]+)/)[1]];
      node.setAttribute(key, name);
      document.head.appendChild(node);
    }
    node.setAttribute(attr, value);
  };
  ensureMeta('meta[property="og:image"]', 'content', socialImage);
  ensureMeta('meta[name="twitter:image"]', 'content', socialImage);

  document.querySelectorAll('script[type="application/ld+json"]').forEach((script) => {
    try {
      const data = JSON.parse(script.textContent);
      if (data['@type'] === 'Article' || data['@type'] === 'NewsArticle') {
        data.author = {
          '@type': 'Organization',
          name: 'Pickleball Cosmos Editorial',
          url: 'https://www.pickleballcosmos.com/editorial/'
        };
        data.image = data.image || socialImage;
        data.publisher = {
          '@type': 'NewsMediaOrganization',
          name: 'Pickleball Cosmos',
          url: 'https://www.pickleballcosmos.com/',
          logo: {
            '@type': 'ImageObject',
            url: 'https://www.pickleballcosmos.com/assets/logo.svg'
          }
        };
        script.textContent = JSON.stringify(data);
      }
      if (data['@type'] === 'NewsMediaOrganization') {
        data.url = 'https://www.pickleballcosmos.com/';
        data.publishingPrinciples = 'https://www.pickleballcosmos.com/methodology/';
        data.correctionsPolicy = 'https://www.pickleballcosmos.com/corrections/';
        script.textContent = JSON.stringify(data);
      }
    } catch (_) {
      // Leave valid page content untouched if a structured-data block cannot be parsed.
    }
  });
})();
