#!/usr/bin/env python3
"""Princeton Intelligence (PI) wireframes — v3.

Design language (from the FORUM dashboard): warm cream + soft pastel gradient blobs,
fully ROUNDED cards/pills, coral-red primary (#ff7151), a per-app rainbow, friendly
personal greetings.  roughness=0 => clean render.

Product model — apps as branded "lenses": every TigerApp is a chattable surface with
its own color + REAL name (PrincetonCourses, TigerJunction, TigerPath, TigerSnatch,
The Forum, TigerMenus). Users chat with EVERYTHING (PI routes across all MCP tools),
a GROUP (a curated several-app scope), or ONE app (focus, docks its live data).

Outputs .excalidraw files into the parent wireframes/ dir.
Run:  python3 wireframes/scripts/generate.py
"""
import json, math, os, random
random.seed(11)
HERE = os.path.dirname(os.path.abspath(__file__))
OUT  = os.path.join(os.path.dirname(HERE), "1")        # -> wireframes/1/

# ---- warm palette (FORUM) ------------------------------------------------
BG     = "#fbf6ee"; CARD = "#ffffff"
INK    = "#3a2f24"; MUT = "#8c8175"; LINE = "#ece3d6"
CORAL  = "#ff7151"; CORAL_T = "#ffe7e0"        # PI / Everything
CERU   = "#0a9cd5"; CERU_T  = "#d8eef9"        # PrincetonCourses
TURQ   = "#15b3c1"; TURQ_T  = "#d6f3f5"        # TigerJunction
PURPLE = "#8b5cf6"; PURPLE_T= "#ece4fd"        # TigerPath
MAG    = "#ec4899"; MAG_T   = "#fbe0ef"        # TigerSnatch
AMBER  = "#f3a712"; AMBER_T = "#fdeccc"        # The Forum
GREEN  = "#1f9d57"; GREEN_T = "#dcf2e4"        # TigerMenus
YELLOW = "#fee882"; PINK = "#ffd3ea"; SKY = "#a2eff0"; WHITE = "#ffffff"
UI = 2                                          # clean sans (real build: serif display)

# lens: (real name, badge, color, tint, blurb, example, rail-label)
APPS = [
    ("Everything",       "π",  CORAL,  CORAL_T,  "all your apps, one chat",       "Plan my whole spring",        "Everything"),
    ("PrincetonCourses", "PC", CERU,   CERU_T,   "courses & evaluations",         "Best-rated COS electives?",   "Courses"),
    ("TigerJunction",    "TJ", TURQ,   TURQ_T,   "build your schedule",           "Add COS 226 to my schedule",  "Junction"),
    ("TigerPath",        "TP", PURPLE, PURPLE_T, "4-year plan & requirements",    "What do I still need?",       "TigerPath"),
    ("TigerSnatch",      "TS", MAG,    MAG_T,    "a seat when one opens",         "Ping me when ECO 100 opens",  "Snatch"),
    ("The Forum",        "TF", AMBER,  AMBER_T,  "events · listservs · free food","Any free food right now?",    "Forum"),
    ("TigerMenus",       "TM", GREEN,  GREEN_T,  "dining hall menus",             "What's for dinner tonight?",  "Menus"),
]
NAME, BADGE, COLOR, TINT, BLURB, EX, RAIL = range(7)

# curated several-app scopes ("talk to a few apps at once")
GROUPS = [
    ("Course Planning", "assemble next semester, end to end", [1, 2, 3, 4], TURQ),
    ("Campus Life",     "food, events & what's happening",    [5, 6],       AMBER),
    ("Stay on Track",   "keep your degree plan moving",       [3, 2, 4],    PURPLE),
]

CAPS = {
    "PrincetonCourses": ["Search & compare courses", "Read evaluations & ratings", "Look up instructors & top-rated"],
    "TigerJunction":    ["Build & edit your schedule", "Check for time conflicts", "Find courses that fit"],
    "TigerPath":        ["Track requirements left", "Your four-year plan", "When students take a course"],
    "TigerSnatch":      ["Get a seat when one opens", "See how competitive a class is", "Trending hard-to-get courses"],
    "The Forum":        ["What's happening this week", "Free food right now", "Summarize your listservs"],
    "TigerMenus":       ["Today's dining hall menus", "Find dishes & dietary options", "What's for dinner tonight"],
}

# ---- element helpers -----------------------------------------------------
def _rid():  return "".join(random.choices("abcdefghijklmnopqrstuvwxyz0123456789", k=18))
def _seed(): return random.randint(1, 2**31)

def _base(t, x, y, w, h, stroke=INK, bg="transparent", fill="solid", sw=1, ss="solid",
          rough=0, opacity=100, rounded=False):
    return {"id": _rid(), "type": t, "x": float(x), "y": float(y), "width": float(w),
            "height": float(h), "angle": 0, "strokeColor": stroke, "backgroundColor": bg,
            "fillStyle": fill, "strokeWidth": sw, "strokeStyle": ss, "roughness": rough,
            "opacity": opacity, "groupIds": [], "frameId": None,
            "roundness": ({"type": 3} if rounded else None), "seed": _seed(), "version": 1,
            "versionNonce": _seed(), "isDeleted": False, "boundElements": None,
            "updated": 1717000000000, "link": None, "locked": False}

def rect(x, y, w, h, rounded=True, **kw):  return _base("rectangle", x, y, w, h, rounded=rounded, **kw)
def ellipse(x, y, w, h, **kw):             return _base("ellipse", x, y, w, h, **kw)

def text(x, y, s, size=15, color=INK, align="left", w=None, family=UI):
    lines = s.split("\n")
    if w is None: w = max(len(l) for l in lines) * size * 0.56 + 6
    e = _base("text", x, y, w, len(lines) * size * 1.25, stroke=color)
    e.update({"text": s, "fontSize": size, "fontFamily": family, "textAlign": align,
              "verticalAlign": "top", "containerId": None, "originalText": s,
              "autoResize": True, "lineHeight": 1.25})
    return e

def ctext(box, s, size=15, color=INK, family=UI):
    x, y, w, h = box
    th = len(s.split("\n")) * size * 1.25
    return text(x, y + (h - th) / 2, s, size=size, color=color, align="center", w=w, family=family)

def line(pts, stroke=LINE, sw=1, ss="solid", arrow=False):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    x0, y0 = min(xs), min(ys)
    e = _base("arrow" if arrow else "line", x0, y0, max(xs)-x0, max(ys)-y0, stroke=stroke, sw=sw, ss=ss)
    e.update({"points": [[p[0]-x0, p[1]-y0] for p in pts], "lastCommittedPoint": None,
              "startBinding": None, "endBinding": None, "startArrowhead": None,
              "endArrowhead": ("triangle" if arrow else None)})
    return e

# ---- components ----------------------------------------------------------
def blob(o, x, y, w, h, color, op=45):
    o.append(ellipse(x, y, w, h, bg=color, stroke="transparent", fill="solid", opacity=op))

def card(o, x, y, w, h, fill=CARD, stroke=LINE, sw=1):
    o.append(rect(x, y, w, h, bg=fill, stroke=stroke, sw=sw, fill="solid"))

def pill(o, x, y, label, bg=CORAL, fg=WHITE, size=12, h=28, padx=14):
    w = len(label) * size * 0.6 + padx * 2
    o.append(rect(x, y, w, h, bg=bg, stroke="transparent", fill="solid"))
    o.append(ctext((x, y, w, h), label, size=size, color=fg)); return w

def button(o, x, y, w, h, label, color=CORAL, fg=WHITE, ghost=False, size=14):
    o.append(rect(x, y, w, h, bg=("transparent" if ghost else color),
                  stroke=(color if ghost else "transparent"), fill="solid"))
    o.append(ctext((x, y, w, h), label, size=size, color=(color if ghost else fg)))

def squircle(o, x, y, d, color, letter, fg=WHITE, size=None):
    o.append(rect(x, y, d, d, bg=color, stroke="transparent", fill="solid"))
    o.append(ctext((x, y, d, d), letter, size=size or int(d*0.42), color=fg,
                   family=(3 if letter == "π" else UI)))

def avatar(o, x, y, d, color, initial):
    o.append(ellipse(x, y, d, d, bg=color, stroke="transparent", fill="solid"))
    o.append(ctext((x, y, d, d), initial, size=int(d*0.42), color=WHITE))

def progress(o, x, y, w, frac, color):
    o.append(rect(x, y, w, 8, bg=LINE, stroke="transparent", fill="solid"))
    o.append(rect(x, y, max(8, w*frac), 8, bg=color, stroke="transparent", fill="solid"))

def app_rail(o, x, y, h, active=0):
    w = 92
    card(o, x, y, w, h, fill=CARD)
    squircle(o, x + 26, y + 18, 40, CORAL, "π", size=20)
    o.append(text(x + 16, y + 62, "PI", size=12, color=INK))
    yy = y + 96
    for i, a in enumerate(APPS):
        if i == active:
            o.append(rect(x + 8, yy - 8, w - 16, 64, bg=a[TINT], stroke="transparent", fill="solid"))
            o.append(rect(x, yy - 8, 4, 64, bg=a[COLOR], stroke="transparent", fill="solid"))
        squircle(o, x + 26, yy, 40, a[COLOR], a[BADGE], size=14)
        o.append(ctext((x, yy + 42, w, 14), a[RAIL], size=10, color=(INK if i == active else MUT)))
        yy += 70
    avatar(o, x + 26, y + h - 56, 40, MAG, "G")
    return x + w

def focus_chip(o, x, y, app_idx):
    a = APPS[app_idx]
    o.append(text(x, y + 7, "Chatting with", size=12, color=MUT))
    bx = x + 110
    w = len(a[NAME]) * 13 * 0.6 + 64
    o.append(rect(bx, y, w, 30, bg=a[TINT], stroke="transparent", fill="solid"))
    squircle(o, bx + 6, y + 5, 20, a[COLOR], a[BADGE], size=10)
    o.append(text(bx + 32, y + 7, a[NAME], size=13, color=INK))
    o.append(text(bx + w - 18, y + 7, "⌄", size=13, color=MUT))
    return bx + w

def course_card(o, x, y, w, code, title, rating, dist, status, seats, meta, tags):
    h = 104
    card(o, x, y, w, h)
    o.append(rect(x, y, 5, h, bg=CERU, stroke="transparent", fill="solid"))
    o.append(text(x + 22, y + 16, code, size=19, color=INK))
    o.append(text(x + 22, y + 45, title, size=14, color=INK))
    o.append(text(x + 22, y + 70, meta, size=11, color=MUT))
    tx = x + 22
    for (lab, col, til) in tags:
        wlab = len(lab) * 10 * 0.6 + 18
        o.append(rect(tx, y + 86, wlab, 18, bg=til, stroke="transparent", fill="solid"))
        o.append(ctext((tx, y + 86, wlab, 18), lab, size=10, color=col)); tx += wlab + 8
    cb = x + w - 250
    o.append(text(cb, y + 16, f"★ {rating}", size=16, color=AMBER))
    wd = len(dist) * 11 * 0.6 + 18
    o.append(rect(cb, y + 44, wd, 20, bg=CERU_T, stroke="transparent", fill="solid"))
    o.append(ctext((cb, y + 44, wd, 20), dist, size=11, color=CERU))
    rb = x + w - 150
    if status == "Open": pill(o, rb, y + 14, f"● Open · {seats}", bg=GREEN_T, fg=GREEN, size=11, h=24)
    else:                pill(o, rb, y + 14, "● Full", bg=MAG_T, fg=MAG, size=11, h=24)
    button(o, rb, y + 52, 120, 32, ("+ Add" if status == "Open" else "Watch seat"),
           color=(TURQ if status == "Open" else MAG), size=12)
    return h

def schedule_panel(o, x, y, w, h, blocks, title="Spring 2026"):
    card(o, x, y, w, h)
    o.append(text(x + 18, y + 14, title, size=14, color=INK))
    o.append(text(x + w - 90, y + 16, "via Junction", size=11, color=MUT))
    gx, gy = x + 14, y + 44; gw, gh = w - 28, h - 58
    gutter, header = 38, 26; days = ["M", "T", "W", "Th", "F"]; colw = (gw - gutter) / 5
    for i, d in enumerate(days):
        cx = gx + gutter + i * colw
        o.append(ctext((cx, gy, colw, header - 4), d, size=11, color=MUT))
        if i: o.append(line([(cx, gy + header), (cx, gy + gh)], stroke=LINE))
    o.append(line([(gx, gy + header), (gx + gw, gy + header)], stroke=LINE))
    rows = 9; rh = (gh - header) / rows
    for r in range(rows):
        ry = gy + header + r * rh
        o.append(text(gx, ry + 3, f"{9+r}", size=9, color=MUT))
        if r: o.append(line([(gx + gutter, ry), (gx + gw, ry)], stroke="#f4efe6"))
    for (day, start, dur, code, room, col, til) in blocks:
        bx = gx + gutter + day * colw + 2; by = gy + header + start * rh + 1
        bw, bh = colw - 4, dur * rh - 2
        o.append(rect(bx, by, bw, bh, bg=til, stroke="transparent", fill="solid"))
        o.append(rect(bx, by, 3, bh, bg=col, stroke="transparent", fill="solid"))
        o.append(text(bx + 7, by + 5, code, size=10, color=INK))
        if room: o.append(text(bx + 7, by + 19, room, size=8, color=MUT))

def callout(o, x, y, label, tip=None, color=CORAL):
    w = max(len(l) for l in label.split("\n")) * 11 * 0.6 + 22
    h = len(label.split("\n")) * 11 * 1.25 + 14
    o.append(rect(x, y, w, h, stroke=color, ss="dashed", bg="#fffaf6", fill="solid"))
    o.append(text(x + 11, y + 7, label, size=11, color=color))
    if tip: o.append(line([(x + w/2, y + h), tip], stroke=color, sw=1.5, ss="dashed", arrow=True))

def dump(name, o):
    json.dump({"type": "excalidraw", "version": 2, "source": "https://princeton-intelligence",
               "elements": o, "appState": {"gridSize": None, "viewBackgroundColor": BG},
               "files": {}}, open(os.path.join(OUT, name), "w"), indent=2)
    print(f"wrote {name}: {len(o)} elements")

# =========================================================================
# 1. LANDING
# =========================================================================
def build_landing():
    o = []; W = 1440
    o.append(rect(0, 0, W, 2180, bg=BG, stroke="transparent", fill="solid", rounded=False))
    o.append(rect(0, 0, W, 720, bg="#fff1ea", stroke="transparent", fill="solid", rounded=False))
    blob(o, W - 520, -160, 620, 560, CORAL, 35); blob(o, W - 280, 120, 360, 360, YELLOW, 40)
    blob(o, -160, 360, 420, 380, PINK, 35)
    squircle(o, 80, 40, 38, CORAL, "π", size=19)
    o.append(text(128, 49, "Princeton Intelligence", size=16, color=INK))
    for i, l in enumerate(["How it works", "Apps", "For TigerApps"]):
        o.append(text(720 + i*150, 50, l, size=13, color=INK))
    o.append(text(W - 230, 50, "Sign in", size=13, color=INK))
    button(o, W - 160, 38, 130, 40, "Get started", color=CORAL)
    o.append(text(80, 190, "Your whole campus,", size=58, color=INK))
    o.append(text(80, 262, "one conversation.", size=58, color=CORAL))
    o.append(text(82, 360, "Chat with every TigerApp — PrincetonCourses, TigerJunction, TigerPath,\n"
                  "TigerSnatch and The Forum — together, in plain English.", size=17, color=MUT))
    button(o, 82, 452, 250, 52, "Continue with NetID  →", color=CORAL, size=15)
    button(o, 348, 452, 150, 52, "See a demo", color=INK, ghost=True, size=15)
    o.append(text(82, 530, "Sign in with your princeton.edu NetID · built by TigerApps", size=12, color=MUT))
    mx, my = 880, 150
    card(o, mx, my, 470, 420)
    o.append(rect(mx, my, 470, 46, bg=CORAL_T, stroke="transparent", fill="solid"))
    squircle(o, mx + 14, my + 9, 28, CORAL, "π", size=14)
    o.append(text(mx + 52, my + 15, "Ask PI · Everything", size=13, color=INK))
    pill(o, mx + 24, my + 70, "Build me a balanced spring schedule", bg=CORAL, size=12, h=30)
    o.append(text(mx + 24, my + 120, "Looked across your apps:", size=11, color=MUT))
    o.append(text(mx + 24, my + 140, "✓ Courses  ✓ Junction  ✓ TigerPath  ✓ Snatch", size=11, color=CORAL))
    for i, (code, c) in enumerate([("COS 226", CERU), ("ECO 100", TURQ), ("MAT 202", PURPLE)]):
        cy = my + 170 + i*78; card(o, mx + 24, cy, 420, 66)
        o.append(rect(mx + 24, cy, 4, 66, bg=c, stroke="transparent", fill="solid"))
        o.append(text(mx + 40, cy + 12, code, size=14, color=INK))
        o.append(text(mx + 40, cy + 36, "★ 4.3 · QCR · 12 seats open", size=10, color=MUT))
        button(o, mx + 340, cy + 18, 70, 30, "Add", color=TURQ, size=11)
    # section 2
    o.append(rect(0, 720, W, 740, bg="#e9fafb", stroke="transparent", fill="solid", rounded=False))
    blob(o, -120, 760, 460, 420, SKY, 50); blob(o, W - 360, 1180, 420, 360, PINK, 35)
    o.append(text(80, 800, "FOR STUDENTS", size=12, color=TURQ))
    o.append(text(80, 824, "Chat with one app —", size=46, color=INK))
    o.append(text(80, 884, "or all of them at once.", size=46, color=TURQ))
    o.append(text(82, 968, "Pick a lens to focus, or let PI route across everything.", size=16, color=MUT))
    for i, a in enumerate(APPS):
        x = 80 + (i % 3) * 440; y = 1050 + (i // 3) * 180
        card(o, x, y, 408, 150)
        squircle(o, x + 22, y + 22, 44, a[COLOR], a[BADGE], size=17)
        o.append(text(x + 80, y + 26, a[NAME], size=17, color=INK))
        o.append(text(x + 80, y + 52, a[BLURB], size=12, color=MUT))
        o.append(rect(x + 22, y + 96, 364, 34, bg=a[TINT], stroke="transparent", fill="solid"))
        o.append(text(x + 36, y + 105, f"“{a[EX]}”", size=12, color=a[COLOR]))
    # section 3
    o.append(rect(0, 1460, W, 720, bg=CORAL, stroke="transparent", fill="solid", rounded=False))
    blob(o, W - 420, 1500, 460, 460, YELLOW, 35); blob(o, -120, 1820, 420, 380, PINK, 30)
    o.append(text(80, 1600, "From “what should I take?”", size=50, color=WHITE))
    o.append(text(80, 1664, "to done — in one chat.", size=50, color="#fff0ea"))
    o.append(text(82, 1760, "PI reads your degree plan on TigerPath, checks ratings & conflicts,\n"
                  "finds open seats via TigerSnatch, and writes it to TigerJunction.", size=17, color="#fff0ea"))
    button(o, 82, 1880, 240, 54, "Continue with NetID  →", color=WHITE, fg=CORAL, size=15)
    o.append(text(82, 1960, "Princeton Intelligence · a TigerApps project", size=12, color="#ffe7e0"))
    dump("homepage.excalidraw", o)

# =========================================================================
# 2. DASHBOARD
# =========================================================================
def build_dashboard():
    o = []; W, H = 1500, 1020
    o.append(rect(-40, -40, W + 80, H + 80, bg=BG, stroke="transparent", fill="solid", rounded=False))
    blob(o, W - 360, -120, 460, 420, CORAL, 22); blob(o, -160, H - 360, 420, 420, SKY, 30)
    rail_r = app_rail(o, 24, 24, H - 48, active=0)
    mx = rail_r + 28; mw = W - mx - 28
    o.append(text(mx, 40, "Hi Geraldine,", size=34, color=INK))
    o.append(text(mx + 2, 86, "Tuesday, 31 March · course selection opens in 6 days", size=14, color=MUT))
    avatar(o, W - 64, 40, 44, MAG, "G")
    o.append(rect(W - 124, 46, 36, 36, bg=CARD, stroke=LINE, fill="solid"))
    o.append(ctext((W - 124, 46, 36, 36), "◔", size=16, color=MUT))
    ay = 124; card(o, mx, ay, mw, 66, stroke=CORAL, sw=2)
    squircle(o, mx + 16, ay + 15, 36, CORAL, "π", size=18)
    o.append(text(mx + 64, ay + 24, "Ask PI anything across your campus…", size=15, color=MUT))
    pill(o, mx + mw - 210, ay + 18, "Everything ⌄", bg=CORAL_T, fg=CORAL, size=12, h=30)
    o.append(rect(mx + mw - 64, ay + 15, 36, 36, bg=CORAL, stroke="transparent", fill="solid"))
    o.append(ctext((mx + mw - 64, ay + 15, 36, 36), "↑", size=16, color=WHITE))
    gy = 218; colw = (mw - 24) * 0.62
    rcolx = mx + colw + 24; rcolw = mw - colw - 24
    # Today (Junction)
    card(o, mx, gy, colw, 250); o.append(rect(mx, gy, 5, 250, bg=TURQ, stroke="transparent", fill="solid"))
    o.append(text(mx + 22, gy + 16, "Today", size=16, color=INK))
    o.append(text(mx + 22, gy + 40, "Tuesday classes · via TigerJunction", size=11, color=MUT))
    pill(o, mx + colw - 130, gy + 16, "Open Junction", bg=TURQ_T, fg=TURQ, size=11, h=26)
    for i, (tm, code, sub, c, ct) in enumerate([("9:00", "ECO 100", "Microeconomics · McCosh 50", TURQ, TURQ_T),
            ("11:00", "WWS 301", "Public Policy · Robertson 016", PURPLE, PURPLE_T),
            ("1:30", "COS 226", "Algorithms · Friend 101", CERU, CERU_T)]):
        ry = gy + 76 + i * 54
        o.append(text(mx + 22, ry + 8, tm, size=12, color=MUT))
        o.append(rect(mx + 80, ry, colw - 100, 42, bg=ct, stroke="transparent", fill="solid"))
        o.append(rect(mx + 80, ry, 4, 42, bg=c, stroke="transparent", fill="solid"))
        o.append(text(mx + 96, ry + 7, code, size=13, color=INK))
        o.append(text(mx + 96, ry + 25, sub, size=10, color=MUT))
    # Degree (TigerPath)
    dy = gy + 274; card(o, mx, dy, colw, 252); o.append(rect(mx, dy, 5, 252, bg=PURPLE, stroke="transparent", fill="solid"))
    o.append(text(mx + 22, dy + 16, "Degree progress", size=16, color=INK))
    o.append(text(mx + 22, dy + 40, "COS B.S.E. · Class of 2027 · via TigerPath", size=11, color=MUT))
    o.append(text(mx + colw - 90, dy + 18, "76%", size=22, color=PURPLE))
    for i, (lab, f) in enumerate([("Math & Science", 1.0), ("CS Core", 0.7), ("Departmentals", 0.6), ("General Eds", 0.85)]):
        ry = dy + 84 + i * 30
        o.append(text(mx + 22, ry - 2, lab, size=11, color=INK)); progress(o, mx + 200, ry + 2, colw - 240, f, PURPLE)
    pill(o, mx + 22, dy + 218, "Ask: what's left?", bg=PURPLE_T, fg=PURPLE, size=11, h=26)
    # Seat alerts (Snatch)
    card(o, rcolx, gy, rcolw, 150); o.append(rect(rcolx, gy, 5, 150, bg=MAG, stroke="transparent", fill="solid"))
    o.append(text(rcolx + 20, gy + 16, "Seat alerts", size=15, color=INK))
    o.append(text(rcolx + 20, gy + 37, "via TigerSnatch", size=10, color=MUT))
    pill(o, rcolx + rcolw - 80, gy + 16, "2 active", bg=MAG_T, fg=MAG, size=10, h=22)
    for i, (c, s) in enumerate([("MAT 202 P01", "watching · 28 ahead"), ("COS 217 L01", "watching · 4 ahead")]):
        ry = gy + 62 + i * 42
        o.append(ellipse(rcolx + 20, ry, 24, 24, bg=MAG_T, stroke="transparent", fill="solid"))
        o.append(ctext((rcolx + 20, ry, 24, 24), "◉", size=11, color=MAG))
        o.append(text(rcolx + 54, ry - 1, c, size=12, color=INK))
        o.append(text(rcolx + 54, ry + 15, s, size=10, color=MUT))
    # Campus today (The Forum)
    cy2 = gy + 174; card(o, rcolx, cy2, rcolw, 200); o.append(rect(rcolx, cy2, 5, 200, bg=AMBER, stroke="transparent", fill="solid"))
    o.append(text(rcolx + 20, cy2 + 16, "Campus today", size=15, color=INK))
    o.append(text(rcolx + 20, cy2 + 38, "via The Forum · your listservs · live", size=10, color=MUT))
    for i, (ic, t, s, ct) in enumerate([("🍕", "Free pizza — Frist 100", "~40 min left", AMBER_T),
             ("🎤", "AI & Society talk", "5pm · Friend Center", CERU_T),
             ("🎶", "Sinfonia concert", "8pm · Richardson", PURPLE_T)]):
        ry = cy2 + 60 + i * 44
        o.append(rect(rcolx + 20, ry, rcolw - 40, 38, bg=ct, stroke="transparent", fill="solid"))
        o.append(text(rcolx + 32, ry + 11, ic, size=14, color=INK))
        o.append(text(rcolx + 58, ry + 6, t, size=11, color=INK))
        o.append(text(rcolx + 58, ry + 21, s, size=9, color=MUT))
    # Recent
    ry0 = cy2 + 224; card(o, rcolx, ry0, rcolw, 106)
    o.append(text(rcolx + 20, ry0 + 14, "Pick up where you left off", size=14, color=INK))
    for i, (t, c) in enumerate([("Spring planning", CORAL), ("COS 226 reviews", CERU)]):
        ry = ry0 + 44 + i * 28
        o.append(ellipse(rcolx + 20, ry, 14, 14, bg=c, stroke="transparent", fill="solid"))
        o.append(text(rcolx + 44, ry - 2, t, size=12, color=INK))
    dump("dashboard.excalidraw", o)

# =========================================================================
# 3. CHAT  (A: Everything · B: app-focus split view)
# =========================================================================
def build_chat():
    o = []; H = 1040; W = 1500
    o.append(text(60, 36, "Chat · Everything mode — PI routes across every TigerApp", size=22, color=INK))
    ox, oy = 60, 80
    o.append(rect(ox - 20, oy - 20, W + 40, H + 40, bg=BG, stroke="transparent", fill="solid", rounded=False))
    blob(o, ox + W - 320, oy - 60, 380, 340, CORAL, 18)
    rail_r = app_rail(o, ox + 16, oy + 16, H - 32, active=0)
    mx = rail_r + 24; mw = ox + W - mx - 24
    focus_chip(o, mx, oy + 24, 0)
    o.append(text(ox + W - 150, oy + 30, "Spring planning", size=12, color=MUT))
    o.append(line([(mx, oy + 66), (ox + W - 24, oy + 66)], stroke=LINE))
    q = "Find 3 classes that finish my QCR, fit MWF mornings, rated >4, with open seats"
    bw = len(q) * 13 * 0.58 + 32
    o.append(rect(mx + mw - bw, oy + 90, bw, 38, bg=CORAL, stroke="transparent", fill="solid"))
    o.append(text(mx + mw - bw + 16, oy + 101, q, size=13, color=WHITE))
    squircle(o, mx, oy + 150, 26, CORAL, "π", size=13)
    o.append(text(mx + 36, oy + 156, "PI", size=13, color=MUT))
    sy = oy + 188
    o.append(rect(mx, sy, mw, 36, bg=CARD, stroke=LINE, fill="solid"))
    o.append(text(mx + 16, sy + 10, "Looked across your apps:", size=12, color=MUT))
    sx = mx + 200
    for (lab, c) in [("TigerPath", PURPLE), ("PrincetonCourses", CERU), ("TigerJunction", TURQ), ("TigerSnatch", MAG)]:
        o.append(ellipse(sx, sy + 12, 12, 12, bg=c, stroke="transparent", fill="solid"))
        o.append(text(sx + 18, sy + 10, lab, size=12, color=INK)); sx += len(lab)*7 + 36
    callout(o, mx + mw - 240, sy - 34, "Plain language —\nnot raw tool calls", tip=(mx + mw - 120, sy))
    o.append(text(mx, sy + 50, "Here are 3 that fit all four conditions:", size=13, color=INK))
    yy = sy + 80
    cards = [
        ("COS 226", "Algorithms & Data Structures", "4.3", "QCR", "Open", "12 open", "MWF 10:00 · Dondero",
         [("QCR ✓ TigerPath", PURPLE, PURPLE_T), ("fits Junction", TURQ, TURQ_T)]),
        ("ECO 100", "Intro to Microeconomics", "4.1", "SA", "Open", "5 open", "MWF 9:00 · Kasparov",
         [("fills SA req", PURPLE, PURPLE_T), ("fits Junction", TURQ, TURQ_T)]),
        ("MAT 202", "Linear Algebra", "4.2", "QCR", "Full", "wait", "MWF 11:00 · Ionescu",
         [("QCR ✓ TigerPath", PURPLE, PURPLE_T), ("watch on Snatch", MAG, MAG_T)]),
    ]
    for c in cards: yy += course_card(o, mx, yy, mw, *c) + 14
    button(o, mx, yy + 2, 230, 42, "Add COS 226 + ECO 100", color=TURQ)
    button(o, mx + 246, yy + 2, 180, 42, "Watch MAT 202", color=MAG)
    cyb = oy + H - 70; card(o, mx, cyb, mw, 48)
    o.append(text(mx + 18, cyb + 15, "Reply…", size=13, color=MUT))
    o.append(rect(mx + mw - 42, cyb + 8, 32, 32, bg=CORAL, stroke="transparent", fill="solid"))
    o.append(ctext((mx + mw - 42, cyb + 8, 32, 32), "↑", size=15, color=WHITE))
    # Frame B
    ox2 = ox + W + 160
    o.append(text(ox2, 36, "Chat · focused on TigerJunction — it docks your live schedule beside the chat", size=22, color=INK))
    o.append(rect(ox2 - 20, oy - 20, W + 40, H + 40, bg=BG, stroke="transparent", fill="solid", rounded=False))
    blob(o, ox2 + 60, oy + H - 320, 380, 360, SKY, 30)
    rail_r2 = app_rail(o, ox2 + 16, oy + 16, H - 32, active=2)
    mx2 = rail_r2 + 24; full = ox2 + W - mx2 - 24
    chatw = full * 0.52; panelx = mx2 + chatw + 20; panelw = full - chatw - 20
    focus_chip(o, mx2, oy + 24, 2)
    o.append(line([(mx2, oy + 66), (ox2 + W - 24, oy + 66)], stroke=LINE))
    q2 = "Swap COS 226 to the 1:30 section and add a Friday-free seminar"
    bw2 = len(q2) * 13 * 0.58 + 32
    o.append(rect(mx2 + chatw - bw2, oy + 92, bw2, 38, bg=TURQ, stroke="transparent", fill="solid"))
    o.append(text(mx2 + chatw - bw2 + 16, oy + 103, q2, size=13, color=WHITE))
    squircle(o, mx2, oy + 150, 26, TURQ, "TJ", size=11)
    o.append(text(mx2 + 36, oy + 156, "TigerJunction", size=13, color=MUT))
    o.append(text(mx2, oy + 190, "Done — moved COS 226 to P02 (1:30) and added\nGSS 350 (Th, no Friday class). No conflicts.", size=13, color=INK))
    pill(o, mx2, oy + 250, "✓ Saved to TigerJunction", bg=GREEN_T, fg=GREEN, size=12, h=28)
    o.append(text(mx2, oy + 300, "Want me to also drop the Friday lab? →", size=12, color=MUT))
    callout(o, mx2, oy + 360, "Scoped to TigerJunction:\nonly Junction tools run here", color=TURQ)
    o.append(text(panelx, oy + 86, "Your live TigerJunction schedule", size=12, color=MUT))
    o.append(rect(panelx + panelw - 70, oy + 84, 56, 22, bg=TURQ_T, stroke="transparent", fill="solid"))
    o.append(ctext((panelx + panelw - 70, oy + 84, 56, 22), "edit", size=10, color=TURQ))
    schedule_panel(o, panelx, oy + 116, panelw, H - 220, blocks=[
        (0, 0, 1, "ECO 100", "McCosh", TURQ, TURQ_T), (2, 0, 1, "ECO 100", "McCosh", TURQ, TURQ_T), (4, 0, 1, "ECO 100", "McCosh", TURQ, TURQ_T),
        (1, 2, 1.5, "WWS 301", "Robert", PURPLE, PURPLE_T), (3, 2, 1.5, "WWS 301", "Robert", PURPLE, PURPLE_T),
        (0, 4.5, 1, "COS 226", "Friend", CERU, CERU_T), (2, 4.5, 1, "COS 226", "Friend", CERU, CERU_T),
        (3, 5.5, 1.5, "GSS 350", "Aaron", MAG, MAG_T)])
    callout(o, panelx + panelw - 230, oy + H - 150, "Live TigerJunction —\nnot tool output", tip=(panelx + panelw/2, oy + H - 160), color=TURQ)
    dump("chat.excalidraw", o)

# =========================================================================
# 4. APPS  (lens gallery / connections)
# =========================================================================
def build_apps():
    o = []; W, H = 1320, 1010
    o.append(rect(-40, -40, W + 80, H + 80, bg=BG, stroke="transparent", fill="solid", rounded=False))
    blob(o, W - 340, -120, 440, 420, CORAL, 20); blob(o, -160, H - 320, 420, 380, SKY, 28)
    o.append(text(80, 56, "Your Princeton apps", size=34, color=INK))
    o.append(text(82, 102, "Chat with one, a few, or all at once. No setup, no jargon — just toggle what PI can see.", size=14, color=MUT))
    avatar(o, W - 80, 56, 44, MAG, "G")
    by = 150; card(o, 80, by, W - 160, 90, fill=CORAL_T, stroke="transparent")
    squircle(o, 104, by + 22, 46, CORAL, "π", size=18)
    o.append(text(168, by + 24, "Everything mode", size=18, color=INK))
    o.append(text(168, by + 52, "PI automatically uses any TigerApp it needs in one conversation — on by default.", size=12, color=INK))
    pill(o, W - 260, by + 28, "● On by default", bg=WHITE, fg=CORAL, size=12, h=34)
    gx, gy = 80, 270; cw = (W - 160 - 2*24) / 3; ch = 206
    for i, a in enumerate(APPS[1:]):
        x = gx + (i % 3) * (cw + 24); y = gy + (i // 3) * (ch + 24)
        card(o, x, y, cw, ch); o.append(rect(x, y, cw, 6, bg=a[COLOR], stroke="transparent", fill="solid"))
        squircle(o, x + 20, y + 24, 46, a[COLOR], a[BADGE], size=18)
        o.append(text(x + 80, y + 24, a[NAME], size=17, color=INK))
        o.append(text(x + 80, y + 50, a[BLURB], size=11, color=MUT))
        for j, cap in enumerate(CAPS[a[NAME]]):
            o.append(ellipse(x + 22, y + 98 + j*26, 8, 8, bg=a[COLOR], stroke="transparent", fill="solid"))
            o.append(text(x + 40, y + 94 + j*26, cap, size=11, color=INK))
        pill(o, x + 20, y + ch - 36, "● Connected", bg=GREEN_T, fg=GREEN, size=10, h=24)
        o.append(text(x + cw - 92, y + ch - 32, "Chat now →", size=11, color=a[COLOR]))
    sy = gy + 2*(ch + 24)
    for i, (name, blurb, color) in enumerate([("MyPrincetonU", "registrar read/write", CERU), ("TigerDraw", "room draw planning", PURPLE), ("Add your app", "any TigerApp MCP", MUT)]):
        x = gx + i * (cw + 24); card(o, x, sy, cw, 64, fill="#f6f1e8")
        squircle(o, x + 16, sy + 14, 36, "#d9cfc0", name[0], size=14)
        o.append(text(x + 64, sy + 16, name, size=14, color=MUT)); o.append(text(x + 64, sy + 38, blurb, size=10, color=MUT))
        pill(o, x + cw - 96, sy + 20, "Coming soon", bg="#efe8db", fg=MUT, size=10, h=24)
    dump("apps.excalidraw", o)

# =========================================================================
# 5. WORKFLOWS  (talk to several apps at once: groups + cross-app asks)
# =========================================================================
def build_workflows():
    o = []; W, H = 1440, 1010
    o.append(rect(-40, -40, W + 80, H + 80, bg=BG, stroke="transparent", fill="solid", rounded=False))
    blob(o, W - 360, -120, 460, 420, CORAL, 18); blob(o, -180, H - 360, 440, 420, SKY, 26)
    rail_r = app_rail(o, 24, 24, H - 48, active=-1)
    mx = rail_r + 28; mw = W - mx - 28
    o.append(text(mx, 40, "Do more across your apps", size=32, color=INK))
    o.append(text(mx + 2, 84, "Ask one thing — PI uses as many TigerApps as it takes.", size=14, color=MUT))
    # scope explainer (three tiers)
    ey = 124; ew = (mw - 2*16) / 3
    tiers = [("One app", "focus a single lens", CERU), ("A group", "several apps at once", PURPLE), ("Everything", "every app, automatically", CORAL)]
    for i, (t, s, c) in enumerate(tiers):
        x = mx + i * (ew + 16); card(o, x, ey, ew, 58)
        o.append(rect(x, ey, 5, 58, bg=c, stroke="transparent", fill="solid"))
        o.append(text(x + 20, ey + 12, t, size=15, color=INK)); o.append(text(x + 20, ey + 34, s, size=11, color=MUT))
        if i < 2: o.append(text(x + ew + 2, ey + 18, "›", size=18, color=MUT))
    # GROUPS
    o.append(text(mx, 214, "App groups — talk to a few at once", size=16, color=INK))
    gy = 246; gw = (mw - 2*20) / 3
    for i, (gname, blurb, members, accent) in enumerate(GROUPS):
        x = mx + i * (gw + 20); card(o, x, gy, gw, 196)
        o.append(rect(x, gy, gw, 6, bg=accent, stroke="transparent", fill="solid"))
        for j, mi in enumerate(members):
            a = APPS[mi]; squircle(o, x + 22 + j*34, gy + 24, 30, a[COLOR], a[BADGE], size=12)
        o.append(text(x + 22, gy + 72, gname, size=17, color=INK))
        o.append(text(x + 22, gy + 98, blurb, size=12, color=MUT))
        o.append(text(x + 22, gy + 126, " · ".join(APPS[mi][RAIL] for mi in members), size=10, color=accent))
        button(o, x + 22, gy + 150, gw - 44, 34, "Chat with this group  →", color=accent, size=12)
    # CROSS-APP ASKS
    o.append(text(mx, 478, "Try asking across apps", size=16, color=INK))
    ay = 510; aw = (mw - 2*20) / 3
    asks = [
        ("COURSE SELECTION", "“Build a balanced spring schedule\nand watch the full ones for me”", [1,2,3,4]),
        ("COURSE SELECTION", "“3 backups that still fit if I don't\nget into MAT 202”", [1,2,4]),
        ("LOOKING AHEAD", "“What should I take to finish my\ncertificate and explore ML?”", [3,1,2]),
        ("EVERYDAY", "“Catch me up on campus and\nwhat's for lunch today”", [5,6]),
        ("EVERYDAY", "“Add the free study break from my\nlistserv to my calendar”", [5]),
        ("DECIDE", "“Compare COS 226 and COS 217\nside by side, with demand”", [1,4]),
    ]
    for i, (tag, ex, members) in enumerate(asks):
        x = mx + (i % 3) * (aw + 20); y = ay + (i // 3) * 156
        card(o, x, y, aw, 138)
        o.append(text(x + 18, y + 14, tag, size=10, color=MUT))
        o.append(text(x + 18, y + 38, ex, size=13, color=INK))
        for j, mi in enumerate(members):
            a = APPS[mi]
            o.append(ellipse(x + 18 + j*84, y + 100, 12, 12, bg=a[COLOR], stroke="transparent", fill="solid"))
            o.append(text(x + 34 + j*84, y + 98, a[RAIL], size=9, color=MUT))
        o.append(text(x + aw - 30, y + 96, "→", size=16, color=CORAL))
    dump("workflows.excalidraw", o)

# =========================================================================
# 6. PROACTIVE  (new feature: PI watches your apps and checks in)
# =========================================================================
def build_proactive():
    o = []; W, H = 1200, 1010
    o.append(rect(-40, -40, W + 80, H + 80, bg=BG, stroke="transparent", fill="solid", rounded=False))
    blob(o, W - 320, -120, 420, 400, CORAL, 20); blob(o, -160, H - 340, 420, 400, SKY, 26)
    rail_r = app_rail(o, 24, 24, H - 48, active=-1)
    mx = rail_r + 28; mw = W - mx - 28
    o.append(text(mx, 40, "Good morning, Geraldine", size=30, color=INK))
    o.append(text(mx + 2, 82, "PI checked your apps — 5 things worth a look · Tue 8:02am", size=14, color=MUT))
    pill(o, mx + mw - 150, 44, "● PI for you", bg=CORAL_T, fg=CORAL, size=12, h=32)

    def feed_item(y, app_idx, title, detail, source, actions):
        a = APPS[app_idx]; h = 96
        card(o, mx, y, mw, h); o.append(rect(mx, y, 5, h, bg=a[COLOR], stroke="transparent", fill="solid"))
        o.append(ellipse(mx + 20, y + 28, 40, 40, bg=a[TINT], stroke="transparent", fill="solid"))
        o.append(ctext((mx + 20, y + 28, 40, 40), a[BADGE], size=14, color=a[COLOR]))
        o.append(text(mx + 76, y + 18, title, size=15, color=INK))
        o.append(text(mx + 76, y + 42, detail, size=12, color=MUT))
        o.append(text(mx + 76, y + 66, "from " + source, size=10, color=a[COLOR]))
        rb = mx + mw - 18
        for (lab, primary) in reversed(actions):
            bw = len(lab) * 12 * 0.6 + 28; rb -= bw
            button(o, rb, y + (h - 32) / 2, bw, 32, lab, color=(a[COLOR] if primary else INK), ghost=(not primary), size=12)
            rb -= 10
        return h

    y = 124
    y += feed_item(y, 4, "A seat just opened in MAT 202 P01",
                   "It's on your watchlist and fits your schedule.", "TigerSnatch → TigerJunction",
                   [("Add to Junction", True), ("Keep watching", False)]) + 16
    y += feed_item(y, 3, "You're one course from finishing your QCR",
                   "COS 226 (★4.3) fits your plan and has 12 seats open.", "TigerPath + PrincetonCourses",
                   [("See it", True), ("Add", False)]) + 16
    y += feed_item(y, 2, "Course selection opens in 6 days",
                   "Want a draft schedule ready to go the moment it opens?", "TigerJunction",
                   [("Draft my schedule", True)]) + 16
    y += feed_item(y, 5, "AI & Society talk today, 5pm — free food",
                   "Matches your interests and it's near your last class.", "The Forum · listservs",
                   [("Add to calendar", True), ("Dismiss", False)]) + 16
    y += feed_item(y, 6, "Chicken parm at Whitman tonight",
                   "One of your usual favorites is on the menu.", "TigerMenus",
                   [("Remind me", True), ("Not interested", False)]) + 16
    o.append(text(mx, y + 6, "PI checks in each morning · choose what it watches →", size=12, color=MUT))
    callout(o, mx + mw - 250, 82, "PI is proactive —\nit watches, you decide", tip=(mx + mw - 90, 124))
    dump("proactive.excalidraw", o)


# =========================================================================
# 7. USER STORY  (warm storyboard, real app names, snake flow)
# =========================================================================
def build_user_story():
    o = []
    o.append(rect(-60, -60, 2300, 1500, bg=BG, stroke="transparent", fill="solid", rounded=False))
    blob(o, 1700, -80, 520, 480, CORAL, 16); blob(o, -120, 1000, 460, 440, SKY, 24)
    o.append(text(80, 40, "Geraldine plans her spring — across every TigerApp, in one sitting", size=26, color=INK))
    o.append(text(82, 80, "Everything mode → focus TigerJunction → done → asks The Forum", size=14, color=MUT))
    FW, FH = 640, 420
    pos = [(80, 150), (820, 150), (1560, 150), (1560, 660), (820, 660), (80, 660)]

    def frame(i, title, accent):
        x, y = pos[i]; card(o, x, y, FW, FH)
        o.append(rect(x, y, FW, 8, bg=accent, stroke="transparent", fill="solid"))
        o.append(ellipse(x - 16, y - 16, 36, 36, bg=accent, stroke="transparent", fill="solid"))
        o.append(ctext((x - 16, y - 16, 36, 36), str(i + 1), size=16, color=WHITE))
        o.append(text(x, y + FH + 14, f"{i+1} · {title}", size=13, color=INK)); return x, y + 8

    def head(x, y, label, accent, badge="π"):
        squircle(o, x + 16, y + 14, 28, accent, badge, size=13)
        o.append(text(x + 54, y + 20, label, size=13, color=INK))
        o.append(line([(x, y + 52), (x + FW, y + 52)], stroke=LINE))

    x, y = frame(0, "Lands → continues with NetID", CORAL)
    blob(o, x + FW - 200, y + 10, 240, 200, CORAL, 25)
    o.append(text(x + 30, y + 90, "Your whole campus,", size=30, color=INK))
    o.append(text(x + 30, y + 126, "one conversation.", size=30, color=CORAL))
    button(o, x + 30, y + 196, 230, 46, "Continue with NetID  →", color=CORAL)
    o.append(text(x + 30, y + 260, "PrincetonCourses · TigerJunction · TigerPath · TigerSnatch · The Forum", size=11, color=MUT))

    x, y = frame(1, "Dashboard — her campus at a glance", TURQ)
    head(x, y, "PI · Home", TURQ)
    o.append(text(x + 20, y + 70, "Hi Geraldine,", size=20, color=INK))
    for i, (lab, c, ct) in enumerate([("Today · via Junction", TURQ, TURQ_T), ("2 alerts · Snatch", MAG, MAG_T), ("Degree 76% · Path", PURPLE, PURPLE_T), ("Free pizza · Forum", AMBER, AMBER_T)]):
        cx = x + 20 + (i % 2) * 300; cy = y + 110 + (i // 2) * 80
        o.append(rect(cx, cy, 280, 64, bg=ct, stroke="transparent", fill="solid"))
        o.append(rect(cx, cy, 4, 64, bg=c, stroke="transparent", fill="solid"))
        o.append(text(cx + 16, cy + 22, lab, size=13, color=INK))
    o.append(rect(x + 20, y + FH - 70, FW - 40, 40, bg=CARD, stroke=CORAL, fill="solid"))
    o.append(text(x + 36, y + FH - 58, "Ask PI anything…  Everything ⌄", size=12, color=MUT))

    x, y = frame(2, "Asks once → PI answers across 4 apps", CORAL)
    head(x, y, "PI · Everything", CORAL)
    o.append(rect(x + 20, y + 66, FW - 40, 30, bg=CARD, stroke=LINE, fill="solid"))
    o.append(text(x + 32, y + 73, "Build my spring — QCR, MWF, good profs, open seats", size=11, color=INK))
    for i, (c, col) in enumerate([("TigerPath", PURPLE), ("Courses", CERU), ("Junction", TURQ), ("Snatch", MAG)]):
        o.append(ellipse(x + 24 + i*100, y + 108, 12, 12, bg=col, stroke="transparent", fill="solid"))
        o.append(text(x + 40 + i*100, y + 106, c, size=10, color=INK))
    for i, (code, s, c) in enumerate([("COS 226", "★4.3 · 12 open", CERU), ("ECO 100", "★4.1 · 5 open", TURQ), ("MAT 202", "★4.2 · full", MAG)]):
        cy = y + 138 + i*70; card(o, x + 20, cy, FW - 40, 60)
        o.append(rect(x + 20, cy, 4, 60, bg=c, stroke="transparent", fill="solid"))
        o.append(text(x + 36, cy + 12, code, size=15, color=INK)); o.append(text(x + 36, cy + 34, s, size=11, color=MUT))
        button(o, x + FW - 110, cy + 16, 80, 28, "+ Add", color=TURQ, size=11)

    x, y = frame(3, "Switches to TigerJunction — live calendar", TURQ)
    head(x, y, "PI · TigerJunction", TURQ, "TJ")
    o.append(text(x + 20, y + 70, "“tidy it up and free my Fridays”", size=12, color=INK))
    schedule_panel(o, x + 20, y + 96, FW - 40, FH - 180, blocks=[
        (0, 0, 1, "ECO", "", TURQ, TURQ_T), (2, 0, 1, "ECO", "", TURQ, TURQ_T), (4, 0, 1, "ECO", "", TURQ, TURQ_T),
        (1, 2, 1.5, "WWS", "", PURPLE, PURPLE_T), (3, 2, 1.5, "WWS", "", PURPLE, PURPLE_T),
        (0, 4.5, 1, "COS", "", CERU, CERU_T), (2, 4.5, 1, "COS", "", CERU, CERU_T)], title="Spring 2026 · Fridays free")

    x, y = frame(4, "Confirms — PI writes schedule + alert", MAG)
    head(x, y, "PI · TigerJunction", TURQ, "TJ")
    pill(o, x + 20, y + 70, "✓ Saved to TigerJunction", bg=GREEN_T, fg=GREEN, size=12, h=30)
    card(o, x + 20, y + 120, FW - 40, 70); o.append(rect(x + 20, y + 120, 4, 70, bg=MAG, stroke="transparent", fill="solid"))
    o.append(ellipse(x + 36, y + 138, 30, 30, bg=MAG_T, stroke="transparent", fill="solid"))
    o.append(ctext((x + 36, y + 138, 30, 30), "◉", size=14, color=MAG))
    o.append(text(x + 80, y + 132, "TigerSnatch · watching MAT 202 P01", size=13, color=INK))
    o.append(text(x + 80, y + 156, "I'll email geraldine@princeton.edu", size=11, color=MUT))
    pill(o, x + FW - 110, y + 140, "Active", bg=GREEN_T, fg=GREEN, size=11, h=26)
    o.append(text(x + 20, y + 220, "✓ COS 226 + ECO 100 added · Fridays free · MAT 202 watched", size=12, color=GREEN))

    x, y = frame(5, "Back home — then asks The Forum", AMBER)
    head(x, y, "PI · Home", TURQ)
    o.append(text(x + 20, y + 66, "Spring is set ✓ — schedule, degree & alerts updated", size=12, color=GREEN))
    o.append(rect(x + FW - 230, y + 98, 200, 30, bg=AMBER, stroke="transparent", fill="solid"))
    o.append(text(x + FW - 218, y + 105, "any free food right now?", size=11, color=WHITE))
    card(o, x + 20, y + 144, FW - 40, 110); o.append(rect(x + 20, y + 144, 4, 110, bg=AMBER, stroke="transparent", fill="solid"))
    o.append(text(x + 38, y + 158, "The Forum · freshest first:", size=12, color=INK))
    o.append(text(x + 38, y + 184, "🍕  Frist 100 — pizza, ~40 min left", size=11, color=MUT))
    o.append(text(x + 38, y + 208, "🥯  Friend Center — bagels, ~20 min", size=11, color=MUT))
    o.append(text(x + 20, y + 268, "from your res-college + free-food listservs · live", size=10, color=MUT))

    def arr(a, b): o.append(line([a, b], stroke=CORAL, sw=2.5, arrow=True))
    arr((pos[0][0]+FW+8, pos[0][1]+FH/2), (pos[1][0]-8, pos[1][1]+FH/2))
    arr((pos[1][0]+FW+8, pos[1][1]+FH/2), (pos[2][0]-8, pos[2][1]+FH/2))
    arr((pos[2][0]+FW/2, pos[2][1]+FH+8), (pos[3][0]+FW/2, pos[3][1]-8))
    arr((pos[3][0]-8, pos[3][1]+FH/2), (pos[4][0]+FW+8, pos[4][1]+FH/2))
    arr((pos[4][0]-8, pos[4][1]+FH/2), (pos[5][0]+FW+8, pos[5][1]+FH/2))
    dump("user-story.excalidraw", o)


if __name__ == "__main__":
    build_landing(); build_dashboard(); build_chat(); build_apps()
    build_workflows(); build_proactive(); build_user_story()
    for n in ("homepage", "dashboard", "chat", "apps", "workflows", "proactive", "user-story"):
        json.load(open(os.path.join(OUT, n + ".excalidraw")))
    print("all files valid JSON")
