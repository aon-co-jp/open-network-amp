import math
DIG = (30, 70, 180); ANA = (25, 115, 60); PWR = (190, 100, 20); CTL = (110, 110, 110)
def box(x0, y0, x1, y1, lines, col, fill=(250, 250, 240)):
    d.rectangle([*P(x0, y1), *P(x1, y0)], outline=col, width=LW, fill=fill)
    n = len(lines); cy = (y0 + y1) / 2; top = cy + (n - 1) * 1.05
    for i, (t, sz, b, c) in enumerate(lines):
        text((x0 + x1) / 2, top - 2.1 * i, t, sz, c or INK, "mm", b)
def arrow(pts, col=INK):
    line(pts, col)
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    a = math.atan2(y1 - y0, x1 - x0)
    for s_ in (0.45, -0.45):
        line([(x1, y1), (x1 - 1.8 * math.cos(a - s_), y1 - 1.8 * math.sin(a - s_))], col)
def L(t, sz=1.15, b=False, c=None): return (t, sz, b, c)
text(3, 127, "スピーカー / ヘッドホン / サブウーファー出力の ON・OFF スイッチ (前面・耐久性と音質重視)  Speaker / headphone / subwoofer ON-OFF switches", 2.3, INK, "la", True)
text(3, 123.6, "ユーザーが触るスイッチは音声信号を通さない (非接触) → 信号経路には 密閉・ラッチング・金/ルテニウム接点のリレーだけ。両方 ON で同時使用も可能。", 1.35, GRY)
text(3, 121.2, "参考設計 Reference design. Python の計算 (SPICE・実機測定ではありません)。 Python calculations, not bench measurements.", 1.2, GRY)
box(2, 92, 30, 114, [L("前面スイッチ ×3", 1.2, True), L("SPEAKER ON/OFF", 1.0), L("HEADPHONE ON/OFF", 1.0), L("SUBWOOFER ON/OFF", 1.0), L("ホール素子の押しボタン (非接触) + LED", 0.85)], CTL)
box(38, 92, 66, 114, [L("制御 MCU", 1.2, True), L("状態を記憶・チャタリング除去", 0.95), L("シーケンス制御", 0.95), L("DC 検出で強制 OFF", 0.95)], DIG)
box(74, 92, 102, 114, [L("リレー ドライバ", 1.2, True), L("ラッチング (コイル通電は切替時だけ)", 0.9), L("フライバック保護", 0.95)], DIG)
for a, b in ((30, 38), (66, 74)): arrow([(a, 103), (b, 103)], CTL)
box(112, 105, 160, 116, [L("スピーカーリレー K1 (L/R・Hot/Cold)", 1.0, True), L("パワーリレー、接点 2 並列 (約 5mΩ)、AgSnO2 + 金フラッシュ", 0.85)], PWR)
box(112, 92, 160, 103, [L("ヘッドホンリレー K9 (L/R・Hot/Cold)", 1.0, True), L("密閉信号リレー、金クラッド/ルテニウム接点、2 並列", 0.85)], ANA)
box(112, 79, 160, 90, [L("サブウーファーリレー K10 (RCA + XLR・Hot/Cold)", 1.0, True), L("密閉信号リレー、金クラッド/ルテニウム接点、2 並列 (ライン信号)", 0.85)], ANA)
line([(102, 110), (112, 110)], DIG); arrow([(110, 110), (112, 110)], DIG)
line([(102, 98), (108, 98), (108, 97.5), (112, 97.5)], DIG); arrow([(110, 97.5), (112, 97.5)], DIG)
line([(108, 97.5), (108, 84.5), (112, 84.5)], DIG); arrow([(110, 84.5), (112, 84.5)], DIG)
box(168, 105, 198, 116, [L("スピーカー端子", 1.0, True), L("バイワイヤ・金めっき", 0.85)], ANA)
box(168, 92, 198, 103, [L("ヘッドホン端子", 1.0, True), L("3.5 / 4.4 / 6.35 / XLR", 0.85)], ANA)
box(168, 79, 198, 90, [L("サブウーファー出力", 1.0, True), L("モノラル RCA + XLR ×2系統", 0.85)], ANA)
arrow([(160, 110.5), (168, 110.5)], PWR); arrow([(160, 97.5), (168, 97.5)], ANA); arrow([(160, 84.5), (168, 84.5)], ANA)
box(2, 50, 98, 74, [L("切替シーケンス (ポップ音・接点の傷みを防ぐ)", 1.2, True), L("OFF: ① 出力段をミュート → ② 20ms 待つ → ③ リレーを開く (電流ゼロ)。ON: ① リレーを閉じる → ② 50ms → ③ ミュート解除", 0.95), L("Turn OFF: mute, wait 20 ms, open the relay at zero current. Turn ON: close the relay, wait 50 ms, then unmute softly.", 0.9)], CTL)
box(102, 50, 198, 74, [L("耐久性・音質の理由", 1.2, True), L("信号は 接点 (金/ルテニウム) だけを通る → 接触抵抗が小さく安定、経年で増えにくい", 1.0), L("電流ゼロで開閉 → 接点が焼けない。ラッチング → 通電中の発熱・ハムなし", 1.0), L("Only gold / ruthenium relay contacts carry the signal; switching at zero current avoids arcing.", 0.95)], PWR)
box(2, 8, 98, 44, [L("スイッチの種類の比較 (計算)", 1.2, True), L("信号を通す安価なトグル: 寿命 約 5 万回、接触抵抗 30〜100mΩ (経年で増加)", 1.0), L("本設計の密閉リレー: 寿命 約 1000 万回 (ゼロ電流開閉)、接触抵抗 約 5mΩ", 1.0), L("ユーザーの押しボタン: ホール素子で 約 1 億回以上、摩耗する接点なし", 1.0)], ANA)
box(102, 8, 198, 44, [L("安全", 1.2, True), L("DC 検出・過電流・過熱で K1 を強制 OFF (スイッチより優先)", 1.0), L("電源投入時は K1・K9 とも OFF から始め、遅延して ON", 1.0), L("State is remembered, but a fault forces the speaker relay OFF.", 0.95)], CTL)
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_sw.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300)); print(out)
