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
