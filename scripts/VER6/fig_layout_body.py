NET = bool(globals().get("NET", True))
LDO = (60, 130, 90)


def small(x0, y0, x1, y1, t, col=PWR):
    d.rectangle([*P(x0, y1), *P(x1, y0)], outline=col, width=LW, fill=(252, 244, 230))
    text((x0 + x1) / 2, (y0 + y1) / 2, t, 0.95, col, "mm", True)


def blk(x0, y0, x1, y1, lines, col=ANA, fill=(250, 250, 240)):
    box(x0, y0, x1, y1, lines, col, fill)


title = ("筐体内レイアウト VER5 (配線最短・ネットワーク版)  Internal layout VER5 - network version" if NET else
         "筐体内レイアウト VER5 (配線最短・アナログ版)  Internal layout VER5 - analog version")
text(3, 127, title, 2.4, INK, "la", True)
text(3, 123.6, "上から見た図 (上 = 背面、下 = 前面)  |  左右完全分離 (デュアルモノ)  |  信号は中央から左右へ一直線  |  ケーブルを使わず基板どうしを直接接続", 1.45, GRY)
text(3, 121.2, "参考設計 Reference design  |  配線長は設計目標 (実機で確認)  Wire lengths are design targets.", 1.2, GRY)

d.rectangle([*P(2, 112), *P(198, 8)], outline=(150, 160, 190), width=int(LW * .8))
text(4, 110.8, "背面 REAR", 1.2, (60, 80, 150), "la", True)
text(4, 11.0, "前面 FRONT  (表示・ボリュームノブ・電源スイッチ)", 1.2, (60, 80, 150), "la", True)

# rear terminals
blk(5, 96, 40, 109, [L("スピーカー端子 L", 1.1, True), L("バイワイヤ HF/LF", 1.0)], ANA)
blk(160, 96, 195, 109, [L("スピーカー端子 R", 1.1, True), L("バイワイヤ HF/LF", 1.0)], ANA)
blk(44, 100, 62, 109, [L("入力", 1.0, True), L("RCA/XLR", 0.95)], ANA)
blk(138, 100, 156, 109, [L("PRE / SUB OUT", 0.95, True), L("RCA+XLR", 0.95)], ANA)
blk(114, 100, 134, 109, [L("DC IN", 1.0, True), L("外付け電源", 0.95)], PWR)
if NET:
    blk(66, 100, 110, 109, [L("USB-C / LAN / HDMI / アンテナ (背面中央)", 1.0, True)], DIG)

# power amps (outer sides)
blk(8, 40, 44, 90, [L("パワーアンプ L", 1.2, True), L("(Class A / AB / D)", 1.0), L("出力リレー K1 を", 1.0), L("端子の真後ろに配置", 1.0), L("局所コンデンサ + LDO", 1.0)], ANA)
blk(156, 40, 192, 90, [L("パワーアンプ R", 1.2, True), L("(Class A / AB / D)", 1.0), L("出力リレー K1 を", 1.0), L("端子の真後ろに配置", 1.0), L("局所コンデンサ + LDO", 1.0)], ANA)
arrow([(24, 90), (24, 96)], ANA)
arrow([(174, 90), (174, 96)], ANA)
text(27, 93, "≤ 30mm", 1.0, GRY, "lm")
text(177, 93, "≤ 30mm", 1.0, GRY, "lm")

if NET:
    # centre: DAC, left/right chains
    blk(84, 52, 116, 72, [L("DAC", 1.2, True), L("AK4191 + BD34302", 1.0), L("(中央・前寄り)", 1.0)], DIG)
    blk(70, 54, 81, 70, [L("I/V", 1.1, True), L("LPF L", 1.0)], ANA)
    blk(119, 54, 130, 70, [L("I/V", 1.1, True), L("LPF R", 1.0)], ANA)
    blk(56, 54, 67, 70, [L("ボリューム", 0.95, True), L("L", 1.0)], ANA)
    blk(133, 54, 144, 70, [L("ボリューム", 0.95, True), L("R", 1.0)], ANA)
    blk(46, 54, 53, 70, [L("バッファ", 0.8, True), L("L", 0.9)], ANA)
    blk(147, 54, 154, 70, [L("バッファ", 0.8, True), L("R", 0.9)], ANA)
    for x0, x1, t in ((81, 84, "≤8"), (67, 70, "≤20"), (53, 56, "≤12"), (44, 46, "≤20")):
        arrow([(x1, 62), (x0, 62)], ANA)
    for x0, x1 in ((116, 119), (130, 133), (144, 147), (154, 156)):
        arrow([(x0, 62), (x1, 62)], ANA)
    text(75.5, 50.6, "≤8mm", 0.95, GRY, "mm")
    text(60, 50.6, "≤12mm", 0.95, GRY, "mm")
    text(124.5, 50.6, "≤8mm", 0.95, GRY, "mm")
    text(139, 50.6, "≤12mm", 0.95, GRY, "mm")
    # LDO next to stages
    for (x, y) in ((70, 71.5), (56, 71.5), (119, 71.5), (133, 71.5), (96, 73.5)):
        small(x, y, x + 8, y + 3.5, "LDO")
    # digital zone
    d.rectangle([*P(66, 98), *P(134, 76)], outline=DIG, width=int(LW * .8))
    text(67, 97.5, "デジタル領域 (シールド) + アイソレータで GND 分離", 1.0, DIG, "la", True)
    blk(68, 78, 88, 92, [L("ストリーマ", 1.0, True), L("Wi-Fi/BT (遠く)", 0.9)], DIG)
    blk(90, 78, 110, 92, [L("DDC / FPGA", 1.0, True), L("MQA XU316", 0.95)], DIG)
    blk(112, 78, 132, 92, [L("クロック", 1.0, True), L("+ アイソレータ", 0.9)], DIG)
    arrow([(100, 78), (100, 72)], DIG)
    text(103, 75, "≤8mm", 0.95, GRY, "lm")
else:
    blk(84, 56, 116, 82, [L("入力セレクタ", 1.1, True), L("+ ボリューム", 1.1, True), L("デュアルモノ", 1.0), L("(中央)", 1.0)], ANA)
    pre = "真空管プリ L" if False else "プリ L"
    blk(66, 58, 82, 80, [L("プリ段 L", 1.1, True), L("半導体 or", 0.9), L("真空管", 0.9)], ANA)
    blk(118, 58, 134, 80, [L("プリ段 R", 1.1, True), L("半導体 or", 0.9), L("真空管", 0.9)], ANA)
    blk(46, 58, 62, 80, [L("ラインバッファ", 0.85, True), L("L", 0.9)], ANA)
    blk(138, 58, 154, 80, [L("ラインバッファ", 0.85, True), L("R", 0.9)], ANA)
    for x0, x1 in ((84, 82), (66, 62), (46, 44)):
        arrow([(x0, 69), (x1, 69)], ANA)
    for x0, x1 in ((116, 118), (134, 138), (154, 156)):
        arrow([(x0, 69), (x1, 69)], ANA)
    text(83, 55.6, "≤8", 0.95, GRY, "mm")
    text(64, 55.6, "≤12", 0.95, GRY, "mm")
    text(117, 55.6, "≤8", 0.95, GRY, "mm")
    text(136, 55.6, "≤12", 0.95, GRY, "mm")
    for (x, y) in ((66, 81.5), (118, 81.5), (46, 81.5), (138, 81.5)):
        small(x, y, x + 8, y + 3.5, "LDO")
    blk(86, 86, 114, 96, [L("電源分配 (B+ / ヒーター / ±15V)", 0.95, True), L("真空管プリ版は ヒーター線をツイスト", 0.9)], PWR)
    arrow([(124, 100), (112, 96)], PWR)

if NET:
    blk(90, 26, 110, 46, [L("ヘッドホン基板", 1.0, True), L("前面ジャックに直付け", 0.9), L("≤30mm", 0.9)], ANA)
    blk(136, 82, 160, 98, [L("サブウーファー基板", 0.95, True), L("RCA+XLR 直近", 0.9)], ANA)
    arrow([(148, 98), (148, 100)], ANA)
else:
    blk(90, 28, 110, 48, [L("ヘッドホン基板", 1.0, True), L("前面ジャックに直付け", 0.9), L("≤30mm", 0.9)], ANA)
    blk(120, 84, 146, 98, [L("サブウーファー基板", 0.95, True), L("RCA+XLR 直近", 0.9)], ANA)
# star ground
circ(100, 38, 2.0, INK)
text(104, 38, "1点アース (スターグランド): 中央のボリューム/DAC の真下", 1.1, INK, "lm", True)
# notes
box(8, 12, 192, 32, [L("配線短縮の要点  Key points", 1.3, True),
                     L("1chの信号経路 ≈ 60mm (設計目標。VER2 の 95mm の約 63%、一般的な配置の約 1/5)。中央から左右へ一直線で、折り返しや長いケーブルなし", 1.05),
                     L("基板どうしはコネクタ直結 (信号ケーブルなし)。スピーカー端子はパワーアンプ基板の背面端に直付け。各段の横に LDO と局所コンデンサ (ポイント・オブ・ロード)", 1.05),
                     L("VER5: about 60 mm per channel. Short, straight signal path from the centre outwards, board-to-board connectors, speaker terminals right behind the output relays, LDOs next to each stage.", 1.0),
                     L("Hot / Cold は並走・同長。デジタル/無線はシールドして遠ざけ、GND は 1 点で接続。外付け電源なので本体にトランスなし。", 1.05)], ANA)

img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
outn = "amp_layout_net.jpg" if NET else "amp_layout_analog.jpg"
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad" + "\\" + outn
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
