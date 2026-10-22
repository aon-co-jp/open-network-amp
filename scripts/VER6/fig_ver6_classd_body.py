import math
exec(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_block_body.py", encoding="utf-8").read().split("text(3, 127")[0])
V = 45.0
pd_ab = 2 * V * V / (math.pi ** 2 * 8)
pd_d = (V * V / (2 * 8)) * (1 / 0.9 - 1)
L_, C_ = 22e-6, 0.47e-6
f0 = 1 / (2 * math.pi * math.sqrt(L_ * C_))
text(3, 127, "VER6 追加: アナログ入力のクラス D パワーアンプ (完全バランス / アンバランス)  Analog-input Class D power stage", 2.3, INK, "la", True)
text(3, 123.6, "Eigentakt 型 (自己発振 + 負帰還)。デジタル PWM 変換を使わず、DAC の後はアナログのまま。全 3 系統 (半導体プリ・真空管プリ・ネットワーク版) に選択可。", 1.4, GRY)
text(3, 121.2, "参考設計 Reference design. Python の計算 (SPICE・実機測定ではありません)。 Python calculations, not SPICE or bench measurements.", 1.2, GRY)
box(2, 88, 30, 112, [L("入力", 1.2, True), L("XLR (バランス) / RCA", 1.0), L("ボリューム VER6 の後", 1.0)], ANA)
box(36, 88, 70, 112, [L("入力バッファ + 積分器", 1.15, True), L("バランス版: 差動のまま", 1.0), L("アンバランス版: 単相", 1.0)], ANA)
box(76, 88, 110, 112, [L("自己発振 + 負帰還", 1.15, True), L("Eigentakt 型・約 500kHz", 1.0), L("出力から直接フィードバック", 1.0)], ANA)
box(116, 88, 150, 112, [L("ハーフブリッジ", 1.15, True), L("GaN / MOSFET + ゲートドライバ", 1.0), L("デッドタイム最小化", 1.0)], PWR)
box(156, 88, 198, 112, [L("出力 LC フィルタ + ゾベル", 1.15, True), L("22µH / 0.47µF (共振 約 %.0fkHz)" % (f0 / 1000), 1.0), L("RC ダンピングで 16Ω のピークを抑える", 1.0)], ANA)
for a, b in ((30, 36), (70, 76), (110, 116), (150, 156)):
    arrow([(a, 100), (b, 100)], ANA)
box(2, 48, 62, 80, [L("保護・制御", 1.2, True), L("DC 検出・過電流・温度・スピーカーリレー", 1.0), L("電源投入時のポップ防止ミュート", 1.0), L("バイワイヤ対応スピーカー端子 (金/ロジウムめっき)", 1.0)], CTL)
box(68, 48, 132, 80, [L("電源 (外付けリニア DC・R コア)", 1.2, True), L("パワー段: 非安定の大容量 C (4×22,000µF)", 1.0), L("アナログ ±15V・クロック: 低雑音リニア", 1.0), L("スイッチング電源は使わない", 1.0)], PWR)
box(138, 48, 198, 80, [L("配置 (配線を短く)", 1.2, True), L("パワー段は筐体の外側、シールド板で仕切る", 1.0), L("500kHz のスイッチングをアナログに入れない", 1.0), L("チャンネルごとに 40mm の直線", 1.0)], PWR)
box(2, 8, 98, 42, [L("計算結果 (Python)  Results", 1.3, True),
    L("発熱 (8Ω 最大): クラス D 約 %.0fW / Class AB 約 %.0fW (1 ch、損失)。効率 90%% を仮定" % (pd_d, pd_ab), 1.0),
    L("LC フィルタ: 4Ω で 20kHz −0.7dB、8Ω で +0.9dB、16Ω でピーク 7.6dB → ゾベルで 0.7dB (計算、簡易モデル)", 1.0),
    L("Heat per channel at 8 ohm full power: about %.0f W (Class D) versus %.0f W (Class AB). Filter peak into 16 ohm 7.6 dB, 0.7 dB with a Zobel." % (pd_d, pd_ab), 0.95)], ANA)
box(104, 8, 198, 42, [L("注意 Notes", 1.3, True),
    L("クラス D のほうが必ず音がよいとは言えず、フィルタ・電源・配線次第です。", 1.0),
    L("Class D is not automatically better sounding; filter, supply and wiring decide.", 0.95),
    L("未実施: 実機測定 (THD・雑音・出力インピーダンス・EMI)、過渡応答。", 1.0)], CTL)
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_ver6_classD.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, round(pd_d), round(pd_ab), round(f0))
