import io, contextlib, math
_ns = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\sim.py", encoding="utf-8").read().replace('with open("sim_results.json"', 'with open("sim_results_tmp.json"'), _ns)
sk, lc, db, logspace = _ns["sk"], _ns["lc"], _ns["db"], _ns["logspace"]

text(3, 127, "シミュレーション (TEST / DEBUG) の結果  Simulation (test and debug) results", 2.4, INK, "la", True)
text(3, 123.6, "Python による計算 (交流応答・直流動作点・真空管モデル・設計計算)。実機測定ではありません。過渡応答・歪み・安定性の SPICE 解析は未実施。", 1.45, GRY)
text(3, 121.2, "Calculated in Python (AC response, DC operating points, tube model, design arithmetic). Not bench measurements. Transient / THD / stability SPICE runs were not done.", 1.2, GRY)


def plot(x0, y0, x1, y1, xmin, xmax, ymin, ymax, logx, title, xlabel, ylabel):
    d.rectangle([*P(x0, y1), *P(x1, y0)], outline=(150, 160, 190), width=int(LW * .7), fill=(252, 252, 252))
    text(x0, y1 + 2.2, title, 1.3, INK, "la", True)

    def mx(v):
        t = (math.log10(v) - math.log10(xmin)) / (math.log10(xmax) - math.log10(xmin)) if logx else (v - xmin) / (xmax - xmin)
        return x0 + t * (x1 - x0)

    def my(v):
        return y0 + (v - ymin) / (ymax - ymin) * (y1 - y0)
    # grid
    yv = ymin
    step = (ymax - ymin) / 6
    for k in range(7):
        v = ymin + k * step
        line([(x0, my(v)), (x1, my(v))], (225, 225, 230), int(LW * .5))
        text(x0 - 0.6, my(v), "%g" % round(v, 1), 0.95, GRY, "rm")
    if logx:
        e = math.floor(math.log10(xmin))
        while 10 ** e <= xmax:
            if 10 ** e >= xmin:
                line([(mx(10 ** e), y0), (mx(10 ** e), y1)], (225, 225, 230), int(LW * .5))
                lab = ("%gk" % (10 ** e / 1e3)) if 10 ** e >= 1e3 else ("%g" % 10 ** e)
                text(mx(10 ** e), y0 - 1.5, lab, 0.95, GRY, "mm")
            e += 1
    text((x0 + x1) / 2, y0 - 3.6, xlabel, 1.0, GRY, "mm")
    text(x0 - 0.6, y1 + 0.6, ylabel, 0.95, GRY, "rb")
    return mx, my


def curve(mx, my, pts, col, dashed=False, w=None):
    seg = []
    for i, (x, y) in enumerate(pts):
        seg.append((mx(x), my(y)))
    if dashed:
        for i in range(0, len(seg) - 1, 2):
            line([seg[i], seg[i + 1]], col, w or int(LW * .9))
    else:
        line(seg, col, w or LW)


def legend(x, y, items):
    for i, (t, col, dashed) in enumerate(items):
        yy = y - i * 2.0
        line([(x, yy), (x + 4, yy)], col, int(LW * .9))
        text(x + 5, yy, t, 0.95, INK, "lm")


# ---- panel 1: Sallen-Key
mx, my = plot(8, 70, 62, 108, 10, 1000, -30, 3, True, "① サブウーファー LPF (2次バターワース)  Sub-woofer LPF", "Hz", "dB")
fs = logspace(10, 1000, 160)
cols = {"80Hz": (30, 70, 180), "100Hz": (25, 115, 60), "120Hz": (190, 30, 30)}
for name, c1, c2 in (("80Hz", 270e-9, 150e-9), ("100Hz", 220e-9, 110e-9), ("120Hz", 180e-9, 100e-9)):
    Hf, f0, q = sk(10e3, 10e3, c1, c2)
    curve(mx, my, [(f, max(-30, db(Hf(f)))) for f in fs], cols[name], dashed=True)
for name, rr in (("80Hz", 12.7e3), ("100Hz", 10.2e3), ("120Hz", 8.45e3)):
    Hf, f0, q = sk(rr, rr, 220e-9, 110e-9)
    curve(mx, my, [(f, max(-30, db(Hf(f)))) for f in fs], cols[name])
legend(36, 105, [("修正後 (実線) / after", INK, False), ("修正前 (破線) / before", INK, True)])

# ---- panel 2: Class D
mx, my = plot(70, 70, 124, 108, 1e3, 1e6, -50, 10, True, "② Class D 出力フィルタ (BTL 8Ω, 片側 4Ω)  Class D output filter", "Hz", "dB")
fs = logspace(1e3, 1e6, 200)
Ho = lc(10e-6, 1e-6, 4); Hn = lc(22e-6, 0.47e-6, 4)
curve(mx, my, [(f, max(-50, db(Ho(f)))) for f in fs], (190, 30, 30), dashed=True)
curve(mx, my, [(f, max(-50, db(Hn(f)))) for f in fs], (25, 115, 60))
legend(95, 105, [("22µH/0.47µF (修正後)", (25, 115, 60), False), ("10µH/1µF (修正前)", (190, 30, 30), True)])

# ---- panel 3: Class A idle current
mx, my = plot(132, 70, 192, 108, 3.0, 5.5, 0, 4.5, False, "③ Class A アイドル電流  Class A idle current", "Vgs (V)", "A")
pts = [(v, max(0.0, (5.6 - v) / 0.62)) for v in [3.0 + 0.05 * k for k in range(51)]]
curve(mx, my, pts, (190, 30, 30), dashed=True)
curve(mx, my, [(3.0, 2.306), (5.5, 2.306)], (25, 115, 60))
legend(150, 105, [("電流サーボ (修正後) 2.31A", (25, 115, 60), False), ("ツェナー固定 (修正前)", (190, 30, 30), True)])

# ---- result table
rows = [
 ("① LPF: -3dB が 74.7 / 100 / 112 Hz → 抵抗切替で 80.6 / 100.3 / 121.2 Hz (Q = 0.707)",
  "① LPF: the -3 dB points were 74.7 / 100 / 112 Hz; resistor switching now gives 80.6 / 100.3 / 121.2 Hz (Q = 0.707)."),
 ("② Class D: 10µH/1µF は BTL 8Ω で +2.8dB のピーク (Q 1.27) → 22µH/0.47µF で Q 0.58・20kHz −0.7dB。4Ω は −4.2dB (帰還が補正)",
  "② Class D: 10 µH / 1 µF peaked +2.8 dB at BTL 8 ohm; 22 µH / 0.47 µF gives Q 0.58 and -0.7 dB at 20 kHz (4 ohm: -4.2 dB, corrected by feedback)."),
 ("③ Class A: ツェナー固定は Vgs 3〜5.5V で 0.2〜4.2A とばらつく → 電流サーボ (Vset ÷ R7) で 2.31A (R7 ±1% で 2.28A)",
  "③ Class A: a fixed zener bias swung from 0.2 to 4.2 A over Vgs 3-5.5 V; a current servo (Vset / R7) holds 2.31 A (2.28 A with R7 +1%)."),
 ("④ 真空管: 12AX7 は利得 56倍 (35dB) で高すぎ → 12AU7 の片側 (利得 10.9倍 = 20.7dB、入力 3.9Vrms まで余裕)。V2 カソードフォロワの出力 ≈ 1.44kΩ",
  "④ Tube: the 12AX7 stage had 56x (35 dB) gain, too high; a 12AU7 half now gives 10.9x (20.7 dB) with room for 3.9 Vrms input. V2 output impedance is about 1.44 kohm."),
 ("⑤ 外付け電源: 二次 2×18V/2×32V/2×42V では整流後電圧が足りない (±45V 用は最低 38.6V < 48V) → 2×24V / 2×40V / 2×52V (最低 28.4 / 48.8 / 64.0V)",
  "⑤ External supply: the old secondaries (2x18 / 2x32 / 2x42 V) left too little raw voltage (38.6 V minimum for +-45 V, below 48 V); now 2x24 / 2x40 / 2x52 V (28.4 / 48.8 / 64.0 V minimum)."),
 ("問題なし: 加算 (L=R) −0.02dB、I/V LPF 141kHz (バランス) / 133kHz、Class AB バイアス比 R1/R2 = 3、LTP+VAS 帰還帯域 ≈ 0.83MHz (利得 23)。",
  "No problem found: mono sum -0.02 dB, I/V low-pass 141 kHz (balanced) / 133 kHz, Class AB bias ratio R1/R2 = 3, LTP + VAS loop bandwidth about 0.83 MHz (gain 23)."),
 ("未実施: 過渡応答・歪み (THD)・位相余裕 (Class AB / D)・デッドタイム・熱。実機または SPICE での確認が必要です。",
  "Not done: transient response, THD, phase margin (Class AB / D), dead time and thermal checks. Bench or SPICE verification is still required."),
]
y = 60
text(6, 63.5, "見つかった問題と修正 / 確認結果  Problems found, fixes and checks", 1.6, INK, "la", True)
for ja, en in rows:
    text(6, y, ja, 1.15, INK, "la")
    text(6, y - 2.0, en, 1.05, GRY, "la")
    y -= 5.6

img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_test.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
