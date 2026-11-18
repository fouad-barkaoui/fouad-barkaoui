"""Frame real portfolio screenshots into uniform project cards for the profile README."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter

SRC = Path(sys.argv[1])          # portfolio/src/assets
OUT = Path(sys.argv[2]); OUT.mkdir(parents=True, exist_ok=True)

BG, PANEL, LINE = (8, 9, 10), (15, 16, 17), (35, 37, 42)
TEXT, MUTED = (232, 233, 235), (138, 143, 152)
ACID, CYAN, RED, INDIGO = (228, 242, 34), (34, 195, 214), (255, 90, 95), (124, 128, 255)
F = "/usr/share/fonts/opentype/inter/"
MONO = "/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf"
bold = ImageFont.truetype(F + "Inter-Bold.otf", 40)
med = ImageFont.truetype(F + "Inter-Medium.otf", 21)
mono = ImageFont.truetype(MONO, 18)
monos = ImageFont.truetype(MONO, 15)

W, H = 1200, 860
SX, SY, SW, SH = 28, 28, W - 56, 690  # screenshot window


def rounded(im, r):
    m = Image.new("L", im.size, 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, im.width - 1, im.height - 1], r, fill=255)
    out = Image.new("RGBA", im.size); out.paste(im, (0, 0), m); return out


def cover(im, w, h, anchor_top=True, left=False):
    s = max(w / im.width, h / im.height)
    im = im.resize((round(im.width * s), round(im.height * s)), Image.LANCZOS)
    x = 0 if left else (im.width - w) // 2
    y = 0 if anchor_top else (im.height - h) // 2
    return im.crop((x, y, x + w, y + h))


def card(slug, shot, name, kind, status, scol, link_label, accent):
    c = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(c)
    # accent glow behind the screenshot
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ImageDraw.Draw(glow).rounded_rectangle([SX + 60, SY + 40, SX + SW - 60, SY + SH], 30, fill=accent + (70,))
    c.paste(glow.filter(ImageFilter.GaussianBlur(40)), (0, 0), glow.filter(ImageFilter.GaussianBlur(40)))
    d.rounded_rectangle([0, 0, W - 1, H - 1], 22, outline=LINE, width=2)
    im = Image.open(SRC / shot).convert("RGB")
    win = rounded(cover(im, SW, SH, left=slug == "work-assas"), 14)
    c.paste(win, (SX, SY), win)
    d.rounded_rectangle([SX, SY, SX + SW, SY + SH], 14, outline=LINE, width=2)
    # footer
    fy = SY + SH + 30
    d.rectangle([SX, fy + 6, SX + 4, fy + 50], fill=accent)
    d.text((SX + 22, fy - 2), name, font=bold, fill=TEXT)
    d.text((SX + 24, fy + 52), kind, font=med, fill=MUTED)
    # status pill
    tw = d.textlength(status, font=monos)
    px = W - SX - tw - 46
    d.rounded_rectangle([px, fy + 4, W - SX, fy + 38], 17, fill=tuple(int(v * .12) for v in scol), outline=scol, width=2)
    d.ellipse([px + 14, fy + 16, px + 24, fy + 26], fill=scol)
    d.text((px + 32, fy + 11), status, font=monos, fill=scol)
    lw = d.textlength(link_label + "  ->", font=mono)
    d.text((W - SX - lw, fy + 54), link_label + "  ->", font=mono, fill=TEXT)
    c.save(OUT / f"{slug}.webp", "WEBP", quality=82, method=6)
    return slug


PROJECTS = [
    ("work-kanz", "kanz/news-dark.avif", "Kanz", "Private spatial workspace · React, Supabase", "LIVE", ACID, "kanz-workspace.vercel.app", ACID),
    ("work-windows", "windows/home.avif", "Windows Field Manual", "189 investigation commands · 8 playbooks", "LIVE", ACID, "windows-field-manual.vercel.app", INDIGO),
    ("work-prompt", "prompt/crawl.avif", "Prompt Engine", "Prompt review and spec scoring · PEbyFOUAD", "LIVE", ACID, "pebyfouad.vercel.app", CYAN),
    ("work-studio", "studio/home.avif", "Resume Studio", "Offline AI resume and ATS optimizer", "LOCAL", CYAN, "case study", (255, 170, 60)),
    ("work-assas", "assas/scan-sweep.avif", "ASSAS", "Codebase security scanner · SaaS", "IN DEVELOPMENT", RED, "case study", RED),
]
for p in PROJECTS:
    print(card(*p))

# portfolio card: portrait + pointer to all case studies
c = Image.new("RGB", (W, H), BG); d = ImageDraw.Draw(c)
d.rounded_rectangle([0, 0, W - 1, H - 1], 22, outline=LINE, width=2)
por = Image.open(SRC / "portrait/fouad.avif").convert("RGB")
pw = 520
pimg = rounded(cover(por, pw, H - 56), 14)
c.paste(pimg, (28, 28), pimg)
x = 28 + pw + 56
d.text((x, 120), "// PORTFOLIO", font=mono, fill=ACID)
big = ImageFont.truetype(F + "Inter-Bold.otf", 64)
d.text((x, 160), "Fouad", font=big, fill=TEXT); d.text((x, 232), "Barkaoui", font=big, fill=TEXT)
body = ImageFont.truetype(F + "Inter-Medium.otf", 24)
for i, ln in enumerate(["SOC analyst and fullstack developer.", "Vibe coder and prompt engineer.", "", "Every project, with full case", "studies, in one place."]):
    d.text((x, 350 + i * 36), ln, font=body, fill=MUTED)
d.rounded_rectangle([x, 640, W - 60, 700], 30, outline=ACID, width=2)
d.text((x + 30, 659), "fouad-barkaoui.vercel.app  ->", font=mono, fill=ACID)
c.save(OUT / "work-portfolio.webp", "WEBP", quality=82, method=6)

# square avatar from the same portrait
s = min(por.size)
av = por.crop(((por.width - s) // 2, 40, (por.width - s) // 2 + s, 40 + s)).resize((600, 600), Image.LANCZOS)
av.save("/home/claude/gen/avatar.png", optimize=True)
print("portfolio + avatar done")
