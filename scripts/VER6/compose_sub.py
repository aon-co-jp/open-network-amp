import re, os
from PIL import Image, ImageDraw, ImageFont
SD = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad"
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


HEAD_JA = "サブウーファー端子の回路 VER3 (シミュレーション・デバッグ済み)"
HEAD_EN = "Subwoofer output circuit VER3 (simulated and debugged)"
V2_JA = """#VER3 の変更点 (音質改善の見直し)
- 上の回路図 (完全バランス用 / アンバランス用) を Python のシミュレーションで見直しました。VER2 (LPF 定数の修正・サブソニック HPF 7.2Hz) は継続しています。
- 雑音を低減: 加算段の入力抵抗を 10k → 4.99k、Rf を 4.99k → 2.49k、Rb を 1.24k にして、7〜120Hz の雑音を 0.21µV → 0.15µV (-3.3dB) にしました。プリアウト (約 47Ω) への負荷は -0.08dB です。
- LR4 (24dB/oct) の選択を追加 (SW4): 2段目の LPF を入れると、メインスピーカーが 24dB/oct のときに電気的な和が平坦になります。12dB/oct は逆相でも 80Hz に +3dB のこぶが出ます。
- 位相を連続可変: 1次オールパス (C 100nF + VR2 0〜220k) で 60Hz の位相を 0° → -166° まで変えられます。SW2 の 180° 反転と併用します。
- 未実施: 過渡応答・歪み (THD)・実機の位相。実機または SPICE での確認が必要です。"""
V2_EN = """#What changed in VER3 (a second look at sound quality)
- The circuits above (fully balanced and unbalanced) were reviewed with a Python simulation. VER2 (corrected LPF values and the 7.2 Hz subsonic HPF) is kept.
- Lower noise: the summer input resistors went from 10k to 4.99k, Rf from 4.99k to 2.49k and Rb to 1.24k, which lowers the 7-120 Hz noise from 0.21 uV to 0.15 uV (-3.3 dB). The load on a pre-out (about 47 ohm) is -0.08 dB.
- An LR4 (24 dB/oct) option (SW4): inserting the second LPF stage makes the electrical sum flat when the main speaker is 24 dB/oct. At 12 dB/oct a +3 dB hump appears at 80 Hz even with inverted polarity.
- Continuously variable phase: a first-order all-pass (100 nF + VR2 0-220 kohm) varies the phase at 60 Hz from 0 to -166 degrees. It is used together with the 180-degree switch SW2.
- Not done: transient response, THD and real-hardware phase. Bench or SPICE verification is still required."""
FIGS = [("mono_sub_out_schematic.jpg", "mono_sub_out_v3_balanced.jpg", "図1 / Figure 1: 完全バランス用 VER3 / Fully balanced VER3"),
        ("mono_sub_out_unbalanced.jpg", "mono_sub_out_v3_unbalanced.jpg", "図2 / Figure 2: アンバランス用 VER3 / Unbalanced VER3"),
        ("mono_sub_out_v3_test.jpg", "mono_sub_out_v3_test.jpg", "図3 / Figure 3: VER3 のシミュレーション結果 / VER3 simulation results")]
W = 3200; pad = 60; colw = (W - 3 * pad) // 2
outdir = SD + r"\site\mono-sub-out"
os.makedirs(outdir, exist_ok=True)

W = 3200; pad = 60; colw = (W - 3 * pad) // 2
exec(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\sim_append.py", encoding="utf-8").read())
pages = []
for src, dst, cap in FIGS:
    fig = Image.open(SD + "\\" + src).convert("RGB")
    rj = layout(V2_JA, colw); re_ = layout(V2_EN, colw)
    th = max(height(rj), height(re_))
    head = pad + int(BIG.size * 1.5) * 2 + int(FS * 1.8)
    im = Image.new("RGB", (W, head + fig.height + int(FS * 1.0) + th + pad), "white")
    d = ImageDraw.Draw(im)
    d.text((pad, pad), HEAD_JA, font=BIG, fill=INK)
    d.text((pad, pad + int(BIG.size * 1.5)), HEAD_EN, font=BIG, fill=INK)
    d.text((pad, pad + int(BIG.size * 1.5) * 2), cap, font=HD, fill=(60, 80, 150))
    im.paste(fig, (0, head))
    y0 = head + fig.height + int(FS * 1.0)
    draw_rows(d, pad, y0, rj); draw_rows(d, 2 * pad + colw, y0, re_)
    if dst == "mono_sub_out_v3_test.jpg":
        im = append_sim(im)
    im.save(outdir + "\\" + dst, "JPEG", quality=90, dpi=(300, 300))
    pages.append(im)
    print(dst, im.size)
DPI = 3200 / 11.69
pages[0].save(outdir + r"\mono-sub-out-v3.pdf", "PDF", resolution=DPI, save_all=True, append_images=pages[1:])
print("pdf", len(pages))
