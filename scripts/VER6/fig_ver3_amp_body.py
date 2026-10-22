import math, json
exec(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\plot_helpers.py", encoding="utf-8").read())
logspace = lambda a, b, n: [a * (b / a) ** (i / (n - 1)) for i in range(n)]
R3 = json.load(open(r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\sim3_results.json", encoding="utf-8"))
text(3, 127, "音質改善 VER3 の仮想シミュレーション (プリメインアンプ)  VER3 sound-quality simulation (integrated amplifier)", 2.4, INK, "la", True)
text(3, 123.6, "Python による計算 (設計計算)。実機測定ではありません。過渡応答・歪み (THD)・ノイズの SPICE 解析は未実施です。", 1.45, GRY)
text(3, 121.2, "Calculated in Python (design arithmetic). Not bench measurements. Transient, THD and noise SPICE runs were not done.", 1.2, GRY)
GR, BL, RD = (25, 115, 60), (30, 70, 180), (190, 30, 30)

# 1) jitter
mx, my = plot(8, 70, 62, 108, 10, 10000, 110, 180, True, "① クロックジッタの SNR 限界 (20kHz フルスケール)  Jitter SNR limit", "jitter (fs)", "dB")
fs = logspace(10, 10000, 120)
curve(mx, my, [(f, -20 * math.log10(2 * math.pi * 20e3 * f * 1e-15)) for f in fs], GR)
line([(mx(100), 70), (mx(100), 108)], RD, int(LW * .7))
text(mx(100) + 1, 104, "100 fs (目標) → 158 dB", 1.0, RD, "la", True)
# 2) digital volume
mx, my = plot(70, 70, 124, 108, 0, 60, 10, 32, False, "② デジタル減衰で失うビット  Bits lost by digital attenuation", "attenuation (dB)", "bits")
curve(mx, my, [(a, 24 - a / 6.02) for a in range(0, 61)], RD)
curve(mx, my, [(a, 32 - a / 6.02) for a in range(0, 61)], BL)
line([(mx(0), my(24)), (mx(60), my(24))], (160, 160, 160), int(LW * .5))
legend(88, 105, [("32bit から (最大 -60dB で 22bit)", BL, False), ("24bit から (-40dB で 17.4bit)", RD, False)])
text(97, 74.0, "→ VER3: アナログ ATT を使い、デジタルは SW5 でバイパス", 1.0, GR, "mm", True)
# 3) Class AB Cdom
mx, my = plot(132, 70, 192, 108, 20, 110, 0.2, 1.0, False, "③ Class AB: Cdom とループ交差周波数  Cdom vs loop crossover", "Cdom (pF)", "MHz")
pts = [(c, (1 / (2 * (26 + 100))) / (2 * math.pi * c * 1e-12) / 23 / 1e6) for c in range(25, 106, 2)]
curve(mx, my, pts, BL)
for c in (33, 68):
    v = (1 / (2 * (26 + 100))) / (2 * math.pi * c * 1e-12) / 23 / 1e6
    d.ellipse([*[(a) for a in (mx(c) * S - 9, (H - my(v)) * S - 9)], mx(c) * S + 9, (H - my(v)) * S + 9], outline=RD, width=LW) if False else None
    text(mx(c), my(v) + 1.2, "%dpF: %.2f MHz, 余裕 %.0f°" % (c, v, 90 - math.degrees(math.atan(v * 1e6 / 3e6)) - math.degrees(math.atan(v * 1e6 / 6e6))), 1.0, RD, "mm", True)
text(162, 73.5, "VER3: 33pF → 68pF (余裕 66.6° → 78.5°、仮定: 補助極 3/6MHz)", 1.0, GR, "mm", True)

rows = [
    ("① クロック: 目標ジッタ ≤ 100fs で SNR 限界は 158dB。クロックは音質の律速にならない (DAC チップ内部が支配)。XO ×2 + FPGA 再クロック + 外部クロック入力を継続",
     "① Clock: with a 100 fs jitter target the SNR limit is 158 dB, so the clock is not the limiting factor; two XOs, FPGA reclocking and an external clock input are kept."),
    ("② ボリューム: デジタル減衰は -40dB で 24bit が 17.4bit に落ちる → アナログ ATT (電子 / リレー式) を主にし、デジタル Vol/EQ は SW5 でバイパス (ビットパーフェクト)",
     "② Volume: digital attenuation of -40 dB drops 24 bit to 17.4 bit, so the analog attenuator is primary and the digital volume / EQ can be bypassed with SW5 (bit-perfect)."),
    ("③ Class AB: Cdom 33pF → 68pF でループ交差 0.83 → 0.40MHz、位相余裕 66.6° → 78.5° (計算、仮定あり)。ゲイン 23、LTP エミッタ抵抗 100Ω",
     "③ Class AB: Cdom 33 pF -> 68 pF moves the loop crossover from 0.83 to 0.40 MHz and the phase margin from 66.6 to 78.5 deg (calculated, with assumptions); gain 23, 100 ohm LTP emitter resistors."),
    ("④ ボリューム ノブ: クリック感あり / なしを SW6 で切替える触覚ハイブリッド (図7)。クリック 1 回 ≈ 0.11mJ、ピークトルク ≈ 6mN·m、触覚ループ 5kHz (計算)",
     "④ Volume knob: a haptic hybrid with SW6 selecting clicks or smooth (Figure 7): about 0.11 mJ per click, peak torque about 6 mN-m, 5 kHz haptic loop (calculated)."),
    ("⑤ 配線短縮 (VER2) と 外付けリニア電源・電流サーボ・12AU7 の修正 (VER2) は継続。未実施: 過渡応答・歪み・ノイズ・熱、実機の測定",
     "⑤ The shorter wiring (VER2) and the fixes to the external supply, current servo and 12AU7 stage (VER2) are kept. Not done: transient response, distortion, noise, heat and bench measurement."),
]
y = 60
text(6, 63.5, "音質改善 VER3 の要点 / 確認結果  VER3 improvements and checks", 1.6, INK, "la", True)
for ja, en in rows:
    text(6, y, ja, 1.15, INK, "la")
    text(6, y - 2.0, en, 1.05, GRY, "la")
    y -= 5.6

img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad\amp_ver3_sim.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300))
print(out, img.size)
