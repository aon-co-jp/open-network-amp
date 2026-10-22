import re, os, sys
from PIL import Image, ImageDraw, ImageFont
SD = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad"
exec(open(SD + r"\v5_text.py", encoding="utf-8").read())
FS = 38
REG = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", FS)
HD = ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc", int(FS * 1.2))
BIG = ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc", int(FS * 1.5))
INK = (20, 30, 60)
TOK = re.compile(r"[\x21-\x7e\u00a0-\u024f\u0400-\u04ff]+|\s|.", re.S)
W = 3200
pad = 60
colw = (W - 3 * pad) // 2
LANGS = ("ja", "en", "de", "ru")


def wrap(text, font, width):
    out, cur = [], ""
    for t in TOK.findall(text):
        if font.getlength(cur + t) > width and cur.strip():
            out.append(cur.rstrip())
            cur = t.lstrip()
        else:
            cur += t
    out.append(cur.rstrip())
    return out


def layout(txt, width):
    rows = []
    for para in txt.split(chr(10)):
        if not para.strip():
            continue
        if para.startswith("#"):
            rows.append((HD, wrap(para[1:], HD, width), 0, int(FS * 0.5), int(FS * 0.2)))
        elif para.startswith("- "):
            rows.append((REG, wrap(para[2:], REG, width - int(FS * 1.2)), int(FS * 1.2), 0, int(FS * 0.25)))
        else:
            rows.append((REG, wrap(para, REG, width), 0, 0, int(FS * 0.4)))
    return rows


def height(rows):
    return sum(pre + int(f.size * 1.5) * len(l) + gap for f, l, ind, pre, gap in rows)


def draw_rows(d, x, y, rows):
    for f, lines, ind, pre, gap in rows:
        y += pre
        for i, ln in enumerate(lines):
            if ind and i == 0:
                d.text((x, y), "\u2022", font=f, fill=INK)
            d.text((x + ind, y), ln, font=f, fill=INK)
            y += int(f.size * 1.5)
        y += gap
    return y


def grid_height(texts):
    L = {k: layout(texts[k], colw) for k in LANGS}
    h1 = max(height(L["ja"]), height(L["en"]))
    h2 = max(height(L["de"]), height(L["ru"]))
    return L, h1, h2


def draw_grid(d, y0, L, h1, h2):
    draw_rows(d, pad, y0, L["ja"])
    draw_rows(d, 2 * pad + colw, y0, L["en"])
    draw_rows(d, pad, y0 + h1 + int(FS * 0.6), L["de"])
    draw_rows(d, 2 * pad + colw, y0 + h1 + int(FS * 0.6), L["ru"])
    return y0 + h1 + int(FS * 0.6) + h2


def header(d, settitle=None):
    y = pad
    for k in LANGS:
        d.text((pad, y), HEAD[k], font=BIG, fill=INK)
        y += int(BIG.size * 1.45)
    if settitle:
        d.text((pad, y), "  /  ".join(settitle[k] for k in LANGS[:2]), font=HD, fill=(60, 80, 150))
        y += int(HD.size * 1.5)
        d.text((pad, y), "  /  ".join(settitle[k] for k in LANGS[2:]), font=HD, fill=(60, 80, 150))
        y += int(HD.size * 1.6)
    return y


def build(setkey, figmap=None):
    st = SETS[setkey]
    outdir = SD + "\\site\\" + st["dir"]
    os.makedirs(outdir, exist_ok=True)
    pages = []
    # page 1: summary
    L, h1, h2 = grid_height(SUMMARY)
    tmp = Image.new("RGB", (W, 10), "white")
    top = header(ImageDraw.Draw(tmp), st["title"])
    im = Image.new("RGB", (W, top + h1 + h2 + int(FS * 0.6) + pad), "white")
    d = ImageDraw.Draw(im)
    header(d, st["title"])
    draw_grid(d, top, L, h1, h2)
    pages.append(im)
    for n, fn in enumerate(st["files"], 1):
        fig = Image.open(SD + "\\" + fn).convert("RGB")
        cap = dict(CAP[fn if fn in CAP else "amp_ver5_sim.jpg"])
        texts = {k: cap[k] + "\n" + COMMON[k] for k in LANGS}
        L, h1, h2 = grid_height(texts)
        top = header(ImageDraw.Draw(Image.new("RGB", (W, 10), "white")), st["title"])
        im = Image.new("RGB", (W, top + fig.height + int(FS * 1.0) + h1 + h2 + int(FS * 0.6) + pad), "white")
        d = ImageDraw.Draw(im)
        header(d, st["title"])
        d.text((W - pad - 400, pad), "図 %d / Fig. %d" % (n, n), font=HD, fill=(60, 80, 150))
        im.paste(fig, (0, top))
        draw_grid(d, top + fig.height + int(FS * 1.0), L, h1, h2)
        name = fn
        if "prefix" in st:
            name = st["prefix"] + {"mono_sub_out_schematic.jpg": "balanced.jpg", "mono_sub_out_unbalanced.jpg": "unbalanced.jpg", "amp_ver5_sim.jpg": "sim.jpg"}[fn]
        im.save(outdir + "\\" + name, "JPEG", quality=88, dpi=(300, 300))
        pages.append(im)
        print(setkey, name, im.size)
    DPI = 3200 / 11.69
    pages[0].save(outdir + "\\" + st["pdf"], "PDF", resolution=DPI, save_all=True, append_images=pages[1:])
    print(setkey, "pdf", len(pages))


for k in (sys.argv[1:] or ["streaming", "analog", "sub"]):
    build(k)
