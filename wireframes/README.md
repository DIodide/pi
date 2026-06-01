# PI wireframes

Two fidelities:

- **`1/`** — low-fi **Excalidraw** wireframes (7 screens). Import the `.excalidraw`
  files into any Excalidraw viewer. Regenerate with `python3 wireframes/scripts/generate.py`.
- **`2/`** — high-fidelity **HTML** mockups built with the frontend-design skill.
  Open `2/index.html` in a browser (double-click works; for the nicest result serve it:
  `cd wireframes/2 && python3 -m http.server`, then visit `localhost:8000`).

## Design system (`2/styles.css`)
"TigerApps spirit": warm cream + gradient-blob atmosphere + grain, fully rounded, **coral
`#ff7151`** primary, per-app rainbow. Type: **Fraunces** (serif display, italic accents) +
**Hanken Grotesk** (body) + JetBrains Mono (metadata). Staggered load animations, hover lifts.

## Product principle: a *connector* chat app
PI is mostly chat. For "special" data it renders a rich inline card **styled to match the
target app's own look** (e.g. a live **TigerJunction** schedule in TJ blue/ReCal style,
**PrincetonCourses** course rows) — visibly *replacing* the raw tool call (`get_schedule()`,
`search_courses()`) — and then **links out** ("Open in TigerJunction ↗") for deep,
fine-grained work in the real app. Inline = cohesive preview; the app = power features.

## Screens (`2/`)
| File | Screen |
|------|--------|
| `index.html`     | Nav hub linking all mockups |
| `chat.html`      | **The core** — lens rail, chat-history sidebar (search / pin / rename / delete, grouped by date), real **chat turns** (user prompt → assistant), tool-call→custom render replacement, target-styled renders w/ deep-links, composer |
| `dashboard.html` | Home hub — greeting, Ask-PI launcher, Today / Degree / Seats / Campus tiles, **recent chats**; every card links out |
| `apps.html`      | The six TigerApp lenses + capabilities, jargon-free |
| `workflows.html` | Talk to several apps at once — scope tiers · app groups · cross-app asks |
| `proactive.html` | New feature — PI watches your apps and checks in each morning |
| `landing.html`   | Marketing front door |

Chat management lives in the chat sidebar **and** the dashboard's recent-chats tile.
