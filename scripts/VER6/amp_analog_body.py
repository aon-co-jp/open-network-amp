ANA = (25, 115, 60)
OFFY = 10


def P(x, y):
    return (x * S, (H - y - OFFY) * S)


HOT = (190, 30, 30)
COLD = (30, 70, 180)


def flag(x, y, t, col):
    d.rectangle([*P(x - 3.6, y + 1.4), *P(x + 3.6, y - 1.4)], outline=col, width=LW, fill="white")
    text(x, y, t, 1.3, col, "mm", True)


def sbox(x0, y0, x1, y1, lines, col=INK, fill=(250, 250, 240)):
    d.rectangle([*P(x0, y1), *P(x1, y0)], outline=col, width=LW, fill=fill)
    n = len(lines)
    top = (y0 + y1) / 2 + (n - 1) * 1.05
    for i, (t, sz, b) in enumerate(lines):
        text((x0 + x1) / 2, top - 2.1 * i, t, sz, INK, "mm", b)


text(3, 127, "アナログ信号経路 (1ch分)  Analog signal path (one channel; the other channel is identical)", 2.4, INK, "la", True)
text(3, 123.6, "DAC電流出力 → I/V → LPF → バランスボリューム → バッファ → PRE OUT (XLR+RCA) / SUB OUT (XLR+RCA) / パワーアンプ → バイワイヤリング対応スピーカー端子", 1.45, GRY)
text(3, 121.2, "参考設計 Reference design  |  値は机上計算。シミュレーション・実機測定は未実施 (Values are on paper only).  ds = データシート推奨値 per datasheet.", 1.2, GRY)

HY, CY = 100, 68
# ---- DAC
sbox(2, 62, 18, 106, [("DAC", 1.4, True), ("AK4191", 1.15, True), ("+ BD34302", 1.15, True), ("HDモノラル", 1.0, False), ("mono mode", 1.0, False)], ANA)
text(18.6, HY + 1.6, "IOUT+", 1.15, HOT, "la", True)
text(18.6, CY + 1.6, "IOUT−", 1.15, COLD, "la", True)


def tia(yc, col, name, rf, cf):
    plus, minus, out = opamp(34, yc, name, "OPA1612", plus_top=False)
    line([(18, yc), (24, yc), (24, minus[1]), minus], col)
    yf = yc + 11.5
    line([(24, minus[1]), (24, yf), (30, yf)], col)
    res(34, yf, rf, "ds", col)
    xo = out[0] + 3.5
    line([(38, yf), (xo, yf), (xo, yc)], col)
    line([out, (xo, yc)], col)
    dot(xo, yc, col)
    dot(24, minus[1], col)
    cfy = yf + 4.6
    line([(24, yf), (24, cfy), (38.6, cfy)], col)
    d.line([*P(38.6, cfy + 1.8), *P(38.6, cfy - 1.8)], fill=col, width=LW)
    d.line([*P(40.4, cfy + 1.8), *P(40.4, cfy - 1.8)], fill=col, width=LW)
    line([(40.4, cfy), (xo, cfy), (xo, yf)], col)
    text(39.5, cfy + 2.6, cf, 1.2, GRY, "mm")
    line([plus, (25, plus[1])], col)
    gnd(25, plus[1])
    return xo


xH = tia(HY, HOT, "U1A", "Rf1", "Cf 100p")
tia(CY, COLD, "U1B", "Rf2", "Cf 100p")
# ---- LPF
for (y, col, rn) in ((HY, HOT, "R3"), (CY, COLD, "R4")):
    line([(xH, y), (48, y)], col)
    res(52, y, rn, "1.2k 0.1%", col)
    line([(56, y), (70, y)], col)
dot(62, HY, HOT)
dot(62, CY, COLD)
line([(62, HY), (62, 85.9)], HOT)
line([(62, 82.1), (62, CY)], COLD)
vcap(62, 84, "Cd", "470p C0G", col=INK, left=True)
text(62, 106.5, "差動LPF fc≈141kHz", 1.1, GRY, "mm")
# ---- volume
sbox(70, 56, 94, 112, [("バランス", 1.3, True), ("電子ボリューム", 1.3, True), ("MUSES72323", 1.1, False), ("×2 / ch 等", 1.1, False), ("Hot / Cold", 1.1, False), ("各々を減衰", 1.1, False), ("+ 入力セレクタ", 1.1, False), ("(アナログ入力", 1.0, False), ("XLR/RCA を合流)", 1.0, False)], ANA)
text(82, 59.0, "Balanced volume", 1.0, GRY, "mm")
# ---- buffers
for (y, col, nm, rn, pin, lab) in ((HY, HOT, "U3A", "R9", 2, "Hot"), (CY, COLD, "U3B", "R10", 3, "Cold")):
    plus, minus, out = opamp(104, y, nm, "OPA1612", plus_top=True, w=10, h=12)
    line([(94, y), (96, y), (96, plus[1]), plus], col)
    line([minus, (minus[0] - 2, minus[1]), (minus[0] - 2, y - 9), (113, y - 9), (113, y)], col)
    line([out, (113, y)], col)
    dot(113, y, col)
    line([(113, y), (117, y)], col)
    res(121, y, rn, "47R", col)
    line([(125, y), (134.8, y)], col)
    circ(136, y, 1.2, col)
    text(136, y, str(pin), 1.3, col, "mm", True)
    text(136, y + (3.0 if pin == 2 else -3.0), "XLR %d %s" % (pin, lab), 1.15, col, "mm", True)
line([(113, HY), (113, 105.5)], HOT)
flag(113, 107.2, "PRE+", HOT)
line([(113, CY), (113, 62.5)], COLD)
flag(113, 60.8, "PRE−", COLD)
circ(136, 109, 1.2, INK)
text(136, 109, "1", 1.3, INK, "mm", True)
line([(134.8, 109), (131, 109)], INK)
res(127, 109, "R11", "10R||C5", INK)
line([(123, 109), (121, 109)], INK)
gnd(121, 109)
text(146, 100, "PRE OUT XLR", 1.5, INK, "la", True)
text(146, 97.6, "(バランス出力)", 1.2, GRY, "la")
# right-top notes
sbox(144, 66, 199, 92, [("PRE OUT は XLR と RCA の両方", 1.25, True), ("XLR: バッファ + 47Ω 直結 (2=Hot, 3=Cold, 1=シールド)", 1.05, False),
                         ("RCA: 差動レシーバ U5 でシングルエンド化 (下段)", 1.05, False),
                         ("PRE+ / PRE− の旗は同名の点どうしが接続 (配線の交差を避けるため)", 1.0, False),
                         ("Flags with the same name are connected.", 1.0, False)], ANA)

# ================= bottom band
OFFY = 0
frame(1, 5, 199, 58, "出力段 Output stage:  PRE OUT RCA  /  SUB OUT  /  POWER AMP + bi-wire terminals")
# U5 and RCA
flag(6, 49, "PRE+", HOT)
flag(6, 42, "PRE−", COLD)
line([(9.6, 49), (14, 49)], HOT)
line([(9.6, 42), (14, 42)], COLD)
sbox(14, 38, 30, 53, [("U5", 1.4, True), ("THAT1240", 1.1, True), ("差動レシーバ", 1.05, False)], INK)
line([(30, 45.5), (32, 45.5)], INK)
res(36, 45.5, "R12", "100R", INK)
line([(40, 45.5), (45, 45.5)], INK)
circ(46.6, 45.5, 1.6, INK)
text(41, 38.2, "PRE OUT RCA", 1.3, INK, "mm", True)
text(41, 36.2, "(Hot = チップ)", 1.1, GRY, "mm")
# SUB OUT
flag(54, 49, "PRE+", HOT)
flag(54, 42, "PRE−", COLD)
text(54, 53.2, "L+R", 1.1, GRY, "mm")
line([(57.6, 49), (62, 49)], HOT)
line([(57.6, 42), (62, 42)], COLD)
sbox(62, 26, 100, 54, [("SUB OUT (モノ)", 1.35, True), ("L+R バランス加算", 1.1, False), ("→ 位相 0/180° → LPF 80/100/120Hz", 1.05, False), ("→ バッファ (前の図の回路)", 1.05, False), ("Mono sum + phase + LPF", 1.0, False), ("(previous circuit)", 1.0, False)], ANA)
for (y, col, t) in ((49, HOT, "XLR 2 Hot"), (42, COLD, "XLR 3 Cold")):
    line([(100, y), (106.8, y)], col)
    circ(108, y, 1.2, col)
    text(110, y, t, 1.0, col, "lm", True)
line([(100, 34), (106.4, 34)], INK)
circ(108, 34, 1.6, INK)
text(110.4, 34, "SUB OUT RCA", 1.15, INK, "lm", True)
text(108, 54.5, "SUB OUT XLR", 1.25, INK, "mm", True)
# power amp
flag(122, 46, "PRE+", HOT)
flag(122, 24, "PRE−", COLD)
line([(125.6, 46), (126, 46)], HOT)
line([(125.6, 24), (126, 24)], COLD)
sbox(126, 12, 148, 50, [("パワーアンプ", 1.3, True), ("Class-D", 1.2, True), ("バランス入力", 1.1, False), ("Eigentakt型", 1.1, False), ("モジュール", 1.1, False), ("例 Purifi", 1.0, False), ("1ET400A", 1.0, False)], ANA)
line([(148, 35), (152, 35)], HOT)
line([(148, 23), (152, 23)], COLD)
sbox(152, 14, 162, 46, [("K1", 1.3, True), ("DC保護", 1.0, False), ("リレー", 1.0, False), ("遅延", 1.0, False), ("ミュート", 1.0, False)], ANA)
line([(162, 35), (170, 35)], HOT)
line([(170, 32), (170, 38)], HOT)
line([(170, 38), (184.8, 38)], HOT)
line([(170, 32), (184.8, 32)], HOT)
dot(170, 35, HOT)
line([(162, 23), (174, 23)], COLD)
line([(174, 20), (174, 26)], COLD)
line([(174, 26), (184.8, 26)], COLD)
line([(174, 20), (184.8, 20)], COLD)
dot(174, 23, COLD)
for (y, col, t) in ((38, HOT, "HF+"), (32, HOT, "LF+"), (26, COLD, "HF−"), (20, COLD, "LF−")):
    circ(186, y, 1.2, col)
    text(189.4, y, t, 1.3, col, "lm", True)
G = (130, 130, 130)
d.line([*P(193.6, 38), *P(196, 38), *P(196, 32), *P(193.6, 32)], fill=G, width=LW)
d.line([*P(193.6, 26), *P(196, 26), *P(196, 20), *P(193.6, 20)], fill=G, width=LW)
text(176, 53.2, "スピーカー端子 バイワイヤ対応", 1.3, INK, "mm", True)
text(176, 51.0, "Bi-wire speaker terminals (L ch / R ch 各1組)", 1.0, GRY, "mm")
text(176, 15.0, "灰の折れ線 = ジャンパー板 (シングルワイヤ時のみ装着)", 1.0, GRY, "mm")
text(176, 13.0, "Gray bars = jumpers; fit them for single-wire, remove for bi-wire", 1.0, GRY, "mm")
text(3, 9.2, "各アンプ/DAC/バッファは ±15V (LT3045/LT3094) + 100nF X7R + 10µF。I/V の Rf・Cf は DAC データシートの出力電流から決定 (ds)。XLR は 2=Hot / 3=Cold / 1=シールド。", 1.1, GRY)
text(3, 7.0, "Supplies: ±15V low-noise regulators, 100nF + 10uF per IC. Rf/Cf of the I/V stage follow the DAC datasheet. XLR: 2 = Hot, 3 = Cold, 1 = shield.", 1.1, GRY)

img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\streaming_amp_analog.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
