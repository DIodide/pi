// Lightweight page-switcher injected on every wireframe page.
// Renders a floating top-right pill: ← Prev · current · Next →
// Each link is a real <a href>, so browser back/forward works naturally.
(function () {
  const pages = [
    { file: 'landing.html',   label: 'Landing'   },
    { file: 'dashboard.html', label: 'Dashboard' },
    { file: 'chat.html',      label: 'Chat'      },
    { file: 'apps.html',      label: 'Apps'      },
    { file: 'proactive.html', label: 'Proactive' },
  ];

  const current = (location.pathname.split('/').pop() || 'index.html').toLowerCase();
  const idx = pages.findIndex(p => p.file === current);
  if (idx === -1) return;  // only show on the tracked pages

  const prev = pages[(idx - 1 + pages.length) % pages.length];
  const next = pages[(idx + 1) % pages.length];

  const css = document.createElement('style');
  css.textContent = `
    .pn{position:fixed;top:14px;right:14px;z-index:9999;display:flex;align-items:stretch;
      background:#fffdf9ee;backdrop-filter:blur(8px);
      border:1px solid rgba(0,0,0,.10);border-radius:999px;
      box-shadow:0 6px 20px rgba(120,80,40,.12),0 2px 4px rgba(120,80,40,.06);
      font-family:'Hanken Grotesk',system-ui,sans-serif;overflow:hidden}
    .pn a{padding:9px 14px;color:#5b4f42;font-weight:600;font-size:13px;text-decoration:none;
      display:inline-flex;align-items:center;gap:6px;transition:.13s background,.13s color}
    .pn a:hover{background:#0000000a;color:#36291d}
    .pn .pn-label{color:#9a8d7b;font-size:11px;font-weight:700;letter-spacing:.07em;
      text-transform:uppercase;padding:9px 12px}
    .pn .pn-label b{color:#36291d;font-weight:700;letter-spacing:0;text-transform:none;font-size:12.5px;margin-left:6px}
    .pn .pn-label:hover{background:#0000000a;color:#36291d}
    .pn .pn-sep{width:1px;background:rgba(0,0,0,.08)}
    .pn .pn-arrow{font-size:15px;line-height:1}
    @media print { .pn{display:none} }
  `;
  document.head.appendChild(css);

  function mkLink(href, title, parts) {
    const a = document.createElement('a');
    a.href = href;
    a.title = title;
    for (const p of parts) {
      if (typeof p === 'string') {
        a.appendChild(document.createTextNode(p));
      } else {
        const el = document.createElement(p.tag);
        if (p.cls) el.className = p.cls;
        el.textContent = p.text;
        a.appendChild(el);
      }
    }
    return a;
  }

  function mkSep() {
    const s = document.createElement('span');
    s.className = 'pn-sep';
    return s;
  }

  const nav = document.createElement('nav');
  nav.className = 'pn';
  nav.setAttribute('aria-label', 'Page navigation');

  nav.appendChild(mkLink(prev.file, 'Previous · ' + prev.label, [
    { tag: 'span', cls: 'pn-arrow', text: '←' }, ' Prev',
  ]));
  nav.appendChild(mkSep());

  const hub = mkLink('index.html', 'All pages', [(idx + 1) + '/' + pages.length]);
  hub.className = 'pn-label';
  const hubBold = document.createElement('b');
  hubBold.textContent = pages[idx].label;
  hub.appendChild(hubBold);
  nav.appendChild(hub);

  nav.appendChild(mkSep());
  nav.appendChild(mkLink(next.file, 'Next · ' + next.label, [
    'Next ', { tag: 'span', cls: 'pn-arrow', text: '→' },
  ]));

  document.body.appendChild(nav);
})();
