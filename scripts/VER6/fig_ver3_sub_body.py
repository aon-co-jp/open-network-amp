import math, json
exec(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\plot_helpers.py", encoding="utf-8").read())
text(3, 127, "サブウーファー出力 VER3 の仮想シミュレーション  Subwoofer output VER3 - simulation", 2.4, INK, "la", True)
text(3, 123.6, "Python による計算 (交流応答・設計計算)。実機測定ではありません。過渡応答・歪み (THD) の SPICE 解析は未実施です。", 1.45, GRY)
text(3, 121.2, "Calculated in Python (AC response and design arithmetic). Not bench measurements. Transient and THD SPICE runs were not done.", 1.2, GRY)
GR, BL, RD = (25, 115, 60), (30, 70, 180), (190, 30, 30)
fc = 80.0


def bw2_lp(f):
    s = 1j * f / fc
    return 1 / (s * s + math.sqrt(2) * s + 1)


def bw2_hp(f):
    s = 1j * f / fc
    return (s * s) / (s * s + math.sqrt(2) * s + 1)


db = lambda x: 20 * math.log10(max(abs(x), 1e-6))
fs = [20 * (400 / 20) ** (i / 200) for i in range(201)]
mx, my = plot(8, 70, 96, 108, 20, 400, -20, 6, True, "① サブ LPF + メイン HPF の合成 (電気的な和, 80Hz)  Sum of sub LPF and main HPF", "Hz", "dB")
curve(mx, my, [(f, max(-20, db(bw2_lp(f) ** 2 + bw2_hp(f) ** 2))) for f in fs], GR)
curve(mx, my, [(f, max(-20, db(bw2_lp(f) + bw2_hp(f)))) for f in fs], RD, dashed=True)
curve(mx, my, [(f, max(-20, db(-bw2_lp(f) + bw2_hp(f)))) for f in fs], BL, dashed=True)
legend(48, 105, [("LR4 (24dB/oct) 同相: 平坦 0dB", GR, False), ("12dB/oct 同相: 谷", RD, True), ("12dB/oct 逆相: +3dB のこぶ", BL, True)])
fap = [10 * (300 / 10) ** (i / 200) for i in range(201)]
mx, my = plot(108, 70, 192, 108, 10, 300, -180, 0, True, "② オールパス位相 (C 100nF、VR2 を変える)  All-pass phase", "Hz", "deg")
for rv, col in ((22e3, GR), (47e3, BL), (100e3, RD), (220e3, (120, 60, 160))):
    curve(mx, my, [(f, -2 * math.degrees(math.atan(2 * math.pi * f * rv * 0.1e-6))) for f in fap], col)
legend(150, 105, [("VR2 22k", GR, False), ("47k", BL, False), ("100k", RD, False), ("220k (60Hz で −166°)", (120, 60, 160), False)])
rows = [
    ("① 加算段の雑音 (7〜120Hz): 入力 R 10k / Rf 4.99k = 0.21µV → 4.99k / 2.49k = 0.15µV (−3.3dB)。プリアウト (≈47Ω) への負荷は −0.08dB",
     "① Summer noise (7-120 Hz): 0.21 uV with 10k / 4.99k becomes 0.15 uV with 4.99k / 2.49k (-3.3 dB); the load on a 47 ohm pre-out is -0.08 dB."),
    ("② クロスオーバー: メインが 24dB/oct (LR4) なら、サブも LR4 (SW4) で同相 → 電気的な和は平坦 (±0dB)。12dB/oct は逆相でも +3dB のこぶ (80Hz) になる",
     "② Crossover: with a 24 dB/oct (LR4) main speaker the sub should be LR4 (SW4) and in phase; the electrical sum is flat. At 12 dB/oct a +3 dB hump appears at 80 Hz even with inverted polarity."),
    ("③ 位相: 1次オールパス (C 100nF + VR2 0〜220k) で 60Hz の位相を 0° → −166° まで連続可変。SW2 の 180° 反転と併用で全周をカバー",
     "③ Phase: a first-order all-pass (100 nF + VR2 0-220 kohm) varies the 60 Hz phase continuously from 0 to -166 deg; with the 180 deg switch SW2 the full circle is covered."),
    ("④ VER2 から継続: LPF 80.6 / 100.3 / 121.2Hz、サブソニック HPF 7.2Hz (DC を遮断)。 未実施: 実機の位相・歪み・過渡応答",
     "④ Kept from VER2: LPF at 80.6 / 100.3 / 121.2 Hz and the 7.2 Hz subsonic HPF (blocks DC). Not done: real-hardware phase, distortion and transient response."),
]
y = 60
text(6, 63.5, "VER3 の要点 / 確認結果  VER3 improvements and checks", 1.6, INK, "la", True)
for ja, en in rows:
    text(6, y, ja, 1.15, INK, "la")
    text(6, y - 2.0, en, 1.05, GRY, "la")
    y -= 5.6
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\mono_sub_out_v3_test.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
