import math, json, io, contextlib
_ns = {}
with contextlib.redirect_stdout(io.StringIO()):
    exec(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\sim5.py", encoding="utf-8").read().replace('open("sim5_results.json", "w", encoding="utf-8")', 'open("sim5_tmp.json", "w", encoding="utf-8")'), _ns)
summer, sk_noise, hpf_noise, nb = _ns["summer"], _ns["sk_noise"], _ns["hpf_noise"], _ns["nb"]
v4 = math.sqrt(summer(4.99e3, 2.49e3) ** 2 + 2 * sk_noise(12.7e3) ** 2 + hpf_noise(22e3) ** 2) * math.sqrt(nb) * 1e6
v2 = math.sqrt(summer(4.99e3, 2.49e3) ** 2 + 2 * sk_noise(6.34e3) ** 2 + hpf_noise(10e3) ** 2) * math.sqrt(nb) * 1e6
v3 = math.sqrt(summer(2.49e3, 1.24e3) ** 2 + 2 * sk_noise(6.34e3) ** 2 + hpf_noise(10e3) ** 2) * math.sqrt(nb) * 1e6
v5 = math.sqrt(summer(3.32e3, 1.65e3) ** 2 + 2 * sk_noise(6.34e3) ** 2 + hpf_noise(10e3) ** 2) * math.sqrt(nb) * 1e6
ld5 = 20 * math.log10(3.32e3 / (3.32e3 + 47))
ld3 = 20 * math.log10(2.49e3 / (2.49e3 + 47))
text(3, 127, "VER5 の仮想シミュレーション (TEST / DEBUG を 3 回)  VER5 simulation - three test and debug rounds", 2.4, INK, "la", True)
text(3, 123.6, "Python による計算 (雑音・設計計算)。実機測定ではありません。過渡応答・歪み (THD) の SPICE 解析は未実施です。", 1.45, GRY)
text(3, 121.2, "Calculated in Python (noise and design arithmetic). Not bench measurements. Transient and THD SPICE runs were not done.", 1.2, GRY)
GR, BL, RD, PU = (25, 115, 60), (30, 70, 180), (190, 30, 30), (120, 60, 160)


def bars(x0, y0, x1, y1, title, items, unit, vmax):
    d.rectangle([*P(x0, y1), *P(x1, y0)], outline=(150, 160, 190), width=int(LW * .7), fill=(252, 252, 252))
    text(x0, y1 + 2.2, title, 1.3, INK, "la", True)
    n = len(items)
    w = (x1 - x0) / n
    for i, (lab, val, col) in enumerate(items):
        h = (y1 - y0 - 6) * val / vmax
        xa = x0 + i * w + w * 0.18
        xb = x0 + (i + 1) * w - w * 0.18
        d.rectangle([*P(xa, y0 + h), *P(xb, y0)], fill=col)
        text((xa + xb) / 2, y0 + h + 1.4, "%.3g %s" % (val, unit), 1.0, INK, "mm", True)
        text((xa + xb) / 2, y0 - 1.8, lab, 0.95, GRY, "mm")


bars(8, 70, 96, 108, "① サブウーファー回路の雑音 (7〜120Hz)  Subwoofer circuit noise", [("VER4", v4, RD), ("回目1 R半減", v2, (200, 130, 40)), ("回目2 2.49k", v3, BL), ("VER5 3.32k", v5, GR)], "µV", 0.5)
bars(108, 70, 192, 108, "② 配線長 (1ch の信号経路)  Signal path length", [("VER2", 95, RD), ("VER5 (設計目標)", 60, GR)], "mm", 110)
rows = [
    ("TEST 1 (VER4 の確認): 雑音 %.2f µV。支配項は SK 段の R (12.7k) と HPF の R (22k)。LR4 の 2 段目で雑音が √2 倍になる → 問題あり。対策: SK を C1 440n / C2 220n・R 6.34k にし、HPF を 10k + 2.2µF に。" % v4,
     "TEST 1 (VER4): noise %.2f uV; the dominant terms are the SK resistors (12.7k) and the HPF resistor (22k), and the LR4 second stage adds a factor of root 2. Fix: SK with C1 440n / C2 220n and R 6.34k, HPF 10k + 2.2 uF." % v4),
    ("TEST 2: 雑音 %.2f µV (-%.1f dB)。さらに加算段を 2.49k / 1.24k にすると %.2f µV だが、プリアウト (約 47Ω) への負荷が %.2f dB → やや大きい。対策: 加算段を 3.32k / 1.65k に。" % (v2, 20 * math.log10(v4 / v2), v3, ld3),
     "TEST 2: noise %.2f uV (-%.1f dB); a 2.49k / 1.24k summer gives %.2f uV but loads the 47 ohm pre-out by %.2f dB, slightly too much. Fix: a 3.32k / 1.65k summer." % (v2, 20 * math.log10(v4 / v2), v3, ld3)),
    ("TEST 3 (VER5): 雑音 %.2f µV (VER4 から -%.1f dB)、プリアウトへの負荷 %.2f dB。LPF は 80.7 / 100.0 / 121.3 Hz (Q = 0.707)、HPF は 7.2 Hz。" % (v5, 20 * math.log10(v4 / v5), ld5),
     "TEST 3 (VER5): noise %.2f uV (-%.1f dB from VER4), pre-out load %.2f dB; LPF at 80.7 / 100.0 / 121.3 Hz (Q = 0.707) and HPF at 7.2 Hz." % (v5, 20 * math.log10(v4 / v5), ld5)),
    ("ボリューム VER2: リレー式ラダーの出力 Z は最大 2.5kΩ、熱雑音は -121dBV (-6dB 時)、0.1% 抵抗で誤差 ±0.009dB、リレー 1000 万回 = 500 回/日で約 55 年。",
     "Volume VER2: the relay ladder output impedance is at most 2.5 kohm, the thermal noise is -121 dBV (at -6 dB) and the error with 0.1% resistors is +-0.009 dB; 10 million relay operations last about 55 years at 500 operations per day."),
    ("配線: 信号経路 95mm → 60mm (設計目標。DAC → I/V → ボリューム+バッファ → パワーアンプ → リレー → 端子)。拾う雑音の目安 -4.0 dB。サブウーファー基板とヘッドホン基板も端子の近くに置く。",
     "Wiring: the signal path goes from 95 mm to 60 mm (a design target: DAC, I/V, volume + buffer, power amplifier, relay, terminals), about -4.0 dB of pickup; the subwoofer and headphone boards also sit next to their jacks."),
    ("未実施: 過渡応答・歪み (THD)・実機の雑音と位相・触覚の感触。実機または SPICE での確認が必要です。",
     "Not done: transient response, THD, real noise and phase, and the haptic feel. Bench or SPICE verification is still required."),
]
y = 60
text(6, 63.5, "TEST / DEBUG の記録  Test and debug log", 1.6, INK, "la", True)
for ja, en in rows:
    text(6, y, ja, 1.1, INK, "la")
    text(6, y - 2.0, en, 1.0, GRY, "la")
    y -= 5.2
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_ver5_sim.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size, round(v4, 3), round(v2, 3), round(v3, 3), round(v5, 3))
