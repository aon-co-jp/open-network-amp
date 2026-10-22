text(3, 127, "ヘッドホンアンプ HP-VER2 (前面・通常プリメインアンプと AV アンプの両方)  Headphone amplifier — front panel: 3.5 / 4.4 / 6.35 mm / XLR (stereo 4-pin, two mono 3-pin)", 2.4, INK, "la", True)
text(3, 123.6, "1ch分 (Lch=Rch同一・完全バランス)  |  バス (ラインバッファ出力) から分岐 → アナログゲイン段 → 電流バッファ → ジャック  |  スピーカー出力・ヘッドホン出力 各々に ON/OFF スイッチ", 1.45, GRY)
text(3, 121.2, "参考設計 Reference design  |  値は机上計算。シミュレーション (図) は計算のみ・実機測定は未実施。 Values are on paper only.", 1.2, GRY)


def flag(x, y, t, col=INK):
    d.rectangle([*P(x - 3.0, y + 1.4), *P(x + 3.0, y - 1.4)], outline=col, width=LW, fill="white")
    text(x, y, t, 1.3, col, "mm", True)


HY, CY = 100, 66
flag(5, HY, "PRE+", HOT)
flag(5, CY, "PRE−", COLD)
for (y, col, nm, tag) in ((HY, HOT, "U5A", "H"), (CY, COLD, "U5B", "C")):
    line([(8, y), (12, y)], col)
    res(16, y, "R20" if tag == "H" else "R21", "47k", col)
    line([(20, y), (24, y)], col)
    plus, minus, out = opamp(32, y, nm, "OPA1612", plus_top=True)
    line([(24, y), (24, plus[1]), plus], col)
    # feedback
    line([minus, (26, minus[1]), (26, y - 10), (44, y - 10), (44, y)], col)
    text(27, y - 13, "→ Rg ラダー (ゲイン段)", 0.9, GRY, "la")
    res(34, y - 10, "Rf", "1k", col)
    line([(44, y), (50, y)], col)
    line([out, (44, y)], col)
    dot(44, y, col)
    # gain ladder box to ground from minus node
    line([(26, minus[1]), (26, y - 14)], col)
    dot(26, minus[1], col)
box(2, 39, 40, 47, [L("ゲイン段 (アナログ): Rg を リレー K5-K7 で切替", 1.0, True), L("0 / +6 / +12 / +18 dB  (Hot / Cold 同時)", 0.95)], ANA)
# current buffers
for (y, col, nm) in ((HY, HOT, "U6A"), (CY, COLD, "U6B")):
    line([(50, y), (54, y)], col)
    plus, minus, out = opamp(62, y, nm, "LME49600 ×2並列", plus_top=True, w=10, h=12)
    line([(54, y), (54, plus[1]), plus], col)
    line([minus, (59, minus[1]), (59, y - 9), (73, y - 9), (73, y)], col)
    line([out, (73, y)], col)
    dot(73, y, col)
    line([(73, y), (76, y)], col)
    res(80, y, "Rs", "2.2Ω", col)
    line([(84, y), (90, y)], col)
    dot(90, y, col)
    # real feedback from after Rs : annotate
text(70, HY + 8, "帰還は Rs の後ろから (出力 ≈ 0.1Ω)", 1.0, GRY, "mm")
text(70, CY + 8, "", 1.0)
# output selector
box(94, 44, 124, 112, [L("出力リレー", 1.2, True), L("K2: XLR (4ピン / 3ピン×2)", 1.0), L("K3: 4.4mm バランス", 1.0), L("K4: 3.5mm・6.35mm", 1.0), L("", 0.5), L("ジャック検出で自動切替", 0.95), L("TRS 挿入 → Cold を切離し", 0.95), L("Hot のみ + スリーブ=GND", 0.95), L("", 0.5), L("起動 / 停止 ミュート", 0.95), L("DC 保護 (サーボ U7)", 0.95)], ANA)
line([(90, HY), (94, HY)], HOT)
line([(90, CY), (94, CY)], COLD)
# jacks
box(132, 98, 198, 112, [L("4.4mm バランス (Pentaconn)", 1.1, True), L("L+ L− R+ R−  (4極)", 0.95)], ANA)
box(132, 80, 198, 94, [L("3.5mm バランス / アンバランス兼用 (4極ジャック)", 1.05, True), L("TRRS = バランス / TRS = アンバランス (自動検出)", 0.95)], ANA)
box(132, 62, 198, 76, [L("6.35mm アンバランス (TRS)", 1.1, True), L("Tip = Hot / Sleeve = GND", 0.95)], ANA)
arrow([(124, 105), (132, 105)], ANA)
arrow([(124, 87), (132, 87)], ANA)
arrow([(124, 69), (132, 69)], ANA)
box(132, 44, 164, 58, [L("XLR 3ピン ×2 (モノラル)", 1.0, True), L("L 用・R 用 各: 1=GND 2=+ 3=−", 0.85)], ANA)
box(166, 44, 198, 58, [L("XLR 4ピン ×1 (ステレオ)", 1.0, True), L("1=L+ 2=L− 3=R+ 4=R−", 0.85)], ANA)
arrow([(124, 51), (132, 51)], ANA)
# modes
box(100, 8, 198, 38, [L("2種類のゲイン調整 (スピーカーとヘッドホンの両方に同時に効く)", 1.2, True),
                       L("SW7 = ANALOG: ゲイン段 / アッテネータで調整 (ビットパーフェクト維持)", 1.05),
                       L("SW7 = DIGITAL: FPGA のデジタルゲインで調整 (±0.5dB 刻み)", 1.05),
                       L("前面に ON/OFF スイッチ 2 個: スピーカー用・ヘッドホン用 (独立。信号は通さない非接触スイッチ → 密閉リレーを駆動)", 1.05),
                       L("ゲイン自動推奨: ヘッドホンの抵抗を検出 (16〜600Ω) → 低い抵抗・高感度ほど 0dB 側 (ヒスを抑える)", 1.05), L("ヘッドホン専用 LDO ±15V (LT3045 / LT3094) + 局所コンデンサ・星型アース", 1.05)], PWR)
box(44, 26, 98, 38, [L("アンバランス版プリの場合", 1.0, True), L("Cold は 反転バッファ (U8) で作る", 0.95)], ANA)
box(2, 26, 40, 38, [L("電流バッファ", 1.0, True), L("±0.5A / 脚、並列 2 個", 0.95)], ANA)
text(4, 8.0, "U5: OPA1612 (ゲイン段)  U6: LME49600 ×2 並列/脚 (電流バッファ)  U7: サーボ OPA1612  Rs: 2.2Ω 薄膜  K3-K7: 信号用リレー (金接点・低ノイズ)  ±15V は専用 LDO から", 1.1, INK)
text(4, 5.6, "PRE+/PRE− の旗は 本体のラインバッファ出力 (PRE) と同じ点。 Flags with the same name are connected.", 1.1, GRY)

img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_hp2.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
