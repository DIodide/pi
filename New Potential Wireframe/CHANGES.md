# What Has Changed

## TL;DR

The nav rail no longer lists every TigerApp — it lists product destinations (**Dashboard / Chat / For you**), with **Calendars**, **Connections**, and the user's avatar pinned to the bottom. The dashboard's ask bar is now a real input that hands the prompt off to the chat page. Chat gained **import / export**, lost the "Quick starts" trio, and the suggested prompts stack vertically. **Calendars** is new — multi-account Google + Apple. **Workflows** as a separate page is gone; its content folded into the chat new-chat picker. A small **"Add a TigerApp"** tile lets users grow their dashboard.

---

## User flow — what's different

- **Rail is product-level, not app-level.** Old rail = seven TigerApp lenses. New rail = Dashboard, Chat, For you (each page shows the other two). TigerApps moved into Connections and into "Open in …" buttons on cards.
- **Dashboard → Chat handoff.** Typing in the dashboard ask bar and hitting Enter (or ↑) navigates to `chat.html?q=…`. Chat opens its new-chat picker with the prompt pre-filled in the composer.
- **Connections + identity moved into the rail.** No more floating "Connections / Geraldine W." card in the bottom-left corner. Click the gear → app toggles. Click the `G` avatar → name, email, account links.
- **New-chat page is leaner.** The three "Quick starts" cards (Course Planning / Campus Life / Stay on Track) are gone. Just intro + a vertical list of suggested prompts.
- **Workflows page deleted.** Anything users reached via Workflows is now reached from the chat new-chat picker.

---

## New features

- **Calendars** (new rail item, above Connections). Popup supports multiple Google accounts (`+ Add another Google account`) and Apple Calendar / iCloud. Per-account on/off toggles. Footer: "PI never moves events without your OK."
- **Export this chat** (chat topbar, ↓ icon). Downloads the current chat as `pi-<slug>.json` with title + turns.
- **Import chats** (chat topbar, ↑ icon). Multi-file `.json` picker. Reports count via toast.
- **Add a TigerApp** tile on the dashboard. Dashed ghost tile, links to the Apps page so users can browse and connect more.
- **Profile popover.** Click `G` → small popover with name, email, Account settings / Notifications / Sign out.

---

## Notes for the design team

- Coral is still the only brand color. New accent chips (Google blue, Apple black) appear inside the Calendars popup only.
- The three rail popovers (Calendars / Connections / profile) share the same animation, shadow, radius, and anchor (`left:96px; bottom:14px`). Worth documenting as one component.
- The rail has an `.active` state already styled but not applied — designers should decide whether the current page's rail link should be marked.
- Apple Calendar's logo chip is currently a black square with no glyph. Needs a real mark before review.
- Toast is the canonical success/info channel (used by toggles, undo, import, export).
