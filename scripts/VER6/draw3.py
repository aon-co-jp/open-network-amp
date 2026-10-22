from PIL import Image, ImageDraw, ImageFont

W, H = 200, 196
OFFY = 46
S = 32
img = Image.new("RGB", (W * S, H * S), "white")
d = ImageDraw.Draw(img)
LW = int(S * 0.13)
INK = (20, 30, 60)
HOT = (190, 30, 30)
COLD = (30, 70, 180)
GRY = (110, 110, 110)
ORG = (170, 90, 10)


def F(size, bold=False):
    name = "meiryob.ttc" if bold else "meiryo.ttc"
    return ImageFont.truetype("C:/Windows/Fonts/" + name, int(size * S * 0.92))


def P(x, y):
    return (x * S, (H - y - OFFY) * S)


def line(pts, col=INK, w=LW):
    pp = [P(*p) for p in pts]
    d.line(pp, fill=col, width=w, joint="curve")
    for p in (pp[0], pp[-1]):
        d.ellipse([p[0] - w / 2, p[1] - w / 2, p[0] + w / 2, p[1] + w / 2], fill=col)


def dot(x, y, col=INK):
    px, py = P(x, y)
    r = S * 0.32
    d.ellipse([px - r, py - r, px + r, py + r], fill=col)


def text(x, y, s, size=1.6, col=INK, anchor="la", bold=False):
    d.text(P(x, y), s, fill=col, font=F(size, bold), anchor=anchor)


def circ(x, y, r, col, fill="white"):
    px, py = P(x, y)
    d.ellipse([px - S * r, py - S * r, px + S * r, py + S * r], outline=col, width=LW, fill=fill)


def res(x, y, label, val, col=INK, vertical=False):
    L, Wd = 8, 2.6
    if vertical:
        d.rectangle([*P(x - Wd / 2, y + L / 2), *P(x + Wd / 2, y - L / 2)], outline=col, width=LW)
        text(x + 2.2, y + 0.3, label, 1.5, col, "lm", True)
        text(x + 2.2, y - 1.4, val, 1.3, GRY, "lm")
    else:
        d.rectangle([*P(x - L / 2, y + Wd / 2), *P(x + L / 2, y - Wd / 2)], outline=col, width=LW)
        text(x, y + 3.6, label, 1.5, col, "mm", True)
        text(x, y + 1.9, val, 1.3, GRY, "mm")


def vcap(x, y, label, val, col=INK, left=False):
    g, h = 0.9, 2.6
    line([(x - h, y + g), (x + h, y + g)], col)
    line([(x - h, y - g), (x + h, y - g)], col)
    if left:
        text(x - 3.4, y + 0.3, label, 1.5, col, "rm", True)
        text(x - 3.4, y - 1.4, val, 1.3, GRY, "rm")
    else:
        text(x + 3.4, y + 0.3, label, 1.5, col, "lm", True)
        text(x + 3.4, y - 1.4, val, 1.3, GRY, "lm")


def hcap(x, y, label="", val="", col=INK):
    line([(x - 0.9, y + 2.6), (x - 0.9, y - 2.6)], col)
    line([(x + 0.9, y + 2.6), (x + 0.9, y - 2.6)], col)
    if label:
        text(x, y + 4.4, label, 1.4, col, "mm", True)
        text(x, y - 4.2, val, 1.1, GRY, "mm")


def gnd(x, y):
    line([(x, y), (x, y - 1.5)])
    line([(x - 1.8, y - 1.5), (x + 1.8, y - 1.5)])
    line([(x - 1.1, y - 2.3), (x + 1.1, y - 2.3)])
    line([(x - 0.4, y - 3.1), (x + 0.4, y - 3.1)])


def opamp(cx, cy, name, part, plus_top=False, w=11, h=13):
    x0, x1 = cx - w / 2, cx + w / 2
    pts = [P(x0, cy + h / 2), P(x0, cy - h / 2), P(x1, cy)]
    d.polygon(pts, outline=INK, fill=(250, 250, 235))
    d.line(pts + [pts[0]], fill=INK, width=LW)
    top, bot = cy + h / 4, cy - h / 4
    plus_y, minus_y = (top, bot) if plus_top else (bot, top)
    text(x0 + 1.0, plus_y, "+", 2.0, INK, "lm", True)
    text(x0 + 1.0, minus_y, "\u2212", 2.0, INK, "lm", True)
    text(cx - 1.2, cy + h / 2 + 1.2, name, 1.7, INK, "mm", True)
    text(cx - 1.2, cy - h / 2 - 1.6, part, 1.3, GRY, "mm")
    return (x0, plus_y), (x0, minus_y), (x1, cy)


def frame(x0, y0, x1, y1, title):
    d.rectangle([*P(x0, y1), *P(x1, y0)], outline=(150, 160, 190), width=int(LW * 0.7))
    text(x0 + 1, y1 - 0.8, title, 1.9, (60, 80, 150), "la", True)


HY, CY = 100, 44

text(3, 147, "完全バランスアンプのモノラル・サブウーファー出力 VER5  Mono Subwoofer Output (XLR + RCA) VER5", 2.8, INK, "la", True)
text(3, 143.4, "参考回路図 Reference schematic  |  ボリューム後段から分岐 tapped after volume (サブ音量が連動)  |  "
     "L+R加算 → 位相 → LPF 80/100/120Hz → バッファ → XLR / 差動RCA", 1.5, GRY)
text(3, 141.0, "VER5: 雑音を低減 (SK の R を下げ C を増やす)・GND リフト・出力ミュートリレーを追加 (VER3/4: LR4・位相可変・サブソニック HPF)  VER5: lower noise, ground lift, mute relay.", 1.25, GRY)
text(140, 141.0, "赤 red = Hot (+)", 1.3, HOT, "la", True)
text(158, 141.0, "青 blue = Cold (\u2212)", 1.3, COLD, "la", True)
text(176, 141.0, "橙 orange = スイッチ", 1.3, ORG, "la", True)

frame(1, 23, 62, 139, "STAGE 1  バランス L+R 加算  Balanced summing")
frame(64, 23, 83, 139, "STAGE 2 位相")
frame(85, 23, 143, 139, "STAGE 3  2次バターワース LPF (バランス)  2nd-order low-pass")
frame(145, 23, 199, 139, "STAGE 4  出力バッファ  Output buffers")


# ---------------------------------------------------------------- stage 1
def sum_row(yc, col, lname, rname, rf_ref, r_refs, u_name, part):
    yl, yr = yc + 12, yc + 6
    text(2, yl, lname, 1.9, col, "lm", True)
    text(2, yr, rname, 1.9, col, "lm", True)
    plus, minus, out = opamp(46, yc, u_name, part, plus_top=False)
    xr = 20
    res(xr, yl, r_refs[0], "3.32k 0.1%", col)
    line([(13, yl), (xr - 4, yl)], col)
    res(xr, yr, r_refs[1], "3.32k 0.1%", col)
    line([(13, yr), (xr - 4, yr)], col)
    xb = 29
    line([(xr + 4, yl), (xb, yl), (xb, minus[1])], col)
    line([(xr + 4, yr), (xb, yr)], col)
    dot(xb, yr, col)
    line([(xb, minus[1]), minus], col)
    yf = yc + 19.5
    res(46, yf, rf_ref, "1.65k 0.1%", col)
    line([(xb, yl), (xb, yf), (42, yf)], col)
    xo = out[0] + 4.5
    line([(50, yf), (xo, yf), (xo, out[1])], col)
    line([out, (xo, out[1])], col)
    dot(xo, out[1], col)
    cfy = yf + 5.2
    line([(xb + 3, yf), (xb + 3, cfy), (36.8, cfy)], col)
    d.line([*P(36.8, cfy + 1.8), *P(36.8, cfy - 1.8)], fill=col, width=LW)
    d.line([*P(38.4, cfy + 1.8), *P(38.4, cfy - 1.8)], fill=col, width=LW)
    line([(38.4, cfy), (xo, cfy), (xo, yf)], col)
    dot(xb + 3, yf, col)
    dot(xo, yf, col)
    text(37.6, cfy + 3.0, "Cf 33p C0G", 1.3, GRY, "mm")
    line([plus, (plus[0] - 6, plus[1])], col)
    res(plus[0] - 6, plus[1] - 4.5, "Rb", "825", col, vertical=True)
    line([(plus[0] - 6, plus[1] - 8.5), (plus[0] - 6, plus[1] - 9.5)], col)
    gnd(plus[0] - 6, plus[1] - 9.5)
    return (xo, out[1])


oH = sum_row(HY, HOT, "L +  (Hot)", "R +  (Hot)", "Rf1", ("R1", "R2"), "U1A", "OPA1612  ch.A")
oC = sum_row(CY, COLD, "L \u2212  (Cold)", "R \u2212  (Cold)", "Rf2", ("R3", "R4"), "U1B", "OPA1612  ch.B")
text(3, 133.6, "バランス入力 (ボリューム後段より)  Balanced inputs, post-volume", 1.25, GRY, "la")

d.rectangle([*P(3, 82), *P(35, 72)], outline=(200, 120, 20), width=int(LW * .7))
text(19, 80.0, "SW1  MONO / STEREO 切替 (R2,R4連動)", 1.25, ORG, "mm", True)
text(19, 77.6, "MONO: LとRを1本に加算 summed", 1.25, GRY, "mm")
text(19, 75.4, "STEREO: R側は同一回路へ", 1.25, GRY, "mm")
text(19, 73.3, "→ SUB OUT 2 (2本目のXLR/RCA)", 1.25, GRY, "mm")

text(3, 25.9, "入力あたり利得 Rf/R = 0.5 → 同相の低音 (L=R) は 0 dB = (L+R)/2 (単純加算の +6 dB を吸収)  Gain per input = 0.5", 1.15, GRY)
text(3, 24.2, "両側とも反転動作。最終極性は SW2 で決定  Both legs invert; SW2 sets the final polarity.", 1.15, GRY)

# ---------------------------------------------------------------- stage 2
d.rectangle([*P(66, 106), *P(81, 36)], outline=(200, 120, 20), width=int(LW * .7))
text(73.5, 104.2, "SW2", 1.8, ORG, "mm", True)
text(73.5, 101.8, "位相 PHASE", 1.3, ORG, "mm", True)
text(73.5, 99.6, "0\u00b0 / 180\u00b0", 1.4, ORG, "mm", True)
line([oH, (69, oH[1]), (69, 76), (70, 76)], HOT)
line([oC, (69, oC[1]), (69, 66), (70, 66)], COLD)
line([(77, 76), (78, 76), (78, HY), (84, HY)], HOT)
line([(77, 66), (78, 66), (78, CY), (84, CY)], COLD)
G = (130, 130, 130)
d.line([*P(70, 76), *P(77, 76)], fill=G, width=LW)
d.line([*P(70, 66), *P(77, 66)], fill=G, width=LW)
d.line([*P(70, 76), *P(77, 66)], fill=G, width=LW)
d.line([*P(70, 66), *P(77, 76)], fill=G, width=LW)
for (x, y, c) in ((70, 76, HOT), (70, 66, COLD), (77, 76, HOT), (77, 66, COLD)):
    dot(x, y, c)
for i, t in enumerate(["ストレート", "= 0\u00b0"]):
    text(73.5, 88.5 - 1.7 * i, t, 1.05, GRY, "mm")
for i, t in enumerate(["クロス", "= 180\u00b0"]):
    text(73.5, 62.5 - 1.7 * i, t, 1.05, GRY, "mm")
for i, t in enumerate(["リレー/トグル", "(リレーなら", "無音切替)"]):
    text(73.5, 56.0 - 1.7 * i, t, 1.05, GRY, "mm")


# ---------------------------------------------------------------- stage 3
def lpf(yc, col, tag, ua, part):
    n = 1 if tag == "H" else 3
    y = yc
    line([(84, y), (88, y)], col)
    res(92, y, "R%d" % (n + 4), "6.34k..4.22k", col)
    line([(96, y), (99, y)], col)
    dot(99, y, col)
    res(103, y, "R%d" % (n + 5), "6.34k..4.22k", col)
    line([(107, y), (110, y)], col)
    dot(110, y, col)
    plus, minus, out = opamp(121, y, ua, part, plus_top=True)
    line([(110, y), (110, plus[1]), plus], col)
    line([(110, y), (110, y - 5.0)], col)
    vcap(110, y - 7.0, "C%d" % (2 if tag == "H" else 4), "220n 固定", col=col, left=True)
    line([(110, y - 8.1), (110, y - 11.5)], col)
    gnd(110, y - 11.5)
    yfb = y + 12.0
    line([(99, y), (99, yfb), (104.6, yfb)], col)
    d.line([*P(104.6, yfb + 2.6), *P(104.6, yfb - 2.6)], fill=col, width=LW)
    d.line([*P(106.4, yfb + 2.6), *P(106.4, yfb - 2.6)], fill=col, width=LW)
    line([(106.4, yfb), (130, yfb), (130, y)], col)
    text(105.5, yfb + 3.2, "C%d" % (1 if tag == "H" else 3), 1.5, col, "mm", True)
    text(105.5, yfb + 4.9, "440n 固定", 1.3, GRY, "mm")
    line([minus, (minus[0] - 2.5, minus[1]), (minus[0] - 2.5, y - 17.0), (130, y - 17.0), (130, y)], col)
    line([out, (130, y)], col)
    dot(130, y, col)
    line([(130, y), (132.1, y)], col)
    hcap(133, y, "C5" if tag == "H" else "C6", "2.2µF", col)
    line([(133.9, y), (146, y)], col)
    dot(139, y, col)
    line([(139, y), (139, y - 4)], col)
    res(139, y - 8, "R13" if tag == "H" else "R14", "10k", col, vertical=True)
    line([(139, y - 12), (139, y - 13)], col)
    gnd(139, y - 13)


lpf(HY, HOT, "H", "U2A", "OPA1612  ch.A")
lpf(CY, COLD, "C", "U2B", "OPA1612  ch.B")
d.rectangle([*P(87, 81.5), *P(141, 64)], outline=(200, 120, 20), width=int(LW * .7))
text(114, 79.3, "SW3  ロータリー  BYPASS / 80 / 100 / 120 Hz", 1.45, ORG, "mm", True)
for i, t in enumerate([
    "R5〜R8 の値を切替  (fc = 1/(2πR√(C1C2)), C1 440n・C2 220n 固定, Q = 0.707)",
    "80 Hz: R 6.34k    100 Hz: R 5.11k    120 Hz: R 4.22k  (計算: -3dB が 80.7 / 100.0 / 121.3 Hz)",
    "BYPASS = 全帯域モノ (サブ側クロスオーバーを使用)  コンデンサ: PPS / C0G フィルム 1%",
    "Hot / Cold 側は同値でバランス (CMRR) を維持  identical values keep the balance",
    "12 dB/oct。24 dB/oct は2段目を追加  add a 2nd section for 24 dB/oct",
    "切替部: 2回路4接点ロータリー またはアナログスイッチIC",
]):
    text(114, 76.8 - 2.1 * i, t, 1.1, GRY, "mm")


# ---------------------------------------------------------------- stage 4
def buf(yc, col, ua, part):
    plus, minus, out = opamp(155, yc, ua, part, plus_top=True, w=10, h=12)
    line([(146, yc), (150, yc), (150, plus[1]), plus], col)
    line([minus, (minus[0] - 2, minus[1]), (minus[0] - 2, yc - 10), (163, yc - 10), (163, yc)], col)
    line([out, (163, yc)], col)
    dot(163, yc, col)
    return (163, yc)


bH = buf(HY, HOT, "U4A", "OPA1612  ch.A")
bC = buf(CY, COLD, "U4B", "OPA1612  ch.B")
for (b, col, rn, pin, lab) in ((bH, HOT, "R9", 2, "Hot"), (bC, COLD, "R10", 3, "Cold")):
    line([b, (168, b[1])], col)
    res(172, b[1], rn, "47R", col)
    line([(176, b[1]), (188.8, b[1])], col)
    circ(190, b[1], 1.2, col)
    text(190, b[1], str(pin), 1.4, col, "mm", True)
    text(190, b[1] + (3.0 if pin == 2 else -3.0), "XLR %d %s" % (pin, lab), 1.25, col, "mm", True)
circ(190, 113, 1.2, INK)
text(190, 113, "1", 1.4, INK, "mm", True)
line([(188.8, 113), (184, 113)], INK)
res(180, 113, "R11", "10R || C5 10n", INK)
line([(176, 113), (172, 113)], INK)
gnd(172, 113)
text(198, 108.0, "SUB OUT XLR (バランス・モノ)", 1.25, INK, "ra", True)

text(166, 73.8, "RCA出力: バランス→シングルエンド", 1.3, INK, "la", True)
d.rectangle([*P(168, 68), *P(181, 54)], outline=INK, width=LW, fill=(250, 250, 235))
text(174.5, 65.8, "U5", 1.6, INK, "mm", True)
text(174.5, 63.8, "THAT1240", 1.3, INK, "mm", True)
for i, t in enumerate(["差動レシーバ", "(OPA1612+", "10k×4でも可)"]):
    text(174.5, 62.0 - 1.6 * i, t, 1.15, GRY, "mm")
line([(163, HY), (163, 66), (168, 66)], HOT)
line([(163, CY), (163, 56), (168, 56)], COLD)
text(169, 66.0, "IN+", 1.1, HOT, "lm", True)
text(169, 56.0, "IN\u2212", 1.1, COLD, "lm", True)
line([(181, 61), (184, 61)], INK)
res(188, 61, "R12", "100R", INK)
line([(192, 61), (192.6, 61)], INK)
circ(194.2, 61, 1.6, INK)
text(196.4, 63.5, "RCA", 1.1, INK, "lm", True)
text(190, 55.0, "SUB OUT RCA (Hot=チップ)", 1.25, INK, "mm", True)
gnd(174.5, 54)

# ---------------------------------------------------------------- bottom panels
frame(1, 1, 98, 21, "POWER / BYPASS  電源・バイパス (全IC共通)")
pw = [
    ("±15 V 低雑音ポストレギュレータ (LT3045 / LT3094、または LM317/LM337 + RC)", INK),
    ("アンプ既存のアナログ電源 (または小型の別巻線) から供給  Use the existing analog rails.", GRY),
    ("各IC: 100 nF X7R をピン直近 + 10 µF / 電源ごと (10 mm 以内)", INK),
    ("アナログGNDへ1点アース。XLR 1番ピンは R11 || C5 でシャーシへ  Star ground.", INK),
    ("任意: 各XLR線に 4.7 µF フィルムのDCカット (R9/R10 の後) とミュートリレー", GRY),
    ("R1〜R8 は 0.1% 25 ppm 薄膜抵抗アレイ。全てSMDで自動実装向き  All SMD.", GRY),
]
for i, (t, c) in enumerate(pw):
    text(3, 16.2 - 2.45 * i, t, 1.3, c)

frame(100, 1, 199, 21, "BILL OF MATERIALS  部品表 (概要)")
for i, t in enumerate([
    "U1, U2, U4   OPA1612 デュアル (低コストなら NJM4580 / LME49720)  ×3",
    "U5   THAT1240 (レーザートリム差動レシーバ)  ×1",
    "R1-R4 3.32k 0.1% 25ppm 薄膜    Rf1, Rf2 1.65k 0.1%    Rb 825 1%",
    "C1-C4 PPS / C0G フィルム (440n / 220n 固定)    R5-R8 6.34k / 5.11k / 4.22k (SW3 で切替)",
    "R9, R10 47R   R11 10R   R12 100R   C5 10n   Cf 33p C0G",
    "SW1 MONO/STEREO   SW2 位相   SW3 LPF (BYPASS/80/100/120 Hz)",
    "J1 XLR-3 オス   J2 RCA   (J3 = STEREO時の SUB OUT 2)",
]):
    text(102, 17.2 - 2.2 * i, t, 1.2, INK)

exec(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\ver3_panel.py", encoding="utf-8").read())
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\mono_sub_out_schematic.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
