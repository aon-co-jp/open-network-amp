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
text(3, 127, "ゲイン調整 (1dB 刻み・3 モード: ANALOG / DIGITAL / ANALOG+DIGITAL)  Gain control in 1 dB steps, three modes", 2.3, INK, "la", True)
text(3, 123.6, "スピーカー出力用とヘッドホン出力用に 2 個 (各々が独立: 前面ノブ 2 個・モード切替 2 個・触覚ハイブリッド VER6 で 1 クリック = 1dB)。 Two independent controls: one for the speaker output and one for the headphone output.", 1.3, GRY)
text(3, 121.2, "参考設計 Reference design. Python の計算 (SPICE・実機測定ではありません)。 Python calculations, not bench measurements.", 1.2, GRY)
def chain(y0, tag, col_out):
    box(2, y0, 24, y0 + 16, [L("信号入力", 1.1, True), L("DAC / アナログ", 0.9)], ANA)
    arrow([(24, y0 + 8), (30, y0 + 8)], ANA)
    box(30, y0, 84, y0 + 16, [L("① アナログゲイン (ANALOG / A+D)", 1.0, True), L("粗 6dB: リレー 2 個 (6/12dB) → 0/6/12/18dB", 0.85), L("微 1dB: リレー 3 個 (1/2/2dB) → 0〜5dB (ANALOG のみ)", 0.85)], ANA)
    arrow([(84, y0 + 8), (90, y0 + 8)], ANA)
    box(90, y0, 132, y0 + 16, [L("② デジタルゲイン (DIGITAL / A+D)", 1.0, True), L("FPGA 32bit 1dB 刻み (A+D は微調整 0〜5dB)", 0.85), L("クロスフェードで変更", 0.85)], DIG)
    arrow([(132, y0 + 8), (138, y0 + 8)], DIG)
    box(138, y0, 164, y0 + 16, [L(tag, 1.0, True), L("専用ノブ + SW7 (3 モード)", 0.85), L("前面", 0.85)], CTL)
    arrow([(164, y0 + 8), (170, y0 + 8)], CTL)
    box(170, y0, 198, y0 + 16, [L("出力", 1.0, True), L(col_out, 0.85), L("ON/OFF スイッチ", 0.85)], ANA)
chain(98, "スピーカー用ゲイン", "スピーカー端子")
chain(78, "ヘッドホン用ゲイン", "ヘッドホン端子 (3.5/4.4/6.35/XLR)")
box(2, 50, 70, 72, [L("モード切替 SW7 (3 ポジション)", 1.2, True), L("ANALOG: アナログだけで 1dB 刻み (ビットパーフェクトを保つ)", 1.0), L("DIGITAL: デジタルだけで 1dB 刻み (リレーは動かない)", 1.0), L("ANALOG+DIGITAL: アナログ 6dB 粗調整 + デジタル 1dB 微調整", 1.0), L("(リレーの動作回数が少なく、ビット損失も少ない)", 0.95)], CTL)
box(76, 50, 198, 72, [L("切替の順序 (ポップ音・ゲインの飛びを防ぐ)", 1.2, True), L("リレーを動かす変更 (粗調整の境目など) は: ミュート 3ms → リレー → 5ms 待つ → ミュート解除。デジタルだけの変更はミュート不要 (クロスフェード)。", 1.0), L("Relay changes (e.g. at the coarse boundaries): mute 3 ms, switch the relay(s), wait 5 ms, unmute. Digital-only changes need no mute (crossfade).", 0.95), L("多数のリレーが同時に動く境目 (最大 5 個) があるため、メイク・ビフォア・ブレイクの順で動かす", 1.0)], PWR)
box(2, 6, 98, 44, [L("3 モードの使い分け", 1.25, True), L("ANALOG: ビットパーフェクトを重視。リレー動作は多め (ゼロ電流・ミュートで寿命は十分)", 1.0), L("DIGITAL: リレーを使わない・可動部なし。32bit のうち最大 3bit を使うが 29bit 残る", 1.0), L("ANALOG+DIGITAL: リレー寿命が長く、ビット損失も 最大 0.83bit。通常はこれを推奨", 1.0), L("All three act on the speakers and the headphones; 1 dB per haptic click.", 0.95)], ANA)
box(102, 6, 198, 44, [L("1dB 刻みの精度 (95% の組)", 1.25, True), L("0.1% 抵抗: 微調整のずれ 約 0.02dB (チャンネル間 0.1dB 以内)", 1.0), L("1% 抵抗なら 約 0.2dB → 0.1% 薄膜 を採用", 1.0), L("デジタルの 1dB 刻みは誤差ゼロ (計算上)", 1.0), L("Matched 0.1% thin-film resistors keep the fine steps within about 0.02 dB.", 0.95)], PWR)
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_gain3.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300)); print(out)
