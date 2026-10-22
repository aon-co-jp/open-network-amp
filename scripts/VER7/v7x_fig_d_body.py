text(3, 127, "VER7  真空管プリアンプ(アナログ・プリメイン用)  Vacuum-tube preamplifier stage", 2.4, INK, "la", True)
text(3, 123.6, "1ch分 (Lch=Rch同一)  |  入力セレクタ → ボリューム → V1 12AU7 の片側 (電圧増幅) → V2 12AU7 の残り半分 (カソードフォロワ) → パワーアンプへ  |  アンバランス (RCA)", 1.45, GRY)
text(3, 121.2, "参考設計 Reference design  |  値は机上計算。シミュレーション・実機測定は未実施 (Values are on paper only).  B+ と ヒーターは外付けリニアDC電源から。", 1.2, GRY)

circ(4, 60, 1.6, INK)
text(4, 64, "IN (RCA ×3)", 1.2, INK, "mm", True)
line([(5.6, 60), (10, 60)], ANA)
box(10, 54, 26, 66, [L("入力セレクタ", 1.1, True), L("(リレー)", 1.0)], ANA)
line([(26, 60), (30, 60)], ANA)
box(30, 54, 46, 66, [L("ボリューム", 1.1, True), L("リレー式 ATT + 触覚ノブ", 0.9)], ANA)
line([(46, 60), (52, 60)], ANA)
res(56, 60, "R1", "1k", ANA)
line([(60, 60), (62, 60)], ANA)
dot(62, 60, ANA)
line([(62, 60), (62, 56)], ANA)
res(62, 52, "R2", "1M", ANA, vertical=True)
line([(62, 48), (62, 47)], ANA)
gnd(62, 47)
v1 = triode(70, 60, "V1", "12AU7 (1/2)", ANA)
# plate load + decoupling
line([v1["P"], (70, 72)], ANA)
dot(70, 70, ANA)
res(70, 76, "R3", "47k", ANA, vertical=True)
line([(70, 80), (70, 86)], ANA)
dot(70, 84, ANA)
res(70, 90, "Rd", "4.7k", ANA, vertical=True)
line([(70, 94), (70, 95)], ANA)
rail(70, 95, "B+ 250V", PWR, up=True)
line([(70, 84), (76, 84), (76, 82.6)], ANA)
d.line([*P(73.4, 82.6), *P(78.6, 82.6)], fill=ANA, width=LW)
d.line([*P(73.4, 80.8), *P(78.6, 80.8)], fill=ANA, width=LW)
text(80, 81.7, "Cd 47µF/400V", 1.1, GRY, "lm")
line([(76, 80.8), (76, 79)], ANA)
gnd(76, 79)
# cathode bias
line([v1["K"], (70, 50)], ANA)
dot(70, 50, ANA)
res(70, 46, "R4", "1k", ANA, vertical=True)
line([(70, 42), (70, 41.5)], ANA)
gnd(70, 41.5)
# coupling to V2
line([(70, 70), (80, 70)], ANA)
hcap(82, 70, "C1", "0.1µF", ANA)
line([(82.9, 70), (88, 70), (88, 60)], ANA)
dot(88, 60, ANA)
line([(88, 60), (88, 56)], ANA)
res(88, 52, "R5", "470k", ANA, vertical=True)
line([(88, 48), (88, 47)], ANA)
gnd(88, 47)
v2 = triode(96, 60, "V2", "12AU7 (2/2) CF", ANA)
line([v2["P"], (96, 72)], ANA)
rail(96, 72, "B+ 250V", PWR, up=True)
line([v2["K"], (96, 50)], ANA)
dot(96, 50, ANA)
res(96, 46, "R6", "10k", ANA, vertical=True)
line([(96, 42), (96, 41.5)], ANA)
gnd(96, 41.5)
line([(96, 50), (104, 50)], ANA)
hcap(106, 50, "C2", "2.2µF", ANA)
line([(106.9, 50), (112, 50)], ANA)
res(116, 50, "R7", "100R", ANA)
line([(120, 50), (126.4, 50)], ANA)
circ(128, 50, 1.6, INK)
text(128, 54.5, "PRE OUT → パワーアンプ", 1.2, INK, "mm", True)
box(134, 84, 198, 112, [L("設計メモ Design notes", 1.4, True), L("V1: 12AU7 の片側で電圧増幅 (計算: 利得 ≈ 11倍 = 約21dB)、V2: 残り半分のカソードフォロワ (出力 ≈ 1.4kΩ)", 1.05),
  L("B+ 250V は外付けリニアDC電源から遅延投入 (ウォームアップ ≈ 30秒)", 1.05),
  L("ヒーター 6.3V DC (V1・V2 各 0.3A) も外付け電源。DC点火でハムを抑える", 1.05),
  L("V1 provides voltage gain, V2 is a cathode follower for a low output impedance.", 1.0),
  L("B+ is switched on after a delay; the heaters run on regulated DC to avoid hum.", 1.0), L("耐久: ヒーターのソフトスタート・B+ 遅延で球寿命を延ばす (約 10,000 時間 = 1 日 4 時間で約 6.8 年)", 1.0)], ANA)
text(4, 14.0, "1本の 12AU7 (双3極管): V1 = 電圧増幅、V2 = カソードフォロワ   Rd/Cd: B+ のデカップリング   R4: カソード抵抗 (バイパスなしで歪みを低減)   C1/C2: フィルムコンデンサ", 1.15, INK)
text(4, 11.6, "B+ / 0V: 外付けリニアDC電源から。ヒーター 6.3V DC 配線は図から省略 (V1・V2 の 4-5 / 9 ピン)。", 1.15, GRY)

import textwrap as _tw
_y = 30.0
for _l in _tw.wrap('VER7 真空管版: 真空管プリ (12AU7) + VER7 の A級パワー (1.5A バイアスで 8Ω に 9W、ピーク 約 90dB・平均 約 75dB)。12 畳の部屋の小音量〜実用音量向け。ヒーターは 6.3V DC のソフトスタート、B+ は遅延投入、電源は外付けリニア DC。', 55 if any(ord(c) > 12000 for c in 'VER7 真空管版: 真空管プリ (12AU7) + VER7 の A級パワー (1.5A バイアスで 8Ω に 9W、ピーク 約 90dB・平均 約 75dB)。12 畳の部屋の小音量〜実用音量向け。ヒーターは 6.3V DC のソフトスタート、B+ は遅延投入、電源は外付けリニア DC。') else 100):
    text(104, _y, _l, 0.85, INK, 'la'); _y -= 1.2
_y -= 0.6
for _l in _tw.wrap('VER7 valve version: the 12AU7 valve preamp with the VER7 Class A power stage (1.5 A bias gives 9 W into 8 ohm, peaks about 90 dB, about 75 dB average), for quiet to practical levels in a 12-tatami room. 6.3 V DC heater with soft start, delayed B+ and the external linear DC supply.', 55 if any(ord(c) > 12000 for c in 'VER7 valve version: the 12AU7 valve preamp with the VER7 Class A power stage (1.5 A bias gives 9 W into 8 ohm, peaks about 90 dB, about 75 dB average), for quiet to practical levels in a 12-tatami room. 6.3 V DC heater with soft start, delayed B+ and the external linear DC supply.') else 100):
    text(104, _y, _l, 0.85, INK, 'la'); _y -= 1.2
_y -= 0.6
for _l in _tw.wrap('VER7 Röhre / Лампа / Valvola / Lampe: 9 W (8 Ω). Alle Texte in 8 Sprachen / all texts in 8 languages: README, manual-v7.', 55 if any(ord(c) > 12000 for c in 'VER7 Röhre / Лампа / Valvola / Lampe: 9 W (8 Ω). Alle Texte in 8 Sprachen / all texts in 8 languages: README, manual-v7.') else 100):
    text(104, _y, _l, 0.85, INK, 'la'); _y -= 1.2
_y -= 0.6
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_ver7_tube.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
