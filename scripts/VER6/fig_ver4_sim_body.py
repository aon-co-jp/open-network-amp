import math
exec(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\plot_helpers.py", encoding="utf-8").read())
logspace = lambda a, b, n: [a * (b / a) ** (i / (n - 1)) for i in range(n)]
GR, BL, RD, PU = (25, 115, 60), (30, 70, 180), (190, 30, 30), (120, 60, 160)
text(3, 127, "ヘッドホンアンプ VER4 の仮想シミュレーション  Headphone amplifier VER4 - simulation", 2.4, INK, "la", True)
text(3, 123.6, "Python による計算 (交流応答・設計計算)。実機測定ではありません。過渡応答・歪み (THD)・実機の雑音の SPICE 解析は未実施です。", 1.45, GRY)
text(3, 121.2, "Calculated in Python (AC response and design arithmetic). Not bench measurements. Transient, THD and real noise SPICE runs were not done.", 1.2, GRY)

# ---- 1) output impedance vs frequency response of a dynamic headphone
def zhp(f):
    f0, q = 70.0, 3.0
    return 32 + 70 / (1 + (q * (f / f0 - f0 / f)) ** 2)


fs = logspace(20, 20000, 200)
mx, my = plot(8, 70, 62, 108, 20, 20000, -3, 0.2, True, "① 出力インピーダンスと周波数特性のずれ (32Ω ダイナミック型)  Response error", "Hz", "dB")
for zo, col in ((0.1, GR), (1.0, BL), (10.0, RD)):
    curve(mx, my, [(f, 20 * math.log10(zhp(f) / (zhp(f) + zo))) for f in fs], col)
legend(26, 105, [("出力 0.1Ω (VER4: 帰還後 ≈ 0.1Ω): ±0.02dB", GR, False), ("1Ω: ±0.2dB", BL, False), ("10Ω (一般的な民生機): ≈ 2dB", RD, False)])
# ---- 2) max output power vs load
mx, my = plot(70, 70, 124, 108, 8, 1000, 0.01, 6, True, "② 最大出力 (±15V・電流 0.5A/脚)  Max power vs load", "load (ohm)", "W")
rl = logspace(8, 1000, 120)


def pbal(r):
    v = min(24.0, 0.5 * r)       # differential peak (each leg 12 V, 0.5 A)
    return 0.5 * v * v / r


def pse(r):
    v = min(12.0, 0.5 * r)
    return 0.5 * v * v / r


curve(mx, my, [(r, min(6, pbal(r))) for r in rl], GR)
curve(mx, my, [(r, min(6, pse(r))) for r in rl], BL)
legend(88, 105, [("4.4mm / 3.5mm バランス (最大 4W @ 32Ω)", GR, False), ("6.35mm / 3.5mm アンバランス", BL, False)])
# ---- 3) noise vs gain
mx, my = plot(132, 70, 192, 108, 0, 18, 0.5, 3.5, False, "③ ゲイン段の雑音 (20Hz〜20kHz)  Output noise vs gain", "analog gain (dB)", "uV rms")
en = 1.1e-9


def noise(gdb):
    g = 10 ** (gdb / 20)
    rg = 1e3 / max(g - 1, 1e-9)
    rf = 1e3
    tot2 = (en * g) ** 2 + (math.sqrt(4 * 1.38e-23 * 300 * rf) * 1) ** 2 + (math.sqrt(4 * 1.38e-23 * 300 * (rf * rg / (rf + rg))) * g) ** 2
    return math.sqrt(tot2 * 19980) * 1e6


curve(mx, my, [(g, noise(g)) for g in [0.5 + 0.5 * k for k in range(36)]], PU)
for g in (6, 12, 18):
    text(mx(g), my(noise(g)) + 1.6, "+%ddB: %.2fµV" % (g, noise(g)), 1.0, PU, "mm", True)

rows = [
    ("① 出力インピーダンス: 32Ω の動的ヘッドホン (70Hz 付近で 100Ω に上がる) で、出力 10Ω だと周波数特性が約 2dB ずれる → VER4 は帰還後の出力 ≈ 0.1Ω で ±0.02dB",
     "① Output impedance: a 32 ohm dynamic headphone whose impedance rises to 100 ohm near 70 Hz shifts its response by about 2 dB with a 10 ohm source; VER4 (about 0.1 ohm after feedback) keeps it within 0.02 dB."),
    ("② 最大出力: バランス (4.4mm) は 32Ω で 4W、300Ω で 0.96W、600Ω で 0.48W。アンバランス (6.35mm) は 32Ω で 2.3W (±15V・0.5A/脚の計算)。IEM でも高能率ヘッドホンでも余裕",
     "② Maximum power: balanced (4.4 mm) gives 4 W at 32 ohm, 0.96 W at 300 ohm and 0.48 W at 600 ohm; unbalanced (6.35 mm) gives 2.3 W at 32 ohm (+-15 V, 0.5 A per leg). Plenty for IEMs and efficient headphones."),
    ("③ アナログゲイン (0 / +6 / +12 / +18dB、リレー切替): 雑音は +18dB でも約 3µV (計算)。120dB/V の IEM でも SPL に換算して約 10dB 未満で聞こえない",
     "③ Analog gain (0 / +6 / +12 / +18 dB by relay): noise stays at about 3 uV even at +18 dB (calculated), below about 10 dB SPL on a 120 dB/V IEM, so it is inaudible."),
    ("④ 2種類のゲイン調整: ANALOG = ゲイン段・アッテネータ (ビットパーフェクト維持) / DIGITAL = FPGA のデジタルゲイン (−40dB で 24bit が 17.4bit)。どちらもスピーカーとヘッドホンに同時に効く (SW7)",
     "④ Two gain modes: ANALOG = gain stage and attenuator (bit-perfect kept) / DIGITAL = digital gain in the FPGA (-40 dB turns 24 bit into 17.4 bit). Both affect the speakers and the headphones at the same time (SW7)."),
    ("⑤ ヘッドホンアンプの入力は 47kΩ でバスへの負荷は -0.01dB 以下。スピーカーを同時に鳴らせる (自動ミュートは SW8 で ON / OFF)。未実施: 過渡応答・歪み・実機の雑音",
     "⑤ The headphone amp loads the bus with 47 kohm (-0.01 dB or less) and the speakers can play at the same time (auto-mute is switchable with SW8). Not done: transient response, distortion and real noise."),
]
y = 60
text(6, 63.5, "VER4 ヘッドホンアンプの確認結果  VER4 headphone amplifier checks", 1.6, INK, "la", True)
for ja, en_ in rows:
    text(6, y, ja, 1.15, INK, "la")
    text(6, y - 2.0, en_, 1.05, GRY, "la")
    y -= 5.6
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_ver4_sim.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
