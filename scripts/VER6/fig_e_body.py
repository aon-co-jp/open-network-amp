def flag(x, y, t, col=INK):
    d.rectangle([*P(x - 3.0, y + 1.4), *P(x + 3.0, y - 1.4)], outline=col, width=LW, fill="white")
    text(x, y, t, 1.3, col, "mm", True)


text(3, 127, "外付けリニアDC電源  External linear DC power supply", 2.4, INK, "la", True)
text(3, 123.6, "AC → トロイダルトランス → 整流・大容量コンデンサ → リニアレギュレータ → DC出力 (別筐体)  |  Class A / AB / D と 半導体プリ / 真空管プリ の全バージョンに対応", 1.45, GRY)
text(3, 121.2, "参考設計 Reference design  |  値は机上計算。シミュレーション・実機測定は未実施 (Values are on paper only).  安全規格・絶縁・高電圧 (B+ 250V) の取り扱いに注意。", 1.2, GRY)

box(2, 92, 18, 108, [L("AC入力", 1.2, True), L("100V", 1.1), L("(IEC C14)", 1.0)], PWR)
box(22, 92, 42, 108, [L("EMIフィルタ", 1.1, True), L("ヒューズ", 1.0), L("突入電流制限", 1.0), L("(NTC/リレー)", 1.0)], PWR)
box(46, 56, 68, 110, [L("トロイダル×2", 1.2, True), L("左右独立(ﾃﾞｭｱﾙﾓﾉ)", 1.0, True), L("静電ｼｰﾙﾄﾞ+ﾐｭｰﾒﾀﾙ缶", 1.0), L("二次巻線(各):", 1.0), L("2×24V / 2×40V", 1.0), L("2×52V / 15V×2", 1.0), L("6.3V / 200V", 1.0)], PWR)
arrow([(18, 100), (22, 100)], PWR)
arrow([(42, 100), (46, 100)], PWR)
box(74, 98, 118, 110, [L("パワーレール ±V / +V", 1.2, True), L("ブリッジ整流 → 4×10,000µF → 直列パス・リニアレギュレータ", 1.0)], PWR)
box(74, 84, 118, 96, [L("アナログ ±15V", 1.2, True), L("整流 → LT3045 / LT3094 (超低ノイズ)", 1.0)], PWR)
box(74, 70, 118, 82, [L("B+ 250V (真空管プリ用)", 1.2, True), L("整流 → CRC → MOSFET容量倍増 → 遅延投入", 1.0)], PWR)
box(74, 56, 118, 68, [L("ヒーター 6.3V DC (真空管プリ用)", 1.2, True), L("整流 → LT3081 / LM338 (ソフトスタート)", 1.0)], PWR)
for y in (104, 90, 76, 62):
    arrow([(68, y), (74, y)], PWR)
box(126, 56, 156, 110, [L("DC出力コネクタ", 1.2, True), L("多ピン + 太い線", 1.0), L("+V / −V / 0V", 1.0), L("±15V", 1.0), L("B+ 250V", 1.0), L("6.3V DC", 1.0), L("センス線", 1.0), L("(リモートセンス)", 1.0)], PWR)
for y in (104, 90, 76, 62):
    arrow([(118, y), (126, y)], PWR)
box(162, 84, 198, 110, [L("保護・起動シーケンス", 1.2, True), L("DC / 過電流 / 過熱", 1.0), L("B+ は ヒーター後に投入", 1.0), L("LED / 電圧表示", 1.0)], PWR)
arrow([(156, 97), (162, 97)], PWR)
box(162, 56, 198, 80, [L("出力電圧 (版ごと)", 1.2, True), L("Class A: ±24V", 1.05), L("Class AB: ±45V", 1.05), L("Class D: +60V", 1.05), L("真空管プリ: B+ 250V", 1.05), L("ヒーター 6.3V DC", 1.05)], PWR)

# regulator core
text(2, 54.5, "レギュレータ中核 (+V側)  Series-pass regulator core", 1.5, PWR, "la", True)
q1 = bjt(60, 36, "npn", "Q1", "2SC5200 (パス)", ANA)
line([q1["C"], (62.6, 47)], ANA)
rail(62.6, 47, "+Vraw (整流後)", PWR, up=True)
line([q1["E"], (62.6, 33)], ANA)
res(62.6, 29, "Re", "0.1Ω", ANA, vertical=True)
line([(62.6, 25), (62.6, 22)], ANA)
dot(62.6, 22, ANA)
line([(62.6, 22), (104, 22)], ANA)
circ(105.6, 22, 1.6, PWR)
text(110, 22, "+V OUT", 1.3, PWR, "lm", True)
dot(88, 22, ANA)
line([(88, 22), (88, 18.6)], ANA)
d.line([*P(85.4, 18.6), *P(90.6, 18.6)], fill=ANA, width=LW)
d.line([*P(85.4, 16.8), *P(90.6, 16.8)], fill=ANA, width=LW)
text(92.5, 17.7, "Cout 4,700µF", 1.1, GRY, "lm")
line([(88, 16.8), (88, 14.5)], ANA)
gnd(88, 14.5)
plus, minus, out = opamp(30, 36, "U1", "OPA", plus_top=True)
line([out, (35.5, 36), (40, 36)], ANA)
res(44, 36, "Rb", "100R", ANA)
line([(48, 36), (53.5, 36)], ANA)
box(6, 43, 22, 51, [L("基準電圧", 1.05, True), L("LM4040 + RC", 1.0)], ANA)
line([(14, 43), (14, 39.25), (24.5, 39.25)], ANA)
box(32, 14, 52, 22, [L("分圧 R1/R2", 1.05, True), L("Vout=Vref(1+R1/R2)", 0.95)], ANA)
line([(62.6, 22), (52, 22)], ANA)
line([(32, 18), (20, 18), (20, 32.75), (24.5, 32.75)], ANA)
box(70, 26, 94, 38, [L("電流制限", 1.05, True), L("Re 両端 0.6V で", 0.95), L("Q1 のベースを引き込む", 0.95)], ANA)
box(116, 14, 198, 46, [L("設計メモ Design notes", 1.4, True), L("−V 側は PNP パス素子で同じ構成 (ミラー)。出力は大容量・低ノイズ", 1.05),
  L("トランス: トロイダル左右独立 + 静電シールド + 商用DCブロッカ + 整流ダイオードのスナバ。二次 A 2×24V / AB 2×40V / D 2×52V", 1.0),
  L("ヒーター・B+・±15V は別巻線・別レギュレータで他のレールと分離", 1.05),
  L("Separate windings and regulators keep the rails apart (low noise).", 1.0),
  L("本体との間は太いケーブル + センス線で電圧降下を補償", 1.05),
  L("The main unit is connected by a thick cable plus sense wires.", 1.0), L("耐久: 電解コンデンサ (105°C 10,000h) は外付け筐体 (45°C 以下) で 約 73 年 (計算)", 1.0), L("NTC + リレーの突入電流制限・MOV・DC / 過電流 / 温度の保護", 1.0)], PWR)
text(2, 8.5, "外付けのため、トランスの磁気・熱・ノイズを本体から離せます。コンデンサ容量・トランス容量は版ごとの出力 (Class A ≈ 6A/ch) に合わせて選定。", 1.15, GRY)

img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_psu.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
