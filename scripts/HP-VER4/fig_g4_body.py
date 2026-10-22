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
text(3, 127, "音量 と ゲイン (低い音・高い音の 2 種) の調整 — 各 1dB 刻み・3 モード・スピーカー出力とヘッドホン出力の両方  Volume and two gains (low and high) on both outputs", 2.0, INK, "la", True)
text(3, 123.6, "各出力に 音量 (0〜−90dB)・低音ゲイン (100Hz 以下のシェルビング ±10dB)・高音ゲイン (8kHz 以上のシェルビング ±10dB) の 3 個、合計 6 個。各々に前面ノブと ANALOG / DIGITAL / ANALOG+DIGITAL の切替。", 1.25, GRY)
text(3, 121.2, "Each output has a volume (0 to -90 dB), a low-frequency gain (shelf below 100 Hz, +-10 dB) and a high-frequency gain (shelf above 8 kHz, +-10 dB): six controls. Python calculations, not bench measurements.", 1.1, GRY)
def chain(y0, tag, rng, analog, digital, out):
    h = 9.5
    box(2, y0, 26, y0 + h, [L(tag, 1.0, True), L(rng, 0.85)], CTL)
    arrow([(26, y0 + h / 2), (30, y0 + h / 2)], CTL)
    box(30, y0, 92, y0 + h, [L("① アナログ (ANALOG / A+D)", 0.95, True), L(analog, 0.8)], ANA)
    arrow([(92, y0 + h / 2), (96, y0 + h / 2)], ANA)
    box(96, y0, 150, y0 + h, [L("② デジタル (DIGITAL / A+D)", 0.95, True), L(digital, 0.8)], DIG)
    arrow([(150, y0 + h / 2), (154, y0 + h / 2)], DIG)
    box(154, y0, 198, y0 + h, [L(out, 0.95, True), L("専用ノブ + モード切替 (ON/OFF 別)", 0.8)], ANA)
VOLA = "粗 6dB: リレー 4 個 (6/12/24/48dB) + 微 1dB: リレー 3 個 (1/2/2dB)"
VOLD = "FPGA 32bit 1dB 刻み (A+D は微調整 0〜5dB)"
SHA = "反転/非反転の符号リレー + 粗 6dB 1 個 + 微 1dB 3 個 (1/2/2dB) (抵抗 0.1% 薄膜)"
SHD = "FPGA のシェルビング・バイクアッド (係数 32bit 以上・倍精度) 1dB 刻み"
for k, (nm, ty) in enumerate((("スピーカー", "スピーカー端子"), ("ヘッドホン", "ヘッドホン端子"))):
    base = 108 - k * 30.5
    chain(base, nm + " 音量", "0〜−90 dB", VOLA, VOLD, ty)
    chain(base - 10, nm + " 低音ゲイン", "100Hz 以下 ±10dB", SHA, SHD, ty)
    chain(base - 20, nm + " 高音ゲイン", "8kHz 以上 ±10dB", SHA, SHD, ty)
box(2, 25, 98, 44, [L("3 モード (音量・低音ゲイン・高音ゲインとも共通)", 1.15, True), L("ANALOG: アナログだけ (リレー + 抵抗)、ビットパーフェクト。DIGITAL: FPGA だけ (リレーなし)", 0.95), L("ANALOG+DIGITAL: アナログ 6dB 粗調整 + デジタル 1dB 微調整 (通常はこれを推奨)", 0.95)], CTL)
box(102, 25, 198, 44, [L("デジタルのシェルビング: 係数の語長が重要", 1.15, True), L("384kHz で 100Hz の低音シェルビングを 24bit 係数にすると、20Hz で −0.67dB ずれる", 0.95), L("→ 32bit 以上 (倍精度) の係数にすると ずれは 0.004dB 以下", 0.95)], DIG)
box(2, 4, 98, 21, [L("切替の順序 (ポップ音を防ぐ)", 1.15, True), L("リレーが動く変更: ミュート 3ms → メイク・ビフォア・ブレイク → 5ms 待つ → 解除", 0.95), L("デジタルだけの変更は ミュート不要 (係数をクロスフェード)", 0.95)], PWR)
box(102, 4, 198, 21, [L("リレー寿命 (1 日 1000 ステップ)", 1.15, True), L("ゲイン (±10dB): ANALOG 約 16 年 / ANALOG+DIGITAL 約 180 年", 0.95), L("音量: ANALOG 約 14 年 / ANALOG+DIGITAL 約 95 年", 0.95)], PWR)
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_gain4.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300)); print(out)
