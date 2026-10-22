def flag(x, y, t, col=INK):
    d.rectangle([*P(x - 3.0, y + 1.4), *P(x + 3.0, y - 1.4)], outline=col, width=LW, fill="white")
    text(x, y, t, 1.3, col, "mm", True)


text(3, 127, "Class A パワーアンプ(アナログ・プリメイン)  Class A power amplifier - analog integrated amplifier", 2.4, INK, "la", True)
text(3, 123.6, "1ch分 (Lch=Rch同一)  |  Nch MOSFET 共通ソース + Pch 定電流源 (CCS) 負荷  |  全体帰還 + DCサーボ  |  バイワイヤ対応スピーカー端子", 1.45, GRY)
text(3, 121.2, "参考設計 Reference design  |  値は机上計算。シミュレーション・実機測定は未実施 (Values are on paper only).  電源は外付けリニアDC電源 ±24V.", 1.2, GRY)

# input
circ(4, 60.75, 1.6, INK)
text(4, 64.5, "IN (RCA)", 1.2, INK, "mm", True)
line([(5.6, 60.75), (8, 60.75)], ANA)
res(12, 60.75, "R1", "1k", ANA)
line([(16, 60.75), (40.5, 60.75)], ANA)
dot(22, 60.75, ANA)
line([(22, 60.75), (22, 58)], ANA)
res(22, 54, "R2", "47k", ANA, vertical=True)
line([(22, 50), (22, 49)], ANA)
gnd(22, 49)
plus, minus, out = opamp(46, 64, "U1", "OPA1612", plus_top=False)
# feedback network box
box(24, 72, 40, 82, [L("帰還回路", 1.15, True), L("Rf 10k / Rg 470Ω", 1.0), L("(利得 ≈22倍)", 1.0)], ANA)
flag(32, 86, "FB", ANA)
line([(32, 84.6), (32, 82)], ANA)
line([(32, 72), (32, 67.25), (40.5, 67.25)], ANA)
# DC servo
box(24, 36, 44, 46, [L("DCサーボ U2", 1.1, True), L("積分 1MΩ / 1µF", 1.0)], ANA)
flag(52, 41, "FB", ANA)
line([(49, 41), (44, 41)], ANA)
line([(34, 46), (34, 60.75)], ANA)
dot(34, 60.75, ANA)
# gate drive
line([out, (56, 64), (56, 57)], ANA)
res(56, 53, "R5", "100R", ANA, vertical=True)
line([(56, 49), (56, 42), (63.5, 42)], ANA)
q1 = mos(70, 42, "n", "", "", ANA)
text(60, 33.5, "Q1", 1.4, ANA, "lm", True)
text(60, 31.5, "IRFP240", 1.1, GRY, "lm")
q2 = mos(70, 80, "p", "Q2 (CCS)", "IRFP9240", ANA)
line([q2["D"], q1["D"]], ANA)
dot(72.6, 61, ANA)
# source / rails
line([q1["S"], (72.6, 35)], ANA)
res(72.6, 31, "R6", "0.22Ω", ANA, vertical=True)
line([(72.6, 27), (72.6, 24)], ANA)
rail(72.6, 24, "−V (−24V)", PWR, up=False)
line([q2["S"], (72.6, 89)], ANA)
res(72.6, 93, "R7", "0.62Ω", ANA, vertical=True)
line([(72.6, 97), (72.6, 98)], ANA)
rail(72.6, 98, "+V (+24V)", PWR, up=True)
# CCS bias: current servo (I = Vset / R7)
line([q2["G"], (60, 80)], ANA)
box(40, 72, 60, 88, [L("電流制御 U3", 1.1, True), L("OPA1612 + VR1 2kΩ", 0.95), L("I = Vset ÷ R7", 1.0)], ANA)
line([(72.6, 89), (56, 89), (56, 88)], ANA)
line([(72.6, 97), (46, 97), (46, 88)], ANA)
dot(72.6, 89, ANA)
text(44, 91.5, "+V 側", 1.0, GRY, "rm")
text(54, 91.5, "ソース側", 1.0, GRY, "rm")
# output network
out_net(72.6, 61)
line([(75, 61), (75, 66)], ANA)
dot(75, 61, ANA)
flag(75, 68, "FB", ANA)
box(128, 70, 198, 112, [L("設計メモ Design notes", 1.4, True), L("Q1 は定電流源 Q2 を負荷とした Class A (共通ソース)", 1.15), L("アイドル電流 = Vset ÷ R7 = 1.43V ÷ 0.62Ω ≈ 2.3A/ch (VR1 で調整。MOSFET の Vgs に依存しない)", 1.1),
  L("出力 ≈ 20W / 8Ω、ピーク電流 ≈ 2.2A < アイドル電流 → Class A を維持", 1.1), L("発熱 ≈ 120W/ch (±24V × 2.5A)。大型ヒートシンクが必要", 1.1),
  L("Idle current ≈ 2.3 A keeps Q1 in Class A up to ≈ 20 W / 8 ohm.", 1.05), L("Dissipation ≈ 120 W per channel: a large heatsink is needed.", 1.05),
  L("電源: 外付けリニアDC電源 ±24V (大容量・低ノイズ)", 1.1), L("耐久: ヒートシンク ≤0.3°C/W/ch + 温度制御ファン、高温時はアイドル電流を自動で下げる", 1.0)], ANA)
text(4, 14.0, "Q1: IRFP240 (Nch MOSFET)  Q2: IRFP9240 (Pch MOSFET, 定電流源)  U1 / U2 / U3: OPA1612 (±15V)  Rz/Cz: ゾベル  L1//R: 出力コイル  K1: DC保護リレー", 1.15, INK)
text(4, 11.6, "FB 旗どうしは接続 / Flags with the same name are connected.   +V / −V / 0V: 外付けリニアDC電源から。", 1.15, GRY)

img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_classA.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
