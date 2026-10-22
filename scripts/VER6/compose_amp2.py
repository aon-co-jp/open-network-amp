import re
from PIL import Image, ImageDraw, ImageFont
SD = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad"
ns = {}
exec(open(SD + r"\amp_text.py", encoding="utf-8").read(), ns)
FS = 38
REG = ImageFont.truetype("C:/Windows/Fonts/meiryo.ttc", FS)
HD = ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc", int(FS * 1.2))
BIG = ImageFont.truetype("C:/Windows/Fonts/meiryob.ttc", int(FS * 1.9))
INK = (20, 30, 60)
TOK = re.compile(r"[\x21-\x7e]+|\s|.", re.S)

def wrap(text, font, width):
    out, cur = [], ""
    for t in TOK.findall(text):
        if font.getlength(cur + t) > width and cur.strip():
            out.append(cur.rstrip()); cur = t.lstrip()
        else:
            cur += t
    out.append(cur.rstrip())
    return out

def sections(txt):
    secs, cur = [], None
    for ln in txt.split(chr(10)):
        if ln.startswith("#"):
            cur = [ln]; secs.append(cur)
        elif cur is not None:
            cur.append(ln)
    return ["\n".join(s).strip() for s in secs]

def layout(txt, width):
    rows = []
    for para in txt.split(chr(10)):
        if not para.strip():
            continue
        if para.startswith("#"):
            rows.append((HD, wrap(para[1:], HD, width), 0, int(FS * 0.7), int(FS * 0.2)))
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

HEAD_JA = "最新プリメインアンプをCLAUDEで設計してみました。"
HEAD_EN = "I designed the latest integrated amplifier with CLAUDE."
ja = sections(ns["AMP_JA"]); en = sections(ns["AMP_EN"])
# 0 intro, 1 common, 2 balanced, 3 unbalanced, 4 notes
def pick(sec, ver):
    return "\n\n".join([sec[0], sec[1], sec[2 if ver == "bal" else 3], sec[4]])

def compose(fn, cap, ver):
    fig = Image.open(SD + "\\" + fn).convert("RGB")
    W = 3200
    pad = 60
    colw = (W - 3 * pad) // 2
    rj = layout(pick(ja, ver), colw); re_ = layout(pick(en, ver), colw)
    th = max(height(rj), height(re_))
    top = pad + int(BIG.size * 1.5) * 2 + int(FS * 1.4) + int(FS * 1.0)
    H = top + fig.height + int(FS * 1.2) + th + pad
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im)
    d.text((pad, pad), HEAD_JA, font=BIG, fill=INK)
    d.text((pad, pad + int(BIG.size * 1.5)), HEAD_EN, font=BIG, fill=INK)
    d.text((pad, pad + int(BIG.size * 1.5) * 2), cap, font=HD, fill=(60, 80, 150))
    im.paste(fig, (0, top))
    y0 = top + fig.height + int(FS * 1.2)
    draw_rows(d, pad, y0, rj)
    draw_rows(d, 2 * pad + colw, y0, re_)
    return im


W = 3200; pad = 60; colw = (W - 3 * pad) // 2
exec(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\sim_append.py", encoding="utf-8").read())
outs = []
for cap, fn in ns["CAPS"]:
    ver = "lay" if fn in ("amp_layout_net.jpg", "amp_test.jpg", "amp_volume_haptic.jpg", "amp_ver3_sim.jpg", "amp_hp.jpg", "amp_ver4_sim.jpg") else ("bal" if "unbalanced" not in fn else "unb")
    im = compose(fn, cap, ver)
    if fn == "amp_test.jpg":
        im = append_sim(im)
    p = SD + "\site\streaming-amp\\" + fn
    im.save(p, "JPEG", quality=90, dpi=(300, 300))
    outs.append(im)
    print(fn, im.size)
# PDF: pages = the 4 composites, page size = 11.69in wide
DPI = 3200 / 11.69
outs[0].save(SD + r"\site\streaming-amp\streaming-integrated-amp.pdf", "PDF", resolution=DPI, save_all=True, append_images=outs[1:])
print("pdf ok")
