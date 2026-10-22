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
text(3, 127, "ゲインと音量の調整 (1dB 刻み・3 モード) — スピーカー出力とヘッドホン出力の両方で  Gain and volume in 1 dB steps, three modes, on both outputs", 2.2, INK, "la", True)
text(3, 123.6, "各出力に ゲイン (上げる 0〜+18dB) と 音量 (下げる 0〜−90dB) の 2 つ、合計 4 個の調整。各々に前面ノブと ANALOG / DIGITAL / ANALOG+DIGITAL のモード切替。", 1.3, GRY)
text(3, 121.2, "Each output has a gain control (0 to +18 dB) and a volume control (0 to -90 dB): four controls, each with its own knob and mode switch. Python calculations, not bench measurements.", 1.1, GRY)
def chain(y0, tag, rng, coarse, out):
    box(2, y0, 22, y0 + 12, [L(tag, 1.05, True), L(rng, 0.9)], CTL)
    arrow([(22, y0 + 6), (28, y0 + 6)], CTL)
    box(28, y0, 92, y0 + 12, [L("① アナログ (ANALOG / A+D)", 1.0, True), L(coarse, 0.85), L("微 1dB: リレー 3 個 (1/2/2dB) → 0〜5dB (ANALOG のみ)", 0.85)], ANA)
    arrow([(92, y0 + 6), (98, y0 + 6)], ANA)
    box(98, y0, 150, y0 + 12, [L("② デジタル (DIGITAL / A+D)", 1.0, True), L("FPGA 32bit 1dB 刻み (A+D は微調整 0〜5dB)", 0.85), L("変更はクロスフェード", 0.85)], DIG)
    arrow([(150, y0 + 6), (156, y0 + 6)], DIG)
    box(156, y0, 198, y0 + 12, [L(out, 1.0, True), L("専用ノブ + モード切替", 0.85), L("(ON/OFF スイッチ別)", 0.85)], ANA)
chain(102, "スピーカー ゲイン", "0〜+18 dB", "粗 6dB: リレー 2 個 (6/12dB) → 0/6/12/18dB", "スピーカー端子")
chain(88, "スピーカー 音量", "0〜−90 dB", "粗 6dB: リレー 4 個 (6/12/24/48dB) → 0〜−90dB", "スピーカー端子")
chain(74, "ヘッドホン ゲイン", "0〜+18 dB", "粗 6dB: リレー 2 個 (6/12dB) → 0/6/12/18dB", "ヘッドホン端子")
chain(60, "ヘッドホン 音量", "0〜−90 dB", "粗 6dB: リレー 4 個 (6/12/24/48dB) → 0〜−90dB", "ヘッドホン端子")
box(2, 30, 98, 54, [L("3 モード (ゲイン・音量とも共通)", 1.2, True), L("ANALOG: アナログだけで 1dB 刻み。ビットパーフェクト。リレー動作は多め", 0.95), L("DIGITAL: FPGA の 32bit だけ。リレーなし。音量では深く絞るほどビット深度が減る", 0.95), L("ANALOG+DIGITAL: アナログ 6dB 粗調整 + デジタル 1dB 微調整 (通常はこれを推奨)", 0.95)], CTL)
box(102, 30, 198, 54, [L("切替の順序 (ポップ音・飛びを防ぐ)", 1.2, True), L("リレーが動く変更: ミュート 3ms → メイク・ビフォア・ブレイクで切替 → 5ms 待つ → 解除", 0.95), L("デジタルだけの変更はミュート不要 (クロスフェード)。境目で最大 7 個のリレーが同時に動く", 0.95)], PWR)
box(2, 6, 98, 26, [L("音量のビット深度 (DIGITAL は深く絞ると減る)", 1.15, True), L("−40dB で 25.4bit、−60dB で 22bit (24bit 音源に不足)、−90dB で 17bit", 0.95), L("ANALOG+DIGITAL なら 31.2bit 以上を常に保つ → 音量は ANALOG+DIGITAL を推奨", 0.95)], ANA)
box(102, 6, 198, 26, [L("1dB 刻みの精度とリレー寿命", 1.15, True), L("0.1% 薄膜抵抗: 微調整のずれ 約 0.02dB。リレー寿命 (1 日 1000 ステップ)", 0.95), L("ANALOG 約 14 年 / ANALOG+DIGITAL 約 95 年 (音量)", 0.95)], PWR)
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_gain3.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300)); print(out)
