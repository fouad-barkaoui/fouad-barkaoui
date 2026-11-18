"""Generate the animated SVG assets for the fouad-barkaoui GitHub profile README.

All assets share one palette and are fully self-contained (no external fonts,
scripts or network calls), so they render inside GitHub's <img> sandbox and
never break when a third-party stats service goes down.
"""
from pathlib import Path
from xml.sax.saxutils import escape as esc
import sys

OUT = Path(sys.argv[1] if len(sys.argv) > 1 else "assets")
OUT.mkdir(parents=True, exist_ok=True)

# ---------------------------------------------------------------- palette
BG, PANEL, PANEL2, LINE = "#08090a", "#0f1011", "#161718", "#23252a"
TEXT, MUTED, DIM = "#e8e9eb", "#8a8f98", "#5b616e"
ACID, CYAN, RED, INDIGO = "#e4f222", "#22c3d6", "#ff5a5f", "#7c80ff"

MONO = "'JetBrains Mono','Fira Code','Cascadia Code',SFMono-Regular,Consolas,'DejaVu Sans Mono',monospace"
SANS = "Inter,'Segoe UI',system-ui,-apple-system,'Helvetica Neue',Arial,sans-serif"
CW = 0.6  # monospace advance width / font-size, enforced with textLength

REDUCED = "@media (prefers-reduced-motion: reduce){*{animation:none!important}}"


def mono_len(s, size):
    return round(len(s) * size * CW, 1)


def svg(w, h, title, body, style=""):
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{w}" height="{h}" '
        f'viewBox="0 0 {w} {h}" role="img" aria-labelledby="t">'
        f'<title id="t">{esc(title)}</title>'
        f"<style>{style}{REDUCED}</style>{body}</svg>"
    )


def frame(w, h, rid="g"):
    """Rounded background with a faint grid."""
    return (
        f'<defs><pattern id="{rid}" width="32" height="32" patternUnits="userSpaceOnUse">'
        f'<path d="M32 0H0V32" fill="none" stroke="#ffffff" stroke-opacity=".035"/></pattern>'
        f'<clipPath id="{rid}c"><rect width="{w}" height="{h}" rx="16"/></clipPath></defs>'
        f'<rect width="{w}" height="{h}" rx="16" fill="{BG}"/>'
        f'<rect width="{w}" height="{h}" rx="16" fill="url(#{rid})"/>'
    )


def border(w, h, accent=ACID, dur=8):
    """Static hairline border plus a light that travels around it."""
    per = 2 * (w + h)
    return (
        f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="15.5" fill="none" stroke="{LINE}"/>'
        f'<rect class="run" x=".5" y=".5" width="{w-1}" height="{h-1}" rx="15.5" fill="none" '
        f'stroke="{accent}" stroke-width="1.5" stroke-dasharray="120 {per}" '
        f'style="animation:run{w}x{h} {dur}s linear infinite"/>'
        f'<style>@keyframes run{w}x{h}{{to{{stroke-dashoffset:-{per + 120}}}}}</style>'
    )


RUN_KF = ""


def mtext(x, y, s, size, fill, extra="", fixed=True):
    tl = f' textLength="{mono_len(s, size)}" lengthAdjust="spacingAndGlyphs"' if fixed else ""
    return (f'<text x="{x}" y="{y}" font-family="{MONO}" font-size="{size}" fill="{fill}"'
            f'{tl} {extra}>{esc(s)}</text>')


# =================================================================== HERO
def hero():
    W, H = 1200, 420
    roles = ["SOC Analyst", "Fullstack Developer", "Prompt Engineer",
             "Reverse Engineer", "Digital Investigator"]
    slot, n = 4, len(roles)
    cyc = slot * n
    p = 100 / n  # percent of cycle owned by each role

    css = [RUN_KF, f"""
    .blink{{animation:blink 1.1s steps(1) infinite}}
    @keyframes blink{{50%{{opacity:0}}}}
    .scan{{animation:scan 7s linear infinite}}
    @keyframes scan{{from{{transform:translateY(-40px)}}to{{transform:translateY({H}px)}}}}
    .sweep{{transform-origin:930px 222px;animation:spin 6s linear infinite}}
    @keyframes spin{{to{{transform:rotate(360deg)}}}}
    .ring{{transform-box:fill-box;transform-origin:center;animation:ring 3s ease-out infinite}}
    @keyframes ring{{from{{transform:scale(.4);opacity:.9}}to{{transform:scale(2.6);opacity:0}}}}
    .flow{{animation:flow 2.4s linear infinite}}
    @keyframes flow{{to{{stroke-dashoffset:-40}}}}
    .gl1{{animation:gl1 7s infinite}} .gl2{{animation:gl2 7s infinite}}
    @keyframes gl1{{0%,91%,100%{{transform:none;opacity:0}}92%{{transform:translate(-4px,1px);opacity:.75}}94%{{transform:translate(3px,-2px);opacity:.75}}96%{{transform:none;opacity:0}}}}
    @keyframes gl2{{0%,91%,100%{{transform:none;opacity:0}}92%{{transform:translate(4px,-1px);opacity:.75}}94%{{transform:translate(-3px,2px);opacity:.75}}96%{{transform:none;opacity:0}}}}
    .in{{opacity:0;animation:in .8s ease-out forwards}}
    @keyframes in{{from{{opacity:0;transform:translateY(8px)}}to{{opacity:1;transform:none}}}}
    """]

    b = [frame(W, H, "hg")]
    b.append(f'''<defs>
      <radialGradient id="gA" cx="20%" cy="35%" r="55%"><stop offset="0" stop-color="{ACID}" stop-opacity=".10"/><stop offset="1" stop-color="{ACID}" stop-opacity="0"/></radialGradient>
      <radialGradient id="gC" cx="78%" cy="55%" r="45%"><stop offset="0" stop-color="{CYAN}" stop-opacity=".12"/><stop offset="1" stop-color="{CYAN}" stop-opacity="0"/></radialGradient>
      <linearGradient id="sw" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{ACID}" stop-opacity="0"/><stop offset="1" stop-color="{ACID}" stop-opacity=".22"/></linearGradient>
      <linearGradient id="sl" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{ACID}" stop-opacity="0"/><stop offset="1" stop-color="{ACID}" stop-opacity=".07"/></linearGradient>
    </defs>
    <g clip-path="url(#hgc)">
      <rect width="{W}" height="{H}" fill="url(#gA)"/><rect width="{W}" height="{H}" fill="url(#gC)"/>
      <rect class="scan" width="{W}" height="40" fill="url(#sl)"/>
    </g>''')

    # window chrome
    b.append(f'<path d="M0 16a16 16 0 0 1 16-16h{W-32}a16 16 0 0 1 16 16v26H0z" fill="{PANEL}"/>'
             f'<line x1="0" y1="42" x2="{W}" y2="42" stroke="{LINE}"/>')
    for i, c in enumerate(["#3a3d44", "#3a3d44", "#3a3d44"]):
        b.append(f'<circle cx="{24 + i*18}" cy="21" r="5.5" fill="{c}"/>')
    t = "fouad@sentinel: ~/profile"
    b.append(mtext(W/2 - mono_len(t, 13)/2, 26, t, 13, MUTED))
    b.append(f'<circle class="blink" cx="{W-92}" cy="21" r="4" fill="{ACID}"/>')
    b.append(mtext(W-80, 26, "ONLINE", 12, ACID, 'letter-spacing="1"'))

    # left identity block
    x0 = 56
    lab = "// SOC ANALYST  ·  FULLSTACK DEVELOPER  ·  PROMPT ENGINEER"
    b.append(f'<g class="in" style="animation-delay:.1s">{mtext(x0, 108, lab, 13, ACID)}</g>')
    name = "FOUAD BARKAOUI"
    nm = (f'font-family="{SANS}" font-size="66" font-weight="800" letter-spacing="1" '
          f'textLength="560" lengthAdjust="spacingAndGlyphs"')
    b.append(f'<g class="in" style="animation-delay:.25s">'
             f'<text class="gl1" x="{x0}" y="182" {nm} fill="{CYAN}">{name}</text>'
             f'<text class="gl2" x="{x0}" y="182" {nm} fill="{RED}">{name}</text>'
             f'<text x="{x0}" y="182" {nm} fill="{TEXT}">{name}</text></g>')

    # typed role field
    fy, fh, fw = 212, 50, 560
    b.append(f'<g class="in" style="animation-delay:.45s">'
             f'<rect x="{x0}" y="{fy}" width="{fw}" height="{fh}" rx="10" fill="{PANEL}" stroke="{LINE}"/>'
             f'<clipPath id="fld"><rect x="{x0 + 1}" y="{fy + 1}" width="{fw - 2}" height="{fh - 2}" rx="9"/></clipPath>')
    b.append(mtext(x0 + 18, fy + 32, "role >", 15, DIM))
    tx, size = x0 + 92, 22
    b.append('<g clip-path="url(#fld)">')
    for i, r in enumerate(roles):
        L = mono_len(r, size)
        n_ch = len(r)
        a, ty, hold, er = i * p, i * p + p * .30, i * p + p * .80, i * p + p * .95
        css.append(f"""
        .r{i}{{animation:r{i} {cyc}s linear infinite both}}
        @keyframes r{i}{{0%,{a:.2f}%{{opacity:0}}{a + .01:.2f}%{{opacity:1}}{er:.2f}%{{opacity:1}}{er + .01:.2f}%,100%{{opacity:0}}}}
        .c{i}{{animation:c{i} {cyc}s infinite both}}
        @keyframes c{i}{{0%,{a:.2f}%{{transform:translateX(0);animation-timing-function:steps({n_ch})}}
          {ty:.2f}%,{hold:.2f}%{{transform:translateX({L}px);animation-timing-function:steps({n_ch})}}
          {er:.2f}%,100%{{transform:translateX(0)}}}}""")
        b.append(
            f'<g class="r{i}" opacity="{1 if i == 0 else 0}">'
            f'{mtext(tx, fy + 33, r, size, TEXT)}'
            f'<g class="c{i}" transform="translate({L} 0)">'
            f'<rect x="{tx}" y="{fy + 8}" width="{L + 14}" height="{fh - 16}" fill="{PANEL}"/>'
            f'<rect class="blink" x="{tx + 1}" y="{fy + 13}" width="11" height="24" fill="{ACID}"/></g></g>')
    b.append("</g></g>")

    tag = "I turn ideas into working products: fast, clean and secure by default."
    b.append(f'<g class="in" style="animation-delay:.65s"><text x="{x0}" y="300" font-family="{SANS}" '
             f'font-size="17" fill="{MUTED}">{esc(tag)}</text></g>')

    # focus chips
    chips = [("DFIR", RED), ("MALWARE ANALYSIS", RED), ("THREAT HUNTING", CYAN), ("CTI / OSINT", CYAN), ("WEB ENGINEERING", ACID)]
    cx = x0
    b.append('<g class="in" style="animation-delay:.85s">')
    for label, col in chips:
        w = mono_len(label, 11) + 30
        b.append(f'<rect x="{cx}" y="322" width="{w}" height="26" rx="13" fill="{col}" fill-opacity=".07" stroke="{col}" stroke-opacity=".45"/>'
                 f'<circle cx="{cx + 12}" cy="335" r="3" fill="{col}"/>'
                 + mtext(cx + 21, 339, label, 11, TEXT, 'letter-spacing=".5"'))
        cx += w + 8
    b.append("</g>")

    # right: lab topology / radar
    C = (930, 222)
    b.append(f'<g opacity=".9">')
    for r in (60, 112, 164):
        b.append(f'<circle cx="{C[0]}" cy="{C[1]}" r="{r}" fill="none" stroke="#ffffff" stroke-opacity=".06" stroke-dasharray="2 6"/>')
    b.append(f'<path class="sweep" d="M{C[0]} {C[1]} L{C[0] + 164} {C[1]} A164 164 0 0 0 {C[0] + 142} {C[1] - 82} Z" fill="url(#sw)"/>')
    nodes = {
        "SIEM": (930, 222, ACID), "pfSense": (800, 128, CYAN), "PROXMOX": (1072, 118, CYAN),
        "SENSOR": (792, 318, CYAN), "IRIS": (1080, 322, CYAN), "TAP": (700, 236, DIM),
        "": (1150, 220, DIM),
    }
    edges = [("SIEM", "pfSense"), ("SIEM", "PROXMOX"), ("SIEM", "SENSOR"), ("SIEM", "IRIS"),
             ("pfSense", "TAP"), ("SENSOR", "TAP"), ("PROXMOX", ""), ("IRIS", ""), ("pfSense", "PROXMOX")]
    paths = []
    for k, (a, z) in enumerate(edges):
        ax, ay, _ = nodes[a]; zx, zy, _ = nodes[z]
        d = f"M{ax} {ay}L{zx} {zy}"
        paths.append((d, a, z))
        b.append(f'<path d="{d}" fill="none" stroke="#ffffff" stroke-opacity=".12"/>'
                 f'<path id="e{k}" class="flow" d="{d}" fill="none" stroke="{CYAN}" stroke-opacity=".35" stroke-dasharray="3 17"/>')
    # packets travelling along edges (SMIL)
    for k, dur, col, rev in [(0, 3.2, ACID, False), (1, 2.6, CYAN, True), (2, 3.8, ACID, True),
                             (3, 2.9, CYAN, False), (5, 3.4, ACID, False), (8, 4.2, CYAN, False)]:
        kp = 'keyPoints="1;0" keyTimes="0;1" calcMode="linear"' if rev else ""
        b.append(f'<circle r="3" fill="{col}"><animateMotion dur="{dur}s" repeatCount="indefinite" {kp}>'
                 f'<mpath xlink:href="#e{k}"/></animateMotion></circle>')
    # hostile packet dropped at the firewall
    b.append(f'<path id="thr" d="M700 52L800 128" stroke="{RED}" stroke-opacity=".25" stroke-dasharray="2 5"/>'
             f'<circle r="3.5" fill="{RED}"><animateMotion dur="5s" repeatCount="indefinite" keyPoints="0;1;1" keyTimes="0;.4;1" calcMode="linear"><mpath xlink:href="#thr"/></animateMotion>'
             f'<animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.4;.42;1" dur="5s" repeatCount="indefinite"/></circle>'
             f'<circle cx="800" cy="128" r="10" fill="none" stroke="{RED}" opacity="0">'
             f'<animate attributeName="opacity" values="0;0;1;0;0" keyTimes="0;.4;.42;.6;1" dur="5s" repeatCount="indefinite"/>'
             f'<animate attributeName="r" values="6;6;6;22;22" keyTimes="0;.4;.42;.6;1" dur="5s" repeatCount="indefinite"/></circle>'
             + f'<g opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.41;.43;.75;.8" dur="5s" repeatCount="indefinite"/>'
             + mtext(712, 104, "DROP", 10, RED, 'letter-spacing="1"') + "</g>")
    for label, (x, y, col) in nodes.items():
        big = label == "SIEM"
        rr = 7 if big else 5
        b.append(f'<circle class="ring" cx="{x}" cy="{y}" r="{rr}" fill="none" stroke="{col}" style="animation-delay:{(x % 7) * .35:.2f}s"/>'
                 f'<circle cx="{x}" cy="{y}" r="{rr}" fill="{BG}" stroke="{col}" stroke-width="2"/>'
                 f'<circle cx="{x}" cy="{y}" r="{rr - 3.5}" fill="{col}"/>')
        if label:
            b.append(mtext(x - mono_len(label, 10) / 2, y + (26 if y > 200 else -16), label, 10, MUTED, 'letter-spacing=".5"'))
    b.append("</g>")

    # status strip
    b.append(f'<line x1="24" y1="378" x2="{W-24}" y2="378" stroke="{LINE}"/>')
    items = [("STATUS", "ONLINE", ACID), ("FOCUS", "DFIR / MALWARE ANALYSIS", TEXT),
             ("LAB", "PROXMOX · PFSENSE · SIEM", TEXT), ("BASE", "MOROCCO · UTC+0", TEXT)]
    sx = 56
    for k, v, col in items:
        b.append(mtext(sx, 403, k, 11, DIM, 'letter-spacing="1"'))
        sx += mono_len(k, 11) + 12
        b.append(mtext(sx, 403, v, 11, col, 'letter-spacing=".5"'))
        sx += mono_len(v, 11) + 40
    b.append(border(W, H, ACID, 10))
    return svg(W, H, "Fouad Barkaoui — Digital Investigator, Reverse Engineer, Builder",
               "".join(b), "".join(css))


# ================================================================ WHOAMI
def whoami():
    W = 1200
    rows = [
        ("name", "Fouad Barkaoui", TEXT),
        ("role", "SOC Analyst  ·  Fullstack Developer  ·  Vibe Coder  ·  Prompt Engineer", TEXT),
        ("security", "SOC monitoring  ·  Threat intel & OSINT  ·  MITRE ATT&CK mapping  ·  Offensive labs", TEXT),
        ("shipped", "Kanz  ·  Windows Field Manual  ·  Prompt Engine  ·  Resume Studio  ·  ASSAS", ACID),
        ("lab", "Multi-node SOC lab: Proxmox VE, pfSense, inline packet brokers", TEXT),
        ("research", "PE memory dumping  ·  IAT reconstruction  ·  malware analysis", TEXT),
        ("speaks", "Darija  ·  Arabic  ·  French  ·  English", TEXT),
        ("status", "open to work  ·  based in Morocco", ACID),
        ("note", "the most powerful repos are private. ask for a walkthrough.", MUTED),
    ]
    top, lh, size = 104, 30, 15
    H = top + lh * len(rows) + 70
    css = [RUN_KF, """
    .blink{animation:blink 1.1s steps(1) infinite}
    @keyframes blink{50%{opacity:0}}
    .ln{opacity:0;animation:ln .35s ease-out forwards}
    @keyframes ln{from{opacity:0;transform:translateX(-6px)}to{opacity:1;transform:none}}
    """]
    b = [frame(W, H, "wg")]
    b.append(f'<path d="M0 16a16 16 0 0 1 16-16h{W-32}a16 16 0 0 1 16 16v26H0z" fill="{PANEL}"/>'
             f'<line x1="0" y1="42" x2="{W}" y2="42" stroke="{LINE}"/>')
    for i in range(3):
        b.append(f'<circle cx="{24 + i*18}" cy="21" r="5.5" fill="#3a3d44"/>')
    t = "whoami — zsh"
    b.append(mtext(W/2 - mono_len(t, 13)/2, 26, t, 13, MUTED))

    x0 = 40
    prompt = "fouad@sentinel:~$"
    cmd = "whoami --verbose"
    py = 78
    b.append(mtext(x0, py, prompt, size, ACID))
    cx = x0 + mono_len(prompt + " ", size)
    L = mono_len(cmd, size)
    t_type = 1.4
    css.append(f".cmd{{animation:cmd {t_type}s steps({len(cmd)}) .3s both}}"
               f"@keyframes cmd{{from{{transform:translateX(0)}}to{{transform:translateX({L}px)}}}}")
    b.append(mtext(cx, py, cmd, size, TEXT))
    b.append(f'<g class="cmd" transform="translate({L} 0)"><rect x="{cx}" y="{py - 17}" width="{L + 12}" height="24" fill="{BG}"/>'
             f'<rect x="{cx + 1}" y="{py - 15}" width="9" height="19" fill="{ACID}" opacity=".9"/></g>')

    start = .3 + t_type + .25
    b.append(f'<line x1="{x0}" y1="{top - 12}" x2="{W - x0}" y2="{top - 12}" stroke="{LINE}" class="ln" style="animation-delay:{start:.2f}s"/>')
    keyw = 12
    for i, (k, v, col) in enumerate(rows):
        y = top + 14 + i * lh
        d = start + .12 * (i + 1)
        b.append(f'<g class="ln" style="animation-delay:{d:.2f}s">'
                 f'<rect x="{x0}" y="{y - 13}" width="3" height="18" fill="{ACID if col == ACID else LINE}"/>'
                 + mtext(x0 + 18, y, k, size, CYAN)
                 + mtext(x0 + 18 + mono_len(" " * keyw, size), y, v, size, col, fixed=False) + "</g>")
    fy = top + 14 + len(rows) * lh + 18
    d = start + .12 * (len(rows) + 2)
    b.append(f'<g class="ln" style="animation-delay:{d:.2f}s">' + mtext(x0, fy, prompt, size, ACID)
             + f'<rect class="blink" x="{x0 + mono_len(prompt + " ", size) + 1}" y="{fy - 15}" width="9" height="19" fill="{ACID}"/></g>')
    b.append(border(W, H, CYAN, 12))
    return svg(W, H, "whoami: Fouad Barkaoui profile summary", "".join(b), "".join(css))


# =============================================================== ARSENAL
def arsenal():
    W = 1200
    cols = [
        ("REVERSE ENGINEERING", RED, ["x64dbg", "Scylla / ScyllaHide", "PE format internals", "Memory dumping", "IAT reconstruction", "Anti-debug evasion"]),
        ("DFIR · THREAT HUNTING", CYAN, ["MITRE ATT&CK / ATLAS", "Packet analysis", "DFIR IRIS", "ELK Stack", "OpenSearch", "CTI · OSINT recon"]),
        ("ENGINEERING", ACID, ["TypeScript", "React · Vite", "Radix UI · Tailwind", "GSAP · Three.js", "Supabase", "Python · PHP"]),
        ("INFRA · DEVOPS", INDIGO, ["Proxmox VE (Type-1)", "pfSense", "Docker Compose", "Linux · WSL", "PowerShell automation", "Inline packet brokers"]),
    ]
    pad, gap, top = 32, 16, 92
    cw = (W - 2 * pad - 3 * gap) / 4
    rh = 40
    ch = 60 + rh * 6 + 10
    H = top + ch + 32
    css = [RUN_KF, """
    .ln{opacity:0;animation:ln .5s ease-out forwards}
    @keyframes ln{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}
    .bar{animation:bar 3.2s ease-in-out infinite}
    @keyframes bar{0%,100%{opacity:.55}50%{opacity:1}}
    """]
    b = [frame(W, H, "ag")]
    b.append(mtext(pad, 50, "// ARSENAL", 13, ACID, 'letter-spacing="2"'))
    b.append(f'<text x="{pad}" y="76" font-family="{SANS}" font-size="15" fill="{MUTED}">'
             f'Tools I use daily, from the debugger to the hypervisor.</text>')
    for ci, (title, col, items) in enumerate(cols):
        x = pad + ci * (cw + gap)
        b.append(f'<g class="ln" style="animation-delay:{.1 + ci * .12:.2f}s">'
                 f'<rect x="{x}" y="{top}" width="{cw:.1f}" height="{ch}" rx="12" fill="{PANEL}" stroke="{LINE}"/>'
                 f'<rect class="bar" x="{x + 16}" y="{top}" width="{cw - 32:.1f}" height="2" fill="{col}" style="animation-delay:{ci * .6:.1f}s"/>'
                 + mtext(x + 18, top + 36, title, 12, col, 'letter-spacing="1.2"')
                 + mtext(x + cw - 18 - mono_len("0" + str(len(items)), 11), top + 36, f"0{len(items)}", 11, DIM)
                 + f'<line x1="{x + 18}" y1="{top + 52}" x2="{x + cw - 18:.1f}" y2="{top + 52}" stroke="{LINE}"/></g>')
        for ri, it in enumerate(items):
            y = top + 60 + ri * rh
            d = .35 + ci * .12 + ri * .07
            b.append(f'<g class="ln" style="animation-delay:{d:.2f}s">'
                     f'<rect x="{x + 12}" y="{y + 4}" width="{cw - 24:.1f}" height="{rh - 8}" rx="7" fill="{PANEL2}"/>'
                     f'<rect x="{x + 24}" y="{y + rh/2 - 3}" width="6" height="6" rx="1.5" fill="{col}"/>'
                     + mtext(x + 40, y + rh/2 + 5, it, 13.5, TEXT, fixed=False)
                     + "</g>")
    b.append(border(W, H, ACID, 12))
    return svg(W, H, "Arsenal: reverse engineering, DFIR, engineering and infrastructure tools", "".join(b), "".join(css))


# ================================================================= CARDS
def card(code, cat, title, desc_lines, tags, status, scol, accent):
    W, H = 590, 250
    css = [RUN_KF, """
    .pulse{transform-box:fill-box;transform-origin:center;animation:pulse 2s ease-out infinite}
    @keyframes pulse{from{transform:scale(1);opacity:.8}to{transform:scale(3);opacity:0}}
    .ret{animation:ret 4s ease-in-out infinite}
    @keyframes ret{0%,100%{opacity:.35}50%{opacity:1}}
    """]
    b = [frame(W, H, "cg")]
    b.append(f'<defs><radialGradient id="cgl" cx="100%" cy="0%" r="70%"><stop offset="0" stop-color="{accent}" stop-opacity=".12"/>'
             f'<stop offset="1" stop-color="{accent}" stop-opacity="0"/></radialGradient></defs>'
             f'<rect width="{W}" height="{H}" rx="16" fill="url(#cgl)"/>')
    # corner reticle
    b.append(f'<g class="ret" stroke="{accent}" stroke-width="1.5" fill="none">'
             f'<path d="M{W-56} 22h34v34"/><path d="M{W-22} {H-56}v34h-34"/></g>')
    b.append(mtext(28, 44, f"{code}  /  {cat}", 12, DIM, 'letter-spacing="1.2"'))
    # status pill
    sw = mono_len(status, 11) + 34
    sx = 28
    b.append(f'<rect x="{sx}" y="{H - 52}" width="{sw}" height="26" rx="13" fill="{scol}" fill-opacity=".08" stroke="{scol}" stroke-opacity=".5"/>'
             f'<circle class="pulse" cx="{sx + 14}" cy="{H - 39}" r="3.5" fill="{scol}"/><circle cx="{sx + 14}" cy="{H - 39}" r="3.5" fill="{scol}"/>'
             + mtext(sx + 24, H - 35, status, 11, scol, 'letter-spacing="1"'))
    b.append(f'<text x="28" y="86" font-family="{SANS}" font-size="28" font-weight="700" fill="{TEXT}">{esc(title)}</text>')
    for i, ln in enumerate(desc_lines):
        b.append(f'<text x="28" y="{118 + i * 23}" font-family="{SANS}" font-size="15" fill="{MUTED}">{esc(ln)}</text>')
    tx = sx + sw + 10
    for tg in tags:
        w = mono_len(tg, 10.5) + 20
        b.append(f'<rect x="{tx}" y="{H - 52}" width="{w}" height="26" rx="6" fill="{PANEL2}" stroke="{LINE}"/>'
                 + mtext(tx + 10, H - 35, tg, 10.5, TEXT, 'letter-spacing=".5"'))
        tx += w + 6
    b.append(border(W, H, accent, 9))
    return svg(W, H, f"{title}: {' '.join(desc_lines)}", "".join(b), "".join(css))


CARDS = {
    "card-sentinel-lab": ("OP-01", "INFRASTRUCTURE", "Sentinel Lab",
        ["Multi-node home SOC built on Proxmox VE and pfSense,", "with inline packet brokers for live threat hunting."],
        ["PROXMOX", "PFSENSE", "SIEM", "PCAP"], "ACTIVE", ACID, CYAN),
    "card-ops-console": ("OP-02", "SIMULATION", "Sentinel Ops Console",
        ["Offline, single-file SOC lab simulator", "rendered in Three.js. Runs anywhere, no backend."],
        ["THREE.JS", "HTML", "OFFLINE"], "BUILDING", CYAN, INDIGO),
    "card-nexus": ("OP-03", "PRODUCT", "Nexus",
        ["Local-first spatial workspace: notes, tasks and docs,", "synced to Supabase with per-user row-level security."],
        ["REACT", "TYPESCRIPT", "SUPABASE", "GSAP"], "ACTIVE", ACID, ACID),
    "card-malware-lab": ("OP-04", "RESEARCH", "Malware Analysis",
        ["Low-level investigations: PE memory dumping,", "IAT de-obfuscation and anti-debug bypass."],
        ["X64DBG", "SCYLLA", "PE", "ATT&CK"], "ONGOING", RED, RED),
}


# ================================================================ FOOTER
def footer():
    W, H = 1200, 110
    css = ["""
    .wave{animation:wave 4s linear infinite}
    @keyframes wave{to{stroke-dashoffset:-1200}}
    .blink{animation:blink 1.1s steps(1) infinite}
    @keyframes blink{50%{opacity:0}}
    """]
    # stylised signal trace: flat, spike (packet), flat
    pts, x = [], 0
    while x <= W:
        y = 40
        m = x % 300
        if 130 < m < 170:
            y = 40 + [0, -14, 18, -26, 10, -6, 0][int((m - 130) / 6)]
        pts.append(f"{x},{y}")
        x += 6
    d = "M" + " L".join(pts)
    b = [f'<defs><linearGradient id="fd" x1="0" x2="1"><stop offset="0" stop-color="{ACID}" stop-opacity="0"/>'
         f'<stop offset=".5" stop-color="{ACID}"/><stop offset="1" stop-color="{ACID}" stop-opacity="0"/></linearGradient></defs>',
         f'<path d="{d}" fill="none" stroke="{LINE}" stroke-width="1.5"/>',
         f'<path class="wave" d="{d}" fill="none" stroke="url(#fd)" stroke-width="2" stroke-dasharray="220 980"/>']
    t = "// END OF TRANSMISSION"
    b.append(mtext(W/2 - mono_len(t, 13)/2, 86, t, 13, MUTED, 'letter-spacing="2"'))
    b.append(f'<rect class="blink" x="{W/2 + mono_len(t, 13)/2 + 6}" y="74" width="8" height="15" fill="{ACID}"/>')
    return svg(W, H, "End of transmission", "".join(b), "".join(css))


# ======================================================== SECTION LABELS
def section(label, sub, accent=ACID):
    W, H = 1200, 64
    css = """.dot{animation:blink 1.6s steps(1) infinite}@keyframes blink{50%{opacity:.2}}"""
    b = [f'<rect width="{W}" height="{H}" rx="12" fill="{BG}" stroke="{LINE}"/>',
         f'<rect x="0" y="16" width="3" height="32" fill="{accent}"/>',
         f'<circle class="dot" cx="28" cy="32" r="4" fill="{accent}"/>',
         mtext(44, 37, label, 14, accent, 'letter-spacing="2"'),
         f'<text x="{44 + mono_len(label, 14) + 22}" y="37" font-family="{SANS}" font-size="15" fill="{MUTED}">{esc(sub)}</text>']
    return svg(W, H, f"{label} — {sub}", "".join(b), css)


files = {"hero.svg": hero(), "whoami.svg": whoami(), "arsenal.svg": arsenal(), "footer.svg": footer(),
         "sec-work.svg": section("// SHIPPED", "Real products, built end to end. Click any card to open it."),
         "sec-telemetry.svg": section("// TELEMETRY", "Contribution signal, refreshed daily.", CYAN)}
for name, data in files.items():
    (OUT / name).write_text(data, encoding="utf-8")
    print(f"{name:28s} {len(data)/1024:6.1f} KB")
