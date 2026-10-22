import sys
TUBE = bool(globals().get("TUBE", False))
if TUBE:
    title = "アナログ・プリメインアンプ (真空管プリ版)  Analog integrated amplifier - vacuum-tube preamp version  VER5"
    sub = "外付けリニアDC電源  +  真空管プリ (12AX7 + 12AU7)  +  パワーアンプ 3種から選択 (Class A / Class AB / Class D)  |  PRE OUT・SUB OUT・バイワイヤ対応スピーカー端子"
    pre = [L("真空管プリ", 1.25, True), L("V1 12AX7 (電圧増幅)", 1.0), L("V2 12AU7 (カソードF)", 1.0), L("B+ 250V / ヒーター", 1.0)]
    outname = "amp_block_tube.jpg"
else:
    title = "アナログ・プリメインアンプ (半導体プリ版)  Analog integrated amplifier - solid-state preamp version  VER5"
    sub = "外付けリニアDC電源  +  半導体プリ (OPA1612 ライン段)  +  パワーアンプ 3種から選択 (Class A / Class AB / Class D)  |  PRE OUT・SUB OUT・バイワイヤ対応スピーカー端子"
    pre = [L("半導体プリ", 1.25, True), L("OPA1612 ライン段", 1.0), L("(バッファ + ゲイン)", 1.0), L("±15V", 1.0)]
    outname = "amp_block_solid.jpg"
text(3, 127, title, 2.4, INK, "la", True)
text(3, 123.6, sub, 1.45, GRY)
text(3, 121.2, "参考設計 Reference design  |  パワーアンプは交換式モジュール (同じ筐体・同じ入出力)。値は机上計算で、実機測定は未実施。", 1.2, GRY)
text(150, 118.0, "緑 analog", 1.2, ANA, "la", True)
text(166, 118.0, "橙 power", 1.2, PWR, "la", True)

# external PSU
lines = [L("外付けリニアDC電源", 1.3, True, PWR), L("(別筐体)", 1.0), L("AC → トロイダル", 1.0), L("→ 整流・大容量C", 1.0), L("→ リニアレギュレータ", 1.0), L("出力 (版ごと):", 1.05, True),
         L("Class A: ±24V", 1.0), L("Class AB: ±45V", 1.0), L("Class D: +60V", 1.0), L("アナログ ±15V", 1.0)]
if TUBE:
    lines += [L("B+ 250V (遅延投入)", 1.0), L("ヒーター 6.3V DC", 1.0)]
lines += [L("センス線 + 保護", 1.0)]
box(2, 14, 46, 112, lines, PWR)

# input row
box(52, 96, 76, 112, [L("アナログ入力", 1.15, True), L("RCA ×3 / XLR", 1.0), L("(デジタル化せず)", 0.95)], ANA)
arrow([(76, 104), (82, 104)], ANA)
box(82, 96, 104, 112, [L("入力セレクタ", 1.15, True), L("(リレー)", 1.0)], ANA)
arrow([(104, 104), (110, 104)], ANA)
box(110, 94, 142, 114, pre, ANA)
arrow([(142, 104), (148, 104)], ANA)
box(148, 96, 172, 112, [L("ボリューム", 1.2, True), L("電子 / リレー式", 0.95), L("触覚ノブ SW6", 0.95)], ANA)

# power amp modules
d.rectangle([*P(110, 90), *P(176, 60)], outline=ANA, width=int(LW * .7))
text(143, 88.0, "パワーアンプ (交換式モジュール: 1つ選択)  Power amp module (choose one)", 1.15, ANA, "mm", True)
box(112, 62, 130, 84, [L("Class A", 1.2, True), L("MOSFET + CCS", 0.95), L("≈ 20W / 8Ω", 0.95), L("±24V", 1.0)], ANA)
box(132, 62, 152, 84, [L("Class AB", 1.2, True), L("ディスクリート", 0.95), L("≈ 100W / 8Ω", 0.95), L("±45V", 1.0)], ANA)
box(154, 62, 174, 84, [L("Class D", 1.2, True), L("アナログ入力", 0.95), L("≈ 150W / 8Ω", 0.95), L("+60V", 1.0)], ANA)
line([(160, 96), (160, 92), (121, 92)], ANA)
for x in (121, 142, 164):
    line([(x, 92), (x, 90)], ANA)
    arrow([(x, 90), (x, 84)], ANA)
line([(160, 92), (164, 92)], ANA)
# pre out / sub out
box(52, 76, 76, 90, [L("PRE OUT", 1.2, True), L("RCA + XLR", 1.0)], ANA)
box(52, 58, 76, 72, [L("SUB OUT (モノ)", 1.15, True), L("RCA + XLR", 1.0)], ANA)
line([(121, 92), (64, 92), (64, 90)], ANA)
arrow([(64, 92), (64, 90)], ANA)
arrow([(64, 76), (64, 72)], ANA)
# outputs
line([(121, 62), (121, 56), (164, 56)], ANA)
line([(142, 62), (142, 56)], ANA)
line([(164, 62), (164, 56)], ANA)
arrow([(142, 56), (142, 52)], ANA)
box(116, 38, 168, 52, [L("DC保護 + スピーカーリレー", 1.2, True), L("(起動 / 停止時のミュート)", 1.0)], ANA)
arrow([(168, 45), (174, 45)], ANA)
box(174, 36, 198, 54, [L("スピーカー端子", 1.15, True), L("バイワイヤ対応", 1.15, True), L("HF / LF ×2組", 1.0)], ANA)
box(52, 32, 108, 52, [L("ヘッドホンアンプ (VER5)", 1.2, True), L("3.5mm バランス/SE 兼用 · 4.4mm バランス · 6.35mm SE", 0.95), L("スピーカーと同時に動作 / ゲイン SW7 ANALOG・DIGITAL", 0.95)], ANA)
arrow([(64, 58), (64, 52)], ANA)
# power distribution
box(52, 14, 198, 28, [L("DC入力コネクタ → 各ブロックへ分配   (+V/−V/0V" + (" / ±15V / B+ 250V / ヒーター 6.3V" if TUBE else " / ±15V") + ")   センス線で電圧降下を補償", 1.1, False, PWR)], PWR)
arrow([(46, 21), (52, 21)], PWR)
text(52, 32, "電源ケーブル: 太い線 + センス線  Thick cable plus sense wires", 1.1, PWR)
text(52, 8.5, ("真空管プリ版: B+ は遅延投入 (ヒーターが温まってから)、ヒーターは安定化DC。" if TUBE else "半導体プリ版: プリ段は ±15V のリニア電源で駆動。") +
     "  パワーアンプの種類を変えても、入出力と筐体は共通。", 1.15, GRY)

img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad" + "\\" + outname
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
