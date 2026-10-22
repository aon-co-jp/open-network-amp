import math
exec(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_block_body.py", encoding="utf-8").read().split("text(3, 127")[0])
text(3, 127, "クラス D アナログ版 + 外付けリニア DC 電源  CD-VER2  Analog-input Class D amplifier with external linear DC supply", 2.3, INK, "la", True)
text(3, 123.6, "全体の耐久性・音質・配線短縮の見直し (VER1 は VER6 の amp_ver6_classD.jpg)。 Durability, sound and shorter wiring reviewed (VER1 = amp_ver6_classD.jpg in VER6).", 1.35, GRY)
text(3, 121.2, "参考設計 Reference design. Python の計算 (SPICE・実機測定ではありません)。 Python calculations, not SPICE or bench measurements.", 1.2, GRY)
text(2, 117.5, "本体 Main unit", 1.5, ANA, "la", True)
box(2, 94, 28, 114, [L("入力", 1.2, True), L("XLR / RCA", 1.0), L("ボリューム VER6", 1.0)], ANA)
box(32, 94, 62, 114, [L("入力バッファ", 1.15, True), L("+ 積分器", 1.0), L("(バランス / 単相)", 1.0)], ANA)
box(66, 94, 100, 114, [L("自己発振クラス D", 1.15, True), L("Eigentakt 型 約 500kHz", 1.0), L("チャンネルごと 1 モジュール", 1.0)], PWR)
box(104, 94, 140, 114, [L("LC フィルタ + ゾベル", 1.15, True), L("22µH / 0.47µF + RC", 1.0), L("スピーカーリレー・DC 検出", 1.0)], ANA)
box(144, 94, 198, 114, [L("スピーカー端子", 1.15, True), L("バイワイヤ・金 / ロジウムめっき", 1.0), L("ケーブル最短 (リレーのすぐ隣)", 1.0)], ANA)
for a, b in ((28, 32), (62, 66), (100, 104), (140, 144)):
    arrow([(a, 104), (b, 104)], ANA)
text(2, 89.5, "外付けリニア DC 電源 筐体 (45°C 以下)  External linear DC supply case", 1.5, PWR, "la", True)
box(2, 64, 26, 86, [L("AC 100V", 1.2, True), L("IEC C14 + EMI フィルタ", 1.0), L("ヒューズ・MOV", 1.0)], PWR)
box(30, 64, 54, 86, [L("投入", 1.2, True), L("NTC 10Ω + リレー", 1.0), L("DC ブロッカ (偏磁防止)", 1.0)], PWR)
box(58, 64, 90, 86, [L("R コア トランス 1.0kVA", 1.2, True), L("左右独立・静電シールド", 1.0), L("ミューメタル缶", 1.0)], PWR)
box(94, 64, 130, 86, [L("整流 (ループ 20mm 以下)", 1.15, True), L("ソフトリカバリ + RC スナバ", 1.0), L("コンデンサ端子に直付け", 1.0)], PWR)
box(134, 64, 166, 86, [L("パワー段レール (非安定)", 1.15, True), L("4×22,000µF 63V + フィルム", 1.0), L("グランドは 1 点スター", 1.0)], PWR)
box(170, 64, 198, 86, [L("低雑音リニア", 1.15, True), L("容量倍増 → LT3045 / 3094", 1.0), L("クロック・DAC は専用", 1.0)], ANA)
for a, b in ((26, 30), (54, 58), (90, 94), (130, 134), (166, 170)):
    arrow([(a, 75), (b, 75)], PWR)
line([(150, 86), (150, 90.5), (83, 90.5)], PWR)
arrow([(83, 90.5), (83, 94)], PWR)
text(116, 91.2, "DC ケーブル 6mm² 0.8m + センス線 (アナログ側)", 1.0, PWR, "mm", True)
box(2, 6, 62, 44, [L("配線を短く (CD-VER2 の変更)", 1.25, True),
    L("DC ケーブル: 6mm² 0.8m に短縮 (ピーク 13.6A で 62mV、VER1 の 281mV)", 1.0),
    L("整流 → コンデンサのループ 20mm 以下 (スパイク 4.0V → 1.0V)", 1.0),
    L("パワーモジュールは スピーカー端子のすぐ隣、DAC・ボリュームと シールド板で仕切る", 1.0),
    L("チャンネルごとに入力から出力へ 約 40mm の一直線、グランド面を直下に", 1.0)], ANA)
box(66, 6, 134, 44, [L("耐久性 (CD-VER2 の変更)", 1.25, True),
    L("電解 63V (レール 45V の 1.4 倍)・リップル電流 50% 以下・フィルム並列", 1.0),
    L("45°C で約 52 年 (リップル発熱 +5K)、旧 +20K だと約 18 年", 1.0),
    L("NTC + リレーの投入、DC ブロッカ、MOV・過電圧・過電流・温度・DC 出力の保護", 1.0),
    L("発熱はクラス D のため小さく (8Ω 最大で 1ch 約 14W)、ファンはほぼ停止", 1.0)], PWR)
box(138, 6, 198, 44, [L("音質 (CD-VER2 の変更)", 1.25, True),
    L("リップル 0.10V → 容量倍増で 約 1mV → LT3045/3094 で 約 0.1µV (仮定)", 1.0),
    L("クロック・DAC は 専用レギュレータ、他と共用しない", 1.0),
    L("16Ω でのフィルタのピーク 7.6dB を ゾベルで 0.7dB に", 1.0),
    L("クラス D が必ず音がよいとは限らず、実機測定が必要", 1.0)], ANA)
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\cd_v2_block.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out)
