#!/usr/bin/env python3
"""Genereert de Full Circle Delivery-plaat (SVG) uit een declaratief FCD-bestand (YAML)."""
import sys, re, os, json, yaml
from xml.sax.saxutils import escape
from PIL import ImageFont

src, dst = sys.argv[1], sys.argv[2]
docs = [d for d in yaml.safe_load_all(open(src)) if d]
by = {}
for d in docs: by.setdefault(d["kind"], []).append(d)
name = lambda d: d["metadata"]["name"]
title = lambda d: d["metadata"].get("title", name(d))
spec = lambda d: d.get("spec") or {}

W, H = 3840, 2160
FONT = "Segoe UI, Inter, sans-serif"
FD = os.environ.get("FCD_FONTS", "/usr/share/fonts/opentype/inter/")
ICONS = os.environ.get("FCD_ICONS", "node_modules/@fluentui/svg-icons/icons/")
INK, MUTED, RULE, BG = "#1F2937", "#5B6472", "#DDE2E9", "#F2F4F7"
C_INT, C_CON, C_SUB, C_PROD, C_USE, C_LEARN, C_GAP, C_EXP = "#7B3FB2", "#2176C7", "#1AA6B7", "#239B45", "#4C6FFF", "#6F2DBD", "#8A3FC2", "#C56A00"
_f = {}
def tw(s, size, bold=False):
    k = (size, bold)
    if k not in _f: _f[k] = ImageFont.truetype(FD + ("Inter-Bold.otf" if bold else "Inter-Regular.otf"), size)
    return _f[k].getlength(s)
def wrap(s, size, bold, maxw):
    lines, cur = [], ""
    for w in s.split(" "):
        t = (cur + " " + w).strip()
        if cur and tw(t, size, bold) > maxw: lines.append(cur); cur = w
        else: cur = t
    return lines + [cur]
out = []; add = out.append
def text(x, y, s, size, bold=False, fill=INK, anchor="start", ls=0):
    add(f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" font-size="{size}" font-weight="{700 if bold else 400}" '
        f'fill="{fill}" text-anchor="{anchor}" letter-spacing="{ls}">{escape(s)}</text>')
def rect(x, y, w, h, fill, rx=0, stroke=None, sw=0, dash=None):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    if dash: st += f' stroke-dasharray="{dash}"'
    add(f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}"{st}/>')
def icon(nm, x, y, size, fill):
    ds = re.findall(r'<path d="([^"]+)"', open(f"{ICONS}{nm}_24_regular.svg").read())
    add(f'<g transform="translate({x:.1f},{y:.1f}) scale({size/24:.3f})" fill="{fill}">' + "".join(f'<path d="{d}"/>' for d in ds) + "</g>")
def _chip(x, y, s, color, size=22, dashed=False, solid=False, anchor="start"):
    w, h = tw(s, size, True) + 30, size + 18
    if anchor == "end": x -= w
    if dashed: rect(x, y, w, h, "#FFFFFF", rx=h/2, stroke=C_GAP, sw=2.5, dash="8 6"); fc = C_GAP
    elif solid: rect(x, y, w, h, color, rx=h/2); fc = "#FFFFFF"
    else: rect(x, y, w, h, color + "1A", rx=h/2, stroke=color, sw=2.5); fc = color
    text(x + w/2, y + h/2 + size*0.36, s, size, True, fc, "middle")
    return w
def chip(*a, **k):
    d = k.get("dashed")
    if d: add('<g class="backlog">')
    w = _chip(*a, **k)
    if d: add('</g>')
    return w
gaps = []
def gap(s):
    if s not in gaps: gaps.append(s)

fac = by["Factory"][0]

# ------------------------------------------------------------ pipeline: stappen en gates (berekenen)
# Uit Pipeline (spec.steps, de volgorde), Step en QualityGate. Kolommen: Bouwen tot de stap deploy,
# Deployen tot de stap release, Releasen vanaf release.
STEPS = {name(x): x for x in by.get("Step", [])}
GATES = by.get("QualityGate", [])
porder = next((spec(p).get("steps") for p in by.get("Pipeline", []) if spec(p).get("steps")), [])
porder = [n for n in porder if n in STEPS]
cols3 = {"Bouwen": [], "Deployen": [], "Releasen": []}
if porder:
    col = "Bouwen"; lvl = None; nr = 0
    for n in porder:
        if n == "deploy": col = "Deployen"; lvl = None
        if n == "release": col = "Releasen"; lvl = None
        rows = cols3[col]
        for g in GATES:
            if n in (spec(g).get("beforeSteps") or []): rows.append(("gate", g))
        l = spec(STEPS[n]).get("level") or "subProduct"
        if l != lvl and col != "Releasen":
            rows.append(("label", "per container" if l == "container" else "het deelproduct")); lvl = l
        nr += 1; rows.append(("step", STEPS[n], nr))
        for b_ in by.get("Step", []):
            if spec(b_).get("status") == "backlog" and spec(b_).get("after") == n: rows.append(("backlog", b_))
        for g in GATES:
            if (spec(g).get("afterSteps") or [None])[-1] == n: rows.append(("gate", g))
GEXP = {}
for e in by.get("Explanation", []):
    if spec(e).get("gate") and not spec(e).get("step"): GEXP.setdefault(spec(e)["gate"], []).append(e)
RH = {"step": 56, "backlog": 56, "gate": 54, "label": 44}
def rows_h(rows): return sum(RH[r[0]] + (30 if r[0] == "gate" and name(r[1]) in GEXP else 0) for r in rows)
BY = 990
BH = (max(rows_h(r) for r in cols3.values()) + 150) if porder else 0
KY0 = BY + BH + 40 if porder else 1010
H = KY0 + 1100 + 50
add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
add('<defs><marker id="ah" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse">'
    f'<path d="M0,0 L10,5 L0,10 z" fill="{INK}"/></marker></defs>')
rect(0, 0, W, H, BG)
text(60, 112, f"Full Circle Delivery: {title(fac)}", 68, True)
text(62, 162, f"Hoe het product ontstaat en levend blijft  ·  gegenereerd uit {os.path.basename(src)}", 28, False, MUTED)

# ------------------------------------------------------------ de cirkel
pipes = by.get("Pipeline", [])
build = [p for p in pipes if spec(p).get("builds")]
deploy = [p for p in pipes if spec(p).get("deploys")]
tests = by.get("TestType", [])
envs = by.get("Environment", [])
UNIT = {"SubProduct": "het hele deelproduct", "Container": "één container", "Product": "het hele product"}
steps = []
s = [("Intent", spec(fac).get("intentParts")), ("Beschrijving van het deelproduct", spec(fac).get("subProductDescriptionParts"))]
if not all(v for _, v in s): gap("Intentie: opbouw van de intent ontbreekt")
steps.append(("Intentie", None, C_INT, "lightbulb", [(h, v) for h, v in s if v], []))
b, g_ = [], []
if build:
    p = build[0]
    u = spec(p).get("uses") or {}
    b.append(("Pipeline", ([title(p)] if title(p) != "Pipeline" else []) + ([f"{u['subProduct']} {u.get('version', '')}".strip()] if u.get("subProduct") else [])
              + ([f"aangeroepen door {spec(p)['calledBy']}"] if spec(p).get("calledBy") else [])))
    if spec(p).get("artifact"): b.append(("Levert", [spec(p)["artifact"]]))
else: g_.append("pipeline ?"); gap("Bouwen: geen pipeline")
if tests: b.append(("Testsoorten", [title(t) for t in tests]))
else: g_.append("testsoorten ?"); gap("Bouwen: geen testsoorten")
steps.append(("Bouwen", "bouwen", C_CON, "wrench_screwdriver", b, g_))
b, g_ = [], []
if deploy:
    p = deploy[0]
    b.append(("Pipeline", [title(p)] + ([f"{spec(p)['uses']['subProduct']} {spec(p)['uses'].get('version', '')}".strip()] if (spec(p).get("uses") or {}).get("subProduct") else [])))
    if b[-1][1][0] == "Pipeline": b[-1] = ("Pipeline", b[-1][1][1:] or ["Pipeline"])
    if spec(p).get("deployUnit"): b.append(("Eenheid", [UNIT.get(spec(p)["deployUnit"], spec(p)["deployUnit"])]))
    if spec(p).get("deployTarget"): b.append(("Waarop", [spec(p)["deployTarget"]]))
else: g_.append("pipeline ?"); gap("Deployen: geen pipeline")
if envs: b.append(("Omgevingen", [title(e) for e in envs]))
else: g_.append("omgevingen ?"); gap("Deployen: geen omgevingen")
steps.append(("Deployen", "deployen", C_SUB, "puzzle_piece", b, g_))
rel = by.get("Release", [])
prel = next((spec(p).get("release") for p in pipes if spec(p).get("release")), None)
if rel: steps.append(("Releasen", "releasen", C_PROD, "rocket", [("Release", [title(r) for r in rel])], []))
elif prel:
    rv = []
    if prel.get("tag"): rv.append(f"tag {prel['tag']}")
    if prel.get("notesFrom"): rv.append(f"tekst uit {prel['notesFrom']}")
    if prel.get("githubRelease") is False: rv.append("geen GitHub Release")
    steps.append(("Releasen", "releasen", C_PROD, "rocket", [("Release", rv), ("Eenheid", ["het deelproduct"])], []))
else:
    steps.append(("Releasen", "releasen", C_PROD, "rocket", [], ["release ?"]))
    gap("Releasen: hoe een deelproduct beschikbaar komt voor de gebruiker")
steps.append(("Gebruiken", None, C_USE, "people", [("Persona", ["staat in de intent van het product"])], []))
learn = by.get("Dashboard", []) + by.get("KeyPerformanceIndicator", [])
if learn:
    lv = [title(x) + (f" ({spec(x)['uses']['subProduct']} {spec(x)['uses'].get('version', '')})".rstrip() if (spec(x).get("uses") or {}).get("subProduct") else "") for x in learn]
    steps.append(("Leren", None, C_LEARN, "pulse", [("Zichtbaar", lv), ("Meten", ["het key result uit de intent"])], []))
else:
    steps.append(("Leren", None, C_LEARN, "pulse", [], ["dashboard ?", "meting ?"]))
    gap("Leren: dashboard en meting, zodat de cirkel rond is")

AX, AW = 60, 2780
CY, CH, GAPX = 220, 640, 56
cw = (AW - GAPX * (len(steps) - 1)) / len(steps)
for i, (nm, vb, col, ic, blocks, miss) in enumerate(steps):
    x = AX + i * (cw + GAPX)
    rect(x, CY, cw, CH, "#FFFFFF", rx=24)
    add(f'<path d="M{x},{CY+96} V{CY+24} Q{x},{CY} {x+24},{CY} H{x+cw-24} Q{x+cw},{CY} {x+cw},{CY+24} V{CY+96} Z" fill="{col}"/>')
    icon(ic, x + 24, CY + 26, 44, "#FFFFFF")
    text(x + 82, CY + 62, nm, 36, True, "#FFFFFF")
    if vb: text(x + cw - 24, CY + 60, "werkwoord", 20, False, "#FFFFFF", "end")
    y = CY + 150
    for h, vals in blocks:
        text(x + 26, y, h, 22, True, col, ls=1); y += 36
        for v in vals:
            for l in wrap(v, 25, False, cw - 52):
                text(x + 26, y, l, 25); y += 33
            y += 4
        y += 22
    for m in miss:
        chip(x + 26, y - 26, m, C_GAP, 24, dashed=True); y += 60
    if i < len(steps) - 1:
        add(f'<line x1="{x+cw+8}" y1="{CY+CH/2}" x2="{x+cw+GAPX-10}" y2="{CY+CH/2}" stroke="{INK}" stroke-width="6" marker-end="url(#ah)"/>')
# terug naar intentie
x1, x2, yb = AX + AW - cw / 2, AX + cw / 2, CY + CH + 62
add(f'<path d="M{x1},{CY+CH+6} V{yb-24} Q{x1},{yb} {x1-24},{yb} H{x2+24} Q{x2},{yb} {x2},{yb-24} V{CY+CH+14}" fill="none" stroke="{INK}" stroke-width="6" marker-end="url(#ah)"/>')
lab = "Wat het gebruik ons leert, voedt de volgende intentie"
lw = tw(lab, 26, True) + 48
rect(AX + AW/2 - lw/2, yb - 24, lw, 48, BG); text(AX + AW/2, yb + 9, lab, 26, True, INK, "middle")

# ------------------------------------------------------------ kaders
# ------------------------------------------------------------ pipeline: stappen en gates (tekenen)
if porder:
    rect(AX, BY, AW, BH, "#FFFFFF", rx=24)
    colx = {nm: AX + i * (cw + GAPX) for i, (nm, *_r) in enumerate(steps)}
    colc = {nm: c for nm, _v, c, *_r in steps}
    # links: titel en legenda
    x0 = AX + 30; y = BY + 64
    text(x0, y, "Pipeline", 36, True); y += 46
    for l in wrap("De stappen en quality gates per blok, uit Pipeline, Step en QualityGate.", 23, False, cw - 40):
        text(x0, y, l, 23, False, MUTED); y += 31
    y += 26
    add(f'<path d="M{x0+12},{y-20} l12,12 l-12,12 l-12,-12 z" fill="{INK}"/>'); text(x0 + 36, y, "quality gate", 23); y += 50
    _chip(x0, y - 26, "ingekort", C_EXP, 19); text(x0 + tw("ingekort", 19, True) + 44, y - 4, "alleen voor de demo", 21, False, MUTED); y += 50
    chip(x0, y - 26, "backlog", C_GAP, 19, dashed=True); text(x0 + tw("backlog", 19, True) + 44, y - 4, "nog niet gebouwd", 21, False, MUTED)
    for cn, rows in cols3.items():
        x = colx[cn]; c = colc[cn]; y = BY + 40
        text(x, y + 24, cn.upper(), 22, True, c, ls=2); y += 56
        for r in rows:
            if r[0] == "label":
                text(x + 4, y + 28, r[1].upper(), 18, True, MUTED, ls=2); y += RH["label"]
            elif r[0] == "step":
                st = r[1]; rect(x, y, cw, 46, "#FFFFFF", rx=12, stroke=c, sw=2.5)
                text(x + 16, y + 31, f"{r[2]}. {title(st)}", 22, True)
                if spec(st).get("shortened"):
                    tw_ = tw("ingekort", 17, True) + 30
                    _chip(x + cw - 10 - tw_, y + 7, "ingekort", C_EXP, 17)
                y += RH["step"]
            elif r[0] == "backlog":
                add('<g class="backlog">')
                rect(x, y, cw, 46, "#FFFFFF", rx=12, stroke=C_GAP, sw=2.5, dash="8 6")
                text(x + 16, y + 31, title(r[1]), 22, False, C_GAP)
                tw_ = tw("backlog", 17, True) + 30
                _chip(x + cw - 10 - tw_, y + 7, "backlog", C_GAP, 17, dashed=True)
                add('</g>'); y += RH["backlog"]
            else:
                g = r[1]
                add(f'<path d="M{x+14},{y+10} l13,13 l-13,13 l-13,-13 z" fill="{INK}"/>')
                text(x + 38, y + 32, title(g), 23, True)
                y += RH["gate"]
                if name(g) in GEXP:
                    text(x + 38, y + 4, "afwijking " + ", ".join(name(e) for e in GEXP[name(g)]), 20, True, C_EXP); y += 30
    # rechts: de afwijkingen op een stap of gate
    sx = colx["Gebruiken"]; sw_ = 2 * cw + GAPX; y = BY + 64
    text(sx, y, "Afwijkingen op stap en gate", 30, True); y += 44
    sexp = [e for e in by.get("Explanation", []) if spec(e).get("step") or spec(e).get("gate")]
    for e in sexp:
        where = title(STEPS[spec(e)["step"]]) if spec(e).get("step") in STEPS else next((title(g) for g in GATES if name(g) == spec(e).get("gate")), spec(e).get("gate", "?"))
        text(sx, y, f"{name(e)}  ·  {where}: {spec(e).get('rule', '')}", 22, True, C_EXP); y += 30
        meta = " · ".join(v for v in [f"tot {spec(e)['until']}" if spec(e).get("until") else "", f"goedgekeurd door {spec(e)['approver']}" if spec(e).get("approver") else ""] if v)
        if meta: text(sx, y, meta, 20, False, MUTED); y += 40
    if not sexp: text(sx, y, "Geen", 22, False, MUTED)
KY, KH = KY0, 1100
rect(AX, KY, AW, KH, "#FFFFFF", rx=24)
prins = by.get("Principle", [])
exps = {}
for e in by.get("Explanation", []):
    if not (spec(e).get("step") or spec(e).get("gate")): exps.setdefault(spec(e).get("principle"), []).append(e)
text(AX + 36, KY + 62, f"Kaders ({len(prins)})", 36, True)
text(AX + 36 + tw(f"Kaders ({len(prins)})", 36, True) + 24, KY + 60, "comply or explain  ·  samen de guardrails voor AI", 24, False, MUTED)
lx = AX + AW - 36
for lab, kw in [("explain ?", dict(dashed=True)), ("explain: nee", dict(solid=True)), ("explain: ja", {})]:
    lx -= chip(lx, KY + 30, lab, INK, 20, anchor="end", **kw) + 14
COLS, cgap = 4, 24
kw_ = (AW - 72 - cgap * (COLS - 1)) / COLS
FS, LH = 27, 35
def ph(p):
    n = len(wrap(spec(p)["statement"], FS, False, kw_ - 172))
    return n * LH + 38 * len(exps.get(name(p), [])) + 24
def draw(p, x, y):
    for k, l in enumerate(wrap(spec(p)["statement"], FS, False, kw_ - 172)): text(x, y + k * LH, l, FS)
    ea = spec(p).get("explainAllowed")
    if ea is True: chip(x + kw_, y - 24, "explain: ja", INK, 21, anchor="end")
    elif ea is False: chip(x + kw_, y - 24, "explain: nee", INK, 21, solid=True, anchor="end")
    else: chip(x + kw_, y - 24, "explain ?", C_GAP, 21, dashed=True, anchor="end")
    yy = y + len(wrap(spec(p)["statement"], FS, False, kw_ - 172)) * LH
    for e in exps.get(name(p), []):
        r = spec(e).get("reason", "?")
        if tw("Afwijking: " + r, 25, True) > kw_: r = r.split(".")[0]
        while tw("Afwijking: " + r, 25, True) > kw_: r = r[:-2].rstrip() + "…"
        text(x, yy, "Afwijking: " + r, 25, True, C_EXP); yy += 38
    add(f'<line x1="{x}" y1="{yy-12}" x2="{x+kw_}" y2="{yy-12}" stroke="{RULE}" stroke-width="1.5"/>')
    return yy + 24
unl = [p for p in prins if not spec(p).get("label")]
labs = []
for p in prins:
    l = spec(p).get("label")
    if l and l not in labs: labs.append(l)
TOP = KY + 150
# zonder label over COLS-1 kolommen
tot = sum(ph(p) for p in unl); per = tot / (COLS - 1)
col, y, maxy = 0, TOP, TOP
text(AX + 36, TOP - 44, f"ZONDER LABEL ({len(unl)})", 22, True, MUTED, ls=2)
acc = 0
for p in unl:
    if acc >= per * (col + 1) - 1 and col < COLS - 2: col += 1; y = TOP
    x = AX + 36 + col * (kw_ + cgap)
    y = draw(p, x, y + 0); acc += ph(p); maxy = max(maxy, y)
x = AX + 36 + (COLS - 1) * (kw_ + cgap); y = TOP
for l in labs:
    grp = [p for p in prins if spec(p).get("label") == l]
    text(x, y - 44, f"{l.upper()} ({len(grp)})", 22, True, MUTED, ls=2)
    for p in grp: y = draw(p, x, y)
    maxy = max(maxy, y); y += 70
if maxy > KY + KH - 10: print("OVERLOOP kaders", maxy, KY + KH)
n_unk = sum(1 for p in prins if spec(p).get("explainAllowed") is None)
if n_unk: gap(f"{n_unk} van de {len(prins)} kaders: niet bekend of explain is toegestaan")
if unl: gap(f"{len(unl)} van de {len(prins)} kaders: geen label")
bad = [e for e in by.get("Explanation", []) if not spec(e).get("approver") or not (spec(e).get("endDate") or spec(e).get("until"))]
if bad: gap(f"{len(bad)} afwijkingen: geen goedkeurder en geen einddatum")
pn = {name(p): p for p in prins}
unk = [e for e in by.get("Explanation", []) if spec(e).get("principle") in pn and spec(pn[spec(e)["principle"]]).get("explainAllowed") is None]
nok = [e for e in by.get("Explanation", []) if spec(e).get("principle") not in pn]
if nok: gap(f"{len(nok)} afwijkingen op een kader dat niet in het bestand staat ({', '.join(sorted({spec(e).get('principle', '?') for e in nok}))})")
if unk: gap(f"{len(unk)} afwijkingen op een kader waarvan niet bekend is of explain mag")

# ------------------------------------------------------------ rechterkolom
RX, RW, RY = 2890, 890, 220
rect(RX, RY, RW, 470, "#FFFFFF", rx=24)
text(RX + 40, RY + 66, "Wie doet het werk", 36, True)
y = RY + 130
for g in by.get("Group", []):
    icon("people", RX + 40, y - 34, 44, INK)
    text(RX + 100, y - 14, spec(g).get("type", "groep").upper(), 22, True, MUTED, ls=2)
    text(RX + 100, y + 26, title(g), 32, True); y += 84
    comp = {"ai-agents-only": "Alleen AI-agents", "humans": "Mensen", "humans-and-ai-agents": "Mensen en AI-agents"}.get(spec(g).get("composition"))
    if comp: text(RX + 40, y, f"Samenstelling: {comp}", 26); y += 44
    if spec(g).get("owner"):
        for l in wrap(f"Eigenaar van het deelproduct: {spec(g)['owner']}. Die keurt afwijkingen goed.", 26, False, RW - 80):
            text(RX + 40, y, l, 26); y += 36
if not by.get("Group"): gap("Geen squad of team")
GY = RY + 510
add('<g class="backlog">')
rect(RX, GY, RW, H - 50 - GY, "#FFFFFF", rx=24, stroke=C_GAP if gaps else C_PROD, sw=4, dash="14 10" if gaps else None)
text(RX + 40, GY + 70, f"Backlog ({len(gaps)})" if gaps else "De backlog is leeg", 36, True, C_GAP if gaps else C_PROD)
text(RX + 40, GY + 112, "Wat het FCD-model vraagt en nog niet is ingevuld", 24, False, MUTED)
y = GY + 176
for g_ in gaps:
    add(f'<circle cx="{RX+52}" cy="{y-9}" r="7" fill="{C_GAP}"/>')
    for l in wrap(g_, 26, False, RW - 120): text(RX + 76, y, l, 26); y += 36
    y += 18
add('</g>')
add("</svg>")
open(dst, "w").write("\n".join(out))
json.dump(gaps, open(dst + ".backlog.json", "w"), ensure_ascii=False)
print(len(gaps), "backlog"); [print(" -", g_) for g_ in gaps]
