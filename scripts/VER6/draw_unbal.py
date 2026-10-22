from PIL import Image, ImageDraw, ImageFont

W, H = 200, 168
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


SIG = (25, 115, 60)

text(3, 119.5, "アンバランス設計アンプ用 モノラル・サブウーファー出力 VER5  Mono Subwoofer Output for an Unbalanced Amplifier VER5", 2.5, INK, "la", True)
text(3, 116.0, "参考回路図 Reference schematic  |  ボリューム後段から分岐 tapped after volume (サブ音量が連動)  |  "
     "L+R加算 → 位相 → LPF 80/100/120Hz → RCA出力 / 任意でXLR(バランス化)", 1.5, GRY)
text(3, 113.4, "VER5: 雑音を低減 (SK の R を下げ C を増やす)・GND リフト・出力ミュートリレーを追加 (VER3/4: LR4・位相可変・サブソニック HPF)  VER5: lower noise, ground lift, mute relay.", 1.25, GRY)
text(140, 113.4, "緑 green = 信号 signal (シングルエンド)", 1.25, SIG, "la", True)
text(176, 113.4, "橙 orange = スイッチ", 1.25, ORG, "la", True)

frame(1, 22, 62, 110, "STAGE 1  L+R 加算  Summing")
frame(64, 22, 100, 110, "STAGE 2 位相")
frame(102, 22, 152, 110, "STAGE 3  2次バターワース LPF")
frame(154, 22, 199, 110, "STAGE 4  出力 Outputs")

YC = 75
col = SIG
# ------------------------------------------------ stage 1
yl, yr = YC + 12, YC + 6
text(2, yl, "L (入力)", 1.7, col, "lm", True)
text(2, yr, "R (入力)", 1.7, col, "lm", True)
plus, minus, out = opamp(46, YC, "U1A", "OPA1612  ch.A", plus_top=False)
res(20, yl, "R1", "3.32k 0.1%", col)
line([(13, yl), (16, yl)], col)
res(20, yr, "R2", "3.32k 0.1%", col)
line([(13, yr), (16, yr)], col)
xb = 29
line([(24, yl), (xb, yl), (xb, minus[1])], col)
line([(24, yr), (xb, yr)], col)
dot(xb, yr, col)
line([(xb, minus[1]), minus], col)
yf = YC + 19.5
res(46, yf, "Rf1", "1.65k 0.1%", col)
line([(xb, yl), (xb, yf), (42, yf)], col)
xo = out[0] + 4.5
line([(50, yf), (xo, yf), (xo, out[1])], col)
line([out, (xo, out[1])], col)
dot(xo, out[1], col)
dot(xb + 3, yf, col)
dot(xo, yf, col)
cfy = yf + 5.2
line([(xb + 3, yf), (xb + 3, cfy), (36.8, cfy)], col)
d.line([*P(36.8, cfy + 1.8), *P(36.8, cfy - 1.8)], fill=col, width=LW)
d.line([*P(38.4, cfy + 1.8), *P(38.4, cfy - 1.8)], fill=col, width=LW)
line([(38.4, cfy), (xo, cfy), (xo, yf)], col)
text(37.6, cfy + 3.0, "Cf 33p C0G", 1.3, GRY, "mm")
line([plus, (plus[0] - 6, plus[1])], col)
res(plus[0] - 6, plus[1] - 4.5, "Rb", "825", col, vertical=True)
line([(plus[0] - 6, plus[1] - 8.5), (plus[0] - 6, plus[1] - 9.5)], col)
gnd(plus[0] - 6, plus[1] - 9.5)
text(3, 107.0, "シングルエンド入力 (ボリューム後段)  Single-ended inputs, post-volume", 1.2, GRY, "la")

d.rectangle([*P(3, 55), *P(35, 44)], outline=(200, 120, 20), width=int(LW * .7))
text(19, 53.0, "SW1  MONO / STEREO 切替 (R2連動)", 1.25, ORG, "mm", True)
text(19, 50.6, "MONO: LとRを1本に加算 summed", 1.2, GRY, "mm")
text(19, 48.4, "STEREO: R側は同一回路へ", 1.2, GRY, "mm")
text(19, 46.2, "→ SUB OUT 2 (2本目のRCA/XLR)", 1.2, GRY, "mm")
text(3, 25.9, "入力あたり利得 Rf/R = 0.5 → 同相の低音 (L=R) は 0 dB = (L+R)/2 (単純加算の +6 dB を吸収)", 1.15, GRY)
text(3, 24.2, "反転加算。最終極性は SW2 で決定  Inverting summer; SW2 sets the final polarity.", 1.15, GRY)

# ------------------------------------------------ stage 2
line([(56, YC), (66, YC)], col)
dot(66, YC, col)
line([(66, YC), (66, 78), (88, 78)], col)
line([(66, YC), (66, 55.25), (69, 55.25)], col)
res(73, 55.25, "R7", "10k 0.1%", col)
line([(77, 55.25), (79.5, 55.25)], col)
dot(78.5, 55.25, col)
p2, m2, o2 = opamp(85, 52, "U1B", "OPA1612  ch.B", plus_top=False)
line([(78.5, 55.25), (78.5, 66), (81, 66)], col)
res(85, 66, "R8", "10k 0.1%", col)
line([(89, 66), (94, 66), (94, 52), o2], col)
dot(94, 66, col)
line([(94, 66), (94, 72), (88, 72)], col)
line([p2, (75, p2[1])], col)
gnd(75, p2[1])
G = (130, 130, 130)
d.line([*P(96, 75), *P(88, 78)], fill=G, width=LW)
d.line([*P(96, 75), *P(88, 72)], fill=G, width=LW)
for (x, y) in ((88, 78), (88, 72), (96, 75)):
    dot(x, y, col)
text(86.6, 78.2, "A", 1.4, ORG, "rm", True)
text(86.6, 72.2, "B", 1.4, ORG, "rm", True)
line([(96, 75), (103, 75)], col)
d.rectangle([*P(66, 90), *P(98, 40)], outline=(200, 120, 20), width=int(LW * .7))
text(82, 88.0, "SW2  位相 PHASE  0° / 180°", 1.35, ORG, "mm", True)
text(82, 85.5, "(SPDT)", 1.2, GRY, "mm")
for i, t in enumerate(["A: U1A出力を直結 = 180°", "B: U1B (反転) 経由 = 0° (正相)", "リレーなら無音切替"]):
    text(82, 42.5 - 0 + 0, "", 1.0)
text(66, 38.0, "A: U1A出力を直結 = 180°", 1.2, GRY, "la")
text(66, 36.0, "B: U1B (反転) 経由 = 0° (正相)", 1.2, GRY, "la")
text(66, 34.0, "リレーなら無音切替で使える", 1.2, GRY, "la")
text(66, 31.6, "Relay = click-free switching", 1.2, GRY, "la")


# ------------------------------------------------ stage 3
y = YC
line([(103, y), (108, y)], col)
res(112, y, "R5", "6.34k/5.11k/4.22k", col)
line([(116, y), (119, y)], col)
dot(119, y, col)
res(123, y, "R6", "6.34k/5.11k/4.22k", col)
line([(127, y), (130, y)], col)
dot(130, y, col)
plus, minus, out = opamp(141, y, "U2A", "OPA1612  ch.A", plus_top=True)
line([(130, y), (130, plus[1]), plus], col)
line([(130, y), (130, y - 5.0)], col)
vcap(130, y - 7.0, "C2", "220n 固定", col=col, left=True)
line([(130, y - 8.1), (130, y - 11.5)], col)
gnd(130, y - 11.5)
yfb = y + 12.0
line([(119, y), (119, yfb), (124.6, yfb)], col)
d.line([*P(124.6, yfb + 2.6), *P(124.6, yfb - 2.6)], fill=col, width=LW)
d.line([*P(126.4, yfb + 2.6), *P(126.4, yfb - 2.6)], fill=col, width=LW)
line([(126.4, yfb), (150, yfb), (150, y)], col)
text(125.5, yfb + 3.2, "C1", 1.5, col, "mm", True)
text(125.5, yfb + 4.9, "440n 固定", 1.3, GRY, "mm")
line([minus, (minus[0] - 2.5, minus[1]), (minus[0] - 2.5, y - 17.0), (150, y - 17.0), (150, y)], col)
line([out, (150, y)], col)
dot(150, y, col)
line([(150, y), (152.1, y)], col)
hcap(153, y, "C5", "2.2µF", col)
line([(153.9, y), (158, y)], col)
dot(156, y, col)
line([(156, y), (156, y - 4)], col)
res(156, y - 8, "R9", "10k", col, vertical=True)
line([(156, y - 12), (156, y - 13)], col)
gnd(156, y - 13)

d.rectangle([*P(104, 52), *P(150, 26)], outline=(200, 120, 20), width=int(LW * .7))
text(127, 50.0, "SW3  ロータリー  BYPASS / 80 / 100 / 120 Hz", 1.3, ORG, "mm", True)
for i, t in enumerate([
    "R5・R6 の値を切替 (C1 440n・C2 220n 固定)",
    "fc = 1/(2πR√(C1C2)),  Q = 0.707",
    "80 Hz: R 6.34k (計算 80.7 Hz)",
    "100 Hz: R 5.11k (計算 100.0 Hz)",
    "120 Hz: R 4.22k (計算 121.3 Hz)",
    "BYPASS = 全帯域モノ (サブ側クロスオーバー使用)",
    "12 dB/oct。24 dB/oct は2段目を追加",
]):
    text(127, 47.0 - 2.9 * i, t, 1.1, GRY, "mm")

# ------------------------------------------------ stage 4
dot(158, y, col)
# RCA branch
line([(158, y), (158, 95), (165.1, 95)], col)
d.line([*P(165.1, 97.6), *P(165.1, 92.4)], fill=col, width=LW)
d.line([*P(166.9, 97.6), *P(166.9, 92.4)], fill=col, width=LW)
text(166, 100.2, "C6 4.7µ film", 1.3, col, "mm", True)
line([(166.9, 95), (171, 95)], col)
res(175, 95, "R12", "100R", col)
line([(179, 95), (190.4, 95)], col)
circ(192, 95, 1.6, col)
text(198, 90.0, "SUB OUT RCA (Hot = チップ)", 1.2, INK, "ra", True)
text(166, 106.0, "RCA出力 (DCカット+直列抵抗)", 1.25, INK, "la", True)
# XLR branch (optional)
line([(158, y), (158, 62), (164, 62)], col)
d.rectangle([*P(164, 70), *P(180, 52)], outline=INK, width=LW, fill=(250, 250, 235))
text(172, 67.6, "U4", 1.5, INK, "mm", True)
text(172, 65.7, "THAT1646", 1.2, INK, "mm", True)
text(172, 64.0, "バランスライン", 1.05, GRY, "mm")
text(172, 62.4, "ドライバ", 1.05, GRY, "mm")
text(172, 60.8, "SE→バランス", 1.05, GRY, "mm")
text(165, 62, "IN", 1.0, col, "lm", True)
line([(180, 66), (190.8, 66)], col)
line([(180, 56), (190.8, 56)], col)
circ(192, 66, 1.2, col)
circ(192, 56, 1.2, col)
text(192, 66, "2", 1.3, col, "mm", True)
text(192, 56, "3", 1.3, col, "mm", True)
text(192, 69.2, "XLR 2 Hot", 1.15, col, "mm", True)
text(192, 52.8, "XLR 3 Cold", 1.15, col, "mm", True)
text(181.4, 64.7, "OUT+", 1.0, GRY, "la")
text(181.4, 54.7, "OUT−", 1.0, GRY, "la")
circ(192, 46, 1.2, INK)
text(192, 46, "1", 1.3, INK, "mm", True)
line([(190.8, 46), (186, 46)], INK)
res(182, 46, "R11", "10R || C5 10n", INK)
line([(178, 46), (174, 46)], INK)
gnd(174, 46)
text(198, 74.5, "SUB OUT XLR (任意・バランス化)", 1.25, INK, "ra", True)
text(198, 41.5, "XLRが不要なら U4 一式は省略", 1.1, GRY, "ra")

# ------------------------------------------------ bottom
frame(1, 1, 98, 21, "POWER / BYPASS  電源・バイパス (全IC共通)")
pw = [
    ("±15 V 低雑音ポストレギュレータ (LT3045 / LT3094、または LM317/LM337 + RC)", INK),
    ("アンプ既存のアナログ電源 (または小型の別巻線) から供給  Use the existing analog rails.", GRY),
    ("各IC: 100 nF X7R をピン直近 + 10 µF / 電源ごと (10 mm 以内)", INK),
    ("アナログGNDへ1点アース。RCA入出力のGNDが多点接続にならないよう注意 (ハム対策)", INK),
    ("任意: ミュートリレー。U2B など未使用側のopampは入力を固定して休ませる", GRY),
    ("R1〜R8 は 0.1% 25 ppm 薄膜抵抗アレイ。全てSMDで自動実装向き  All SMD.", GRY),
]
for i, (t, c) in enumerate(pw):
    text(3, 16.2 - 2.45 * i, t, 1.3, c)
frame(100, 1, 199, 21, "BILL OF MATERIALS  部品表 (概要)")
for i, t in enumerate([
    "U1, U2   OPA1612 デュアル (低コストなら NJM4580 / LME49720)  ×2",
    "U4   THAT1646 (バランスラインドライバ、XLR出力が必要な場合のみ)  ×1",
    "R1, R2 3.32k / R7, R8 10k 0.1% 25ppm 薄膜    Rf1 1.65k 0.1%    Rb 825 1%",
    "C1 440n / C2 220n PPS・C0G フィルム (固定)   R5, R6 6.34k / 5.11k / 4.22k",
    "C6 4.7µ フィルム   R11 10R   R12 100R   C5 10n   Cf 33p C0G",
    "SW1 MONO/STEREO   SW2 位相 (SPDT)   SW3 LPF (BYPASS/80/100/120 Hz)",
    "J1 RCA 入力2系統   J2 RCA 出力   J3 XLR-3 オス (任意)",
]):
    text(102, 17.2 - 2.2 * i, t, 1.2, INK)

exec(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\ver3_panel.py", encoding="utf-8").read())
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\mono_sub_out_unbalanced.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
