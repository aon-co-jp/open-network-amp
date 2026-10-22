import io, contextlib, math
_ns = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\sim.py", encoding="utf-8").read().replace('with open("sim_results.json"', 'with open("sim_results_tmp.json"'), _ns)
sk, lc, db, logspace = _ns["sk"], _ns["lc"], _ns["db"], _ns["logspace"]
text(3, 127, "サブウーファー出力 VER2 のシミュレーション結果  Subwoofer output VER2 - simulation results", 2.4, INK, "la", True)
text(3, 123.6, "Python による計算 (交流応答・設計計算)。実機測定ではありません。過渡応答・歪み (THD)・ノイズの SPICE 解析は未実施。", 1.45, GRY)
text(3, 121.2, "Calculated in Python (AC response and design arithmetic). Not bench measurements. Transient, THD and noise SPICE runs were not done.", 1.2, GRY)


def plot(x0, y0, x1, y1, xmin, xmax, ymin, ymax, logx, title, xlabel, ylabel):
    d.rectangle([*P(x0, y1), *P(x1, y0)], outline=(150, 160, 190), width=int(LW * .7), fill=(252, 252, 252))
    text(x0, y1 + 2.2, title, 1.3, INK, "la", True)

    def mx(v):
        t = (math.log10(v) - math.log10(xmin)) / (math.log10(xmax) - math.log10(xmin)) if logx else (v - xmin) / (xmax - xmin)
        return x0 + t * (x1 - x0)

    def my(v):
        return y0 + (v - ymin) / (ymax - ymin) * (y1 - y0)
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
                text(mx(10 ** e), y0 - 1.5, "%g" % (10 ** e), 0.95, GRY, "mm")
            e += 1
    text((x0 + x1) / 2, y0 - 3.6, xlabel, 1.0, GRY, "mm")
    text(x0 - 0.6, y1 + 0.6, ylabel, 0.95, GRY, "rb")
    return mx, my


def curve(mx, my, pts, col, dashed=False, w=None):
    seg = [(mx(x), my(y)) for (x, y) in pts]
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


hp = lambda f: (2j * math.pi * f * 22e3 * 1e-6) / (1 + 2j * math.pi * f * 22e3 * 1e-6)
cols = {"80Hz": (30, 70, 180), "100Hz": (25, 115, 60), "120Hz": (190, 30, 30)}
mx, my = plot(8, 70, 96, 108, 3, 300, -24, 3, True, "① 全体の周波数応答 (加算 → LPF → HPF)  Overall response", "Hz", "dB")
fs = logspace(3, 300, 220)
for name, c1, c2 in (("80Hz", 270e-9, 150e-9), ("100Hz", 220e-9, 110e-9), ("120Hz", 180e-9, 100e-9)):
    Hf, f0, q = sk(10e3, 10e3, c1, c2)
    curve(mx, my, [(f, max(-24, db(Hf(f)))) for f in fs], cols[name], dashed=True)
for name, rr in (("80Hz", 12.7e3), ("100Hz", 10.2e3), ("120Hz", 8.45e3)):
    Hf, f0, q = sk(rr, rr, 220e-9, 110e-9)
    curve(mx, my, [(f, max(-24, db(Hf(f) * hp(f)))) for f in fs], cols[name])
legend(52, 105, [("VER2 (実線): 12.7k/10.2k/8.45k + HPF 7Hz", INK, False), ("VER1 (破線): 旧 C 値・HPFなし", INK, True)])
mx, my = plot(108, 70, 192, 108, 2, 60, -12, 2, True, "② 低域の拡大 (サブソニック)  Low-frequency zoom", "Hz", "dB")
fl = logspace(2, 60, 200)
for name, rr in (("80Hz", 12.7e3), ("100Hz", 10.2e3), ("120Hz", 8.45e3)):
    Hf, f0, q = sk(rr, rr, 220e-9, 110e-9)
    curve(mx, my, [(f, max(-12, db(Hf(f) * hp(f)))) for f in fl], cols[name])
Hf, f0, q = sk(10e3, 10e3, 220e-9, 110e-9)
curve(mx, my, [(f, max(-12, db(Hf(f)))) for f in fl], (120, 120, 120), dashed=True)
legend(146, 105, [("VER2: 7Hz で -3dB、5Hz で -4.9dB", INK, False), ("VER1: 低域は平坦 (DC・超低域も通す)", INK, True)])
rows = [
    ("① LPF: VER1 の C 値では -3dB が 74.7 / 102.2 / 112.3 Hz (目標 80 / 100 / 120) → 抵抗切替 (12.7k / 10.2k / 8.45k) で 80.6 / 100.3 / 121.2 Hz",
     "① LPF: with the VER1 capacitor values the -3 dB points were 74.7 / 102.2 / 112.3 Hz (targets 80 / 100 / 120); switching the resistors (12.7k / 10.2k / 8.45k) gives 80.6 / 100.3 / 121.2 Hz."),
    ("② サブソニック: VER1 は DC・超低域も通していた → C 1µF + R 22k の HPF (7.2Hz、1次) を追加。20Hz で -0.55dB、10Hz で -1.8dB、5Hz で -4.9dB (DC を遮断)",
     "② Subsonic: VER1 passed DC and very low frequencies; a 1 uF + 22 kohm high-pass (7.2 Hz, first order) was added: -0.55 dB at 20 Hz, -1.8 dB at 10 Hz, -4.9 dB at 5 Hz, and DC is blocked."),
    ("③ 加算: L=R の低音は 0dB (-0.02dB)。L と R が逆相だと打ち消す。Rf/Cf の極 966kHz、帰還帯域は GBW 制限で ≈ 20MHz。バイアス整合 (2.497kΩ vs Rb 2.49kΩ) でオフセットは無視できる",
     "③ Summer: correlated bass (L=R) is 0 dB (-0.02 dB); anti-phase bass cancels. The Rf/Cf pole is 966 kHz and the loop bandwidth is about 20 MHz (GBW limit). The bias resistor matches (2.497 kohm vs Rb 2.49 kohm), so offset is negligible."),
    ("④ 負荷: 各入力は 10kΩ。プリアウト (出力 ≈ 47Ω) への影響は -0.04dB。出力 47Ω + ケーブル 10nF の極は 339kHz で影響なし",
     "④ Loading: each input is 10 kohm; the effect on a 47 ohm pre-out is -0.04 dB. The 47 ohm plus 10 nF cable pole is at 339 kHz and has no effect."),
    ("未実施: 過渡応答・歪み (THD)・ノイズ・実機の位相。実機または SPICE での確認が必要です。",
     "Not done: transient response, THD, noise and real-hardware phase. Bench or SPICE verification is still required."),
]
y = 60
text(6, 63.5, "見つかった問題と修正 / 確認結果 (VER2)  Problems found, fixes and checks", 1.6, INK, "la", True)
for ja, en in rows:
    text(6, y, ja, 1.15, INK, "la")
    text(6, y - 2.0, en, 1.05, GRY, "la")
    y -= 5.6
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\mono_sub_out_v2_test.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
