import math
SDIR = r"C:\Users\noruk\AppData\Local\Temp\claude\F--runo\58accee1-c937-49c6-954f-77e9dc39b2c8\scratchpad"
exec(open(SDIR + r"\plot_helpers.py", encoding="utf-8").read())
c = {}
exec(open(SDIR + r"\g3_calc.py", encoding="utf-8").read().replace('if __name__ == "__main__":', 'if False:'), c)
GR, BL, RD, PU, OR = (25, 115, 60), (30, 70, 180), (190, 30, 30), (120, 60, 160), (200, 120, 20)
text(3, 127, "ゲイン・音量調整 TEST / DEBUG: ビット深度・リレー動作・精度  Gain and volume control: bit depth, relay operations, accuracy", 2.2, INK, "la", True)
text(3, 123.6, "Python による設計計算 (SPICE・実機測定ではありません)。仮定: デジタル 32bit、リレー 1000 万回、1 日 1000 ステップ。音量は 0〜−90dB。 Python calculations with assumed 32-bit path and 10-million-operation relays.", 1.2, GRY)
mx, my = plot(8, 72, 62, 108, 0, 90, 14, 33, False, "① 音量 (減衰量) とビット深度 (bit)  Effective bits vs volume attenuation", "音量を下げた量 (dB、1dB 刻み)", "bit")
curve(mx, my, [(a, c["vol_bits"](a, "analog")) for a in range(0, 91)], GR)
curve(mx, my, [(a, c["vol_bits"](a, "digital")) for a in range(0, 91)], RD)
curve(mx, my, [(a, c["vol_bits"](a, "mixed")) for a in range(0, 91)], BL)
line([(mx(0), my(24)), (mx(90), my(24))], (150, 150, 150), int(LW * .6))
text(mx(89), my(24) + 1.5, "24bit 音源", 1.0, GRY, "rm")
legend(12, 106, [("ANALOG: 32bit のまま", GR, False), ("DIGITAL: −60dB で %.0fbit・−90dB で %.0fbit" % (c["vol_bits"](60, "digital"), c["vol_bits"](90, "digital")), RD, False), ("ANALOG+DIGITAL: 最小 %.1fbit" % c["vol_bits"](5, "mixed"), BL, False)])
mx, my = plot(70, 72, 124, 108, 0, 90, 0, 8, False, "② 1 ステップで動くリレーの数 (音量)  Relays toggled per step", "音量を下げた量 (dB)", "個")
for a in range(90):
    ta = sum(x != y for x, y in zip(c["vol_analog_state"](a), c["vol_analog_state"](a + 1)))
    tm = sum(x != y for x, y in zip(c["vol_mixed_state"](a), c["vol_mixed_state"](a + 1)))
    d.rectangle([*P(mx(a + 0.05), my(ta)), *P(mx(a + 0.5), my(0))], fill=RD)
    d.rectangle([*P(mx(a + 0.5), my(tm)), *P(mx(a + 0.95), my(0))], fill=BL)
legend(76, 106, [("ANALOG (最大 7 個が同時に動く)", RD, False), ("ANALOG+DIGITAL (最大 4 個)", BL, False)])
mx, my = plot(132, 72, 192, 108, 100, 5000, 1, 1000, True, "③ リレー寿命 (年) と 1 日のステップ数 (音量)  Relay life vs steps per day", "1 日のステップ数", "年")
for fn, col in ((c["vol_analog_state"], RD), (c["vol_mixed_state"], BL)):
    t, _ = c["vol_toggles"](fn)
    curve(mx, my, [(n, min(1000, c["relay_years"](t, n))) for n in (100, 200, 500, 1000, 2000, 5000)], col)
legend(138, 106, [("ANALOG", RD, False), ("ANALOG+DIGITAL", BL, False)])
text(6, 62, "結果 (全文は下の 8 言語の説明)  Results (full text in 8 languages below)", 1.5, INK, "la", True)
ta, tamax = c["vol_toggles"](c["vol_analog_state"]); tm, tmmax = c["vol_toggles"](c["vol_mixed_state"])
rows = ["TEST 1 [不具合]: 音量を DIGITAL だけで下げると、−40dB で %.1fbit、−60dB で %.0fbit (24bit 音源に不足)、−90dB で %.0fbit → 音量は ANALOG か ANALOG+DIGITAL (常に %.1fbit 以上) を推奨。ゲイン (0〜+18dB) は DIGITAL でも %.1fbit 残る。" % (c["vol_bits"](40, "digital"), c["vol_bits"](60, "digital"), c["vol_bits"](90, "digital"), c["vol_bits"](5, "mixed"), c["bits"](18, "digital")),
        "TEST 2 [不具合]: ANALOG の 1dB 刻みは、境目で最大 %d 個のリレーが同時に動き (音量)、ゲインが一瞬飛ぶ → 修正: メイク・ビフォア・ブレイク + 3ms ミュート。" % tamax,
        "TEST 3: 1 日 1000 ステップの音量操作でのリレー寿命は、ANALOG が約 %.0f 年、ANALOG+DIGITAL が約 %.0f 年。" % (c["relay_years"](ta, 1000), c["relay_years"](tm, 1000)),
        "TEST 4: 1dB 微調整の精度は 0.1%% 薄膜抵抗で約 %.2fdB、1%% だと約 %.2fdB → 0.1%% 薄膜を採用。" % (c["step_error_db"](0.001), c["step_error_db"](0.01))]
y = 59.5
for r_ in rows:
    import textwrap
    for ln in textwrap.wrap(r_, 90):
        text(6, y, ln, 1.05, INK, "la"); y -= 2.0
    y -= 0.4
img = img.resize((W * S // 2, H * S // 2), Image.LANCZOS)
out = SDIR + r"\amp_gain3_sim.jpg"
img.save(out, "JPEG", quality=92, dpi=(300, 300)); print(out, round(y, 1))
