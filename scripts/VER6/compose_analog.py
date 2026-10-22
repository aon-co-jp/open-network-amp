import re, os
from PIL import Image, ImageDraw, ImageFont
SD = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad"
ns = {}
exec(open(SD + r"\analog_text.py", encoding="utf-8").read(), ns)
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

W = 3200; pad = 60; colw = (W - 3 * pad) // 2
def header(d, cap=None):
    d.text((pad, pad), ns["HEAD_JA"], font=BIG, fill=INK)
    d.text((pad, pad + int(BIG.size * 1.5)), ns["HEAD_EN"], font=BIG, fill=INK)
    d.text((pad, pad + int(BIG.size * 1.5) * 2), ns["SUB_JA"] + "  /  " + ns["SUB_EN"], font=REG, fill=(90, 100, 130))
    if cap:
        d.text((pad, pad + int(BIG.size * 1.5) * 2 + int(FS * 1.7)), cap, font=HD, fill=(60, 80, 150))
HEADH = pad + int(BIG.size * 1.5) * 2 + int(FS * 1.7) + int(FS * 1.8)

COMMON_JA = "共通の注意: 参考設計です。部品値は机上計算で、シミュレーションも実機測定もしていません。高電圧・大電流を扱うため、製品化の前に実機測定と安全規格・認証の確認が必要です。"
COMMON_EN = "Common note: reference design. Component values were only worked out on paper; no simulation or bench measurement has been done. High voltage and high current are involved, so bench measurement and safety standards and certification must be checked before productization."


W = 3200; pad = 60; colw = (W - 3 * pad) // 2
exec(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\sim_append.py", encoding="utf-8").read())
pages = []
outdir = SD + r"\site\analog-amp"
os.makedirs(outdir, exist_ok=True)
# page 1: intro
rj = layout(ns["INTRO_JA"], colw); re_ = layout(ns["INTRO_EN"], colw)
th = max(height(rj), height(re_))
im = Image.new("RGB", (W, HEADH + th + pad), "white")
d = ImageDraw.Draw(im); header(d)
draw_rows(d, pad, HEADH, rj); draw_rows(d, 2 * pad + colw, HEADH, re_)
pages.append(im)
for fn, cap, tj, te in ns["FIGS"]:
    fig = Image.open(SD + "\\" + fn).convert("RGB")
    rj = layout(tj + "\n" + COMMON_JA, colw); re_ = layout(te + "\n" + COMMON_EN, colw)
    th = max(height(rj), height(re_))
    H = HEADH + fig.height + int(FS * 1.0) + th + pad
    im = Image.new("RGB", (W, H), "white")
    d = ImageDraw.Draw(im); header(d, cap)
    im.paste(fig, (0, HEADH))
    y0 = HEADH + fig.height + int(FS * 1.0)
    draw_rows(d, pad, y0, rj); draw_rows(d, 2 * pad + colw, y0, re_)
    if fn == "amp_test.jpg":
        im = append_sim(im)
    im.save(outdir + "\\" + fn, "JPEG", quality=90, dpi=(300, 300))
    pages.append(im)
    print(fn, im.size)
DPI = 3200 / 11.69
pages[0].save(outdir + r"\analog-integrated-amp.pdf", "PDF", resolution=DPI, save_all=True, append_images=pages[1:])
print("pdf", len(pages))
