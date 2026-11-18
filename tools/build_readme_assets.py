"""Poster-style profile README assets for github.com/fouad-barkaoui.

Every SVG embeds its own subsetted fonts (Anton, Caveat, Source Sans 3, the portfolio's
typefaces) and images as data URIs, so it renders identically inside GitHub's <img> sandbox.
Usage: python3 build.py <out_dir> <portfolio_src_assets_dir> <cutout.png>
"""
import base64, io, sys
from pathlib import Path
from xml.sax.saxutils import escape as esc
from fontTools.ttLib import TTFont
from fontTools import subset
from PIL import Image

OUT, SRC, CUTOUT = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
OUT.mkdir(parents=True, exist_ok=True)
NM = Path(__file__).parent / "node_modules/@fontsource"
FONTS = {
    "anton": NM / "anton/files/anton-latin-400-normal.woff2",
    "hand": NM / "caveat/files/caveat-latin-600-normal.woff2",
    "sans": NM / "source-sans-3/files/source-sans-3-latin-400-normal.woff2",
    "sans6": NM / "source-sans-3/files/source-sans-3-latin-600-normal.woff2",
}
FAMILY = {"anton": "A", "hand": "H", "sans": "S", "sans6": "S6"}

WALL, WALL_HI, INK, PAPER, ACID = "#6e1218", "#9a1d24", "#000000", "#ffffff", "#e4f222"
REDUCED = "@media (prefers-reduced-motion:reduce){*{animation:none!important}}"

_tt = {k: TTFont(v) for k, v in FONTS.items()}


def width(font, s, size):
    f = _tt[font]; cmap = f.getBestCmap(); hm = f["hmtx"]; upm = f["head"].unitsPerEm
    return sum(hm[cmap.get(ord(ch), cmap.get(32))][0] for ch in s) * size / upm


def face(font, text):
    """Subset a font to exactly the glyphs used and return an @font-face rule."""
    opts = subset.Options(); opts.flavor = "woff2"; opts.layout_features = ["kern", "liga"]
    f = TTFont(FONTS[font]); s = subset.Subsetter(opts)
    s.populate(text="".join(sorted(set(text + " ")))); s.subset(f)
    buf = io.BytesIO(); f.flavor = "woff2"; f.save(buf)
    b64 = base64.b64encode(buf.getvalue()).decode()
    return f"@font-face{{font-family:{FAMILY[font]};src:url(data:font/woff2;base64,{b64}) format('woff2')}}"


class Doc:
    def __init__(self, w, h, title):
        self.w, self.h, self.title, self.parts, self.css, self.used = w, h, title, [], [], {}

    def t(self, font, x, y, s, size, fill, extra=""):
        self.used[font] = self.used.get(font, "") + s
        return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FAMILY[font]}" font-size="{size:.1f}" '
                f'fill="{fill}" {extra}>{esc(s)}</text>')

    def add(self, *p): self.parts.extend(p)

    def render(self):
        faces = "".join(face(k, v) for k, v in self.used.items())
        return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
                f'width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" role="img" aria-label="{esc(self.title)}">'
                f'<title>{esc(self.title)}</title><style>{faces}{"".join(self.css)}{REDUCED}</style>'
                f'{"".join(self.parts)}</svg>')


def img_uri(im, fmt="WEBP", q=80):
    buf = io.BytesIO(); im.save(buf, fmt, quality=q, method=6)
    return f"data:image/{fmt.lower()};base64,{base64.b64encode(buf.getvalue()).decode()}"


GRAIN = ('<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" '
         'baseFrequency=".85" numOctaves="2" stitchTiles="stitch"/><feColorMatrix type="saturate" values="0"/>'
         '<feComponentTransfer><feFuncA type="table" tableValues="0 .5"/></feComponentTransfer></filter>')


def marquee(d, font, items, y, size, fill, dot, speed, x0=0, reverse=False, gap=34):
    """Seamless scrolling row of words separated by small dots."""
    seq, x = [], 0
    for it in items:
        seq.append(d.t(font, x, y, it, size, fill))
        x += width(font, it, size) + gap
        seq.append(f'<circle cx="{x - gap / 2:.1f}" cy="{y - size * .36:.1f}" r="{size * .11:.1f}" fill="{dot}"/>')
        x += gap * 0.05
    L = x
    reps = int(d.w // L) + 2
    body = "".join(f'<g transform="translate({k * L:.1f} 0)">{"".join(seq)}</g>' for k in range(reps))
    name = f"mq{len(d.css)}"
    frm, to = (f"-{L:.1f}px", "0px") if reverse else ("0px", f"-{L:.1f}px")
    d.css.append(f".{name}{{animation:{name} {L / speed:.1f}s linear infinite}}"
                 f"@keyframes {name}{{from{{transform:translateX({frm})}}to{{transform:translateX({to})}}}}")
    return f'<g transform="translate({x0} 0)"><g class="{name}">{body}</g></g>'


# =================================================================== HERO
def hero():
    W, H = 1200, 880
    d = Doc(W, H, "Fouad Barkaoui. SOC analyst and fullstack developer. Vibe coder and prompt engineer. Open to work, based in Morocco.")
    d.css.append("""
      .up{animation:up 1.1s cubic-bezier(.22,1,.36,1) both}
      @keyframes up{from{transform:translateY(380px)}}
      .me{animation:me 1.4s cubic-bezier(.22,1,.36,1) .25s both}
      @keyframes me{from{opacity:0;transform:translateY(40px)}}
      .draw{stroke-dasharray:2600;animation:draw 2.2s cubic-bezier(.65,0,.35,1) .9s both}
      @keyframes draw{from{stroke-dashoffset:2600}}
      .loop{stroke-dasharray:900;animation:loop 1s ease-out 2.6s both}
      @keyframes loop{from{stroke-dashoffset:900}}
      .fade{animation:fade .8s ease-out both}
      @keyframes fade{from{opacity:0}}
    """)
    cut = Image.open(CUTOUT).convert("RGBA")
    ph = 780; pw = round(cut.width * ph / cut.height)
    cut = cut.resize((pw, ph), Image.LANCZOS)
    # fade the photo's cropped edges into the wall
    a = cut.getchannel("A"); fade = Image.new("L", cut.size, 255); fp = fade.load()
    for yy in range(ph):
        for xx in range(pw):
            k = min(1, xx / 90, (pw - 1 - xx) / 90, (ph - 1 - yy) / 170 + .15)
            fp[xx, yy] = int(255 * max(0, k))
    from PIL import ImageChops
    cut.putalpha(ImageChops.multiply(a, fade))
    px, py = 600 - pw / 2 + 40, H - 64 - ph + 10
    d.add(f'''<defs>{GRAIN}
      <radialGradient id="spot" cx="56%" cy="42%" r="62%"><stop offset="0" stop-color="{WALL_HI}"/><stop offset=".6" stop-color="{WALL}"/><stop offset="1" stop-color="#3d070b"/></radialGradient>
      <clipPath id="l1"><rect x="0" y="40" width="{W}" height="360"/></clipPath>
    </defs>
    <rect width="{W}" height="{H}" fill="url(#spot)"/>''')

    # FOUAD: fills the width, sits behind the subject, letters rise one by one
    word = "FOUAD"; margin = 40
    size = (W - 2 * margin) / (width("anton", word, 1) )
    base = 40 + size * 0.735
    x = margin
    d.add('<g clip-path="url(#l1)">')
    for i, ch in enumerate(word):
        d.add(f'<g class="up" style="animation-delay:{i * .07:.2f}s">' + d.t("anton", x, base, ch, size, PAPER) + "</g>")
        x += width("anton", ch, size)
    d.add("</g>")

    # the subject, in front of FOUAD
    d.add(f'<g class="me"><image x="{px:.0f}" y="{py:.0f}" width="{pw}" height="{ph}" href="{img_uri(cut)}"/></g>')

    # BARKAOUI: outline drawn over the subject
    word2 = "BARKAOUI"
    s2 = (W - 2 * margin) / width("anton", word2, 1)
    b2 = H - 64 - 26
    d.add(d.t("anton", margin, b2, word2, s2, "none",
              f'class="draw" stroke="{PAPER}" stroke-width="2.5" stroke-linejoin="round"'))

    # top line + handwritten note
    d.add('<g class="fade" style="animation-delay:.6s">'
          + d.t("sans6", margin + 4, base + 46, "SOC analyst and fullstack developer.", 25, PAPER)
          + d.t("sans", margin + 4, base + 78, "Vibe coder and prompt engineer.", 25, PAPER, 'fill-opacity=".82"') + "</g>")
    note = "open to work"
    nx, ny = 880, base + 58
    nw = width("hand", note, 46)
    d.add(f'<g transform="rotate(-6 {nx + nw / 2:.0f} {ny})" class="fade" style="animation-delay:2.3s">'
          + d.t("hand", nx, ny, note, 46, ACID)
          + d.t("hand", nx + 22, ny + 38, "based in Morocco", 30, ACID, 'fill-opacity=".85"') + "</g>")
    cx, cy, rx, ry = nx + nw / 2 + 8, ny + 4, nw / 2 + 44, 54
    d.add(f'<path class="loop" d="M{cx - rx * .15:.0f} {cy - ry:.0f} A{rx:.0f} {ry} 0 1 0 {cx + rx * .12:.0f} {cy - ry + 3:.0f} l 34 9" '
          f'fill="none" stroke="{ACID}" stroke-width="3.5" stroke-linecap="round" transform="rotate(-6 {nx + nw / 2:.0f} {ny})"/>')

    # role ribbon
    d.add(f'<rect x="0" y="{H - 64}" width="{W}" height="64" fill="{INK}"/>')
    roles = ["Fullstack web developer", "SOC analyst", "Prompt engineer", "Vibe coder",
             "Problem solver", "Analytical thinker", "Cybersecurity enthusiast", "Fast, curious learner"]
    d.add(marquee(d, "anton", roles, H - 19, 30, PAPER, ACID, 70))
    d.add(f'<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".16" style="mix-blend-mode:overlay" pointer-events="none"/>')
    return d.render()


# ============================================================ PROJECTS
PROJECTS = [
    # slug, screenshot, name lines, two lines of copy, hand note, accent (shadow), note ink
    ("kanz", "kanz/news-dark.avif", ["KANZ"],
     ["A private workspace that keeps notes, tasks, articles,", "courses, docs and analytics on one spatial canvas."],
     "live at kanz-workspace.vercel.app", "#e4f222", "#5a6000"),
    ("windows", "windows/home.avif", ["WINDOWS", "FIELD MANUAL"],
     ["189 investigation commands for diagnosing, repairing,", "cleaning and hardening Windows, with 8 playbooks."],
     "live at windows-field-manual.vercel.app", "#5b5ff0", "#3a3dc4"),
    ("prompt", "prompt/crawl.avif", ["PROMPT", "ENGINE"],
     ["Reviews the prompts behind AI apps the way code gets", "reviewed: section by section, with a spec score."],
     "live at pebyfouad.vercel.app", "#18c1d2", "#0b7c88"),
    ("studio", "studio/home.avif", ["RESUME", "STUDIO"],
     ["Makes a resume readable to every ATS with a local AI.", "Nothing leaves the computer."],
     "runs fully offline", "#ff7a1a", "#c4520a"),
    ("assas", "assas/scan-sweep.avif", ["ASSAS"],
     ["Scans a whole codebase and reports every security", "finding in one place."],
     "still in the lab", "#ff3d9a", "#c2186f"),
]


def project(i, slug, shot, lines, copy, note, accent, note_ink):
    W, H = 1200, 540
    d = Doc(W, H, f"{' '.join(lines).title()}: {' '.join(copy)}")
    flip = i % 2 == 1
    d.add(f'<defs>{GRAIN}<clipPath id="win"><rect width="700" height="438" rx="14"/></clipPath></defs>'
          f'<rect width="{W}" height="{H}" fill="{PAPER}"/>')
    # screenshot: tilted, hard block shadow in the project colour, bleeding off the edge
    im = Image.open(SRC / shot).convert("RGB")
    s = max(700 / im.width, 438 / im.height); im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    left = 0 if slug == "assas" else (im.width - 700) // 2
    im = im.crop((left, 0, left + 700, 438))
    wx = 40 if flip else 560
    rot = 3 if flip else -3
    d.add(f'<g transform="translate({wx} 52) rotate({rot} 350 219)">'
          f'<rect x="22" y="22" width="700" height="438" rx="14" fill="{accent}"/>'
          f'<g clip-path="url(#win)"><image width="700" height="438" href="{img_uri(im, q=78)}"/></g>'
          f'<rect width="700" height="438" rx="14" fill="none" stroke="{INK}" stroke-width="3"/></g>')
    # giant name
    tx = 790 if flip else 44
    maxw = 370
    size = min(210 if len(lines) == 1 else 132, min(maxw / width("anton", ln, 1) for ln in lines))
    y = 60 + size * .74
    for ln in lines:
        d.add(d.t("anton", tx, y, ln, size, INK)); y += size * .92
    # copy
    words, rows, cur = " ".join(copy).split(), [], ""
    for wd in words:
        trial = (cur + " " + wd).strip()
        if width("sans", trial, 21) > maxw and cur: rows.append(cur); cur = wd
        else: cur = trial
    rows.append(cur)
    cy = 456 - 28 * len(rows)
    for k, ln in enumerate(rows):
        d.add(d.t("sans6" if k == 0 else "sans", tx, cy + k * 28, ln, 21, INK, '' if k == 0 else 'fill-opacity=".8"'))
    # handwritten note
    nx = tx; ny = 482
    d.add(f'<g transform="rotate(-3 {nx} {ny})">' + d.t("hand", nx, ny, note, 30, note_ink) + "</g>")
    nw = width("hand", note, 30)
    d.add(f'<path d="M{nx} {ny + 10} q {nw / 2:.0f} 9 {nw:.0f} -2" fill="none" stroke="{note_ink}" stroke-width="2.5" '
          f'stroke-linecap="round" transform="rotate(-3 {nx} {ny})"/>')
    d.add(f'<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".07" pointer-events="none"/>')
    return d.render()


# =============================================================== TAPES
def tapes():
    W, H = 1200, 360
    d = Doc(W, H, "Security: SOC monitoring, threat intel and OSINT, MITRE ATT&CK mapping, ELK Stack, OpenSearch, Kibana, Kali Linux. "
                  "Build: Python, TypeScript, React, Vite, Tailwind CSS, Three.js, FastAPI, Supabase, PostgreSQL, Docker, Vercel, Ollama, Claude.")
    sec = ["SOC monitoring", "Threat intel & OSINT", "MITRE ATT&CK mapping", "Offensive labs",
           "ELK Stack", "OpenSearch", "Kibana", "Kali Linux"]
    build = ["Python", "TypeScript", "React", "Vite", "Tailwind CSS", "Three.js", "FastAPI",
             "Supabase", "PostgreSQL", "Docker", "Vercel", "Ollama", "Claude"]
    d.add(f'<g transform="rotate(-8 600 180)"><rect x="-100" y="139" width="{W + 200}" height="82" fill="{INK}"/>'
          + marquee(d, "anton", sec, 197, 46, PAPER, ACID, 55, x0=-100) + "</g>")
    d.add(f'<g transform="rotate(7 600 180)"><rect x="-100" y="139" width="{W + 200}" height="82" fill="{ACID}"/>'
          + marquee(d, "anton", build, 197, 46, INK, INK, 55, x0=-100, reverse=True) + "</g>")
    return d.render()


# ============================================================== FOOTER
def footer():
    W, H = 1200, 420
    d = Doc(W, H, "Have an idea? Let's build it, and build it safe. Write to fouadbr2001@gmail.com")
    d.add(f'<defs>{GRAIN}<radialGradient id="spot" cx="30%" cy="40%" r="80%"><stop offset="0" stop-color="{WALL_HI}"/>'
          f'<stop offset="1" stop-color="#3d070b"/></radialGradient></defs><rect width="{W}" height="{H}" fill="url(#spot)"/>')
    line = "HAVE AN IDEA?"
    size = (W - 80) / width("anton", line, 1)
    d.add(d.t("anton", 40, 40 + size * .74, line, size, PAPER))
    d.add('<g transform="rotate(-3 300 330)">' + d.t("hand", 48, 330, "Let's build it, and build it safe.", 54, ACID) + "</g>")
    d.add(d.t("sans6", 50, 388, "Write to fouadbr2001@gmail.com", 24, PAPER, 'fill-opacity=".9"'))
    d.add(f'<rect width="{W}" height="{H}" filter="url(#grain)" opacity=".16" style="mix-blend-mode:overlay"/>')
    return d.render()


files = {"hero.svg": hero(), "stack.svg": tapes(), "contact.svg": footer()}
for i, p in enumerate(PROJECTS):
    files[f"project-{p[0]}.svg"] = project(i, *p)
for n, s in files.items():
    (OUT / n).write_text(s, encoding="utf-8"); print(f"{n:24s}{len(s) / 1024:7.1f} KB")
