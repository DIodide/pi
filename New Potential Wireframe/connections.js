// Connections gear + profile.
// If the page has a left rail (.rrail), the gear and profile avatar are
// appended to the rail. Otherwise we fall back to the original floating
// widget in the bottom-left corner (used on pages without the rail).
(function () {
  if (document.getElementById('connections-widget')) return;
  if (document.getElementById('rrail-conn-gear')) return;

  const rail = document.querySelector('.rrail');
  const inRail = !!rail;

  // -------- SVG helpers --------
  const svgNS = 'http://www.w3.org/2000/svg';
  function mkSvg(paths) {
    const s = document.createElementNS(svgNS, 'svg');
    s.setAttribute('viewBox', '0 0 24 24');
    s.setAttribute('fill', 'none');
    s.setAttribute('stroke', 'currentColor');
    s.setAttribute('stroke-width', '2');
    s.setAttribute('stroke-linecap', 'round');
    s.setAttribute('stroke-linejoin', 'round');
    paths.forEach(p => {
      const el = document.createElementNS(svgNS, p.tag);
      Object.entries(p.attrs).forEach(([k, v]) => el.setAttribute(k, v));
      s.appendChild(el);
    });
    return s;
  }
  const gearSvg = () => mkSvg([
    { tag: 'circle', attrs: { cx: 12, cy: 12, r: 3 } },
    { tag: 'path', attrs: { d: 'M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 1 1-2.83 2.83l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 1 1-4 0v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 1 1-2.83-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 1 1 0-4h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 1 1 2.83-2.83l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 1 1 4 0v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 1 1 2.83 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 1 1 0 4h-.09a1.65 1.65 0 0 0-1.51 1z' } },
  ]);

  // -------- connections rollup data --------
  const apps = [
    { code: 'PC', name: 'Courses & evaluations',     desc: 'ratings, descriptions, reqs',  color: '#0a9cd5', on: true  },
    { code: 'TJ', name: 'Class schedule',            desc: 'build & edit your semester',   color: '#15b3c1', on: true  },
    { code: 'TP', name: 'Degree plan',               desc: 'track to graduate',            color: '#8b5cf6', on: true  },
    { code: 'TS', name: 'Seat alerts',               desc: 'watch full classes',           color: '#ec4899', on: true  },
    { code: 'TF', name: 'Campus events & listservs', desc: 'The Forum · free food',        color: '#f0a020', on: true  },
    { code: 'TM', name: 'Dining menus',              desc: "what's for dinner",            color: '#1f9d57', on: false },
  ];

  // -------- styles (only the floating-widget fallback lives here) --------
  if (!inRail) {
    const css = document.createElement('style');
    css.textContent = `
      #connections-widget{position:fixed;left:14px;bottom:14px;z-index:60;
        width:240px;background:#fffdf9ee;backdrop-filter:blur(8px);
        border:1px solid rgba(0,0,0,.08);border-radius:18px;
        box-shadow:0 8px 24px rgba(120,80,40,.12),0 2px 6px rgba(120,80,40,.06);
        padding:8px;display:flex;flex-direction:column;gap:4px;
        font-family:'Hanken Grotesk',system-ui,sans-serif}
      #connections-widget .cw-gear{display:flex;align-items:center;gap:10px;width:100%;
        padding:10px 12px;border-radius:12px;border:1px solid transparent;background:transparent;
        cursor:pointer;color:#5b4f42;font:600 13px/1 'Hanken Grotesk';text-align:left;
        transition:.13s background,.13s color,.13s border-color}
      #connections-widget .cw-gear:hover{background:#0000000a;color:#36291d}
      #connections-widget .cw-gear svg{width:17px;height:17px;flex:none}
      #connections-widget .cw-gear.active{background:#ffe7e0;color:#c63d1c;border-color:#0000000a}
      #connections-widget .cw-profile{display:flex;align-items:center;gap:10px;padding:6px 8px 4px}
      #connections-widget .cw-me{width:30px;height:30px;border-radius:50%;background:#ec4899;color:#fff;
        display:grid;place-items:center;font-weight:700;font-size:13px;flex:none}
      #connections-widget .cw-name{font-weight:600;font-size:13px;color:#36291d;line-height:1.15}
      #connections-widget .cw-mail{font-size:11px;color:#9a8d7b;margin-top:1px}
    `;
    document.head.appendChild(css);
  }

  // -------- rollup styles (shared) --------
  const rollupCss = document.createElement('style');
  rollupCss.textContent = `
    #cw-rollup{position:fixed;z-index:60;width:328px;max-width:calc(100vw - 28px);
      background:#fffdf9;border:1px solid #ece1d0;border-radius:20px;
      box-shadow:0 22px 50px rgba(120,80,40,.14);overflow:hidden;
      transform-origin:bottom left;transform:translateY(12px) scale(.94);
      opacity:0;visibility:hidden;
      transition:.22s transform cubic-bezier(.2,.9,.3,1.1),.18s opacity,.22s visibility}
    #cw-rollup.open{transform:translateY(0) scale(1);opacity:1;visibility:visible}
    #cw-rollup .cw-rh{display:flex;align-items:flex-start;padding:14px 16px 10px;
      border-bottom:1px solid #ece1d0;gap:10px}
    #cw-rollup .cw-rh-text{flex:1}
    #cw-rollup .cw-rh-title{font:600 14px/1.1 'Fraunces',Georgia,serif}
    #cw-rollup .cw-rh-sub{font-size:11.5px;color:#9a8d7b;margin-top:4px}
    #cw-rollup .cw-rh-info{width:40px;height:40px;border-radius:50%;border:2px solid #36291d;
      background:#dceefb;cursor:pointer;display:grid;place-items:center;
      font:700 18px/1 'Fraunces',Georgia,serif;color:#36291d;text-decoration:none;flex:none;
      transition:.15s background,.15s transform,.15s color}
    #cw-rollup .cw-rh-info:hover{background:#0a9cd5;color:#fff;transform:scale(1.06)}
    #cw-rollup .cw-list{padding:6px 8px 12px;max-height:340px;overflow:auto}
    #cw-rollup .cw-row{display:flex;align-items:center;gap:12px;padding:10px;border-radius:12px;
      transition:.13s background}
    #cw-rollup .cw-row:hover{background:#00000006}
    #cw-rollup .cw-sq{width:32px;height:32px;border-radius:30%;color:#fff;display:grid;place-items:center;
      font:800 12px/1 'Hanken Grotesk';flex:none;letter-spacing:-.02em}
    #cw-rollup .cw-text{flex:1;min-width:0}
    #cw-rollup .cw-name{font-weight:600;font-size:13.5px;color:#36291d}
    #cw-rollup .cw-desc{font-size:11.5px;color:#9a8d7b;margin-top:2px}
    #cw-rollup .cw-foot{padding:10px 16px 14px;border-top:1px solid #ece1d0;
      font-size:11.5px;color:#9a8d7b;text-align:center}
    #cw-rollup .cw-toggle{position:relative;width:38px;height:22px;flex:none;cursor:pointer;display:inline-block}
    #cw-rollup .cw-toggle input{opacity:0;width:0;height:0;position:absolute}
    #cw-rollup .cw-track{position:absolute;inset:0;background:#d8ccb6;border-radius:999px;transition:.18s background}
    #cw-rollup .cw-knob{position:absolute;top:2px;left:2px;width:18px;height:18px;background:#fff;border-radius:50%;
      box-shadow:0 1px 3px rgba(0,0,0,.18);transition:.2s transform}
    #cw-rollup .cw-toggle input:checked + .cw-track{background:#ff7151}
    #cw-rollup .cw-toggle input:checked + .cw-track + .cw-knob{transform:translateX(16px)}
  `;
  document.head.appendChild(rollupCss);

  // -------- build the gear + profile --------
  let gear, avatar, profilePop;

  if (inRail) {
    const foot = document.createElement('div');
    foot.className = 'rrail-foot';

    // Calendars button (above Connections)
    const calBtn = document.createElement('button');
    calBtn.id = 'rrail-cal-btn';
    calBtn.className = 'rrail-btn';
    calBtn.setAttribute('aria-label', 'Calendars');
    calBtn.setAttribute('aria-expanded', 'false');
    const calSvg = document.createElementNS(svgNS, 'svg');
    calSvg.setAttribute('viewBox', '0 0 24 24');
    calSvg.setAttribute('fill', 'none');
    calSvg.setAttribute('stroke', 'currentColor');
    calSvg.setAttribute('stroke-width', '2');
    calSvg.setAttribute('stroke-linecap', 'round');
    calSvg.setAttribute('stroke-linejoin', 'round');
    [
      { tag: 'rect', attrs: { x: 3, y: 4, width: 18, height: 18, rx: 2, ry: 2 } },
      { tag: 'line', attrs: { x1: 16, y1: 2, x2: 16, y2: 6 } },
      { tag: 'line', attrs: { x1: 8,  y1: 2, x2: 8,  y2: 6 } },
      { tag: 'line', attrs: { x1: 3,  y1: 10, x2: 21, y2: 10 } },
    ].forEach(p => {
      const el = document.createElementNS(svgNS, p.tag);
      Object.entries(p.attrs).forEach(([k, v]) => el.setAttribute(k, v));
      calSvg.appendChild(el);
    });
    calBtn.appendChild(calSvg);
    const calLabel = document.createElement('span');
    calLabel.textContent = 'Calendars';
    calBtn.appendChild(calLabel);
    foot.appendChild(calBtn);

    gear = document.createElement('button');
    gear.id = 'rrail-conn-gear';
    gear.className = 'rrail-btn';
    gear.setAttribute('aria-label', 'Connections');
    gear.setAttribute('aria-expanded', 'false');
    gear.appendChild(gearSvg());
    const gLabel = document.createElement('span');
    gLabel.textContent = 'Connections';
    gear.appendChild(gLabel);
    foot.appendChild(gear);

    avatar = document.createElement('button');
    avatar.id = 'rrail-conn-me';
    avatar.className = 'rrail-me';
    avatar.setAttribute('aria-label', 'Geraldine W. — account');
    avatar.setAttribute('aria-expanded', 'false');
    avatar.textContent = 'G';
    foot.appendChild(avatar);

    rail.appendChild(foot);

    // profile popup
    profilePop = document.createElement('div');
    profilePop.className = 'rrail-pop';
    profilePop.id = 'rrail-conn-pop';
    profilePop.setAttribute('role', 'dialog');
    profilePop.setAttribute('aria-label', 'Account');
    const ppRow = document.createElement('div');
    ppRow.className = 'pp-row';
    const ppAv = document.createElement('div');
    ppAv.className = 'pp-av';
    ppAv.textContent = 'G';
    const ppId = document.createElement('div');
    const ppName = document.createElement('div');
    ppName.className = 'pp-name';
    ppName.textContent = 'Geraldine W.';
    const ppMail = document.createElement('div');
    ppMail.className = 'pp-mail';
    ppMail.textContent = 'geraldine@princeton.edu';
    ppId.appendChild(ppName);
    ppId.appendChild(ppMail);
    ppRow.appendChild(ppAv);
    ppRow.appendChild(ppId);
    profilePop.appendChild(ppRow);
    profilePop.appendChild(document.createElement('hr'));
    ['Account settings', 'Notifications', 'Sign out'].forEach(label => {
      const link = document.createElement('a');
      link.className = 'pp-link';
      link.href = '#';
      link.textContent = label;
      profilePop.appendChild(link);
    });
    document.body.appendChild(profilePop);
  } else {
    // floating widget fallback (pages without a rail)
    const widget = document.createElement('div');
    widget.id = 'connections-widget';

    gear = document.createElement('button');
    gear.className = 'cw-gear';
    gear.setAttribute('aria-label', 'Connections');
    gear.setAttribute('aria-expanded', 'false');
    gear.appendChild(gearSvg());
    gear.appendChild(document.createTextNode(' Connections'));
    widget.appendChild(gear);

    const profile = document.createElement('div');
    profile.className = 'cw-profile';
    const av = document.createElement('div');
    av.className = 'cw-me';
    av.textContent = 'G';
    const idBlock = document.createElement('div');
    const nm = document.createElement('div');
    nm.className = 'cw-name';
    nm.textContent = 'Geraldine W.';
    const ml = document.createElement('div');
    ml.className = 'cw-mail';
    ml.textContent = 'geraldine@princeton.edu';
    idBlock.appendChild(nm);
    idBlock.appendChild(ml);
    profile.appendChild(av);
    profile.appendChild(idBlock);
    widget.appendChild(profile);

    document.body.appendChild(widget);
  }

  // -------- calendars popup (rail-only feature) --------
  let calBtn = null, calPop = null;
  if (inRail) {
    calBtn = document.getElementById('rrail-cal-btn');
    calPop = document.createElement('div');
    calPop.className = 'cal-pop';
    calPop.id = 'cal-pop';
    calPop.setAttribute('role', 'dialog');
    calPop.setAttribute('aria-label', 'Calendars');

    const head = document.createElement('div');
    head.className = 'cal-head';
    const ht = document.createElement('div');
    ht.className = 'cal-head-title';
    ht.textContent = 'Calendars';
    const hs = document.createElement('div');
    hs.className = 'cal-head-sub';
    hs.textContent = 'Sync events to and from PI — pick what to share.';
    head.appendChild(ht);
    head.appendChild(hs);
    calPop.appendChild(head);

    const body = document.createElement('div');
    body.className = 'cal-body';

    function mkSection(titleText, lgBg, lgChar) {
      const sec = document.createElement('div');
      sec.className = 'cal-section';
      const title = document.createElement('div');
      title.className = 'cal-sec-title';
      const lg = document.createElement('span');
      lg.className = 'lg';
      lg.style.background = lgBg;
      lg.textContent = lgChar;
      title.appendChild(lg);
      title.appendChild(document.createTextNode(titleText));
      sec.appendChild(title);
      return sec;
    }
    function mkRow(email, sub, avBg, avChar) {
      const row = document.createElement('div');
      row.className = 'cal-row';
      const av = document.createElement('div');
      av.className = 'av';
      av.style.background = avBg;
      av.textContent = avChar;
      const who = document.createElement('div');
      who.className = 'who';
      const b = document.createElement('b');
      b.textContent = email;
      const small = document.createElement('small');
      small.textContent = sub;
      who.appendChild(b);
      who.appendChild(small);
      const tog = document.createElement('label');
      tog.className = 'toggle';
      const cb = document.createElement('input');
      cb.type = 'checkbox';
      cb.checked = true;
      const track = document.createElement('span');
      track.className = 'track';
      const knob = document.createElement('span');
      knob.className = 'knob';
      tog.appendChild(cb);
      tog.appendChild(track);
      tog.appendChild(knob);
      row.appendChild(av);
      row.appendChild(who);
      row.appendChild(tog);
      return row;
    }
    function mkAdd(text) {
      const b = document.createElement('button');
      b.type = 'button';
      b.className = 'cal-add';
      b.textContent = text;
      return b;
    }

    const google = mkSection('Google Calendar', '#1a73e8', 'G');
    google.appendChild(mkRow('geraldine@princeton.edu', 'Princeton · default', '#1a73e8', 'G'));
    google.appendChild(mkRow('g.wong@gmail.com',        'Personal',            '#1a73e8', 'G'));
    google.appendChild(mkAdd('+ Add another Google account'));
    body.appendChild(google);

    const apple = mkSection('Apple Calendar', '#000', '');
    apple.appendChild(mkAdd('+ Connect Apple Calendar (iCloud)'));
    body.appendChild(apple);

    calPop.appendChild(body);

    const calFoot = document.createElement('div');
    calFoot.className = 'cal-foot';
    calFoot.textContent = 'PI never moves events without your OK.';
    calPop.appendChild(calFoot);

    document.body.appendChild(calPop);
  }

  // -------- rollup --------
  const rollup = document.createElement('div');
  rollup.id = 'cw-rollup';
  rollup.setAttribute('role', 'dialog');
  rollup.setAttribute('aria-label', 'App connections');

  const head = document.createElement('div');
  head.className = 'cw-rh';
  const headText = document.createElement('div');
  headText.className = 'cw-rh-text';
  const headTitle = document.createElement('div');
  headTitle.className = 'cw-rh-title';
  headTitle.textContent = 'Connections';
  const headSub = document.createElement('div');
  headSub.className = 'cw-rh-sub';
  headSub.textContent = 'What PI can see for you. All on by default.';
  headText.appendChild(headTitle);
  headText.appendChild(headSub);
  const info = document.createElement('a');
  info.className = 'cw-rh-info';
  info.href = 'apps.html';
  info.title = 'Learn what each app does';
  info.textContent = 'i';
  head.appendChild(headText);
  head.appendChild(info);
  rollup.appendChild(head);

  const list = document.createElement('div');
  list.className = 'cw-list';
  apps.forEach(app => {
    const row = document.createElement('div');
    row.className = 'cw-row';
    const sq = document.createElement('span');
    sq.className = 'cw-sq';
    sq.textContent = app.code;
    sq.style.background = app.color;
    const text = document.createElement('div');
    text.className = 'cw-text';
    const nm = document.createElement('div');
    nm.className = 'cw-name';
    nm.textContent = app.name;
    const ds = document.createElement('div');
    ds.className = 'cw-desc';
    ds.textContent = app.desc;
    text.appendChild(nm);
    text.appendChild(ds);
    const tog = document.createElement('label');
    tog.className = 'cw-toggle';
    const cb = document.createElement('input');
    cb.type = 'checkbox';
    if (app.on) cb.checked = true;
    const track = document.createElement('span');
    track.className = 'cw-track';
    const knob = document.createElement('span');
    knob.className = 'cw-knob';
    tog.appendChild(cb);
    tog.appendChild(track);
    tog.appendChild(knob);
    row.appendChild(sq);
    row.appendChild(text);
    row.appendChild(tog);
    list.appendChild(row);
  });
  rollup.appendChild(list);

  const foot = document.createElement('div');
  foot.className = 'cw-foot';
  foot.textContent = 'No tokens, no "MCP" — just toggle what PI can see.';
  rollup.appendChild(foot);

  document.body.appendChild(rollup);

  // anchor the rollup
  if (inRail) {
    rollup.style.left   = '96px';
    rollup.style.bottom = '14px';
  } else {
    rollup.style.left   = '14px';
    rollup.style.bottom = '130px';
  }

  // -------- interaction --------
  function closeRollup() {
    rollup.classList.remove('open');
    gear.classList.remove('active');
    gear.setAttribute('aria-expanded', 'false');
  }
  function closeProfile() {
    if (!profilePop) return;
    profilePop.classList.remove('open');
    avatar.classList.remove('active');
    avatar.setAttribute('aria-expanded', 'false');
  }
  function closeCal() {
    if (!calPop) return;
    calPop.classList.remove('open');
    calBtn.classList.remove('active');
    calBtn.setAttribute('aria-expanded', 'false');
  }
  function closeAll() { closeRollup(); closeProfile(); closeCal(); }

  gear.addEventListener('click', (e) => {
    e.stopPropagation();
    closeProfile(); closeCal();
    const open = rollup.classList.toggle('open');
    gear.classList.toggle('active', open);
    gear.setAttribute('aria-expanded', open ? 'true' : 'false');
  });

  if (avatar && profilePop) {
    avatar.addEventListener('click', (e) => {
      e.stopPropagation();
      closeRollup(); closeCal();
      const open = profilePop.classList.toggle('open');
      avatar.classList.toggle('active', open);
      avatar.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  if (calBtn && calPop) {
    calBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      closeRollup(); closeProfile();
      const open = calPop.classList.toggle('open');
      calBtn.classList.toggle('active', open);
      calBtn.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
  }

  document.addEventListener('click', (e) => {
    if (!gear.contains(e.target) && !rollup.contains(e.target)) closeRollup();
    if (profilePop && !avatar.contains(e.target) && !profilePop.contains(e.target)) closeProfile();
    if (calPop && !calBtn.contains(e.target) && !calPop.contains(e.target)) closeCal();
  });
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeAll();
  });
})();
