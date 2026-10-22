def flag(x, y, t, col=INK):
    d.rectangle([*P(x - 3.0, y + 1.4), *P(x + 3.0, y - 1.4)], outline=col, width=LW, fill="white")
    text(x, y, t, 1.3, col, "mm", True)


text(3, 127, "Class AB パワーアンプ(アナログ・プリメイン)  Class AB power amplifier - analog integrated amplifier", 2.4, INK, "la", True)
text(3, 123.6, "1ch分 (Lch=Rch同一)  |  差動入力段 + VAS + Vbe倍率バイアス + 2段エミッタフォロワ出力  |  全体帰還  |  バイワイヤ対応スピーカー端子", 1.45, GRY)
text(3, 121.2, "参考設計 Reference design  |  値は机上計算。シミュレーション・実機測定は未実施 (Values are on paper only).  電源は外付けリニアDC電源 ±45V.", 1.2, GRY)

# input
circ(4, 48, 1.6, INK)
text(4, 52, "IN (RCA)", 1.2, INK, "mm", True)
line([(5.6, 48), (8, 48)], ANA)
res(12, 48, "R1", "47k", ANA)
line([(16, 48), (24, 48)], ANA)
box(24, 30, 48, 54, [L("入力段", 1.2, True), L("差動対 Q1/Q2", 1.05), L("2SC2240 ペア", 1.0), L("+ カレントミラー", 1.05), L("テイル電流 2mA", 1.0)], ANA)
text(25.5, 48, "+", 1.5, ANA, "lm", True)
text(25.5, 36, "−", 1.5, ANA, "lm", True)
# feedback network
box(2, 24, 18, 34, [L("帰還 Rf 22k", 1.05, True), L("Rg 1k (利得 ≈23)", 1.0)], ANA)
flag(10, 20, "FB", ANA)
line([(10, 21.4), (10, 24)], ANA)
line([(10, 34), (10, 36), (24, 36)], ANA)
# VAS
line([(48, 42), (60, 42), (60, 38)], ANA)
dot(60, 38, ANA)
line([(60, 38), (65.5, 38)], ANA)
q3 = bjt(72, 38, "npn", "Q3", "VAS 2SC3503", ANA)
line([q3["E"], (74.6, 31)], ANA)
res(74.6, 27, "R2", "100R", ANA, vertical=True)
line([(74.6, 23), (74.6, 22)], ANA)
rail(74.6, 22, "−V", PWR, up=False)
# Cdom
line([q3["C"], (74.6, 52)], ANA)
dot(74.6, 50, ANA)
line([(74.6, 50), (67.9, 50)], ANA)
hcap(67, 50, "C1", "68p", ANA)
line([(66.1, 50), (60, 50), (60, 38)], ANA)
# node A / B
line([(74.6, 52), (86.6, 52)], ANA)
line([(86.6, 58), (86.6, 38), (91.5, 38)], ANA)
dot(86.6, 52, ANA)
box(80, 58, 93, 82, [L("Vbe倍率", 1.1, True), L("Q4 BD139", 1.0), L("+ VR 500Ω", 1.0), L("(温度追従)", 0.95)], ANA)
line([(86.6, 82), (86.6, 97.2)], ANA)
dot(86.6, 94, ANA)
line([(86.6, 94), (91.5, 94)], ANA)
isrc(86.6, 100, "6mA", ANA)
line([(86.6, 102.8), (86.6, 103.5)], ANA)
rail(86.6, 103.5, "+V", PWR, up=True)
# drivers
q5 = bjt(98, 94, "npn", "Q5", "2SC5171", ANA)
line([q5["C"], (100.6, 101)], ANA)
rail(100.6, 101, "+V", PWR, up=True)
q6 = bjt(98, 38, "pnp", "Q6", "2SA1930", ANA)
line([q6["C"], (100.6, 31)], ANA)
rail(100.6, 31, "−V", PWR, up=False)
# outputs
q7 = bjt(110, 88, "npn", "Q7", "2SC5200 ×2並列", ANA)
q8 = bjt(110, 44, "pnp", "Q8", "", ANA)
line([q5["E"], (100.6, 88), q7["B"]], ANA)
line([q6["E"], (100.6, 44), q8["B"]], ANA)
line([q7["C"], (112.6, 95)], ANA)
rail(112.6, 95, "+V", PWR, up=True)
line([q8["C"], (112.6, 37)], ANA)
rail(112.6, 37, "−V", PWR, up=False)
line([q7["E"], (112.6, 80)], ANA)
res(112.6, 76, "R3", "0.33Ω", ANA, vertical=True)
line([(112.6, 72), (112.6, 66)], ANA)
line([q8["E"], (112.6, 52)], ANA)
res(112.6, 56, "R4", "0.33Ω", ANA, vertical=True)
line([(112.6, 60), (112.6, 66)], ANA)
dot(112.6, 66, ANA)
out_net(112.6, 66)
line([(116.6, 66), (116.6, 68.6)], ANA)
dot(116.6, 66, ANA)
flag(116.6, 70, "FB", ANA)
box(128, 88, 198, 116, [L("設計メモ Design notes", 1.4, True), L("出力 ≈ 100W / 8Ω (±45V)、アイドル電流 ≈ 50mA/組 (VR で調整)", 1.1),
  L("Q4 を出力段ヒートシンクに取り付け、温度変化に追従してバイアスを保つ", 1.05),
  L("Output ≈ 100 W / 8 ohm; idle ≈ 50 mA per output pair, set with the VR.", 1.05),
  L("Mount Q4 on the output heatsink so the bias follows temperature.", 1.05),
  L("電源: 外付けリニアDC電源 ±45V", 1.1), L("耐久: 出力素子 2 並列 (4Ω でも接合部 ≈91°C)、ヒートシンク 90°C で温度保護", 1.0)], ANA)
text(4, 14.0, "Q1/Q2: 2SC2240  Q3: 2SC3503  Q4: BD139  Q5: 2SC5171  Q6: 2SA1930  Q7: 2SC5200  Q8: 2SA1943 (各 ×2 並列)  Rz/Cz: ゾベル  L1//R: 出力コイル  K1: DC保護リレー", 1.15, INK)
text(4, 11.6, "FB 旗どうしは接続 / Flags with the same name are connected.   +V / −V: 外付けリニアDC電源から。", 1.15, GRY)

img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_classAB.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
