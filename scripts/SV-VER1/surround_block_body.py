import os
BAL = os.environ.get("BAL", "1") == "1"
exec(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_block_body.py", encoding="utf-8").read().split("text(3, 127")[0])
T = "全段バランス" if BAL else "アンバランス"
E = "Fully Balanced" if BAL else "Unbalanced"
text(3, 127, "最新サラウンド AV アンプ (%s)  Surround AV Amplifier (%s)  SV-VER1" % (T, E), 2.4, INK, "la", True)
text(3, 123.6, "Dolby Atmos・DTS:X (IMAX Enhanced 対応) 11.2.4 処理 / 7.1.4 スピーカー + サブウーファー 2 系統 (モノラル RCA + XLR) + 4DX 風の触覚 (バスシェーカー) 出力 2ch", 1.45, GRY)
text(3, 121.2, "参考設計 Reference design  |  IMAX Enhanced / Dolby / DTS の認証は別途ライセンスが必要。4DX は映画館の方式で、家庭用の公式規格は無いため触覚出力 + 制御ポートで近い体験を作る。", 1.15, GRY)
text(150, 119.0, "青 digital", 1.2, DIG, "la", True); text(163, 119.0, "緑 analog", 1.2, ANA, "la", True)
text(176, 119.0, "橙 power", 1.2, PWR, "la", True); text(188, 119.0, "灰 control", 1.2, CTL, "la", True)
box(2, 98, 30, 116, [L("HDMI 2.1 入力 ×6", 1.2, True), L("8K60 / 4K120・eARC・HDCP 2.3", 1.0), L("ARC/eARC 出力 + HDMI 出力 ×2", 1.0)], DIG)
box(34, 98, 62, 116, [L("ネットワーク / USB-C / I2S", 1.15, True), L("Wi-Fi 8・GbE・Bluetooth", 1.0), L("Qobuz・Roon・AirPlay", 1.0)], DIG)
box(66, 98, 94, 116, [L("アナログ入力", 1.2, True), L("XLR ×2 / RCA ×3" if BAL else "RCA ×4 / XLR ×1", 1.0), L("7.1ch マルチ入力", 1.0)], ANA)
box(98, 98, 140, 116, [L("制御・表示", 1.2, True), L("触覚ハイブリッド音量 VER6 (磁気エンコーダ2重・約17年)", 1.0), L("RS-232 / IP / トリガー出力 12V", 1.0)], CTL)
box(2, 68, 62, 92, [L("映像 + 音声デコード SoC / DSP (マルチコア)", 1.2, True), L("Dolby Atmos・DTS:X・IMAX Enhanced・Auro-3D", 1.0), L("11.2.4 オブジェクトレンダラ・ルーム補正 (測定マイク)", 1.0), L("ビットパーフェクト経路 (SW5 でバイパス)", 1.0)], DIG)
box(66, 68, 94, 92, [L("FPGA", 1.2, True), L("低ジッタ クロック (フェムト秒級)", 1.0), L("I2S/TDM 12ch 出力", 1.0)], DIG)
arrow([(16, 98), (16, 92)], DIG); arrow([(48, 98), (48, 92)], DIG); arrow([(80, 98), (80, 92)], ANA)
arrow([(62, 80), (66, 80)], DIG)
box(98, 68, 140, 92, [L("DAC 12ch", 1.2, True), L("AK4191 + BD34302 を 6 組 (2ch ずつ)", 1.0), L("PCM 最大 1536kHz / DSD1024", 1.0), L("各組をチャンネルの真下に配置 (配線最短)", 1.0)], ANA)
arrow([(94, 80), (98, 80)], DIG)
box(144, 68, 198, 92, [L("I/V → LPF → ボリューム → バッファ", 1.15, True), L("全 12ch を " + ("バランスのまま処理 (差動)" if BAL else "各ch 単相で処理 (差動→単相は DAC 直後の 1 段)"), 1.0), L("ラッチングリレー + 0.1% 薄膜抵抗 (ラダー)", 1.0)], ANA)
arrow([(140, 80), (144, 80)], ANA)
box(2, 36, 62, 62, [L("パワーアンプ 11ch (フロント 7 + ハイト 4)", 1.2, True), L("フロント L/C/R 3ch: Class AB (2 並列)", 1.0), L("他 8ch: クラス D (Eigentakt 型、発熱 約 1/9)", 1.0), L("バイワイヤ対応・DC 検出・リレー保護", 1.0)], ANA)
box(66, 36, 110, 62, [L("サブウーファー出力 ×2", 1.2, True), L("モノラル RCA + XLR (各系統)", 1.0), L("LPF 80/100/120Hz・LR4・位相可変", 1.0), L("グランドリフト SW・低雑音 0.28µV (VER5 の改良版)", 1.0)], ANA)
box(114, 36, 154, 62, [L("触覚 (4DX 風) 出力 ×2", 1.2, True), L("バスシェーカー用アンプ 2ch", 1.0), L("LFE + 効果トラックから生成", 1.0), L("制御ポートで椅子・風・照明へ", 1.0)], ANA)
box(158, 36, 198, 62, [L("ヘッドホン / PRE OUT", 1.2, True), L("4.4 / 6.35 / 3.5mm", 1.0), L("PRE OUT 11.2ch XLR" if BAL else "PRE OUT 11.2ch RCA", 1.0)], ANA)
line([(171, 68), (171, 65), (32, 65)], ANA)
for x in (32, 88, 134, 178):
    arrow([(x, 65), (x, 62)], ANA)
line([(32, 65), (178, 65)], ANA)
box(2, 6, 62, 30, [L("外付けリニア DC 電源 (トロイダル左右独立)", 1.15, True), L("バンク分割: 前 / 後+ハイト / サブ・触覚 / デジタル", 1.0), L("電解コンデンサは 45°C 以下の別筐体 (寿命 約 73 年)", 1.0)], PWR)
box(66, 6, 198, 30, [L("配線を短く・耐久・音質 設計メモ Design notes", 1.3, True),
  L("DAC → ボリューム → パワーアンプをチャンネルごとに一直線 (経路 約 40mm)。グランド面を直下に切れ目なく敷き、デジタル / アナログ / 電源を別区画 1 点接続 (擬似スター)", 1.0),
  L("Each channel runs in a straight line, DAC to volume to power amp (about 40 mm), over an unbroken ground plane; digital, analog and power areas are joined at one point.", 0.95),
  L("耐久: 出力素子 2 並列 (4Ω でも 約 91°C)・温度制御ファン・ラッチングリレー・非接触磁気エンコーダ (VER6 の音量ノブ)", 1.0)], PWR)
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\surround_%s.jpg" % ("balanced" if BAL else "unbalanced")
img.save(out, "JPEG", quality=92, dpi=(300, 300)); print(out)
