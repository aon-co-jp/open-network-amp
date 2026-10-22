ANA = (25, 115, 60)
HOT = (190, 30, 30)
COLD = (30, 70, 180)
SIG = ANA
OFFY = 10


def P(x, y):
    return (x * S, (H - y - OFFY) * S)


def flag(x, y, t, col):
    d.rectangle([*P(x - 3.6, y + 1.4), *P(x + 3.6, y - 1.4)], outline=col, width=LW, fill="white")
    text(x, y, t, 1.3, col, "mm", True)


def sbox(x0, y0, x1, y1, lines, col=INK, fill=(250, 250, 240)):
    d.rectangle([*P(x0, y1), *P(x1, y0)], outline=col, width=LW, fill=fill)
    n = len(lines)
    top = (y0 + y1) / 2 + (n - 1) * 1.05
    for i, (t, sz, b) in enumerate(lines):
        text((x0 + x1) / 2, top - 2.1 * i, t, sz, INK, "mm", b)


text(3, 127, "アナログ信号経路 (アンバランス版・1ch分)  Analog signal path, unbalanced (one channel)", 2.4, INK, "la", True)
text(3, 123.6, "DAC電流出力 → I/V → 差動→シングルエンド → LPF → ボリューム → バッファ → PRE OUT (RCA+XLR) / SUB OUT (RCA+XLR) / パワーアンプ → バイワイヤリング対応スピーカー端子", 1.4, GRY)
text(3, 121.2, "参考設計 Reference design  |  値は机上計算。シミュレーション・実機測定は未実施 (Values are on paper only).  ds = データシート推奨値 per datasheet.", 1.2, GRY)

HY, CY = 100, 68
sbox(2, 62, 18, 106, [("DAC", 1.4, True), ("AK4191", 1.15, True), ("+ BD34302", 1.15, True), ("ステレオ", 1.0, False), ("stereo mode", 1.0, False)], ANA)
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


tia(HY, HOT, "U1A", "Rf1", "Cf 100p")
tia(CY, COLD, "U1B", "Rf2", "Cf 100p")

# ---- differential -> single-ended (U2)
p2, m2, o2 = opamp(72, 84, "U2", "", plus_top=False)
line([(43, HY), (48, HY), (48, m2[1]), (54, m2[1])], HOT)
res(58, m2[1], "R5", "10k 0.1%", HOT)
line([(62, m2[1]), m2], HOT)
dot(64, m2[1], HOT)
line([(64, m2[1]), (64, 96), (69, 96)], SIG)
res(73, 96, "Rf3", "10k 0.1%", SIG)
line([(77, 96), (81, 96), (81, 84)], SIG)
line([o2, (81, 84)], SIG)
dot(81, 84, SIG)
line([(43, CY), (48, CY), (48, p2[1]), (54, p2[1])], COLD)
res(58, p2[1], "R6", "10k 0.1%", COLD)
line([(62, p2[1]), p2], COLD)
dot(64, p2[1], COLD)
line([(64, p2[1]), (64, 80)], COLD)
res(64, 76, "R7", "10k 0.1%", COLD, vertical=True)
line([(64, 72), (64, 71)], COLD)
gnd(64, 71)
text(72, 71.5, "差動→シングルエンド", 1.15, GRY, "mm")
text(72, 69.6, "(減算回路)", 1.1, GRY, "mm")

# ---- LPF
line([(81, 84), (84, 84)], SIG)
res(88, 84, "R8", "1.2k 0.1%", SIG)
line([(92, 84), (96, 84)], SIG)
dot(96, 84, SIG)
line([(96, 84), (96, 80)], SIG)
vcap(96, 78, "C1", "1nF C0G", col=SIG, left=False)
line([(96, 76.9), (96, 74)], SIG)
gnd(96, 74)
text(92, 90.0, "LPF fc≈133kHz", 1.1, GRY, "mm")
line([(96, 84), (102, 84)], SIG)

# ---- volume
sbox(102, 70, 118, 98, [("ボリューム", 1.3, True), ("MUSES72323", 1.05, False), ("×1 / ch 等", 1.05, False), ("+ 入力セレクタ", 1.05, False), ("(RCA入力を合流)", 1.0, False), ("Volume", 1.0, False)], ANA)

# ---- buffer
plus, minus, out = opamp(130, 84, "U3", "OPA1612", plus_top=True, w=10, h=12)
line([(118, 84), (120, 84), (120, plus[1]), plus], SIG)
line([minus, (minus[0] - 2, minus[1]), (minus[0] - 2, 75), (139, 75), (139, 84)], SIG)
line([out, (139, 84)], SIG)
dot(139, 84, SIG)
line([(139, 84), (141, 84)], SIG)
res(145, 84, "R9", "47R", SIG)
line([(149, 84), (156, 84)], SIG)
circ(158, 84, 1.6, INK)
text(158, 88.2, "PRE OUT RCA", 1.3, INK, "mm", True)
text(158, 86.4, "(Hot = チップ)", 1.0, GRY, "mm")
line([(139, 84), (139, 90.5)], SIG)
flag(139, 92.0, "PRE", SIG)
sbox(166, 66, 199, 106, [("PRE OUT は RCA と XLR の両方", 1.2, True), ("RCA: バッファ + 47Ω 直結", 1.05, False),
                         ("XLR: THAT1646 でバランス化 (下段)", 1.05, False),
                         ("PRE の旗は同名の点どうしが", 1.0, False), ("接続されます (交差を避けるため)", 1.0, False),
                         ("Flags with the same name connect.", 1.0, False)], ANA)

OFFY = 0
frame(1, 5, 199, 58, "出力段 Output stage:  PRE OUT XLR  /  SUB OUT  /  POWER AMP + bi-wire terminals")
# THAT1646 XLR
flag(6, 46, "PRE", SIG)
line([(9.6, 46), (14, 46)], SIG)
sbox(14, 36, 34, 52, [("U4", 1.4, True), ("THAT1646", 1.1, True), ("バランスライン", 1.0, False), ("ドライバ", 1.0, False), ("(XLR用)", 1.0, False)], INK)
for (y, col, t) in ((49, HOT, "XLR 2 Hot"), (40, COLD, "XLR 3 Cold")):
    line([(34, y), (43.8, y)], col)
    circ(45, y, 1.2, col)
    text(47, y, t, 1.1, col, "lm", True)
circ(45, 32, 1.2, INK)
text(47, 32, "XLR 1", 1.1, INK, "lm", True)
line([(43.8, 32), (40, 32)], INK)
res(36, 32, "R11", "10R||C5", INK)
line([(32, 32), (30, 32)], INK)
gnd(30, 32)
text(30, 54.6, "PRE OUT XLR (任意)", 1.25, INK, "mm", True)
# SUB OUT
flag(60, 46, "PRE", SIG)
text(60, 50.4, "L+R", 1.1, GRY, "mm")
line([(63.6, 46), (68, 46)], SIG)
sbox(68, 24, 104, 52, [("SUB OUT (モノ)", 1.35, True), ("L+R 反転加算 (1系統)", 1.1, False), ("→ 位相 0/180° → LPF 80/100/120Hz", 1.0, False), ("→ バッファ (前の図のアンバランス版)", 1.0, False), ("Mono sum + phase + LPF", 1.0, False), ("RCA = Hot / XLR は THAT1646 (任意)", 1.0, False)], ANA)
line([(104, 40), (110.4, 40)], SIG)
circ(112, 40, 1.6, INK)
text(112, 36.4, "SUB OUT RCA", 1.15, INK, "mm", True)
line([(104, 30), (108, 30)], SIG)
text(108.4, 30, "→ XLR (任意)", 1.1, GRY, "lm")
# power amp
flag(122, 40, "PRE", SIG)
line([(125.6, 40), (130, 40)], SIG)
sbox(130, 12, 150, 50, [("パワーアンプ", 1.3, True), ("Class-D", 1.2, True), ("シングルエンド入力", 1.05, False), ("(Class-AB でも可)", 1.0, False), ("例 Purifi", 1.0, False), ("1ET400A (SE入力)", 1.0, False)], ANA)
line([(150, 35), (153, 35)], HOT)
line([(150, 23), (153, 23)], COLD)
sbox(153, 14, 163, 46, [("K1", 1.3, True), ("DC保護", 1.0, False), ("リレー", 1.0, False), ("遅延", 1.0, False), ("ミュート", 1.0, False)], ANA)
line([(163, 35), (170, 35)], HOT)
line([(170, 32), (170, 38)], HOT)
line([(170, 38), (184.8, 38)], HOT)
line([(170, 32), (184.8, 32)], HOT)
dot(170, 35, HOT)
line([(163, 23), (174, 23)], COLD)
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
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\streaming_amp_analog_unbalanced.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
