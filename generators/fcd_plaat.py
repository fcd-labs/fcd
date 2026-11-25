#!/usr/bin/env python3
"""Genereert de productplaat (SVG) uit een declaratief FCD-bestand (YAML)."""
import sys, re, os, json, yaml
from xml.sax.saxutils import escape
from PIL import ImageFont

src, dst = sys.argv[1], sys.argv[2]
# Optioneel: versions.env van de repository van het deelproduct, de ene bron voor de versies.
vsrc = sys.argv[3] if len(sys.argv) > 3 else None
docs = [d for d in yaml.safe_load_all(open(src)) if d]
by = {}
for d in docs:
    by.setdefault(d["kind"], []).append(d)
name = lambda d: d["metadata"]["name"]
title = lambda d: d["metadata"].get("title", name(d))
spec = lambda d: d.get("spec") or {}
SEMVER = re.compile(r"^\d+\.\d+\.\d+$")

# Versies uit versions.env (KEY=waarde) in het declaratieve model zetten, als ze daar nog niet staan.
if vsrc and os.path.exists(vsrc):
    env = {}
    for l in open(vsrc):
        l = l.split("#", 1)[0].strip()
        if "=" in l:
            k, v = l.split("=", 1); env[k.strip()] = v.strip()
    key = lambda s: re.sub(r"[^A-Z0-9]", "_", s.upper()) + "_VERSION"
    for d in docs:
        sp = d.setdefault("spec", {}) if isinstance(d.get("spec"), dict) or d.get("spec") is None else None
        if sp is None or sp.get("version"): continue
        if d["kind"] == "SubProduct" and env.get("SUBPRODUCT") == name(d): v = env.get("SUBPRODUCT_VERSION")
        elif d["kind"] == "Container": v = env.get(key(sp.get("service") or name(d)))
        else: v = None
        if v: sp["version"] = v
    vbron = os.path.basename(os.path.dirname(os.path.abspath(vsrc))) + "/" + os.path.basename(vsrc)
else:
    vbron = None

W, H = 3840, 2160
FONT = "Segoe UI, Inter, sans-serif"
FD = os.environ.get("FCD_FONTS", "/usr/share/fonts/opentype/inter/")
ICONS = os.environ.get("FCD_ICONS", "node_modules/@fluentui/svg-icons/icons/")
INK, MUTED, RULE, BG = "#1F2937", "#5B6472", "#DDE2E9", "#F2F4F7"
C_PROD, C_SUB, C_CON, C_CODE, C_LIB, C_GAP = "#239B45", "#1AA6B7", "#2176C7", "#1F8F4E", "#EF8A21", "#8A3FC2"
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
out = []
add = out.append
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
def _chip(x, y, s, color, size=26, dashed=False, bold=True):
    w, h = tw(s, size, bold) + 36, size + 22
    if dashed: rect(x, y, w, h, "#FFFFFF", rx=h/2, stroke=C_GAP, sw=2.5, dash="8 6")
    else: rect(x, y, w, h, color + "1A", rx=h/2, stroke=color, sw=2.5)
    text(x + w/2, y + h/2 + size*0.36, s, size, bold, C_GAP if dashed else color, "middle")
    return w
def version_chip(x, y, d, size=26):
    v = spec(d).get("version")
    ok = isinstance(v, str) and SEMVER.match(v)
    return chip(x, y, f"v{v}" if ok else "versie ?", INK, size, dashed=not ok)
def verb(x_right, y, s, color):
    w = tw(s, 26, True) + 40
    rect(x_right - w, y, w, 46, color, rx=23)
    text(x_right - w/2, y + 32, s, 26, True, "#FFFFFF", "middle")

def chip(*a, **k):
    d = k.get("dashed")
    if d: add('<g class="backlog">')
    w = _chip(*a, **k)
    if d: add('</g>')
    return w

def zonder_backlog(regels):
    """Laat alle groepen met class backlog weg."""
    uit, diep = [], 0
    for r in regels:
        if diep == 0 and r == '<g class="backlog">':
            diep = 1; continue
        if diep:
            diep += r.count("<g") - r.count("</g>")
            continue
        uit.append(r)
    return uit
# Schakelaar in het bestand: spec.plateBacklog: false laat de backlog van de plaat weg.
TOON_BACKLOG = (spec(by["Product"][0]).get("plateBacklog", True) is not False) if by.get("Product") else True
gaps = []
def gap(s):
    if s not in gaps: gaps.append(s)
def check_version(d, label):
    v = spec(d).get("version")
    if not (isinstance(v, str) and SEMVER.match(v)): gap(f"{label} {title(d)}: geen versie")

add(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">')
rect(0, 0, W, H, BG)
prod = by["Product"][0]
text(60, 112, f"Productplaat: {title(prod)}", 68, True)
text(62, 162, f"Wat zit in wat  ·  gegenereerd uit {os.path.basename(src)}" + (f", versies uit {vbron}" if vbron else ""), 28, False, MUTED)

# ------------------------------------------------------------ product
PX, PY, PW, PH = 60, 210, 2780, 1890
rect(PX, PY, PW, PH, "#FFFFFF", rx=28, stroke=C_PROD, sw=6)
icon("globe", PX + 36, PY + 34, 52, C_PROD)
text(PX + 106, PY + 54, "PRODUCT", 24, True, C_PROD, ls=2)
text(PX + 106, PY + 98, title(prod), 44, True)
tx = PX + 106 + tw(title(prod), 44, True) + 28
version_chip(tx, PY + 60, prod)
if spec(prod).get("description"): text(PX + 106, PY + 138, spec(prod)["description"], 26, False, MUTED)
check_version(prod, "Product")

subs = [s for s in by.get("SubProduct", []) if spec(s).get("product") == name(prod)]
cons = by.get("Container", [])
stubs = [c for c in cons if spec(c).get("stub")]
SX0, SY, SH = PX + 50, PY + 180, PH - 230
stub_w = 620 if stubs else 0
avail = PW - 100 - (stub_w + 50 if stubs else 0)
sw_each = (avail - 40 * (len(subs) - 1)) / max(len(subs), 1)
groups = {name(g): g for g in by.get("Group", [])}

for i, s in enumerate(subs):
    sx = SX0 + i * (sw_each + 40)
    rect(sx, SY, sw_each, SH, "#F3FBFC", rx=24, stroke=C_SUB, sw=5)
    icon("puzzle_piece", sx + 32, SY + 30, 48, C_SUB)
    text(sx + 96, SY + 50, "DEELPRODUCT", 24, True, C_SUB, ls=2)
    text(sx + 96, SY + 92, title(s), 40, True)
    version_chip(sx + 96 + tw(title(s), 40, True) + 26, SY + 56, s)
    verb(sx + sw_each - 32, SY + 32, "releasen", C_PROD)
    verb(sx + sw_each - 32 - tw("releasen", 26, True) - 56, SY + 32, "deployen", C_SUB)
    check_version(s, "Deelproduct")
    g = groups.get(spec(s).get("owner"))
    if g:
        own = f"Eigenaar: squad {title(g)}"
        if spec(g).get("composition") == "ai-agents-only" and spec(g).get("owner"):
            own += f" (alleen AI-agents; aanspreekbaar: {spec(g)['owner']})"
        text(sx + 96, SY + 134, own, 24, False, MUTED)
    else: gap(f"Deelproduct {title(s)}: geen eigenaar")
    repos = [r for r in by.get("Repository", []) if spec(r).get("subProduct") == name(s)]
    if not repos and spec(s).get("repository"):
        # Eén repository voor het hele deelproduct (spec.repository van het deelproduct).
        repos = [{"kind": "Repository", "metadata": {"name": spec(s)["repository"]}, "spec": {"subProduct": name(s)}}]
    if not repos: gap(f"Deelproduct {title(s)}: geen repository (monorepo of per service)")
    mine = [c for c in cons if spec(c).get("subProduct") == name(s)]
    if not mine: gap(f"Deelproduct {title(s)}: geen containers")
    CY, CH = SY + 180, SH - 220
    cw = (sw_each - 80 - 36 * (len(mine) - 1)) / max(len(mine), 1)
    for j, c in enumerate(mine):
        cx = sx + 40 + j * (cw + 36)
        rect(cx, CY, cw, CH, "#FFFFFF", rx=20, stroke=C_CON, sw=4)
        icon("cube", cx + 28, CY + 28, 44, C_CON)
        text(cx + 86, CY + 46, "CONTAINER", 22, True, C_CON, ls=2)
        text(cx + 86, CY + 86, title(c), 36, True)
        verb(cx + cw - 28, CY + 28, "bouwen", C_CON)
        y = CY + 112
        version_chip(cx + 28, y, c); check_version(c, "Container")
        if spec(c).get("technology"): text(cx + 28, y + 96, spec(c)["technology"], 24, False, MUTED)
        y += 150
        add(f'<line x1="{cx+28}" y1="{y}" x2="{cx+cw-28}" y2="{y}" stroke="{RULE}" stroke-width="2"/>')
        # service
        text(cx + 28, y + 52, "Service", 26, True, INK)
        text(cx + 28, y + 84, "draait in de container", 22, False, MUTED)
        svcs = [v for v in by.get("Service", []) if spec(v).get("container") == name(c)]
        yy = y + 108
        if svcs:
            for v in svcs: chip(cx + 28, yy, title(v), C_CON); yy += 62
        else:
            chip(cx + 28, yy, "service ?", C_GAP, dashed=True); yy += 62
            gap(f"Container {title(c)}: geen service")
        y = yy + 30
        add(f'<line x1="{cx+28}" y1="{y}" x2="{cx+cw-28}" y2="{y}" stroke="{RULE}" stroke-width="2"/>')
        text(cx + 28, y + 52, "Gebouwd uit", 26, True, INK)
        # code
        text(cx + 28, y + 108, "Code", 24, True, C_CODE)
        text(cx + 28, y + 138, "uit een repository van het deelproduct", 22, False, MUTED)
        crepos = [r for r in repos if name(c) in (spec(r).get("containers") or [])] or (repos if len(repos) == 1 else [])
        yy = y + 160
        if crepos:
            for r in crepos:
                lab = title(r) + ("  ·  open source" if spec(r).get("openSource") else "")
                chip(cx + 28, yy, lab, C_CODE); yy += 62
        else:
            chip(cx + 28, yy, "repository ?", C_GAP, dashed=True); yy += 62
        # libraries
        y = yy + 26
        text(cx + 28, y + 30, "Libraries", 24, True, C_LIB)
        text(cx + 28, y + 60, "kunnen open source zijn", 22, False, MUTED)
        libs = [l for l in by.get("Library", []) if name(c) in (spec(l).get("containers") or [])]
        yy = y + 82
        if libs:
            for l in libs:
                lab = title(l) + (f" {spec(l)['version']}" if spec(l).get("version") else "") + ("  ·  open source" if spec(l).get("openSource") else "")
                chip(cx + 28, yy, lab, C_LIB); yy += 62
        else:
            chip(cx + 28, yy, "libraries ?", C_GAP, dashed=True)
            gap(f"Container {title(c)}: geen libraries")

if stubs:
    bx = PX + PW - 50 - stub_w
    text(bx, SY + 50, "STUBS", 24, True, MUTED, ls=2)
    for k, l in enumerate(wrap("Losse containers, geen onderdeel van een deelproduct. Ze staan voor deelproducten die er nog niet zijn.", 24, False, stub_w)):
        text(bx, SY + 88 + k * 32, l, 24, False, MUTED)
    y = SY + 180
    for c in stubs:
        rect(bx, y, stub_w, 150, "#FFFFFF", rx=20, stroke="#8A94A3", sw=4, dash="14 10")
        icon("cube", bx + 28, y + 28, 44, "#8A94A3")
        text(bx + 86, y + 46, "CONTAINER · STUB", 22, True, "#8A94A3", ls=2)
        text(bx + 86, y + 90, title(c), 36, True)
        version_chip(bx + stub_w - 28 - (tw("versie ?", 26, True) + 36), y + 82, c)
        y += 180

# ------------------------------------------------------------ rechterkolom
RX, RW = 2890, 890
rect(RX, PY, RW, 620, "#FFFFFF", rx=28)
text(RX + 40, PY + 70, "Drie werkwoorden", 36, True)
y = PY + 120
for vb, col, lvl, zin in [("bouwen", C_CON, "Container", "Code en libraries worden één container."),
                          ("deployen", C_SUB, "Deelproduct", "Eén versie van één deelproduct op één omgeving."),
                          ("releasen", C_PROD, "Deelproduct", "Eén versie van een deelproduct komt beschikbaar voor de gebruiker.")]:
    w = tw(vb, 26, True) + 40
    rect(RX + 40, y, w, 46, col, rx=23); text(RX + 40 + w/2, y + 32, vb, 26, True, "#FFFFFF", "middle")
    text(RX + 40 + w + 20, y + 33, lvl, 28, True)
    for k, l in enumerate(wrap(zin, 24, False, RW - 80)): text(RX + 40, y + 84 + k * 32, l, 24, False, MUTED)
    y += 162
GY = PY + 660
add('<g class="backlog">')
rect(RX, GY, RW, PH - 660, "#FFFFFF", rx=28, stroke=C_GAP if gaps else C_PROD, sw=4, dash="14 10" if gaps else None)
text(RX + 40, GY + 70, f"Backlog ({len(gaps)})" if gaps else "De backlog is leeg", 36, True, C_GAP if gaps else C_PROD)
text(RX + 40, GY + 112, "Wat het FCD-model vraagt en nog niet is ingevuld", 24, False, MUTED)
y = GY + 170
for g_ in gaps:
    ls_ = wrap(g_, 25, False, RW - 110)
    if y + len(ls_) * 34 > PY + PH - 30:
        text(RX + 40, y, "…", 25); break
    add(f'<circle cx="{RX+52}" cy="{y-9}" r="7" fill="{C_GAP}"/>')
    for k, l in enumerate(ls_): text(RX + 76, y + k * 34, l, 25)
    y += len(ls_) * 34 + 16
add('</g>')
add("</svg>")
if not TOON_BACKLOG: out = zonder_backlog(out); gaps = []
open(dst, "w").write("\n".join(out))
json.dump(gaps, open(dst + ".backlog.json", "w"), ensure_ascii=False)
print(len(gaps), "backlog"); [print(" -", g_) for g_ in gaps]
